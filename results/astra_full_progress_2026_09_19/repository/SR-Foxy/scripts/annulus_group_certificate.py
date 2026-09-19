#!/usr/bin/env python3
"""Exact finite-image obstruction for the marked Abe–Tagami surgery circles.

Generate with the repository knot venv; verify with ordinary Python using
check_annulus_group_certificate.py. No floating-point holonomy enters the proof.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

import snappy
from spherogram import Link

ROOT = Path(__file__).resolve().parents[1]
IDENTITY = (1, 0, 0, 1)


def multiply(x, y, p):
    a, b, c, d = x
    e, f, g, h = y
    return ((a*e+b*g) % p, (a*f+b*h) % p,
            (c*e+d*g) % p, (c*f+d*h) % p)


def inverse(x, p):
    a, b, c, d = x
    return (d, -b % p, -c % p, a)


def evaluate(word, generators, p):
    result = IDENTITY
    for letter in word:
        matrix = generators[abs(letter)-1]
        result = multiply(result, matrix if letter > 0 else inverse(matrix, p), p)
    return result


def matrices(p):
    return [x for x in itertools.product(range(p), repeat=4)
            if (x[0]*x[3]-x[1]*x[2]) % p == 1]


def presentation(group):
    return {
        'generators': group.generators(),
        'relators': group.relators(),
        'relator_letters': group.relators(as_int_list=True),
        'peripheral_letters': [[group.meridian(i, as_int_list=True),
                                group.longitude(i, as_int_list=True)]
                               for i in range(3)],
        'peripheral_words': group.peripheral_curves(),
    }


def find_witness(group):
    if group.num_generators() != 2:
        raise ValueError('This bounded search requires a two-generator presentation')
    relators = group.relators(as_int_list=True)
    words = [group.longitude(i, as_int_list=True) for i in (1, 2)]
    exhausted = []
    for p in (2, 3, 5):
        valid = 0
        for generators in itertools.product(matrices(p), repeat=2):
            if any(evaluate(r, generators, p) != IDENTITY for r in relators):
                continue
            valid += 1
            images = [evaluate(w, generators, p) for w in words]
            traces = [(x[0]+x[3]) % p for x in images]
            if traces[0] != traces[1]:
                return {
                    'prime': p, 'generator_images': generators,
                    'longitude_images': images, 'longitude_traces': traces,
                    'earlier_complete_trace_searches': exhausted,
                    'valid_representations_seen_at_witness_prime': valid,
                }
        exhausted.append({'prime': p, 'valid_representations': valid,
                          'unequal_trace_witness_found': False})
    raise RuntimeError('No unequal-trace witness in the stated finite search')


def generate(seed, input_path, output_dir):
    snappy.set_rand_seed(seed)
    data = json.loads(input_path.read_text())
    manifold = Link(data['pd_code']).exterior()
    manifold.dehn_fill((1, 0), 1)
    manifold.dehn_fill((1, 0), 2)
    triangulation_path = output_dir / f'annulus_group_seed_{seed}.tri'
    manifold.save(str(triangulation_path))
    simplified = manifold.fundamental_group()
    original = manifold.fundamental_group(simplify_presentation=False)
    assert original.num_generators() == simplified.num_original_generators()
    witness = find_witness(simplified)
    return {
        'seed': seed,
        'triangulation_path': str(triangulation_path.relative_to(ROOT)),
        'triangulation_sha256': hashlib.sha256(triangulation_path.read_bytes()).hexdigest(),
        'simplified': presentation(simplified),
        'original': presentation(original),
        'original_generators_in_simplified': simplified.original_generators(as_int_list=True),
        'simplified_generators_in_original': simplified.generators_in_originals(),
        'witness': witness,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seeds', nargs='+', type=int, default=[20260913, 20260914, 20260915])
    parser.add_argument('--output', type=Path, default=ROOT/'results/annulus_group_certificate.json')
    args = parser.parse_args()
    args.output = args.output.resolve()
    input_path = ROOT/'data/knots/AbeTagami_L_63_c1_c2.json'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    certificate = {
        'status': 'local_construction_obstructed_not_a_sliceness_obstruction',
        'input_path': str(input_path.relative_to(ROOT)),
        'input_sha256': hashlib.sha256(input_path.read_bytes()).hexdigest(),
        'snappy_version': snappy.__version__,
        'filling_slopes': [[0, 0], [1, 0], [1, 0]],
        'meaning': 'Restore surgery-circle solid tori; their longitudes represent their cores in G(K0).',
        'scope': 'Product disk alpha x I for K0 # -K0; both circles in one end ball.',
        'runs': [],
    }
    for seed in args.seeds:
        record = generate(seed, input_path, args.output.parent)
        certificate['runs'].append(record)
        print(json.dumps({'seed': seed, 'prime': record['witness']['prime'],
                          'traces': record['witness']['longitude_traces']}), flush=True)
    args.output.write_text(json.dumps(certificate, indent=2)+'\n')


if __name__ == '__main__':
    main()
