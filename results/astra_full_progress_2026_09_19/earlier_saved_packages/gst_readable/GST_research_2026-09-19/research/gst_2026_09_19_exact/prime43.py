"""Exact F_43[t]/(t^2-4t+1) ranks, with no floating-point arithmetic."""
import json
from pathlib import Path
from pd_algebra import fox_matrix,t
P=43
def add(z,w):return ((z[0]+w[0])%P,(z[1]+w[1])%P)
def neg(z):return (-z[0]%P,-z[1]%P)
def mul(z,w):
 a,b=z;c,d=w
 return ((a*c-b*d)%P,(a*d+b*c+4*b*d)%P)
def inv(z):
 a,b=z;n=(a*a+4*a*b+b*b)%P
 if n==0:raise ZeroDivisionError
 c=pow(n,-1,P);return ((a+4*b)*c%P,-b*c%P)
def power(z,n):
 ans=(1,0)
 while n:
  if n%2:ans=mul(ans,z)
  z=mul(z,z);n//=2
 return ans
def rank(M):
 M=[[z for z in r] for r in M];nr=len(M);nc=len(M[0]);k=0;piv=[]
 for col in range(nc):
  row=next((i for i in range(k,nr) if M[i][col]!=(0,0)),None)
  if row is None:continue
  M[k],M[row]=M[row],M[k];u=inv(M[k][col]);M[k]=[mul(x,u) for x in M[k]]
  for i in range(nr):
   if i!=k and M[i][col]!=(0,0):
    c=M[i][col];M[i]=[add(a,neg(mul(c,b))) for a,b in zip(M[i],M[k])]
  piv.append(col);k+=1
  if k==nr:break
 return k,piv
if __name__=='__main__':
 ROOT=Path(__file__).parent;pd=json.loads((ROOT/'gst48.json').read_text())['pd'];A=fox_matrix(pd)
 F=[[ (int(e.coeff(t,0))%P,int(e.coeff(t,1))%P) for e in row] for row in A.tolist()]
 r,piv=rank(F);re,pe=rank([row[:-1] for row in F[:-1]])
 order=next(n for n in range(1,P*P) if power((0,1),n)==(1,0))
 print('extension rank',r,'reducedrank',re,'t order',order)
 out={'prime':43,'irreducible_modulus_ascending':[1,-4,1],'t_multiplicative_order':order,'full_Fox_rank':r,'reduced_Fox_rank':re,'full_pivot_columns':piv,'reduced_pivot_columns':pe,'reduced_dimension':47,'reduced_nullity':47-re}
 (ROOT/'prime43_results.json').write_text(json.dumps(out,indent=2)+'\n')
 # exhaustive field inverse check: only 1848 elements
 assert all(mul((a,b),inv((a,b)))==(1,0) for a in range(P) for b in range(P) if (a,b)!=(0,0))
