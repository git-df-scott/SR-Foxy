import json, collections, sympy as s, time, hashlib
from pathlib import Path
root=Path(__file__).parent
pd=json.loads((root/'gst48.json').read_text())['pd']
n=len(pd)
occ=collections.defaultdict(list)
for i,q in enumerate(pd):
 for j,a in enumerate(q): occ[a].append((i,j))
assert all(len(v)==2 for v in occ.values()) and len(occ)==2*n
# Rotation system: pairing of halfedges (alpha), rotation (sigma)
darts=[(i,j) for i in range(n) for j in range(4)]
alpha={a:b for vs in occ.values() for a,b in [vs,vs[::-1]]}
def cycles(perm):
 unseen=set(perm); out=[]
 while unseen:
  a=min(unseen); cycle=[]; x=a
  while x not in cycle:
   assert x in unseen
   unseen.remove(x); cycle.append(x); x=perm[x]
  assert x==a; out.append(cycle)
 return out
faces=cycles({d:(alpha[d][0],(alpha[d][1]+1)%4) for d in darts})
strandcycles=cycles({d:(alpha[d][0],(alpha[d][1]+2)%4) for d in darts})
print('n=',n,'labels=',len(occ),'faces=',len(faces),'Euler=',n-2*n+len(faces),'link components=',len(strandcycles)//2)
# Each label follows a single oriented tour 1,...,2n.
assert all(c==a%(2*n)+1 and (d==b%(2*n)+1 or b==d%(2*n)+1) for a,b,c,d in pd)
parent={a:a for a in occ}
def find(a):
 while parent[a]!=a:
  parent[a]=parent[parent[a]]; a=parent[a]
 return a
def union(a,b): parent[find(b)]=find(a)
for a,b,c,d in pd: union(b,d)
roots=sorted({find(a) for a in occ})
idx={a:i for i,a in enumerate(roots)}
arc={a:idx[find(a)] for a in occ}
assert len(roots)==n
F=s.zeros(n)
for i,(a,b,c,d) in enumerate(pd):
 F[i,arc[b]]+=2; F[i,arc[a]]-=1; F[i,arc[c]]-=1
start=time.time(); fdet=int(F[:-1,:-1].det(method='domain-ge'))
print('Fox determinant',fdet,'seconds',time.time()-start,flush=True)
t=s.symbols('t'); A=s.zeros(n)
for i,(a,b,c,d) in enumerate(pd):
 if d==b%(2*n)+1:
  A[i,arc[b]]+=1-t; A[i,arc[a]]+=t; A[i,arc[c]]-=1
 else:
  A[i,arc[b]]+=t-1; A[i,arc[a]]+=1; A[i,arc[c]]-=t
start=time.time(); D=s.expand(A[:-1,:-1].det(method='domain-ge'))
P=s.Poly(D,t); minexp=min(k[0] for k,v in P.terms()); D=s.expand(D/t**minexp)
if D.subs(t,1)==-1: D=-D
print('Alexander=',D,'factors=',s.factor(D),'seconds',time.time()-start,flush=True)
result={'source_sha256':hashlib.sha256((root/'gst48.json').read_bytes()).hexdigest(),'crossings':n,'faces':len(faces),'euler_characteristic':n-2*n+len(faces),'components':len(strandcycles)//2,'fox_determinant':abs(fdet),'alexander_ascending_coefficients':[int(s.expand(D).coeff(t,i)) for i in range(s.degree(D,t)+1)],'alexander_factorization':str(s.factor(D)), 'fox_matrix':[[int(x) for x in row] for row in F.tolist()],'pd_halfedge_faces':faces,'arc_labels':arc}
(root/'invariants.json').write_text(json.dumps(result,indent=2)+'\n')
