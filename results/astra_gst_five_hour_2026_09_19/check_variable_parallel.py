from pathlib import Path
import sys,json,snappy
p=Path(__file__).parent;sys.path.insert(0,str(p.resolve().parents[1]/'scripts'))
from variable_parallel import parallel
from cable import cable_braid
rows=[]
for name in ['3_1','4_1','6_1']:
 w=snappy.Link(name).braid_word()
 for mult in [2,3]:
  L,r=parallel(w,[mult]);ref,_=cable_braid(w,max(map(abs,w))+1,mult,0,sum(1 if x>0 else -1 for x in w));assert ref==r['output_braid'];rows.append({'name':name,'multiplicity':mult,'legacy_braid_agrees':True,'linking_matrix':L.linking_matrix()})
(p/'VARIABLE_PARALLEL_CONTROLS.json').write_text(json.dumps(rows,indent=2)+'\n');print('Six knot-only braid and zero-framing controls pass')
