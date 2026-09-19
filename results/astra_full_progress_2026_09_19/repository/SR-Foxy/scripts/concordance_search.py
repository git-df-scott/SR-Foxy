#!/usr/bin/env python3
"""Historical COMMON-PREDECESSOR search, not a common-successor search.

A splitting band followed by deleting a split unknot gives A <= K. A shared
A would imply concordance after its movies and endpoint identity were verified.
Numerical signature matches are nominations only, never proofs.

For the current Abe-Tagami inputs this direction is futile: their fibered,
irreducible-monodromy condition forces every ribbon predecessor to be the
input itself, and the inputs are distinct. See RESEARCH_AUDIT_2026-09-12.md.
Use fusion_successors.py for the constructive common-UPPER-bound search.
This historical script remains available for other inputs.

Usage: concordance_search.py <out.json> <n_diagrams> <max_band_len> <max_twists> <knot.json>...
"""
import json, sys, time, datetime
import snappy
from spherogram.links.bands.core import banded_links, normalize_crossing_labels

def successors(pd, n_diagrams, max_band_len, max_twists, checkpoint):
    """Legacy function name: generates PREDECESSORS A <= K, not successors."""
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
                sig = L.exterior().isometry_signature(of_link=True, ignore_orientation=False)
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
             'search_direction': 'common_predecessors', 'certified_slice': False,
             'meaning': 'Numerical hits only. Complete movie replay and verified oriented endpoint identification are required before any concordance or sliceness claim.'}
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
                                          'certified': False, 'n_common': len(common),
                                          'common': sorted(common)[:20]})
                    print('*** NUMERICAL COMMON PREDECESSOR CANDIDATE ***', names[a], names[b], len(common), flush=True)
        flush()
    print('HITS:', len(state['hits']))
