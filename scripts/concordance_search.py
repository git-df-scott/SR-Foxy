#!/usr/bin/env python3
"""Common-successor search: the one search in this campaign whose SUCCESS IS A PROOF.

Logic.  A ribbon concordance from K to J built from one birth and one saddle is an
annulus in S^3 x I (chi = 0 + 1 - 1 = 0), hence a genuine concordance, so [K] = [J]
in the smooth concordance group.  Concretely: form K u U with U a split unknot, then
add one band; any result with a single component is such a J.

If some knot J is reachable from BOTH K_n and K_m, then
        [K_n] = [J] = [K_m],
so D_{n,m} = K_n # (-K_m) is smoothly slice.  Miyazaki (Trans. AMS 341 (1994) Thm 5.5,
as applied in Abe-Tagami Cor. 4.3) proves D_{n,m} is NOT ribbon whenever K_n and K_m
are non-isotopic, i.e. n != m and n + m != -1.  A hit is therefore a counterexample
to the Slice-Ribbon Conjecture.

Failure proves nothing: it is a coverage statement over the parameter box.

Usage: concordance_search.py <out.json> <n_diagrams> <max_band_len> <max_twists> <knot.json>...
"""
import json, sys, time, datetime, collections
import snappy
from spherogram.links.bands.core import banded_links, normalize_crossing_labels

def with_split_unknot(pd):
    mx = max(max(c) for c in pd)
    return [tuple(c) for c in pd] + [(mx + 1, mx + 2, mx + 2, mx + 1)]

def successors(pd, n_diagrams, max_band_len, max_twists, tag):
    """Knots J with a 1-birth 1-saddle ribbon concordance K -> J, by isometry signature."""
    found = {}
    base = snappy.Link(with_split_unknot(pd))
    for i in range(n_diagrams):
        L0 = base.copy()
        if i:
            L0.backtrack(20); L0.simplify('basic')
        normalize_crossing_labels(L0)
        for L, spec in banded_links(L0, max_twists, max_band_len, 'shortest'):
            L.simplify('global'); L.unlinked_unknot_components = 0
            if len(L.link_components) != 1:      # need a KNOT for a concordance
                continue
            if not L.crossings:                  # unknot
                found.setdefault('UNKNOT', (tag, i, spec)); continue
            E = L.exterior()
            try:
                sig = E.isometry_signature(of_link=True)
            except Exception:
                continue
            if sig:
                found.setdefault(sig, (tag, i, spec, len(L.crossings)))
    return found

if __name__ == '__main__':
    out, n_diagrams, max_band_len, max_twists = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    sets, meta = {}, {}
    t0 = time.time()
    for f in sys.argv[5:]:
        d = json.load(open(f))
        pd = d.get('pd_code_snappy_0indexed') or d['pd_code']
        name = d['name']
        s = successors(pd, n_diagrams, max_band_len, max_twists, name)
        sets[name] = s; meta[name] = len(s)
        print(f'{name}: {len(s)} distinct concordance successors  ({round(time.time()-t0)}s)', flush=True)
    names = list(sets)
    hits = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            common = set(sets[names[i]]) & set(sets[names[j]])
            if common:
                hits.append({'pair': [names[i], names[j]], 'common': sorted(common)[:20],
                             'n_common': len(common)})
                print('*** COMMON SUCCESSOR ***', names[i], names[j], len(common), flush=True)
    rec = {'date': datetime.datetime.utcnow().isoformat() + 'Z',
           'box': {'n_diagrams': n_diagrams, 'max_band_len': max_band_len,
                   'max_twists': max_twists, 'births': 1, 'saddles': 1},
           'successor_counts': meta, 'seconds': round(time.time() - t0, 1),
           'hits': hits,
           'meaning': 'a hit proves [K_n]=[K_m], hence D_{n,m} slice; with Miyazaki that is a counterexample'}
    json.dump(rec, open(out, 'w'), indent=1, default=str)
    print(json.dumps({k: v for k, v in rec.items() if k != 'hits'}, indent=1))
    print('HITS:', len(hits))
