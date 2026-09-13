#!/usr/bin/env python3
"""Calibrated, bounded reverse-band search on saved nonfibered upper knots.

Two phases: the library's shortest paths, then seeded edge-aware face-simple
paths. Neither phase is exhaustive. A detected split unknot can be deleted;
failure to detect one does not prove nonsplitting. Endpoint matches are
nominations requiring an independent geometric certificate.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import time

import snappy
from spherogram.links.bands.core import Band, add_one_band, min_len_bands, normalize_crossing_labels
from fusion_successors import diagram_signature, pd_hash, replay
from two_fission_target import alex_rank


def sampled_bands(link, seed, attempts, max_length=8, max_twists=2):
    """Sample explicit edges, retaining parallel-edge choices.

    Choose a desired internal path length uniformly, then a random simple
    dual walk of that length. Choose attaching arcs at its two ends, excluding
    crossed arcs. No face repeats; hence the projected core is embedded.
    This is deliberately a biased sample, not uniform sampling of all bands.
    Failed walks count toward attempts and are not mathematical rejections.
    """
    rng = random.Random(seed)
    faces = link.faces()
    edge_faces, edge_cs, adj = defaultdict(list), {}, defaultdict(list)
    face_arcs = []
    for i, face in enumerate(faces):
        face_arcs.append(sorted({cs.strand_label() for cs in face}))
        for cs in face:
            arc = cs.strand_label()
            edge_faces[arc].append(i)
            edge_cs[arc, i] = cs.opposite()
    for arc, ends in sorted(edge_faces.items()):
        if len(ends) != 2:
            raise AssertionError('Expected two face incidences per arc')
        a, b = ends
        adj[a].append((b, arc))
        adj[b].append((a, arc))
    seen = set()
    for attempt in range(attempts):
        length = rng.randrange(max_length - 1)
        start = node = rng.randrange(len(faces))
        visited, path = {start}, []
        for _ in range(length):
            choices = [(v, e) for v, e in adj[node] if v not in visited]
            if not choices:
                break
            nxt, arc = rng.choice(choices)
            path.append((node, arc, nxt))
            visited.add(nxt)
            node = nxt
        if len(path) != length:
            continue
        crossed = {e for _, e, _ in path}
        starts = [a for a in face_arcs[start] if a not in crossed]
        ends = [a for a in face_arcs[node] if a not in crossed]
        if not starts or not ends:
            continue
        a, b = rng.choice(starts), rng.choice(ends)
        if a == b:
            continue
        X, Z = edge_cs[a, start].opposite(), edge_cs[b, node]
        along = [X] + [edge_cs[e, f] for f, e, _ in path] + [Z]
        parity = int((X == X.oriented()) == (Z == Z.oriented()))
        twists = [t for t in range(-max_twists, max_twists + 1) if t % 2 == parity]
        band = Band([(cs.crossing.label, cs.strand_index) for cs in along],
                    rng.randrange(2 ** length), rng.choice(twists))
        spec = band.compressed_spec()
        if spec in seen:
            continue
        seen.add(spec)
        yield band, {'attempt': attempt, 'dual_path': path,
                     'attaching_arcs': [a, b], 'internal_length': length}


def hfk(pd):
    w = subprocess.run([sys.executable, str(Path(__file__).with_name('hfk_worker.py'))],
                       input=json.dumps(pd), capture_output=True, text=True,
                       timeout=5, check=True)
    return json.loads(w.stdout)


def run(args):
    out = Path(args.output)
    if out.exists():
        raise FileExistsError(out)
    raw_input = Path(args.targets).read_bytes()
    targets = [r for r in json.loads(raw_input)['candidates'] if not r['hfk_check']['fibered']]
    targets = targets[args.offset:args.offset + args.count]
    sought = 'K1' if args.forward_source == 'K0' else 'K0'
    nomination_key = sought + '_nominations'
    controls = {}
    for name, file in [('K0', 'AbeTagami_K_0_K_-1__6_3'), ('K1', 'AbeTagami_K_1')]:
        pd = json.loads(Path('data/knots/' + file + '.json').read_text())['pd_code_snappy_0indexed']
        L = snappy.Link(pd)
        L.simplify('basic')
        controls[name] = {'pd': L.PD_code(), 'diagram_signature': diagram_signature(L.PD_code()),
                          'hfk': hfk(L.PD_code())}
    rec = {'status': 'BOUNDED_SEARCH_NOT_A_COUNTEREXAMPLE', 'parameters': vars(args),
           'input_sha256': hashlib.sha256(raw_input).hexdigest(), 'controls': controls,
           'snappy_version': snappy.__version__, 'runs': [], 'complete': False,
           'limitations': ['No exhaustive band or isotopy coverage.',
                          'Failure to detect splitness remains inconclusive.',
                          'HFK equality is only a filter; diagram matches need movie verification.',
                          'Face-simple sampler is biased; numerical isometries do not deduplicate targets.']}
    def save():
        out.write_text(json.dumps(rec, indent=2) + '\n')
    save()
    for r in targets:
        if not replay(r):
            raise AssertionError('Stored forward movie failed exact raw replay')
        J = snappy.Link(r['endpoint_pd'])
        normalize_crossing_labels(J)
        row = {'source_index': r['index'], 'start_pd': J.PD_code(),
               'start_pd_sha256': pd_hash(J.PD_code()), 'forward_raw_replay': True,
               'counts': Counter(), 'length_counts': Counter(), 'endpoints': [], 'phases': [],
               'K0_diagram_control_recovered': False,
               'forward_source_diagram_recovered': False,
               'forward_source_HFK_recovered': False, nomination_key: []}
        rec['runs'].append(row)
        cache, seen_bands = set(), set()
        started = time.monotonic()
        # Link simplification uses Python's global RNG; isolate its seed from
        # the local Random object used for band sampling.
        random.seed(args.seed + r['index'])
        for phase in ['shortest', 'edge_sample']:
            phase_start, n, stop = time.monotonic(), 0, 'enumeration_finished'
            if phase == 'shortest':
                bands = ((b, {}) for b in min_len_bands(J, 2, args.length))
                cap = args.shortest_moves
            else:
                bands = sampled_bands(J, args.seed + r['index'], args.sample_attempts, args.length)
                cap = args.sample_moves
            for band, metadata in bands:
                if n >= cap or time.monotonic() - phase_start >= args.seconds:
                    stop = 'move_cap' if n >= cap else 'time_cap'
                    break
                spec = band.compressed_spec()
                if spec in seen_bands:
                    row['counts']['duplicate_band_specs'] += 1
                    continue
                seen_bands.add(spec)
                L = add_one_band(J, band)
                if not L.is_planar() or len(L.link_components) != 2:
                    raise AssertionError('Band generator failed planarity/component control')
                n += 1
                row['counts'][phase + '_bands'] += 1
                row['length_counts'][str(len(band.cs_along_top))] += 1
                raw = L.PD_code()
                L.simplify('basic')
                split = L.unlinked_unknot_components == 1 and len(L.link_components) == 1
                method = 'basic'
                if not split and args.global_checks and row['counts']['global_attempts'] < args.global_checks:
                    # These necessary conditions only decide where to spend
                    # extra simplification effort, never certify a concordance.
                    if len(L.link_components) == 2 and L.linking_number() == 0:
                        rank, cols = alex_rank(L)
                        row['counts']['nullity_checks'] += 1
                        if rank < cols - 1:
                            row['counts']['global_attempts'] += 1
                            L.simplify('global', type_III_limit=30)
                            method = 'global'
                            split = L.unlinked_unknot_components == 1 and len(L.link_components) == 1
                if not split:
                    row['counts']['split_unknot_not_detected'] += 1
                    continue
                row['counts']['split_unknot_detected'] += 1
                L.unlinked_unknot_components = 0
                pd = L.PD_code()
                signature = diagram_signature(pd)
                if signature in cache:
                    continue
                cache.add(signature)
                endpoint = {'phase': phase, 'band': spec, 'path_metadata': metadata,
                            'raw_split_pd': raw, 'simplification': method, 'endpoint_pd': pd,
                            'diagram_signature': signature, 'certified': False}
                # Independent fresh replay of every retained band, before any
                # simplification, detects accidental mutable-input corruption.
                if add_one_band(snappy.Link(row['start_pd']), spec).PD_code() != raw:
                    raise AssertionError('Reverse band raw replay failed')
                endpoint['raw_replay'] = True
                try:
                    endpoint['hfk'] = hfk(pd)
                    endpoint['HFK_matches'] = [k for k, c in controls.items()
                                               if endpoint['hfk']['ranks'] == c['hfk']['ranks']]
                except Exception as e:
                    endpoint['HFK_unknown'] = type(e).__name__ + ': ' + str(e)
                endpoint['diagram_matches'] = [k for k, c in controls.items() if signature == c['diagram_signature']]
                if 'K0' in endpoint['diagram_matches']:
                    row['K0_diagram_control_recovered'] = True
                if args.forward_source in endpoint['diagram_matches']:
                    row['forward_source_diagram_recovered'] = True
                if args.forward_source in endpoint.get('HFK_matches', []):
                    row['forward_source_HFK_recovered'] = True
                if sought in endpoint.get('HFK_matches', []) or sought in endpoint['diagram_matches']:
                    row[nomination_key].append(len(row['endpoints']))
                row['endpoints'].append(endpoint)
            row['phases'].append({'phase': phase, 'bands_tested': n, 'stop': stop,
                                  'seconds': round(time.monotonic() - phase_start, 3)})
            save()
        row['seconds'] = round(time.monotonic() - started, 3)
        print(json.dumps({k: row[k] for k in ['source_index', 'counts', 'forward_source_diagram_recovered', nomination_key, 'seconds']}), flush=True)
        save()
    rec['complete'] = True
    save()


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('targets'); p.add_argument('output')
    p.add_argument('--count', type=int, default=60); p.add_argument('--offset', type=int, default=0)
    p.add_argument('--seed', type=int, default=20260913)
    p.add_argument('--forward-source', choices=['K0','K1'], default='K0')
    p.add_argument('--length', type=int, default=8)
    p.add_argument('--shortest-moves', type=int, default=20000)
    p.add_argument('--sample-moves', type=int, default=12000)
    p.add_argument('--sample-attempts', type=int, default=100000)
    p.add_argument('--global-checks', type=int, default=0)
    p.add_argument('--seconds', type=float, default=30)
    a = p.parse_args()
    if min(a.count, a.length - 1, a.seconds) <= 0 or min(a.shortest_moves, a.sample_moves, a.sample_attempts, a.global_checks) < 0:
        p.error('Invalid bounds')
    run(a)
