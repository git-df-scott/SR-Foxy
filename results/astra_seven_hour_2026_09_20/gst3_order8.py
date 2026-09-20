"""Upgrade two mixed traces and audit/contract GST3's four-parallel at order8."""
from pathlib import Path
import json,sys,time,random,signal,hashlib
from math import comb
import snappy,regina
p=Path(__file__).resolve().parent
old=p.parent/'astra_gst_five_hour_2026_09_19'
sys.path[:0]=[str(old),str(p.parents[1]/'scripts')]
from suzuki_taylor_order8 import Jet,Ring
from sagefree_jones import PerfectMatching,install
from spherogram.links import jones,exhaust
from variable_parallel import parallel
label=sys.argv[1];assert label in ('mixed0','mixed1','double')
layout_only='--layout-only' in sys.argv
out=p/'gst3_order8'/label;out.mkdir(parents=True,exist_ok=True)
assert not (out/'RESULT.json').exists(),'Preserve completed traces'
def timeout(*_):raise TimeoutError('240_SECOND_LIMIT_INCONCLUSIVE')
signal.signal(signal.SIGALRM,timeout);signal.alarm(240)
start=time.monotonic()
if (out/'INPUT.json').exists():
    inp=json.loads((out/'INPUT.json').read_text());L=snappy.Link(inp['pd'])
else:
    if label.startswith('mixed'):
        ci=int(label[-1]);d=old/'suzuki_mixed'/f'GST3_c{ci}'
        raw=(d/'TAYLOR_INPUT_PD.json').read_bytes();L=snappy.Link(json.loads(raw))
        inp={'pd':L.PD_code(),'missing_unknots':0,'source_file':str(d/'TAYLOR_INPUT_PD.json'),'source_sha256':hashlib.sha256(raw).hexdigest()}
    else:
        inp0=json.loads((old/'suzuki_mixed/GST3_c0/INPUT.json').read_text())
        inp1=json.loads((old/'suzuki_mixed/GST3_c1/INPUT.json').read_text())
        word=inp0['full_cable']['input_braid'];assert word==inp1['full_cable']['input_braid']
        L,meta=parallel(word,[2,2]);random.seed(20260920);L.simplify('global')
        inp={'pd':L.PD_code(),'missing_unknots':4-len(L.link_components),'construction':meta}
    assert all(x==0 for row in L.linking_matrix() for x in row)
    (out/'INPUT.json').write_text(json.dumps(inp,indent=2)+'\n')
def signature(L):return regina.Link.fromPD([[x+1 for x in row] for row in L.PD_code()]).sig(False,True,True)
if (out/'LAYOUT.json').exists():lay=json.loads((out/'LAYOUT.json').read_text())
else:
    if label=='mixed0':
        saved=json.loads((old/'suzuki_mixed/GST3_c0/TAYLOR_INTEGER_SEEDED_RESULT.json').read_text())
        lay={'events':saved['morse_events'],'origin':'saved order6 mixed0 layout'}
    else:
        def cost(e):return (e.width,sum(comb(n,n//2)//(n//2+1) for n in e.frontier_lengths))
        choices=[]
        for seed in (20260920,20260921,20260922,20260923):
            random.seed(seed)
            choices.extend(exhaust.MorseExhaustion(L,c) for c in L.crossings)
        best=min(choices,key=cost)
        lay={'events':best.events,'score':cost(best),'origin':'four seeded rounds, every starting crossing','chosen_index':choices.index(best)}
    encoded=exhaust.MorseEncoding(lay['events'])
    assert signature(L)==signature(encoded.link()),'Morse diagram mismatch'
    width=encoded.width;lay.update(width=width,crossings=len(L.crossings),catalan_max=comb(width,width//2)//(width//2+1),diagram_signature=signature(L),reflection_allowed=False)
    (out/'LAYOUT.json').write_text(json.dumps(lay,indent=2)+'\n')
if layout_only:
    signal.alarm(0);print({k:v for k,v in lay.items() if k not in ('events','diagram_signature')});sys.exit(0)
cap=20000 if label.startswith('mixed') else 210000
encoded=exhaust.MorseEncoding(lay['events']);assert signature(L)==signature(encoded.link())
install();Jet.order=8;jones.R=Ring();jones.q=Jet([1,1]);jones.PerfectMatching=PerfectMatching
value=jones.VElement();peak=1;r={'label':label,'precision':8,'cap':cap,'time_limit_seconds':240,'layout':lay,'input_sha256':hashlib.sha256((out/'INPUT.json').read_bytes()).hexdigest()}
try:
    for i,event in enumerate(encoded):
        if event.kind=='cup':value=value.insert_cup(event.min)
        elif event.kind=='cap':value=value.cap_off(event.min)
        elif event.a<event.b:value=value.add_positive_crossing(event.min)
        else:value=value.add_negative_crossing(event.min)
        value.dict={key:c for key,c in value.dict.items() if c};peak=max(peak,len(value.dict))
        if peak>cap:raise RuntimeError('STATE_CAP_INCONCLUSIVE')
    empty=PerfectMatching([]);assert not(set(value.dict)-{empty})
    signs=[c.sign for c in L.crossings];minus,plus=signs.count(-1),signs.count(1)
    v=jones.q;result=(-1)**minus*v**(plus-2*minus)*value.dict.get(empty,Jet(0))*(v+v**-1)**inp['missing_unknots']
    r.update(status='complete',coefficients_integer=list(result.d))
    if label.startswith('mixed'):
        ci=int(label[-1]);d=old/'suzuki_mixed'/f'GST3_c{ci}'
        filename='TAYLOR_INTEGER_SEEDED_RESULT.json' if ci==0 else 'TAYLOR_INTEGER_RESULT.json'
        prior=json.loads((d/filename).read_text());assert list(result.d[:6])==prior['coefficients_integer'],'Changed known low-order coefficients'
        r['prior_six_coefficients_agree']=True
except Exception as exc:r.update(status='inconclusive',error=repr(exc))
finally:
    signal.alarm(0);r.update(seconds=time.monotonic()-start,max_states=peak,last_event=i)
    path=out/('RESULT.json' if r['status']=='complete' else 'FAILURE.json')
    assert not path.exists(),'Preserve previous attempt';path.write_text(json.dumps(r,indent=2)+'\n')
print({k:v for k,v in r.items() if k!='layout'},flush=True)
