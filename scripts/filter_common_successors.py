#!/usr/bin/env python3
"""Necessary bigraded HFK test for a common ribbon successor (Zemke Thm 1.2).

This is a rejection filter, never a certificate of concordance. A failure of
the source-to-endpoint check invalidates the generated-movie interpretation.
Samples are reproducible; timeouts/errors are inconclusive, never rejections.
"""
import argparse
import gzip
import json
from pathlib import Path
import random
import signal
import time

import snappy


def rows(ranks):
    return [[int(a), int(m), int(n)] for (a, m), n in sorted(ranks.items())]


def dominates(actual, required):
    return all(actual.get(k, 0) >= n for k, n in required.items())


def missing(actual, required):
    return rows({k: n - actual.get(k, 0) for k, n in required.items()
                 if n > actual.get(k, 0)})


def read_unique(path):
    opener = gzip.open if str(path).endswith('.gz') else open
    with opener(path, 'rt') as f:
        return [r for line in f if (r := json.loads(line)).get('new_signature')]


def expired(signum, frame):
    raise TimeoutError('HFK time limit')


def run(paths, cards, output, sample=256, seed=20260912, timeout=20):
    if Path(output).exists():
        raise FileExistsError(output)
    source_hfk = []
    for card in cards:
        d = json.loads(Path(card).read_text())
        source_hfk.append(snappy.Link(d['pd_code_snappy_0indexed']).knot_floer_homology())
    required = {}
    for h in source_hfk:
        for k, v in h['ranks'].items():
            required[k] = max(required.get(k, 0), v)
    result = {'source_cards': list(map(str, cards)), 'source_ranks': [rows(h['ranks']) for h in source_hfk],
              'required_ranks': rows(required), 'minimum_total_rank': sum(required.values()),
              'source': 'Ian Zemke, arXiv:1902.04050, Theorem 1.2',
              'seed': seed, 'sample_per_side': sample, 'timeout_per_case_seconds': timeout,
              'snappy': snappy.__version__, 'sides': [],
              'meaning': 'Necessary condition only; passing does not imply concordance.'}
    signal.signal(signal.SIGALRM, expired)
    for side, path in enumerate(paths):
        t0 = time.monotonic()
        candidates = read_unique(path)
        rng = random.Random(seed + side)
        if sample and len(candidates) > sample:
            candidates = rng.sample(candidates, sample)
        checks = []
        for i, r in enumerate(candidates):
            out = {'index': r['index'], 'diagram_signature': r['diagram_signature'],
                   'crossings': r['crossings']}
            try:
                signal.setitimer(signal.ITIMER_REAL, timeout)
                h = snappy.Link(r['endpoint_pd']).knot_floer_homology()
                signal.setitimer(signal.ITIMER_REAL, 0)
                out.update({'status': 'computed', 'ranks': rows(h['ranks']),
                            'total_rank': h['total_rank'], 'tau': h['tau'],
                            'genus': h['seifert_genus'], 'fibered': h['fibered'],
                            'own_source_injection_passed': dominates(h['ranks'], source_hfk[side]['ranks']),
                            'common_successor_not_excluded': dominates(h['ranks'], required),
                            'missing_required_ranks': missing(h['ranks'], required)})
            except Exception as e:
                signal.setitimer(signal.ITIMER_REAL, 0)
                out.update({'status': 'inconclusive', 'error': type(e).__name__ + ': ' + str(e)})
            checks.append(out)
            if (i+1) % 64 == 0:
                print(json.dumps({'side': side, 'checked': i+1}), flush=True)
        computed = [c for c in checks if c['status'] == 'computed']
        summary = {'input': str(path), 'attempted': len(checks), 'computed': len(computed),
                   'own_source_injection_failures': sum(not c['own_source_injection_passed'] for c in computed),
                   'not_excluded': sum(c['common_successor_not_excluded'] for c in computed),
                   'seconds': round(time.monotonic()-t0, 3), 'checks': checks}
        result['sides'].append(summary)
        print(json.dumps({k:v for k,v in summary.items() if k != 'checks'}), flush=True)
    Path(output).write_text(json.dumps(result, indent=2) + '\n')
    if any(s['own_source_injection_failures'] for s in result['sides']):
        raise AssertionError('Stop using the movie generator: a source injection check failed')
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('output')
    p.add_argument('--inputs', nargs=2, required=True)
    p.add_argument('--cards', nargs=2, default=['data/knots/AbeTagami_K_0_K_-1__6_3.json', 'data/knots/AbeTagami_K_1.json'])
    p.add_argument('--sample', type=int, default=256, help='0 means all unique diagrams')
    p.add_argument('--seed', type=int, default=20260912)
    a = p.parse_args()
    run(a.inputs, a.cards, a.output, a.sample, a.seed)
