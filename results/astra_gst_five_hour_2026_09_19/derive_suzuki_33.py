"""Exact coefficients and cyclotomic orders for the first extra Phi2 test."""
import sympy as S,json
from pathlib import Path
v,X,Y=S.symbols('v X Y');q=v*v;h=v*v+1
P=S.prod(X-(v**(2*j+1)+v**(-2*j-1)) for j in range(3));co={a:S.expand(P).coeff(X,a) for a in range(4)}
def order(expr):
 num,den=S.fraction(S.cancel(expr));n=S.Poly(num,v);d=S.Poly(den,v);ord=0
 while not n.is_zero and S.rem(n,S.Poly(h,v)).is_zero:n=S.quo(n,S.Poly(h,v));ord+=1
 while S.rem(d,S.Poly(h,v)).is_zero:d=S.quo(d,S.Poly(h,v));ord-=1
 return ord
rows=[{'a':a,'b':b,'coefficient':str(S.factor(co[a]*co[b])),'coefficient_Phi2_order':order(co[a]*co[b]),'unreduced_cable_trace':f'J_{a}{b}','minimum_trace_precision_to_test_order5':max(0,5-order(co[a]*co[b]))} for a in range(4) for b in range(4)]
D=S.prod(q**i-1 for i in [1,2,3])**2;H3=S.prod(q**i-1 for i in [4,5,6,7])/(q-1);I3=(q-1)**3*(q+1)
assert order(D)==2 and order(H3)==2 and order(I3)==1
out={'variable_convention':'q_Suzuki=v^2; Phi2(q)=v^2+1','P3_numerator':str(S.factor(P)),'P3_prefactor':'v^3/((q-1)*(q^2-1)*(q^3-1))','terms':rows,'denominator_Phi2_order':order(D),'Habiro_H3_Phi2_order':order(H3),'extra_I3_Phi2_order':order(I3),'required_numerator_Phi2_order':5,'criterion':'Using Habiro baseline, the q=-1 part of Suzuki(3,3) is N33 divisible by (v^2+1)^5. Full I3 also requires order3 atq=1. Passing this local test does not establish all ideal conditions.','boundary_condition':'Boundary links satisfy Suzuki ideal by theorem; use known boundary links as passing controls.','coefficient_drop':'Terms with a+b<=1 have coefficient order>=5 and contribute zero to this local test. Remaining traces need the listed precisions; no extra trace nullity is assumed.'}
(Path(__file__).parent/'SUZUKI_33_DESIGN.json').write_text(json.dumps(out,indent=2)+'\n');print({k:x for k,x in out.items() if k not in ['terms','P3_numerator']})
