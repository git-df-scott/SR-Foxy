"""Small-diagram Kauffman bracket state sum, exact integers. Exponential in crossings."""
from collections import defaultdict
from math import comb
from pd_algebra import structure

def jones_A(pd):
    if not pd:return {0:1}
    labels=sorted({a for q in pd for a in q});idx={a:i for i,a in enumerate(labels)}
    qs=[[idx[a] for a in q] for q in pd];n=len(qs);N=len(labels)
    hist=defaultdict(int)
    for state in range(1<<n):
        parent=list(range(N));k=N
        def find(a):
            while parent[a]!=a:
                parent[a]=parent[parent[a]];a=parent[a]
            return a
        def union(a,b):
            nonlocal k
            a,b=find(a),find(b)
            if a!=b:parent[b]=a;k-=1
        for i,(a,b,c,d) in enumerate(qs):
            if (state>>i)&1:union(a,d);union(b,c)
            else:union(a,b);union(c,d)
        hist[(n-2*state.bit_count(),k-1)]+=1
    ans=defaultdict(int)
    w=sum(structure(pd)['signs'])
    for (exp,loops),count in hist.items():
        sign=(-1)**((loops+w)%2)
        for j in range(loops+1):ans[exp+2*loops-4*j+3*w]+=sign*count*comb(loops,j)
    return dict(sorted((e,c) for e,c in ans.items() if c))
