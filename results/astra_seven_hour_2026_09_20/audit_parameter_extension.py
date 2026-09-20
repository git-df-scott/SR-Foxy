"""Small exhaustive linking-form controls and exact root-of-unity checks.

This tests the proposed unequal-valuation lemma, including equal-valuation
negative controls. It is not a substitute for its all-parameter proof.
"""
from itertools import product
from fractions import Fraction as F
from pathlib import Path
import json,time,signal
pdir=Path(__file__).resolve().parent
out=pdir/'PARAMETER_EXTENSION_CONTROLS.json';assert not out.exists()
def timeout(*_):raise TimeoutError('90_SECOND_LIMIT_INCONCLUSIVE')
signal.signal(signal.SIGALRM,timeout);signal.alarm(90);start=time.monotonic()
def check(p,r,s,u=1,v=1):
    mods=(p**r,p**s,p**s,p**r);den=p**r
    elems=list(product(*(range(m) for m in mods)));ix={e:i for i,e in enumerate(elems)}
    def add(i,j):return ix[tuple((a+b)%m for a,b,m in zip(elems[i],elems[j],mods))]
    def pairing(i,j):
        A,B,E,D=elems[i];a,b,e,d=elems[j]
        return (u*(A*a-D*d)+v*p**(r-s)*(E*e-B*b))%den
    iso=[i for i in range(len(elems)) if pairing(i,i)==0];cyclic={}
    for g in iso:
        row=[0];k=g
        while k:row.append(k);k=add(k,g)
        cyclic[g]=row
    seen={frozenset([0])};queue=list(seen);met=[];size=p**(r+s)
    for V in queue:
        if len(V)==size:met.append(V);continue
        for g in iso:
            if g in V or any(pairing(g,h) for h in V):continue
            W=frozenset(add(h,k) for h in V for k in cyclic[g])
            assert len(W)<=size
            if W not in seen:seen.add(W);queue.append(W)
    chars=[(1,0,c,d) for c,d in product(range(p) if s else [0],range(p))]
    failures=[]
    for V in met:
        if not any(all(sum(x*y for x,y in zip(ch,elems[h]))%p==0 for h in V) for ch in chars):
            failures.append([elems[h] for h in sorted(V)])
    assert met
    if r>s:assert not failures
    else:assert failures,'Equal-valuation negative control must reject universal witness claim'
    return {'p':p,'r':r,'s':s,'u':u,'v':v,'metabolizers':len(met),'without_witness':len(failures),'first_failure':failures[:1]}
records=[check(3,1,0),check(3,2,0),check(5,1,0),check(3,1,1)]
records += [check(3,2,1,u,v) for u,v in product((1,2),repeat=2)]
roots=[];torus_checks=0
for p in (3,5,7,11,13,17,19,23,29,31):
    omega=(F(1,6)-F(1,p))%1
    isroot=lambda t:t%1 in (F(1,6),F(5,6))
    vals=[int(isroot(omega+F(1,p))),int(isroot(omega-F(1,p))),int(isroot(omega))]
    parity=(vals[0]+vals[1]-2*vals[2])%2;assert parity==1
    assert omega.denominator%2==0
    for q in range(1,100,2):
        assert (omega*q)%1
        for d in range(p) if q%p==0 else (0,):
            assert omega != F(d,p)%1 and omega != -F(d,p)%1
            torus_checks+=1
    roots.append({'p':p,'omega_turns':str(omega),'valuations':vals,'parity':parity})
signal.alarm(0)
result={'complete':True,'linking_form_cases':records,'cyclotomic_roots':roots,'torus_local_unit_checks':torus_checks,'seconds':time.monotonic()-start,'scope':'Small exhaustive controls, including required failure at equal valuations. General proof is in SAME_SIGN_CABLE_FILTER.md.'}
out.write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k not in ('linking_form_cases','cyclotomic_roots')})
