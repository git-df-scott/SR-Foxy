"""Exact peripheral test for every saved partial-conjugation collar q_n."""
from pathlib import Path
import json
import resource
import sys

resource.setrlimit(resource.RLIMIT_CPU, (30,35))
ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT/'results/chat_archive_2026_09_17/expanded/SR_Foxy_pass09_product_collar_2026_09_17/pass09_product_collar'
sys.path.insert(0,str(ARCHIVE))
import diagram_core as g
import verify_product_collar as v
import check_saved_proof as replay

C = json.loads((ARCHIVE/'RESULTS.json').read_text())
assert replay.check(C)
A = g.adjacency_from_pd(g.SCAFFOLD)
q = g.quotient_R_wirtinger(A)
col = {int(k)+1:tuple(w) for k,w in C['boundary_arc_images'].items()}
cur = start = (1,1)
assert cur in q['incoming'] and q['arcs'][cur]+1 == 5
seen = set()
events = []
while cur not in seen:
    seen.add(cur)
    c,p = cur
    assert cur in q['incoming']
    if p in (0,2) and q['cmap'][c,1] == 0:
        events.append({'crossing':c,'port':p,'letter':(q['arcs'][c,1]+1)*q['signs'][c]})
    cur = A[c][(p+2)%4]
assert cur == start
assert len(events) == len(q['relations']) == 18
assert [e['crossing']<27 for e in events] == [True]*9+[False]*9
upper = [e['letter'] for e in events[:9]]
lower = [e['letter'] for e in events[9:]]
exp = lambda w:sum(1 if x>0 else -1 for x in w)
assert exp(upper) == -1 and exp(lower) == 1
u,l = v.subst(upper,col),v.subst(lower,col)
mu = col[5]
assert mu == col[15]
rules = [tuple(w) for w in C['proof_rule_relators']]
checks = []
for name,word in [('longitude',v.mul(u,l)),
                  ('upper_transport_centralizes_seam_meridian',v.mul(u,mu,v.inv(u),v.inv(mu)))]:
    end,trace = v.reduce_proven(word,rules)
    assert end == () and replay.replay(word,trace,rules) == ()
    checks.append({'claim':name,'source_word':word,'trace':trace,'residue':end})
bad = v.mul(u,l,mu)
assert exp(bad) == 1
print(json.dumps({'scope':'Necessary peripheral condition; not a geometric identification',
    'seam_start':start,'boundary_meridian':5,'events':events,
    'upper_boundary_transport':upper,'lower_boundary_transport':lower,
    'preferred_boundary_longitude':upper+lower,'total_writhe':0,
    'upper_source_transport':u,'lower_source_transport':l,'seam_source_meridian':mu,
    'proofs':checks,'all_integer_n_argument':'u l=1 and [u,mu]=1 imply u mu^n l mu^-n=1',
    'negative_control_longitude_times_meridian_exponent':exp(bad)},indent=2))
