#!/usr/bin/env python3
"""Band search over many randomly perturbed ("shaken") diagrams of one knot,
following the Dunfield–Gong practice of searching several diagrams because the
band moves available depend on the diagram.

Usage: python3 band_search_shaken.py <knot.json> <n_diagrams> <backtrack_steps> <max_bands> <max_twists> <max_band_len> <paths> <out.json> [seed]
"""
import json, sys, time, random, datetime
import snappy
from spherogram.links.bands.search import ribbon_concordant_links, verify_ribbon_to_unknot
import snappy.sage_helper as sh
assert sh._within_sage

knot_file, n_diag, steps, max_bands, max_twists, max_band_len, paths, out = sys.argv[1:9]
seed = int(sys.argv[9]) if len(sys.argv) > 9 else 0
n_diag, steps, max_bands, max_twists, max_band_len = map(int, (n_diag, steps, max_bands, max_twists, max_band_len))
random.seed(seed)
d = json.load(open(knot_file))
pd = d.get('pd_code_snappy_0indexed') or d['pd_code']
K0 = snappy.Link([tuple(c) for c in pd])

runs = []
t0 = time.time()
found = None
for i in range(n_diag):
    K = K0.copy()
    if i > 0:
        K.backtrack(steps)
        # partially simplify so diagrams stay small but differ
        K.simplify('basic')
    t = time.time()
    res = ribbon_concordant_links(K, max_bands=max_bands, max_twists=max_twists,
                                  max_band_len=max_band_len, paths=paths,
                                  filter_for_plausibly_slice=True,
                                  use_ribbon_link_cache=True, certify=True)
    rec = {'diagram': i, 'crossings': len(K.crossings), 'seconds': round(time.time() - t, 1),
           'survivors': len([k for k in res if k != 'unknot']), 'unknot': 'unknot' in res}
    if 'unknot' in res:
        cert = res['unknot']
        rec['certificate'] = cert
        rec['certificate_verified'] = bool(verify_ribbon_to_unknot(K, cert))
        rec['start_pd'] = K.PD_code()
        found = rec
    runs.append(rec)
    print(json.dumps({k: v for k, v in rec.items() if k not in ('certificate', 'start_pd')}), flush=True)
    json.dump({'knot': d['name'], 'date': datetime.datetime.utcnow().isoformat() + 'Z',
               'box': {'n_diagrams': n_diag, 'backtrack_steps': steps, 'max_bands': max_bands,
                       'max_twists': max_twists, 'max_band_len': max_band_len, 'paths': paths, 'seed': seed},
               'seconds': round(time.time() - t0, 1), 'runs': runs, 'unknot_found': found is not None},
              open(out, 'w'), indent=1, default=str)
    if found:
        break
print('DONE unknot_found =', found is not None)
