"""Check the recovered planar-map certificate; no source-transcription claim."""
from pathlib import Path
from collections import defaultdict
import json,copy
P=Path(__file__).parent

def alpha(pd):
 occ=defaultdict(list)
 for i,row in enumerate(pd):
  for k,e in enumerate(row):occ[e].append(4*i+k)
 assert all(len(v)==2 for v in occ.values())
 return {a:b for v in occ.values() for a,b in [v,v[::-1]]}

def verify(a,b,f):
 n=4*len(a);assert len(b)*4==n and sorted(f)==list(range(n))
 x,y=alpha(a),alpha(b)
 for d in range(n):
  assert f[x[d]]==y[f[d]],'edge gluing'
  assert f[4*(d//4)+(d+1)%4]==4*(f[d]//4)+(f[d]+1)%4,'cyclic order'
  assert d%2==f[d]%2,'over/under'
 return True
j=json.loads((P/'recovered/figure2_identification.json').read_text())
a,b,f=j['trace_pd'],j['stored_pd'],j['dart_bijection'];verify(a,b,f)
bad=copy.deepcopy(b);bad[0]=bad[0][1:]+bad[0][:1]
rejected=[]
for name,A,B,F in [('crossing_rotation',a,bad,f),('bijection_swap',a,b,[f[1],f[0]]+f[2:])]:
 try:verify(A,B,F)
 except AssertionError:rejected.append(name)
assert len(rejected)==2
result={'status':'PASS','crossings':len(a),'darts':len(f),'edge_gluing_preserved':True,'cyclic_order_preserved':True,'over_under_preserved':True,'corruptions_rejected':rejected,'scope':'Trace PD equals stored PD as marked planar maps. The raster gap transcription and twist handedness remain separate assumptions; no L31 identification.'}
(P/'FIGURE2_REPLAY.json').write_text(json.dumps(result,indent=2));print(result)
