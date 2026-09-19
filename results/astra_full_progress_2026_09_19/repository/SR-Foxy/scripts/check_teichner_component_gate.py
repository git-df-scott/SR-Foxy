#!/usr/bin/env python3
"""Independent determinant checks and explicit Fox-Milnor norm witnesses."""
from collections import Counter
import json
from pathlib import Path
import snappy,sympy
from component_guided_bands import jones
from fission_ancestry_audit import determinant
from teichner_component_slice_gate import norm_test
T=sympy.Symbol('t');D=json.loads(Path('results/teichner_component_slice_gate.json').read_text());assert D['complete'] and D['unknown_component_calculations']==0
checks=[]
for key,row in D['components'].items():
    L=snappy.Link(row['pd'])
    if not L.crossings:L.unlinked_unknot_components=1
    det=determinant(jones(L));assert det==row['determinant']
    check={'component':key,'determinant_by_Jones':det}
    if 'alexander_coefficients_low_to_high' in row:
        P=sympy.Poly(sum(n*T**i for i,n in enumerate(row['alexander_coefficients_low_to_high'])),T);_,factors=sympy.factor_list(P.as_expr(),T);F=sympy.Poly(1,T)
        canon=lambda p:tuple(int(x) for x in (p if p.LC()>0 else -p).all_coeffs())
        for f,n in factors:
            f=sympy.Poly(f,T);k=canon(f);r=canon(sympy.Poly.from_list(list(reversed(k)),T))
            if k==r:
                assert n%2==0;F*=f**(n//2)
            elif k<r:F*=f**n
        reverse=sympy.Poly.from_list(list(reversed(F.all_coeffs())),T);N=F*reverse
        assert N.eval(1) in [-1,1];N=N.mul_ground(int(N.eval(1)))
        assert N==P
        check['explicit_norm_factor_low_to_high']=[int(F.nth(i)) for i in range(F.degree()+1)]
    checks.append(check)
Path('results/teichner_component_gate_validation.json').write_text(json.dumps({'status':'PASSED','independent_Jones_determinants':len(checks),'explicit_norm_factorizations':sum('explicit_norm_factor_low_to_high' in r for r in checks),'checks':checks,'limitations':'Norm and determinant conditions are necessary, not sliceness proofs. HFK computed by the existing library.'},separators=(',',':'))+'\n');print('independent determinants',len(checks),flush=True)
