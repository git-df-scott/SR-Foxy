"""Independent full Jones-polynomial verification with Regina's treewidth engine."""
import json,sys,time
from pathlib import Path
import regina,snappy
p=Path(__file__).parent;sys.path.insert(0,str(p.resolve().parents[1]/'scripts'))
from sagefree_jones import jones_polynomial

def check(label,pd):
 L=snappy.Link(pd);R=regina.Link.fromPD([[v+1 for v in row] for row in pd]);t=time.time()
 J=R.jones(regina.Algorithm.Treewidth);raw={e:int(str(J[e])) for e in range(J.minExp(),J.maxExp()+1) if J[e]!=0}
 # Regina documents x=-q conversion to Khovanov normalization used by repo.
 converted={e:c*(-1 if e%2 else 1) for e,c in raw.items()};converted={e:int(c) for e,c in converted.items()}
 target=jones_polynomial(L).d
 r={'label':label,'crossings':len(pd),'seconds':time.time()-t,'regina_x_coefficients':raw,'converted_q_coefficients':converted,'repository_q_coefficients':target,'equal':converted==target}
 print(label,r['equal'],r['seconds'],flush=True);return r
rows=[]
for name in ['3_1','4_1','L2a1','L10n36']:
 rows.append(check(name,snappy.Link(name).PD_code()))
for n in [0,1,2,3]:
 a=json.loads((p/f'RECONSTRUCTED_n{n}.json').read_text());rows.append(check(f'provisional_n{n}',a['pd']))
(p/'REGINA_JONES_CHECK.json').write_text(json.dumps({'regina_version':regina.versionString(),'rows':rows,'all_pass':all(x['equal'] for x in rows)},indent=2)+'\n')
assert all(x['equal'] for x in rows)
