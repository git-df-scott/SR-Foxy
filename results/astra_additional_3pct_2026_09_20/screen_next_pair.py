"""Elementary norm certificate attempt for K8a5#-K12n13 at prime29."""
from pathlib import Path
import json,math,sys
root=Path(__file__).resolve().parent;filename=sys.argv[1] if len(sys.argv)>1 else 'EXACT_NEXT_PAIR.json';rows=json.loads((root/filename).read_text())['rows'];q=rows[0]['q'];half=(q-1)//2
cs=[]
for row in rows:
 assert row['degree']==2 and row['all_coefficients_integral'];assert row['coefficients_in_z_ascending'][0]==row['coefficients_in_z_ascending'][2]==['1']
 c=list(map(int,row['coefficients_in_z_ascending'][1]));c += [0]*(q-len(c));assert all(c[j]==c[q-j] for j in range(1,q));cs.append(c)
def prime(n):return n>1 and all(n%d for d in range(2,math.isqrt(n)+1))
def cheb(w,n,l):
 if not n:return 2
 a,b=2,w
 for _ in range(1,n):a,b=b,(w*b-a)%l
 return b%l
def middle(c,w,l):return (c[0]+sum(c[j]*cheb(w,j,l) for j in range(1,half+1)))%l
witness={};rounds=[]
for ell in [l for l in range(2*q-1,5000,2*q) if prime(l)]:
 roots=[w for w in range(ell) if w!=2 and cheb(w,q,ell)==2];assert len(roots)==half;w=roots[0]
 A=[middle(cs[0],cheb(w,a,ell),ell) for a in range(1,half+1)];B=[middle(cs[1],cheb(w,b,ell),ell) for b in range(1,half+1)]
 for a,x in enumerate(A,1):
  for b,y in enumerate(B,1):
   if (a,b) in witness or x==y:continue
   legs=[pow((v*v-4)%ell,(ell-1)//2,ell) for v in (x,y)]
   if ell-1 in legs:witness[a,b]={'pair':[a,b],'ell':ell,'w':w,'A':x,'B':y,'legendre':[-1 if z==ell-1 else z for z in legs]}
 rounds.append({'ell':ell,'root_trace':w,'A':A,'B':B,'remaining_pairs':half*half-len(witness)})
 print(ell,half*half-len(witness),flush=True)
 if len(witness)==half*half:break
r={'q':q,'pair':[row['label'] for row in rows],'all_pairs_excluded':len(witness)==half*half,'remaining_pairs':[(a,b) for a in range(1,half+1) for b in range(1,half+1) if (a,b) not in witness],'rounds':rounds,'witnesses':[witness[k] for k in sorted(witness)],'method':'Pure integer arithmetic; same norm-specialization lemma as SMALL_DIFFERENCE_PROOF.md'}
out=root/(filename.replace('EXACT_','CERTIFICATE_')) if len(sys.argv)>1 else root/'NEXT_PAIR_NORM_CERTIFICATE.json';assert not out.exists();out.write_text(json.dumps(r,indent=2)+'\n');print('All excluded:',r['all_pairs_excluded'])
