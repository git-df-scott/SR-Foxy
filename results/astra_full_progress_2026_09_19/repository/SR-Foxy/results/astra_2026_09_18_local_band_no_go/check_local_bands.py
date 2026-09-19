#!/usr/bin/env python3
"""Astra: exact local-family audit. Reads repository inputs; prints JSON only."""
import json, hashlib
from pathlib import Path
if not __debug__:raise RuntimeError("Assertions must be enabled")
REPO=Path(__file__).resolve().parents[2]
PINNED={
  "results/chat_archive_2026_09_17/expanded/SR_Foxy_pass09_product_collar_2026_09_17/pass09_product_collar/diagram_core.py": "66cc09e760cbfbb6a41cc725972fb86e8af49cc3",
  "results/astra_2026_09_17_overnight/pass06_0055_explicit_unlink_bands/check_explicit_unlink_bands.py": "baf481237bbbcd9ab57c3c378a6fc8e34286c0ef",
  "results/astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json": "86bb4e5ec1ae5a1762f4ce724279c7c5a509fed6"
}
def pinned(path):
 raw=(REPO/path).read_bytes()
 assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==PINNED[path],path
 return raw.decode()
CORE=pinned("results/chat_archive_2026_09_17/expanded/SR_Foxy_pass09_product_collar_2026_09_17/pass09_product_collar/diagram_core.py")
UNLINK=pinned("results/astra_2026_09_17_overnight/pass06_0055_explicit_unlink_bands/check_explicit_unlink_bands.py")
FOX="\nimport types,json,math\ng=types.ModuleType('core');exec(CORE,g.__dict__)\nA=g.adjacency_from_pd(g.SCAFFOLD)\nD=g.add_zero_twist_band(g.add_zero_twist_band(A,g.BAND1),g.BAND2)\ncs,cmap,incoming,signs=g.oriented_component_data(D)\nparent={(c,p):(c,p) for c in D for p in range(4)}\ndef root(a):\n    while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]\n    return a\ndef join(a,b):parent[root(a)]=root(b)\nfor c in D:\n    for p,x in enumerate(D[c]):join((c,p),x)\n    join((c,1),(c,3))\nroots=sorted({root(x) for x in parent})\nrid={x:i+1 for i,x in enumerate(roots)}\narc={x:rid[root(x)] for x in parent}\neps={arc[x]:int(cmap[x]==0) for x in arc}\nrels=[]\nfor c in D:\n    ui=next(p for p in (0,2) if (c,p) in incoming)\n    i,o,b=arc[c,ui],arc[c,(ui+2)%4],arc[c,1]\n    s=signs[c];rels.append([-s*b,i,s*b,-o])\nlongs=[];meridians=[];linking=[]\nfor comp in range(3):\n    cur=min(cs[comp]);seen=set();w=[];selfw=0;cross=[0]*3\n    meridians.append(arc[cur])\n    while cur not in seen:\n        seen.add(cur);c,p=cur\n        if p in (0,2):\n            w.append(signs[c]*arc[c,1])\n            cross[cmap[c,1]]+=signs[c]\n            if cmap[c,1]==comp:selfw+=signs[c]\n        cur=D[c][(p+2)%4]\n    mi=meridians[-1]\n    longs.append(([-mi]*selfw if selfw>=0 else [mi]*(-selfw))+w)\n    linking.append(cross)\nN=len(roots);reference=meridians[0]\n\nimport sympy as sp, signal\nfrom sympy.matrices.normalforms import smith_normal_form\nt=sp.Symbol('t')\ndef fox(w):\n    row=[{} for _ in range(N)];prefix=0\n    for x in w:\n        e=eps[abs(x)]\n        power=prefix if x>0 else prefix-e\n        row[abs(x)-1][power]=row[abs(x)-1].get(power,0)+(1 if x>0 else -1)\n        prefix+=e if x>0 else -e\n    assert prefix==0\n    return [sum(v*t**k for k,v in col.items()) for col in row]\ndef timeout(*a):raise TimeoutError('30 second symbolic Smith cap')\nsignal.signal(signal.SIGALRM,timeout)\nout=[]\nfor n in [0,1]:\n    try:\n        signal.alarm(30)\n        rr=[fox(w) for w in rels]\n        for comp,p in [(1,1),(2,-1)]:\n            row=[n*x for x in fox(longs[comp])]\n            row[meridians[comp]-1]+=p;rr.append(row)\n        rr=[r[:reference-1]+r[reference:] for r in rr]\n        cleared=[]\n        for row in rr:\n            exps=[int(term.as_powers_dict().get(t,0)) for x in row for term in sp.Add.make_args(sp.expand(x)) if term!=0]\n            e=min(exps) if exps else 0\n            cleared.append([sp.expand(x*t**(-e)) for x in row])\n        S=smith_normal_form(sp.Matrix(cleared),domain=sp.QQ.poly_ring(t))\n        order=sp.Poly(sp.prod(S[i,i] for i in range(N-1)),t)\n        while order.degree()>0 and order.nth(0)==0:order=sp.Poly(order.as_expr()/t,t)\n        order=order.monic()\n        out.append({'parameter':n,'status':'SYMBOLIC_FOX_ORDER_VERIFIED','polynomial':str(order.as_expr()),'coefficients_ascending':[int(order.nth(i)) for i in range(order.degree()+1)]})\n    except Exception as e:out.append({'parameter':n,'status':'UNKNOWN','reason':type(e).__name__+': '+str(e)})\n    finally:signal.alarm(0)\n    print(json.dumps(out[-1]),flush=True)\n"

import types,json,itertools,contextlib,io,time
g=types.ModuleType("core");exec(CORE,g.__dict__)
u=types.ModuleType("unlink")
exec(UNLINK,u.__dict__)
base=g.adjacency_from_pd(g.SCAFFOLD);q=g.quotient_R_wirtinger(base)
rows=[]
for bits in itertools.product([False,True],repeat=4):
 b1=dict(g.BAND1,arc_is_under=list(bits[:2]));b2=dict(g.BAND2,arc_is_under=list(bits[2:]))
 D=g.add_zero_twist_band(g.add_zero_twist_band(base,b1),b2)
 qf=g.quotient_R_wirtinger(D);mp=g.map_final_R_arcs_to_scaffold(q,qf)
 words=[]
 for comp in (1,2):
  cur=min(qf["components"][comp]);seen=set();word=[]
  while cur not in seen:
   seen.add(cur);c,p=cur
   if p in (0,2) and qf["cmap"][c,1]==qf["cmap"][c,3]==0:word.append((mp[qf["arcs"][c,1]]+1)*qf["signs"][c])
   cur=D[c][(p+2)%4]
  words.append(word)
 eta,ret=u.sublink_delete_component(D,0)
 moves,active=u.r2_simplify(eta)
 rec={"bits":list(bits),"axis_words":words,"eta_pd":eta,"unlink_R2_moves":moves,"unlink_certified":not active}
 code=FOX.replace("g=types.ModuleType('core');exec(CORE,g.__dict__)","g=types.ModuleType('core');exec(CORE,g.__dict__)\ng.BAND1['arc_is_under']="+repr(list(bits[:2]))+"\ng.BAND2['arc_is_under']="+repr(list(bits[2:])))
 code=code.replace("for n in [0,1]:","for n in [1]:")
 ns={"CORE":CORE}
 try:
  with contextlib.redirect_stdout(io.StringIO()):exec(code,ns)
  rec["surgery"]=ns["out"][0]
  rec["linking_sums"]=ns["linking"]
 except Exception as e:rec["error"]=str(e)
 rows.append(rec)
expected=json.loads(Path(__file__).with_name("SCAN.json").read_text())
assert len(rows)==len(expected)==16
for actual,saved in zip(rows,expected):
 assert all(actual[k]==saved[k] for k in actual)
assert all(row["unlink_certified"] for row in rows[:8])
assert all(row["axis_words"]==rows[i+8]["axis_words"] for i,row in enumerate(rows[:8]))
print(json.dumps({"status":"ALL_16_LOCAL_VARIANTS_REPRODUCED","rows":rows}),flush=True)
