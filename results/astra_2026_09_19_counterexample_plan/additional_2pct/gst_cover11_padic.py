"""Determine the 43-primary invariant factors by elementary operations modulo 43^5."""
from gst_cover11 import cover_matrix,P
import json,time,math
import sympy as s

def valuations(matrix,p=43,e=5):
 modulus=p**e;A=[[int(x)%modulus for x in row] for row in matrix.tolist()];n=len(A);vals=[]
 def val(x):
  if not x:return e
  v=0
  while x%p==0:x//=p;v+=1
  return v
 for k in range(n):
  v,i,j=min((val(A[i][j]),i,j) for i in range(k,n) for j in range(k,n))
  if v==e:vals.extend([e]*(n-k));break
  A[k],A[i]=A[i],A[k]
  for row in A:row[k],row[j]=row[j],row[k]
  pv=p**v;inverse=pow(A[k][k]//pv,-1,modulus//pv)
  for col in range(k,n):A[k][col]=(A[k][col]*inverse)%modulus
  assert A[k][k]==pv
  for row in range(k+1,n):
   assert A[row][k]%pv==0
   factor=A[row][k]//pv
   for col in range(k,n):A[row][col]=(A[row][col]-factor*A[k][col])%modulus
   assert A[row][k]==0
  # Column operations can now clear pivot row without changing the trailing block.
  assert all(A[k][j]%pv==0 for j in range(k,n))
  vals.append(v)
 return vals

def main():
 start=time.monotonic()
 # Mixed valuation test with nontrivial unimodular row/column changes.
 C=s.diag(1,43,43**2,43**3);U=s.eye(4);U[0,2]=7;U[2,3]=-11;W=s.eye(4);W[3,1]=9
 assert valuations(U*C*W)==[0,1,2,3]
 V=s.Matrix(json.loads((P/'GST_SEIFERT_MATRIX.json').read_text()));R=cover_matrix(V,11)
 vals=valuations(R);assert sum(vals)==4
 factors=[43**v for v in vals if v]
 # Order certified independently by the Alexander resultant, not inferred from mod p alone.
 t=s.Symbol('t');f=t**8-2*t**7+t**6+t**5-2*t**4+t**3-1;g=-s.expand(t**8*f.subs(t,1/t));D=-s.expand(f*g)
 order=abs(int(s.resultant(D,t**11-1,t)));assert order==43**4==math.prod(factors)
 out={'status':'PASS','n':11,'source_dimension':V.rows,'nonunit_invariant_factors':factors,'valuations':vals,'homology_order':order,'modulus':43**5,'presentation_matrix':[[int(x) for x in row] for row in R.tolist()],'seconds':time.monotonic()-start,'method':'KnotInfo Seifert presentation; elementary modular Smith elimination with exact order from independent polynomial resultant','scope':'Homology only; saved Seifert matrix trusted as the literal GST48 matrix. Not a pairing, disk kernel or nonribbonness result.'}
 (P/'GST_COVER11_PADIC.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k not in ['presentation_matrix','valuations']})
if __name__=='__main__':main()
