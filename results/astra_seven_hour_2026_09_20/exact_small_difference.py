"""Lift the same checked Fox contractions to Q(zeta19), then verify reductions.

Generated function source is saved so the arithmetic substitution is reviewable.
"""
from pathlib import Path
import inspect,json,time,signal,math
import sympy as S,snappy
from sympy.polys.domains import QQ
import metabelian_probe as base
root=Path(__file__).resolve().parent

def exact_context(q):
    z=S.Symbol('z');F=QQ.algebraic_field((sum(z**i for i in range(q)),z));ring=F.poly_ring('t').ring
    def R(v):
        if isinstance(v,(list,tuple)):return ring.from_dict({(i,):F.convert(c) for i,c in enumerate(v) if c!=0})
        return ring(v)
    return F,R,F.unit

def dense(f):return [f.get((i,),f.ring.domain.zero) for i in range(f.degree()+1)]

source=inspect.getsource(base.probe)
lines=source.splitlines()
for i,line in enumerate(lines):
    if line.strip().startswith('F=fq_default_ctx'):lines[i]='    F,R,z=exact_context(q)'
    if line.strip().startswith('assert z**q'):lines[i]='    assert z**q==F.one'
source='\n'.join(lines).replace('coeff=f.coeffs()','coeff=dense(f)').replace('if d[e]==0','if not d[e]').replace('if c!=0','if c')
source=source[:source.index('    def bar(f):')]+'''    coeffs=dense(delta)
    rational_coeffs=[list(reversed(c.to_list())) for c in coeffs]
    integral=all(c.denominator==1 for row in rational_coeffs for c in row)
    return {'label':label,'q':q,'p':p,'scale':scale,'generators':gens,'relators':rels,'abelianization':eps,'cocycle':coc,'degree':delta.degree(),'coefficients_in_z_ascending':[[str(c) for c in row] for row in rational_coeffs],'all_coefficients_integral':integral,'seconds':time.monotonic()-start}
'''
(root/'exact_fox_generated.py').write_text(source+'\n')
namespace=dict(vars(base));namespace.update(exact_context=exact_context,dense=dense);exec(compile(source,'exact_fox_generated.py','exec'),namespace);probe=namespace['probe']
out=root/'EXACT_SMALL_DIFFERENCE_v2.json';assert not out.exists()
rows=[];start=time.monotonic()
def timeout(*_):raise TimeoutError('180_SECOND_EXACT_LIMIT_INCONCLUSIVE')
signal.signal(signal.SIGALRM,timeout);signal.alarm(180)
try:
 for name in ('K7a2','K10n4'):
    r=probe(name,snappy.Link(name).exterior(),2,19,18,37);rows.append(r);print(r,flush=True)
 result={'status':'complete','rows':rows,'seconds':time.monotonic()-start}
except Exception as exc:result={'status':'inconclusive','rows':rows,'error':repr(exc),'seconds':time.monotonic()-start}
finally:signal.alarm(0)
out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'],result.get('error'))
