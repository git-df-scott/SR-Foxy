"""Enumerate untwisted orientable saddle bands inside single faces of fixed PD.
Negative output concerns exactly this finite class, not arbitrary ribbon disks.
No knot/link recognition is inferred from Alexander polynomials.
"""
import json,itertools,collections,time
from pathlib import Path
from pd_algebra import *
ROOT=Path(__file__).parent
pd=json.loads((ROOT/'gst48.json').read_text())['pd']; st=structure(pd)
seen=set(); results=[]; bad=[]
start=time.time()
for face_id,face in enumerate(st['faces']):
 for da,db in itertools.combinations(face,2):
  a,b=pd[da[0]][da[1]],pd[db[0]][db[1]]
  if a==b or (da in st['outgoing']) != (db in st['outgoing']):continue
  key=tuple(sorted((a,b)))
  # Retain the first face witness for each identical resulting reconnection.
  if key in seen:continue
  seen.add(key)
  ina=st['alpha'][da] if da in st['outgoing'] else da
  inb=st['alpha'][db] if db in st['outgoing'] else db
  new=[q[:] for q in pd]; new[ina[0]][ina[1]]=b; new[inb[0]][inb[1]]=a
  ss=structure(new)
  # Euler characteristic 2 for each component of the embedded projection graph.
  uf=DSU(range(len(new)))
  for d,e in ss['alpha'].items():uf.union(d[0],e[0])
  cc=len({uf.find(i) for i in range(len(new))})
  assert len(ss['faces'])-len(new)==2*cc
  assert len(ss['tours'])==2
  pieces=[component_pd(new,k,ss) for k in range(2)]
  dets=[determinant(p) for p in pieces]
  lk=linking_numbers(new,ss).get((0,1),0)
  results.append({'face':face_id,'edge_labels':list(key),'attachment_darts':[list(da),list(db)],'swapped_incoming_darts':[list(ina),list(inb)],'component_crossings':[len(p) for p in pieces],'component_determinants':dets,'linking_number':lk})
  if len(results)%50==0:print(len(results),'elapsed',round(time.time()-start,2),flush=True)
print('total',len(results),'det pair counts',collections.Counter(tuple(sorted(r['component_determinants'])) for r in results))
for r in results:
 if sorted(r['component_determinants']) in [[9,9],[1,1]]:
  a,b=r['edge_labels'];ina,inb=r['swapped_incoming_darts']
  # swapped darts were associated with unsorted a,b above: simply swap their current entries
  new=[q[:] for q in pd];new[ina[0]][ina[1]],new[inb[0]][inb[1]]=new[inb[0]][inb[1]],new[ina[0]][ina[1]]
  ss=structure(new)
  pol=[alexander(component_pd(new,k,ss)) for k in range(2)]
  r['component_alexander_coefficients']=[[int(p.coeff(t,i)) for i in range(s.degree(p,t)+1)] for p in pol]
  r['resulting_pd']=new
  print('SELECT',r['edge_labels'],'lk',r['linking_number'],'cross',r['component_crossings'],'polys',[s.factor(p) for p in pol],flush=True)
(ROOT/'face_band_results.json').write_text(json.dumps({'scope':'One orientable untwisted band with core lying within one complementary face of this fixed planar diagram; duplicate edge reconnections collapsed. No Reidemeister changes, added crossings, self-crossings, or extra bands.','total':len(results),'records':results},indent=2)+'\n')
