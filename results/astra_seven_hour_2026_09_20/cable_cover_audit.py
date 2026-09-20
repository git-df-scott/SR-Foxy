"""Independent cyclic-cover homology checks for the precise stored cable."""
from pathlib import Path
import json,time,signal,hashlib
import snappy,sympy as S
from sympy.matrices.normalforms import smith_normal_form
p=Path(__file__).resolve().parent;out=p/'CABLE_COVER_AUDIT.json';assert not out.exists()
card=p.parents[1]/'data/knots/10_17_2_1-cable.json';d=json.loads(card.read_text())
L=snappy.Link(d.get('pd_code_snappy_0indexed') or d['pd_code']);M=L.exterior()
V=S.Matrix(snappy.Link('10_17').seifert_matrix());assert V.det() in (1,-1)
T=V.inv()*V.T;assert all(x.q==1 for x in T);g=T.rows
C=S.zeros(g).row_join(T).col_join(S.eye(g).row_join(S.zeros(g)))
x=S.Symbol('x');delta=(V-x*V.T).det();assert C.charpoly(x).as_expr()==S.expand(delta.subs(x,x*x))
rows=[];start=time.monotonic()
def timeout(*_):raise TimeoutError('90_SECOND_LIMIT_INCONCLUSIVE')
signal.signal(signal.SIGALRM,timeout);signal.alarm(90)
for n in (2,3,4,5,7,8,9,11,13,16):
 D=smith_normal_form(C**n-S.eye(2*g),domain=S.ZZ);factors=[abs(int(D[i,i])) for i in range(2*g) if abs(D[i,i])!=1]
 cover=M.covers(n,cover_type='cyclic')[0];actual=[int(a) for a in cover.homology().elementary_divisors() if a!=0]
 assert factors==actual,(n,factors,actual)
 rows.append({'cover_degree':n,'nontrivial_invariant_factors':factors,'independent_snappy_cyclic_exterior_torsion_agrees':True})
 print(n,factors,flush=True)
signal.alarm(0)
r={'candidate':d['name'],'input_sha256':hashlib.sha256(card.read_bytes()).hexdigest(),'companion_seifert_matrix':V.tolist(),'cable_monodromy':C.tolist(),'alexander_companion':str(delta),'companion_determinant':abs(int(delta.subs(x,-1))),'companion_Arf':0,'cover_rows':rows,'seconds':time.monotonic()-start,'explanation':'For a cyclic knot-exterior cover, the lift of meridian^n maps to1 under the lifted abelianization; filling kills the free generator and preserves torsion. Compare that torsion with the cable monodromy presentation. This determines homology, not a slice disk.'}
out.write_text(json.dumps(r,indent=2,default=int)+'\n')
