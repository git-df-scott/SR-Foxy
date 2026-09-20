"""Fresh invariant checks for the unexcluded prime-seven pair."""
from pathlib import Path
import json,time,signal
import snappy,regina,sympy as S
root=Path(__file__).resolve().parent;out=root/'SURVIVOR_AUDIT.json';assert not out.exists()
def timeout(*_):raise TimeoutError('120_SECOND_LIMIT_INCONCLUSIVE')
signal.signal(signal.SIGALRM,timeout);signal.alarm(120);start=time.monotonic();rows=[];x=S.Symbol('x')
for name in ('K9n4','K14n282'):
 L=snappy.Link(name);V=S.Matrix(L.seifert_matrix());f=S.Poly((V-x*V.T).det(),x);lo=min(m[0] for m in f.monoms());f=S.Poly(f.as_expr()/x**lo,x);f=f.monic();assert f.is_irreducible
 hfk={}
 for prime in (2,3):
  h=L.knot_floer_homology(prime=prime);assert h['fibered'] and h['seifert_genus']==2 and h['tau']==0
  h['ranks']={str(k):v for k,v in h['ranks'].items()};hfk[str(prime)]=h
 R=regina.Link.fromPD([[a+1 for a in c] for c in L.PD_code()]);J=R.jones(regina.Algorithm.Treewidth)
 jones={str(i):int(str(J[i])) for i in range(J.minExp(),J.maxExp()+1) if J[i]!=0}
 rows.append({'name':name,'pd':L.PD_code(),'seifert_matrix':V.tolist(),'alexander_monic':str(f.as_expr()),'irreducible':True,'hfk':hfk,'jones_regina_sqrt_t':jones})
assert rows[0]['alexander_monic']==rows[1]['alexander_monic'];assert rows[0]['jones_regina_sqrt_t']!=rows[1]['jones_regina_sqrt_t']
signal.alarm(0);r={'rows':rows,'distinct_by_Jones':True,'same_irreducible_Alexander':True,'fibered_genus2_over_F2_F3':True,'seconds':time.monotonic()-start,'scope':'Computational hypotheses for Miyazaki/Abe-Tagami nonribbonness. No smooth concordance or slice disk supplied. HFK uses one implementation at two coefficients.'};out.write_text(json.dumps(r,indent=2,default=int)+'\n');print({k:v for k,v in r.items() if k!='rows'})
