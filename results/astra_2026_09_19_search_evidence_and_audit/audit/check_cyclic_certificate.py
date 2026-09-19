#!/usr/bin/env python3
"""Standard-library verification of saved cyclic-cover integer certificates.

Verifies the declared PD-to-Wirtinger relators via independent arc-component
traversal, rebuilds the cover relation matrix, verifies U*M*V = D and the
unimodularity of U,V, and independently computes the mod-5 first Betti
number. No SymPy, Spherogram, SnapPy, or Regina imports.
"""
import argparse,copy,json
from collections import defaultdict
from pathlib import Path

def check(ok,msg):
    if not ok:raise ValueError(msg)

def product(A,B):
    bt=list(zip(*B))
    return [[sum(x*y for x,y in zip(row,col)) for col in bt] for row in A]

def determinant(A):
    A=[r[:] for r in A];n=len(A);sign=1;denom=1
    if n==0:return 1
    for k in range(n-1):
        at=next((i for i in range(k,n) if A[i][k]),None)
        if at is None:return 0
        if at!=k:A[k],A[at]=A[at],A[k];sign=-sign
        p=A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                v=p*A[i][j]-A[i][k]*A[k][j]
                check(v%denom==0,'Bareiss division is not exact');A[i][j]=v//denom
        for i in range(k+1,n):A[i][k]=0
        denom=p
    return sign*A[-1][-1]

def rank_mod(A,p):
    A=[[x%p for x in row] for row in A];rank=0;pivots=[]
    for j in range(len(A[0])):
        i=next((i for i in range(rank,len(A)) if A[i][j]),None)
        if i is None:continue
        A[rank],A[i]=A[i],A[rank];inv=pow(A[rank][j],-1,p)
        A[rank]=[(inv*x)%p for x in A[rank]]
        for k in range(rank+1,len(A)):
            if A[k][j]:
                mult=A[k][j];A[k]=[(x-mult*y)%p for x,y in zip(A[k],A[rank])]
        pivots.append(j);rank+=1
        if rank==len(A):break
    return rank,pivots

def check_pd(record):
    pd=record['pd'];occ=defaultdict(list)
    for c,row in enumerate(pd):
        check(len(row)==4,'PD valence')
        for p,e in enumerate(row):occ[e].append((c,p))
    check(all(len(v)==2 for v in occ.values()),'PD edge multiplicity')
    edge={}
    for x,y in occ.values():edge[x]=y;edge[y]=x
    def connected_arc(start):
        seen=set();stack=[start]
        while stack:
            x=stack.pop()
            if x in seen:continue
            seen.add(x);stack.append(edge[x])
            c,p=x
            if p%2:stack.append((c,(p+2)%4))
        return seen
    arcids={};representatives=[]
    for port in sorted(edge):
        if port not in arcids:
            members=connected_arc(port);representatives.append(min(members))
            for x in members:arcids[x]=len(representatives)
    check(len(representatives)==record['presentation']['generator_count'],'Generator count')
    incoming=set();start=min(edge);x=start
    while x not in incoming:
        incoming.add(x);c,p=x;x=edge[c,(p+2)%4]
    check(x==start and len(incoming)==2*len(pd),'One oriented knot expected')
    rels=[]
    for c,row in enumerate(pd):
        under=0 if (c,0) in incoming else 2
        over_in=1 if (c,1) in incoming else 3
        # Relative order of incoming tangent rays determines crossing sign.
        s=1 if (under-over_in)%4==1 else -1
        over=arcids[c,1]
        rels.append([-s*over,arcids[c,under],s*over,-arcids[c,(under+2)%4]])
    check(rels==record['presentation']['relators'],'PD relators disagree')
    return rels

def verify(record):
    rels=check_pd(record);k=record['degree'];n=record['presentation']['generator_count']
    cols=[(level,g) for level in range(k) for g in range(n) if g!=0 or level==k-1]
    check([list(c) for c in cols]==record['non_tree_edges'],'Cover basis')
    indices={x:i for i,x in enumerate(cols)};M=[]
    for start in range(k):
        for word in rels:
            row=[0]*len(cols);level=start
            for signed in word:
                if signed<0:level=(level-1)%k
                c=(level,abs(signed)-1)
                if c in indices:row[indices[c]]+=1 if signed>0 else -1
                if signed>0:level=(level+1)%k
            check(level==start,'Relator lift must close');M.append(row)
    check(M==record['relation_matrix'],'Cover relation matrix')
    U=record['left_unimodular'];V=record['right_unimodular'];D=product(product(U,M),V)
    diag=record['smith_diagonal']
    check(all(D[i][j]==(diag[i] if i==j else 0) for i in range(len(M)) for j in range(len(cols))),'Smith product')
    check(abs(determinant(U))==1 and abs(determinant(V))==1,'Unimodular transformations')
    nonzero=[abs(x) for x in diag if x]
    check(all(y%x==0 for x,y in zip(nonzero,nonzero[1:])),'Divisibility order')
    factors=[abs(x) for x in diag if abs(x)>1]+[0]*(len(cols)-len(nonzero))
    check(factors==record['h1_elementary_divisors'],'Homology factors')
    rank,pivots=rank_mod(M,5);betti=len(cols)-rank
    check(betti==sum(v%5==0 for v in factors),'Independent mod-5 rank')
    return {'node':record.get('node'),'h1':factors,'mod5_betti':betti,'matrix_rank_mod5':rank,'pivots':pivots,'status':'PASS'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('certificates',type=Path,nargs='+');ap.add_argument('--output',type=Path);a=ap.parse_args()
    results=[];rejected=0
    for path in a.certificates:
        record=json.loads(path.read_text());results.append(verify(record))
        for mutation in ['matrix','left','right','homology','pd']:
            bad=copy.deepcopy(record)
            if mutation=='matrix':bad['relation_matrix'][0][0]+=1
            if mutation=='left':bad['left_unimodular'][0][0]+=1
            if mutation=='right':bad['right_unimodular'][0][0]+=1
            if mutation=='homology':bad['h1_elementary_divisors'][0]+=1
            if mutation=='pd':bad['pd'][0][0]=999999
            try:verify(bad)
            except ValueError:rejected+=1
            else:raise ValueError('Corrupt certificate accepted: '+mutation)
    out={'status':'PASS','results':results,'mutated_certificates_rejected':rejected,'libraries':'Python standard library only'}
    if a.output:a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
