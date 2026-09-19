import sympy as s
from math import comb
z=s.symbols('z')
S=[s.Integer(1),z]
for r in range(2,10): S.append(s.expand(z*S[-1]-S[-2]))
E=s.symbols('E0:10')
for n in range(2,9):
 f={r:s.cancel(sum(S[r].coeff(z,j)*z**j*(1 if j==0 else E[j]) for j in range(r+1))/S[r]) for r in range(n%2,n+1,2)}
 out={j:s.cancel(sum((comb(n,(n-r)//2)-(comb(n,(n-r)//2-1) if (n-r)//2 else 0))*S[r].coeff(z,j)*f[r] for r in range(n%2,n+1,2))) for j in range(n%2,n+1,2)}
 print('n',n)
 for j,v in out.items():
  numer,denom=s.fraction(v); pn=s.Poly(numer,z);pd=s.Poly(denom,z)
  valuation=min((k[0] for k,c in pn.terms() if c),default=999)-min((k[0] for k,c in pd.terms() if c),default=999)
  print(j,valuation, 'wanted',n-j)
  if n<=4:print('  ',s.factor(v))
