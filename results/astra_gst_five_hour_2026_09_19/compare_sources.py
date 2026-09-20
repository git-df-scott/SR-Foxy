from pathlib import Path
import json,snappy,sys
p=Path(__file__).parent;n=int(sys.argv[1]) if len(sys.argv)>1 else 1
r=json.loads((p/f'GOMPF6_n{n}.json').read_text());s=json.loads((p/f'PREBLOW_n{n}.json').read_text())
A=snappy.Link(r['pd']);B=snappy.Link(s['pd']);red=A.sublink([0,1]);red.simplify('global')
print('gompf6 red unlink',len(red.crossings),red.unlinked_unknot_components,flush=True)
assert len(red.crossings)==0 and red.unlinked_unknot_components==2
M=A.exterior();N=B.exterior();print('unfilled',str(M.volume()),str(N.volume()),flush=True)
isos=M.is_isometric_to(N,return_isometries=True)
rec={'n':n,'red_unlink_crossings':0,'red_unlink_components':2,'unfilled_isometries':[{'cusp_images':x.cusp_images(),'maps':[str(z) for z in x.cusp_maps()],'extends_to_link':x.extends_to_link()} for x in isos]}
for X in [M,N]:X.dehn_fill((1,1),0);X.dehn_fill((-1,1),1)
MF=M.filled_triangulation([0,1]);NF=N.filled_triangulation([0,1]);rec['filled_volumes_approx']=[str(MF.volume()),str(NF.volume())]
isos=MF.is_isometric_to(NF,return_isometries=True);rec['filled_isometries']=[{'cusp_images':x.cusp_images(),'maps':[str(z) for z in x.cusp_maps()],'extends_to_link':x.extends_to_link()} for x in isos]
print(json.dumps(rec),flush=True);(p/f'SOURCE_COMPARISON_n{n}.json').write_text(json.dumps(rec,indent=2)+'\n')
