#!/usr/bin/env python3
"""Teichner lane, swept over many diagrams of K # J instead of one.

Rationale.  `results/band_generator_saturation.json` shows `max_band_len`
saturates at 6 on `D_{0,1} # 6_1`, so deepening that dial buys nothing.  The
r = 0 RBG sweeps showed the opposite dial does matter: 29 to 85 survivors
across diagrams of ONE knot in an IDENTICAL box.  Every Teichner run in this
repository has searched exactly one diagram.  This script searches many.

It also sweeps partner MIRRORS.  `mirror(J)` is ribbon iff `J` is, but
`K # J` and `K # mirror(J)` are different knots, and the repository's own
component audit found a match against `D_{0,1} # mirror(6_1)` that the
original partner list could not produce.

A verified certificate here proves `K # J` ribbon, hence `K` smoothly slice.
For `K = D_{0,1}`, which carries a Miyazaki non-ribbon certificate, that is a
counterexample to the Slice-Ribbon Conjecture.  Nothing weaker is.  Negatives
are coverage of the box only.

Usage:
  teichner_shaken_sweep.py <out.json> <knot.json> <J,J,...> <n_diagrams>
                           <max_bands> <max_band_len> [max_twists] [paths]
"""
import json, sys, time, datetime, os, random
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


def main():
    out = sys.argv[1]
    knot_json = sys.argv[2]
    partners = sys.argv[3].split(',')
    n_diagrams = int(sys.argv[4])
    max_bands = int(sys.argv[5])
    max_band_len = int(sys.argv[6])
    max_twists = int(sys.argv[7]) if len(sys.argv) > 7 else 2
    paths = sys.argv[8] if len(sys.argv) > 8 else 'shortest'

    d = json.load(open(knot_json))
    pd = d.get('pd_code_snappy_0indexed') or d['pd_code']
    K = snappy.Link([tuple(c) for c in pd])

    rec = {'date': datetime.datetime.utcnow().isoformat() + 'Z',
           'knot': d['name'], 'knot_file': knot_json,
           'filter': 'sagefree_slice_filter; calibrated by rediscovering the '
                     'verified ribbon disk of K_B (31 crossings) in 1.4 s',
           'box': {'partners': partners, 'n_diagrams': n_diagrams,
                   'max_bands': max_bands, 'max_band_len': max_band_len,
                   'max_twists': max_twists, 'paths': paths,
                   'backtrack_steps': 25},
           'runs': [], 'hits': []}
    t0 = time.time()

    def flush():
        rec['elapsed_seconds'] = round(time.time() - t0, 1)
        tmp = out + '.tmp'
        with open(tmp, 'w') as fh:
            json.dump(rec, fh, indent=1)
        os.replace(tmp, out)

    for jname in partners:
        base = jname[1:] if jname.startswith('m') else jname
        J = snappy.Link(base)
        if jname.startswith('m'):
            J = J.mirror()
        # Partner's own ribbon certificate, required by the Teichner criterion.
        pr = ribbon_concordant_links(J, max_bands=2, max_twists=2,
                                     max_band_len=6, paths='shortest',
                                     certify=True)
        pv = ('unknot' in pr) and bool(verify_ribbon_to_unknot(J, pr['unknot']))
        print(f'[{time.time()-t0:8.1f}s] partner {jname}: ribbon certificate '
              f'verified={pv}', flush=True)
        for i in range(n_diagrams):
            S = K.connected_sum(J)
            S.simplify('global')
            if i > 0:
                random.seed(1000 * i + 7)
                S.backtrack(steps=25)
                S.simplify('global')
            n_cross = len(S.crossings)
            ts = time.time()
            try:
                res = ribbon_concordant_links(S, max_bands=max_bands,
                                              max_twists=max_twists,
                                              max_band_len=max_band_len,
                                              paths=paths, certify=True)
                err = None
            except Exception as e:
                res, err = {}, f'{type(e).__name__}: {e}'
            found = 'unknot' in res
            verified = False
            if found:
                try:
                    verified = bool(verify_ribbon_to_unknot(S, res['unknot']))
                except Exception as e:
                    err = f'verify {type(e).__name__}: {e}'
            row = {'J': jname, 'partner_certificate_verified': pv,
                   'diagram': i, 'crossings': n_cross,
                   'endpoints': sorted(res.keys()),
                   'unknot_endpoint_found': found,
                   'certificate_verified': verified,
                   'seconds': round(time.time() - ts, 1), 'error': err}
            if verified:
                row['certificate'] = res['unknot']
                row['sum_pd'] = [list(c) for c in S.PD_code()]
                rec['hits'].append(row)
            rec['runs'].append(row)
            flush()
            tag = ' *** VERIFIED CERTIFICATE ***' if verified else ''
            print(f'[{time.time()-t0:8.1f}s] {d["name"]} # {jname} diagram {i} '
                  f'({n_cross} cr): unknot={found} verified={verified} '
                  f'{row["seconds"]}s{tag}', flush=True)
    flush()
    print(f'[{time.time()-t0:8.1f}s] sweep complete; hits={len(rec["hits"])}',
          flush=True)


if __name__ == '__main__':
    main()
