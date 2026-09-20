import sys,json,time
from pathlib import Path
import snappy,sympy as S
p=Path(__file__).parent;sys.path.insert(0,str(p.resolve().parents[1]/'scripts'))
from suzuki_taylor_integer_seeded import probe,Jet
v=S.Symbol('v')
def convert(expr):
 out=Jet(0)
 for term in S.Add.make_args(S.expand(expr)):
  exp=int(term.as_powers_dict().get(v,0));coef=int(term/v**exp);out=out+coef*Jet([1,1])**exp
 return out
name=sys.argv[1];ci=int(sys.argv[2]);d=p/'suzuki_mixed'/f'{name}_c{ci}';inputs=json.loads((d/'INPUT.json').read_text());polys=json.loads((d/'POLYNOMIALS.json').read_text());L=snappy.Link(json.loads((d/'TAYLOR_INPUT_PD.json').read_text()));start=time.monotonic();r=probe(L)
if 'AAB' in polys:assert r['coefficients_integer']==list(convert(S.sympify(polys['AAB']['polynomial'])).d),'Taylor/full-Jones control mismatch'
if 'AA' not in polys:
 assert not inputs['selected_knot_pd']
 polys['AA']={'polynomial':str((v+1/v)**2)}
a={k:convert(S.sympify(polys[k]['polynomial'])) for k in ['A','B','L','AA']};z=Jet([1,1]);delta=z+z**-1;eps=z**3+z**-3
num=Jet(r['coefficients_integer'])-delta*a['AA']-(delta+eps)*a['L']+(delta+eps)*delta*a['A']+delta*eps*a['B']-delta*delta*eps
r.update(label=name,cycle=ci,numerator_jet_integer=list(num.d),baseline_low_orders_vanish=not any(num.d[:5]),ribbon_obstruction_exact=bool(num.d[5]),seconds=time.monotonic()-start,scope='Exact mixed(2,1) criterion, using Habiro baseline ideal theorem for the zero-framed algebraically split input. Numerator must vanish to order6 atv=1. Source identity remains qualified; passing does not prove ribbonness.')
assert r['baseline_low_orders_vanish'],'Habiro baseline failed'
(d/'TAYLOR_INTEGER_SEEDED_RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='morse_events'}),flush=True)
