#!/usr/bin/env python3
"""Compare direct D01 jets with cleared colored connected-sum identities.
No division by delta at the root is performed. Needs completed p=1,2,3 jobs.
"""
import hashlib,json
from pathlib import Path
import sympy as S
P=Path(__file__).resolve().parent
x=S.symbols('x');mod=S.Poly((x*x+1)**5,x)
def red(f):return S.rem(f,mod.as_expr(),x).expand()
xi=S.invert(x,mod.as_expr(),x)
delta=red(-x-xi)
def poly(target,p):
 r=json.loads((P/f'results/{target}_p{p}/result.json').read_text())
 if r['status']!='COMPUTED' or r['raw']['modulus'] is not None:raise RuntimeError('missing exact result')
 return S.Poly.from_list(list(reversed(r['raw']['coefficients_x'])),x).as_expr()
def mirror(f):
 ans=S.Integer(0)
 for c in S.Poly(f,x).all_coeffs():ans=red(ans*xi+c)
 return ans
A={j:poly('K0',j) for j in (1,2,3)}
B={j:mirror(poly('K1',j)) for j in (1,2,3)}
D={j:poly('D01',j) for j in (1,2,3)}
identities={
 'ordinary':red(delta*D[1]-A[1]*B[1]),
 'two_parallel':red((delta**2-1)*D[2]-(A[2]*B[2]-A[2]-B[2]+delta**2)),
 'three_parallel':red(delta*(delta**2-2)*D[3]-(A[3]*B[3]-2*A[3]*B[1]-2*A[1]*B[3]+2*delta**2*A[1]*B[1]))}
if any(identities.values()):raise RuntimeError({k:str(v) for k,v in identities.items()})
# Satisfying a nonzero-modulus identity is required; mutate D02 at its leading
# order and require the full two-parallel relation to reject it.
mutation=red((delta**2-1)*(D[2]+delta**2)-(A[2]*B[2]-A[2]-B[2]+delta**2))
if mutation==0:raise RuntimeError('mutation was not detected')
a2=b2=-23;a3=b3=-1067;d=13
pred2=a2+b2-1;pred3=a3*d+d*b3-d*d
diffs={2:pred2-(d*d)**2,3:pred3-(d*d)**3}
out={'status':'DIRECT_AND_COMPOSED_JETS_AGREE','counterexample_found':False,'modulus':'(x^2+1)^5 over Z','cleared_composition_remainders':{k:str(v) for k,v in identities.items()},'checks_passed':4,'mutated_two_parallel_rejected':True,'D01':{'e2':pred2,'e3':pred3,'determinant':d*d,'e2_difference_divided_32':diffs[2]//32,'e3_difference_divided_32':diffs[3]//32,'both_mod32_necessary_conditions_pass':all(v%32==0 for v in diffs.values())},'limitation':'Composition identities are checked only to the available jet order. Shared cabler/state-sum engine; not independent knot identity or disk verification.','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
f=P/'results/composition_check.json'
if f.exists():raise RuntimeError('refusing overwrite')
f.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
