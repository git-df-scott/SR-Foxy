"""Build an exact nonribbon link whose two components are square knots.
This is a positive obstruction control, not a slice-link/knot counterexample.
"""
import json,sys,math
from pathlib import Path
import snappy,regina
p=Path(__file__).parent;sys.path.insert(0,str(p.resolve().parents[1]/'scripts'))
from sagefree_eisermann import null_and_det_V
from sources.compdet import component_determinants
name='L14n38935';base=snappy.Link(name);pieces=[];proof=[];attachments=[]
for i in range(2):
 C=base.sublink([i]);C.simplify('global');assert len(C.crossings)==3
 jr=regina.Link.fromPD([[v+1 for v in row] for row in C.PD_code()]);T=snappy.Link('3_1');tr=regina.Link.fromPD([[v+1 for v in row] for row in T.PD_code()]);tm=regina.Link.fromPD([[v+1 for v in row] for row in T.mirror().PD_code()])
 sig=jr.sig(False,True,True);assert sig in [tr.sig(False,True,True),tm.sig(False,True,True)]
 J=C.mirror();pieces.append(J);proof.append({'component':i,'trefoil_pd':C.PD_code(),'mirror_to_attach_pd':J.PD_code(),'is_trefoil_diagram_up_to_rotation_and_reversal':True})
# Save original attachment half-edges; crossing objects survive the rewiring.
for i,J in enumerate(pieces):
 c,a=base.link_components[i][0];d,b=c.adjacent[a];e,u=J.link_components[0][0];f,v=e.adjacent[u]
 attachments.append({'base_crossing':base.crossings.index(c),'base_slot':a,'summand_crossing':J.crossings.index(e),'summand_slot':u})
 c[a]=f[v];e[u]=d[b]
L=snappy.Link(base.crossings+pieces[0].crossings+pieces[1].crossings)
assert len(L.link_components)==2 and L.linking_number()==0
nu,dv,notes=null_and_det_V(L);dets=component_determinants(L)
assert nu==1 and dv==225 and dets==[9,9]
R=regina.Link.fromPD([[v+1 for v in row] for row in L.PD_code()]);Q=R.jones(regina.Algorithm.Treewidth);q={e:int(str(Q[e]))*(-1 if e%2 else 1) for e in range(Q.minExp(),Q.maxExp()+1) if Q[e]!=0}
from sagefree_jones import jones_polynomial
assert q==jones_polynomial(L).d
result={'status':'CERTIFIED_POSITIVE_NONRIBBON_LINK_CONTROL','base_name':name,'base_pd':snappy.Link(name).PD_code(),'component_proofs':proof,'attachments':attachments,'pd':L.PD_code(),'crossings':len(L.crossings),'components':2,'component_knot_types':['square knot','square knot'],'linking_number':0,'null_V':nu,'det_V':dv,'component_determinants':dets,'mod32':dv%32,'required_ribbon_mod32':math.prod(dets)%32,'independent_regina_full_jones_agrees':True,'q_coefficients':q,'scope':'Each component is K#mirror(K), explicitly formed with K a trefoil. Eisermann obstructs ribbonness of the whole link. Sliceness is not established; this is not a Slice-Ribbon counterexample.'}
(p/'SQUARE_PAIR_NONRIBBON_CONTROL.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['pd','base_pd','component_proofs','q_coefficients']}))
