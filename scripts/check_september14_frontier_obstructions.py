#!/usr/bin/env python3
"""Independent polynomial checks for the two new component exclusions."""
from collections import Counter
import hashlib,json
from pathlib import Path
import snappy,sympy
from nonfibered_reverse_audit import hfk
from fusion_successors import diagram_signature
T=sympy.Symbol('t')
src=Path('results/september14_frontier_components.json')
D=json.loads(src.read_text());checks=[]
for key,row in D['components'].items():
    if not row['rejections']:continue
    V=sympy.Matrix(snappy.Link(row['pd']).seifert_matrix());N=V.rows
    P=sympy.Poly.from_list(list(reversed(row['alexander_coefficients_low_to_high'])),T)
    assert N%2==0 and P.degree()%2==0 and N>=P.degree()
    expected=sympy.Poly(T**((N-P.degree())//2)*P.as_expr(),T)
    # Both are degree <= N. N+1 distinct exact integer evaluations prove equality.
    evaluations=[]
    for x in range(N+1):
        actual=int((x*V-V.T).det(method='domain-ge'))
        assert actual==expected.eval(x)
        evaluations.append([x,actual])
    extra={}
    if 'tau_nonzero' in row['rejections']:
        mirror=hfk(snappy.Link(row['pd']).mirror().PD_code())
        assert mirror['tau']==-row['HFK']['tau']
        assert sorted(mirror['ranks'])==sorted([[-a,-m,n] for a,m,n in row['HFK']['ranks']])
        extra['mirror_HFK']=mirror
    checks.append({'component':key,'seifert_size':N,'full_polynomial_identity_checked':True,
                   'exact_evaluations':evaluations,**extra})

# SnapPy's Whitehead example uses a free abelian basis, not component meridians.
a,b,x,y=sympy.symbols('a b x y');M=snappy.Manifold('L5a1');G=M.fundamental_group()
assert G.generators()==['a','b']
meridians=[mu for mu,la in G.peripheral_curves()]
exponents=[[mu.count(g)-mu.count(g.upper()) for g in ['a','b']] for mu in meridians]
assert sorted(exponents)==[[1,1],[1,2]]
reported=a*a*b**3-a*b*b-a*b+1
assert sympy.expand(reported-(a*b-1)*(a*b*b-1))==0
assert abs(int(sympy.Matrix(exponents).det()))==1
converted=sympy.cancel(reported.subs({a:x*x/y,b:y/x},simultaneous=True))
assert sympy.expand(converted-(x-1)*(y-1))==0
rec={'status':'PASSED','input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
     'component_checks':checks,'whitehead_basis_check':{'generators':G.generators(),
     'relators':G.relators(),'meridians':meridians,'meridian_exponents':exponents,
     'reported_polynomial':str(reported),'component_basis_polynomial':str(sympy.factor(converted)),
     'conclusion':'The alleged Torres failure was a basis mismatch; it does not establish a different polynomial invariant.'},
     'scope':'Full Alexander identities checked independently; mirror HFK uses the same library and is only a consistency check. The one failed HFK calculation remains unknown.'}
Path('results/september14_frontier_validation.json').write_text(json.dumps(rec,indent=2)+'\n')
print('checked',len(checks),'component obstructions and Whitehead meridian basis',flush=True)
