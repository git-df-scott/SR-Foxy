#!/usr/bin/env python3
"""Finite full-ring audit of mixed basis changes and possible iota structures.

No geometric iota map is supplied by HFK Calculator. This script quantifies
over all homogeneous algebraic maps satisfying the necessary iota axioms on
the identified small complex. A universal result requires every diagonal
case and every basis vector of the admissible off-diagonal space to pass.
"""
import argparse
import hashlib
import json
from pathlib import Path


def xor(*items):
    out=set()
    for item in items:out.symmetric_difference_update(item)
    return out


def comp(first,second,skew_second=False):
    out=set()
    for i,j,a,b in first:
        for k,l,c,d in second:
            if j!=k:continue
            if skew_second:term=(i,l,b+c,a+d)
            else:term=(i,l,a+c,b+d)
            if term in out:out.remove(term)
            else:out.add(term)
    return out


def possible(src,dst,degree=0,skew=False):
    out=[]
    for i,(Ai,Mi) in src.items():
        if skew:Ai,Mi=-Ai,Mi-2*Ai
        for j,(Aj,Mj) in dst.items():
            twice=Mj-Mi-degree
            if twice%2:continue
            a=twice//2;b=Ai-Aj+a
            if a>=0 and b>=0:out.append((i,j,a,b))
    return out


def boundary(P,ds,dt,skew=False):
    return xor(comp(P,dt),comp(ds,P,skew))


def linear_span(columns):
    pivots={};kernel=[]
    for n,column in enumerate(columns):
        row=set(column);comb=1<<n
        while row:
            p=max(row)
            if p not in pivots:pivots[p]=(row,comb);break
            r,c=pivots[p];row^=r;comb^=c
        if not row:kernel.append(comb)
    def reduce(row):
        row=set(row);comb=0
        # Keep unreducible coordinates and continue: this is the linear
        # quotient remainder, not an early-exit membership test.
        residual=set()
        while row:
            p=max(row)
            if p in pivots:r,c=pivots[p];row^=r;comb^=c
            else:row.remove(p);residual.add(p)
        return residual,comb
    return reduce,kernel


def combine(columns,mask):
    return xor(*(c for i,c in enumerate(columns) if mask>>i&1))


def cycle_basis(src,dst,ds,dt,degree=0,skew=False):
    variables=possible(src,dst,degree,skew)
    images=[boundary({t},ds,dt,skew) for t in variables]
    _,kernel=linear_span(images)
    result=[{t for j,t in enumerate(variables) if mask>>j&1} for mask in kernel]
    assert all(not boundary(P,ds,dt,skew) for P in result)
    return result


def derivative(d,variable):
    return {(i,j,a-1,b) if variable==0 else (i,j,a,b-1)
            for i,j,a,b in d if (a if variable==0 else b)%2}


def diagonal_iotas(g,d):
    cycles=cycle_basis(g,g,d,d,skew=True)
    assert len(cycles)<20,'Explicit diagonal enumeration too large'
    rhs=xor({(i,i,0,0) for i in g},comp(derivative(d,1),derivative(d,0)))
    assert not possible(g,g,degree=1),'Diagonal homotopy terms must be included'
    good=[]
    for mask in range(1<<len(cycles)):
        I=combine(cycles,mask)
        if comp(I,I,True)==rhs:good.append(I)
    return good,{'cycle_dimension':len(cycles),'enumerated':1<<len(cycles),'solutions':len(good)}


def canonical_model():
    # E = figure-eight box plus its free generator; two further boxes are
    # centred at A=-1,+1 and delta=-2.
    g={0:(0,0),1:(0,0),2:(0,0),3:(1,1),4:(-1,-1),
       5:(-1,-3),6:(-1,-3),7:(0,-2),8:(-2,-4),
       9:(1,-1),10:(1,-1),11:(2,0),12:(0,-2)}
    d=set()
    for a,bottom,b,c in [(0,2,3,4),(5,6,7,8),(9,10,11,12)]:
        d|={(a,b,1,0),(a,c,0,1),(b,bottom,0,1),(c,bottom,1,0)}
    old_images={0:[5],1:[1],2:[1,10],3:[6],4:[9],5:[0],6:[0,4],7:[3],8:[2],
                9:[7],10:[7,12],11:[8],12:[11]}
    T={(i,j,0,0) for i,js in old_images.items() for j in js}
    return g,d,T


def run(output):
    if Path(output).exists():raise FileExistsError(output)
    cp=Path('results/chain_map_filter_wider.json');mp=Path('results/mixed_lift_audit.json')
    raw=json.loads(cp.read_text())['source_complexes'][1]
    oldg={int(i):tuple(v) for i,v in raw['generators'].items()};oldd=set(map(tuple,raw['arrows']))
    mixed=json.loads(mp.read_text())['results'][1]['completions']
    result={'status':'EXACT_ALGEBRAIC_IOTA_AUDIT_NOT_A_SLICE_CERTIFICATE','inputs_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [cp,mp]},
        'ring':'F2[U,V]','mixed_gauges':[],'cases':[],
        'limitations':'Conditional on the previously audited minimal-complex lifting argument and correct HFK Calculator data. No geometric iota was computed. The universal linear checks, if successful, avoid selecting an unverified iota. Local equivalence is not smooth concordance.'}
    # First remove ALL mixed differentials by a homogeneous basis change
    # T=Id+X, with X divisible by UV and X^2=0.
    xs=[t for t in possible(oldg,oldg) if t[2]>0 and t[3]>0]
    cols=[boundary({x},oldd,oldd) for x in xs];solve,_=linear_span(cols)
    identity={(i,i,0,0) for i in oldg}
    for row in mixed:
        m=set(map(tuple,row['mixed_terms']));res,mask=solve(m);assert not res
        X={x for j,x in enumerate(xs) if mask>>j&1};T=xor(identity,X)
        assert not comp(X,X) and comp(T,T)==identity
        assert comp(comp(T,xor(oldd,m)),T)==oldd
        result['mixed_gauges'].append({'mask':row['free_mask'],'X':sorted(X)})
    g,d,T=canonical_model()
    assert not comp(d,d) and comp(T,oldd)==comp(d,T)
    # Verify that the constant change of basis has full rank independently
    # of the differential equation.
    _,ker=linear_span([{j for i,j,a,b in T if i==k} for k in g]);assert not ker
    for i,j,a,b in T:assert g[i]==oldg[j]
    result.update(canonical_generators=g,canonical_differential=sorted(d),canonical_to_original=sorted(T))
    eg={i:v for i,v in g.items() if i<5};bg={i:v for i,v in g.items() if i>=5}
    ed={t for t in d if t[0]<5};bd=d-ed
    assert not possible(eg,bg,skew=True)
    ies,estat=diagonal_iotas(eg,ed);ibs,bstat=diagonal_iotas(bg,bd)
    assert ies and ibs
    result['diagonal_enumeration']={'E':estat,'B':bstat}
    Qbasis=cycle_basis(bg,eg,bd,ed,skew=True)
    Xbasis=cycle_basis(bg,eg,bd,ed)
    Hvars=possible(bg,eg,degree=1)
    Hcols=[boundary({t},bd,ed) for t in Hvars];Hsolve,_=linear_span(Hcols)
    Yvars=possible(bg,eg,degree=1,skew=True)
    Ycols=[boundary({t},bd,ed,True) for t in Yvars]
    result['spaces']={'Q_cycle_dimension':len(Qbasis),'X_cycle_dimension':len(Xbasis),'H_variables':len(Hvars),'Y_variables':len(Yvars)}
    for ie_no,Ie in enumerate(ies):
        for ib_no,Ib in enumerate(ibs):
            square_cross=lambda Q:xor(comp(Q,Ie,True),comp(Ib,Q,True))
            residuals=[Hsolve(square_cross(Q))[0] for Q in Qbasis]
            _,admissible=linear_span(residuals)
            corrections=[xor(comp(Ib,X),comp(X,Ie,True)) for X in Xbasis]+Ycols
            Psolve,_=linear_span(corrections)
            case={'E_index':ie_no,'B_index':ib_no,'Ie':sorted(Ie),'Ib':sorted(Ib),'admissible_Q_dimension':len(admissible),'basis_checks':[]}
            for basis_mask in admissible:
                Q=combine(Qbasis,basis_mask);r,hmask=Hsolve(square_cross(Q));assert not r
                H={t for j,t in enumerate(Hvars) if hmask>>j&1}
                assert square_cross(Q)==boundary(H,bd,ed)
                residual,solution=Psolve(Q)
                check={'Q':sorted(Q),'square_homotopy':sorted(H),'projection_exists':not residual}
                if not residual:
                    X=combine(Xbasis,solution & ((1<<len(Xbasis))-1))
                    Y={t for j,t in enumerate(Yvars) if solution>>(len(Xbasis)+j)&1}
                    assert not boundary(X,bd,ed)
                    assert xor(Q,comp(Ib,X),comp(X,Ie,True))==boundary(Y,bd,ed,True)
                    check.update(projection_off_diagonal=sorted(X),projection_homotopy=sorted(Y))
                else:check['unmatched_remainder']=sorted(residual)
                case['basis_checks'].append(check)
            case['all_admissible_Q_have_projection']=all(c['projection_exists'] for c in case['basis_checks'])
            result['cases'].append(case)
    result['all_cases_pass']=all(c['all_admissible_Q_have_projection'] for c in result['cases'])
    result['complete']=True
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'mixed_gauges':len(result['mixed_gauges']),'diagonal':result['diagonal_enumeration'],'spaces':result['spaces'],
        'cases':[(c['admissible_Q_dimension'],c['all_admissible_Q_have_projection']) for c in result['cases']],'all_cases_pass':result['all_cases_pass']}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output');run(p.parse_args().output)
