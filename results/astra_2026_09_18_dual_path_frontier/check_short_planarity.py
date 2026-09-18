#!/usr/bin/env python3
"""Astra: fixed-endpoint dual-path search. Reads pinned repository data only."""
import json,hashlib
from pathlib import Path
if not __debug__:raise RuntimeError("Assertions must be enabled")
REPO=Path(__file__).resolve().parents[2]
INPUTS={"results/chat_archive_2026_09_17/expanded/SR_Foxy_pass09_product_collar_2026_09_17/pass09_product_collar/diagram_core.py":"66cc09e760cbfbb6a41cc725972fb86e8af49cc3","results/astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json":"86bb4e5ec1ae5a1762f4ce724279c7c5a509fed6"}
def read_pinned(path):
 raw=(REPO/path).read_bytes()
 assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==INPUTS[path]
 return raw.decode()
CORE=read_pinned("results/chat_archive_2026_09_17/expanded/SR_Foxy_pass09_product_collar_2026_09_17/pass09_product_collar/diagram_core.py")
CERT=json.loads(read_pinned("results/astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json"))
FOX="cs,cmap,incoming,signs=g.oriented_component_data(D)\nparent={(c,p):(c,p) for c in D for p in range(4)}\ndef root(a):\n    while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]\n    return a\ndef join(a,b):parent[root(a)]=root(b)\nfor c in D:\n    for p,x in enumerate(D[c]):join((c,p),x)\n    join((c,1),(c,3))\nroots=sorted({root(x) for x in parent})\nrid={x:i+1 for i,x in enumerate(roots)}\narc={x:rid[root(x)] for x in parent}\neps={arc[x]:int(cmap[x]==0) for x in arc}\nrels=[]\nfor c in D:\n    ui=next(p for p in (0,2) if (c,p) in incoming)\n    i,o,b=arc[c,ui],arc[c,(ui+2)%4],arc[c,1]\n    s=signs[c];rels.append([-s*b,i,s*b,-o])\nlongs=[];meridians=[];linking=[]\nfor comp in range(3):\n    cur=min(cs[comp]);seen=set();w=[];selfw=0;cross=[0]*3\n    meridians.append(arc[cur])\n    while cur not in seen:\n        seen.add(cur);c,p=cur\n        if p in (0,2):\n            w.append(signs[c]*arc[c,1])\n            cross[cmap[c,1]]+=signs[c]\n            if cmap[c,1]==comp:selfw+=signs[c]\n        cur=D[c][(p+2)%4]\n    mi=meridians[-1]\n    longs.append(([-mi]*selfw if selfw>=0 else [mi]*(-selfw))+w)\n    linking.append(cross)\nN=len(roots);reference=meridians[0]\n\nimport sympy as sp, signal\nfrom sympy.matrices.normalforms import smith_normal_form\nt=sp.Symbol('t')\ndef fox(w):\n    row=[{} for _ in range(N)];prefix=0\n    for x in w:\n        e=eps[abs(x)]\n        power=prefix if x>0 else prefix-e\n        row[abs(x)-1][power]=row[abs(x)-1].get(power,0)+(1 if x>0 else -1)\n        prefix+=e if x>0 else -e\n    assert prefix==0\n    return [sum(v*t**k for k,v in col.items()) for col in row]\ndef timeout(*a):raise TimeoutError('30 second symbolic Smith cap')\nsignal.signal(signal.SIGALRM,timeout)\nout=[]\nfor n in [0,1]:\n    try:\n        signal.alarm(30)\n        rr=[fox(w) for w in rels]\n        for comp,p in [(1,1),(2,-1)]:\n            row=[n*x for x in fox(longs[comp])]\n            row[meridians[comp]-1]+=p;rr.append(row)\n        rr=[r[:reference-1]+r[reference:] for r in rr]\n        cleared=[]\n        for row in rr:\n            exps=[int(term.as_powers_dict().get(t,0)) for x in row for term in sp.Add.make_args(sp.expand(x)) if term!=0]\n            e=min(exps) if exps else 0\n            cleared.append([sp.expand(x*t**(-e)) for x in row])\n        M=cleared\n        while M and M[0]:\n            found=None\n            for ai,row in enumerate(M):\n                for bi,x in enumerate(row):\n                    c,e=sp.sympify(x).as_coeff_exponent(t)\n                    if c in [1,-1] and e.is_Integer:found=(ai,bi,x);break\n                if found:break\n            if not found:break\n            ai,bi,pivot=found\n            M=[[sp.expand(M[i][j]-M[i][bi]*M[ai][j]/pivot) for j in range(len(M[0])) if j!=bi] for i in range(len(M)) if i!=ai]\n        M=[row for row in M if any(x!=0 for x in row)]\n        for i,row in enumerate(M):\n            exps=[int(term.as_powers_dict().get(t,0)) for x in row for term in sp.Add.make_args(sp.expand(x)) if term!=0]\n            e=min(exps) if exps else 0\n            M[i]=[sp.expand(x*t**(-e)) for x in row]\n        S=smith_normal_form(sp.Matrix(M),domain=sp.QQ.poly_ring(t))\n        order=sp.Poly(sp.prod(S[i,i] for i in range(S.cols)),t)\n        while order.degree()>0 and order.nth(0)==0:order=sp.Poly(order.as_expr()/t,t)\n        order=order.monic()\n        out.append({'parameter':n,'status':'SYMBOLIC_FOX_ORDER_VERIFIED','polynomial':str(order.as_expr()),'coefficients_ascending':[int(order.nth(i)) for i in range(order.degree()+1)]})\n    except Exception as e:out.append({'parameter':n,'status':'UNKNOWN','reason':type(e).__name__+': '+str(e)})\n    finally:signal.alarm(0)\n    print(json.dumps(out[-1]),flush=True)\n"
ROWS=json.loads(Path(__file__).with_name("SHORT_RESULTS.json").read_text())["rows"]

import types,json
g=types.ModuleType("core");exec(CORE,g.__dict__)
A=g.add_zero_twist_band(g.adjacency_from_pd(g.SCAFFOLD),g.BAND1)
parent={(c,p):(c,p) for c in A for p in range(4)}
def root(x):
 while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
 return x
def join(a,b):parent[root(a)]=root(b)
for c in A:
 for p,(d,q) in enumerate(A[c]):join((c,p),(d,(q-1)%4));join((c,(p-1)%4),(d,q))
roots=sorted({root(x) for x in parent});rid={x:i for i,x in enumerate(roots)};face={x:rid[root(x)] for x in parent}
def check_planarity(D):
 seen=set();faces=0
 for c in D:
  for p in range(4):
   if (c,p) in seen:continue
   faces+=1;x=(c,p)
   while x not in seen:
    seen.add(x);a,b=D[x[0]][x[1]];x=(a,(b-1)%4)
 assert faces==len(D)+2
for row in ROWS:
 b=row["band"];b["along_top"]=[tuple(x) for x in b["along_top"]]
 D=g.add_zero_twist_band(A,b);check_planarity(D);assert len(g.components(D))==3
print("ALL_88_DIAGRAMS_PLANAR_THREE_COMPONENTS")
