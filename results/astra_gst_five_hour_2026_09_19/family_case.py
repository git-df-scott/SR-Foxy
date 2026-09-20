"""One bounded exploratory source-family case. Source identity remains qualified."""
import json,time,sys,math
from pathlib import Path
import snappy,regina
from build_preblow import build
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from sources.compdet import component_determinants
p=Path(__file__).parent;n,k=map(int,sys.argv[1:3]);out=p/'family'/f'n{n}_k{k}';out.mkdir(parents=True,exist_ok=True)
if (out/'RESULT.json').exists():raise SystemExit('Refusing to overwrite completed case')
r=build(n,k);(out/'INPUT.json').write_text(json.dumps(r,indent=2)+'\n');L=snappy.Link(r['pd'])
assert len(L.link_components)==4
# PD edge walks begin A,I,B,M; assert this in the concrete imported diagram.
counts={c:sum(cr[s][0]==c for cr in r['crossings'] for s in ['a','b']) for c in ['A','I','B','M']};off=0;labels={}
for c,count in counts.items():
 labels[c]=next(i for i,comp in enumerate(L.link_components) if off in [z.strand_label() for z in comp]);off+=count
red=L.sublink([labels['A'],labels['I']]);red.simplify('global');assert not red.crossings and red.unlinked_unknot_components==2
M=L.exterior();M.dehn_fill((1,1),labels['A']);M.dehn_fill((-1,1),labels['I']);N=M.filled_triangulation([labels['A'],labels['I']]);N.save(str(out/'FILLED.tri'))
K=N.exterior_to_link(seed=20260920,check_input=True,check_answer=True,careful_perturbation=True)
pd=K.PD_code();(out/'OUTPUT_PD.json').write_text(json.dumps(pd)+'\n');R=regina.Link.fromPD([[e+1 for e in row] for row in pd]);J=R.jones(regina.Algorithm.Treewidth)
q={e:int(str(J[e]))*(-1 if e%2 else 1) for e in range(J.minExp(),J.maxExp()+1) if J[e]!=0}
# Independent exact division by q^2+1 and evaluation at i.
shift=min(q);co=[q.get(e,0) for e in range(shift,max(q)+1)];cur=co[:];order=0;first=None
while len(cur)>2:
 rem=cur[:];quo=[0]*(len(rem)-2)
 for i in range(len(rem)-1,1,-1):
  c=rem[i];quo[i-2]=c;rem[i]=0;rem[i-2]-=c
 if any(rem):break
 if first is None:first=quo[:]
 cur=quo;order+=1
real=imag=0
if first is not None:
 for e,c in enumerate(first):
  exp=(e+shift+1)%4
  if exp==0:real+=c
  elif exp==1:imag+=c
  elif exp==2:real-=c
  else:imag-=c
assert imag==0
comp=component_determinants(K);prod=math.prod(comp)
a={'n':n,'k':k,'source_status':'EXPERIMENTAL_TWO_FIGURE_SUPPORTED_FAMILY','input_crossings':len(r['pd']),'output_crossings':len(pd),'components':len(K.link_components),'linking_matrix':K.linking_matrix(),'component_determinants':comp,'q_coefficients':q,'null_V':order,'det_V':real if first is not None else None,'product_mod32':prod%32,'det_V_mod32':real%32 if first is not None else None,'ribbon_gate_passes':order==len(K.link_components)-1 and (real-prod)%32==0,'scope':'Numerical construction and exact invariant of stored PD; GST source identity still requires independent certificate. Passing is not ribbon proof.'}
(out/'RESULT.json').write_text(json.dumps(a,indent=2)+'\n');print(json.dumps({kk:vv for kk,vv in a.items() if kk!='q_coefficients'}),flush=True)
