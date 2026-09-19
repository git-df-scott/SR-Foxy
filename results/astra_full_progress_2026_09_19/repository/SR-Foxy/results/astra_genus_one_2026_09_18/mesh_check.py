#!/usr/bin/env python3
"""Integer/Fraction triangle intersection checker for the proposed torus mesh."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict,Counter,deque
import json,itertools,time
P=Path(__file__).resolve().parent;SCALE=10**12

def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def det(a,b):return a[0]*b[1]-a[1]*b[0]

def pair_ok(a,b,ids_a,ids_b):
 n=cross(sub(a[1],a[0]),sub(a[2],a[0]));m=cross(sub(b[1],b[0]),sub(b[2],b[0]))
 da=[dot(m,sub(x,b[0])) for x in a];db=[dot(n,sub(x,a[0])) for x in b]
 if min(da)>0 or max(da)<0 or min(db)>0 or max(db)<0:return True
 common=set(ids_a)&set(ids_b);shared=[a[ids_a.index(i)] for i in common]
 v=cross(n,m)
 if v!=(0,0,0):
  j=max(range(3),key=lambda k:abs(v[k]))
  def interval(t,d):
   pts=[F(t[i][j]) for i in range(3) if d[i]==0]
   for i in range(3):
    k=(i+1)%3
    if d[i]*d[k]<0:pts.append(F(t[i][j]*d[k]-t[k][j]*d[i],d[k]-d[i]))
   return None if not pts else (min(pts),max(pts))
  A=interval(a,da);B=interval(b,db)
  if A is None or B is None:return True
  lo,hi=max(A[0],B[0]),min(A[1],B[1])
  if lo>hi:return True
  if not shared:return False
  if len(shared)==1:return lo==hi==shared[0][j]
  return min(x[j] for x in shared)<=lo<=hi<=max(x[j] for x in shared)
 # Coplanar convex polygon intersection, dropping a nonzero normal coordinate.
 if any(da) or any(db):return True
 drop=max(range(3),key=lambda k:abs(n[k]));inds=[i for i in range(3) if i!=drop]
 proj=lambda x:tuple(F(x[i]) for i in inds)
 A=list(map(proj,a));B=list(map(proj,b));sg=1 if det(sub(B[1],B[0]),sub(B[2],B[0]))>0 else -1
 poly=A
 for i in range(3):
  u,w=B[i],B[(i+1)%3];edge=sub(w,u)
  def side(x):return sg*det(edge,sub(x,u))
  new=[]
  for k,x in enumerate(poly):
   y=poly[(k+1)%len(poly)];sx,sy=side(x),side(y)
   if sx>=0:new.append(x)
   if (sx<0<sy) or (sy<0<sx):new.append(tuple((x[j]*sy-y[j]*sx)/(sy-sx) for j in range(2)))
  poly=list(dict.fromkeys(new))
  if not poly:return True
 if not shared:return False
 ss=list(map(proj,shared))
 if len(ss)==1:return all(x==ss[0] for x in poly)
 u,w=ss[:2];ed=sub(w,u)
 return all(det(ed,sub(x,u))==0 and all(min(u[j],w[j])<=x[j]<=max(u[j],w[j]) for j in range(2)) for x in poly)

def buildmesh(model):
 import numpy as np
 root=np.array(model['root']);eps=model['band_half_width'];half=5.;vertices=[];index={};faces=[]
 def vid(x):
  key=tuple(int(round(v*SCALE)) for v in x)
  if key not in index:index[key]=len(vertices);vertices.append(key)
  return index[key]
 disk=[(-half,-eps),(-half,-half),(-eps,-half),(eps,-half),(half,-half),(half,-eps),(half,eps),(half,half),(eps,half),(-eps,half),(-half,half),(-half,eps)]
 dd=[vid(root+[x,y,0]) for x,y in disk];cent=vid(root)
 for i in range(len(dd)):faces.append([cent,dd[i],dd[(i+1)%len(dd)]])
 for h,(core,frames) in enumerate(zip(model['band_cores'],model['band_width_vectors'])):
  cc=np.array(core);ww=np.array(frames);target=np.array([0,1,0]) if h==0 else np.array([-1,0,0]);ww[0]=ww[-1]=target
  plus=[vid(c+eps*w) for c,w in zip(cc,ww)];minus=[vid(c-eps*w) for c,w in zip(cc,ww)]
  for i in range(len(core)-1):faces.extend([[plus[i],minus[i],plus[i+1]],[minus[i],minus[i+1],plus[i+1]]])
 return vertices,faces

def check(vertices,faces,max_errors=10):
 t0=time.monotonic();edges=defaultdict(list)
 for i,f in enumerate(faces):
  for j in range(3):
   u,v=f[j],f[(j+1)%3];edges[tuple(sorted((u,v)))].append((i,1 if u<v else -1))
 manifold=all(len(v)<=2 for v in edges.values());be=[e for e,a in edges.items() if len(a)==1];adj=defaultdict(set)
 for u,v in be:adj[u].add(v);adj[v].add(u)
 unseen=set(adj);ncomp=0
 while unseen:
  ncomp+=1;todo=[unseen.pop()]
  while todo:
   for w in adj[todo.pop()]:
    if w in unseen:unseen.remove(w);todo.append(w)
 # Face orientability equations.
 fadj=defaultdict(list)
 for a in edges.values():
  if len(a)==2:
   (i,s),(j,t)=a;fadj[i].append((j,-s*t));fadj[j].append((i,-s*t))
 orient={};orientable=True
 for i in range(len(faces)):
  if i in orient:continue
  orient[i]=1;todo=[i]
  while todo:
   a=todo.pop()
   for b,sg in fadj[a]:
    value=orient[a]*sg
    if b in orient and orient[b]!=value:orientable=False
    elif b not in orient:orient[b]=value;todo.append(b)
 boxes=[];deg=[]
 for i,f in enumerate(faces):
  aa=[vertices[j] for j in f];bb=tuple((min(a[k] for a in aa),max(a[k] for a in aa)) for k in range(3));boxes.append(bb)
  if cross(sub(aa[1],aa[0]),sub(aa[2],aa[0]))==(0,0,0):deg.append(i)
 errors=[];active=[];pairs=0
 for i in sorted(range(len(faces)),key=lambda i:boxes[i][0][0]):
  box=boxes[i];active=[j for j in active if boxes[j][0][1]>=box[0][0]]
  for j in active:
   if any(box[k][0]>boxes[j][k][1] or boxes[j][k][0]>box[k][1] for k in (1,2)):continue
   pairs+=1
   if not pair_ok([vertices[k] for k in faces[i]],[vertices[k] for k in faces[j]],faces[i],faces[j]):
    errors.append([i,j]);
    if len(errors)>=max_errors:break
  if len(errors)>=max_errors:break
  active.append(i)
 return {'vertices':len(vertices),'edges':len(edges),'faces':len(faces),'euler_characteristic':len(vertices)-len(edges)+len(faces),'boundary_components':ncomp,'boundary_valence_two':all(len(a)==2 for a in adj.values()),'combinatorial_manifold':manifold,'orientable':orientable,'degenerate_faces':deg,'tested_candidate_pairs':pairs,'bad_triangle_pairs':errors,'complete':len(errors)<max_errors,'seconds':time.monotonic()-t0}
if __name__=='__main__':
 d=json.loads((P/'spatial_model.json').read_text());v,f=buildmesh(d);out=check(v,f);print(out,flush=True)
 (P/'surface_mesh.json').write_text(json.dumps({'denominator':SCALE,'vertices':v,'faces':f,'check':out},indent=2)+'\n')
