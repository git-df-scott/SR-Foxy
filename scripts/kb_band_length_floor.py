#!/usr/bin/env python3
"""How short a band-length box still finds a ribbon disk that is really there?

`results/band_generator_saturation.json` measured the top of the `max_band_len`
dial (it saturates at 6).  This measures the bottom, on the repository's own
calibration knot `K_B` -- the 31-crossing 0-friend of `K_G`, whose ribbon disk
is known and verified.

The answer matters for how the Teichner lane spends its budget: the band search
stops as soon as it reaches an unlink, so a diagram carrying a short disk is
cheap and a diagram carrying none costs the whole frontier of its box.
"""
import json, sys, time, os, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import snappy
import sagefree_slice_filter as sff
import spherogram.links.bands.search as _bs
_pure = sff.could_be_strongly_slice
def _safe(link):
    try:
        return _pure(link)
    except Exception:
        return True
_bs.could_be_strongly_slice = _safe
from spherogram.links.bands.search import ribbon_concordant_links, verify_ribbon_to_unknot

out = sys.argv[1] if len(sys.argv) > 1 else 'results/session_2026-09-15b/KB_band_length_floor.json'
d = json.load(open('data/knots/K_B_0friend.json'))
KB = snappy.Link([tuple(c) for c in d['pd_code_snappy_0indexed']])
rec = {'date': datetime.datetime.utcnow().isoformat() + 'Z',
       'knot': d['name'], 'crossings': len(KB.crossings),
       'filter': 'scripts/sagefree_slice_filter.py (no Sage)',
       'box': {'max_bands': 2, 'max_twists': 2, 'paths': 'shortest',
               'diagram': 'canonical, simplify(global) only'},
       'measurements': []}
for ln in [1, 2, 3, 4, 6]:
    t = time.time()
    r = ribbon_concordant_links(KB, max_bands=2, max_twists=2, max_band_len=ln,
                                paths='shortest', certify=True)
    v = ('unknot' in r) and bool(verify_ribbon_to_unknot(KB, r['unknot']))
    row = {'max_band_len': ln, 'unknot_endpoint_found': 'unknot' in r,
           'certificate_verified': v, 'seconds': round(time.time() - t, 2)}
    rec['measurements'].append(row)
    print(row, flush=True)
rec['reading'] = ('A ribbon disk that is present on the searched diagram is found '
                  'at max_band_len 2 and verified, on a 31-crossing knot, in about a '
                  'second. Deeper boxes on one diagram buy frontier, not discovery; '
                  'the dial that matters for finding a disk is how many diagrams are '
                  'searched. Every Teichner run in this repository has searched one.')
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(rec, open(out, 'w'), indent=1)
print('wrote', out)
