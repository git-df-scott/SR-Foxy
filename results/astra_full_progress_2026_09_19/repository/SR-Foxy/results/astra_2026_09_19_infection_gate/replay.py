#!/usr/bin/env python3
"""Replay the pinned Whitehead-stabilizer experiment; never certify a CE.

Requires the pinned packages in requirements.txt. Writes a complete distinct-band
ledger and fresh report to --out; it does not change the repository or its inputs.
The diagram libraries and HFK implementation remain trusted dependencies.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
import hashlib
import importlib.metadata
import json
from pathlib import Path
import random
import sys
import time

import regina
import sympy as sp
from sympy.polys.matrices import DomainMatrix
from spherogram import Link
from spherogram.links.bands.core import (
    add_one_band, normalize_crossing_labels, simple_bands,
)

PRIME = 1000003
X = sp.Symbol('t')
D_COEFF = [1, -3, 5, -3, 1]
D_PD = [[18,21,19,22],[22,26,23,25],[28,24,29,23],[24,30,25,29],
        [26,19,27,20],[20,27,21,28],[30,35,31,36],[44,16,45,15],
        [13,43,14,42],[8,45,9,46],[4,44,5,43],[7,33,8,32],
        [1,37,2,36],[47,39,48,38],[39,47,40,46],[40,31,41,32],
        [33,7,34,6],[34,41,35,42],[14,5,15,6],[48,9,49,10],
        [16,12,17,11],[3,12,4,13],[17,3,18,2],[10,49,11,0],[37,1,38,0]]
EXPECTED = {'small': {'distinct_mixed': 544, 'linking_exclusions': 439,
                     'rank_zero_exclusions': 105, 'necessary_passes': 0},
            'wider': {'distinct_mixed': 8106, 'linking_exclusions': 6703,
                      'rank_zero_exclusions': 1383, 'necessary_passes': 20}}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def as_regina(knot: Link):
    return regina.Link.fromPD([[a + 1 for a in c] for c in knot.PD_code()])


def diagram_signature(knot: Link) -> str:
    # Positive equality only. Inequality does not distinguish knot types.
    return as_regina(knot).sig(True, True, True) if knot.crossings else 'unknot'


def rank_mod_p(rows: list[list[int]], ncols: int) -> int:
    a = [[v % PRIME for v in row] for row in rows]
    r = 0
    for c in range(ncols):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inverse = pow(a[r][c], -1, PRIME)
        a[r] = [v * inverse % PRIME for v in a[r]]
        for i in range(r + 1, len(a)):
            coefficient = a[i][c]
            if coefficient:
                for j in range(c, ncols):
                    a[i][j] = (a[i][j] - coefficient * a[r][j]) % PRIME
        r += 1
        if r == len(a):
            break
    return r


def wirtinger_ports(link: Link):
    pieces = link._pieces()
    ports = {(c, p): i for i, piece in enumerate(pieces) for c, p in piece}
    n = len(pieces)
    for component in link.link_components:
        # Components entirely over other components have no underpass pieces.
        if not any(cs.strand_index == 0 for cs in component):
            for cs in component:
                ports[cs.crossing, cs.strand_index] = n
                ports[cs.crossing, (cs.strand_index + 2) % 4] = n
            n += 1
    n += link.unlinked_unknot_components
    return ports, n


def alexander_rank_upper_bound(link: Link) -> int:
    """Bound the MULTIVARIATE Alexander rank, not an invariant at one t.

    This evaluates every component variable at 2 in F_1000003. A nonzero
    specialized minor proves the corresponding integral multivariate minor is
    nonzero. H_1 of the abelian cover has rank n-1-rank(Fox). A bound of zero
    excludes a strongly slice two-component link; a bound of one proves nothing
    positive about sliceness, nor even equality of the generic rank to one.
    """
    ports, n = wirtinger_ports(link)
    rows = []
    for c in link.crossings:
        i, j, k = ports[c, 0] + 1, ports[c, 2] + 1, ports[c, 1] + 1
        require(ports[c, 1] == ports[c, 3], 'Overpass arc inconsistency')
        word = [-k, i, k, -j] if c.sign > 0 else [k, i, -k, -j]
        row, power = [0] * n, 0
        for letter in word:
            if letter > 0:
                row[letter - 1] = (row[letter - 1] + pow(2, power, PRIME)) % PRIME
                power += 1
            else:
                power -= 1
                row[-letter - 1] = (row[-letter - 1] - pow(2, power, PRIME)) % PRIME
        require(power == 0 and sum(row) % PRIME == 0, 'Fox identity failed')
        rows.append(row)
    bound = n - 1 - rank_mod_p(rows, n)
    require(bound >= 0, 'Negative Alexander-rank bound')
    return bound


def linking_number(link: Link) -> int:
    value = sum(c.sign for c in link.crossings
                if c.strand_components[0] != c.strand_components[1])
    require(value % 2 == 0, 'Odd signed mixed-crossing sum')
    return value // 2


def normalized_polynomial(expression):
    p = sp.Poly(expression, X)
    require(not p.is_zero, 'Zero polynomial where a knot polynomial was expected')
    low = min(m[0] for m, _ in p.terms())
    return sp.Poly(sp.cancel(p.as_expr() / X**low), X).monic()


def alexander_from_fox(knot: Link):
    if not knot.crossings:
        return sp.Poly(1, X)
    require(len(knot.link_components) == 1, 'Fox determinant input is not a knot')
    ports, n = wirtinger_ports(knot)
    require(n == len(knot.crossings), 'Unexpected knot Wirtinger presentation')
    matrix = sp.zeros(n)
    for r, c in enumerate(knot.crossings):
        i, j, k = ports[c, 0], ports[c, 2], ports[c, 1]
        coefficients = [(i, 1), (j, -X), (k, X - 1)] if c.sign > 0 else [
            (i, X), (j, -1), (k, 1 - X)]
        for column, value in coefficients:
            matrix[r, column] += value
    return normalized_polynomial(DomainMatrix.from_Matrix(matrix[:-1, :-1]).det().as_expr())


def passes_norm_factor_condition(p) -> bool:
    # Necessary over Q; passing is not an integral norm or slice certificate.
    _, factors = sp.factor_list(p)
    multiplicities = {tuple(f.monic().all_coeffs()): e for f, e in factors}
    for f, e in factors:
        key = tuple(f.monic().all_coeffs())
        reciprocal = tuple(sp.Poly.from_list(list(reversed(key)), X).monic().all_coeffs())
        if (key == reciprocal and e % 2) or (key != reciprocal and multiplicities.get(reciprocal) != e):
            return False
    return True


def checked_hfk(knot: Link, modulus: int = 2):
    h = Link(knot.PD_code()).knot_floer_homology(prime=modulus)
    ranks = h['ranks']
    require(all(ranks.get((-a, m - 2*a), 0) == v for (a, m), v in ranks.items()),
            'HFK output failed conjugation symmetry: quarantine, do not use')
    euler = Counter()
    for (a, m), value in ranks.items():
        euler[a] += value * (-1 if m % 2 else 1)
    euler = {a: value for a, value in euler.items() if value}
    lo, hi = min(euler), max(euler)
    p = normalized_polynomial(sum(value * X**(a-lo) for a, value in euler.items()))
    h['alexander_Q_monic_coefficients'] = [str(v) for v in p.all_coeffs()]
    h['ranks'] = {str(k): v for k, v in ranks.items()}
    return h


def check_controls():
    require(sp.isprime(PRIME), 'Rank modulus is not prime')
    square = Link(braid_closure=[1, 1, 1, -2, -2, -2])
    parallel = Link(as_regina(square).parallel(2).pdData())
    unlink = Link([])
    unlink.unlinked_unknot_components = 2
    controls = [('unlink2', unlink, 1), ('Hopf', Link('L2a1'), 0),
                ('Whitehead', Link('L5a1'), 0), ('zero_parallel_square', parallel, 1)]
    report = {}
    for name, link, expected in controls:
        report[name] = alexander_rank_upper_bound(link)
        require(report[name] == expected, 'Rank control failed: ' + name)
    for name, expected in [('3_1', False), ('6_3', False), ('6_1', True)]:
        value = passes_norm_factor_condition(alexander_from_fox(Link(name)))
        require(value == expected, 'Fox norm control failed: ' + name)
    require(passes_norm_factor_condition(alexander_from_fox(square)), 'Square norm control failed')
    return report


def build_targets(out: Path):
    square = Link(braid_closure=[1, 1, 1, -2, -2, -2])
    whitehead = Link(as_regina(square).whiteheadDouble(positive=True).pdData())
    d = Link(D_PD)
    target = d.connected_sum(whitehead)
    objects = {'R': square, 'J': whitehead, 'D': d, 'T': target}
    info = {}
    for name, knot in objects.items():
        h = checked_hfk(knot)
        require(len(knot.link_components) == 1, 'Construction not a knot')
        if name != 'T':
            p = alexander_from_fox(knot)
            require(h['alexander_Q_monic_coefficients'] == [str(v) for v in p.all_coeffs()],
                    'Independent Fox/HFK mismatch for ' + name)
        info[name] = {'pd': knot.PD_code(), 'diagram_crossings': len(knot.crossings), 'hfk': h}
    parsed = {name: {ast.literal_eval(k): v for k, v in info[name]['hfk']['ranks'].items()}
              for name in ['D', 'J', 'T']}
    product = Counter()
    for (a, m), v in parsed['D'].items():
        for (b, n), w in parsed['J'].items():
            product[a+b, m+n] += v*w
    require(dict(product) == parsed['T'], 'Full bigraded Kunneth identity failed')
    require([info[n]['diagram_crossings'] for n in ['R','J','D','T']] == [6,26,25,51],
            'Library diagram generation changed; do not reuse the saved search bounds')
    (out/'TARGETS.json').write_text(json.dumps(info, indent=2)+'\n')
    return target, d


def cheap_test_control(out: Path):
    k = Link('12n382')
    h2, h3 = checked_hfk(k, 2), checked_hfk(k, 3)
    v = sp.Matrix(k.seifert_matrix())
    p = normalized_polynomial(DomainMatrix.from_Matrix(v-X*v.T).det().as_expr())
    expected = [1,-5,7,-5,1]
    require(p.all_coeffs() == expected and p.is_irreducible, '12n382 polynomial control failed')
    for h in [h2, h3]:
        require(h['seifert_genus'] == 2 and not h['fibered'] and h['total_rank'] == 35,
                '12n382 HFK control failed')
        require(h['alexander_Q_monic_coefficients'] == [str(a) for a in expected],
                '12n382 independent determinant mismatch')
        require(sum(value for key, value in h['ranks'].items() if ast.literal_eval(key)[0] == 2) == 3,
                '12n382 top grading mismatch')
    result = {'name': '12n382', 'pd': k.PD_code(), 'HFK_F2': h2, 'HFK_F3': h3,
              'seifert_matrix': [list(map(int, v.row(i))) for i in range(v.rows)],
              'alexander_coefficients_high_to_low': expected,
              'scope': 'Prime nonfibered cheap-test control; tau=1, NOT a slice candidate.'}
    (out/'CONTROL.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


def screen(target: Link, twists: int, length: int):
    link = Link(target.PD_code())
    normalize_crossing_labels(link)
    bands = simple_bands(link, max_twists=twists, max_band_len=length)
    mixed = [b for b in bands if (b.cs_along_top[0][0] < len(D_PD)) !=
             (b.cs_along_top[-1][0] < len(D_PD))]
    unique = {b.compressed_spec(): b for b in mixed}
    counts = {'distinct_mixed': len(unique), 'linking_exclusions': 0,
              'rank_zero_exclusions': 0, 'necessary_passes': 0}
    ledger, survivors = [], []
    for spec, band in sorted(unique.items()):
        after = add_one_band(link, band)
        require(len(after.link_components) == 2, 'Band did not produce two components')
        linking = linking_number(after)
        bound = None
        if linking:
            counts['linking_exclusions'] += 1
        else:
            bound = alexander_rank_upper_bound(after)
            if bound == 0:
                counts['rank_zero_exclusions'] += 1
            else:
                counts['necessary_passes'] += 1
                after.simplify('basic')
                survivors.append({'band': spec, 'pd': after.PD_code(),
                                  'removed_unknot_components': after.unlinked_unknot_components})
        ledger.append([spec, linking, bound])
    return {'raw_generated': len(bands), 'raw_mixed': len(mixed), 'counts': counts,
            'ledger': ledger, 'survivors': survivors}


def inspect_survivor(row: dict, d_signature: str):
    link = Link(row['pd'])
    components, flags = [], set()
    for index in range(len(link.link_components)):
        k = link.sublink(index)
        k.simplify('basic')
        record = {'component': index, 'pd': k.PD_code(), 'crossings': len(k.crossings)}
        record['exact_D_diagram_up_to_mirror'] = diagram_signature(k) == d_signature
        if record['exact_D_diagram_up_to_mirror']:
            flags.add('D_diagram')
        if len(k.crossings) <= 30:
            p = alexander_from_fox(k)
            record['alexander_Q_monic_coefficients'] = [str(v) for v in p.all_coeffs()]
            record['norm_factor_condition'] = passes_norm_factor_condition(p)
            if not record['norm_factor_condition']:
                flags.add('Fox_Milnor')
        components.append(record)
    if not flags:
        for component in components:
            k = Link(component['pd'])
            if not k.crossings:
                continue
            factors = k.deconnect_sum()
            if len(factors) != 2:
                continue
            tests = []
            for factor in factors:
                factor.simplify('basic')
                if not factor.crossings:
                    continue
                h = checked_hfk(factor)
                p = alexander_from_fox(factor)
                require(h['alexander_Q_monic_coefficients'] == [str(v) for v in p.all_coeffs()],
                        'Factor Fox/HFK mismatch')
                jones = as_regina(factor).jones()
                tests.append({'pd': factor.PD_code(), 'hfk': h,
                              'alexander_coefficients': [str(v) for v in p.all_coeffs()],
                              'jones': str(jones), 'jones_sqrt_variable_span': jones.maxExp()-jones.minExp()})
            component['factor_tests'] = tests
            if len(tests) == 2 and all(q['hfk']['fibered'] and
                 q['alexander_coefficients'] == [str(v) for v in D_COEFF] for q in tests) and \
                 tests[0]['jones_sqrt_variable_span'] != tests[1]['jones_sqrt_variable_span']:
                flags.add('Miyazaki_distinct_prime_fibered_factors')
    return {'band': row['band'], 'components': components,
            'prefix_exclusion_reasons': sorted(flags), 'ribbon_prefix_excluded': bool(flags)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--skip-hfk', action='store_true', help='Replay only band counts; do not claim HFK/control/factor certificates.')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    require(not any(args.out.iterdir()), '--out must be empty to avoid overwriting prior evidence')
    start = time.monotonic()
    random.seed(0)
    versions = {package: importlib.metadata.version(package) for package in
                ['spherogram', 'snappy', 'regina', 'knot_floer_homology', 'sympy']}
    controls = check_controls()
    if args.skip_hfk:
        square = Link(braid_closure=[1,1,1,-2,-2,-2])
        d = Link(D_PD)
        target = d.connected_sum(Link(as_regina(square).whiteheadDouble(positive=True).pdData()))
    else:
        target, d = build_targets(args.out)
        cheap_test_control(args.out)
    reports = {}
    for name, twists, length in [('small',1,3), ('wider',3,4)]:
        report = screen(target, twists, length)
        require(report['counts'] == EXPECTED[name], 'Pinned band counts changed: '+name)
        reports[name] = report
        (args.out/(name.upper()+'_BANDS.json')).write_text(json.dumps(report, indent=2)+'\n')
        print(name, report['counts'], flush=True)
    prefixes = []
    if not args.skip_hfk:
        for row in reports['wider']['survivors']:
            result = inspect_survivor(row, diagram_signature(d))
            prefixes.append(result)
            print(row['band'], result['prefix_exclusion_reasons'], flush=True)
        require(sum(r['ribbon_prefix_excluded'] for r in prefixes) == 19, 'Prefix exclusion count changed')
        require([r['band'] for r in prefixes if not r['ribbon_prefix_excluded']] == ['ca080502_0_-1'],
                'Remaining prefix changed')
        (args.out/'PREFIXES.json').write_text(json.dumps(prefixes, indent=2)+'\n')
    report = {'status': 'NO_COUNTEREXAMPLE_NO_DISK', 'target_slice_status': 'UNKNOWN',
              'target_ribbon_status': 'UNKNOWN', 'versions': versions,
              'rank_controls': controls, 'counts': {k:v['counts'] for k,v in reports.items()},
              'prefixes_excluded': sum(r['ribbon_prefix_excluded'] for r in prefixes) if prefixes else None,
              'full_hfk_replay': not args.skip_hfk, 'seconds': time.monotonic()-start,
              'scope': 'One pinned 51-crossing diagram and these generated bands only; no isotopy or all-band exhaustion.'}
    (args.out/'REPORT.json').write_text(json.dumps(report, indent=2)+'\n')
    manifest = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(args.out.iterdir()) if p.is_file()}
    (args.out/'MANIFEST.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
