"""Screen D*=K7a2#-K10n4, comparing every nonzero prime19 character pair.

All candidate metabolizers must give nonzero characters on both cyclic
prime19 summands. We intentionally retain all character pairings rather
than assuming a particular linking-form identification.
"""
from pathlib import Path
import json,time,signal
import snappy
from flint import fq_default_ctx,fq_default_poly_ctx
from metabelian_probe import probe
root=Path(__file__).resolve().parent;out=root/'SMALL_DIFFERENCE_SCREEN.json';assert not out.exists()
Ms=[snappy.Link(k).exterior() for k in ('K7a2','K10n4')]
possible={(a,b) for a in range(1,10) for b in range(1,10)};rounds=[];start=time.monotonic()
def timeout(*_):raise TimeoutError('120_SECOND_LIMIT_INCONCLUSIVE')
signal.signal(signal.SIGALRM,timeout);signal.alarm(120)
status='complete'
try:
 for ell in (37,113,227,379):
    F=fq_default_ctx(ell,2,'u');R=fq_default_poly_ctx(F)
    def parse(s):return eval(s.replace('^','**'),{'__builtins__':{}},{'x':R.gen(),'u':R([F.gen()])}).monic()
    def bar(f):return R([c**ell for c in reversed(f.coeffs())]).monic()
    records=[[probe(k,M,2,19,18,ell,scale=a) for a in range(1,10)] for k,M in zip(('K7a2','K10n4'),Ms)]
    polynomials=[[parse(r['reduced_twisted_polynomial']) for r in row] for row in records]
    survivors=set()
    for a,b in possible:
        fs=list((polynomials[0][a-1]*polynomials[1][b-1]).factor()[1]);norm=True
        for f,m in fs:
            fb=bar(f);other=next((n for h,n in fs if h==fb),0)
            if (f==fb and m%2) or m!=other:norm=False;break
        if norm:survivors.add((a,b))
    rounds.append({'ell':ell,'records':records,'previous_pair_count':len(possible),'surviving_pairs':sorted(survivors)})
    possible=survivors;print({'ell':ell,'surviving_pairs':len(possible)},flush=True)
    if not possible:break
except Exception as exc:status='inconclusive';error=repr(exc)
finally:signal.alarm(0)
r={'status':status,'candidate':'K7a2#-K10n4','p':2,'q':19,'rounds':rounds,'remaining_pairs':sorted(possible),'seconds':time.monotonic()-start,'scope':'Finite-field necessary norm screens. Remaining pairs need not preserve linking forms. Empty set would require good-reduction and full topology audit before a nonsliceness claim. Nonempty does not establish sliceness.'}
if status!='complete':r['error']=error
out.write_text(json.dumps(r,indent=2)+'\n');print({k:v for k,v in r.items() if k!='rounds'})
