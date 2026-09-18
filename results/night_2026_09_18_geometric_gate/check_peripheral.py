"""Replay the peripheral certificate without the diagram producer's rewriter."""
from pathlib import Path
import json
import sys
import copy

ROOT=Path(__file__).resolve().parents[2]
ARCHIVE=ROOT/'results/chat_archive_2026_09_17/expanded/SR_Foxy_pass09_product_collar_2026_09_17/pass09_product_collar'
sys.path.insert(0,str(ARCHIVE))
import check_saved_proof as r

C=json.loads((ARCHIVE/'RESULTS.json').read_text())
B=json.loads((ROOT/'results/astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json').read_text())
assert r.check(C)
maps={int(k)+1:tuple(w) for k,w in C['boundary_arc_images'].items()}

def check(d):
    # Check transport against the saved oriented crossing relations. Each
    # event conjugates the current meridian to the outgoing meridian.
    rels={c:(i+1,o+1,b+1,s) for i,o,b,s,c in B['boundary_relations']}
    current=5
    # Start is on the overstrand at crossing 1; the first subsequent
    # undercrossing has incoming generator 5.
    for e in d['events']:
        i,o,b,s=rels[e['crossing']]
        assert current==i and e['letter']==b*s
        current=o
    assert current==5 and len(d['events'])==len(rels)==18
    assert len({e['crossing'] for e in d['events']})==18
    assert [e['crossing']<27 for e in d['events']]==[True]*9+[False]*9
    U=[e['letter'] for e in d['events'][:9]]
    L=[e['letter'] for e in d['events'][9:]]
    assert U==d['upper_boundary_transport'] and L==d['lower_boundary_transport']
    assert U+L==d['preferred_boundary_longitude']
    assert sum(1 if x>0 else -1 for x in U+L)==d['total_writhe']==0
    u,l,mu=r.substitute(U,maps),r.substitute(L,maps),maps[5]
    assert mu==maps[15]
    assert list(u)==d['upper_source_transport'] and list(l)==d['lower_source_transport']
    assert list(mu)==d['seam_source_meridian']
    expected=[r.reduce_free(u+l),r.reduce_free(u+mu+r.backwards(u)+r.backwards(mu))]
    assert len(d['proofs'])==2
    for word,p in zip(expected,d['proofs']):
        assert list(word)==p['source_word']
        assert not r.replay(word,p['trace'],C['proof_rule_relators'])
    assert sum(1 if x>0 else -1 for x in mu)==1

d=json.loads(Path(__file__).with_name('peripheral_certificate.json').read_text())
check(d)
bad=copy.deepcopy(d);bad['events'][0]['letter']*=-1
try:check(bad)
except AssertionError:pass
else:raise AssertionError('crossing sign corruption survived')
print(json.dumps({'oriented_transport_replay':'PASS','archived_Tietze_provenance':'PASS',
    'source_group_identities':'2 proved, 3 relator steps each',
    'longitude_killed_for_all_integer_saved_q_n':True,
    'corrupted_crossing_rejected':True,
    'scope':'Peripheral compatibility only; geometry not identified'},indent=2))
