#!/usr/bin/env python3
"""Astra: verify the saved boundary polynomial by independent stored inputs."""
import json, math
from pathlib import Path
import sympy as sp

def verify(d):
    if not __debug__: raise RuntimeError("Assertions must be enabled")
    t=sp.Symbol("t")
    c=d["alexander_coefficients_ascending"]
    polynomial=sum(x*t**i for i,x in enumerate(c))
    v=d["seifert_matrix_sparse"]
    V=sp.zeros(v["rows"],v["cols"])
    for i,j,x in v["entries"]:V[i,j]=x
    raw=sp.Poly((V-t*V.T).det(method="domain-ge"),t)
    removed=0
    while raw.degree()>0 and raw.nth(0)==0:
        raw=sp.Poly(raw.as_expr()/t,t);removed+=1
    if raw.LC()<0:raw=-raw
    assert raw.as_expr()==polynomial
    euler={}
    for (a,m),rank in d["hfk_ranks"]:
        euler[a]=euler.get(a,0)+(1 if m%2==0 else -1)*rank
    assert all(euler.get(a,0)==c[a+4] for a in range(-4,5))
    assert sum(v for k,v in d["hfk_ranks"])==d["hfk"]["total_rank"]==409
    f=sum(x*t**i for i,x in enumerate(d["fox_milnor_factor_ascending"]))
    assert sp.expand(f*t**4*f.subs(t,1/t))==polynomial
    old=(t**4-3*t**3+5*t**2-3*t+1)**2
    assert sp.expand(polynomial-old+t**2*(t**2-1)**2)==0
    assert polynomial.subs(t,-1)==169
    assert d["fox_surgery_verification"][0]["coefficients_ascending"]==[1,-6,19,-36,45,-36,19,-6,1]
    assert d["fox_surgery_verification"][1]["coefficients_ascending"]==c
    return {"status":"BOUNDARY_CHECKS_PASSED",
            "seifert_determinant_matches_hfk_euler":True,
            "seifert_removed_t_power":removed,
            "original_surgery_fox_matches_recovered_pd":True,
            "fox_milnor_norm":True,"equals_Abe_Tagami_difference_polynomial":False,
            "sliceness":"UNKNOWN","nonribbonness":"UNKNOWN"}

if __name__=="__main__":
    print(json.dumps(verify(json.loads(Path(__file__).with_name("BOUNDARY.json").read_text())),indent=2))
