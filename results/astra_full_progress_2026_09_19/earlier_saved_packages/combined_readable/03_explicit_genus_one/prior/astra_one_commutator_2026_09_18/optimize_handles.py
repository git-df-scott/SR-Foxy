"""Bounded greedy commutator extraction; output identities are exactly checked."""
import json,time
from free_words import *
from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=json.loads((ROOT/'fiber_probe.json').read_text());word=tuple(p['delta_fiber'])

def candidates(w):
    w=red(w)
    for i in range(len(w)):
        pref=w[:i];v=w[i:]+w[:i];a=v[:1]
        for k in range(2,len(v)-1):
            if v[k]!=-v[0]:continue
            for j in range(1,k):
                for l in range(k+1,len(v)):
                    if v[l]!=-v[j]:continue
                    U=v[1:j];b=v[j:j+1];V=v[j+1:k];X=v[k+1:l];Y=v[l+1:]
                    Z=mul(X,V,U)
                    f=mul(a,U,inv(Z));g=mul(Z,b,V,U,inv(Z));rest=mul(X,V,U,Y)
                    fp=mul(pref,f,inv(pref));gp=mul(pref,g,inv(pref));res=mul(pref,rest,inv(pref))
                    if mul(fp,gp,inv(fp),inv(gp),res)!=w:raise ArithmeticError('cut identity failure')
                    _,cr=cyc(res)
                    yield (len(cr),len(res),len(fp)+len(gp)),fp,gp,res,[i,j,k,l]
start=time.monotonic();w=word;factors=[];steps=[]
while w:
    choices=list(candidates(w));best=min(choices,key=lambda a:(a[0],a[4]))
    cost,f,g,r,cut=best
    steps.append({'input':w,'cut':cut,'factor':[f,g],'remainder':r,'choices_examined':len(choices)})
    factors.append((f,g));print('step',len(factors),'length',len(w),'->',len(r),'cost',cost,'candidates',len(choices),flush=True)
    if len(r)>=len(w):raise RuntimeError('no decreasing step')
    w=r
result=mul(*(mul(f,g,inv(f),inv(g)) for f,g in factors))
assert result==word
print('factors',factors,'elapsed',time.monotonic()-start)
(ROOT/'handle_optimization.json').write_text(json.dumps({'method':'deterministic greedy crossing cuts, no minimal-genus claim','input':word,'factors':factors,'steps':steps,'identity_verified':result==word,'elapsed_seconds':time.monotonic()-start},indent=2)+'\n')
