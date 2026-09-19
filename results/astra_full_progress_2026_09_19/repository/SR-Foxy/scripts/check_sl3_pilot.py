#!/usr/bin/env python3
"""Check completed sl3 pilot outputs against independent HOMFLY polynomials.

The two target calculations timed out. This script makes no obstruction
claim from missing data. KnotJob's sl3 quantum convention uses alpha=q^-3
in Regina's HOMFLY(alpha,z), with z=q-q^-1 and unknot value [3].
"""
from collections import Counter
import json
import math
from pathlib import Path
import re
import regina
from khovanov_upper_filter import parse_poincare


def expected_euler(pd):
    text = str(regina.Link.fromPD([[a + 1 for a in c] for c in pd]).homflyAZ())
    answer = Counter()
    for term in text.replace(' - ', ' + -').split(' + '):
        coefficient, x, y = 1, 0, 0
        if term.startswith('-'):
            coefficient = -1; term = term[1:]
        for token in term.split():
            if token.isdigit():
                coefficient *= int(token)
            else:
                m = re.fullmatch(r'([xy])(?:\^(-?\d+))?', token)
                if not m: raise ValueError(token)
                power = int(m[2]) if m[2] else 1
                if m[1] == 'x': x = power
                else: y = power
        if y < 0: raise ValueError('This pilot handles knot polynomials with nonnegative z exponents')
        for k in range(y + 1):
            for shift in [-2, 0, 2]:
                answer[-3*x + y - 2*k + shift] += coefficient * math.comb(y, k) * (-1)**k
    return text, sorted([[j, v] for j, v in answer.items() if v])


def run():
    base = Path('results/nonfibered_sl3_pilot')
    d = json.loads((base / 'manifest.json').read_text())
    inputs = {r['name']: r for r in json.loads(Path('results/nonfibered_khovanov_filter/manifest.json').read_text())['runs']}
    checks = []
    for r in d['runs']:
        if r['status'] != 'finished':
            checks.append({'name': r['name'], 'status': 'inconclusive_' + r['status']}); continue
        text = (base / (r['name'] + '.log')).read_text()
        prefix = 'Unreduced integral sl_3 Homology : '
        line = next(line for line in text.splitlines() if line.startswith(prefix))
        ranks = parse_poincare(line.replace(prefix, 'Unreduced Khovanov Homology mod 2 : '))
        actual = Counter()
        for (i, j), n in ranks.items(): actual[j] += n * (-1 if i % 2 else 1)
        poly, expected = expected_euler(inputs[r['name']]['pd'])
        assert sorted([[j, v] for j, v in actual.items() if v]) == expected
        checks.append({'name': r['name'], 'status': 'free_ranks_and_euler_checked',
                       'total_rational_rank': sum(ranks.values()),
                       'rational_ranks': [[i, j, n] for (i, j), n in sorted(ranks.items())],
                       'HOMFLY_alpha_z': poly, 'Euler': expected})
    result = {'status': 'TARGET_SL3_CALCULATIONS_INCONCLUSIVE',
              'quantum_convention': 'Regina alpha=q^-3, z=q-q^-1; multiply normalized HOMFLY by q^2+1+q^-2.',
              'grading_note': 'The sl3 output convention differs from the even sl2 output; do not compare their bidegrees directly.',
              'checks': checks, 'obstructions': []}
    (base / 'checked.json').write_text(json.dumps(result, indent=2) + '\n')
    print([(r['name'], r['status']) for r in checks])


if __name__ == '__main__': run()
