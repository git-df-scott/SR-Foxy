#!/usr/bin/env python3
"""Apply Abe--Tagami Cor.4.3 to two visible eligible factors of saved knots.

Excludes only ribbon completions of these fixed pure-fission prefixes, never
sliceness of D01. Decomposition and HFK depend on the recorded implementations.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import snappy
import sympy
from component_guided_bands import jones, encoded
from fusion_successors import diagram_signature
from nonfibered_reverse_audit import hfk
from sagefree_slice_filter import signature_and_det


def run(output, rank_screen=None):
    destination = Path(output)
    if destination.exists():
        raise FileExistsError(destination)
    sources = [Path('results/september14_frontier_components.json'),
               Path('results/teichner_D01_J946_component_filtered_continuation.json')]
    screen, front = [json.loads(p.read_text()) for p in sources]
    origins = {}
    if rank_screen:
        rank_path = Path(rank_screen)
        rank = json.loads(rank_path.read_text())
        assert rank['complete']
        screen, front = {'paths': []}, {'frontier': []}
        loaded = {}
        sources = [rank_path]
        for row in rank['rows']:
            if row['obstructed']:
                continue
            path = Path(row['source'])
            if str(path) not in loaded:
                assert hashlib.sha256(path.read_bytes()).hexdigest() == rank['inputs'][str(path)]
                loaded[str(path)] = json.loads(path.read_text())
                sources.append(path)
            i = len(front['frontier'])
            front['frontier'].append(loaded[str(path)]['frontier'][row['index']])
            screen['paths'].append({'lane': 'D01_J946', 'index': i, 'rejected': False})
            origins[i] = {'source': str(path), 'index': row['index']}
    record = {'input_hashes': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
              'source': 'https://arxiv.org/html/1502.01102#S4.SS0.C3',
              'theorem': 'Abe--Tagami Corollary 4.3', 'factors': {}, 'rows': [],
              'complete': False,
              'scope': 'Saved endpoint components with exactly two visible factors. '
                       'HFK fiberedness and exact symbolic irreducibility plus Jones nonidentity. '
                       'Not a sliceness obstruction on D01.'}
    t = sympy.Symbol('t')
    def factor_data(link):
        link.simplify('basic')
        key = diagram_signature(link.PD_code())
        if key not in record['factors']:
            row = {'pd': link.PD_code(), 'eligible': False}
            try:
                H = hfk(link.PD_code())
                coeff = Counter()
                for A, M, n in H['ranks']:
                    coeff[A] += n * (-1 if M % 2 else 1)
                coeff = {a: n for a, n in coeff.items() if n}
                low = min(coeff)
                poly = sympy.Poly(sum(n*t**(a-low) for a, n in coeff.items()), t)
                if poly.eval(1) == -1:
                    poly = -poly
                signature, determinant = signature_and_det(link)
                assert poly.eval(1) == 1 and abs(int(poly.eval(-1))) == abs(determinant)
                row.update(HFK=H, alexander=str(poly.as_expr()),
                           determinant=determinant, signature=signature,
                           irreducible=bool(poly.is_irreducible), Jones=encoded(jones(link)))
                row['eligible'] = bool(H['fibered'] and poly.degree() > 0 and poly.is_irreducible)
            except Exception as e:
                row['error_unknown'] = repr(e)
            record['factors'][key] = row
        return key
    # The criterion retains K0#(-K0); it rejects distinct eligible factors.
    k0 = snappy.Link('6_3')
    a, b = factor_data(k0), factor_data(k0.mirror())
    if not all(record['factors'][k]['eligible'] for k in (a, b)):
        destination.write_text(json.dumps(record, separators=(',', ':')) + '\n')
        raise AssertionError('Positive control calculation failed; see saved unknowns')
    mirrored_b = sorted([[-e, n] for e, n in record['factors'][b]['Jones']])
    assert record['factors'][a]['Jones'] == mirrored_b
    record['square_sum_control_passed'] = True
    for entry in screen['paths']:
        if entry['lane'] != 'D01_J946' or entry['rejected']:
            continue
        i = entry['index']
        row = {'index': i, 'ribbon_completion_obstructed': False, 'component_pairs': [],
               'origin': origins.get(i)}
        link = snappy.Link(front['frontier'][i]['endpoint_pd'])
        for ci in range(len(link.link_components)):
            component = link.sublink([ci])
            component.simplify('basic')
            if not component.crossings:
                continue
            factors = component.deconnect_sum()
            if len(factors) == 2:
                keys = [factor_data(f) for f in factors]
                A, B = [record['factors'][k] for k in keys]
                obstructed = bool(A['eligible'] and B['eligible'] and
                                  A['Jones'] != sorted([[-e, n] for e, n in B['Jones']]))
                row['component_pairs'].append({'component': ci, 'factors': keys, 'obstructed': obstructed})
                row['ribbon_completion_obstructed'] |= obstructed
        record['rows'].append(row)
        destination.write_text(json.dumps(record, separators=(',', ':')) + '\n')
    record.update(complete=True, additional_excluded=sum(r['ribbon_completion_obstructed'] for r in record['rows']),
                  retained_unknown=sum(not r['ribbon_completion_obstructed'] for r in record['rows']))
    destination.write_text(json.dumps(record, separators=(',', ':')) + '\n')
    print(json.dumps({k: record[k] for k in ['additional_excluded', 'retained_unknown', 'square_sum_control_passed']}))


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
