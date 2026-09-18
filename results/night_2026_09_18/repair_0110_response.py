"""Recompute the archived 0110 repair: a counterexample to the asserted
linking-number-to-polynomial implication, NOT a slice-ribbon counterexample.
"""
from pathlib import Path
import sympy as sp,json,resource
resource.setrlimit(resource.RLIMIT_CPU,(90,95))
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'results/astra_2026_09_17_collar_boundary_audit/check_surgery_alexander.py'
src=p.read_text().split('out=[]\nfor n in [0,1]:')[0]
needle='A=g.adjacency_from_pd(g.SCAFFOLD)'
assert src.count(needle)==1
src=src.replace(needle,"g.BAND1['arc_is_under']=[False,True]\ng.BAND2['arc_is_under']=[True,False]\n"+needle)
ns={'__file__':str(p)};exec(compile(src,str(p),'exec'),ns)
t=ns['t'];fox=ns['fox'];ref=ns['reference'];cols=[i for i in range(ns['N']) if i!=ref-1];aux=[cols.index(ns['meridians'][c]-1) for c in (1,2)];order=[j for j in range(len(cols)) if j not in aux]+aux
from sympy.polys.matrices import DomainMatrix
M=sp.Matrix([[fox(w)[cols[j]] for j in order] for w in ns['rels']]);rr,piv=DomainMatrix.from_Matrix(M).to_field().rref();rr=rr.to_Matrix()
assert list(piv)==list(range(len(cols)-2))
Z=sp.zeros(len(cols),2);Z[-2,0]=1;Z[-1,1]=1
for i,p in enumerate(piv):
 for j in range(2):Z[p,j]=-rr[i,-2+j]
assert all(sp.cancel(v)==0 for v in M*Z)
L=sp.Matrix([[fox(ns['longs'][c])[cols[j]] for j in order] for c in (1,2)])
B=(L*Z).applyfunc(sp.factor)
print(json.dumps({'bits':'0110','linking_sums':ns['linking'],'longitude_response':[[str(v) for v in row] for row in B.tolist()],'scope':'Same linking as 0000, different exact longitude response. Archived polynomial match independently rechecked below.'}),flush=True)
# Direct r=1 order, no appeal to a general surgery formula.
from sympy.matrices.normalforms import smith_normal_form
rows=[fox(w) for w in ns['rels']]
for c,p in [(1,1),(2,-1)]:
 row=fox(ns['longs'][c]);row[ns['meridians'][c]-1]+=p;rows.append(row)
M=[[sp.expand(v) for j,v in enumerate(row) if j!=ref-1] for row in rows]
while M and M[0]:
 found=None
 for i,row in enumerate(M):
  for j,v in enumerate(row):
   c,e=v.as_coeff_exponent(t)
   if c in [1,-1] and e.is_Integer:found=(i,j,v);break
  if found:break
 if not found:break
 a,b,p=found
 M=[[sp.expand(M[i][j]-M[i][b]*M[a][j]/p) for j in range(len(M[0])) if j!=b] for i in range(len(M)) if i!=a]
M=[r for r in M if any(v!=0 for v in r)]
for i,row in enumerate(M):
 ex=[int(term.as_powers_dict().get(t,0)) for v in row for term in sp.Add.make_args(v) if term!=0];m=min(ex) if ex else 0
 M[i]=[sp.expand(v*t**(-m)) for v in row]
S=smith_normal_form(sp.Matrix(M),domain=sp.QQ.poly_ring(t));d=sp.Poly(sp.prod(S[i,i] for i in range(S.cols)),t)
while d.nth(0)==0:d=sp.Poly(d.as_expr()/t,t)
d=d.monic();target=(t**4-3*t**3+5*t**2-3*t+1)**2
assert sp.expand(d.as_expr()-target)==0
print(json.dumps({'parameter':1,'exact_polynomial':str(d.as_expr()),'matches_target':True,'counterexample_to_slice_ribbon':False,'meaning':'Refutes uniform non-target-polynomial claim from linking zero, not a geometric concordance certificate'}),flush=True)
