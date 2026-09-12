#!/usr/bin/env python3
"""Enumerate homogeneous full-ring differentials lifting the stored K1 quotient.

These are abstract algebraic completions, not computed knot Floer complexes.
The actual mixed differential is unknown; no completion is called geometric.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import z3
from chain_map_filter import parity,toggle,gf2_pivots
from filter_retractions import restore


def terms(source,target,degree=0):
    out=[]
    for i,(ai,mi) in source.items():
        for j,(aj,mj) in target.items():
            twice=mj-mi-degree
            if twice%2:continue
            a=twice//2;b=ai-aj+a
            if a>=0 and b>=0:out.append((i,j,a,b))
    return out


def compose(first,second):
    out={}
    for i,j,a,b in first:
        for k,l,c,d in second:
            if j==k:toggle(out,(i,l,a+c,b+d))
    return out


def unknot_retract(g,d):
    u={0:(0,0)};fv=terms(u,g);gv=terms(g,u)
    fs=[z3.Bool('f'+str(i)) for i in range(len(fv))]
    gs=[z3.Bool('g'+str(i)) for i in range(len(gv))]
    eq=defaultdict(list);solver=z3.Solver()
    for v,(i,j,a,b) in enumerate(fv):
        for k,l,c,e in d:
            if j==k:eq['df',i,l,a+c,b+e].append(fs[v])
    for v,(i,j,a,b) in enumerate(gv):
        for k,l,c,e in d:
            if l==i:eq['gd',k,j,a+c,b+e].append(gs[v])
    for values in eq.values():solver.add(z3.Not(parity(values)))
    gf=defaultdict(list);gf[0,0,0,0].append(z3.BoolVal(True))
    for v,(i,j,a,b) in enumerate(fv):
        for w,(k,l,c,e) in enumerate(gv):
            if j==k:gf[i,l,a+c,b+e].append(z3.And(fs[v],gs[w]))
    for values in gf.values():solver.add(z3.Not(parity(values)))
    ans=solver.check();result={'status':str(ans).upper()}
    if ans==z3.sat:
        model=solver.model()
        F=[t for v,t in zip(fs,fv) if z3.is_true(model.eval(v,model_completion=True))]
        G=[t for v,t in zip(gs,gv) if z3.is_true(model.eval(v,model_completion=True))]
        assert not compose(F,d) and not compose(d,G) and compose(F,G)=={(0,0,0,0):1}
        result.update(F=F,G=G,plain_full_ring_verification=True)
    return result


def run(input_path,output):
    if Path(output).exists():raise FileExistsError(output)
    sources=list(map(restore,json.loads(Path(input_path).read_text())['source_complexes']))
    results=[]
    for n,c in enumerate(sources):
        g=c['generators'];d=c['arrows']
        mixed=[t for t in terms(g,g,-1) if t[2]>0 and t[3]>0]
        assert not compose(d,d),'Fixed arrows do not already square to zero over full ring'
        assert not any(j==k for i,j,a,b in mixed for k,l,x,y in mixed),'Mixed products require quadratic handling'
        eq=defaultdict(set)
        for v,t in enumerate(mixed):
            total=compose([t],d)
            for key in compose(d,[t]):toggle(total,key)
            for key in total:eq[key].add(v)
        rows=[sorted(v) for v in eq.values() if v];pivots=gf2_pivots(rows)
        free=[i for i in range(len(mixed)) if i not in pivots]
        completions=[]
        for mask in range(1<<len(free)):
            bits=sum(1<<j for i,j in enumerate(free) if mask>>i&1)
            for j,(row,comb) in sorted(pivots.items()):
                if (row&bits).bit_count()%2:bits^=1<<j
            chosen=[mixed[i] for i in range(len(mixed)) if bits>>i&1]
            full=d+chosen
            assert not compose(full,full)
            completions.append({'free_mask':mask,'mixed_terms':chosen,'unknot_retraction':unknot_retract(g,full)})
        entry={'knot':'K'+str(n),'mixed_variables':mixed,'linear_equations':rows,
               'equation_rank':len(pivots),'free_dimension':len(free),'count':len(completions),
               'retraction_passes':sum(r['unknot_retraction']['status']=='SAT' for r in completions),
               'completions':completions}
        results.append(entry)
        print(json.dumps({k:v for k,v in entry.items() if k not in ['mixed_variables','linear_equations','completions']}),flush=True)
    result={'status':'ABSTRACT_FULL_RING_COMPLETIONS_NOT_KNOT_IDENTIFICATIONS','input':input_path,
            'ring':'F2[U,V]','results':results,
            'limitations':'No actual mixed differential was computed. This finite enumeration is conditional on lifting the given minimal quotient basis on the same free generators. Retractions are algebraic, not slice disks; classical algebraic concordance is not detected here.'}
    Path(output).write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('output');a=p.parse_args();run(a.input,a.output)
