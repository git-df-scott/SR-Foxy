"""Deck action on H1/43H1, using the Seifert presentation convention in gst_cover11."""
from pathlib import Path
import json
import sympy as s
P=Path(__file__).parent;p=43

def nullspace(M):
 A=[[int(x)%p for x in r] for r in M.tolist()];m=len(A);n=len(A[0]);piv=[];r=0
 for c in range(n):
  i=next((i for i in range(r,m) if A[i][c]),None)
  if i is None:continue
  A[r],A[i]=A[i],A[r];z=pow(A[r][c],-1,p);A[r]=[(x*z)%p for x in A[r]]
  for i in range(m):
   if i!=r:
    z=A[i][c];A[i]=[(x-z*y)%p for x,y in zip(A[i],A[r])]
  piv.append(c);r+=1
 free=[c for c in range(n) if c not in piv];basis=[]
 for c in free:
  b=[0]*n;b[c]=1
  for i,k in enumerate(piv):b[k]=-A[i][c]%p
  basis.append(b)
 return s.Matrix(basis),free

def mod(M):return M.applyfunc(lambda x:int(x)%p)
V=s.Matrix(json.loads((P/'GST_SEIFERT_MATRIX.json').read_text()));G=(V.T-V).inv()*V.T
R=s.Matrix(json.loads((P/'GST_COVER11_PADIC.json').read_text())['presentation_matrix'])
B,free=nullspace(R.T);assert B.rows==2 and mod(B*R)==s.zeros(2,74)
Gb=mod((B*G)[:,free]);assert mod(B*G)==mod(Gb*B)
T=mod((Gb-s.eye(2)).inv_mod(p)*Gb)
t=s.Symbol('t');poly=s.Poly(T.charpoly(t).as_expr(),t,modulus=p)
assert poly.as_expr()==t**2-4*t+1 and poly.is_irreducible
assert mod(T**11)==s.eye(2)
out={'status':'PASS','prime':p,'quotient_basis':[[int(x) for x in row] for row in B.tolist()],'G_action':[[int(x) for x in row] for row in Gb.tolist()],'deck_action':[[int(x) for x in row] for row in T.tolist()],'characteristic_polynomial_mod43':str(poly.as_expr()),'irreducible':True,'order':11,'scope':'Deck action on H1/43H1; deck generator inversion has same reciprocal characteristic polynomial.'}
(P/'GST_COVER11_DECK.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k!='quotient_basis'})
