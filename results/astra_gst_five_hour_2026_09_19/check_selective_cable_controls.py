"""Replay braid agreement and deliberately wrong-framing negative controls."""
import sys,json,snappy
from pathlib import Path
p=Path(__file__).parent;sys.path.insert(0,str(p.resolve().parents[1]/'scripts'))
from selective_cable import double_component
from cable import cable_braid
rows=[]
for name in ['3_1','4_1','6_1']:
 K=snappy.Link(name);w=K.braid_word();C,r=double_component(w,0)
 other,ns=cable_braid(w,max(map(abs,w))+1,2,0,sum(1 if x>0 else -1 for x in w));assert other==r['output_braid']
 wrong=snappy.Link(braid_closure=r['output_braid']+[1,1]);assert wrong.linking_matrix()[0][1]!=0
 rows.append({'name':name,'input_braid':w,'output_braid':r['output_braid'],'self_writhe':r['self_writhe'],'legacy_braid_implementation_agrees':True,'correct_linking_matrix':C.linking_matrix(),'deliberately_wrong_framing_linking_matrix':wrong.linking_matrix()})
(p/'SELECTIVE_CABLE_FRAMING_AUDIT.json').write_text(json.dumps(rows,indent=2)+'\n');print('Three implementation-agreement checks and three wrong-framing controls passed')
