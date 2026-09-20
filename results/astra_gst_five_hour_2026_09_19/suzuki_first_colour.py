"""Suzuki Theorem1.5, all reduced colours P'_1, using ordinary sublink Jones.
q_suzuki=v^2; J_unreduced=delta*V_repo; zero pairwise linking and zero framing.
"""
import json,sys,itertools
from pathlib import Path
import sympy as S
import snappy
p=Path(__file__).parent;sys.path.insert(0,str(p.resolve().parents[1]/'scripts'))
from sagefree_jones import jones_polynomial
v=S.Symbol('v');q=S.Symbol('q');delta=v+v**-1
known=json.loads((p/'REGINA_JONES_CHECK.json').read_text())['rows'];known={r['label']:r['converted_q_coefficients'] for r in known};components={r['n']:r['component_jones'] for r in json.loads((p/'COMPONENT_JONES_CHECK.json').read_text())}
def expr(d):return sum(int(c)*v**int(e) for e,c in d.items())
def test(label,n,sub):
 total=0
 for mask in range(1<<n):
  size=mask.bit_count();J=1 if not mask else delta*expr(sub[str(mask)]);total+=(-delta)**(n-size)*J
 colored=S.cancel(v**n*total/(v*v-1)**n)
 # max colour=1: Habiro base=(q^3-1)(q^2-1)/(q-1); each other I1=(q-1).
 habiro=(v**6-1)*(v**4-1)/(v*v-1);ribbon=habiro*(v*v-1)**(n-1)
 def integral_laurent(x):
  num,den=S.fraction(S.cancel(x));poly=S.Poly(den,v);monomial=len(poly.terms())==1
  if not monomial:return False,str(S.factor(den))
  for (e,),c in S.Poly(num,v).terms():
   if (e-poly.monoms()[0][0])%2 or not (c/poly.coeffs()[0]).is_Integer:return False,str(den)
  return True,str(den)
 baseline,bd=integral_laurent(colored/habiro);passed,rd=integral_laurent(colored/ribbon)
 return {'label':label,'components':n,'sublink_polynomials':sub,'reduced_coloured_J':str(S.factor(colored)),'habiro_baseline_pass':baseline,'suzuki_ribbon_pass':passed,'ribbon_quotient_denominator':rd}
rows=[]
for name in ['L10n36','L5a1','L6a4']:
 L=snappy.Link(name);n=len(L.link_components);assert all(x==0 for row in L.linking_matrix() for x in row)
 sub={}
 for mask in range(1,1<<n):
  C=L.sublink([i for i in range(n) if mask>>i&1]);C.simplify('global')
  if not C.crossings:poly=S.expand(delta**(mask.bit_count()-1))
  else:
   C.unlinked_unknot_components=0
   poly=S.expand(expr(jones_polynomial(C).d)*delta**(mask.bit_count()-len(C.link_components)))
  sub[str(mask)]={int(t.as_powers_dict().get(v,0)):int(t/v**t.as_powers_dict().get(v,0)) for t in S.Add.make_args(poly)}
 rows.append(test(name,n,sub))
for n in [1,2,3]:
 sub={'1':components[n][0],'2':components[n][1],'3':known[f'provisional_n{n}']};rows.append(test(f'provisional_GST_n{n}',2,sub))
for r in rows:print({k:v for k,v in r.items() if k!='sublink_polynomials'},flush=True)
assert all(r['habiro_baseline_pass'] for r in rows),'Normalization or implementation error'
assert rows[0]['suzuki_ribbon_pass'],'Known ribbon control failed'
assert not rows[2]['suzuki_ribbon_pass'],'Borromean positive obstruction control failed'
(p/'SUZUKI_FIRST_COLOUR.json').write_text(json.dumps({'rows':rows,'normalization':'v is repo q; Suzuki q=v^2. Zero linking makes the oriented Jones normalization agree with the zero-framing quantum trace. Mirror convention does not affect ideal membership.','source':'Suzuki, AGT10(2010),Theorem1.5; DOI10.2140/agt.2010.10.1027','scope':'First reduced colour only. Higher colours are untested; source GST identity remains qualified.'},indent=2)+'\n')
