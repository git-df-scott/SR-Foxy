#!/usr/bin/env python3
"""Teichner certificate search, with the Sage-only slice filter replaced.

Identical in intent to `scripts/teichner_certify.py`: connect-sum K with each
small NON-FIBERED ribbon J and run the Dunfield-Gong band search on K # J.  A
verified certificate for K # J, together with a verified certificate for J,
proves K smoothly slice.  It proves nothing about K being ribbon.

The one difference: `spherogram.links.bands.search.could_be_strongly_slice`
requires SnapPy inside Sage, which this container does not have.  It is
replaced by `scripts/sagefree_slice_filter.py`, whose every test is a
necessary condition for strong sliceness, so the replacement can only keep
MORE links in the search than the original -- never fewer.  A negative from
this script is therefore still coverage of its box; a positive still has to be
replayed by `verify_ribbon_to_unknot`, which needs no Sage.

Dials, all via environment, same names as the Sage version:
  TEICHNER_J       comma-separated partner list   (default: non-fibered <= 10cr)
  TEICHNER_TWISTS  max_twists                      (default 2)
  TEICHNER_PATHS   'shortest' | 'simple'           (default shortest)
  TEICHNER_SEED    integer; shakes the diagram first (default: canonical)

Usage: teichner_certify_nosage.py <out.json> <max_bands> <max_band_len> <knot.json>...
"""
import json, sys, time, datetime, os, random
import snappy
from spherogram.links.bands.search import ribbon_concordant_links, verify_ribbon_to_unknot

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sagefree_slice_filter as sff

import spherogram.links.bands.search as _bs
_pure = sff.could_be_strongly_slice
def _safe_filter(link):
    """Keep the link whenever the filter cannot decide.  Never lose a disk."""
    try:
        return _pure(link)
    except Exception:
        return True
_bs.could_be_strongly_slice = _safe_filter

RIBBON_J = ['6_1', '8_8', '9_41', '10_3', '10_22', '10_87']
if os.environ.get('TEICHNER_J'):
    RIBBON_J = os.environ['TEICHNER_J'].split(',')
SEED = os.environ.get('TEICHNER_SEED')
SEED = int(SEED) if SEED not in (None, '') else None
MAX_TWISTS = int(os.environ.get('TEICHNER_TWISTS', 2))
PATHS = os.environ.get('TEICHNER_PATHS', 'shortest')
if PATHS not in ('shortest', 'simple'):
    raise SystemExit("TEICHNER_PATHS must be 'shortest' or 'simple'")


def certificate_status(link, result):
    if 'unknot' not in result:
        return False
    return bool(verify_ribbon_to_unknot(link, result['unknot']))


def flush(rec, out):
    with open(out, 'w') as fh:
        json.dump(rec, fh, indent=1)


if __name__ == '__main__':
    out, max_bands, max_band_len = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    rec = {'date': datetime.datetime.utcnow().isoformat() + 'Z',
           'filter': 'sagefree_slice_filter (linking numbers, Seifert signature, '
                     'Fox-Milnor on knots, per-component slice tests); weaker than '
                     "spherogram's Sage filter, so coverage is valid and no disk can be lost",
           'box': {'max_bands': max_bands, 'max_band_len': max_band_len,
                   'max_twists': MAX_TWISTS, 'paths': PATHS, 'seed': SEED,
                   'J_list': RIBBON_J},
           'runs': [],
           'meaning': 'a verified certificate proves K smoothly slice; it gives no '
                      'conclusion about K being ribbon or handle-ribbon'}
    t0 = time.time()
    partner_certificates = {}
    for f in sys.argv[4:]:
        d = json.load(open(f))
        pd = d.get('pd_code_snappy_0indexed') or d['pd_code']
        K = snappy.Link([tuple(c) for c in pd])
        for jname in RIBBON_J:
            J = snappy.Link(jname)
            if jname not in partner_certificates:
                pr = ribbon_concordant_links(J, max_bands=max_bands,
                                             max_twists=MAX_TWISTS,
                                             max_band_len=max_band_len,
                                             paths=PATHS, certify=True)
                partner_certificates[jname] = {
                    'verified': certificate_status(J, pr),
                    'certificate': pr.get('unknot'),
                    'pd_code': J.PD_code()}
                print(f'[{time.time()-t0:8.1f}s] partner {jname} verified='
                      f'{partner_certificates[jname]["verified"]}', flush=True)
            partner = partner_certificates[jname]
            S = K.connected_sum(J)
            S.simplify('global')
            if SEED is not None:
                random.seed(SEED)
                S.backtrack(steps=25)
                S.simplify('global')
            rec['in_progress'] = {'knot': d['name'], 'J': jname,
                                  'sum_crossings': len(S.crossings),
                                  'started': datetime.datetime.utcnow().isoformat() + 'Z'}
            flush(rec, out)
            print(f'[{time.time()-t0:8.1f}s] START {d["name"]} # {jname}  '
                  f'{len(S.crossings)} crossings  box={rec["box"]}', flush=True)
            ts = time.time()
            res = ribbon_concordant_links(S, max_bands=max_bands,
                                          max_twists=MAX_TWISTS,
                                          max_band_len=max_band_len,
                                          paths=PATHS, certify=True)
            ok = certificate_status(S, res)
            row = {'knot': d['name'], 'J': jname,
                   'sum_crossings': len(S.crossings),
                   'sum_pd': [list(c) for c in S.PD_code()],
                   'partner_certificate_verified': partner['verified'],
                   'endpoints': sorted(res.keys()),
                   'unknot_endpoint_found': 'unknot' in res,
                   'certificate_verified': ok,
                   'certificate': res.get('unknot') if ok else None,
                   'seconds': round(time.time() - ts, 1)}
            rec['runs'].append(row)
            rec.pop('in_progress', None)
            flush(rec, out)
            print(f'[{time.time()-t0:8.1f}s] DONE  {d["name"]} # {jname}  '
                  f'unknot={row["unknot_endpoint_found"]}  verified={ok}  '
                  f'{row["seconds"]}s', flush=True)
            if ok:
                print('*** VERIFIED RIBBON CERTIFICATE ***', flush=True)
    rec['total_seconds'] = round(time.time() - t0, 1)
    flush(rec, out)
