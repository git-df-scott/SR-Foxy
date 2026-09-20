"""Enumerate one-crossed-edge bands before red surgery; bounded numerical screen."""
import json,time,collections
from pathlib import Path
import snappy
from spherogram.links.bands.core import Band,add_one_band,normalize_crossing_labels
from build_preblow import build
p=Path(__file__).parent;out=p/'preblow_fusion_one_edge';out.mkdir(exist_ok=True)
if (out/'RESULT.json').exists():raise FileExistsError('Preserve completed run')
r=build(3,1);L=snappy.Link(r['pd']);normalize_crossing_labels(L)
counts={c:sum(cr[s][0]==c for cr in r['crossings'] for s in ['a','b']) for c in ['A','I','B','M']};off=0;labels={}
for c,count in counts.items():
 labels[c]=next(i for i,comp in enumerate(L.link_components) if off in [z.strand_label() for z in comp]);off+=count
red_sigs={c:collections.Counter(z.crossing.label for z in L.link_components[labels[c]]) for c in ['A','I']}
target=json.loads((p.parents[1]/'data/knots/GST_B31_regina.json').read_text());T=snappy.Link(target['pd_code_snappy_0indexed']).exterior();tv=float(T.volume())
faces=L.faces();edges=collections.defaultdict(list)
for fi,face in enumerate(faces):
 for cs in face:edges[cs.strand_label()].append((fi,cs))
assert all(len(x)==2 for x in edges.values())
seen=set();specs=[]
for arc,ends in sorted(edges.items()):
 for (fi,middle),(fj,opposite) in [ends,ends[::-1]]:
  if fi==fj:continue
  for X in faces[fi]:
   if X.strand_label()==arc or X.crossing.strand_components[X.strand_index]!=labels['B']:continue
   for end in faces[fj]:
    if end.strand_label()==arc or end.crossing.strand_components[end.strand_index]!=labels['M']:continue
    Z=end.opposite();parity=int((X==X.oriented())==(Z==Z.oriented()))
    for twist in range(-2,3):
     if twist%2!=parity:continue
     for over in [False,True]:
      band=Band([(z.crossing.label,z.strand_index) for z in [X,middle.opposite(),Z]],[over],twist);spec=band.compressed_spec()
      if spec in seen:continue
      seen.add(spec);specs.append({'band':spec,'faces':[fi,fj],'crossed_arc':arc,'band_over':over,'twists':twist})
(out/'INPUT.json').write_text(json.dumps({'n':3,'k':1,'input_pd':r['pd'],'labels':labels,'target_pd':target['pd_code_snappy_0indexed'],'specs':specs},indent=2)+'\n')
start=time.monotonic();rows=[]
for i,meta in enumerate(specs):
 if time.monotonic()-start>120:break
 row=dict(meta,index=i)
 try:
  K=add_one_band(L,meta['band']);assert len(K.link_components)==3
  sigs=[collections.Counter(z.crossing.label for z in comp if z.crossing.label<len(L.crossings)) for comp in K.link_components]
  red={c:next(j for j,s in enumerate(sigs) if s==red_sigs[c]) for c in ['A','I']};assert len(set(red.values()))==2
  N=K.exterior();N.dehn_fill((1,1),red['A']);N.dehn_fill((-1,1),red['I']);N=N.filled_triangulation(list(red.values()));vol=float(N.volume());row.update(pre_surgery_pd=K.PD_code(),red_components=red,volume=vol,volume_difference=vol-tv,solution_type=N.solution_type())
  if abs(vol-tv)<1e-6:
   iso=N.is_isometric_to(T,return_isometries=True);row['isometries']=[{'cusp_images':a.cusp_images(),'cusp_maps':[str(x) for x in a.cusp_maps()],'extends_to_link':a.extends_to_link()} for a in iso];N.save(str(out/f'match_{i}.tri'))
  row['status']='COMPLETED_NUMERICAL_SCREEN'
 except Exception as e:row.update(status='ERROR_INCONCLUSIVE',error=repr(e))
 rows.append(row)
 with (out/'ROWS.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
 if 'isometries' in row:print('MATCH',json.dumps({k:v for k,v in row.items() if k!='pre_surgery_pd'}),flush=True)
result={'n':3,'k':1,'specifications':len(specs),'processed':len(rows),'complete':len(rows)==len(specs),'seconds':time.monotonic()-start,'errors':sum(x['status']=='ERROR_INCONCLUSIVE' for x in rows),'matches':[x['index'] for x in rows if x.get('isometries')],'closest':sorted([{'index':x['index'],'difference':x['volume_difference']} for x in rows if 'volume_difference' in x],key=lambda x:abs(x['difference']))[:5],'scope':'Numerical screen only. Negative results do not exclude bands or establish knot distinctions. Positive numerical maps require exact certification.'};(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
