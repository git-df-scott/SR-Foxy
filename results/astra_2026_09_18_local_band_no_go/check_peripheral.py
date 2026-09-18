#!/usr/bin/env python3
"""Astra: exact local-family audit. Reads repository inputs; prints JSON only."""
import json, hashlib
from pathlib import Path
if not __debug__:raise RuntimeError("Assertions must be enabled")
REPO=Path(__file__).resolve().parents[2]
PINNED={
  "results/chat_archive_2026_09_17/expanded/SR_Foxy_pass09_product_collar_2026_09_17/pass09_product_collar/diagram_core.py": "66cc09e760cbfbb6a41cc725972fb86e8af49cc3",
  "results/astra_2026_09_17_overnight/pass06_0055_explicit_unlink_bands/check_explicit_unlink_bands.py": "baf481237bbbcd9ab57c3c378a6fc8e34286c0ef",
  "results/astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json": "86bb4e5ec1ae5a1762f4ce724279c7c5a509fed6"
}
def pinned(path):
 raw=(REPO/path).read_bytes()
 assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==PINNED[path],path
 return raw.decode()
CORE=pinned("results/chat_archive_2026_09_17/expanded/SR_Foxy_pass09_product_collar_2026_09_17/pass09_product_collar/diagram_core.py")
CERT=json.loads(pinned("results/astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json"))
ROWS=json.loads(Path(__file__).with_name("SCAN.json").read_text())

import types,json,sympy as sp
g=types.ModuleType("core");exec(CORE,g.__dict__)
A=g.adjacency_from_pd(g.SCAFFOLD);U={c:list(A[c]) for c in range(27)};g.connect(U,(0,2),(1,1));q=g.quotient_R_wirtinger(U)
z=sp.Symbol("z");R=z**6+3*z**5+5*z**4+4*z**3+2*z**2+z+1
def reduce(x):return sp.rem(sp.expand(x),R,z)
def mm(a,b):return (a*b).applyfunc(reduce)
def inv(a):return sp.Matrix([[a[1,1],-a[0,1]],[-a[1,0],a[0,0]]])
mat={int(k):sp.Matrix(2,2,[sum(c*z**i for i,c in enumerate(p)) for p in v]) for k,v in CERT["source_matrices"].items()}
start=min(x for x,a in q["arcs"].items() if a==2 and x in q["incoming"])
cur=start;seen=set();word=[];writhe=0
while cur not in seen:
 seen.add(cur);c,p=cur
 if p in (0,2) and q["cmap"][c,1]==0:
  word.append(q["signs"][c]*(q["arcs"][c,1]+1));writhe+=q["signs"][c]
 cur=U[c][(p+2)%4]
word=([-3]*writhe if writhe>=0 else [3]*(-writhe))+word
L=sp.eye(2)
for x in word:L=mm(L,mat[x] if x>0 else inv(mat[-x]))
mu=mat[3];N=mu-sp.eye(2);assert mm(mu,L)==mm(L,mu)
a=reduce(sp.trace(L)/2);assert a in [1,-1]
s=reduce(L[0,1]/a);assert L==a*(sp.eye(2)+s*N).applyfunc(reduce)
print(json.dumps({"seam_start":start,"longitude_word":word,"writhe":writhe,"longitude_scalar_sign":int(a),"longitude_unipotent_parameter":str(s),"longitude_matrix":[str(x) for x in L]}),flush=True)
n,m=sp.symbols("n m")
for row in ROWS[:8]:
 p=[sum(v*z**j for j,v in enumerate(a)) for a in row["trace_difference"]]
 expr=reduce(sum(a*(n+m*s)**i for i,a in enumerate(p)))
 polys=[sp.Poly(expr,z).nth(i) for i in range(6)]
 basis=sp.groebner(polys,n,m);sol=sp.solve(polys,[n,m],dict=True)
 assert [p.as_expr() for p in basis.polys]==([n,m] if row["bits"] in [[False,False,False,False],[False,False,True,True]] else [1])
 print(json.dumps({"bits":row["bits"],"solutions":[{str(k):str(v) for k,v in x.items()} for x in sol],"groebner_basis":[str(x) for x in basis.polys]}),flush=True)
