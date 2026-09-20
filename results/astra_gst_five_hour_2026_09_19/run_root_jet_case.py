import sys,json,snappy,regina,time
from pathlib import Path
p=Path(__file__).parent;sys.path.insert(0,str(p.resolve().parents[1]/'scripts'));from bounded_root_jet import probe
n,k=map(int,sys.argv[1:3]);d=p/'family'/f'n{n}_k{k}';pd=json.loads((d/'OUTPUT_PD.json').read_text());L=snappy.Link(pd);dets=[];component_records=[]
for i in range(len(L.link_components)):
 C=L.sublink([i]);C.simplify('global')
 if C.crossings:
  R=regina.Link.fromPD([[v+1 for v in row] for row in C.PD_code()]);A=R.alexander();co=[int(str(A[j])) for j in range(A.degree()+1)];det=abs(sum(a*(-1 if j%2 else 1) for j,a in enumerate(co)))
 else:co=[1];det=1
 dets.append(det);component_records.append({'pd':C.PD_code(),'alexander_coefficients':co,'determinant':det})
prod=1
for x in dets:prod*=x
start=time.monotonic();a=probe(L,prod);a.update(n=n,k=k,component_determinants=dets,component_records=component_records,seconds=time.monotonic()-start,source_identity='Two source transcriptions agree at k=1; extension in k is exploratory with the same explicit full-twist convention.')
(d/'ROOT_JET_RESULT.json').write_text(json.dumps(a,indent=2)+'\n');print(n,k,a['quotient_at_i_mod_32'],dets,a['ribbon_obstructed_mod_32'],a['max_retained_states'],flush=True)
