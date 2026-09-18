"""Extract rational longitude response; no search, memory bounded by input."""
from pathlib import Path
import sympy as s,json,resource,time
from sympy.polys.matrices import DomainMatrix
resource.setrlimit(resource.RLIMIT_CPU,(90,95))
p=Path(__file__).resolve().parents[2]/'results/astra_2026_09_17_collar_boundary_audit/check_surgery_alexander.py'
ns={'__file__':str(p)};exec(compile(p.read_text().split('out=[]\nfor n in [0,1]:')[0],str(p),'exec'),ns)
t=ns['t']; reference=ns['reference']; fox=ns['fox']
cols=[i for i in range(ns['N']) if i!=reference-1]
aux=[cols.index(ns['meridians'][c]-1) for c in (1,2)]
order=[j for j in range(len(cols)) if j not in aux]+aux
M=s.Matrix([[fox(w)[cols[j]] for j in order] for w in ns['rels']])
# DomainMatrix uses rational-function exact arithmetic, no expression expansion.
R,piv=DomainMatrix.from_Matrix(M).to_field().rref(); R=R.to_Matrix()
assert list(piv)==list(range(len(cols)-2)),piv
Z=s.zeros(len(cols),2)
Z[-2,0]=1;Z[-1,1]=1
for i,col in enumerate(piv):
 for j in range(2):Z[col,j]=-R[i,-2+j]
assert M*Z==s.zeros(M.rows,2) or all(s.cancel(v)==0 for v in M*Z)
L=s.Matrix([[fox(ns['longs'][c])[cols[j]] for j in order] for c in (1,2)])
B=(L*Z).applyfunc(s.factor)
print(json.dumps({'response':[[str(v) for v in row] for row in B.tolist()],'rank':len(piv),'free_aux_meridian_columns':aux,'determinant':str(s.factor(B.det())),'hermitian':all(s.cancel(v)==0 for v in B-B.subs(t,1/t).T)},indent=2))
