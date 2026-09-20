from pathlib import Path
import sympy as S,json
q=S.Symbol('q');out=[]
for l in range(9):
 def fac(n):return S.prod(q**j-1 for j in range(1,n+1))
 gens=[fac(l-k)*fac(k) for k in range(l+1)];g=S.Poly(gens[0],q)
 for a in gens[1:]:g=S.gcd(g,S.Poly(a,q))
 formula=S.prod(S.cyclotomic_poly(m,q)**max(0,(l+1)//m-1) for m in range(1,l+1));assert S.expand(g.as_expr()-formula)==0
 out.append(dict(l=l,generator=str(S.factor(formula)),cyclotomic_exponents={m:(l+1)//m-1 for m in range(1,l+1) if (l+1)//m-1>0}))
(Path(__file__).parent/'SUZUKI_IDEAL_TABLE.json').write_text(json.dumps({'rows':out,'scope':'Symbolic gcd check agrees with Suzuki Theorem3.1. Principality over Z comes from the theorem, not from polynomial gcd alone.'},indent=2)+'\n');print(out[:4])
