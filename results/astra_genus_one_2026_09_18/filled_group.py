#!/usr/bin/env python3
"""Bounded Tietze reduction of the explicitly framed surgery complement group."""
import json,sys,signal,time
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'prior/astra_one_commutator_2026_09_18'))
from free_words import red,sub,eliminate
f=json.loads((P/'framed_fox_boundary.json').read_text());m=f['meridians'];ll=f['preferred_longitudes'];rels=f['relators']+[[m[1]]+ll[1],[-m[2]]+ll[2]]
def cap(*x):raise TimeoutError('90-second full filled-group reduction cap')
signal.signal(signal.SIGALRM,cap);signal.alarm(90);t0=time.monotonic()
try:
 gs,rs,im,log=eliminate(rels,keep=[m[0]])
 out={'status':'COMPLETE','source':'surgery_diagram.json / preferred slopes (1,1),(-1,1)','original_generators':f['n_generators'],'original_relators':rels,'remaining_generators':sorted(gs),'remaining_relators':rs,'meridian':sub([m[0]],im),'longitude':sub(ll[0],im),'tietze_moves':log,'generator_images':im,'seconds':time.monotonic()-t0}
except Exception as e:out={'status':'UNKNOWN','reason':type(e).__name__+': '+str(e),'seconds':time.monotonic()-t0}
finally:signal.alarm(0)
(P/'filled_group_certificate.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['original_relators','tietze_moves','generator_images']},indent=2),flush=True)
