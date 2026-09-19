"""Exact combinatorial PD/Fox utilities. No knot-type recognition is claimed."""
from collections import defaultdict
import sympy as s

t = s.Symbol('t')
class DSU:
    def __init__(self, items): self.p = {a:a for a in items}
    def find(self,a):
        while self.p[a] != a:
            self.p[a] = self.p[self.p[a]]; a = self.p[a]
        return a
    def union(self,a,b): self.p[self.find(b)] = self.find(a)

def cycles(perm):
    unseen = set(perm); out=[]
    while unseen:
        x = a = min(unseen); cyc=[]
        while x in unseen:
            unseen.remove(x); cyc.append(x); x=perm[x]
        if x != a: raise ValueError('Not a permutation')
        out.append(cyc)
    return out

def structure(pd):
    occ=defaultdict(list)
    for i,q in enumerate(pd):
        if len(q)!=4: raise ValueError('Crossing needs four half-edges')
        for j,a in enumerate(q): occ[a].append((i,j))
    if any(len(v)!=2 for v in occ.values()): raise ValueError('Each label must occur twice')
    alpha={a:b for v in occ.values() for a,b in [v,v[::-1]]}
    strands=cycles({d:(alpha[d][0],(alpha[d][1]+2)%4) for d in alpha})
    seen=set(); outgoing=set(); edge_component={}; tours=[]
    for tour in strands:
        ed={pd[i][j] for i,j in tour}
        if ed & seen: continue
        cid=len(tours); tours.append(tour); seen|=ed; outgoing.update(tour)
        edge_component.update({a:cid for a in ed})
    faces=cycles({d:(alpha[d][0],(alpha[d][1]+1)%4) for d in alpha})
    signs=[]; oriented=[]
    for i,(a,b,c,d) in enumerate(pd):
        ui=0 if (i,0) not in outgoing else 2
        oi=1 if (i,1) not in outgoing else 3
        eps=1 if oi==(ui+1)%4 else -1
        signs.append(eps); oriented.append((pd[i][ui],b,pd[i][(ui+2)%4],eps))
    return {'alpha':alpha,'faces':faces,'outgoing':outgoing,'components':edge_component,
            'tours':tours,'signs':signs,'oriented':oriented}

def component_pd(pd,cid,st=None):
    st=st or structure(pd); ec=st['components']
    labels={a for a in ec if ec[a]==cid}; uf=DSU(labels); keep=[]
    for a,b,c,d in pd:
        u,o=ec[a]==cid,ec[b]==cid
        if u and o: keep.append((a,b,c,d))
        elif u: uf.union(a,c)
        elif o: uf.union(b,d)
    return [[uf.find(a) for a in q] for q in keep]

def fox_matrix(pd, variable=t, require_knot=True):
    if not pd: return s.zeros(0)
    st=structure(pd)
    if require_knot and len(st['tours'])!=1: raise ValueError('This routine expects one knot component')
    uf=DSU(st['components'])
    for a,b,c,d in pd: uf.union(b,d)
    roots=sorted({uf.find(a) for a in st['components']}); idx={a:i for i,a in enumerate(roots)}
    arc={a:idx[uf.find(a)] for a in st['components']}
    n=len(pd); A=s.zeros(n,len(roots))
    for row,(u,o,v,eps) in enumerate(st['oriented']):
        if eps==1:
            A[row,arc[o]]+=1-variable; A[row,arc[u]]+=variable; A[row,arc[v]]-=1
        else:
            A[row,arc[o]]+=variable-1; A[row,arc[u]]+=1; A[row,arc[v]]-=variable
    return A

def normalize(poly):
    poly=s.Poly(s.expand(poly),t)
    if poly.is_zero: return s.Integer(0)
    low=min(k[0] for k,v in poly.terms()); ans=s.expand(poly.as_expr()/t**low)
    val=ans.subs(t,1)
    if val==-1: ans=-ans
    elif val!=1: raise ValueError('Knot Alexander polynomial at 1 must be a unit')
    return ans

def alexander(pd,row=-1,col=-1):
    if not pd: return s.Integer(1)
    A=fox_matrix(pd); nr,nc=A.shape
    if nc==1: return s.Integer(1)
    if nr!=nc: raise ValueError(f'Unexpected knot Fox matrix dimensions {A.shape}')
    B=A.minor_submatrix(row%nr,col%nc)
    return normalize(B.det(method='domain-ge'))

def determinant(pd):
    if not pd: return 1
    A=fox_matrix(pd,s.Integer(-1)); nr,nc=A.shape
    if nc==1:return 1
    if nr!=nc: raise ValueError(f'Unexpected knot Fox matrix dimensions {A.shape}')
    return abs(int(A[:-1,:-1].det(method='domain-ge')))

def canonical_genus(pd):
    if not pd:return 0
    st=structure(pd); uf=DSU(st['components'])
    for i,(a,b,c,d) in enumerate(pd):
        incoming=[j for j in range(4) if (i,j) not in st['outgoing']]
        for j in incoming:
            neighbors=[k for k in [(j-1)%4,(j+1)%4] if (i,k) in st['outgoing']]
            if len(neighbors)!=1:raise ValueError('Bad oriented smoothing')
            uf.union(pd[i][j],pd[i][neighbors[0]])
    sc=len({uf.find(a) for a in st['components']})
    return (len(pd)-sc+1)//2

def linking_numbers(pd,st=None):
    st=st or structure(pd); ans=defaultdict(int); ec=st['components']
    for (a,b,c,d),sign in zip(pd,st['signs']):
        if ec[a]!=ec[b]: ans[tuple(sorted((ec[a],ec[b])))]+=sign
    if any(v%2 for v in ans.values()): raise ValueError('Odd signed intercomponent crossing sum')
    return {pair:v//2 for pair,v in ans.items()}

def mirror(pd):return [[q[0],q[3],q[2],q[1]] for q in pd]
