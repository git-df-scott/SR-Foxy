"""Assemble Suzuki's (2,2) numerator from exact order-eight traces."""
from pathlib import Path
import json,sympy as S
from compact_taylor import add,mul,power,neg,ZERO
p=Path(__file__).resolve().parent;old=p.parent/'astra_gst_five_hour_2026_09_19'
out=p/'GST3_SUZUKI_22.json';assert not out.exists()
read=lambda f:json.loads(f.read_text())
inputs=[read(old/f'suzuki_mixed/GST3_c{i}/INPUT.json') for i in (0,1)]
double=read(p/'gst3_order8/double/INPUT.json')
assert inputs[0]['full_cable']['input_braid']==inputs[1]['full_cable']['input_braid']==double['construction']['input_braid']
polys=[read(old/f'suzuki_mixed/GST3_c{i}/POLYNOMIALS.json') for i in (0,1)]
v=S.Symbol('v')
def stored(i,key):
    result=ZERO
    for term in S.Add.make_args(S.expand(S.sympify(polys[i][key]['polynomial']))):
        exp=int(term.as_powers_dict().get(v,0));coef=int(term/v**exp)
        result=add(result,tuple(coef*x for x in power(exp)))
    return result
assert stored(0,'L')==stored(1,'L')
delta=add(power(1),power(-1));eps=add(power(3),power(-3));a=add(delta,eps);b=mul(delta,eps)
j22=tuple(read(p/'gst3_order8/double/RESULT_COMPACT.json')['coefficients_integer'])
j21,j12=[tuple(read(p/f'gst3_order8/mixed{i}/RESULT.json')['coefficients_integer']) for i in (0,1)]
terms=[j22,neg(mul(a,add(j21,j12))),mul(b,add(stored(0,'AA'),stored(1,'AA'))),mul(mul(a,a),stored(0,'L')),neg(mul(mul(a,b),add(stored(0,'A'),stored(0,'B')))),mul(b,b)]
n=ZERO
for t in terms:n=add(n,t)
assert not any(n[:6]),'Habiro baseline fails: audit construction and normalization'
r={'numerator_coefficients_integer':n,'habiro_baseline_low_orders_vanish':True,'ribbon_obstructed_exact':bool(any(n[6:])),'criterion':'Suzuki (2,2), expansion at v=1 to order8 with q=v^2','terms':terms,'scope':'Link obstruction only. GST source identification remains qualified. Passing this criterion does not prove ribbonness or resolve knot Slice-Ribbon.'}
out.write_text(json.dumps(r,indent=2)+'\n');print(r)
