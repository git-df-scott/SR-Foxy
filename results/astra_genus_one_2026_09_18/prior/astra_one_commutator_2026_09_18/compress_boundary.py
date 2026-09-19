import json
from pathlib import Path
from free_words import *
ROOT=Path(__file__).resolve().parent
d=json.loads((ROOT/'inputs.json').read_text());c=json.loads((ROOT/'handle_optimization.json').read_text())
rels=[[-(b+1)*s,i+1,(b+1)*s,-o-1] for i,o,b,s,cross in d['boundary_relations']]
def power(g,n):return tuple((g if n>0 else -g) for _ in range(abs(n)))
y={j:mul(power(3,j-2),(5,),power(3,-j+1)) for j in range(1,5)}
rules=[]
for ri,r in enumerate(rels):
 for sign,rr in [(1,tuple(r)),(-1,inv(r))]:
  for sh in range(len(rr)):
   v=rr[sh:]+rr[:sh]
   for k in range(1,len(v)+1):
    lhs=v[:k];rhs=inv(v[k:])
    if (len(rhs),rhs)<(len(lhs),lhs):rules.append((lhs,rhs,ri,sign,sh,k))
rules.sort(key=lambda x:(-len(x[0]),x))
def shorten(w):
 w=red(w);moves=[]
 while True:
  found=False
  for lhs,rhs,ri,sg,sh,k in rules:
   for pos in range(len(w)-len(lhs)+1):
    if w[pos:pos+len(lhs)]==lhs:
     after=mul(w[:pos],rhs,w[pos+len(lhs):])
     if (len(after),after)>=(len(w),w):continue
     moves.append({'relator':ri,'sign':sg,'rotation':sh,'prefix_length':k,'offset':pos,'before':w,'after':after})
     w=after;found=True;break
   if found:break
  if not found:return w,moves
out=[]
for f,g in c['factors']:
 aa,bb=sub(f,y),sub(g,y);a,ma=shorten(aa);b,mb=shorten(bb)
 print('basis',y)
 print('A',len(aa),'->',len(a),a,'B',len(bb),'->',len(b),b)
 print('exponents',sum(1 if x>0 else -1 for x in a),sum(1 if x>0 else -1 for x in b))
 out.append({'a_original':aa,'b_original':bb,'a':a,'b':b,'a_moves':ma,'b_moves':mb})
(ROOT/'boundary_handle_certificate.json').write_text(json.dumps({'basis':y,'pairs':out,'convention':'[a,b]=a b a^-1 b^-1','genus_upper_bound':len(out),'CE':False},indent=2)+'\n')
