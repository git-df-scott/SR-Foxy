#!/usr/bin/env python3
"""Bounded birth + fusion search; outputs move witnesses, never CE claims.

Uses the Band/add_one_band convention of Spherogram 2.4.1 (Dunfield--Gong).
Unlike its splitting-only band generator, endpoints here lie on different
components. A born unknot is a separate two-kink diagram. An explicit
reverse Reidemeister II move overlaps its projection with an old face while
preserving the split link. Every birth isotopy and fusion is serialized.

By default only one shortest dual path is tried per endpoint/face choice;
--detours adds seeded random simple paths and --per-face-moves balances coverage.
This is a bounded, incomplete search. Stored witnesses allow exact replay of
the band operation. Simplification and knot identification remain separate
verification obligations; matching hashes do not declare sliceness here.
"""
import argparse
from collections import defaultdict, deque
import hashlib
from itertools import product
import json
import random
from pathlib import Path
import time

import regina
import snappy
from spherogram.links.bands.core import Band, add_one_band, normalize_crossing_labels
from spherogram.links.simplify import reverse_type_II


def pd_hash(pd):
    return hashlib.sha256(json.dumps(pd, separators=(',', ':')).encode()).hexdigest()


def diagram_signature(pd):
    if not pd:
        return 'UNKNOT'
    r = regina.Link.fromPD([[a + 1 for a in row] for row in pd])
    # Reversal is allowed here only as a search index; a hit requires an
    # orientation audit. Reflections must never silently identify mirrors.
    return r.sig(False, True, True)


def birth_diagram(pd):
    n = len(pd)
    if not n:
        raise ValueError('Represent the input unknot by a one-crossing RI diagram')
    # Two kinks leave a two-edge interior face. A one-kink birth together
    # with simple shortest paths cannot enter the birth disk through a
    # different edge from the attaching edge; that pilot produced only
    # cancelling births/saddles. Keep the two-edge interior available.
    born = snappy.Link([tuple(c) for c in pd] +
                       [(2*n, 2*n+1, 2*n+1, 2*n+2),
                        (2*n+2, 2*n+3, 2*n+3, 2*n)])
    normalize_crossing_labels(born)
    if len(born.link_components) != 2:
        raise ValueError('Input must be a one-component knot diagram')
    return born


def detour_paths(adj, start, end, excluded, max_edges, rng, attempts):
    """Sample simple dual paths; no self-intersections of the band core."""
    found = set()
    for _ in range(attempts):
        node, path, visited = start, [], {start}
        while node != end and len(path) < max_edges:
            choices = [(v, a) for v, a in adj[node] if a not in excluded and v not in visited]
            if not choices:
                break
            nxt, arc = rng.choice(choices)
            path.append((node, arc, nxt)); visited.add(nxt); node = nxt
        key = tuple(path)
        if node == end and key not in found:
            found.add(key)
            yield path


def fusion_bands(pd, max_length=5, max_twists=2, detours=0, seed=0, per_face_moves=0):
    split = birth_diagram(pd)
    n = len(pd)
    faces = split.faces()
    old_faces = [i for i, f in enumerate(faces) if f[0].crossing.label < n]
    new_faces = [i for i, f in enumerate(faces) if f[0].crossing.label >= n]
    outer_u = max(new_faces, key=lambda i: len(faces[i]))
    seen = set()
    rng = random.Random(seed)
    for placement in old_faces:
        face_moves = 0
        # Draw the birth across an old strand by an explicit reversible RII
        # isotopy. The two components remain split, but their projections
        # now overlap. Without this, simple dual paths produced only trivial
        # concordances, even after the birth acquired two kinks.
        L = split.copy()
        split_faces = L.faces()
        c, d = split_faces[placement][0], split_faces[outer_u][0]
        isotopy = {'c': [c.crossing.label, c.strand_index],
                   'd': [d.crossing.label, d.strand_index],
                   'labels': [len(L.crossings), len(L.crossings)+1]}
        reverse_type_II(L, c, d, *isotopy['labels'], rebuild=True)
        normalize_crossing_labels(L)
        if not L.is_planar() or len(L.link_components) != 2:
            raise AssertionError('Birth RII isotopy failed')
        faces = L.faces()
        old_component = next(comp for comp in L.link_components
                             if any(cs.crossing.label == 0 for cs in comp))
        new_component = next(comp for comp in L.link_components if comp is not old_component)
        old_arcs = sorted(cs.strand_label() for cs in old_component)
        new_arcs = sorted(cs.strand_label() for cs in new_component)
        edge_faces = defaultdict(list)
        edge_cs = {}
        for i, face in enumerate(faces):
            node = i
            for cs in face:
                arc = cs.strand_label()
                edge_faces[arc].append(node)
                edge_cs[arc, node] = cs.opposite()
        adj = defaultdict(list)
        for arc, ends in edge_faces.items():
            if len(ends) != 2:
                raise ValueError('Every arc must have two face incidences')
            a, b = ends
            adj[a].append((b, arc))
            adj[b].append((a, arc))
        arc_pairs = list(product(old_arcs, new_arcs))
        if detours:
            rng.shuffle(arc_pairs)
        for a, b in arc_pairs:
            if per_face_moves and face_moves >= per_face_moves:
                break
            for start, end in product(edge_faces[a], edge_faces[b]):
                queue = deque([(start, [])])
                visited = {start}
                path = None
                while queue:
                    node, prefix = queue.popleft()
                    if node == end:
                        path = prefix
                        break
                    if len(prefix) >= max_length - 2:
                        continue
                    for nxt, arc in sorted(adj[node]):
                        if arc in (a, b) or nxt in visited:
                            continue
                        visited.add(nxt)
                        queue.append((nxt, prefix + [(node, arc, nxt)]))
                if path is None:
                    continue
                paths = [path]
                if detours:
                    paths += list(detour_paths(adj, start, end, {a, b}, max_length-2, rng, detours))
                for path in paths:
                    X = edge_cs[a, start].opposite()
                    Z = edge_cs[b, end]
                    along = [X] + [edge_cs[arc, node] for node, arc, _ in path] + [Z]
                    parity = int((X == X.oriented()) == (Z == Z.oriented()))
                    top = [(cs.crossing.label, cs.strand_index) for cs in along]
                    for twist in range(-max_twists, max_twists + 1):
                        if twist % 2 != parity:
                            continue
                        for over_bits in range(2 ** len(path)):
                            band = Band(top, over_bits, twist)
                            key = (placement, band.compressed_spec())
                            if key in seen:
                                continue
                            seen.add(key)
                            if per_face_moves and face_moves >= per_face_moves:
                                continue
                            face_moves += 1
                            result = add_one_band(L, band)
                            if len(result.link_components) != 1:
                                raise AssertionError('Fusion did not produce one component')
                            yield result, {
                                'birth_face': placement, 'unknot_outer_face': outer_u,
                                'split_pd': split.PD_code(), 'birth_isotopy_RII': isotopy,
                                'birth_pd': L.PD_code(), 'band': band.compressed_spec(),
                                'dual_path': path, 'source_pd_sha256': pd_hash(pd),
                                'raw_output_pd': result.PD_code(),
                            }



def replay(witness):
    if 'split_pd' in witness:
        from spherogram.links.links_base import CrossingStrand
        S = snappy.Link([tuple(c) for c in witness['split_pd']])
        normalize_crossing_labels(S)
        iso = witness['birth_isotopy_RII']
        c = CrossingStrand(S.crossings[iso['c'][0]], iso['c'][1])
        d = CrossingStrand(S.crossings[iso['d'][0]], iso['d'][1])
        reverse_type_II(S, c, d, *iso['labels'], rebuild=True)
        if S.PD_code() != [tuple(c) for c in witness['birth_pd']]:
            return False
    L = snappy.Link([tuple(c) for c in witness['birth_pd']])
    normalize_crossing_labels(L)
    B = add_one_band(L, witness['band'])
    return B.PD_code() == [tuple(c) for c in witness['raw_output_pd']]


def search(pd, output, max_length=5, max_twists=2, max_moves=1000, seconds=120, detours=0, seed=0, per_face_moves=0):
    t0 = time.monotonic()
    seen = set()
    count = 0
    replay_failures = 0
    reason = 'face_caps_or_enumeration_finished' if per_face_moves else 'enumeration_finished'
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise FileExistsError(output)
    with output.open('x') as f:
        f.write(json.dumps({'type': 'header', 'source_pd': pd,
                           'max_length': max_length, 'max_twists': max_twists,
                           'max_moves': max_moves, 'seconds_limit': seconds,
                           'detour_attempts': detours, 'seed': seed, 'per_face_moves': per_face_moves,
                           'snappy': snappy.__version__, 'regina': regina.versionString(),
                           'status': 'EXPLORATORY_NOT_A_SLICE_CERTIFICATE'}) + '\n')
        for B, witness in fusion_bands(pd, max_length, max_twists, detours, seed, per_face_moves):
            count += 1
            valid = replay(witness)
            replay_failures += int(not valid)
            if not valid:
                raise AssertionError('Band witness did not replay')
            B.simplify('basic')
            endpoint = B.PD_code()
            sig = diagram_signature(endpoint)
            witness.update({'type': 'move', 'index': count, 'replay_passed': valid,
                            'endpoint_pd': endpoint, 'diagram_signature': sig,
                            'crossings': len(endpoint), 'new_signature': sig not in seen})
            seen.add(sig)
            f.write(json.dumps(witness) + '\n')
            f.flush()
            if count >= max_moves or time.monotonic() - t0 >= seconds:
                reason = 'move_cap' if count >= max_moves else 'time_cap'
                break
        summary = {'type': 'summary', 'moves': count, 'unique_diagrams': len(seen),
                   'replay_failures': replay_failures, 'stop_reason': reason,
                   'seconds': round(time.monotonic() - t0, 3),
                   'meaning': 'Bounded successor enumeration; no non-ribbonness or sliceness conclusion.'}
        f.write(json.dumps(summary) + '\n')
    return summary


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('knot')
    ap.add_argument('output')
    ap.add_argument('--length', type=int, default=5)
    ap.add_argument('--twists', type=int, default=2)
    ap.add_argument('--moves', type=int, default=1000)
    ap.add_argument('--seconds', type=float, default=120)
    ap.add_argument('--detours', type=int, default=0)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--per-face-moves', type=int, default=0)
    args = ap.parse_args()
    if Path(args.knot).is_file():
        card = json.loads(Path(args.knot).read_text())
        pd = card.get('pd_code_snappy_0indexed') or card['pd_code']
    else:
        pd = snappy.Link(args.knot).PD_code()
    print(json.dumps(search(pd, args.output, args.length, args.twists, args.moves, args.seconds, args.detours, args.seed, args.per_face_moves)))
