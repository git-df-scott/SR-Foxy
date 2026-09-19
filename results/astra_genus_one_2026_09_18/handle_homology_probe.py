#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent
D=json.loads((P/'prior/astra_one_commutator_2026_09_18/inputs_extended.json').read_text())
C=json.loads((P/'prior/astra_one_commutator_2026_09_18/CERTIFICATE.json').read_text())
t=s.Symbol('t'); d=t**4-3*t**3+5*t**2-3*t+1
# Work in the number field Q[t]/d. Inputs are Laurent polynomials.
def mod(x):
 a,b=s.fraction(s.cancel(x)); a=s.Poly(a,t,domain=s.QQ); b=s.Poly(b,t,domain=s.QQ)
 return (a*s.invert(b,s.Poly(d,t))).rem(s.Poly(d,t)).as_expr()
def fox(w,N):
 r=[0]*N; e=0
 for x in w:
  if x>0:r[x-1]+=t**e;e+=1
  else:e-=1;r[-x-1]-=t**e
 return [s.expand(z) for z in r]
M=[[mod(x) for x in fox(r,9)] for r in D['source_relators']]
a=[r[:] for r in M];piv=[];i=0
for j in range(9):
 k=next((k for k in range(i,len(a)) if a[k][j]!=0),None)
 if k is None:continue
 a[i],a[k]=a[k],a[i];u=a[i][j];a[i]=[mod(x/u) for x in a[i]]
 for k in range(len(a)):
  if k!=i and a[k][j]!=0:
   u=a[k][j];a[k]=[mod(x-u*y) for x,y in zip(a[k],a[i])]
 piv.append(j);i+=1
 if i==len(a):break
free=[j for j in range(9) if j not in piv]
ns=[]
for j in free:
 v=[0]*9;v[j]=1
 for row,k in enumerate(piv):v[k]=-a[row][j]
 ns.append(v)
print('rank',len(piv),'nullspace dim',len(ns))
v=next(v for v in ns if len(set(map(str,v)))>1)
# Subtract the constant coboundary for a fixed origin.
v=[mod(x-v[0]) for x in v]
q={int(k)+1:w for k,w in D['q0_images'].items()}
def inv(w):return [-x for x in w[::-1]]
def sub(w):return [y for x in w for y in (q[x] if x>0 else inv(q[-x]))]
def value(w):return mod(sum(x*y for x,y in zip(fox(sub(w),9),v)))
ww={'A':C['words']['A']['boundary_word'],'B':C['words']['B']['boundary_word'],'b':D['axis2'],'a':D['axis1']}
vals={k:value(w) for k,w in ww.items()}
print('v',v);print('images',vals)
cols=s.Matrix([[s.expand(vals[k]).coeff(t,i) for k in ['A','B','b']] for i in range(4)])
print('columns',cols.tolist(),'rank',cols.rank(),'nullspace',cols.nullspace())
result={'status':'ALGEBRAIC_Q0_ONLY','source_commit':D['source_commit'],'modulus':str(d),'source_cochain':[str(x) for x in v],'source_relators_checked':all(mod(sum(x*y for x,y in zip(row,v)))==0 for row in M),'images':{k:str(x) for k,x in vals.items()},'matrix_columns_A_B_b':cols.tolist(),'rational_rank':cols.rank(),'nullspace':[[str(x) for x in z] for z in cols.nullspace()]}
(P/'handle_homology_probe.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
