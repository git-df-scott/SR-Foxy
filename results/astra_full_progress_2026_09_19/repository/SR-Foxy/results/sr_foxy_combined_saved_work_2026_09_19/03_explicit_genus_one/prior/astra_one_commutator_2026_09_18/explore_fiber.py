import json
from free_words import *
d=json.load(open(__file__.replace('explore_fiber.py','inputs.json')))
rels=[[-(b+1)*s,i+1,(b+1)*s,-o-1] for i,o,b,s,c in d['boundary_relations'][1:9]]
gens,rs,im,log=eliminate(rels,(3,))
# encode y_k with k offset20
O=20
def rsword(w):
 k=0;out=[]
 for x in w:
  if abs(x)==5:out.append((k+O) if x>0 else -(k-1+O))
  k+=1 if x>0 else -1
 if k:raise ValueError('nonzero exponent')
 return red(out)
r=rsword(rs[0]);delta=rsword(sub(d['boundary_delta_short'],im))
print('relator y_k',[(1 if x>0 else -1,abs(x)-O) for x in r])
print('delta RS length',len(delta),'k support',sorted({abs(x)-O for x in delta}))
print('delta RS',delta)
from functools import lru_cache
lo,hi=-1,2
base={k:(k-lo+1,) for k in range(lo,hi+1)}
def shift(w,n):return tuple((1 if x>0 else -1)*(abs(x)+n) for x in w)
@lru_cache(None)
def y(k):
 if k in base:return base[k]
 rr=shift(r,k-2 if k>hi else k+2)
 symbol=k+O
 p=next(i for i,x in enumerate(rr) if abs(x)==symbol)
 expr=inv(rr[p+1:]+rr[:p]);expr=expr if rr[p]>0 else inv(expr)
 if sum(abs(x)==symbol for x in rr)!=1:raise ValueError('not unique extremum')
 return red(a for x in expr for a in (y(abs(x)-O) if x>0 else inv(y(abs(x)-O))))
def fy(w):return red(a for x in w for a in (y(abs(x)-O) if x>0 else inv(y(abs(x)-O))))
out=fy(delta)
print('fiber delta length',len(out),'word',out)
p,w=cyc(out)
print('cyclic reduction',len(w),'prefix',p,'word',w)
from collections import Counter
print('counts',Counter(w))
for k in range(-3,5):
 print('y',k,'len',len(y(k)),y(k))
json.dump({'tietze_log':log,'generator_images':im,'relator_two_gen':rs[0],'schreier_relator':r,'schreier_offset':O,'basis_levels':[lo,hi],'delta_two_gen':sub(d['boundary_delta_short'],im),'delta_schreier':delta,'delta_fiber':out,'conjugating_prefix':p,'cyclic_delta':w},open(__file__.replace('explore_fiber.py','fiber_probe.json'),'w'),indent=2)
