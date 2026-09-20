"""Seifert-framed two-parallel of one braid-closure component.
Uses actual braid self-writhe, never the writhe of the input non-braid diagram.
"""
import snappy

def data(word):
 n=max(map(abs,word))+1;position=list(range(n))
 for g in word:i=abs(g)-1;position[i],position[i+1]=position[i+1],position[i]
 cycles=[];unused=set(range(n))
 while unused:
  x=min(unused);cycle=[]
  while x not in cycle:cycle.append(x);unused.remove(x);x=position[x]
  cycles.append(cycle)
 colors={s:i for i,c in enumerate(cycles) for s in c};return n,cycles,colors

def double_component(word,component):
 n,cycles,colors=data(word);width={s:2 if colors[s]==component else 1 for s in range(n)};positions=list(range(n));out=[];w=0
 for g in word:
  i=abs(g)-1;sgn=1 if g>0 else -1;a,b=positions[i:i+2];p,q=width[a],width[b];base=sum(width[s] for s in positions[:i])
  for u in range(p):
   for z in range(q):out.append(sgn*(base+p-u+z))
  if colors[a]==colors[b]==component:w+=sgn
  positions[i],positions[i+1]=b,a
 anchor=min(cycles[component]);base=sum(width[s] for s in range(anchor));out.extend(([base+1] if w<0 else [-(base+1)])*(2*abs(w)))
 ns=sum(width.values())
 if not out or max(map(abs,out))<ns-1:out.extend([ns-1,-(ns-1)])
 L=snappy.Link(braid_closure=out)
 assert len(L.link_components)==len(cycles)+1
 mat=L.linking_matrix()
 return L,{'input_braid':word,'cycles':cycles,'doubled_cycle':component,'self_writhe':w,'framing_half_twists':-2*w,'output_braid':out,'linking_matrix':mat,'pd':L.PD_code()}

if __name__=='__main__':
 import json
 from pathlib import Path
 from collections import Counter
 import regina
 p=Path(__file__).parent
 controls=[]
 for word,ci in [([1,-1],0),([1,1,1],0),([1,1,1,2,-2],0),([1,1,1,2,-2],1)]:
  C,r=double_component(word,ci);assert all(x==0 for row in r['linking_matrix'] for x in row)
  rec=[]
  for i in range(len(C.link_components)):
   K=C.sublink([i]);K.simplify('global');rec.append({'crossings':len(K.crossings),'unknot':not K.crossings})
  r['component_controls']=rec;controls.append(r)
 (p/'SELECTIVE_CABLE_CONTROLS.json').write_text(json.dumps(controls,indent=2)+'\n');print([(x['cycles'],x['self_writhe'],x['component_controls']) for x in controls])
