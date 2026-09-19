#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
import snappy
from spherogram.links.bands.core import add_one_band
from colored_link_rank import check
R=json.loads(Path('results/teichner_live_frontier.json').read_text());summary={}
for j in ['941','946']:
    p=Path('results/teichner_D01_J'+j+'_third_band.json');D=json.loads(p.read_text());assert D['complete'] and not D['certified_slice'];paths=[r['certificate_prefix'] for r in R['partners'][j]['live_frontier'] if r['depth']==2]
    for r in D['frontier']:
        assert r['depth']==3 and r['certificate_prefix'][:-2] in paths
        assert r['certificate_prefix'][-3]==r['start_pd']
        L=add_one_band(snappy.Link(r['start_pd']),r['band']);assert L.PD_code()==[tuple(c) for c in r['raw_pd']];assert L.is_planar()
        for c in r['rank_checks']:assert check(L,c['component_values'],c['prime'])==c
    summary[j]={'bands':D['counts']['bands'],'saved_paths_replayed':len(D['frontier']),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
Path('results/teichner_third_band_validation.json').write_text(json.dumps({'status':'PASSED','summary':summary,'scope':'Exact raw replay and rank checks; same-library simplification and certificate machinery. Finite search, no counterexample.'},indent=2)+'\n');print(json.dumps(summary),flush=True)
