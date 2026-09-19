#!/usr/bin/env python3
"""Exact generic projection of integer polygonal links; no topology package."""
import json, itertools
from pathlib import Path
from fractions import Fraction
D=10**12

def det(a,b):return a[0]*b[1]-a[1]*b[0]
def project(polys,projection=(1,1009,2,1013)):
 u,p,v,q=projection;factor=p*q
 xyz=[[[int(round(z*D)) for z in x] for x in poly] for poly in polys]
 seg=[]
 for ci,poly in enumerate(xyz):
  for j,a in enumerate(poly):
   b=poly[(j+1)%len(poly)]
   if a==b:raise ValueError(f'zero segment {ci},{j}')
   aa=(factor*a[0]+u*q*a[2],factor*a[1]+v*p*a[2]);bb=(factor*b[0]+u*q*b[2],factor*b[1]+v*p*b[2]);dd=(bb[0]-aa[0],bb[1]-aa[1])
   if dd==(0,0):raise ValueError('vertical projected segment')
   seg.append({'comp':ci,'idx':j,'a':aa,'d':dd,'za':a[2],'zd':b[2]-a[2],'minx':min(aa[0],bb[0]),'maxx':max(aa[0],bb[0]),'miny':min(aa[1],bb[1]),'maxy':max(aa[1],bb[1])})
 events=[[] for _ in polys];cross=[];checked=0;active=[]
 for ii in sorted(range(len(seg)),key=lambda i:seg[i]['minx']):
  a=seg[ii];active=[jj for jj in active if seg[jj]['maxx']>=a['minx']]
  for jj in active:
   b=seg[jj]
   if a['miny']>b['maxy'] or b['miny']>a['maxy']:continue
   same=a['comp']==b['comp'];N=len(polys[a['comp']])
   if same and (a['idx']-b['idx'])%N in (0,1,N-1):continue
   checked+=1;delta=(b['a'][0]-a['a'][0],b['a'][1]-a['a'][1]);den=det(a['d'],b['d']);na=det(delta,b['d']);nb=det(delta,a['d'])
   if den==0:
    if na==0 and nb==0:raise ValueError(f'non-generic collinear segments {ii},{jj}')
    continue
   if den<0:den,na,nb=-den,-na,-nb
   if not(0<=na<=den and 0<=nb<=den):continue
   if na in (0,den) or nb in (0,den):raise ValueError(f'non-generic vertex crossing {ii},{jj}')
   za=a['za']*den+na*a['zd'];zb=b['za']*den+nb*b['zd']
   if za==zb:raise ValueError(f'ACTUAL_POLYGON_INTERSECTION {ii},{jj}')
   ao=za>zb;sign=(1 if det(a['d'],b['d'])>0 else -1)*(1 if ao else -1)
   k=len(cross);cross.append({'id':k,'over':[a['comp'],a['idx']] if ao else [b['comp'],b['idx']],'under':[b['comp'],b['idx']] if ao else [a['comp'],a['idx']],'sign':sign,'a':[a['comp'],a['idx']],'b':[b['comp'],b['idx']],'ta':[na,den],'tb':[nb,den],'depth_numerator':str(abs(za-zb))})
   events[a['comp']].append((a['idx'],Fraction(na,den),k,'O' if ao else 'U',sign));events[b['comp']].append((b['idx'],Fraction(nb,den),k,'U' if ao else 'O',sign))
  active.append(ii)
 words=[]
 for ee in events:
  ee.sort();words.append([[k,kind,sign] for j,t,k,kind,sign in ee])
 return {'format':'exact-polygon-projection-v1','coordinate_denominator':D,'integer_polygons':xyz,'projection':projection,'crossings':cross,'gauss_words':words,'bbox_pairs_checked':checked,'embedded_polygon_check':True}

def sublink(diagram,components):
 keep={x['id'] for x in diagram['crossings'] if x['over'][0] in components and x['under'][0] in components}
 return [[x[:] for x in diagram['gauss_words'][ci] if x[0] in keep] for ci in components]

def reduce_gauss(words):
 words=[[x[:] for x in w] for w in words];moves=[]
 while True:
  remove=None;kind=None
  for ci,w in enumerate(words):
   if len(w)<2:continue
   for i in range(len(w)):
    a,b=w[i],w[(i+1)%len(w)]
    if a[0]==b[0]:remove={a[0]};kind=['R1',ci,i];break
   if remove:break
  if not remove:
   pairs={}
   for ci,w in enumerate(words):
    if len(w)<2:continue
    for i in range(len(w)):
     a,b=w[i],w[(i+1)%len(w)]
     if a[0]!=b[0] and a[1]==b[1] and a[2]==-b[2]:
      key=tuple(sorted((a[0],b[0])));pairs.setdefault(key,[]).append((a[1],ci,i))
   for key,oc in sorted(pairs.items()):
    if {x[0] for x in oc}=={'U','O'}:remove=set(key);kind=['R2',oc];break
  if not remove:break
  moves.append({'move':kind,'crossings':sorted(remove)});words=[[x for x in w if x[0] not in remove] for w in words]
 return {'remaining':words,'moves':moves,'all_crossings_removed':all(not w for w in words),'caveat':'Combinatorial Gauss R1/R2 reductions; face/isotopy certificates require independent geometric checking.'}

if __name__=='__main__':
 P=Path(__file__).resolve().parent;d=json.loads((P/'spatial_model.json').read_text());polys=d['base_components']+[d['correction_boundary']]
 errors=[]
 for projection in [(1,1009,2,1013),(3,1009,1,1013),(2,1009,5,1013)]:
  try:out=project(polys,projection);break
  except ValueError as e:errors.append(str(e));print('PROJECTION FAILED',e,flush=True)
 else:raise RuntimeError(errors)
 from collections import Counter
 out['prior_projection_failures']=errors;out['crossing_pair_counts']={str(k):v for k,v in Counter(tuple(sorted((x['over'][0],x['under'][0]))) for x in out['crossings']).items()}
 out['correction_knot_reduction']=reduce_gauss(sublink(out,[3]));out['base_auxiliary_reduction']=reduce_gauss(sublink(out,[1,2]));
 (P/'projected_model.json').write_text(json.dumps(out,indent=2)+'\n')
 print('crossings',len(out['crossings']),out['crossing_pair_counts']);print('K unknot reduction',out['correction_knot_reduction']['all_crossings_removed'],len(out['correction_knot_reduction']['remaining'][0]));print('base aux reduction',out['base_auxiliary_reduction']['all_crossings_removed'])
