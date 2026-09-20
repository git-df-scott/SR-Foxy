"""Exact order-eight Temperley–Lieb contraction with byte partner arrays.

Same skein convention as spherogram.links.jones: positive=I-v e_i,
negative=e_i-v I, loop=v+v^-1; v=1+x. Fixed Z[x]/x^8 arithmetic.
"""
import time,signal,resource,sys
N=8;ZERO=(0,)*N;ONE=(1,)+(0,)*(N-1)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,b):return tuple(sum(a[j]*b[k-j] for j in range(k+1)) for k in range(N))
def power(k):
    # Integer generalized binomial coefficients for (1+x)^k.
    a=[1]
    for i in range(1,N):a.append(a[-1]*(k-i+1)//i)
    return tuple(a)
DELTA=add(power(1),power(-1))
def mv(a):return tuple(a[i]+(a[i-1] if i else 0) for i in range(N))
def neg(a):return tuple(-x for x in a)
def accumulate(d,key,value):
    if key in d:value=add(d[key],value)
    if any(value):d[key]=value
    elif key in d:del d[key]
def cup(k,i):return bytes([x if x<i else x+2 for x in k[:i]]+[i+1,i]+[x if x<i else x+2 for x in k[i:]])
def ei(k,i):
    if k[i]==i+1:return k,True
    a,b=k[i],k[i+1];r=bytearray(k);r[i]=i+1;r[i+1]=i;r[a]=b;r[b]=a
    return bytes(r),False
def cap(k,i):
    r,circle=ei(k,i)
    return bytes(x if x<i else x-2 for j,x in enumerate(r) if j not in (i,i+1)),circle
def step(states,event):
    kind,a,b=event;i=min(a,b);out={}
    if kind=='cup':return {cup(k,i):v for k,v in states.items()}
    if kind=='cap':
        for k,v in states.items():
            key,circle=cap(k,i);accumulate(out,key,mul(DELTA,v) if circle else v)
        return out
    assert kind=='cross'
    for k,v in states.items():
        key,circle=ei(k,i)
        if circle:
            # I-v*delta=-v^2; delta-v=v^-1, exact identities.
            accumulate(out,k,neg(mv(mv(v))) if a<b else mul(power(-1),v))
        elif a<b:
            accumulate(out,k,v);accumulate(out,key,neg(mv(v)))
        else:
            accumulate(out,k,neg(mv(v)));accumulate(out,key,v)
    return out
def probe(pd,events,missing=0,cap_states=800000,seconds=600,progress=None):
    import snappy
    L=snappy.Link(pd);start=time.monotonic();states={b'':ONE};peak=1
    def timeout(*_):raise TimeoutError('COMPACT_TIME_LIMIT_INCONCLUSIVE')
    prior=signal.signal(signal.SIGALRM,timeout);signal.alarm(seconds)
    try:
        for j,event in enumerate(events):
            states=step(states,event);peak=max(peak,len(states))
            if peak>cap_states:raise RuntimeError('COMPACT_STATE_LIMIT_INCONCLUSIVE')
            if j%10==0:
                rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                if sys.platform!='darwin':rss*=1024
                if rss>1300*1024**2:raise MemoryError('COMPACT_1300_MIB_LIMIT_INCONCLUSIVE')
                if progress:progress({'event':j,'states':len(states),'peak':peak,'rss_bytes':rss,'seconds':time.monotonic()-start})
        assert not(set(states)-{b''})
        signs=[c.sign for c in L.crossings];m,plus=signs.count(-1),signs.count(1)
        value=mul(power(plus-2*m),states.get(b'',ZERO))
        if m%2:value=neg(value)
        for _ in range(missing):value=mul(value,DELTA)
        return {'coefficients_integer':value,'max_states':peak,'seconds':time.monotonic()-start,'precision':N,'last_event':j,'state_cap':cap_states,'time_limit_seconds':seconds,'memory_limit_mib':1300}
    finally:signal.alarm(0);signal.signal(signal.SIGALRM,prior)
