"""Exact reduced twisted Alexander quadratics for a new small candidate pair."""
from pathlib import Path
import sys,inspect,json,time,signal
import sympy as S,snappy
from sympy.polys.domains import QQ
root=Path(__file__).resolve().parent;old=root.parent/'astra_seven_hour_2026_09_20';sys.path.insert(0,str(old));import metabelian_probe as base

def exact_context(q):
 z=S.Symbol('z');F=QQ.algebraic_field((sum(z**i for i in range(q)),z));ring=F.poly_ring('t').ring
 def R(v):
  if isinstance(v,(list,tuple)):return ring.from_dict({(i,):F.convert(c) for i,c in enumerate(v) if c})
  return ring(v)
 return F,R,F.unit

def dense(f):return [f.get((i,),f.ring.domain.zero) for i in range(f.degree()+1)]
source=inspect.getsource(base.probe);lines=source.splitlines()
for i,line in enumerate(lines):
 if line.strip().startswith('F=fq_default_ctx'):lines[i]='    F,R,z=exact_context(q)'
 if line.strip().startswith('assert z**q'):lines[i]='    assert z**q==F.one'
source='\n'.join(lines).replace('coeff=f.coeffs()','coeff=dense(f)').replace('if d[e]==0','if not d[e]').replace('if c!=0','if c')
source=source[:source.index('    def bar(f):')]+'''    coeffs=dense(delta); cs=[list(reversed(c.to_list())) for c in coeffs]
    return {'label':label,'q':q,'p':p,'scale':scale,'generators':gens,'relators':rels,'abelianization':eps,'cocycle':coc,'degree':delta.degree(),'coefficients_in_z_ascending':[[str(c) for c in row] for row in cs],'all_coefficients_integral':all(c.denominator==1 for row in cs for c in row),'seconds':time.monotonic()-start}
'''
(root/'EXACT_FUNCTION.py').write_text(source+'\n');namespace=dict(vars(base));namespace.update(exact_context=exact_context,dense=dense);exec(compile(source,'EXACT_FUNCTION.py','exec'),namespace);probe=namespace['probe']

def run():
 args=sys.argv[1:];names=tuple(args[:2]) if args else ('K8a5','K12n13');q=int(args[2]) if args else 29;ell=next(2*k*q-1 for k in range(1,100) if S.isprime(2*k*q-1));filename=('EXACT_'+names[0]+'_'+names[1]+'.json') if args else 'EXACT_NEXT_PAIR.json'
 out=root/filename;assert not out.exists();rows=[]
 def timeout(*_):raise TimeoutError('120_SECOND_LIMIT_INCONCLUSIVE')
 signal.signal(signal.SIGALRM,timeout);signal.alarm(120)
 try:
  for name in names:
   L=snappy.Link(name);M=L.exterior();r=probe(name,M,2,q,q-1,ell);r['pd']=L.PD_code();r['double_cover_torsion']=[int(x) for x in M.covers(2,cover_type='cyclic')[0].homology().elementary_divisors() if x];assert r['double_cover_torsion']==[q];rows.append(r);print({k:r[k] for k in ('label','degree','all_coefficients_integral','seconds')},flush=True)
  result={'status':'complete','rows':rows}
 except Exception as exc:result={'status':'inconclusive','rows':rows,'error':repr(exc)}
 finally:signal.alarm(0)
 out.write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':run()
