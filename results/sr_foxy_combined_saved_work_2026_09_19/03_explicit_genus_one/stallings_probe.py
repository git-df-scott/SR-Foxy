#!/usr/bin/env python3
import json,sys
from pathlib import Path
P=Path(__file__).resolve().parent; Q=P/'prior/astra_one_commutator_2026_09_18'
sys.path.insert(0,str(Q))
from free_words import red,inv,mul,sub,eliminate
D=json.loads((Q/'inputs_extended.json').read_text())
for keep in [(5,),(6,),(8,)]:
 gs,rs,im,log=eliminate(D['source_relators'],keep)
 print('source keep',keep,'gens',gs,'relator lengths',list(map(len,rs)))
 print(rs)
gs,rs,im,log=eliminate(D['source_relators'],(5,))
r0,r1=rs
print('cyclic redundancy',any(tuple(r1)==w[i:]+w[:i] for w in (r0,inv(r0)) for i in range(len(w))))
# Derive a free-by-cyclic target using the cyclically redundant presentation.
from functools import lru_cache
mu=5;x=3;O=100

def rew(w):
 k=0;ans=[]
 for z in w:
  if abs(z) not in (mu,x):raise ValueError('bad letter')
  if abs(z)==x: ans.append((1 if z>0 else -1)*(O+k-(z<0)))
  k+=1 if z>0 else -1
 if k:raise ValueError('nonzero exponent')
 return red(ans)
r=rew(rs[0]);minlev=min(abs(z)-O for z in r);maxlev=max(abs(z)-O for z in r)
print('Schreier',r,'extrema',minlev,maxlev)
lo=minlev+1;hi=maxlev
rules={}
@lru_cache(None)
def y(k):
 if lo<=k<=hi:return (k-lo+1,)
 shift=k-maxlev if k>hi else k-minlev
 rr=tuple((1 if z>0 else -1)*(abs(z)+shift) for z in r)
 js=[j for j,z in enumerate(rr) if abs(z)==O+k]
 if len(js)!=1:raise ValueError('extremum not unique')
 j=js[0];expr=inv(rr[j+1:]+rr[:j]);expr=expr if rr[j]>0 else inv(expr)
 ans=red(v for z in expr for v in (y(abs(z)-O) if z>0 else inv(y(abs(z)-O))))
 rules[k]={'shift':shift,'relation':list(rr),'rhs':list(expr),'image':list(ans)}
 return ans

def normal_src(w):
 return red(v for z in rew(sub(w,im)) for v in (y(abs(z)-O) if z>0 else inv(y(abs(z)-O))))
q={int(k)+1:w for k,w in D['q0_images'].items()}
cc=json.loads((Q/'CERTIFICATE.json').read_text())
ww={'A':cc['words']['A']['boundary_word'],'B':cc['words']['B']['boundary_word'],'b':D['axis2'],'delta':D['original_boundary_delta'],'a':D['axis1']}
norms={name:normal_src(sub(w,q)) for name,w in ww.items()}
print('normal lengths', {k:len(w) for k,w in norms.items()}); print('normal words',norms)
print('relators',[normal_src(w) for w in D['source_relators']])
# Independent labelled-graph rank by iterative complete folding.
def fold(words):
 parent=[0];edges=[]
 def nv():parent.append(len(parent));return len(parent)-1
 for w in words:
  at=0
  for j,l in enumerate(w):
   nxt=0 if j==len(w)-1 else nv();edges.extend([(at,l,nxt),(nxt,-l,at)]);at=nxt
 def root(v):
  while parent[v]!=v:parent[v]=parent[parent[v]];v=parent[v]
  return v
 folds=[]
 while True:
  seen={};change=False
  for u,l,v in edges:
   u,v=root(u),root(v);key=(u,l)
   if key in seen and root(seen[key])!=v:
    p=root(seen[key]);parent[max(p,v)]=min(p,v);folds.append([p,v]);change=True;break
   seen[key]=v
  if not change:break
 ee=sorted({(root(u),l,root(v)) for u,l,v in edges});verts=sorted({v for u,l,v in ee}|{u for u,l,v in ee}|{root(0)})
 return {'vertices':verts,'oriented_edges':ee,'rank':len(ee)//2-len(verts)+1,'root':root(0),'fold_count':len(folds),'folds':folds}
f=fold([norms[k] for k in ('A','B','b')]);print('subgroup',{'rank':f['rank'],'V':len(f['vertices']),'E':len(f['oriented_edges'])//2})
result={'source_commit':D['source_commit'],'tietze':log,'tietze_images':im,'remaining_relators':rs,'mu':mu,'x':x,'offset':O,'schreier_relator':r,'basis_levels':[lo,hi],'rules':rules,'words':{k:list(v) for k,v in norms.items()},'folded_graph':f}
(P/'stallings_probe.json').write_text(json.dumps(result,indent=2)+'\n')
