#!/usr/bin/env python3
"""Independent finite-field operator check, with exhaustive off-diagonal cases.

No imports from the generating audit. Polynomial maps act on a truncated
F2[U,V] module as binary matrices; truncation is above every exponent that
can occur in the checked identities, so checking generator images is exact.
"""
import argparse
import hashlib
import json
from pathlib import Path

N=5
DIM=13*N*N


def unit(i):return 1<<(i*N*N)


def operator(terms,skew=False):
    cols=[0]*DIM
    for source,target,a,b in terms:
        assert 0<=a<N and 0<=b<N
        for u in range(N):
            for v in range(N):
                x,y=(v+a,u+b) if skew else (u+a,v+b)
                if x<N and y<N:cols[source*N*N+u*N+v]^=1<<(target*N*N+x*N+y)
    return cols


def apply(cols,vector):
    result=0
    while vector:
        low=vector & -vector;vector^=low;result^=cols[low.bit_length()-1]
    return result


def plus(A,B):return [a^b for a,b in zip(A,B)]


def rank(vectors):
    basis={}
    for v in vectors:
        while v:
            k=v.bit_length()-1
            if k in basis:v^=basis[k]
            else:basis[k]=v;break
    return len(basis)


def image_columns(T,domain):
    return sum(T[i*N*N]<<(n*DIM) for n,i in enumerate(domain))


def boundary_vector(T,D,domain):
    return sum((apply(D,T[i*N*N])^apply(T,D[i*N*N]))<<(n*DIM) for n,i in enumerate(domain))


def allowed(src,dst,degree=0,skew=False):
    # Compute powers from gr_U=M and gr_V=M-2A independently of the audit's
    # Alexander-grading formula.
    terms=[]
    for i,(a,m) in src.items():
        su,sv=m,m-2*a
        if skew:su,sv=sv,su
        for j,(b,n) in dst.items():
            twice_u=n-su-degree;twice_v=n-2*b-sv-degree
            if twice_u%2 or twice_v%2:continue
            u,v=twice_u//2,twice_v//2
            if u>=0 and v>=0:terms.append((i,j,u,v))
    return terms


def derivatives(terms):
    return (operator([(i,j,a-1,b) for i,j,a,b in terms if a%2]),
            operator([(i,j,a,b-1) for i,j,a,b in terms if b%2]))


def enumerate_diagonal(g,d):
    choices=allowed(g,g,skew=True);assert all(a==b==0 for i,j,a,b in choices)
    assert not allowed(g,g,degree=1)
    D=operator(d);Phi,Psi=derivatives(d)
    rhs={}
    for i in g:
        v=unit(i)^apply(Phi,Psi[i*N*N]);scalar=0
        while v:
            bit=v & -v;v^=bit;k=bit.bit_length()-1
            assert k%(N*N)==0;scalar^=1<<(k//(N*N))
        rhs[i]=scalar
    good=[]
    for mask in range(1<<len(choices)):
        matrix=[0]*13;terms=[]
        for k,t in enumerate(choices):
            if mask>>k&1:matrix[t[0]]^=1<<t[1];terms.append(t)
        if any(apply(matrix,matrix[i])!=rhs[i] for i in g):continue
        T=operator(terms,True)
        if not boundary_vector(T,D,list(g)):good.append(tuple(sorted(terms)))
    return good,1<<len(choices)


def run(path,output):
    if Path(output).exists():raise FileExistsError(output)
    audit=json.loads(Path(path).read_text());assert audit['complete'] and audit['all_cases_pass']
    for p,digest in audit['inputs_sha256'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==digest
    raw=json.loads(Path('results/chain_map_filter_wider.json').read_text())['source_complexes'][1]
    oldg={int(i):tuple(v) for i,v in raw['generators'].items()};oldd=raw['arrows'];D0=operator(oldd)
    all_m=allowed(oldg,oldg,degree=-1);mixed=[t for t in all_m if t[2]>0 and t[3]>0]
    assert len(mixed)==18 and all(a+b==3 for i,j,a,b in mixed)
    # All mixed maps run from delta=-2 to delta=0, so their products vanish.
    assert not any(j==k for i,j,a,b in mixed for k,l,c,d in mixed)
    bcols=[boundary_vector(operator([t]),D0,list(oldg)) for t in mixed]
    dimension=len(mixed)-rank(bcols);assert dimension==8
    stored=json.loads(Path('results/mixed_lift_audit.json').read_text())['results'][1]['completions']
    by_mask={r['free_mask']:r['mixed_terms'] for r in stored}
    assert len({tuple(sorted(map(tuple,r))) for r in by_mask.values()})==1<<dimension
    assert len(audit['mixed_gauges'])==1<<dimension
    assert {r['mask'] for r in audit['mixed_gauges']}==set(by_mask)
    identity=[(i,i,0,0) for i in oldg]
    for row in audit['mixed_gauges']:
        m=by_mask[row['mask']];T=operator(identity+row['X']);D=operator(oldd+m)
        assert set(map(tuple,m))<=set(mixed)
        assert set(map(tuple,row['X']))<=set(allowed(oldg,oldg))
        # Each T entry has exponent <=1; D entries <=2. TDT exponents <=4<N.
        assert all(a<=1 and b<=1 for i,j,a,b in row['X'])
        for i in oldg:
            assert not apply(D,D[i*N*N])
            assert apply(T,T[i*N*N])==unit(i)
            assert apply(T,apply(D,T[i*N*N]))==D0[i*N*N]
    g={int(i):tuple(v) for i,v in audit['canonical_generators'].items()};d=audit['canonical_differential'];D=operator(d)
    T=operator(audit['canonical_to_original']);assert rank([T[i*N*N] for i in g])==13
    for i,j,a,b in audit['canonical_to_original']:assert a==b==0 and g[i]==oldg[j]
    for i in g:assert apply(D0,T[i*N*N])==apply(T,D[i*N*N])
    eg={i:v for i,v in g.items() if i<5};bg={i:v for i,v in g.items() if i>=5}
    ed=[t for t in d if t[0]<5];bd=[t for t in d if t[0]>=5]
    E,countE=enumerate_diagonal(eg,ed);B,countB=enumerate_diagonal(bg,bd)
    assert set(E)=={tuple(map(tuple,c['Ie'])) for c in audit['cases']}
    assert set(B)=={tuple(map(tuple,c['Ib'])) for c in audit['cases']}
    assert {(e,b) for e in E for b in B}=={(tuple(map(tuple,c['Ie'])),tuple(map(tuple,c['Ib']))) for c in audit['cases']}
    assert not allowed(eg,bg,skew=True)
    qvars=allowed(bg,eg,skew=True)
    qdim=len(qvars)-rank([boundary_vector(operator([t],True),D,list(bg)) for t in qvars])
    assert qdim==10
    Phi,Psi=derivatives(d);total=0
    for case in audit['cases']:
        Ie=operator(case['Ie'],True);Ibase=operator(case['Ie']+case['Ib'],True)
        Pbase=operator([(i,i,0,0) for i in eg]);checks=case['basis_checks']
        assert len(checks)==qdim
        Qs=[operator(c['Q'],True) for c in checks]
        assert all(set(map(tuple,c['Q']))<=set(qvars) for c in checks)
        assert rank([image_columns(Q,list(bg)) for Q in Qs])==qdim
        assert all(not boundary_vector(Q,D,list(bg)) for Q in Qs)
        Xs=[operator(c['projection_off_diagonal']) for c in checks]
        Ys=[operator(c['projection_homotopy'],True) for c in checks]
        Hs=[operator(c['square_homotopy']) for c in checks]
        for c,X in zip(checks,Xs):
            assert set(map(tuple,c['projection_off_diagonal']))<=set(allowed(bg,eg))
            assert set(map(tuple,c['projection_homotopy']))<=set(allowed(bg,eg,degree=1,skew=True))
            assert set(map(tuple,c['square_homotopy']))<=set(allowed(bg,eg,degree=1))
            assert not boundary_vector(X,D,list(bg))
        I=Ibase[:];P=Pbase[:];Y=[0]*DIM;H=[0]*DIM;previous=0
        for n in range(1<<qdim):
            gray=n^(n>>1)
            if n:
                k=(gray^previous).bit_length()-1
                I=plus(I,Qs[k]);P=plus(P,Xs[k]);Y=plus(Y,Ys[k]);H=plus(H,Hs[k])
            previous=gray
            for i in g:
                square=apply(I,I[i*N*N])
                rhs=unit(i)^apply(Phi,Psi[i*N*N])^apply(D,H[i*N*N])^apply(H,D[i*N*N])
                assert square==rhs
                lhs=apply(P,I[i*N*N])^apply(Ie,P[i*N*N])
                rhs=apply(D,Y[i*N*N])^apply(Y,D[i*N*N])
                assert lhs==rhs
                if i in eg:assert P[i*N*N]==unit(i) and I[i*N*N]==Ie[i*N*N]
            total+=1
    result={'status':'INDEPENDENT_EXHAUSTIVE_OPERATOR_VERIFICATION_PASSED','audit':path,
        'sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'truncation_per_variable':N,
        'largest_possible_exponent_in_checked_words':4,'mixed_dimension':dimension,'mixed_gauges_checked':len(audit['mixed_gauges']),
        'diagonal_maps_bruteforced':{'E':countE,'B':countB},'diagonal_solutions':{'E':len(E),'B':len(B)},
        'off_diagonal_cycle_dimension':qdim,'full_iota_projection_cases_checked':total,
        'limitations':'Algebraic result conditional on the original complex data and full-ring lifting argument. This is not a formal verification of topology or a slice certificate.'}
    Path(output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('audit');p.add_argument('output');a=p.parse_args();run(a.audit,a.output)
