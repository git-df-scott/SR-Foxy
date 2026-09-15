#!/usr/bin/env python3
"""Teichner certificate: K is smoothly slice iff some ribbon J makes K # J ribbon.

The two required ribbon certificates are for J and K # J. Their existence
implies smooth sliceness of K. This supplies no non-ribbonness certificate,
and gives no conclusion that K must or must not be handle-ribbon. Verification
here replays Spherogram certificates with that same library; it is not an
independent formal proof checker.

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
# This is a search preference. Fiberedness alone is insufficient to apply
# Miyazaki's theorem: its hypotheses on every prime summand must be checked.
# Arbitrary names supplied through TEICHNER_J are checked below, not trusted.
RIBBON_J = ['6_1', '8_8', '9_41', '10_3', '10_22', '10_87']
import os
if os.environ.get('TEICHNER_J'):
    RIBBON_J = os.environ['TEICHNER_J'].split(',')

# Two dials that every Teichner run in this repository has left at their
# defaults. They are independent of max_bands and max_band_len.
#
#   TEICHNER_TWISTS  max_twists on each band (default 2, as hardcoded before).
#   TEICHNER_PATHS   'shortest' (min_len_bands, the default everywhere so far)
#                    or 'simple' (simple_bands), a strictly larger band set:
#                    spherogram's own doctest gives 393 simple bands on L5a1
#                    against the smaller shortest-path set.
#
# Widening either is a different search, not a longer one, so a negative
# result under 'shortest' says nothing about 'simple'.
MAX_TWISTS = int(os.environ.get('TEICHNER_TWISTS', 2))
PATHS = os.environ.get('TEICHNER_PATHS', 'shortest')
if PATHS not in ('shortest', 'simple'):
    raise SystemExit("TEICHNER_PATHS must be 'shortest' or 'simple'")

def connected_sum(pd_a, pd_b):
    """PD code of the connected sum, by relabelling B's arcs above A's."""
    A = snappy.Link([tuple(c) for c in pd_a])
    B = snappy.Link([tuple(c) for c in pd_b])
    return A.connected_sum(B)

def certificate_status(link, result):
    """A discovered endpoint alone must never set the certificate flag."""
    if 'unknot' not in result:
        return False
    return bool(verify_ribbon_to_unknot(link, result['unknot']))

if __name__ == '__main__':
    out, max_bands, max_band_len = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    rec = {'date': datetime.datetime.utcnow().isoformat() + 'Z',
           'box': {'max_bands': max_bands, 'max_band_len': max_band_len,
                   'max_twists': MAX_TWISTS, 'paths': PATHS, 'J_list': RIBBON_J},
           'runs': [],
           'meaning': 'a verified certificate proves K smoothly slice with a disk NOT known handle-ribbon; '
                      'then run homotopy-ribbon obstructions on K'}
    t0 = time.time()
    partner_certificates = {}
    for f in sys.argv[4:]:
        d = json.load(open(f)); pd = d.get('pd_code_snappy_0indexed') or d['pd_code']
        K = snappy.Link([tuple(c) for c in pd])
        for jname in RIBBON_J:
            J = snappy.Link(jname)
            if jname not in partner_certificates:
                partner_result = ribbon_concordant_links(
                    J, max_bands=max_bands, max_twists=MAX_TWISTS,
                    max_band_len=max_band_len, paths=PATHS, certify=True)
                partner_certificates[jname] = {
                    'verified': certificate_status(J, partner_result),
                    'certificate': partner_result.get('unknot'),
                    'pd_code': J.PD_code()}
            partner = partner_certificates[jname]
            S = K.connected_sum(J); S.simplify('global')
            # Heartbeat: record that this pair was STARTED, with its box, before
            # the long call. A `timeout` kill during the search otherwise leaves
            # no trace at all, because a row is only appended once the search for
            # that partner returns. Overwritten by the real row on completion.
            rec['in_progress'] = {'knot': d['name'], 'J': jname,
                                  'sum_crossings': len(S.crossings),
                                  'started': datetime.datetime.now(
                                      datetime.timezone.utc).isoformat(),
                                  'partner_ribbon_verified': partner['verified']}
            json.dump(rec, open(out, 'w'), indent=1, default=str)
            t = time.time()
            res = ribbon_concordant_links(S, max_bands=max_bands,
                                          max_twists=MAX_TWISTS,
                                          max_band_len=max_band_len,
                                          paths=PATHS, certify=True)
            row = {'knot': d['name'], 'J': jname, 'sum_crossings': len(S.crossings),
                   'seconds': round(time.time() - t, 1), 'certified_slice': False,
                   'partner_ribbon_verified': partner['verified'],
                   'partner_certificate': partner['certificate'],
                   'partner_pd_code': partner['pd_code'], 'sum_pd_code': S.PD_code()}
            # Save the actual frontier, not only its size. Each value is the
            # replayable triple [starting PD code, band descriptor, endpoint
            # name] that spherogram returns, so a later session can rebuild any
            # surviving intermediate without re-running the search.
            row['frontier_size'] = len(res)
            # A list, not a dict keyed by str(link): spherogram's Link repr
            # ('<Link: 3 comp; 11 cross>') is not unique, so keying on it
            # silently drops distinct frontier links.
            row['frontier'] = [{'label': str(k), 'certificate': v}
                               for k, v in res.items()]
            if 'unknot' in res:
                row['certificate_verified'] = certificate_status(S, res)
                row['certified_slice'] = row['certificate_verified'] and partner['verified']
                row['certificate'] = res['unknot']
                if row['certified_slice']:
                    print('*** TEICHNER CERTIFICATE ***', d['name'], '#', jname, flush=True)
            rec['runs'].append(row)
            rec.pop('in_progress', None)
            rec['seconds'] = round(time.time() - t0, 1)
            json.dump(rec, open(out, 'w'), indent=1, default=str)
            print(json.dumps({k: v for k, v in row.items()
                              if k not in ('certificate', 'frontier')}), flush=True)
    print('CERTIFIED:', sum(1 for r in rec['runs'] if r['certified_slice']))
