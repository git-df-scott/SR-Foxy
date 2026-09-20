"""Bounded same-face black-component fusions before red surgery.
Numerical isometry is a lead only; no negative finite search closes the lane.
"""
import json,time,collections
from pathlib import Path
import snappy
from spherogram.links.bands.core import Band,add_one_band,normalize_crossing_labels
from build_preblow import build
p=Path(__file__).parent;out=p/'preblow_fusion';out.mkdir(exist_ok=True)
r=build(3,1);L=snappy.Link(r['pd']);normalize_crossing_labels(L)
counts={c:sum(cr[s][0]==c for cr in r['crossings'] for s in ['a','b']) for c in ['A','I','B','M']};off=0;labels={}
for c,count in counts.items():
 labels[c]=next(i for i,comp in enumerate(L.link_components) if off in [z.strand_label() for z in comp]);off+=count
red_sigs={c:collections.Counter(z.crossing.label for z in L.link_components[labels[c]]) for c in ['A','I']}
target_data=json.loads((p.parents[1]/'data/knots/GST_B31_regina.json').read_text());T=snappy.Link(target_data['pd_code_snappy_0indexed']).exterior();tv=float(T.volume());seen=set();rows=[];start=time.monotonic()
for fi,face in enumerate(L.faces()):
 for X in face:
  if X.crossing.strand_components[X.strand_index]!=labels['B']:continue
  for end in face:
   if end.crossing.strand_components[end.strand_index]!=labels['M']:continue
   Z=end.opposite();parity=int((X==X.oriented())==(Z==Z.oriented()))
   for twist in range(-2,3):
    if twist%2!=parity:continue
    band=Band([(z.crossing.label,z.strand_index) for z in [X,Z]],[],twist);spec=band.compressed_spec()
    if spec in seen:continue
    seen.add(spec);row={'face':fi,'band':spec,'twists':twist}
    try:
     K=add_one_band(L,band);assert len(K.link_components)==3
     sigs=[collections.Counter(z.crossing.label for z in comp if z.crossing.label<len(L.crossings)) for comp in K.link_components]
     red={c:next(i for i,s in enumerate(sigs) if s==red_sigs[c]) for c in ['A','I']};assert len(set(red.values()))==2
     N=K.exterior();N.dehn_fill((1,1),red['A']);N.dehn_fill((-1,1),red['I']);N=N.filled_triangulation(list(red.values()));vol=float(N.volume());row.update(pre_surgery_pd=K.PD_code(),red_components=red,volume=vol,volume_difference=vol-tv,solution_type=N.solution_type())
     if abs(vol-tv)<1e-6:
      iso=N.is_isometric_to(T,return_isometries=True);row['isometries']=[{'cusp_images':a.cusp_images(),'cusp_maps':[str(x) for x in a.cusp_maps()],'extends_to_link':a.extends_to_link()} for a in iso];N.save(str(out/f'match_{len(rows)}.tri'))
     row['status']='COMPLETED_NUMERICAL_SCREEN'
    except Exception as e:row.update(status='ERROR_INCONCLUSIVE',error=repr(e))
    rows.append(row);(out/'RESULT.json').write_text(json.dumps({'source_n':3,'source_k':1,'target_volume':tv,'input_pd':r['pd'],'rows':rows,'complete':False},indent=2)+'\n');print({k:v for k,v in row.items() if k!='pre_surgery_pd'},flush=True)
    if time.monotonic()-start>90:break
   if time.monotonic()-start>90:break
  if time.monotonic()-start>90:break
 if time.monotonic()-start>90:break
result={'source_n':3,'source_k':1,'target_volume':tv,'input_pd':r['pd'],'rows':rows,'complete':time.monotonic()-start<=90,'scope':'All enumerated same-face bands, twists -2 through 2 with orientation parity. Numerical screen only; missing a match is inconclusive. Source identity qualified.'};(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print('TOTAL',len(rows),'COMPLETE',result['complete'])
