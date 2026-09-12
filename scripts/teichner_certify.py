#!/usr/bin/env python3
"""Teichner certificate: K is smoothly slice iff some ribbon J makes K # J ribbon.

Why this generator matters (see STRATEGY_2026-09-11.md).  Every other route-A
generator builds K's slice disk from the exterior of a *ribbon* disk of a partner
knot, so K comes out handle-ribbon by construction and every classical obstruction
is logically inert.  The Teichner disk instead runs a ribbon disk backwards inside a
concordance, so it carries local maxima and its exterior needs 3-handles: the output
is NOT known handle-ribbon, NOT known homotopy-ribbon.  Against such a K the whole
homotopy-ribbon battery is live again, and a K that is Teichner-certified slice and
fails a homotopy-ribbon obstruction is a counterexample to Slice-Ribbon.

Usage: teichner_certify.py <out.json> <max_bands> <max_band_len> <knot.json>...
Connect-sums each input K with each small ribbon J and runs the Dunfield-Gong band
search on K # J.  Writes incrementally.
"""
import json, sys, time, datetime
import snappy
from spherogram.links.bands.search import ribbon_concordant_links, verify_ribbon_to_unknot
import snappy.sage_helper as sh
assert sh._within_sage, 'needs SnapPy inside Sage'

# spherogram's slice filter calls Link.signature(), whose white_graph() raises
# ValueError('The link diagram is split.') on split intermediate links.  Connected
# sums hit this where a single knot does not.  Patch conservatively: on failure keep
# the link in the search (returning True can only slow the search, never lose a disk).
import spherogram.links.bands.search as _bs
_orig_filter = _bs.could_be_strongly_slice
def _safe_filter(link):
    try:
        return _orig_filter(link)
    except ValueError:
        return True
_bs.could_be_strongly_slice = _safe_filter

# Small ribbon knots.  The default list is deliberately restricted to the NON-FIBERED
# ones (verified here: 6_1 g1, 8_8 g2, 9_41 g2, 10_3 g1, 10_22 g3, 10_87 g3 are all
# non-fibered; 8_9, 8_20, 9_27, 10_99 are fibered and excluded).
#
# Why.  For a target of Miyazaki type -- D_{n,m} = K_n # (-K_m) with K_n, K_m prime
# fibered, non-isotopic, sharing an irreducible Alexander polynomial -- a FIBERED
# prime ribbon partner J makes D # J a connected sum of prime fibered knots, and
# Miyazaki's Thm 5.5 (via Abe-Tagami Cor 4.3) then forces the summands to pair by
# mirror/reversal.  K_n could only pair with -K_n, but K_n is not isotopic to K_m, so
# D # J is not homotopy-ribbon, hence not ribbon.  Fibered partners are therefore
# provably futile and are excluded from the search rather than wasted on.
RIBBON_J = ['6_1', '8_8', '9_41', '10_3', '10_22', '10_87']
import os
if os.environ.get('TEICHNER_J'):
    RIBBON_J = os.environ['TEICHNER_J'].split(',')

def connected_sum(pd_a, pd_b):
    """PD code of the connected sum, by relabelling B's arcs above A's."""
    A = snappy.Link([tuple(c) for c in pd_a])
    B = snappy.Link([tuple(c) for c in pd_b])
    return A.connected_sum(B)

if __name__ == '__main__':
    out, max_bands, max_band_len = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    rec = {'date': datetime.datetime.utcnow().isoformat() + 'Z',
           'box': {'max_bands': max_bands, 'max_band_len': max_band_len, 'J_list': RIBBON_J},
           'runs': [],
           'meaning': 'a verified certificate proves K smoothly slice with a disk NOT known handle-ribbon; '
                      'then run homotopy-ribbon obstructions on K'}
    t0 = time.time()
    for f in sys.argv[4:]:
        d = json.load(open(f)); pd = d.get('pd_code_snappy_0indexed') or d['pd_code']
        K = snappy.Link([tuple(c) for c in pd])
        for jname in RIBBON_J:
            J = snappy.Link(jname)
            S = K.connected_sum(J); S.simplify('global')
            t = time.time()
            res = ribbon_concordant_links(S, max_bands=max_bands, max_twists=2,
                                          max_band_len=max_band_len, certify=True)
            row = {'knot': d['name'], 'J': jname, 'sum_crossings': len(S.crossings),
                   'seconds': round(time.time() - t, 1), 'certified_slice': 'unknot' in res}
            if 'unknot' in res:
                row['certificate_verified'] = bool(verify_ribbon_to_unknot(S, res['unknot']))
                row['certificate'] = res['unknot']
                print('*** TEICHNER CERTIFICATE ***', d['name'], '#', jname, flush=True)
            rec['runs'].append(row)
            rec['seconds'] = round(time.time() - t0, 1)
            json.dump(rec, open(out, 'w'), indent=1, default=str)
            print(json.dumps({k: v for k, v in row.items() if k != 'certificate'}), flush=True)
    print('CERTIFIED:', sum(1 for r in rec['runs'] if r['certified_slice']))
