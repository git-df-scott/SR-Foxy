#!/usr/bin/env python3
"""Full (not Milnor) link-group presentation, exact Tietze simplification.
The no-R Gauss subdiagram is taken directly, without any Reidemeister shortcut.
"""
import json,sys,time,signal
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'prior/astra_one_commutator_2026_09_18'))
from free_words import red,inv,mul,sub,eliminate
from polygon_diagram import sublink
from framed_fox_boundary import build

def main():
 d=json.loads((P/'surgery_diagram.json').read_text());words=sublink(d,[1,2]);raw=build(words);rels=raw['relators'];t0=time.monotonic()
 def cap(*x):raise TimeoutError('90-second Tietze simplification cap')
 signal.signal(signal.SIGALRM,cap);signal.alarm(90)
 try:
  gs,rs,images,log=eliminate(rels)
  absent=set(range(1,raw['n_generators']+1))-set(images)
  gs|=absent;images.update({a:(a,) for a in absent})
  out={'status':'COMPLETE','input_generators':raw['n_generators'],'input_relators':rels,'input_meridians':raw['meridians'],'input_longitudes':raw['preferred_longitudes'],'remaining_generators':sorted(gs),'remaining_relators':rs,'generator_images':images,'moves':log,'meridian_images':[sub([m],images) for m in raw['meridians']],'longitude_images':[sub(w,images) for w in raw['preferred_longitudes']],'seconds':time.monotonic()-t0}
 except Exception as e:out={'status':'UNKNOWN','reason':type(e).__name__+': '+str(e),'seconds':time.monotonic()-t0}
 finally:signal.alarm(0)
 (P/'auxiliary_group_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k not in ('input_relators','generator_images','moves','input_longitudes')},indent=2),flush=True)
if __name__=='__main__':main()
