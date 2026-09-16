#!/usr/bin/env python3
"""Census: links that Eisermann certifies NON-RIBBON but that pass the cheap
slice screens.

This inverts the usual difficulty.  For knots there is no computable
ribbon-only obstruction at all (`research/02` section 0), so a counterexample
needs the hard half -- proving non-ribbonness -- and only the easy half,
sliceness, is ever available.  For LINKS Eisermann's Theorem 1 gives a
computable non-ribbon certificate outright:

    every n-component RIBBON link satisfies null V(L) = n - 1,

so `null V(L) < n - 1` proves L is not ribbon, full stop.  Meanwhile a slice
link with n >= 2 has Delta(L) = 0, hence det(L) = 0, hence V(L)(q=i) = 0,
hence `null V(L) >= 1`.

For n = 2 those meet -- `1 >= null V >= n-1 = 1` -- so no 2-component link can
be caught, which is `research/22` section 3.1 and why WS5 was vacuous.  From
n = 3 they separate: a 3-component link with

    null V(L) = 1,  all linking numbers 0,  every component a slice knot

is **certified not ribbon** and passes the cheap necessary conditions for
being slice.  If any such link is in fact slice, it is a slice link that is
not ribbon -- the first object of any kind with that property.

This script produces the shortlist over SnapPy's Thistlethwaite census of
hyperbolic link exteriors.  A shortlist entry is NOT a counterexample: it is
certified non-ribbon and merely not yet excluded from being slice.  Sliceness
still has to be established, and for these links the first thing that will
kill most of them is a nonvanishing Milnor triple-linking number, which this
script does not compute.

Usage: eisermann_census.py <out.json> <cusps> [limit] [start]
"""
import json, os, sys, time, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import snappy
from sagefree_jones import jones_polynomial
from sagefree_eisermann import null_and_det_V
from sagefree_slice_filter import slice_knot_screen


def main():
    out = sys.argv[1]
    cusps = int(sys.argv[2])
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 9
    start = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    census = snappy.HTLinkExteriors(cusps=cusps)
    total = min(len(census), start + limit)
    rec = {'date': datetime.datetime.utcnow().isoformat() + 'Z',
           'census': f'HTLinkExteriors(cusps={cusps})',
           'range': [start, total], 'census_size': len(census),
           'screens': ['all pairwise linking numbers zero',
                       'every component a slice knot (signature 0, |det| a '
                       'square, Fox-Milnor)',
                       '1 <= null V(L) < n-1: at least 1 as slice requires, '
                       'less than n-1 as ribbon forbids'],
           'counts': {'examined': 0, 'lk_zero': 0, 'components_slice': 0,
                      'null_V_1': 0, 'shortlist': 0},
           'shortlist': [], 'stop': None}
    t0 = time.time()

    def flush():
        rec['elapsed_seconds'] = round(time.time() - t0, 1)
        tmp = out + '.tmp'
        json.dump(rec, open(tmp, 'w'), indent=1)
        os.replace(tmp, out)

    for idx in range(start, total):
        M = census[idx]
        rec['counts']['examined'] += 1
        try:
            L = M.link()
        except Exception:
            continue
        n = len(L.link_components)
        if n != cusps:
            continue
        try:
            lkm = L.linking_matrix()
            if any(lkm[i][j] != 0 for i in range(n) for j in range(n) if i != j):
                continue
        except Exception:
            continue
        rec['counts']['lk_zero'] += 1
        try:
            ok = True
            for i in range(n):
                C = L.copy()
                S = C.sublink([C.link_components[i]])
                S.simplify('global')
                if S.crossings and not slice_knot_screen(S):
                    ok = False
                    break
            if not ok:
                continue
        except Exception:
            continue
        rec['counts']['components_slice'] += 1
        try:
            nu, dv, notes = null_and_det_V(L)
        except Exception:
            continue
        # slice forces null V >= 1; ribbon forces null V = n-1.  The window
        # 1 <= null V < n-1 is where a link is certified non-ribbon while still
        # passing the slice-necessary condition.  It is empty for n = 2, which
        # is research/22 section 3.1, and widens with n.
        if not (1 <= nu < n - 1):
            continue
        rec['counts']['null_V_1'] += 1
        rec['counts']['shortlist'] += 1
        row = {'name': M.name(), 'components': n, 'crossings': len(L.crossings),
               'null_V': nu, 'ribbon_requires_null_V': n - 1,
               'det_V': str(dv), 'pd_code': [list(c) for c in L.PD_code()],
               'verdict': ('NOT RIBBON by Eisermann Theorem 1; passes the cheap '
                           'slice screens; sliceness NOT established')}
        rec['shortlist'].append(row)
        flush()
        print('SHORTLIST', M.name(), 'n =', n, 'null V =', nu, flush=True)
        if idx % 250 == 0:
            print(f'[{time.time()-t0:7.0f}s] {idx}/{total} ' +
                  json.dumps(rec['counts']), flush=True)
    rec['stop'] = 'finished'
    flush()
    print('done', json.dumps(rec['counts']), flush=True)


if __name__ == '__main__':
    main()
