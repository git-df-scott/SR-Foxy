#!/usr/bin/env python3
"""Exact arithmetic checks for LOW_WRAPPING_LEMMA.md, not a knot search.

Only Python's standard library is used. The proof supplies the universal
quantifiers and topology; these checks audit its scalar identities and the
saved q-jet normalization. No diagram extraction or new Jones run occurs.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import time


def clean(p: list[int]) -> list[int]:
    p = p[:]
    while p and p[-1] == 0:
        p.pop()
    return p


def add(p: list[int], q: list[int]) -> list[int]:
    return clean([(p[i] if i < len(p) else 0) +
                  (q[i] if i < len(q) else 0)
                  for i in range(max(len(p), len(q)))])


def neg(p: list[int]) -> list[int]:
    return [-x for x in p]


def mul(p: list[int], q: list[int]) -> list[int]:
    if not p or not q:
        return []
    r = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i+j] += a*b
    return clean(r)


def shift(p: list[int], n: int) -> list[int]:
    if n < 0:
        raise ValueError('Negative polynomial shift')
    return [0]*n + p if p else []


def valuation(p: list[int]) -> int | None:
    return next((i for i, a in enumerate(p) if a), None)


def jet_quotient_at_i(jet: list[int], n: int) -> tuple[list[int], list[int]]:
    """Divide by (q^2+1)^n and evaluate q^n * quotient at q=i mod 32."""
    d = jet[:]
    quotient = [0] * max(0, len(d) - 2*n)
    for k in range(len(d)-1, 2*n-1, -1):
        c = d[k] % 32
        quotient[k-2*n] = c
        for j in range(n+1):
            d[k-2*n+2*j] -= c * math.comb(n, j)
    value = [0, 0]
    for j, c in enumerate(quotient):
        power = j+n
        value[power % 2] += c * (-1)**(power//2)
    return [x % 32 for x in d[:2*n]], [x % 32 for x in value]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=Path, default=Path(__file__).with_name('inputs.json'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(f'Refusing to overwrite {args.output}')
    start = time.monotonic()
    inputs = json.loads(args.inputs.read_text())
    k = inputs['KDG']
    s = inputs['published_stevedore_control']
    checks: dict[str, bool] = {}

    def check(name: str, condition: bool) -> None:
        if not condition:
            raise ArithmeticError(name)
        checks[name] = True

    d = k['signed_determinant']
    e2 = k['two_parallel_quotient_mod32']
    e3 = k['three_parallel_quotient_exact']
    r = s['signed_determinant']**3
    check('target_square_class', d % 8 == 1)
    check('target_two_residue', e2 % 32 == d*d % 32)
    check('target_three_residue', e3 % 32 == d**3 % 32)
    check('reference_determinant_class', r % 32 == d % 32)
    check('reference_two_moment_class', r*r % 32 == e2 % 32)
    check('reference_three_moment_class', r**3 % 32 == e3 % 32)
    c2 = s['two_parallel_quotient_exact'] - 1
    c3 = s['three_parallel_quotient_exact'] - s['signed_determinant']
    check('even_control_has_exact_order_two', c2 == 48 and c2 != 0)
    check('odd_control_has_exact_order_three', c3 == 1776 and c3 != 0)
    check('do_not_invert_control_constants_mod32', math.gcd(c2, 32) != 1 and math.gcd(c3, 32) != 1)
    check('two_jet_normalization', jet_quotient_at_i(k['two_parallel_jet_mod32'], 2) == ([0]*4, [17, 0]))
    check('three_jet_normalization', jet_quotient_at_i(k['three_parallel_jet_mod32'], 3) == ([0]*6, [9, 0]))

    # Exact polynomial identities with varied higher coefficients. h models
    # delta formally; these are algebraic fixtures, NOT real knot data.
    fixtures = [[], [1], [-2, 3], [4, -1, 0, 7]]
    E1, E2, E3 = [d, 2, -5], [e2, 7, 4], [e3, -6, 9]
    identity_count = 0
    for m in range(1, 13):
        for A in fixtures:
            for C in fixtures:
                a = shift(A, max(0, m-2))
                b = add(neg(shift(a, 2)), shift(C, m))
                lhs = add(mul(a, shift(E2, 2)), b)
                rhs = add(shift(mul(A, add(E2, [-1])), max(0, m-2)+2), shift(C, m))
                check(f'even_identity_{m}_{identity_count}', lhs == rhs and (valuation(lhs) is None or valuation(lhs) >= m))
                identity_count += 1
                a = shift(A, max(0, m-3))
                b = add(neg(shift(a, 2)), shift(C, m-1))
                lhs = add(mul(a, shift(E3, 3)), mul(b, shift(E1, 1)))
                rhs = add(shift(mul(A, add(E3, neg(E1))), max(0, m-3)+3), shift(mul(C, E1), m))
                check(f'odd_identity_{m}_{identity_count}', lhs == rhs and (valuation(lhs) is None or valuation(lhs) >= m))
                identity_count += 1

    # Exhaust all scalar coefficients mod 32. Since the formulas are linear
    # in the coefficient values, equality also holds componentwise in
    # Z[A]/(A^4+1,32). The proof does not infer topology from this enumeration.
    residue_cases = 0
    for a in range(32):
        for c in range(32):
            even_k, even_r = a*(e2-1)+c, a*(r*r-1)+c
            odd_k, odd_r = a*(e3-d)+c*d, a*(r**3-r)+c*r
            if (even_k-even_r) % 32 or (odd_k-odd_r) % 32:
                raise ArithmeticError('Leading coefficient transfer failed')
            residue_cases += 2
    check('all_scalar_leading_coefficient_transfers', residue_cases == 2048)
    check('wrong_even_moment_detected', ((e2+1-1)-(r*r-1)) % 32 != 0)
    check('wrong_odd_moment_detected', ((e3+1-d)-(r**3-r)) % 32 != 0)
    check('insufficient_even_valuation_detected', valuation(shift([c2], 2)) == 2 < 3)
    check('insufficient_odd_valuation_detected', valuation(shift([c3], 3)) == 3 < 4)
    check('ribbon_reference_classes', [9**n % 32 for n in range(4)] == [1, 9, 17, 25])
    report = {
        'status': 'ARITHMETIC_CHECKS_PASS_NO_COUNTEREXAMPLE',
        'scope': 'Proof arithmetic and saved jet normalization only; no new knot or satellite computation.',
        'checks_passed': len(checks), 'polynomial_identity_fixtures': identity_count,
        'scalar_mod32_cases': residue_cases,
        'negative_controls': 4,
        'control_leading_differences': [c2, c3],
        'reference_ribbon_knot': 'connected sum of three copies of 6_1',
        'reference_signed_determinant': r,
        'target_moment_residues': [d % 32, e2 % 32, e3 % 32],
        'input_sha256': hashlib.sha256(args.inputs.read_bytes()).hexdigest(),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'python': platform.python_version(), 'seconds': time.monotonic()-start,
        'deterministic': True,
        'unverified_here': ['satellite diagrams and framing', 'original Jones evaluation', 'independent external review of the transfer proof'],
    }
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
