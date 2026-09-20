from pathlib import Path
import importlib.util,json,signal,time,sys
import sympy as S
from sympy.polys.domains import QQ
p=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('marked',p/'marked_test.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
import metabelian_probe as base

def exact_context(q):
 z=S.Symbol('z');F=QQ.algebraic_field((sum(z**i for i in range(q)),z));ring=F.poly_ring('t').ring
 def R(v):
  if isinstance(v,(list,tuple)):return ring.from_dict({(i,):F.convert(c) for i,c in enumerate(v) if c})
  return ring(v)
 return F,R,F.unit

def dense(f):return [f.get((i,),f.ring.domain.zero) for i in range(f.degree()+1)]
ns=dict(vars(base));ns.update(exact_context=exact_context,dense=dense)
exec((p.parent/'astra_additional_3pct_2026_09_20/EXACT_FUNCTION.py').read_text(),ns)
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('60 second bound')));signal.alarm(60)
rows=[]
try:
 for name in ['K9n4','K14n282']:
  L=m.snappy.Link(name);r=ns['probe'](name,m.M(m.G(L)),2,7,6,13);r['pd']=L.PD_code();rows.append(r);print(name,r['coefficients_in_z_ascending'],r['seconds'],flush=True)
 result={'status':'complete','rows':rows}
except Exception as e:result={'status':'inconclusive','rows':rows,'error':repr(e)}
(p/'EXACT_MARKED.json').write_text(json.dumps(result,indent=2)+'\n')
