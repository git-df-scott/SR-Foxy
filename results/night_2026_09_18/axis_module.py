"""Exact axis classes over Q[t]/Delta from the boundary Wirtinger diagram."""
from pathlib import Path
import sympy as s,json,resource
resource.setrlimit(resource.RLIMIT_CPU,(60,65))
ROOT=Path(__file__).resolve().parents[2]
g={};exec((ROOT/'results/chat_archive_2026_09_17/expanded/SR_Foxy_pass09_product_collar_2026_09_17/pass09_product_collar/diagram_core.py').read_text(),g)
t=s.symbols('t');Delta=t**4-3*t**3+5*t**2-3*t+1
red=lambda x:s.rem(s.cancel(x),Delta,t)
def add(a,b):return red(a+b)
def mul(a,b):return red(a*b)
def inv(a):return s.invert(a,Delta,t)
def power(k):return red(t**k) if k>=0 else red(s.invert(t**(-k),Delta,t))
A=g['adjacency_from_pd'](g['SCAFFOLD']);q=g['quotient_R_wirtinger'](A)
N=1+max(q['arcs'].values());rel=[[-sg*(b+1),i+1,sg*(b+1),-(o+1)] for i,o,b,sg,c in q['relations']]
def fox(w):
 row=[0]*N;pref=0
 for x in w:
  row[abs(x)-1]=add(row[abs(x)-1], (1 if x>0 else -1)*power(pref if x>0 else pref-1))
  pref+=1 if x>0 else -1
 assert pref==0
 return row[1:]
M=[fox(w) for w in rel];piv=[];k=0
for j in range(N-1):
 a=next((i for i in range(k,len(M)) if M[i][j]!=0),None)
 if a is None:continue
 M[k],M[a]=M[a],M[k];c=inv(M[k][j]);M[k]=[mul(v,c) for v in M[k]]
 for i in range(len(M)):
  if i!=k and M[i][j]!=0:
   c=M[i][j];M[i]=[add(v,-mul(c,w)) for v,w in zip(M[i],M[k])]
 piv.append(j);k+=1
free=[i for i in range(N-1) if i not in piv];assert len(free)==2
Z=[[0,0] for _ in range(N-1)]
for j,f in enumerate(free):Z[f][j]=1
for i,p in enumerate(piv):
 for j,f in enumerate(free):Z[p][j]=-M[i][f]
assert all(red(sum(mul(v,Z[i][j]) for i,v in enumerate(fox(w))))==0 for w in rel for j in range(2))
def coords(w):
 row=fox(w)
 return [red(sum(mul(v,Z[i][j]) for i,v in enumerate(row))) for j in range(2)]
def words(D):
 qf=g['quotient_R_wirtinger'](D);mp=g['map_final_R_arcs_to_scaffold'](q,qf)
 ans=[]
 for comp in range(1,len(qf['components'])):
  cur=min(qf['components'][comp]);seen=set();w=[]
  while cur not in seen:
   seen.add(cur);c,p=cur
   if p in (0,2) and qf['cmap'][c,1]==0:w.append((mp[qf['arcs'][c,1]]+1)*qf['signs'][c])
   cur=D[c][(p+2)%4]
  ans.append(w)
 return ans
oldwords=words(A);old=[coords(w) for w in oldwords]
D=g['add_zero_twist_band'](g['add_zero_twist_band'](A,g['BAND1']),g['BAND2'])
newwords=words(D);new=[coords(w) for w in newwords]
print(json.dumps({'Delta':str(Delta),'scaffold_axis_words':oldwords,'scaffold_axis_coordinates':[[str(v) for v in row] for row in old],'mixed_axis_words':newwords,'mixed_axis_coordinates':[[str(v) for v in row] for row in new],'mixed_determinant_mod_Delta':str(red(new[0][0]*new[1][1]-new[0][1]*new[1][0])),'free_columns':free},indent=2),flush=True)
# Decompose each mixed class in the upper/lower source lines. Native base
# whiskers are recorded, so the shifts below refer to these exact words.
base=s.Matrix([old[0],old[2]]).T
assert red(base.det())!=0
Binv=base.adjugate().applyfunc(lambda x:mul(x,inv(red(base.det()))))
expected={'c2_upper':[power(-1),0],'c2_lower':[0,power(-1)],'eta1':[1,-power(-1)],'eta2':[power(-1),-1]}
for label,vec in [('c2_upper',old[1]),('c2_lower',old[3]),('eta1',new[0]),('eta2',new[1])]:
 cs=[red(v) for v in Binv*s.Matrix(vec)]
 assert all(red(a-b)==0 for a,b in zip(cs,expected[label]))
 monomial=[]
 for v in cs:
  hits=[(sg,k) for sg in [1,-1] for k in range(-12,13) if red(v-sg*power(k))==0]
  monomial.append(hits)
 print(json.dumps({'label':label,'coefficients':[str(v) for v in cs],'signed_monomials_in_box':monomial}),flush=True)
