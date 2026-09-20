"""Recheck published GST polynomial arithmetic; this is not a ribbon obstruction."""
import json
from pathlib import Path
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
P=Path(__file__).parent;t=s.Symbol('t')
f=t**8-2*t**7+t**6+t**5-2*t**4+t**3-1
g=t**8-t**5+2*t**4-t**3-t**2+2*t-1
A=3*t**7+t**6+t**5+16*t**3-4*t**2-24*t-32
B=-3*t**7+5*t**6-2*t**5-5*t**4-t**3+19*t**2+2*t-11
assert s.expand(g+t**8*f.subs(t,1/t))==0
assert s.expand(A*f+B*g)==43
assert all(s.Poly(q,t,modulus=2).is_irreducible for q in [f,g])
assert s.resultant(f,g,t)==43**2
h=s.gcd(s.Poly(f,t,modulus=43),s.Poly(g,t,modulus=43))
assert h.as_expr()==t**2-4*t+1 and h.is_irreducible
assert s.rem(s.Poly(t**11-1,t,modulus=43),h).is_zero
M=s.Matrix([[s.expand(t**k*q).coeff(t,j) for j in range(16)] for q in [f,g] for k in range(8)])
SN=smith_normal_form(M,domain=s.ZZ);diag=[abs(int(SN[i,i])) for i in range(16)]
assert diag==[1]*14+[43,43]
D=-s.expand(f*g)
assert D.subs(t,1)==D.subs(t,-1)==1
assert abs(s.resultant(D,t**11-1,t))==43**4
result={'status':'PASS','f':str(f),'g':str(g),'resultant':1849,'smith_diagonal':diag,'gcd_mod43':str(h.as_expr()),'cover11_order':43**4,'scope':'Polynomial arithmetic independently rerun, not a fresh PD Alexander calculation, cover group decomposition or embedded-kernel obstruction.'}
(P/'GST_ALGEBRA_REPLAY.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
