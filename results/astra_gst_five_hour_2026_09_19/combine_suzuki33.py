from pathlib import Path
import sys,json,sympy as S
from suzuki_root_minus_one import Jet
p=Path(__file__).parent;name=sys.argv[1];out=p/'suzuki33'/name;design=json.loads((p/'SUZUKI_33_DESIGN.json').read_text());Jet.order=5;z=Jet([10,1]);v=S.Symbol('v');total=Jet(0);missing=[];terms=[]
def convert(expr):
 ans=Jet(0)
 for term in S.Add.make_args(S.expand(expr)):
  exp=int(term.as_powers_dict().get(v,0));ans=ans+int(term/v**exp)*z**exp
 return ans
for t in design['terms']:
 a,b=t['a'],t['b']
 if t['minimum_trace_precision_to_test_order5']==0:continue
 f=out/f'{a}{b}'/'RESULT.json'
 if not f.exists():missing.append([a,b]);continue
 r=json.loads(f.read_text());assert r['precision']>=t['minimum_trace_precision_to_test_order5'];contribution=convert(S.sympify(t['coefficient']))*Jet(r['coefficients_mod101']);total=total+contribution;terms.append({'a':a,'b':b,'contribution':list(contribution.d)})
r={'label':name,'prime':101,'root_v':10,'complete':not missing,'missing_terms':missing,'partial_or_full_numerator_jet':list(total.d),'terms':terms,'scope':'q=-1 part ofSuzuki(3,3)only. Nonzero coefficient4 after baselinezeros obstructs; zero mod101 is inconclusive. Missing traces prevent conclusions.'}
if not missing:
 assert not any(total.d[:4]),'Habiro baseline failed; investigate'
 r.update(habiro_baseline_pass_mod101=True,ribbon_obstructed_mod101=bool(total.d[4]))
 if name=='L10n36':assert not r['ribbon_obstructed_mod101'],'Known ribbon control failed'
(out/'COMBINED.json').write_text(json.dumps(r,indent=2)+'\n');print({k:v for k,v in r.items() if k!='terms'},flush=True)
