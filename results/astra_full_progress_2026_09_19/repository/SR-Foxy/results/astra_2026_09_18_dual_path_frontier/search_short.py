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

adj={i:[] for i in range(len(roots))}
for c in sorted(A):
 for p in range(4):
  if (c,p)<A[c][p]:
   d,q=A[c][p];f0,f1=face[c,(p-1)%4],face[c,p]
   adj[f0].append((f1,(c,p)));adj[f1].append((f0,(d,q)))
for f in adj:adj[f].sort()
start=(13,2);end=(52,0);forbidden={face[start[0],(start[1]-1)%4],face[end]}
src=face[start];dst=face[end[0],(end[1]-1)%4]
paths=[]
def dfs(at,seen,ports):
 if at==dst:paths.append([start]+ports+[end]);return
 if len(ports)>=4:return
 for nxt,port in adj[at]:
  if nxt not in seen and nxt not in forbidden:dfs(nxt,seen|{nxt},ports+[port])
dfs(src,{src},[])

import itertools,contextlib,io
R=[1,1,2,4,5,3,1]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def mul(a,b):
 p=[0]*11
 for i,x in enumerate(a):
  for j,y in enumerate(b):p[i+j]+=x*y
 for k in range(10,5,-1):
  for j in range(6):p[k-6+j]-=p[k]*R[j]
 return tuple(p[:6])
zero=(0,)*6;one=(1,0,0,0,0,0);I=(one,zero,zero,one)
def mm(a,b):return (add(mul(a[0],b[0]),mul(a[1],b[2])),add(mul(a[0],b[1]),mul(a[1],b[3])),add(mul(a[2],b[0]),mul(a[3],b[2])),add(mul(a[2],b[1]),mul(a[3],b[3])))
def inv(a):return(a[3],neg(a[1]),neg(a[2]),a[0])
def evaluate(w,imgs):
 a=I
 for x in w:a=mm(a,imgs[x] if x>0 else inv(imgs[-x]))
 return a
source={int(k):tuple(tuple(p+[0]*(6-len(p))) for p in v) for k,v in CERT["source_matrices"].items()}
for w in CERT["source_relators"]:assert evaluate(w,source)==I
col={int(k)+1:evaluate(w,source) for k,w in CERT["boundary_arc_images"].items()}
qbase=g.quotient_R_wirtinger(g.adjacency_from_pd(g.SCAFFOLD))
rows=[]
for pi,path in enumerate(paths):
 for bits in itertools.product([False,True],repeat=len(path)-2):
  band={"along_top":path,"arc_is_under":bits,"twist":0}
  D=g.add_zero_twist_band(A,band);qf=g.quotient_R_wirtinger(D);mp=g.map_final_R_arcs_to_scaffold(qbase,qf)
  words=[]
  for comp in (1,2):
   cur=min(qf["components"][comp]);seen=set();word=[]
   while cur not in seen:
    seen.add(cur);c,p=cur
    if p in (0,2) and qf["cmap"][c,1]==qf["cmap"][c,3]==0:word.append((mp[qf["arcs"][c,1]]+1)*qf["signs"][c])
    cur=D[c][(p+2)%4]
   words.append(word)
  traces=[add(v[0],v[3]) for v in (evaluate(w,col) for w in words)]
  rec={"path_index":pi,"band":band,"axis_words":words,"traces":traces,"trace_match":traces[0]==traces[1]}
  if rec["trace_match"]:
   ns={"g":g,"D":D,"json":json,"math":__import__("math")}
   with contextlib.redirect_stdout(io.StringIO()):exec(FOX.replace("for n in [0,1]:","for n in [1]:"),ns)
   rec["surgery"]=ns["out"][0];rec["linking_sums"]=ns["linking"]
  rows.append(rec)
print(json.dumps({"paths":paths,"rows":rows,"scope":"Fixed first band; fixed second endpoints, simple dual paths through at most four internal edges, all over/under choices; exact trace gate for q0 only","CE":False}),flush=True)
