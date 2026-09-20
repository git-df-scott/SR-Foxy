from pathlib import Path
import sys,json
p=Path(__file__).resolve().parent;old=p.parent/'astra_gst_five_hour_2026_09_19'
sys.path[:0]=[str(old),str(p.parents[1]/'scripts')]
from compact_taylor import *
from sagefree_jones import PerfectMatching,install
from suzuki_taylor_order8 import Jet,Ring
from spherogram.links import jones
install();Jet.order=8;jones.R=Ring();jones.q=Jet([1,1]);jones.PerfectMatching=PerfectMatching
def nc(n):
    if n==0:yield [];return
    for j in range(1,n,2):
        for left in nc(j-1):
            for right in nc(n-j-1):yield [(0,j)]+[(a+1,b+1) for a,b in left]+[(a+j+1,b+j+1) for a,b in right]
def key(m):return bytes(m.partner(i) for i in range(2*len(m)))
def asdict(v):return {key(m):c.d for m,c in v.dict.items() if c}
checks=0
for n in range(0,11,2):
    for pairs in nc(n):
        pm=PerfectMatching(pairs);k=key(pm);v=jones.VElement({pm:Jet([2,-1,3,0,5,-2,0,7])});s={k:tuple([2,-1,3,0,5,-2,0,7])}
        for i in range(n+1):
            assert step(s,('cup',i,i+1))==asdict(v.insert_cup(i));checks+=1
        for i in range(n-1):
            for event,want in [(('cap',i,i+1),v.cap_off(i)),(('cross',i,i+1),v.add_positive_crossing(i)),(('cross',i+1,i),v.add_negative_crossing(i))]:
                assert step(s,event)==asdict(want);checks+=1
traces=[]
for label in ['GST1','GST2','L10n36','L10n57']:
    d=old/'suzuki_double'/label;i=json.loads((d/'INPUT.json').read_text());r=json.loads((d/'RESULT.json').read_text())
    got=probe(i['simplified_pd'],r['morse_events'],missing=0,seconds=60)
    assert list(got['coefficients_integer'])==r['coefficients_integer'],label
    traces.append({'label':label,'agrees':True,'max_states':got['max_states']})
for label in ['mixed0','mixed1']:
    d=p/'gst3_order8'/label;i=json.loads((d/'INPUT.json').read_text());r=json.loads((d/'RESULT.json').read_text())
    got=probe(i['pd'],r['layout']['events'],missing=i['missing_unknots'],seconds=60)
    assert list(got['coefficients_integer'])==r['coefficients_integer'],label
    traces.append({'label':'GST3 '+label,'agrees':True,'max_states':got['max_states']})
out={'exact_state_transition_checks':checks,'max_frontier_for_transition_checks':10,'trace_controls':traces,'scope':'Independent comparison with Spherogram operators and six saved ordinary TL contractions; all eight coefficients.'}
(p/'COMPACT_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
