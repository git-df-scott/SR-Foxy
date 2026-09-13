#!/usr/bin/env python3
"""Necessary graded Khovanov inequalities for common ribbon upper knots.

Levine--Zemke, Theorem 1, arXiv:1903.01546v2. Unreduced Khovanov homology
of EACH predecessor must inject bigrading by bigrading. Validate the Euler
characteristic independently with Regina's Jones polynomial and retain the
known K0 -> J movies as positive controls. Unknown calculations never pass.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time
import regina
import snappy


def parse_poincare(text, field=2):
    prefix = ('Rational unreduced Khovanov Homology : ' if field == 1
              else 'Unreduced Khovanov Homology mod ' + str(field) + ' : ')
    lines = [line[len(prefix):].strip() for line in text.splitlines() if line.startswith(prefix)]
    if len(lines) != 1 or not lines[0]:
        raise ValueError('Expected exactly one nonempty unreduced polynomial: ' + prefix)
    ranks = Counter()
    for term in lines[0].split(' + '):
        coefficient, degrees, seen = 1, {'t': 0, 'q': 0}, set()
        for token in term.split():
            if re.fullmatch(r'[1-9][0-9]*', token) and 'coefficient' not in seen:
                coefficient = int(token); seen.add('coefficient')
            else:
                m = re.fullmatch(r'([tq])(?:\^(-?[0-9]+))?', token)
                if not m or m[1] in seen:
                    raise ValueError('Unrecognized polynomial token: ' + token)
                seen.add(m[1]); degrees[m[1]] = int(m[2]) if m[2] else 1
        ranks[degrees['t'], degrees['q']] += coefficient
    return ranks


def euler_check(pd, ranks):
    actual = Counter()
    for (i, j), n in ranks.items():
        actual[j] += n * (-1 if i % 2 else 1)
    P = regina.Link.fromPD([[a + 1 for a in c] for c in pd]).jones()
    expected = Counter()
    # Regina x -> -q gives normalized Jones; unreduced Euler adds q+q^-1.
    for e in range(P.minExp(), P.maxExp() + 1):
        coefficient = int(str(P[e])) * (-1 if e % 2 else 1)
        expected[e + 1] += coefficient; expected[e - 1] += coefficient
    compact = lambda x: sorted([[k, v] for k, v in x.items() if v])
    return {'passed': compact(actual) == compact(expected),
            'khovanov_euler': compact(actual), 'regina_unreduced_jones': compact(expected)}


def deficits(lower, upper):
    return [[i, j, n, upper.get((i, j), 0)] for (i, j), n in sorted(lower.items())
            if upper.get((i, j), 0) < n]


def run(a):
    out = Path(a.output); out.mkdir(parents=True, exist_ok=False)
    raw = Path(a.targets).read_bytes()
    targets = json.loads(raw)['candidates']
    inputs = []
    for name, file in [('K0', 'AbeTagami_K_0_K_-1__6_3'), ('K1', 'AbeTagami_K_1')]:
        inputs.append((name, json.loads(Path('data/knots/' + file + '.json').read_text())['pd_code_snappy_0indexed'], None))
    for name, knot in [('trefoil', '3_1'), ('ribbon_6_1', '6_1')]:
        inputs.append((name, snappy.Link(knot).PD_code(), None))
    inputs += [('J' + str(r['index']), r['endpoint_pd'], r['index']) for r in targets if not r['hfk_check']['fibered']]
    rec = {'status': 'GRADED_KHOVANOV_NECESSARY_CONDITION_ONLY', 'parameters': vars(a),
           'input_sha256': hashlib.sha256(raw).hexdigest(),
           'jar_sha256': hashlib.sha256(Path(a.jar).read_bytes()).hexdigest(),
           'source': 'https://arxiv.org/html/1903.01546v2', 'theorem': 'Theorem 1',
           'coefficient_field': 'Q' if a.field == 1 else 'F' + str(a.field), 'flavor': 'unreduced even',
           'grading_order': ['homological', 'quantum'], 'runs': [], 'complete': False}
    control_ranks = {}
    def save():
        (out / 'manifest.json').write_text(json.dumps(rec, indent=2) + '\n')
    save()
    for name, pd, index in inputs:
        path = out / (name + '.txt')
        path.write_text(name + ' = PD[' + ','.join('X[' + ','.join(str(k + 1) for k in c) + ']' for c in pd) + ']\n')
        row = {'name': name, 'source_index': index, 'pd': pd}
        started = time.monotonic()
        try:
            job = subprocess.run([a.java, '-Xmx2g', '-Djava.awt.headless=true', '-jar', a.jar,
                                  str(path), '-ku' + str(a.field), '-nf'], capture_output=True, text=True,
                                 timeout=a.timeout, check=True)
            (out / (name + '.log')).write_text(job.stdout + job.stderr)
            ranks = parse_poincare(job.stdout, a.field)
            row['ranks'] = [[i, j, n] for (i, j), n in sorted(ranks.items())]
            row['total_rank'] = sum(ranks.values())
            row['euler_validation'] = euler_check(pd, ranks)
            if not row['euler_validation']['passed']:
                raise AssertionError('Independent Jones/Euler check failed')
            row['status'] = 'computed_and_euler_checked'
            if index is None:
                control_ranks[name] = ranks
            else:
                row['K0_deficits'] = deficits(control_ranks['K0'], ranks)
                row['K1_deficits'] = deficits(control_ranks['K1'], ranks)
                if row['K0_deficits']:
                    raise AssertionError('Known forward K0 ribbon movie violates inequality')
                row['K0_positive_control'] = True
                row['K1_ribbon_predecessor_obstructed'] = bool(row['K1_deficits'])
        except AssertionError:
            rec['runs'].append(row); rec['status'] = 'VALIDATION_FAILURE'; save(); raise
        except Exception as e:
            row['status'] = 'inconclusive'; row['error'] = type(e).__name__ + ': ' + str(e)
            if index is None:
                rec['runs'].append(row); save(); raise
        row['seconds'] = round(time.monotonic() - started, 3)
        rec['runs'].append(row); save()
        print(json.dumps({k: row[k] for k in ['name', 'status', 'seconds', 'total_rank', 'K1_ribbon_predecessor_obstructed'] if k in row}), flush=True)
    rec['complete'] = True; save()


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('java'); p.add_argument('jar'); p.add_argument('targets'); p.add_argument('output')
    p.add_argument('--timeout', type=float, default=60)
    p.add_argument('--field', type=int, choices=[1, 2, 3, 5], default=2, help='1 means rational coefficients')
    run(p.parse_args())
