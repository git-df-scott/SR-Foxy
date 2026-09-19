#!/usr/bin/env python3
"""Bounded component screen; no failed calculation is an obstruction.

Run from repository root, passing the pinned Opus frontier JSON path.
This checks components, not the existence of a ribbon completion.
"""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, sys
from pathlib import Path
import snappy, sympy
from component_guided_bands import parts, jones
from fusion_successors import diagram_signature
from nonfibered_reverse_audit import hfk
from teichner_component_slice_gate import norm_test, T
from fission_ancestry_audit import determinant


def main():
    source = Path(sys.argv[1])
    local = Path('results/teichner_D01_J946_component_filtered_continuation.json')
    out = Path('results/september14_frontier_components.json')
    if out.exists(): raise FileExistsError(out)
    opus = json.loads(source.read_text())
    local_data = json.loads(local.read_text())
    cache, paths = {}, []
    for lane, entries in [('D01_J946', local_data['frontier']),
                          ('RBG_KG', opus['diagrams'][0]['frontier'])]:
        for i, row in enumerate(entries):
            pd = row['endpoint_pd'] if lane == 'D01_J946' else row['certificate'][-1]
            keys = []
            for component in parts(snappy.Link(pd)):
                key = diagram_signature(component.PD_code()) if component.crossings else 'U'
                cache.setdefault(key, {'pd': component.PD_code()})
                keys.append(key)
            paths.append({'lane': lane, 'index': i, 'components': keys})

    def compute(item):
        key, row = item
        if key == 'U':
            return key, dict(row, status='known_unknot', rejections=[])
        row['rejections'] = []
        try:
            V = sympy.Matrix(snappy.Link(row['pd']).seifert_matrix())
            det = abs(int((V + V.T).det(method='domain-ge')))
            # Separate Jones implementation checks the determinant.
            assert det == determinant(jones(snappy.Link(row['pd'])))
            row['determinant'] = det
            from math import isqrt
            if isqrt(det)**2 != det:
                row['rejections'] = ['determinant_not_square']
                row['status'] = 'checked'
                return key, row
            H = hfk(row['pd'])
            coeff = Counter()
            for A, M, n in H['ranks']:
                coeff[A] += n * (-1 if M % 2 else 1)
            coeff = {a: n for a, n in coeff.items() if n}
            lo = min(coeff)
            P = sympy.Poly(sum(n*T**(a-lo) for a,n in coeff.items()), T)
            if P.eval(1) == -1: P = -P
            assert P.eval(1) == 1 and abs(int(P.eval(-1))) == det
            # Assign HFK-derived obstructions only AFTER its consistency checks.
            failures = []
            if H['tau'] != 0: failures.append('tau_nonzero')
            if not any(A == M == 0 and n for A,M,n in H['ranks']):
                failures.append('ribbon_HFK_unknot_injection_fails')
            norm_failures = norm_test(P)
            if norm_failures: failures.append('Fox_Milnor_norm_fails')
            row.update(status='checked', HFK=H, rejections=failures,
                       alexander_coefficients_low_to_high=[int(P.nth(i)) for i in range(P.degree()+1)],
                       norm_failure_witnesses=norm_failures)
        except Exception as e:
            row.update(status='UNKNOWN', error=repr(e), rejections=[])
        return key, row

    assert not norm_test(sympy.Poly((T*T-3*T+1)**2, T))
    assert norm_test(sympy.Poly(T*T-3*T+1, T))
    assert not norm_test(sympy.Poly((2*T-1)*(2-T), T))
    print('unique components', len(cache), flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        cache = dict(pool.map(compute, cache.items()))
    summary = {}
    for row in paths:
        row['rejected'] = any(cache[k]['rejections'] for k in row['components'])
    for lane in ['D01_J946', 'RBG_KG']:
        group = [r for r in paths if r['lane'] == lane]
        summary[lane] = {'input_paths': len(group), 'rejected': sum(r['rejected'] for r in group),
                         'retained_unknown': sum(not r['rejected'] for r in group)}
    rec = {'complete': True, 'opus_commit': '345f73ef5aebd1e9c833f177217f2c1b72f08120',
           'input_hashes': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in [source, local]},
           'components': cache, 'paths': paths, 'summary': summary,
           'unknown_calculations': sum(r['status'] == 'UNKNOWN' for r in cache.values()),
           'scope': 'Component obstructions to pure-fission ribbon completion only; passing is inconclusive. Opus certificate transitions require a separate replay audit.'}
    out.write_text(json.dumps(rec, separators=(',', ':')) + '\n')
    print(json.dumps(summary), 'unknown', rec['unknown_calculations'], flush=True)


if __name__ == '__main__': main()
