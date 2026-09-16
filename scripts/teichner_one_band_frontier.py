#!/usr/bin/env python3
"""One-band coverage for the Teichner lane, swept over many diagrams.

The repository already used this argument on K_G: an intermediate link in a
ribbon movie must itself be plausibly slice, so if a box contains NO
plausibly-slice one-band move, no two-band ribbon disk can start inside it
either.  That turns an expensive two-band search into a cheap one-band one.

Here it is applied to `D_{0,1} # J`, the only lane where a verified certificate
is a counterexample outright, across many shaken diagrams and partner mirrors.
A survivor count of 0 on a diagram is coverage of that diagram's box.  It is
never an obstruction, and a nonzero count is not a disk.

Usage: teichner_one_band_frontier.py <out.json> <knot.json> <J,...>
                                     <n_diagrams> <max_band_len> [twists]
"""
import json, sys, time, os, random, datetime
import snappy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
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

out, knot_json, partners = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
n_diagrams, max_len = int(sys.argv[4]), int(sys.argv[5])
twists = int(sys.argv[6]) if len(sys.argv) > 6 else 2

d = json.load(open(knot_json))
K = snappy.Link([tuple(c) for c in (d.get('pd_code_snappy_0indexed') or d['pd_code'])])
rec = {'date': datetime.datetime.utcnow().isoformat() + 'Z', 'knot': d['name'],
       'box': {'max_bands': 1, 'max_band_len': max_len, 'max_twists': twists,
               'paths': 'shortest', 'partners': partners,
               'n_diagrams': n_diagrams, 'backtrack_steps': 25},
       'meaning': ('survivors = plausibly-slice one-band moves. 0 survivors on a '
                   'diagram means no two-band ribbon disk can start in that box on '
                   'that diagram. It is coverage, never an obstruction.'),
       'runs': [], 'hits': []}
t0 = time.time()
for jname in partners:
    base = jname[1:] if jname.startswith('m') else jname
    J = snappy.Link(base)
    if jname.startswith('m'):
        J = J.mirror()
    for i in range(n_diagrams):
        S = K.connected_sum(J)
        S.simplify('global')
        if i:
            random.seed(1000 * i + 7)
            S.backtrack(steps=25)
            S.simplify('global')
        ts = time.time()
        try:
            res = ribbon_concordant_links(S, max_bands=1, max_twists=twists,
                                          max_band_len=max_len, paths='shortest',
                                          certify=True)
            err = None
        except Exception as e:
            res, err = {}, f'{type(e).__name__}: {e}'
        verified = False
        if 'unknot' in res:
            try:
                verified = bool(verify_ribbon_to_unknot(S, res['unknot']))
            except Exception as e:
                err = f'verify {type(e).__name__}: {e}'
        row = {'J': jname, 'diagram': i, 'crossings': len(S.crossings),
               'survivors': len([k for k in res if k != 'unknot']),
               'unknot_endpoint_found': 'unknot' in res,
               'certificate_verified': verified,
               'seconds': round(time.time() - ts, 1), 'error': err}
        if verified:
            row['certificate'] = res['unknot']
            row['sum_pd'] = [list(c) for c in S.PD_code()]
            rec['hits'].append(row)
        rec['runs'].append(row)
        rec['elapsed_seconds'] = round(time.time() - t0, 1)
        tmp = out + '.tmp'
        json.dump(rec, open(tmp, 'w'), indent=1)
        os.replace(tmp, out)
        print(f'[{time.time()-t0:8.1f}s] {d["name"]} # {jname} diagram {i}: '
              f'survivors={row["survivors"]} unknot={row["unknot_endpoint_found"]} '
              f'verified={verified} {row["seconds"]}s'
              + (' *** VERIFIED CERTIFICATE ***' if verified else ''), flush=True)
print('done; hits =', len(rec['hits']), flush=True)
