#!/usr/bin/env python3
import json
from pathlib import Path
from fractions import Fraction as F
from polygon_diagram import project,D as SCALE
from mesh_check import sub,cross,dot,det
P=Path(__file__).resolve().parent

def seg_tri_hit(u,v,T):
 n=cross(sub(T[1],T[0]),sub(T[2],T[0]));a=dot(n,sub(u,T[0]));b=dot(n,sub(v,T[0]))
 if a*b>0:return False
 if a==b==0:
  # Conservatively flag coplanarity with overlapping bounding boxes; none
  # is expected for the curve-vs-surface instances in this check.
  return 'COPLANAR_UNRESOLVED'
 if a==b:return False
 num,den=a,a-b
 if den<0:num,den=-num,-den
 if not 0<=num<=den:return False
 w=tuple(u[i]*den+num*(v[i]-u[i]) for i in range(3))
 vals=[]
 for i in range(3):
  edge=sub(T[(i+1)%3],T[i]);to=tuple(w[k]-den*T[i][k] for k in range(3));vals.append(dot(cross(edge,to),n))
 return min(vals)>=0

if __name__=='__main__':
 d=json.loads((P/'spatial_model.json').read_text());mesh=json.loads((P/'surface_mesh.json').read_text());root=d['root'];loops=[]
 for h,core in enumerate(d['band_cores']):
  loops.append([root]+(core if h==0 else core[::-1]))
 checks={};allok=True
 for h,loop in enumerate(loops):
  pd=project([d['base_components'][0],loop]);crossings={x['id']:x for x in pd['crossings']};word=[];records=[]
  for k,kind,s in pd['gauss_words'][1]:
   x=crossings[k]
   if kind=='U' and x['over'][0]==0:
    seg=x['over'][1];g=d['base_segment_generators'][0][seg];word.append(s*g);records.append([k,seg,s,g])
  expected=d['A_word'] if h==0 else d['B_word'];ok=word==expected
  print('handle',h,'read',word,'expected',expected,'match',ok,flush=True)
  checks['AB'[h]]={'geometric_undercrossing_word':word,'expected':expected,'matches':ok,'crossing_records':records};allok&=ok
 hits=[];tested=0
 for ci,poly in enumerate(d['base_components']):
  poly=[tuple(int(round(x*SCALE)) for x in v) for v in poly]
  for ei,u in enumerate(poly):
   v=poly[(ei+1)%len(poly)];eb=[(min(u[k],v[k]),max(u[k],v[k])) for k in range(3)]
   for fi,face in enumerate(mesh['faces']):
    tri=[mesh['vertices'][k] for k in face]
    if any(eb[k][1]<min(x[k] for x in tri) or eb[k][0]>max(x[k] for x in tri) for k in range(3)):continue
    tested+=1;r=seg_tri_hit(u,v,tri)
    if r:hits.append([ci,ei,fi,r])
 print('curve/surface intersections',len(hits),'bbox tests',tested,'first',hits[:10],flush=True)
 (P/'spatial_marking_check.json').write_text(json.dumps({'handle_checks':checks,'handle_words_match':allok,'base_curve_surface_candidate_pairs':tested,'base_curve_surface_hits':hits,'surface_disjoint_from_base':not hits,'source_commit':d['source_commit']},indent=2)+'\n')
