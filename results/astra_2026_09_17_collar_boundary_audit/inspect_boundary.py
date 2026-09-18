#!/usr/bin/env python3
"""Recompute the saved PD's Seifert matrix and HFK; requires SnapPy and SymPy."""
from pathlib import Path
import json
PD=json.loads(Path(__file__).with_name("BOUNDARY.json").read_text())["pd_code"]

import snappy,sympy as sp,json,signal
K=snappy.Link(PD)
parts=K.deconnect_sum()
M=K.exterior()
out={'pd_code':K.PD_code(),'crossings':len(K.crossings),'planar':K.is_planar(),'components':len(K.link_components),'diagram_deconnect_sum_crossings':[len(p.crossings) for p in parts],'solution_type':M.solution_type(),'volume_numerical_not_certified':float(M.volume()),'meridian_marked_triangulation':M.triangulation_isosig(decorated=True)}
print(json.dumps(out),flush=True)
def timeout(*a):raise TimeoutError('20 second cap')
signal.signal(signal.SIGALRM,timeout)
try:
    signal.alarm(20)
    V=sp.Matrix(K.seifert_matrix());t=sp.Symbol('t');delta=sp.Poly((V-t*V.T).det(method='domain-ge'),t)
    while delta.degree()>0 and delta.nth(0)==0:delta=sp.Poly(delta.as_expr()/t,t)
    if delta.LC()<0:delta=-delta
    print(json.dumps({'seifert_matrix':[[int(x) for x in row] for row in V.tolist()],'alexander':str(delta.as_expr()),'determinant':int(abs(delta.eval(-1))),'is_input_difference_alexander':sp.expand(delta.as_expr()-(t**4-3*t**3+5*t**2-3*t+1)**2)==0}),flush=True)
except Exception as e: print(json.dumps({'alexander_status':'UNKNOWN','reason':type(e).__name__+': '+str(e)}),flush=True)
finally:signal.alarm(0)
try:
    signal.alarm(20)
    h=K.knot_floer_homology()
    print(json.dumps({'hfk':{str(k):v for k,v in h.items() if k!='ranks'},'ranks':[[list(k),v] for k,v in h.get('ranks',{}).items()]}),flush=True)
except Exception as e:print(json.dumps({'hfk_status':'UNKNOWN','reason':type(e).__name__+': '+str(e)}),flush=True)
finally:signal.alarm(0)
