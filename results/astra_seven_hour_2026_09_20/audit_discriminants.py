"""Exact cyclotomic-field checks of the composite torus discriminant step."""
from pathlib import Path
import json,sympy as S
p=Path(__file__).resolve().parent
assert not (p/'DISCRIMINANTS.json').exists()
t=S.Symbol('t');z=S.CRootOf(S.Symbol('z')**2+S.Symbol('z')+1,1)
field=S.QQ.alg_field_from_poly(S.Poly(S.Symbol('z')**2+S.Symbol('z')+1),alias='z')
z=field.ext.as_expr()
def poly(e):return S.Poly(S.expand(e),t,domain=field)
def valuation(e):
    # omega=-z^2 is a primitive sixth root, with z*omega=-1.
    P=poly(e);factor=poly(t+z**2);n=0
    while P.degree()>0:
        q,r=P.div(factor)
        if not r.is_zero:break
        n+=1;P=q
    return n
rows=[];A=S.Matrix([[0,1],[t,0]]);I=S.eye(2)
for q in (3,9):
    for d in (0,1,2):
        ra=t**((q-1)//2)*A
        rb=S.diag(z**d/t,z**(-d)/t)
        # Verify alpha^2 beta^q=I entrywise in Q(z)[t,t^-1].
        rel=ra**2*rb**q-I
        assert all(poly(S.cancel(e*t**(2*q))).is_zero for e in rel)
        numerator=1-t**q
        # Denominator is t^2 det(rho(beta)-I); monomial units do not
        # affect valuation at omega. H0 and (1-t)^e add factors only at1.
        denominator=(t-z**d)*(t-z**(-d))
        nv,dv=valuation(numerator),valuation(denominator)
        assert nv==dv==0
        rows.append({'q':q,'character_phase_d':d,'numerator':'1-t^'+str(q),
                     'denominator':str(S.expand(denominator)),
                     'relator_verified':True,'omega_numerator_order':nv,'omega_denominator_order':dv})
Delta=lambda x:x*x-x+1
orders={'unshifted':valuation(Delta(t)), 'shift_plus':valuation(Delta(z*t)),
        'shift_minus':valuation(Delta(z**-1*t))}
assert orders=={'unshifted':1,'shift_plus':0,'shift_minus':1}
assert (orders['shift_plus']+orders['shift_minus']-2*orders['unshifted'])%2==1
r={'field':'Q(z), z^2+z+1=0','root':'omega=-z^2','torus_checks':rows,
   'companion_Delta':'t^2-t+1','companion_valuations':orders,
   'companion_discriminant_order_mod2':1,'total_discriminant_order_mod2':1,
   'scope':'Exact algebra verifies the formula extension at q=9. Source-backed Casson–Gordon and twisted-Alexander theorems are separate inputs.'}
(p/'DISCRIMINANTS.json').write_text(json.dumps(r,indent=2)+'\n')
print(r)
