"""Bounded previously untested scalar-character screens of (10_17)_(2,1)."""
import json,time,signal
from pathlib import Path
import sympy as S,snappy
from metabelian_probe import probe
root=Path(__file__).resolve().parent;out=root/'metabelian'
d=json.loads((root.parents[1]/'data/knots/10_17_2_1-cable.json').read_text())
M=snappy.Link(d.get('pd_code_snappy_0indexed') or d['pd_code']).exterior()
# Same abelianized companion module; Delta_C(t)=Delta_K(t^2).
coeff=[1,-3,5,-7,9,-7,5,-3,1]
for p,q in ((5,41),(7,29),(11,397),(13,1873)):
    ell=next(2*k*q-1 for k in range(1,100) if S.isprime(2*k*q-1))
    eigen=[a for a in range(2,q) if pow(a,p,q)==1 and sum(c*pow(a,2*j,q) for j,c in enumerate(coeff))%q==0]
    assert len(eigen)==2
    for a in eigen:
        path=out/f'10_17_{p}_{q}_{a}.json';assert not path.exists()
        def timeout(*_):raise TimeoutError('240_SECOND_LIMIT_INCONCLUSIVE')
        signal.signal(signal.SIGALRM,timeout);signal.alarm(240);start=time.monotonic()
        try:r=probe('10_17',M,p,q,a,ell)
        except Exception as exc:r={'status':'failed','error':repr(exc),'p':p,'q':q,'a':a,'seconds':time.monotonic()-start}
        finally:signal.alarm(0)
        path.write_text(json.dumps(r,indent=2)+'\n')
        print({k:r[k] for k in ('cover_degree','character_prime','deck_eigenvalue','reduction_prime','degree','not_norm_mod_reduction','seconds','error') if k in r},flush=True)
