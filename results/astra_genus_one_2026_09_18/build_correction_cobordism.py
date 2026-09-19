#!/usr/bin/env python3
"""Attach the torus and the explicit splice strip to a displaced old-axis collar.
This produces a genus-one surface with TWO boundary components, not an annulus.
"""
from pathlib import Path
from collections import defaultdict,Counter
import json
from mesh_check import check,sub,cross,dot,SCALE
from check_spatial_marking import seg_tri_hit
P=Path(__file__).resolve().parent

def quant(v):return tuple(int(round(x*SCALE)) for x in v)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def build():
 d=json.loads((P/'spatial_model.json').read_text());s=json.loads((P/'surgery_link.json').read_text());mesh=json.loads((P/'surface_mesh.json').read_text());v=[tuple(x) for x in mesh['vertices']];faces=[list(x) for x in mesh['faces']];index={x:i for i,x in enumerate(v)}
 def vid(x):
  x=tuple(x)
  if x not in index:index[x]=len(v);v.append(x)
  return index[x]
 eps=s['splice_half_width'];plus=[quant([a+eps*b for a,b in zip(c,w)]) for c,w in zip(s['splice_core'],s['splice_width_vectors'])];minus=[quant([a-eps*b for a,b in zip(c,w)]) for c,w in zip(s['splice_core'],s['splice_width_vectors'])]
 # Subdivide the one torus boundary edge containing the band attachment.
 ka=quant(d['correction_boundary'][-1]);kb=quant(d['correction_boundary'][0]);i,j=index[ka],index[kb]
 attached=0;new=[]
 for f in faces:
  if i not in f or j not in f:new.append(f);continue
  z=next(k for k in f if k not in (i,j));pts=[ka,plus[-1],minus[-1],kb]
  # Sort along the actual edge independently of the band orientation.
  axis=max(range(3),key=lambda a:abs(kb[a]-ka[a]));pts=sorted(pts,key=lambda x:x[axis],reverse=kb[axis]<ka[axis]);ids=list(map(vid,pts))
  for a,b in zip(ids,ids[1:]):new.append([z,a,b])
  attached+=1
 if attached!=1:raise ValueError(f'torus attachment edge has {attached} incident triangles')
 faces=new
 # The narrow joining ribbon itself.
 ip=list(map(vid,plus));im=list(map(vid,minus))
 for z in range(len(plus)-1):faces.extend([[ip[z],im[z],ip[z+1]],[im[z],im[z+1],ip[z+1]]])
 # A fixed old-axis collar. Its inner boundary b^- is an explicit small isotopic
 # displacement of b. The outer boundary is b except along the splice interval.
 b=[quant(x) for x in d['base_components'][2]];bouter=b+[minus[0],plus[0]]
 inner=[(x,y,z-10**7) for x,y,z in bouter]  # exactly 10^-5 in z.
 io=list(map(vid,bouter));ii=list(map(vid,inner))
 for z in range(len(io)):
  w=(z+1)%len(io);faces.extend([[io[z],ii[z],io[w]],[ii[z],ii[w],io[w]]])
 return d,s,v,faces,inner

def topology_details(v,f):
 edges=Counter(tuple(sorted((x[j],x[(j+1)%3]))) for x in f for j in range(3));be=[e for e,n in edges.items() if n==1];adj=defaultdict(set)
 for a,b in be:adj[a].add(b);adj[b].add(a)
 unseen=set(adj);cycles=[]
 while unseen:
  first=min(unseen);cyc=[first];last=None;cur=first
  while True:
   choices=adj[cur]-({last} if last is not None else set());nxt=min(choices)
   if nxt==first:break
   if nxt in cyc:raise ValueError('boundary is not a simple combinatorial cycle')
   cyc.append(nxt);last,cur=cur,nxt
  unseen-=set(cyc);cycles.append(cyc)
 badlinks=[]
 for vi in range(len(v)):
  link=defaultdict(set)
  for tri in f:
   if vi in tri:
    a,b=[x for x in tri if x!=vi];link[a].add(b);link[b].add(a)
  seen=set();todo=[next(iter(link))]
  while todo:
   a=todo.pop()
   if a in seen:continue
   seen.add(a);todo.extend(link[a]-seen)
  vals=sorted(map(len,link.values()));expected=(vals.count(1)==2 and all(x in (1,2) for x in vals)) if vi in adj else all(x==2 for x in vals)
  if seen!=set(link) or not expected:badlinks.append(vi)
 return cycles,badlinks

def canonical_poly(poly):
 pp=list(poly)
 while True:
  rem=[i for i,x in enumerate(pp) if cross(sub(x,pp[i-1]),sub(pp[(i+1)%len(pp)],x))==(0,0,0) and dot(sub(x,pp[i-1]),sub(pp[(i+1)%len(pp)],x))>=0]
  if not rem:break
  pp=[x for i,x in enumerate(pp) if i not in rem]
 def rotation(p):k=min(range(len(p)),key=lambda i:p[i]);return tuple(p[k:]+p[:k])
 return min(rotation(pp),rotation(pp[::-1]))

if __name__=='__main__':
 d,s,v,f,inner=build();out=check(v,f);cycles,badlinks=topology_details(v,f);out['bad_vertex_links']=badlinks
 desired=[canonical_poly(inner),canonical_poly([quant(x) for x in s['components'][2]])];actual=[canonical_poly([v[i] for i in cyc]) for cyc in cycles]
 out['boundary_polygons_match']=sorted(actual)==sorted(desired);hits=[];pairs=0
 for ci,poly in enumerate(d['base_components'][:2]):
  poly=list(map(quant,poly))
  for ei,u in enumerate(poly):
   w=poly[(ei+1)%len(poly)]
   for fi,face in enumerate(f):
    tri=[v[k] for k in face]
    if any(max(u[k],w[k])<min(x[k] for x in tri) or min(u[k],w[k])>max(x[k] for x in tri) for k in range(3)):continue
    pairs+=1;r=seg_tri_hit(u,w,tri)
    if r:hits.append([ci,ei,fi,r])
 out['R_a_surface_candidate_pairs']=pairs;out['R_a_intersections']=hits;out['complete_surface_valid']=out['complete'] and not out['bad_triangle_pairs'] and not badlinks and not hits and out['boundary_polygons_match'] and out['orientable'] and out['boundary_components']==2 and out['euler_characteristic']==-2
 result={'status':'EXACT_PL_GENUS_ONE_COBORDISM' if out['complete_surface_valid'] else 'INVALID_OR_INCOMPLETE_GEOMETRY','denominator':SCALE,'vertices':v,'faces':f,'boundary_vertex_cycles':cycles,'check':out,'meaning':'Embedded genus-one correction surface from an isotopic pushoff b^- to b_prime, disjoint from R and a. NOT a modifying annulus from a to b_prime.'}
 (P/'correction_cobordism_mesh.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(out,indent=2))
