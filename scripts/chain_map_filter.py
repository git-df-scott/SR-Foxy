#!/usr/bin/env python3
"""Necessary-chain-map experiment over F2[U,V]/(UV), with exact controls.

Finite homogeneous chain-map equations plus injectivity after U=V=0.
SAT is only a necessary-test pass. Mathematical application requires the
two-variable functorial interpretation described in the session report.
UNSAT can sometimes be certified by a universal kernel vector using only
GF(2) row reduction; that witness is independent of the SAT solver.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import time
import snappy
import z3


def monomial(source_grade, target_grade, differential=False):
    ai,mi=source_grade;aj,mj=target_grade
    twice_a=mj-mi+int(differential)
    if twice_a%2:return None
    a=twice_a//2;b=ai-aj+a
    return (a,b) if a>=0 and b>=0 and a*b==0 else None


def product(a,b):
    u,v=a[0]+b[0],a[1]+b[1]
    return (u,v) if not u*v else None


def toggle(d,key,value=1):
    d[key]=d.get(key,0)^value
    if not d[key]:del d[key]


def complex_data(pd):
    h=snappy.Link(pd).knot_floer_homology(complex=True)
    g={int(k):tuple(map(int,v)) for k,v in h['generators'].items()}
    arrows=[]
    for (i,j),c in h['differentials'].items():
        if c%2:
            m=monomial(g[i],g[j],True)
            assert m is not None and m!=(0,0)
            arrows.append((int(i),int(j),*m))
    # Independent D^2 check in the quotient ring.
    squared={}
    for i,j,a,b in arrows:
        for k,l,c,d in arrows:
            if j==k and (m:=product((a,b),(c,d))) is not None:
                toggle(squared,(i,l,*m))
    assert not squared
    return {'generators':g,'arrows':arrows,'total_rank':h['total_rank']}


def build_problem(source,target,include_injection=True):
    variables=[];by_pair={};equations=defaultdict(set)
    for i,gi in source['generators'].items():
        for j,gj in target['generators'].items():
            m=monomial(gi,gj)
            if m is not None:
                by_pair[i,j]=len(variables);variables.append((i,j,*m))
    def term(key,v):
        if v in equations[key]:equations[key].remove(v)
        else:equations[key].add(v)
    for v,(i,j,a,b) in enumerate(variables):
        for k,l,c,d in target['arrows']:
            if j==k and (m:=product((a,b),(c,d))) is not None:term((i,l,*m),v)
        for k,l,c,d in source['arrows']:
            if l==i and (m:=product((a,b),(c,d))) is not None:term((k,j,*m),v)
    rows=[sorted(v) for k,v in sorted(equations.items()) if v]
    if not include_injection:return variables,rows,[]
    grades=defaultdict(list)
    for i,g in source['generators'].items():grades[g].append(i)
    injection=[]
    for grade,src in sorted(grades.items()):
        dst=[j for j,g in target['generators'].items() if g==grade]
        for mask in range(1,1<<len(src)):
            vector=[src[k] for k in range(len(src)) if mask>>k&1]
            outputs=[[by_pair[i,j] for i in vector] for j in dst]
            injection.append({'grade':grade,'source_vector':vector,'outputs':outputs})
    return variables,rows,injection


def gf2_pivots(rows):
    pivots={}
    for r_index,row in enumerate(rows):
        bits=sum(1<<v for v in row);combination=1<<r_index
        while bits:
            j=bits.bit_length()-1
            if j not in pivots:
                pivots[j]=(bits,combination);break
            b,c=pivots[j];bits^=b;combination^=c
    return pivots


def rowspace_certificate(variables,pivots):
    bits=sum(1<<v for v in variables);combination=0
    while bits:
        j=bits.bit_length()-1
        if j not in pivots:return None
        b,c=pivots[j];bits^=b;combination^=c
    return [j for j in range(combination.bit_length()) if combination>>j&1]


def parity(values):
    if not values:return z3.BoolVal(False)
    ans=values[0]
    for v in values[1:]:ans=z3.Xor(ans,v)
    return ans


def check(source,target,timeout_ms=10000):
    t0=time.monotonic();variables,rows,injection=build_problem(source,target)
    pivots=gf2_pivots(rows)
    result={'variables':len(variables),'linear_equations':len(rows),'linear_rank':len(pivots),
            'hat_injectivity_constraints':len(injection),'source_rank':source['total_rank'],
            'target_rank':target['total_rank']}
    for constraint in injection:
        certificates=[rowspace_certificate(v,pivots) for v in constraint['outputs']]
        if all(c is not None for c in certificates):
            # Check each rowspace identity directly, separately from elimination.
            for out,indices in zip(constraint['outputs'],certificates):
                value=set()
                for k in indices:value.symmetric_difference_update(rows[k])
                assert value==set(out)
            result.update({'status':'UNSAT_UNIVERSAL_KERNEL','kernel_witness':constraint,
                           'row_combinations':certificates,'problem_variables':variables,
                           'problem_equations':rows})
            break
    else:
        solver=z3.Solver();solver.set(timeout=timeout_ms)
        vs=[z3.Bool('x'+str(i)) for i in range(len(variables))]
        for row in rows:solver.add(z3.Not(parity([vs[v] for v in row])))
        for c in injection:solver.add(z3.Or([parity([vs[v] for v in out]) for out in c['outputs']]))
        answer=solver.check();result['status']=str(answer).upper()
        if answer==z3.sat:
            model=solver.model();chosen={i for i,v in enumerate(vs) if z3.is_true(model.eval(v,model_completion=True))}
            assert all(len(chosen & set(row))%2==0 for row in rows)
            assert all(any(len(chosen & set(out))%2 for out in c['outputs']) for c in injection)
            result['map_terms']=[variables[i] for i in sorted(chosen)]
        elif answer==z3.unknown:result['reason']=solver.reason_unknown()
    result['seconds']=round(time.monotonic()-t0,3)
    return result


def check_retraction(source,target,timeout_ms=20000):
    """Search F,G,H with GF+I=dH+Hd; all maps homogeneous over R."""
    t0=time.monotonic()
    # A retraction implies hat injectivity. Do not enumerate the exponentially
    # many nonzero target vectors when constructing the reverse map G.
    fv,fr,_=build_problem(source,target,False);gv,gr,_=build_problem(target,source,False)
    hv=[]
    for i,gi in source['generators'].items():
        for j,gj in source['generators'].items():
            if (m:=monomial(gi,gj,-1)) is not None:hv.append((i,j,*m))
    fs=[z3.Bool('f'+str(i)) for i in range(len(fv))]
    gs=[z3.Bool('g'+str(i)) for i in range(len(gv))]
    hs=[z3.Bool('h'+str(i)) for i in range(len(hv))]
    solver=z3.Solver();solver.set(timeout=timeout_ms)
    for row in fr:solver.add(z3.Not(parity([fs[v] for v in row])))
    for row in gr:solver.add(z3.Not(parity([gs[v] for v in row])))
    eq=defaultdict(list)
    for i in source['generators']:eq[i,i,0,0].append(z3.BoolVal(True))
    for f,(i,j,a,b) in enumerate(fv):
        for g,(k,l,c,d) in enumerate(gv):
            if j==k and (m:=product((a,b),(c,d))) is not None:eq[i,l,*m].append(z3.And(fs[f],gs[g]))
    for h,(i,j,a,b) in enumerate(hv):
        for k,l,c,d in source['arrows']:
            m=product((a,b),(c,d))
            if m is None:continue
            if j==k:eq[i,l,*m].append(hs[h])
            if l==i:eq[k,j,*m].append(hs[h])
    for values in eq.values():solver.add(z3.Not(parity(values)))
    answer=solver.check()
    result={'status':str(answer).upper(),'F_variables':len(fv),'G_variables':len(gv),'H_variables':len(hv),
            'linear_equations':len(fr)+len(gr),'homotopy_equations':len(eq)}
    if answer==z3.sat:
        model=solver.model()
        selected=[]
        for vs,terms in [(fs,fv),(gs,gv),(hs,hv)]:
            selected.append([terms[i] for i,v in enumerate(vs) if z3.is_true(model.eval(v,model_completion=True))])
        # Verify the actual maps using plain F2 arithmetic, not solver eval.
        def compose(first,second):
            out={}
            for i,j,a,b in first:
                for k,l,c,d in second:
                    if j==k and (m:=product((a,b),(c,d))) is not None:toggle(out,(i,l,*m))
            return out
        F,G,H=selected;ds=source['arrows'];dt=target['arrows']
        assert compose(F,dt)==compose(ds,F)
        assert compose(G,ds)==compose(dt,G)
        total=compose(F,G)
        for i in source['generators']:toggle(total,(i,i,0,0))
        for term in compose(H,ds):toggle(total,term)
        for term in compose(ds,H):toggle(total,term)
        assert not total
        result.update({'F':F,'G':G,'H':H,'plain_arithmetic_verification':True})
    elif answer==z3.unknown:result['reason']=solver.reason_unknown()
    else:result['smt2']=solver.to_smt2()
    result['seconds']=round(time.monotonic()-t0,3)
    return result


def run(target_file,output,count=0):
    if Path(output).exists():raise FileExistsError(output)
    cards=['AbeTagami_K_0_K_-1__6_3','AbeTagami_K_1']
    sources=[complex_data(json.loads(Path('data/knots/'+n+'.json').read_text())['pd_code_snappy_0indexed']) for n in cards]
    controls={'K0_identity':check(sources[0],sources[0]),'K1_identity':check(sources[1],sources[1]),
              'K0_to_K1':check(sources[0],sources[1]),'K1_to_K0':check(sources[1],sources[0])}
    assert controls['K0_identity']['status']==controls['K1_identity']['status']=='SAT'
    assert controls['K0_to_K1']['status'].startswith('UNSAT') and controls['K1_to_K0']['status'].startswith('UNSAT')
    result={'status':'CHAIN_MAP_NECESSARY_CONDITION_EXPERIMENT','ring':'F2[U,V]/(UV)',
            'source_cards':cards,'source_complexes':sources,'controls':controls,'runs':[],
            'limitations':'SAT does not imply concordance. Application of UNSAT depends on the exact two-variable functorial interpretation and correct HFK Calculator complex data.'}
    entries=json.loads(Path(target_file).read_text())['candidates']
    if count:entries=entries[:count]
    for r in entries:
        target=complex_data(r['endpoint_pd'])
        own=check(sources[0],target);other=check(sources[1],target)
        row={'source_index':r['index'],'target_pd':r['endpoint_pd'],'target_complex':target,
             'fibered':r['hfk_check']['fibered'],'K0_to_J':own,'K1_to_J':other}
        result['runs'].append(row)
        Path(output).write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({'index':r['index'],'K0':own['status'],'K1':other['status'],'variables':other['variables']}),flush=True)
        assert own['status']=='SAT','Own-source control failed; stop using this filter'
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('targets');p.add_argument('output');p.add_argument('--count',type=int,default=0)
    a=p.parse_args();run(a.targets,a.output,a.count)
