#!/usr/bin/env python3
"""Independent replay of the conditional incompressibility calculation.
Integer words and a graph quotient only. No source-producer imports.
"""
import json
if not __debug__: raise RuntimeError("Assertions must be enabled for the subgroup checker")
from pathlib import Path
from functools import lru_cache
P=Path(__file__).resolve().parent

def reduce(w):
 ans=[]
 for x in w:
  if ans and ans[-1]==-x:ans.pop()
  else:ans.append(x)
 return tuple(ans)
def inverse(w):return tuple(-x for x in reversed(w))
def apply(w,d):return reduce(y for x in w for y in (d[abs(x)] if x>0 else inverse(d[abs(x)])))
def cyclic(w):
 w=reduce(w)
 while len(w)>1 and w[0]==-w[-1]:w=w[1:-1]
 return w

def graph(words):
 # Fold an explicit multigraph by repeatedly quotienting vertices, then edges.
 edges=[];N=1
 for w in words:
  at=0
  for j,x in enumerate(w):
   nxt=0 if j==len(w)-1 else N
   if nxt==N:N+=1
   edges.append((at,x,nxt));at=nxt
 classes=list(range(N));rounds=0
 while True:
  oriented=[]
  for a,x,b in edges:oriented.extend([(classes[a],x,classes[b]),(classes[b],-x,classes[a])])
  seen={};pair=None
  for a,x,b in oriented:
   key=(a,x)
   if key in seen and seen[key]!=b:pair=(min(seen[key],b),max(seen[key],b));break
   seen[key]=b
  if pair is None:break
  u,v=pair;classes=[u if c==v else c for c in classes];rounds+=1
 ee=set()
 for a,x,b in edges:ee.add((classes[a],x,classes[b]));ee.add((classes[b],-x,classes[a]))
 vv={classes[0]}|{a for a,x,b in ee}|{b for a,x,b in ee}
 return {'V':len(vv),'E':len(ee)//2,'rank':len(ee)//2-len(vv)+1,'rounds':rounds}

if __name__=='__main__':
 saved=json.loads((P/'stallings_probe.json').read_text());inp=json.loads((P/'prior/astra_one_commutator_2026_09_18/inputs_extended.json').read_text());cert=json.loads((P/'prior/astra_one_commutator_2026_09_18/CERTIFICATE.json').read_text())
 rel=[cyclic(w) for w in inp['source_relators']];images={g:(g,) for g in range(1,10)}
 for move in saved['tietze']:
  r=tuple(move['defining_relator']);g=move['generator'];rep=tuple(move['replacement']);assert r in rel and sum(abs(x)==g for x in r)==1 and all(abs(x)!=g for x in rep)
  im={a:((a,) if a!=g else rep) for a in range(1,10)};assert apply(r,im)==()
  rel.remove(r);rel=[cyclic(apply(r,im)) for r in rel];rel=[r for r in rel if r];images={a:apply(w,im) for a,w in images.items()}
 assert len(rel)==2 and all(tuple(saved['tietze_images'][str(g)])==w for g,w in images.items())
 assert any(rel[1]==r[i:]+r[:i] for r in (rel[0],inverse(rel[0])) for i in range(len(r)))
 mu,x=saved['mu'],saved['x'];offset=saved['offset'];base_lo,base_hi=saved['basis_levels']
 def schreier(w):
  k=0;ans=[]
  for a in w:
   assert abs(a) in (mu,x)
   if abs(a)==x:ans.append((1 if a>0 else -1)*(offset+k-(a<0)))
   k+=1 if a>0 else -1
  assert k==0
  return reduce(ans)
 r=schreier(rel[0]);assert r==tuple(saved['schreier_relator']);lo=min(abs(a)-offset for a in r);hi=max(abs(a)-offset for a in r)
 assert hi-lo==4 and sum(abs(a)==offset+lo for a in r)==1 and sum(abs(a)==offset+hi for a in r)==1
 @lru_cache(None)
 def y(k):
  if base_lo<=k<=base_hi:return (k-base_lo+1,)
  shift=k-hi if k>base_hi else k-lo;rr=tuple((1 if a>0 else -1)*(abs(a)+shift) for a in r);pos=next(j for j,a in enumerate(rr) if abs(a)==offset+k)
  rhs=inverse(rr[pos+1:]+rr[:pos]);rhs=rhs if rr[pos]>0 else inverse(rhs)
  return reduce(z for a in rhs for z in (y(abs(a)-offset) if a>0 else inverse(y(abs(a)-offset))))
 def norm(w):return reduce(z for a in schreier(apply(w,images)) for z in (y(abs(a)-offset) if a>0 else inverse(y(abs(a)-offset))))
 q={int(k)+1:w for k,w in inp['q0_images'].items()};ww={'A':cert['words']['A']['boundary_word'],'B':cert['words']['B']['boundary_word'],'b':inp['axis2'],'a':inp['axis1'],'delta':inp['original_boundary_delta']}
 actual={k:norm(apply(w,q)) for k,w in ww.items()};assert all(actual[k]==tuple(saved['words'][k]) for k in actual);assert all(norm(w)==() for w in inp['source_relators'])
 result=graph([actual[k] for k in ('A','B','b')]);assert result['rank']==3 and result['V']==16 and result['E']==18
 controls={'free_rank_three':graph([(1,),(2,),(3,)])['rank']==3,'dependent_triple_rank_two':graph([(1,),(2,),(1,2)])['rank']==2,'repeated_word_rank_one':graph([(1,2),(1,2)])['rank']==1,'null_word_rank_zero':graph([()])['rank']==0}
 assert all(controls.values())
 out={'status':'PASS','graph':result,'controls':controls,'source_relators_checked':9,'words_checked':list(actual),'conditional_result':'The map F(A,B,b) -> source group determined by saved q0 is injective. A corresponding actual correction surface has no compressing disk IF q0 is its geometric disk-exterior inclusion. This does not exclude a different modifying annulus between a and b_prime.'}
 (P/'independent_subgroup_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
