#!/usr/bin/env python3
"""Common-successor search: the one search in this campaign whose SUCCESS IS A PROOF.

CORRECTED 2026-09-11.  The Dunfield-Gong generator `banded_links` only produces
SPLITTING bands (a ribbon-disk search drives a knot toward an unlink, so every band
raises the component count).  A fusing band, which the naive formulation needed, is
never generated.  The fix is to run the concordance backwards.

Logic.  Apply one splitting band to K and keep the results of the form A u U with U
a split unknot.  Reversing that movie, A -> A u U (birth) -> K (saddle) is an
annulus in S^3 x I (chi = 0 + 1 - 1 = 0), hence a genuine concordance, so

        [A] = [K]   in the smooth concordance group.

If one knot A arises this way from BOTH K_n and K_m then [K_n] = [A] = [K_m], so
D_{n,m} = K_n # (-K_m) is smoothly slice.  Miyazaki (Trans. AMS 341 (1994) Thm 5.5,
via Abe-Tagami Cor. 4.3) proves D_{n,m} is NOT ribbon whenever n != m and
n + m != -1.  A hit is therefore a counterexample to the Slice-Ribbon Conjecture.

Failure proves nothing: it is a coverage statement over the parameter box.
Writes incrementally, so a killed run keeps its partial results.

Usage: concordance_search.py <out.json> <n_diagrams> <max_band_len> <max_twists> <knot.json>...
"""
import json, sys, time, datetime
import snappy
from spherogram.links.bands.core import banded_links, normalize_crossing_labels

def successors(pd, n_diagrams, max_band_len, max_twists, checkpoint):
    """Knots A with a 1-birth 1-saddle concordance A ~ K, keyed by isometry signature."""
    found, stats = {}, {'banded': 0, 'split_off_unknot': 0}
    base = snappy.Link([tuple(c) for c in pd])
    for i in range(n_diagrams):
        L0 = base.copy()
        if i:
            L0.backtrack(20); L0.simplify('basic')
        normalize_crossing_labels(L0)
        for L, spec in banded_links(L0, max_twists, max_band_len, 'shortest'):
            stats['banded'] += 1
            L.simplify('global')
            # want L = A u U with U a split unknot: simplify strips such components
            if L.unlinked_unknot_components < 1:
                continue
            L.unlinked_unknot_components = 0
            if len(L.link_components) != 1:
                continue
            stats['split_off_unknot'] += 1
            if not L.crossings:
                found.setdefault('UNKNOT', {'diagram': i, 'band': spec}); continue
            try:
                sig = L.exterior().isometry_signature(of_link=True)
            except Exception:
                continue
            if sig:
                found.setdefault(sig, {'diagram': i, 'band': spec,
                                       'crossings': len(L.crossings)})
        checkpoint(i, found, stats)
    return found, stats

if __name__ == '__main__':
    out, n_diagrams, max_band_len, max_twists = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    sets, meta, t0 = {}, {}, time.time()
    state = {'date': datetime.datetime.utcnow().isoformat() + 'Z',
             'box': {'n_diagrams': n_diagrams, 'max_band_len': max_band_len,
                     'max_twists': max_twists, 'births': 1, 'saddles': 1},
             'successor_counts': meta, 'hits': [],
             'meaning': 'a hit proves [K_n]=[K_m], hence D_{n,m} slice; with Miyazaki that is a counterexample'}
    def flush():
        state['seconds'] = round(time.time() - t0, 1)
        json.dump(state, open(out, 'w'), indent=1, default=str)
    for f in sys.argv[5:]:
        d = json.load(open(f)); pd = d.get('pd_code_snappy_0indexed') or d['pd_code']
        name = d['name']
        def cp(i, found, stats, name=name):
            meta[name] = {'successors': len(found), 'diagrams_done': i + 1, **stats}
            flush()
        s, st = successors(pd, n_diagrams, max_band_len, max_twists, cp)
        sets[name] = s; meta[name] = {'successors': len(s), 'diagrams_done': n_diagrams, **st}
        print(f'{name}: {len(s)} successors, {st} ({round(time.time()-t0)}s)', flush=True)
        names = list(sets)
        state['hits'] = []
        for a in range(len(names)):
            for b in range(a + 1, len(names)):
                common = set(sets[names[a]]) & set(sets[names[b]])
                if common:
                    state['hits'].append({'pair': [names[a], names[b]],
                                          'n_common': len(common),
                                          'common': sorted(common)[:20]})
                    print('*** COMMON SUCCESSOR ***', names[a], names[b], len(common), flush=True)
        flush()
    print('HITS:', len(state['hits']))
