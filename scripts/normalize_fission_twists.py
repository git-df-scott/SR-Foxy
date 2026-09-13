#!/usr/bin/env python3
"""Normalize linking by full band twists, then audit nearby over/under choices.

For a fission band the two long edges belong to different components. Adding
a full twist only changes mixed crossings; it preserves both component knot
types and changes their linking number by one with coherent orientations.
The library can reverse orientations during rebuilding, so test both signs
of the correction and verify linking zero. This removes one search parameter.
"""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import time
import snappy
from spherogram.links.bands.core import Band, add_one_band
from component_guided_bands import inspect, jones, l1, parts, encoded
from fusion_successors import diagram_signature


def normalize(J, b):
    L = add_one_band(J, b)
    assert len(L.link_components) == 2
    old = int(L.linking_number()); trials = []
    solutions = []
    for t in sorted({b.num_twist - 2*abs(old), b.num_twist + 2*abs(old)}):
        N = Band(b.cs_along_top, b.arc_is_under, t)
        S = add_one_band(J, N)
        trials.append({'twist':t,'linking':S.linking_number()})
        if S.linking_number() == 0: solutions.append((N,S))
    assert len(solutions) == 1
    N,S = solutions[0]; t = N.num_twist
    assert S.is_planar() and len(S.link_components) == 2 and S.linking_number() == 0
    # Independent invariant check of the claimed preservation, including
    # normalization beyond the twist range of the original search.
    sig = lambda X: sorted(encoded(jones(K)) for K in parts(X))
    assert sig(L) == sig(S)
    return N, S, {'old_twist': b.num_twist, 'old_linking': old,
                  'correction_trials': trials, 'normalized_twist': t,
                  'component_Jones_preserved': True}


def run(a):
    out = Path(a.output)
    if out.exists(): raise FileExistsError(out)
    raw = Path(a.input).read_bytes(); source = json.loads(raw)
    assert source['complete']
    wanted = dict(source['wanted_Jones'])
    card = 'AbeTagami_K_0_K_-1__6_3' if source['parameters']['wanted'] == 'K0' else 'AbeTagami_K_1'
    pd = json.loads(Path('data/knots/' + card + '.json').read_text())['pd_code_snappy_0indexed']
    target = snappy.Link(pd); target.simplify('basic'); target_sig = diagram_signature(target.PD_code())
    rec = {'status': 'LINKING_NORMALIZED_NEIGHBORHOOD_SEARCH_NOT_A_CERTIFICATE',
           'parameters': vars(a), 'input_sha256': hashlib.sha256(raw).hexdigest(),
           'runs': [], 'complete': False}
    def save(): out.write_text(json.dumps(rec, indent=2) + '\n')
    for r in source['runs']:
        row = {'index': r['index'], 'counts': Counter(), 'matches': [], 'complete': False}
        rec['runs'].append(row); J = snappy.Link(r['start_pd']); seen = set(); links = set(); t0 = time.monotonic()
        for m in r['matches']:
            b = Band(m['band']); n = len(b.arc_is_under)
            masks = [()] + [(i,) for i in range(n)]
            if a.radius >= 2: masks += list(itertools.combinations(range(n), 2))
            for flip in masks:
                bits = b.arc_is_under.copy()
                for i in flip: bits[i] = not bits[i]
                trial = Band(b.cs_along_top, bits, b.num_twist % 2)
                key = trial.compressed_spec()
                if key in seen: continue
                seen.add(key)
                N, L, control = normalize(J, trial); row['counts']['normalized_bands'] += 1
                c = inspect(L, wanted)
                if not c['component_Jones_match']: continue
                row['counts']['component_matches_before_dedup'] += 1
                key = diagram_signature(c['link_pd']) + ':' + str(c['unlinked_unknots'])
                if key in links: continue
                links.add(key); c.update(inspect(L, wanted, True))
                c['band'] = N.compressed_spec(); c['raw_pd'] = L.PD_code()
                assert add_one_band(J, c['band']).PD_code() == c['raw_pd']
                c['raw_replay'] = True; c['normalization'] = control
                c['seed_band'] = m['band']; c['flipped_positions'] = flip
                i = c['wanted_component']; other = 1-i
                c['component_diagram_matches_target'] = diagram_signature(c['component_pd'][i]) == target_sig
                c['other_component_is_unknot_by_simplification'] = not c['component_pd'][other]
                c['split_product_coefficient_distance'] = l1(dict(c['whole_Jones']), dict(c['split_product_Jones']))
                if not c['nonsplit_by_Jones']:
                    G = L.copy(); G.simplify('global', type_III_limit=200)
                    c['global_split_unknot_detected'] = G.unlinked_unknot_components == 1 and len(G.link_components) == 1
                    c['after_global_pd'] = G.PD_code()
                row['matches'].append(c)
            save()
            if time.monotonic()-t0 > a.seconds:
                row['stop'] = 'time_cap'; break
        row.update(complete=True, seconds=round(time.monotonic()-t0, 3)); row.setdefault('stop', 'neighborhood_finished')
        row['counts']['distinct_matches'] = len(row['matches'])
        row['counts']['nonsplit_by_Jones'] = sum(c['nonsplit_by_Jones'] for c in row['matches'])
        save(); print(json.dumps({k:v for k,v in row.items() if k != 'matches'}), flush=True)
    rec['complete'] = True; save()


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input'); p.add_argument('output'); p.add_argument('--radius', type=int, choices=[1,2], default=1)
    p.add_argument('--seconds', type=float, default=45)
    run(p.parse_args())
