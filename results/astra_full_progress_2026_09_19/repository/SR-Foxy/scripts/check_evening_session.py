#!/usr/bin/env python3
"""Replay this session's retained geometry and recompute logged invariants."""
from collections import Counter
import json,hashlib,subprocess
from pathlib import Path
import snappy
from spherogram.links.bands.core import add_one_band
from colored_link_rank import check
from component_guided_bands import inspect,jones
from returning_fission_search import noninterleaving
from odd_khovanov_gate import parse_odd,unreduced,JAVA,JAR
from khovanov_upper_filter import euler_check,deficits
from fusion_successors import diagram_signature

counts=Counter();sources={}
for name,card in [('K0','AbeTagami_K_0_K_-1__6_3'),('K1','AbeTagami_K_1')]:
    sources[name]=snappy.Link(json.loads(Path('data/knots/'+card+'.json').read_text())['pd_code_snappy_0indexed'])
for file in ['results/returning_fission_K0_to_K1.json','results/returning_fission_K1_to_K0.json']:
    D=json.loads(Path(file).read_text());assert D['complete']
    for r in D['runs']:
        assert r['complete'];J=snappy.Link(r['start_pd'])
        for c in r['retained']:
            L=add_one_band(J,c['band']);assert L.PD_code()==[tuple(x) for x in c['raw_pd']]
            assert L.is_planar() and len(L.link_components)==2 and L.linking_number()==0
            for face in c['path_metadata']['face_chord_certificate']:
                assert noninterleaving(face['boundary'],face['chords'])
            got=inspect(snappy.Link(c['raw_pd']),jones(sources[D['parameters']['wanted']]),True)
            got=json.loads(json.dumps(got))  # JSON stores PD tuples as lists.
            assert all(got[k]==c[k] for k in got if k not in ['link_pd','component_pd'])
            assert diagram_signature(got['link_pd'])==diagram_signature(c['link_pd'])
            assert [diagram_signature(p) if p else 'U' for p in got['component_pd']]==[diagram_signature(p) if p else 'U' for p in c['component_pd']]
            L.simplify('basic')
            for old in c['rank_checks']:assert check(L,old['component_values'],old['prime'])==old
            counts['retained_band_replays']+=1
        counts['search_bands']+=r['counts']['bands'];counts['rank_rejections']+=r['counts']['link_concordance_obstructed']
        counts['wanted_matches']+=len(r['wanted_matches']);counts['source_returns']+=len(r['source_controls'])
D=json.loads(Path('results/odd_khovanov_Q/manifest.json').read_text());assert D['complete'];odd={}
for row in D['runs']:
    r=unreduced(parse_odd(Path('results/odd_khovanov_Q/'+row['name']+'.log').read_text()))
    assert sorted([[i,j,n] for (i,j),n in r.items()])==row['unreduced_ranks']
    assert euler_check(row['pd'],r)['passed'];odd[row['name']]=r;counts['odd_logs_euler_checked']+=1
    if 'K1_deficits' in row:assert deficits(odd['K1'],r)==row['K1_deficits']
    if 'K0_deficits' in row:assert not deficits(odd['K0'],r)
# A reflected diagram reverses both homological and quantum gradings.
mirror=sources['K1'].mirror();file=Path('results/odd_khovanov_Q/mirror_K1.txt')
file.write_text('mirror_K1 = PD['+','.join('X['+','.join(str(a+1) for a in c)+']' for c in mirror.PD_code())+']\n')
job=subprocess.run([str(JAVA),'-Xmx2g','-Djava.awt.headless=true','-jar',str(JAR),str(file),'-ko1','-nf'],capture_output=True,text=True,timeout=60,check=True)
file.with_suffix('.log').write_text(job.stdout+job.stderr);m=unreduced(parse_odd(job.stdout))
assert m==Counter({(-i,-j):n for (i,j),n in odd['K1'].items()});assert euler_check(mirror.PD_code(),m)['passed']
counts['odd_mirror_check']=1
A=json.loads(Path('results/component_link_concordance_independent.json').read_text());assert A['complete'] and len(A['rows'])==1092
counts['independently_group_checked_links']=len(A['rows'])
rec={'status':'PASSED','counts':dict(counts),'limitations':'Finite search; same-library ribbon/PD replay, independent triangulation Fox presentation and integer determinant checks. Jones Euler and mirror controls do not formally verify the Khovanov implementation. No counterexample.'}
Path('results/evening_session_validation.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(counts),flush=True)
