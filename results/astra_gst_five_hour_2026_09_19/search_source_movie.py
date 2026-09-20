"""Bounded local Reidemeister certificate search; no negative proof from timeout."""
import json,random,time,sys,collections
from pathlib import Path
import regina
p=Path(__file__).parent;n=int(sys.argv[1]) if len(sys.argv)>1 else 1
limit=float(sys.argv[2]) if len(sys.argv)>2 else 60
rotation=len(sys.argv)>3 and sys.argv[3]=='rotation'
suffix='_rot' if rotation else ''
rng=random.Random(20260920);start=time.monotonic();states=[{},{}];best=[999,999]
inputs=[json.loads((p/f'{x}_n{n}.json').read_text())['pd'] for x in ['PREBLOW','GOMPF6']]
def new(pd):return regina.Link.fromPD([[int(x)+1 for x in row] for row in pd])
def reduce(L,moves):
 while True:
  changed=False
  for kind in [1,2]:
   for i in range(L.size()):
    if getattr(L,f'hasR{kind}')(L.crossing(i)):
     assert getattr(L,f'r{kind}')(L.crossing(i));moves.append([kind,i]);changed=True;break
   if changed:break
  if not changed:return
iterations=0;hit=None
while time.monotonic()-start<limit and hit is None:
 for side in [0,1]:
  L=new(inputs[side]);moves=[]
  for step in range(300):
   reduce(L,moves);sig=L.sig(False,True,rotation);iterations+=1
   if L.size()<best[side]:best[side]=L.size();print('best',side,best[side],len(moves),flush=True)
   if sig in states[1-side]:
    hit={'n':n,'seed':20260920,'source_names':['PREBLOW','GOMPF6'],'inputs':inputs,'signature':sig,'signature_options':[False,True,rotation],'paths':[None,None],'end_pd':[None,None],'status':'CANDIDATE_MOVIE_ENDPOINT_MATCH_REQUIRES_COLOURED_CHECK'}
    hit['paths'][side]=moves[:];hit['paths'][1-side]=states[1-side][sig]['moves'];hit['end_pd'][side]=L.pd();hit['end_pd'][1-side]=states[1-side][sig]['pd'];break
   if sig not in states[side]:states[side][sig]={'moves':moves[:],'pd':L.pd()}
   opts=[(i,s) for i in range(L.size()) for s in [0,1] if L.hasR3(L.crossing(i),s)]
   if not opts:break
   i,s=rng.choice(opts);assert L.r3(L.crossing(i),s);moves.append([3,i,s])
   if time.monotonic()-start>limit:break
  if hit:break
result={'n':n,'seconds':time.monotonic()-start,'iterations':iterations,'states':list(map(len,states)),'best_crossings':best,'hit':hit}
(p/f'MOVIE_SEARCH_n{n}{suffix}.json').write_text(json.dumps(result,indent=2)+'\n')
print({k:v for k,v in result.items() if k!='hit'},'hit',bool(hit),flush=True)
