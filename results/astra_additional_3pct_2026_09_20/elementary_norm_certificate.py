"""Pure Python prime-field certificate, independent of FLINT factorization.

For t^2+A*t+1, nonsquare A^2-4 over F_l gives simple norm-one
roots in F_(l^2). If A!=B, (t^2+A*t+1)(t^2+B*t+1) has an odd
valuation at either of these roots and cannot be a conjugate-reciprocal norm.
"""
from pathlib import Path
import json
root=Path(__file__).resolve().parent;old=root.parent/'astra_seven_hour_2026_09_20'
rows=json.loads((old/'EXACT_SMALL_DIFFERENCE_v2.json').read_text())['rows']
cs=[]
for row in rows:
 c=list(map(int,row['coefficients_in_z_ascending'][1]));c += [0]*(19-len(c));assert len(c)==19
 assert all(c[j]==c[19-j] for j in range(1,19));cs.append(c)
def cheb(w,n,l):
 if n==0:return 2
 a,b=2,w
 for _ in range(1,n):a,b=b,(w*b-a)%l
 return b%l
def eval_middle(c,w,l):return (c[0]+sum(c[j]*cheb(w,j,l) for j in range(1,10)))%l
witnesses={};rounds=[]
for ell in (37,113,227,379):
 roots=[w for w in range(ell) if w!=2 and cheb(w,19,ell)==2];assert len(roots)==9
 w=roots[0];assert pow((w*w-4)%ell,(ell-1)//2,ell)==ell-1
 As=[eval_middle(cs[0],cheb(w,a,ell),ell) for a in range(1,10)]
 Bs=[eval_middle(cs[1],cheb(w,b,ell),ell) for b in range(1,10)]
 rounds.append({'ell':ell,'trace_of_primitive_19th_root':w,'all_possible_traces':roots,'A_coefficients':As,'B_coefficients':Bs})
 for a,A in enumerate(As,1):
  for b,B in enumerate(Bs,1):
   if (a,b) in witnesses or A==B:continue
   leg=[pow((v*v-4)%ell,(ell-1)//2,ell) for v in (A,B)]
   if ell-1 in leg:witnesses[a,b]={'pair':[a,b],'ell':ell,'w':w,'A':A,'B':B,'quadratic_discriminant_legendre':[-1 if x==ell-1 else x for x in leg]}
assert len(witnesses)==81,('Unexcluded',[(a,b) for a in range(1,10) for b in range(1,10) if (a,b) not in witnesses])
r={'all81_excluded':True,'method':'Integer modular arithmetic and Euler criterion only; no algebra system or finite-field factorization','rounds':rounds,'witnesses':[witnesses[k] for k in sorted(witnesses)]}
out=root/'ELEMENTARY_NORM_CERTIFICATE.json';assert not out.exists();out.write_text(json.dumps(r,indent=2)+'\n');print({'all81_excluded':True,'witnesses_by_prime':{ell:sum(v['ell']==ell for v in witnesses.values()) for ell in (37,113,227,379)}})
