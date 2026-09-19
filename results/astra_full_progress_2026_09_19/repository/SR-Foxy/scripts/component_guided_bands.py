#!/usr/bin/env python3
"""Separate component identity from splitness in a bounded one-fission search.

Jones equality is only a nomination. It does not identify a knot or unknot.
A whole-link Jones mismatch with the split product proves nonsplitting of
that specific link. This gate is necessary after the FINAL splitting saddle;
it must not be imposed on the first stage of a multi-saddle concordance.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import time
import regina
import snappy
from spherogram.links.bands.core import add_one_band, min_len_bands, normalize_crossing_labels
from fusion_successors import diagram_signature, pd_hash, replay
from nonfibered_reverse_audit import sampled_bands, hfk


def compact(p): return {k: v for k, v in p.items() if v}
def encoded(p): return [[k, v] for k, v in sorted(p.items()) if v]


def product(a, b):
    p = Counter()
    for i, x in a.items():
        for j, y in b.items(): p[i + j] += x * y
    return compact(p)


def jones(L):
    """Normalized Jones in q; unlink factor q+q^-1 (Regina x=-q)."""
    if not L.crossings:
        if not L.unlinked_unknot_components: raise ValueError('Empty link has no knot polynomial')
        p = {0: 1}
        for _ in range(L.unlinked_unknot_components - 1): p = product(p, {-1: 1, 1: 1})
        return p
    R = regina.Link.fromPD([[a + 1 for a in c] for c in L.PD_code()]).jones()
    p = {i: int(str(R[i])) * (-1 if i % 2 else 1) for i in range(R.minExp(), R.maxExp() + 1)}
    for _ in range(L.unlinked_unknot_components): p = product(p, {-1: 1, 1: 1})
    return compact(p)


def parts(L):
    answer = [L.sublink(i) for i in range(len(L.link_components))]
    answer += [snappy.Link([]) for _ in range(L.unlinked_unknot_components)]
    for K in answer:
        K.simplify('basic')
        if not K.crossings: K.unlinked_unknot_components = 1
        if len(K.link_components) + K.unlinked_unknot_components != 1:
            raise AssertionError('Sublink did not retain exactly one component')
    return answer


def l1(a, b): return sum(abs(a.get(i, 0) - b.get(i, 0)) for i in a.keys() | b.keys())


def inspect(L, wanted, full=False):
    """The score is polynomial coefficient distance, not a knot distance."""
    L = L.copy(); L.simplify('basic')
    P = parts(L)
    if len(P) != 2: raise AssertionError('Expected a two-component final-stage link')
    polys = [jones(K) for K in P]
    scored = sorted((l1(polys[i], wanted) + l1(polys[1-i], {0: 1}), i) for i in range(2))
    score, i = scored[0]
    answer = {'link_pd': L.PD_code(), 'unlinked_unknots': L.unlinked_unknot_components,
              'component_pd': [K.PD_code() for K in P], 'component_Jones': [encoded(p) for p in polys],
              'component_is_unknot_by_basic_simplification': [not K.crossings for K in P],
              'polynomial_distance': score, 'wanted_component': i,
              'component_Jones_match': score == 0, 'linking_number': L.linking_number(),
              'split_unknot_detected': L.unlinked_unknot_components == 1 and len(L.link_components) == 1,
              'certified_concordance': False}
    if full:
        whole = jones(L); split = product(product(polys[0], polys[1]), {-1: 1, 1: 1})
        answer.update(whole_Jones=encoded(whole), split_product_Jones=encoded(split),
                      nonsplit_by_Jones=whole != split)
    return answer


def controls():
    K = snappy.Link('6_3'); n = 2 * len(K.crossings)
    S = snappy.Link(K.PD_code() + [(n, n+1, n+1, n)])
    W = snappy.Link('L5a1').connected_sum(K)
    positive, negative = inspect(S, jones(K), True), inspect(W, jones(K), True)
    assert positive['component_Jones_match'] and positive['split_unknot_detected']
    assert not positive['nonsplit_by_Jones']
    assert negative['component_Jones_match'] and negative['linking_number'] == 0
    assert negative['nonsplit_by_Jones'] and not negative['split_unknot_detected']
    # Both component knots are explicitly recognized in the negative control,
    # yet their zero-linking union is not split.
    got = {diagram_signature(pd) if pd else 'UNKNOT' for pd in negative['component_pd']}
    assert got == {diagram_signature(K.PD_code()), 'UNKNOT'}
    return {'split_K0_U': positive, 'Whitehead_component_sum_K0': negative}


def run(a):
    out = Path(a.output)
    if out.exists(): raise FileExistsError(out)
    input_bytes = Path(a.targets).read_bytes()
    entries = json.loads(input_bytes)['candidates'][a.offset:a.offset+a.count]
    card = 'AbeTagami_K_1' if a.wanted == 'K1' else 'AbeTagami_K_0_K_-1__6_3'
    wanted_pd = json.loads(Path('data/knots/' + card + '.json').read_text())['pd_code_snappy_0indexed']
    wanted = jones(snappy.Link(wanted_pd)); wanted_hfk = hfk(wanted_pd)
    rec = {'status': 'BOUNDED_COMPONENT_GUIDED_SEARCH', 'parameters': vars(a),
           'input_sha256': hashlib.sha256(input_bytes).hexdigest(),
           'wanted_Jones': encoded(wanted), 'wanted_HFK': wanted_hfk,
           'controls': controls(), 'runs': [], 'complete': False,
           'scope': 'Component polynomial matches and heuristic scores are not knot identifications. Only final one-fission endpoints are filtered.'}
    def save(): out.write_text(json.dumps(rec, indent=2) + '\n')
    save()
    for r in entries:
        if r['hfk_check']['fibered']: raise ValueError('This pass excludes fibered upper targets')
        assert replay(r)
        J = snappy.Link(r['endpoint_pd']); normalize_crossing_labels(J)
        row = {'index': r['index'], 'start_pd': J.PD_code(), 'counts': Counter(),
               'matches': [], 'best': [], 'complete': False}
        rec['runs'].append(row)
        t0 = time.monotonic(); seen = set(); best_keys = set(); random.seed(a.seed + r['index'])
        short = [(b, {'phase': 'shortest'}) for b in min_len_bands(J, a.twists, a.length)] if a.shortest else []
        def candidates():
            yield from short
            for b, meta in sampled_bands(J, a.seed + r['index'], a.attempts, a.length, a.twists):
                yield b, dict(meta, phase='edge_sample')
        stop = 'enumeration_finished'
        for band, meta in candidates():
            if row['counts']['bands'] >= a.moves or time.monotonic() - t0 > a.seconds:
                stop = 'move_cap' if row['counts']['bands'] >= a.moves else 'time_cap'; break
            spec = band.compressed_spec()
            if spec in seen: continue
            seen.add(spec)
            L = add_one_band(J, band)
            assert L.is_planar() and len(L.link_components) == 2
            raw = L.PD_code(); row['counts']['bands'] += 1
            if a.zero_linking_only and L.linking_number() != 0:
                row['counts']['nonzero_linking_skipped'] += 1; continue
            c = inspect(L, wanted)
            row['counts']['component_pairs_checked'] += 1
            keep = c['component_Jones_match'] or len(row['best']) < a.best or c['polynomial_distance'] < row['best'][-1]['polynomial_distance']
            if not keep: continue
            key = diagram_signature(c['link_pd']) + ':' + str(c['unlinked_unknots'])
            if key in best_keys: continue
            best_keys.add(key)
            c.update(band=spec, raw_pd=raw, path_metadata=meta)
            assert add_one_band(snappy.Link(row['start_pd']), spec).PD_code() == raw
            c['raw_replay'] = True
            if c['component_Jones_match']:
                c.update(inspect(L, wanted, True))
                row['counts']['unique_component_Jones_matches'] += 1
                try:
                    w = c['component_pd'][c['wanted_component']]
                    c['component_HFK'] = hfk(w)
                    c['component_HFK_matches'] = c['component_HFK']['ranks'] == wanted_hfk['ranks']
                except Exception as e: c['HFK_unknown'] = type(e).__name__ + ': ' + str(e)
                if not c['nonsplit_by_Jones'] and c['linking_number'] == 0:
                    G = snappy.Link(raw); G.simplify('global', type_III_limit=100)
                    c['global_split_unknot_detected'] = G.unlinked_unknot_components == 1 and len(G.link_components) == 1
                    c['after_global_pd'] = G.PD_code()
                row['matches'].append(c)
            else:
                row['best'].append(c); row['best'].sort(key=lambda x:x['polynomial_distance']); row['best'] = row['best'][:a.best]
            if row['counts']['bands'] % 250 == 0 or c['component_Jones_match']: save()
        row.update(complete=True, stop=stop, seconds=round(time.monotonic()-t0, 3))
        save(); print(json.dumps({'index': r['index'], 'counts': row['counts'], 'best_distance': row['best'][0]['polynomial_distance'] if row['best'] else None, 'seconds': row['seconds']}), flush=True)
    rec['complete'] = True; save()


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('targets'); p.add_argument('output'); p.add_argument('--wanted', choices=['K0','K1'], required=True)
    p.add_argument('--count', type=int, default=2); p.add_argument('--offset', type=int, default=0)
    p.add_argument('--seed', type=int, default=20260916); p.add_argument('--length', type=int, default=10)
    p.add_argument('--twists', type=int, default=4); p.add_argument('--moves', type=int, default=20000)
    p.add_argument('--attempts', type=int, default=200000); p.add_argument('--seconds', type=float, default=90)
    p.add_argument('--best', type=int, default=8); p.add_argument('--shortest', action='store_true')
    p.add_argument('--zero-linking-only', action='store_true')
    run(p.parse_args())
