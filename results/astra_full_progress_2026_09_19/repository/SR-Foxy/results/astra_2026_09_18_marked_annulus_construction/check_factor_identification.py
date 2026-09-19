"""Integer-only replay of the D01 cut and final positive gluing map.

Upstream PD triangulation/retriangulation and peripheral homology remain
kernel-trusted. This does not use a numerical geometric signature.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from check_saved import adjacency

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('previous_checker',ROOT/'results/night_2026_09_18_positive_identification/check_certificate.py')
previous=importlib.util.module_from_spec(spec);spec.loader.exec_module(previous)

def main():
    folder=HERE/'factor_identification'
    d=json.loads((folder/'certificate.json').read_text())
    cards=[]
    for item in d['inputs']:
        path=ROOT/item['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256']
        cards.append(json.loads(path.read_text()))
    A=adjacency(cards[0]['pd_code'])
    actual={tuple(x):tuple(y) for x,y in d['cut_edges']}
    assert actual=={x:y for x,y in A.items() if x[0]<6<=y[0]}
    assert len(actual)==2
    # Independently replay all face walks and identify the dual bigon.
    seen=set();face_of={}
    for i,cycle in enumerate(d['faces']):
        for raw,nxt in zip(cycle,cycle[1:]+cycle[:1]):
            x=tuple(raw);assert x not in seen;seen.add(x);face_of[x]=i
            assert A[x[0],(x[1]+1)%4]==tuple(nxt)
    assert seen==set(A)
    incident=[sorted([face_of[(x[0],(x[1]-1)%4)],face_of[x]]) for x in actual]
    assert incident==d['cut_incident_faces'] and incident[0]==incident[1]
    assert len(set(incident[0]))==2
    for lo,hi,f in [(0,6,d['factors'][0]),(6,25,d['factors'][1])]:
        B=adjacency(f['pd_code']);ports=[tuple(x) for x in f['cut_ports']]
        assert set(ports)=={x for x,y in A.items() if lo<=x[0]<hi and not lo<=y[0]<hi}
        for x,y in B.items():
            old=(x[0]+lo,x[1]);expected=A[old]
            if old in ports:expected=ports[1-ports.index(old)]
            assert (y[0]+lo,y[1])==expected
    assert adjacency(d['factors'][0]['pd_code'])==adjacency(cards[1]['pd_code'])
    for stage in d['stages']:
        assert hashlib.sha256((folder/stage['file']).read_bytes()).hexdigest()==stage['sha256']
    c=d['case']
    for label,name in [('source','factor_retriangulated'),('target','mirror_K1_retriangulated')]:
        gluings,cusps=previous.read_saved_gluings(folder/(name+'.tri'))
        assert gluings==c[label+'_gluings'] and cusps==c[label+'_cusps']
    checks=previous.check_case(c)
    bad=copy.deepcopy(c);p=bad['orientation_preserving_simplex_map'][0]['vertices']
    p[0],p[1],p[2]=p[1],p[2],p[0]
    try:previous.check_case(bad)
    except AssertionError:pass
    else:raise AssertionError('wrong even simplex map accepted')
    print(json.dumps({'D01_dual_bigon_and_factor_reconnections':'PASS',
                      'K0_factor_exact_port_graph':'PASS','mirror_K1_factor_positive_gluing_map':'PASS',
                      'directed_face_checks':checks,'negative_controls_rejected':1,
                      'scope':'Unoriented prime factor identification; upstream triangulation and peripheral matrices remain kernel-trusted'},indent=2))

if __name__=='__main__':main()
