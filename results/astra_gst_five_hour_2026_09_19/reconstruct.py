"""Bounded local reconstruction from experimental four-component source trace."""
import json,sys,time
from pathlib import Path
import snappy
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from sagefree_eisermann import null_and_det_V
from sources.compdet import component_determinants
p=Path(__file__).parent
n=int(sys.argv[1]);r=json.loads((p/f'PREBLOW_n{n}.json').read_text());K=snappy.Link(r['pd']);labels=r['cusp_labels']
red=K.sublink([labels['A'],labels['I']]);red.simplify('global')
print('Red sublink',len(red.crossings),'crossings; unlinked unknot count',red.unlinked_unknot_components,flush=True)
assert len(red.crossings)==0 and red.unlinked_unknot_components==2
M=K.exterior();M.dehn_fill((1,1),labels['A']);M.dehn_fill((-1,1),labels['I']);N=M.filled_triangulation([labels['A'],labels['I']]);N.save(str(p/f'FILLED_n{n}.tri'))
print('Partial filling',N.num_tetrahedra(),'tetrahedra',N.homology(),flush=True)
full=N.copy();full.dehn_fill([(1,0),(1,0)]);G=full.fundamental_group();print('Meridian filled group',G,flush=True)
start=time.time();L=N.exterior_to_link(seed=20260919,check_input=True,check_answer=True,careful_perturbation=True,simplify_link=True)
nu,dv,notes=null_and_det_V(L)
a={'file_tag':n,'n':r['n'],'k':r['k'],'source_status':r['status'],'red_unlink_reduced_crossings':0,'red_unlink_components':2,'pd':L.PD_code(),'crossings':len(L.crossings),'components':len(L.link_components),'linking_matrix':L.linking_matrix(),'component_determinants':component_determinants(L),'null_V':nu,'det_V':dv,'notes':notes,'reconstruction_seconds':time.time()-start,'seed':20260919,'all_reconstruction_checks_enabled':True,'exterior_volume_approx':str(N.volume())}
(p/f'RECONSTRUCTED_n{n}.json').write_text(json.dumps(a,indent=2)+'\n');print(json.dumps(a),flush=True)
