#!/usr/bin/env python3
"""Astra: read pinned repository input and reproduce the calculation."""
from pathlib import Path
import hashlib
CORE_PATH = "results/chat_archive_2026_09_17/expanded/SR_Foxy_pass09_product_collar_2026_09_17/pass09_product_collar/diagram_core.py"
CORE_SHA = "66cc09e760cbfbb6a41cc725972fb86e8af49cc3"
raw=(Path(__file__).resolve().parents[2]/CORE_PATH).read_bytes()
assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==CORE_SHA
CORE=raw.decode()

import types,json,math
g=types.ModuleType('core');exec(CORE,g.__dict__)
A=g.adjacency_from_pd(g.SCAFFOLD)
D=g.add_zero_twist_band(g.add_zero_twist_band(A,g.BAND1),g.BAND2)
cs,cmap,incoming,signs=g.oriented_component_data(D)
parent={(c,p):(c,p) for c in D for p in range(4)}
def root(a):
    while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
    return a
def join(a,b):parent[root(a)]=root(b)
for c in D:
    for p,x in enumerate(D[c]):join((c,p),x)
    join((c,1),(c,3))
roots=sorted({root(x) for x in parent})
rid={x:i+1 for i,x in enumerate(roots)}
arc={x:rid[root(x)] for x in parent}
eps={arc[x]:int(cmap[x]==0) for x in arc}
rels=[]
for c in D:
    ui=next(p for p in (0,2) if (c,p) in incoming)
    i,o,b=arc[c,ui],arc[c,(ui+2)%4],arc[c,1]
    s=signs[c];rels.append([-s*b,i,s*b,-o])
longs=[];meridians=[];linking=[]
for comp in range(3):
    cur=min(cs[comp]);seen=set();w=[];selfw=0;cross=[0]*3
    meridians.append(arc[cur])
    while cur not in seen:
        seen.add(cur);c,p=cur
        if p in (0,2):
            w.append(signs[c]*arc[c,1])
            cross[cmap[c,1]]+=signs[c]
            if cmap[c,1]==comp:selfw+=signs[c]
        cur=D[c][(p+2)%4]
    mi=meridians[-1]
    longs.append(([-mi]*selfw if selfw>=0 else [mi]*(-selfw))+w)
    linking.append(cross)
N=len(roots);reference=meridians[0]

import sympy as sp, signal
from sympy.matrices.normalforms import smith_normal_form
t=sp.Symbol('t')
def fox(w):
    row=[{} for _ in range(N)];prefix=0
    for x in w:
        e=eps[abs(x)]
        power=prefix if x>0 else prefix-e
        row[abs(x)-1][power]=row[abs(x)-1].get(power,0)+(1 if x>0 else -1)
        prefix+=e if x>0 else -e
    assert prefix==0
    return [sum(v*t**k for k,v in col.items()) for col in row]
def timeout(*a):raise TimeoutError('30 second symbolic Smith cap')
signal.signal(signal.SIGALRM,timeout)
out=[]
for n in [0,1]:
    try:
        signal.alarm(30)
        rr=[fox(w) for w in rels]
        for comp,p in [(1,1),(2,-1)]:
            row=[n*x for x in fox(longs[comp])]
            row[meridians[comp]-1]+=p;rr.append(row)
        rr=[r[:reference-1]+r[reference:] for r in rr]
        cleared=[]
        for row in rr:
            exps=[int(term.as_powers_dict().get(t,0)) for x in row for term in sp.Add.make_args(sp.expand(x)) if term!=0]
            e=min(exps) if exps else 0
            cleared.append([sp.expand(x*t**(-e)) for x in row])
        S=smith_normal_form(sp.Matrix(cleared),domain=sp.QQ.poly_ring(t))
        order=sp.Poly(sp.prod(S[i,i] for i in range(N-1)),t)
        while order.degree()>0 and order.nth(0)==0:order=sp.Poly(order.as_expr()/t,t)
        order=order.monic()
        out.append({'parameter':n,'status':'SYMBOLIC_FOX_ORDER_VERIFIED','polynomial':str(order.as_expr()),'coefficients_ascending':[int(order.nth(i)) for i in range(order.degree()+1)]})
    except Exception as e:out.append({'parameter':n,'status':'UNKNOWN','reason':type(e).__name__+': '+str(e)})
    finally:signal.alarm(0)
    print(json.dumps(out[-1]),flush=True)
