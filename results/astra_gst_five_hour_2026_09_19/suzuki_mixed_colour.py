"""Exact mixed Habiro colours(2,1), with explicit zero-framed selective cabling."""
import json,sys,time,collections
from pathlib import Path
import snappy,regina,sympy as S
from selective_cable import data,double_component
from spherogram.links.bands.core import normalize_crossing_labels
p=Path(__file__).parent;v=S.Symbol('v');d=v+1/v;e=v**3+v**-3;q=v*v
label=sys.argv[1];ci=int(sys.argv[2]);out=p/'suzuki_mixed'/f'{label}_c{ci}';out.mkdir(parents=True,exist_ok=True)
if (out/'RESULT.json').exists():raise FileExistsError('Completed output exists')
if label.startswith('GST'):L=snappy.Link(json.loads((p/f'RECONSTRUCTED_n{int(label[3:])}.json').read_text())['pd'])
elif label=='split_trefoil':L=snappy.Link(braid_closure=[1,1,1,2,-2])
elif label=='unlink':L=snappy.Link(braid_closure=[1,-1])
else:L=snappy.Link(label)
word=L.braid_word();n,cycles,colors=data(word);B=snappy.Link(braid_closure=word);normalize_crossing_labels(B);assert len(cycles)==2
# Match braid cycles to imported component ordering by original crossing visits.
pos=list(range(n));sigs=[collections.Counter() for c in cycles]
for j,g in enumerate(word):
 i=abs(g)-1
 for x in pos[i:i+2]:sigs[colors[x]][j]+=1
 pos[i],pos[i+1]=pos[i+1],pos[i]
bsigs=[collections.Counter(z.crossing.label for z in comp) for comp in B.link_components]
matches=[i for i,x in enumerate(bsigs) if x==sigs[ci]];assert matches,('Missing cycle marker',matches)
if len(matches)>1:assert all(max(x.values())==1 for x in sigs),'Ambiguous knotted components'
ai=matches[0];bi=1-ai
K=B.sublink([ai]);K.simplify('global');H=B.sublink([bi]);H.simplify('global');C,meta=double_component(word,ci)
assert all(x==0 for row in meta['linking_matrix'] for x in row)
inputs={'original_pd':L.PD_code(),'braid_pd':B.PD_code(),'selected_component':ai,'selected_knot_pd':K.PD_code(),'other_knot_pd':H.PD_code(),'full_cable':meta};(out/'INPUT.json').write_text(json.dumps(inputs,indent=2)+'\n')
polys={}
def J(tag,X,count):
 X=X.copy();X.simplify('global');visible=len(X.link_components)
 if not X.crossings:poly=S.expand(d**count)
 else:
  R=regina.Link.fromPD([[a+1 for a in row] for row in X.PD_code()]);j=R.jones(regina.Algorithm.Treewidth);poly=S.expand(d**(count-visible+1)*sum(int(str(j[k]))*(-1 if k%2 else 1)*v**k for k in range(j.minExp(),j.maxExp()+1)))
 polys[tag]={'simplified_pd':X.PD_code(),'expected_components':count,'crossings':len(X.crossings),'polynomial':str(poly)};(out/'POLYNOMIALS.json').write_text(json.dumps(polys,indent=2)+'\n');return poly
JA=J('A',K,1);JB=J('B',H,1);JL=J('L',B,2)
if not K.crossings:JAA=d*d
else:
 AA,aa=double_component(K.braid_word(),0);inputs['selected_component_cable']=aa;(out/'INPUT.json').write_text(json.dumps(inputs,indent=2)+'\n');JAA=J('AA',AA,2)
JAAB=J('AAB',C,3)
colored=S.cancel(v**3*(JAAB-d*JAA-(d+e)*JL+(d+e)*d*JA+d*e*JB-d*d*e)/((q-1)**2*(q*q-1)))
H2=(q**5-1)*(q**4-1)*(q**3-1)/(q-1)
def integral(x):
 num,den=S.fraction(S.cancel(x));dp=S.Poly(den,v)
 if len(dp.terms())!=1:return False,str(S.factor(den))
 return all((i-dp.monoms()[0][0])%2==0 and (a/dp.coeffs()[0]).is_Integer for (i,),a in S.Poly(num,v).terms()),str(den)
base,bd=integral(colored/H2);ribbon,rd=integral(colored/(H2*(q-1)))
r={'label':label,'doubled_cycle':ci,'selected_component':ai,'habiro_baseline_pass':bool(base),'suzuki_ribbon_pass':bool(ribbon),'coloured_J':str(S.factor(colored)),'ribbon_quotient_denominator':rd,'scope':'Exact ideal test on encoded link with calibrated framing. A pass is not ribbonness; source identification remains qualified.'}
(out/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True);assert base,'Baseline failed: normalization error'
if label in ['L10n36','unlink']:assert ribbon,'Known ribbon control failed'
