#!/usr/bin/env python3
"""Independently check saved finite-matrix certificates using only Python stdlib.

This checks the algebra and the supplied Tietze maps; identifying the marked
presentation with the input link still relies on SnapPy and the diagram audit.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def product(a, b, p):
    return tuple(sum(a[2*r+k]*b[2*k+c] for k in range(2)) % p
                 for r in range(2) for c in range(2))


def inv(a, p):
    return (a[3], -a[1] % p, -a[2] % p, a[0])


def word_value(word, values, p):
    factors = [values[x-1] if x > 0 else inv(values[-x-1], p) for x in word]
    value = (1, 0, 0, 1)
    for factor in factors:
        value = product(value, factor, p)
    return value


def trace(a, p):
    return (a[0]+a[3]) % p


def check_record(record):
    for presentation in (record['simplified'], record['original']):
        names = presentation['generators']
        assert all(len(name) == 1 and name.islower() for name in names)
        indices = {name: i+1 for i, name in enumerate(names)}
        def encode(word):
            return [indices[x.lower()] * (1 if x.islower() else -1) for x in word]
        assert [encode(w) for w in presentation['relators']] == presentation['relator_letters']
        assert [[encode(w) for w in pair] for pair in presentation['peripheral_words']] == presentation['peripheral_letters']
    w = record['witness']
    p = w['prime']
    assert p in (2, 3, 5)
    identity = (1, 0, 0, 1)
    group = [a for a in itertools.product(range(p), repeat=4)
             if (a[0]*a[3]-a[1]*a[2]) % p == 1]
    values = [tuple(a) for a in w['generator_images']]
    assert len(values) == len(record['simplified']['generators'])
    assert all((a[0]*a[3]-a[1]*a[2]) % p == 1 for a in values)
    for r in record['simplified']['relator_letters']:
        assert word_value(r, values, p) == identity, 'simplified relator failed'
    original_values = [word_value(r, values, p)
                       for r in record['original_generators_in_simplified']]
    assert len(original_values) == len(record['original']['generators'])
    for r in record['original']['relator_letters']:
        assert word_value(r, original_values, p) == identity, 'geometric relator failed'
    alphabet = {name: i+1 for i, name in enumerate(record['original']['generators'])}
    assert all(len(name) == 1 and name.islower() for name in alphabet)
    for i, word in enumerate(record['simplified_generators_in_original']):
        letters = [alphabet[x.lower()] * (1 if x.islower() else -1) for x in word]
        assert word_value(letters, original_values, p) == values[i], 'reverse generator map failed'
    peripheral_images = []
    peripheral_conjugators = []
    for cusp in range(3):
        simple = [word_value(r, values, p)
                  for r in record['simplified']['peripheral_letters'][cusp]]
        raw = [word_value(r, original_values, p)
               for r in record['original']['peripheral_letters'][cusp]]
        # SnapPy returns peripheral words only up to base-path conjugation.
        # Require one simultaneous conjugator for the meridian/longitude pair.
        conjugators = [a for a in group if all(
            product(product(a, x, p), inv(a, p), p) == y
            for x, y in zip(raw, simple))]
        assert conjugators, 'peripheral pair not simultaneously conjugate'
        peripheral_conjugators.append(conjugators[0])
        if cusp in (1, 2):
            assert simple[0] == identity, 'filled meridian not trivial'
        peripheral_images.append(simple)
    u, v = [peripheral_images[i][1] for i in (1, 2)]
    assert [u, v] == [tuple(a) for a in w['longitude_images']]
    assert [trace(u, p), trace(v, p)] == w['longitude_traces']
    assert trace(u, p) != trace(v, p), 'no trace obstruction'
    assert trace(inv(u, p), p) == trace(u, p)
    assert trace(inv(v, p), p) == trace(v, p)
    orbit = {product(product(a, u, p), inv(a, p), p) for a in group}
    assert v not in orbit and inv(v, p) not in orbit
    control = product(product(values[0], u, p), inv(values[0], p), p)
    assert control in orbit and trace(control, p) == trace(u, p)
    generated = {identity}
    pending = [identity]
    while pending:
        a = pending.pop()
        for b in values:
            c = product(a, b, p)
            if c not in generated:
                generated.add(c)
                pending.append(c)
    def order(a):
        b = identity
        for k in range(1, len(group)+1):
            b = product(b, a, p)
            if b == identity:
                return k
        raise AssertionError('matrix order exceeded group size')
    return {'seed': record['seed'], 'prime': p,
            'traces': [trace(u, p), trace(v, p)],
            'orders': [order(u), order(v)], 'image_group_order': len(generated),
            'ambient_group_order': len(group),
            'original_relators_checked': len(record['original']['relator_letters']),
            'peripheral_pair_conjugators': peripheral_conjugators,
            'conjugacy_and_inverse_excluded': True,
            'conjugate_positive_control': True}


def main():
    if not __debug__:
        raise RuntimeError('Run without -O: this certificate checker requires assertions.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', nargs='?', type=Path,
                        default=ROOT/'results/annulus_group_certificate.json')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    data = json.loads(args.certificate.read_text())
    assert hashlib.sha256((ROOT/data['input_path']).read_bytes()).hexdigest() == data['input_sha256']
    results = []
    for record in data['runs']:
        assert hashlib.sha256((ROOT/record['triangulation_path']).read_bytes()).hexdigest() == record['triangulation_sha256']
        results.append(check_record(record))
    report = {'all_checks_passed': True, 'runs': results,
              'limitation': 'Algebra independently checked; source link/group extraction shares SnapPy.'}
    output = json.dumps(report, indent=2)+'\n'
    if args.output:
        args.output.write_text(output)
    print(output, end='')


if __name__ == '__main__':
    main()
