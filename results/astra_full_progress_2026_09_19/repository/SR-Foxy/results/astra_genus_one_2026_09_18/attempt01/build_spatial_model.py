#!/usr/bin/env python3
"""Experimental explicit polygonal ribbon-graph realization.
Outputs are labelled PROTOTYPE until embedding, marking and unlink checks pass.
No change to original repository. Uses numerical geometry for planning only.
"""
import json,math,itertools,time
from pathlib import Path
import numpy as np
from shapely.geometry import LineString,Point,Polygon
from shapely.ops import unary_union
import networkx as nx
P=Path(__file__).resolve().parent
base=json.loads((P/'planar_base.json').read_text());pos={tuple(k):np.array(v,float) for k,v in base['positions']}
paths=[];seglabels=[]
for loop in base['oriented_traversals']:
 path=[];labs=[]
 for c,p in loop:
  out=(p+2)%4;mate=base['adjacency'][str(c)][out]
  path.extend([np.r_[pos['c',c],int(p%2==1)],np.r_[pos['p',c,out],0.],np.r_[pos['p',*mate],0.]])
  labs.extend([base['R_port_marked_generator'].get(f'{c},{out}'),base['R_port_marked_generator'].get(f'{c},{out}'),base['R_port_marked_generator'].get(f'{mate[0]},{mate[1]}')])
 paths.append(path);seglabels.append(labs)
R=paths[0]
Aword=[4,-3,-3,1];Bword=[4,-9,-1,3,-1,8,-5,-8,1,1]
# B is marked opposite to its south-to-north band core.
words=[Aword,[-x for x in Bword[::-1]]]
allwords=[x for w in words for x in w];counts={i:sum(abs(x)==i for x in allwords) for i in set(map(abs,allwords))}
anchors={}
for j,g in enumerate(seglabels[0]):
 v,w=R[j],R[(j+1)%len(R)]
 if g and v[2]==w[2]==0:
  ell=np.linalg.norm(w-v)
  if ell>0 and (g not in anchors or ell>anchors[g][0]):anchors[g]=(ell,j,v,w)
used={g:0 for g in counts};targets=[]
for h,ww in enumerate(words):
 tt=[]
 for letter in ww:
  g=abs(letter);sg=1 if letter>0 else -1;used[g]+=1;L,j,v,w=anchors[g];f=used[g]/(counts[g]+1);c=v*(1-f)+w*f;e=(w-v)/L;n=np.array([-e[1],e[0],0.])
  # Select a disk that meets just this straight R segment.
  distances=[]
  for k in range(len(R)):
   if k==j:continue
   u,z=R[k],R[(k+1)%len(R)];u2,z2=u[:2],z[:2]
   if np.linalg.norm(z2-u2)>0:distances.append(Point(c[:2]).distance(LineString([u2,z2])))
  r=min(.015,min(x for x in distances if x>1e-10)/12,L/(counts[g]+1)/12)
  tt.append({'letter':letter,'component_segment':j,'center':c.tolist(),'e':e.tolist(),'n':n.tolist(),'radius':r,'sign':sg})
 targets.append(tt)
print('targets',len(allwords),'radii',min(d['radius'] for a in targets for d in a),max(d['radius'] for a in targets for d in a),flush=True)
# Route each baseline band in its own horizontal plane, avoiding its already
# constructed path and the vertical footprints of all other finger disks.
root=np.array([900.,400.,500.]);half=5.;H=[520.,540.]
ports=[(root+[-half,0,0],root+[half,0,0]),(root+[0,-half,0],root+[0,half,0])]
alltargets=[d for a in targets for d in a]
EPS=1e-7

def visibility_route(start,end,obstacles):
 start=np.asarray(start);end=np.asarray(end)
 if np.linalg.norm(start-end)<1e-12:return [start,end]
 # Buffer footprints/past arcs so a found open path has geometric clearance.
 obs=unary_union(obstacles) if obstacles else Polygon()
 clear=obs.buffer(-1e-10)
 segment=LineString([start,end])
 if not segment.intersects(clear):return [start,end]
 geoms=list(obs.geoms) if hasattr(obs,'geoms') else [obs]
 vv=[start,end]
 for po in geoms:
  if not isinstance(po,Polygon):continue
  vv.extend(np.array(x) for x in list(po.exterior.coords)[:-1])
 # Remove duplicates before visibility enumeration.
 vv=list({tuple(np.round(v,10)):v for v in vv}.values());si=next(i for i,v in enumerate(vv) if np.linalg.norm(v-start)<1e-8);ei=next(i for i,v in enumerate(vv) if np.linalg.norm(v-end)<1e-8)
 gr=nx.Graph();gr.add_nodes_from(range(len(vv)))
 from shapely.prepared import prep
 pr=prep(clear)
 for i in range(len(vv)):
  for j in range(i):
   line=LineString([vv[i],vv[j]])
   if not pr.intersects(line):gr.add_edge(i,j,weight=float(np.linalg.norm(vv[i]-vv[j])))
 route=nx.shortest_path(gr,si,ei,weight='weight')
 return [vv[i] for i in route]

cores=[];frames=[];baseline=[];route_logs=[]
for h,tt in enumerate(targets):
 start,end=ports[h];outdir=np.array([-1.,0.]) if h==0 else np.array([0.,-1.]);enddir=-outdir
 pts=[start[:2],start[:2]+outdir*2];events=[]
 for k,d in enumerate(tt):
  c=np.array(d['center'])[:2];n=np.array(d['n'])[:2];r=d['radius'];sg=d['sign'];entry=c-sg*3*r*n;exit=c+sg*3*r*n
  prior=LineString(pts)
  # Permit departing from the current endpoint, not passing through old arcs.
  old=prior.buffer(EPS*30,cap_style=2,join_style=2).difference(Point(pts[-1]).buffer(EPS*80,resolution=4))
  obstacles=[old]
  for other in alltargets:
   if other is d:continue
   obstacles.append(Point(other['center'][:2]).buffer(other['radius']*1.5,resolution=4))
  path=visibility_route(pts[-1],entry,obstacles)
  pts.extend(path[1:]);idx=len(pts)-1
  # Fixed approach direction and a short core segment are replaced by the
  # complement of the top edge of the specified vertical meridian disk.
  pts.extend([c-sg*r/4*n,c+sg*r/4*n,exit]);events.append((idx+1,d))
  print('routed',h,k,'vertices',len(pts),flush=True)
 prior=LineString(pts);old=prior.buffer(EPS*30,cap_style=2,join_style=2).difference(Point(pts[-1]).buffer(EPS*80,resolution=4))
 finish=end[:2]+enddir*2
 obstacles=[old]+[Point(d['center'][:2]).buffer(d['radius']*1.5,resolution=4) for d in alltargets]
 pts.extend(visibility_route(pts[-1],finish,obstacles)[1:]);pts.append(end[:2])
 simple=LineString(pts).is_simple
 print('baseline simple',h,simple,'vertices',len(pts),flush=True)
 baseline.append([np.r_[v,H[h]].tolist() for v in pts])
 ev={i:d for i,d in events};core=[];force=[];j=0
 core.append(start.copy());force.append(np.r_[-outdir[1],outdir[0],0.])
 while j<len(pts):
  if j in ev:
   d=ev[j];c=np.array(d['center']);n=np.array(d['n']);e=np.array(d['e']);r=d['radius'];sg=d['sign'];zH=H[h]
   # Coordinates in the (n,z) plane, traversed positive or negative.
   paddle=[(-r/4,zH),(-r/4,r/2),(-r,0),(0,-r),(r,0),(r/4,r/2),(r/4,zH)]
   if sg<0:paddle=paddle[::-1]
   for u,z in paddle:core.append(c+n*u+np.array([0.,0.,z]));force.append(sg*e)
   j+=2
  else:core.append(np.r_[pts[j],H[h]]);force.append(None);j+=1
 core.append(end.copy());force.append(np.r_[enddir[1],-enddir[0],0.])
 W=[]
 for i,v in enumerate(core):
  if force[i] is not None:w=force[i]
  else:
   u=core[max(0,i-1)];z=core[min(len(core)-1,i+1)];a=v-u;b=z-v
   aa=a[:2]/max(np.linalg.norm(a[:2]),1e-20);bb=b[:2]/max(np.linalg.norm(b[:2]),1e-20);tan=aa+bb
   if np.linalg.norm(tan)<1e-12:tan=aa if np.linalg.norm(aa)>0 else bb
   w=np.array([tan[1],-tan[0],0.]);w/=max(np.linalg.norm(w),1e-20)
  W.append(w)
 cores.append(core);frames.append(W);route_logs.append({'simple_baseline':simple,'events':[(i,d['letter']) for i,d in events]})
# Exact band-side connectivity for the alternating A,B handle attachments.
width=EPS
sides=[]
for core,W in zip(cores,frames):sides.append(([c+width*w for c,w in zip(core,W)],[c-width*w for c,w in zip(core,W)]))
# Force attachment widths to match the root disk parametrization.
# A traverses west->east: positive side north. B south->north: positive west.
for h in range(2):
 targetw=np.array([0.,1.,0.]) if h==0 else np.array([-1.,0.,0.])
 for endi in (0,-1):
  sides[h][0][endi]=cores[h][endi]+width*targetw;sides[h][1][endi]=cores[h][endi]-width*targetw
Ap,Am=sides[0];Bp,Bm=sides[1]
# Boundary: A, inverse(B_core), inverse(A), B_core; B_core = inverse(B).
knot=[]
def append(v):
 for x in v:
  if not knot or np.linalg.norm(x-knot[-1])>1e-14:knot.append(x)
append(Ap);append([root+[half,half,0]]);append(Bm[::-1]);append([root+[half,-half,0]]);append(Am[::-1]);append([root+[-half,-half,0]]);append(Bp);append([root+[-half,half,0]])
# This k is the isolated correction knot. A later splice must identify the
# root band with the recorded basing on the existing axis b.
out={'status':'EXPERIMENTAL_SPATIAL_MODEL_NOT_YET_VALIDATED','source_commit':'ceb83c2c86c4b538599f95b62812587d2fa3c6fe','base_components':[[v.tolist() for v in p] for p in paths],'base_segment_generators':seglabels,'root':root.tolist(),'band_half_width':width,'targets':targets,'baseline_bands':baseline,'band_cores':[[v.tolist() for v in c] for c in cores],'band_width_vectors':[[v.tolist() for v in c] for c in frames],'correction_boundary':[v.tolist() for v in knot],'routes':route_logs,'A_word':Aword,'B_word':Bword,'qualifications':['Coordinates are planning floats. No exact embedding, marking, framing, auxiliary-unlink or surgery-boundary certificate yet.','The displayed core carries geometric meridian excursions; root/axis splice remains to be made.']}
(P/'spatial_model.json').write_text(json.dumps(out,indent=2)+'\n')
print('saved model',len(knot),'correction polygon vertices',flush=True)
