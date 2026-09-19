#!/usr/bin/env python3
import json,sys,time,signal
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'prior/astra_one_commutator_2026_09_18'))
from free_words import red,inv,mul,sub,eliminate
from polygon_diagram import sublink,reduce_gauss

def group(words):
 crossings={};gens=0;longs=[];mers=[];arcsbyevent=[]
 for ci,w in enumerate(words):
  n=sum(kind=='U' for k,kind,s in w)
  if not n:
   gens+=1;mers.append(gens);longs.append([]);arcsbyevent.append([]);continue
  start=gens+1;gens+=n;mer=start;current=start;mers.append(mer);arc=[]
  for k,kind,s in w:
   crossings.setdefault(k,{'sign':s})
   if kind=='O':crossings[k]['over']=current
   else:
    nxt=start+(current-start+1)%n;crossings[k]['in']=current;crossings[k]['out']=nxt;current=nxt
   arc.append(current)
  arcsbyevent.append(arc)
 rels=[]
 for k,c in sorted(crossings.items()):
  b=c['over'];ss=c['sign'];rels.append([-ss*b,c['in'],ss*b,-c['out']])
 return gens,rels,crossings

def capped_eliminate(rels,seconds=15):
 def cap(*a):raise TimeoutError('bounded Tietze cap')
 signal.signal(signal.SIGALRM,cap);signal.alarm(seconds)
 try:
  gs,rs,im,log=eliminate(rels)
  return {'status':'COMPLETE','remaining_generators':sorted(gs),'remaining_relators':rs,'steps':len(log),'cyclic_group':len(gs)==1 and len(rs)==0}
 except Exception as e:return {'status':'UNKNOWN','reason':type(e).__name__+': '+str(e)}
 finally:signal.alarm(0)
if __name__=='__main__':
 d=json.loads((P/'projected_model.json').read_text());out={}
 for name,comps in [('correction',[3]),('base_aux',[1,2])]:
  rr=reduce_gauss(sublink(d,comps));n,rels,c=group(rr['remaining']);print(name,'gens',n,'relators',len(rels),flush=True)
  # Empty Gauss words represent visible crossing-free components.
  ans=capped_eliminate(rels) if rels else {'status':'CROSSING_FREE','components':len(comps)};print(ans,flush=True);out[name]=ans
 (P/'gauss_group_probe.json').write_text(json.dumps(out,indent=2)+'\n')
