"""Screen all scalar character classes, modulo deck conjugacy and sign."""
from pathlib import Path
import json,time,signal
import snappy,sympy as S
from metabelian_probe import probe
root=Path(__file__).resolve().parent;out=root/'ALL_CHARACTER_SCREEN.json';assert not out.exists()
d=json.loads((root.parents[1]/'data/knots/10_17_2_1-cable.json').read_text());M=snappy.Link(d.get('pd_code_snappy_0indexed') or d['pd_code']).exterior()
coeff=[1,-3,5,-7,9,-7,5,-3,1];start=time.monotonic();records=[];cases=[]
def timeout(*_):raise TimeoutError('180_SECOND_LIMIT_INCONCLUSIVE')
signal.signal(signal.SIGALRM,timeout);signal.alarm(180)
status='complete'
try:
 for p,q in ((4,41),(5,41),(7,29),(11,397),(13,1873)):
    ell=next(2*k*q-1 for k in range(1,100) if S.isprime(2*k*q-1))
    eigen=[a for a in range(2,q) if pow(a,p,q)==1 and sum(c*pow(a,2*j,q) for j,c in enumerate(coeff))%q==0];assert len(eigen)==2
    for a in eigen:
        orbit_group={s*pow(a,j,q)%q for s in (1,-1) for j in range(p)}
        unseen=set(range(1,q));orbits=[]
        while unseen:
            k=min(unseen);orb={k*g%q for g in orbit_group};assert orb<=unseen
            unseen-=orb;orbits.append(sorted(orb))
            # Save the exact orbit, so the tested and inferred classes differ.
            r=probe('10_17',M,p,q,a,ell,scale=k);r['character_orbit']=sorted(orb);records.append(r)
        assert sum(map(len,orbits))==q-1
        cases.append({'p':p,'q':q,'a':a,'ell':ell,'orbits':len(orbits),'character_count':q-1})
    print({'p':p,'q':q,'tests_so_far':len(records),'non_norms_so_far':sum(r['not_norm_mod_reduction'] for r in records)},flush=True)
except Exception as exc:status='inconclusive';error=repr(exc)
finally:signal.alarm(0)
r={'status':status,'seconds':time.monotonic()-start,'cases':cases,'tested_orbits':len(records),'non_norm_orbits':sum(r['not_norm_mod_reduction'] for r in records),'records':records,'scope':'All nonzero scalar characters on each of the two multiplicity-one deck eigenspaces, modulo conjugate/sign equivalents, at each listed reduction prime. This does not test arbitrary sums across eigenspaces or prove sliceness.'}
if status!='complete':r['error']=error
out.write_text(json.dumps(r,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ('records','cases')})
