"""Suzuki(2,2) from integer Taylor order8 and Habiro's baseline theorem."""
from pathlib import Path
import json,sys,time,sympy as S,snappy,regina
p=Path(__file__).parent;sys.path.insert(0,str(p.resolve().parents[1]/'scripts'))
from selective_cable import data
from cable import cable_braid
from suzuki_taylor_order8 import Jet,probe
label=sys.argv[1];out=p/'suzuki_double'/label;out.mkdir(parents=True,exist_ok=True)
if (out/'RESULT.json').exists():raise FileExistsError('Preserve completed output')
cases=[p/'suzuki_mixed'/f'{label}_c{i}' for i in [0,1]];inputs=[json.loads((f/'INPUT.json').read_text()) for f in cases];polys=[json.loads((f/'POLYNOMIALS.json').read_text()) for f in cases]
word=inputs[0]['full_cable']['input_braid'];assert word==inputs[1]['full_cable']['input_braid'],'Different braid markings'
n,cycles,colors=data(word);assert len(cycles)==2;pos=list(range(n));wr=[0,0]
for g in word:
 i=abs(g)-1;a,b=pos[i:i+2]
 if colors[a]==colors[b]:wr[colors[a]]+=1 if g>0 else -1
 pos[i],pos[i+1]=b,a
cw,ns=cable_braid(word,n,2,0,0)
for ci,cycle in enumerate(cycles):
 anchor=2*min(cycle)+1;cw+=([anchor] if wr[ci]<0 else [-anchor])*(2*abs(wr[ci]))
C=snappy.Link(braid_closure=cw);assert len(C.link_components)==4 and not any(x for r in C.linking_matrix() for x in r)
rawpd=C.PD_code();C.simplify('global');inp={'label':label,'input_braid':word,'cycles':cycles,'component_self_writhes':wr,'output_braid':cw,'raw_pd':rawpd,'simplified_pd':C.PD_code(),'unlinked_components':4-len(C.link_components),'linking_matrix':C.linking_matrix()};(out/'INPUT.json').write_text(json.dumps(inp,indent=2)+'\n')
v=S.Symbol('v');z=Jet([1,1]);delta=z+z**-1;eps=z**3+z**-3;a=delta+eps;b=delta*eps

def convert(expr):
 result=Jet(0)
 for term in S.Add.make_args(S.expand(expr)):
  exp=int(term.as_powers_dict().get(v,0));coef=int(term/v**exp);result=result+coef*z**exp
 return result

def stored(ci,key):
 if key=='AA' and key not in polys[ci]:assert not inputs[ci]['selected_knot_pd'];return delta**2
 if key not in polys[ci]:raise KeyError('Missing exact smaller trace '+key)
 return convert(S.sympify(polys[ci][key]['polynomial']))
start=time.monotonic()
if not C.crossings:trace=delta**4;record={'coefficients_integer':list(trace.d),'crossings':0}
else:
 C.unlinked_unknot_components=0;record=probe(C);trace=Jet(record['coefficients_integer'])*delta**(4-len(C.link_components))
N=trace-a*(stored(0,'AAB')+stored(1,'AAB'))+b*(stored(0,'AA')+stored(1,'AA'))+a*a*stored(0,'L')-a*b*(stored(0,'A')+stored(0,'B'))+b*b
r={**record,'label':label,'numerator_coefficients_integer':list(N.d),'habiro_baseline_low_orders_vanish':not any(N.d[:6]),'ribbon_obstructed_exact':bool(any(N.d[6:8])),'seconds':time.monotonic()-start,'scope':'Exact(2,2) extra ideal criterion using Habiro baseline. N must vanish to order8 atv=1. Source identity qualified; passing does not prove ribbonness.'}
# On small controls compare the new four-component trace to independent full Regina.
if C.crossings and len(C.crossings)<=50:
 R=regina.Link.fromPD([[x+1 for x in row] for row in C.PD_code()]);J=R.jones(regina.Algorithm.Treewidth);full=(v+v**-1)**(5-len(C.link_components))*sum(int(str(J[i]))*(-1 if i%2 else 1)*v**i for i in range(J.minExp(),J.maxExp()+1));assert list(convert(full).d)==list(trace.d);r['independent_full_regina_agrees']=True
assert r['habiro_baseline_low_orders_vanish'],'Habiro baseline failed'
if label=='L10n36':assert not r['ribbon_obstructed_exact'],'Known ribbon control failed'
(out/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='morse_events'}),flush=True)
