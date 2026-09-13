#!/usr/bin/env python3
"""Check the group/Fox algebra used in the relative trace obstruction.

The topology and duality argument are written in research/14_marked_annulus_audit.md.
This script does not construct an intersection matrix or an embedded annulus.
"""
import json
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def clean(p):
    return {k: v for k, v in p.items() if v}


def add_term(p, exponent, coefficient):
    p[exponent] = p.get(exponent, 0)+coefficient


def multiply(p, q):
    result = {}
    for i, a in p.items():
        for j, b in q.items():
            add_term(result, i+j, a*b)
    return clean(result)


def shift(p, n):
    return {i+n: a for i, a in p.items()}


def exponents(word, n=2):
    return [sum(1 if x == i else -1 if x == -i else 0 for x in word)
            for i in range(1, n+1)]


def reduce_word(word):
    result = []
    for x in word:
        if result and result[-1] == -x:
            result.pop()
        else:
            result.append(x)
    return result


def main():
    if not __debug__:
        raise RuntimeError('Run without -O: this algebra checker requires assertions.')
    record = json.loads((ROOT/'results/annulus_group_compact.json').read_text())['runs'][0]
    group = record['simplified']
    assert group['generators'] == ['a', 'b'] and len(group['relator_letters']) == 1
    r = group['relator_letters'][0]
    u, v = [group['peripheral_letters'][i][1] for i in (1, 2)]
    assert len(u) == 4 and u[2:] == [-u[0], -u[1]] and abs(u[0]) != abs(u[1])
    relation_exponents = exponents(r)
    assert relation_exponents == [2, 3]
    assert gcd(*relation_exponents) == 1
    assert exponents(u) == exponents(v) == [0, 0]
    # Killing u forces a,b to commute; r then becomes a^2 b^3 = 1,
    # and v is redundant. Thus the quotient is Z, not merely H_1 = Z.
    phi = [-3, 2]
    assert sum(a*b for a, b in zip(phi, relation_exponents)) == 0
    assert sum(a*b for a, b in zip(phi, exponents(group['peripheral_letters'][0][0]))) == 1
    derivatives = [{}, {}]
    exponent = 0
    for x in r:
        i = abs(x)-1
        if x > 0:
            add_term(derivatives[i], exponent, 1)
            exponent += phi[i]
        else:
            exponent -= phi[i]
            add_term(derivatives[i], exponent, -1)
    assert exponent == 0
    derivatives = [clean(p) for p in derivatives]
    delta = {0: 1, 1: -3, 2: 5, 3: -3, 4: 1}
    assert derivatives[0] == shift(multiply({0: 1, 1: 1}, delta), -3)
    assert derivatives[1] == shift(multiply({0: 1, 1: 1, 2: 1}, delta), -6)
    # The two remaining factors are coprime, so their gcd is Delta up to a unit.
    remainder = {0: 1, 1: 1, 2: 1}
    for i, coefficient in multiply({1: 1}, {0: 1, 1: 1}).items():
        add_term(remainder, i, -coefficient)
    assert clean(remainder) == {0: 1}
    inverse_u = [-x for x in reversed(u)]
    assert reduce_word(inverse_u+u+v+u) == reduce_word(v+u)
    result = {
        'all_algebra_checks_passed': True,
        'source_certificate': 'results/annulus_group_compact.json',
        'relator': group['relators'][0],
        'longitude_words': [group['peripheral_words'][i][1] for i in (1, 2)],
        'longitude_1_is_basis_commutator': True,
        'relator_abelian_exponents': relation_exponents,
        'longitude_abelian_exponents': [exponents(u), exponents(v)],
        'quotient_by_both_longitudes': 'Z (explicit presentation reduction, not homology only)',
        'meridian_normalized_abelianization': {'a': -3, 'b': 2},
        'fox_derivatives': [{str(k): p[k] for k in sorted(p)} for p in derivatives],
        'alexander_coefficients_low_to_high': [delta[i] for i in range(5)],
        'boundary_alexander_order_coefficients_low_to_high': [multiply(delta, delta)[i] for i in range(9)],
        'delta_at_1': sum(delta.values()),
        'delta_at_minus_1': sum(a*(-1)**i for i, a in delta.items()),
        'intersection_determinant_status': 'Delta^2 up to Laurent unit, DEDUCED by the written duality argument; matrix not constructed',
        'mixed_word_proposal': 'u^-1 (uv) u = vu, checked as a free-group identity; no geometric realization certified',
    }
    path = ROOT/'results/trace_complement_audit.json'
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
