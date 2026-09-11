#!/usr/bin/env python3
"""Run the Dunfield–Gong band search (shipped in SnapPy 3.3, spherogram.links.bands)
on one knot with an explicit parameter box, and record the outcome as a coverage
statement.  Requires SnapPy inside Sage (passagemath works) for the slice filter.

Usage: python3 band_search.py <knot.json> <max_bands> <max_twists> <max_band_len> <paths> <out.json>

A positive result is a certificate (checked with verify_ribbon_to_unknot).
A negative result means only: no ribbon disk inside this parameter box.
"""
import json, sys, time, datetime
import snappy
from spherogram.links.bands.search import ribbon_concordant_links, verify_ribbon_to_unknot

knot_file, max_bands, max_twists, max_band_len, paths, out = sys.argv[1:7]
max_bands, max_twists, max_band_len = int(max_bands), int(max_twists), int(max_band_len)
d = json.load(open(knot_file))
pd = d.get('pd_code_snappy_0indexed') or d['pd_code']
K = snappy.Link([tuple(c) for c in pd])
import snappy.sage_helper as sh
assert sh._within_sage, 'run inside Sage: the slice filter needs it'

t0 = time.time()
res = ribbon_concordant_links(K, max_bands=max_bands, max_twists=max_twists,
                              max_band_len=max_band_len, paths=paths,
                              filter_for_plausibly_slice=True,
                              use_ribbon_link_cache=True, certify=True,
                              print_progress=True)
elapsed = time.time() - t0
record = {
    'knot': d['name'], 'date': datetime.datetime.utcnow().isoformat() + 'Z',
    'box': {'max_bands': max_bands, 'max_twists': max_twists,
            'max_band_len': max_band_len, 'paths': paths,
            'filter_for_plausibly_slice': True, 'use_ribbon_link_cache': True},
    'seconds': round(elapsed, 1),
    'survivor_links': len([k for k in res if k != 'unknot']),
    'unknot_found': 'unknot' in res,
}
if 'unknot' in res:
    cert = res['unknot']
    record['certificate'] = [c if isinstance(c, str) else c for c in cert]
    try:
        record['certificate_verified'] = bool(verify_ribbon_to_unknot(K, cert))
    except Exception as e:
        record['certificate_verified'] = f'error: {e}'
json.dump(record, open(out, 'w'), indent=1, default=str)
print(json.dumps({k: v for k, v in record.items() if k != 'certificate'}, indent=1))
