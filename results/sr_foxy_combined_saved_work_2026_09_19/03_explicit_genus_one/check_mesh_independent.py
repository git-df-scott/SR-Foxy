#!/usr/bin/env python3
"""Independent exact edge/triangle clipping check of saved PL surface.
Uses rational segment clipping, not the producer's plane-interval/triangle
polygon-clipping algorithm. Includes synthetic crossing and adjacency controls.
"""
import json,time
from fractions import Fraction as Q
from pathlib import Path
P=Path(__file__).resolve().parent

def minus(a,b):return tuple(x-y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def point(a,b,t):return tuple(Q(x)+t*(y-x) for x,y in zip(a,b))

def clip(a,b,tri):
 n=cross(minus(tri[1],tri[0]),minus(tri[2],tri[0]));da=dot(n,minus(a,tri[0]));db=dot(n,minus(b,tri[0]))
 if da!=db:
  t=Q(da,da-db)
  if not 0<=t<=1:return []
  x=point(a,b,t)
  if any(dot(cross(minus(tri[(i+1)%3],tri[i]),minus(x,tri[i])),n)<0 for i in range(3)):return []
  return [x]
 if da:return []
 lo,hi=Q(0),Q(1)
 for i in range(3):
  edge=minus(tri[(i+1)%3],tri[i]);p=dot(cross(edge,minus(a,tri[i])),n);r=dot(cross(edge,minus(b,tri[i])),n);s=r-p
  if s==0:
   if p<0:return []
  elif s>0:lo=max(lo,Q(-p,s))
  else:hi=min(hi,Q(-p,s))
  if lo>hi:return []
 return list({point(a,b,lo),point(a,b,hi)})

def valid_pair(a,b,common):
 hits=set()
 for t,u in ((a,b),(b,a)):
  for i in range(3):hits.update(clip(t[i],t[(i+1)%3],u))
 if not common:return not hits
 if len(common)==1:return all(x==tuple(common[0]) for x in hits)
 if len(common)==2:
  p,q=common;e=minus(q,p)
  return all(cross(minus(x,p),e)==(0,0,0) and all(min(p[j],q[j])<=x[j]<=max(p[j],q[j]) for j in range(3)) for x in hits)
 return False

def main():
 t0=time.monotonic();m=json.loads((P/'correction_cobordism_mesh.json').read_text());v=m['vertices'];f=m['faces'];tris=[[tuple(v[i]) for i in face] for face in f];boxes=[[(min(x[k] for x in tri),max(x[k] for x in tri)) for k in range(3)] for tri in tris]
 pairs=0;bad=[]
 for i in range(len(f)):
  for j in range(i):
   if any(boxes[i][k][0]>boxes[j][k][1] or boxes[j][k][0]>boxes[i][k][1] for k in range(3)):continue
   pairs+=1;common=[tuple(v[k]) for k in set(f[i])&set(f[j])]
   if not valid_pair(tris[i],tris[j],common):bad.append([i,j])
 d=json.loads((P/'spatial_model.json').read_text());base_hits=[];bp=0
 for ci,poly in enumerate(d['base_components'][:2]):
  poly=[tuple(int(round(x*m['denominator'])) for x in p) for p in poly]
  for ei,a in enumerate(poly):
   b=poly[(ei+1)%len(poly)]
   for j,tri in enumerate(tris):
    if any(max(a[k],b[k])<boxes[j][k][0] or min(a[k],b[k])>boxes[j][k][1] for k in range(3)):continue
    bp+=1
    if clip(a,b,tri):base_hits.append([ci,ei,j])
 controls={}
 a=[(0,0,0),(2,0,0),(0,2,0)];b=[(0,0,1),(2,0,1),(0,2,1)];controls['parallel_disjoint']=valid_pair(a,b,[])
 c=[(0,0,0),(2,0,0),(0,-2,0)];controls['shared_edge_allowed']=valid_pair(a,c,a[:2]);controls['coplanar_overlap_rejected']=not valid_pair(a,[(1,0,0),(3,0,0),(1,2,0)],[])
 controls['transverse_intersection_rejected']=not valid_pair(a,[(1,0,-1),(1,0,1),(1,2,0)],[])
 controls['adjacent_vertex_allowed']=valid_pair(a,[(0,0,0),(-2,0,0),(0,-2,0)],[(0,0,0)])
 controls['degenerate_duplicate_face_rejected']=not valid_pair(a,a,a)
 out={'status':'PASS' if not bad and not base_hits and all(controls.values()) else 'FAIL','algorithm':'independent rational segment-clipping enumeration','surface_triangle_pairs':pairs,'surface_bad_pairs':bad,'R_a_candidate_pairs':bp,'R_a_hits':base_hits,'controls':controls,'seconds':time.monotonic()-t0,'scope':'Checks intersections of the saved integer PL mesh and R,a curves; no 4D annulus asserted.'}
 (P/'independent_mesh_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
 if out['status']!='PASS':raise SystemExit(1)
if __name__=='__main__':main()
