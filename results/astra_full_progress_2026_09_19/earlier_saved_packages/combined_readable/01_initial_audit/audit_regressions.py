#!/usr/bin/env python3
"""Bounded, dependency-free audit of specific SR-Foxy comparison failure modes.

Run: python3 audit_regressions.py --output results.json

The numerical examples and fake isometry engine are SYNTHETIC. They prove
unsoundness of decision rules, not that a particular census pair was misclassified.
The SL(2,F5) calculation reproduces a PRE-EXISTING research/14 certificate from
its displayed presentation. It does NOT independently extract words from the PD.
No SnapPy, network, or repository write access is used.
"""
from __future__ import annotations
import argparse
import itertools
import json
import platform
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

Matrix = tuple[tuple[int, int], tuple[int, int]]
I: Matrix = ((1, 0), (0, 1))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def mul(a: Matrix, b: Matrix, p: int = 5) -> Matrix:
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) % p
                       for j in range(2)) for i in range(2))  # type: ignore[return-value]


def inv(a: Matrix, p: int = 5) -> Matrix:
    det = (a[0][0] * a[1][1] - a[0][1] * a[1][0]) % p
    require(det == 1, 'Matrix must have determinant one')
    return ((a[1][1] % p, -a[0][1] % p), (-a[1][0] % p, a[0][0] % p))


def trace(a: Matrix, p: int = 5) -> int:
    return (a[0][0] + a[1][1]) % p


def sl2(p: int = 5) -> list[Matrix]:
    return [((a, b), (c, d)) for a, b, c, d in itertools.product(range(p), repeat=4)
            if (a * d - b * c) % p == 1]


def evaluate(word: str, generators: dict[str, Matrix]) -> Matrix:
    value = I
    for letter in word:
        if letter not in generators:
            raise ValueError(f'Unrecognized generator {letter!r}')
        value = mul(value, generators[letter])
    return value


def overlap(a: tuple[Fraction, Fraction], b: tuple[Fraction, Fraction]) -> bool:
    return max(a[0], b[0]) <= min(a[1], b[1])


def legacy_try_isometry(filled: Callable[..., tuple[Any, str]], retries: int = 6):
    """Transcription of control flow in 5a4b38a/zero_surgery_confirm.py.

    Only input construction is injected; returning immediately on either Boolean
    is the behavior under test. No claim of running SnapPy is made.
    """
    for hp in (False, True):
        try:
            a, _ = filled(0, hp)
            b, _ = filled(1, hp)
        except Exception:
            continue
        for _ in range(retries):
            try:
                return bool(a.is_isometric_to(b))
            except Exception:
                pass
            try:
                a.randomize()
                b.randomize()
            except Exception:
                break
    return None


def conservative_try_isometry(filled: Callable[..., tuple[Any, str]], retries: int = 6):
    """Minimal semantic repair, NOT a production SnapPy runner.

    A full runner also needs subprocess deadlines, input hashes, explicit map
    witnesses, orientation flags, seeds, and durable per-attempt checkpoints.
    """
    attempts = []
    for hp in (False, True):
        try:
            a, _ = filled(0, hp)
            b, _ = filled(1, hp)
        except Exception as exc:
            attempts.append({'hp': hp, 'construction_error': type(exc).__name__})
            continue
        for k in range(retries):
            try:
                value = a.is_isometric_to(b)
                if type(value) is not bool:
                    raise TypeError('Expected an actual Boolean')
                attempts.append({'hp': hp, 'retry': k, 'returned': value})
                if value:
                    return 'ISOMETRIC_TRUE_RETURN', attempts
            except Exception as exc:
                attempts.append({'hp': hp, 'retry': k, 'error': type(exc).__name__})
            try:
                a.randomize()
                b.randomize()
            except Exception as exc:
                attempts.append({'hp': hp, 'randomization_error': type(exc).__name__})
                break
    return 'UNKNOWN', attempts


def engine_factory(behavior: str):
    events: list[dict[str, Any]] = []
    class FakeManifold:
        def __init__(self, hp: bool):
            self.hp = hp
        def is_isometric_to(self, other):
            events.append({'hp': self.hp})
            if behavior == 'exception':
                raise RuntimeError('Synthetic undecided engine')
            if behavior == 'false_then_hp_true':
                return self.hp
            return behavior == 'always_true'
        def randomize(self):
            return None
    def filled(index: int, hp: bool = False):
        return FakeManifold(hp), f'synthetic-{index}'
    return filled, events


def run() -> dict[str, Any]:
    checks = []
    def save(name: str, evidence: Any, kind: str = 'SYNTHETIC_REGRESSION'):
        checks.append({'name': name, 'status': 'PASS', 'kind': kind, 'evidence': evidence})

    tol = Fraction(1, 10**6)
    center, eps = Fraction(2000001, 2000000), Fraction(1, 10**12)
    a, b = center - eps, center + eps
    bins = [round(float(x) / float(tol)) for x in (a, b)]
    require(abs(a - b) < tol and bins[0] != bins[1], 'Expected missed tolerance-neighbor pair')
    save('volume_rounding_boundary_misses_pair',
         {'a': str(float(a)), 'b': str(float(b)), 'difference_exact': str(b-a),
          'tolerance_exact': str(tol), 'legacy_bins': bins,
          'conclusion': 'Same-bucket grouping is not a lossless tolerance-neighbor filter.'})

    ia, ib = (a-eps, a+eps), (b-eps, b+eps)
    require(overlap(ia, ib) and max(ia[0], ib[0]) == center, 'Expected common exact value')
    save('volume_intervals_allow_identical_true_value',
         {'interval_a': list(map(str, ia)), 'interval_b': list(map(str, ib)),
          'shared_exact_value': str(center), 'actual_manifolds': False})
    require(not overlap((Fraction(1), Fraction(2)), (Fraction(3), Fraction(4))),
            'Disjoint interval control failed')
    save('disjoint_interval_negative_control', {'intervals': [[1, 2], [3, 4]]})

    s_center = Fraction(1400001, 2000000)  # 0.7000005, well below cutoff 1.2
    sa, sb = s_center-eps, s_center+eps
    fa = (round(float(sa), 6), round(0.125, 6))
    fb = (round(float(sb), 6), round(0.125, 6))
    require(fa != fb and overlap((sa-eps, sa+eps), (sb-eps, sb+eps)), 'Fingerprint witness failed')
    save('rounded_spectrum_difference_is_not_certified_separation',
         {'legacy_fingerprint_a': fa, 'legacy_fingerprint_b': fb,
          'shared_possible_exact_length': str(s_center), 'actual_geodesics': False})

    filled, events = engine_factory('false_then_hp_true')
    old = legacy_try_isometry(filled)
    require(old is False and events == [{'hp': False}], 'Legacy premature return not reproduced')
    save('legacy_false_prevents_hp_retry', {'returned': old, 'attempts': events})
    filled, _ = engine_factory('false_then_hp_true')
    verdict, attempts = conservative_try_isometry(filled)
    require(verdict == 'ISOMETRIC_TRUE_RETURN' and any(x.get('hp') and x.get('returned') for x in attempts),
            'Conservative retry failed to reach high precision')
    save('conservative_retry_retains_hp_positive', {'verdict': verdict, 'attempts': attempts})
    for behavior in ('always_false', 'exception', 'always_true'):
        filled, _ = engine_factory(behavior)
        verdict, attempts = conservative_try_isometry(filled)
        expected = 'ISOMETRIC_TRUE_RETURN' if behavior == 'always_true' else 'UNKNOWN'
        require(verdict == expected, f'Incorrect conservative {behavior} verdict')
        save('conservative_' + behavior + '_control', {'verdict': verdict, 'attempt_count': len(attempts)})

    first = [(i / 100, 0.0) for i in range(1, 9)]
    second = first[:]; second[5] = (0.065, 0.0)
    require(first != second and first[:3] == second[:3], 'Expected discarded mismatch witness')
    save('saving_first_three_can_drop_compared_witness',
         {'compared_a': first, 'compared_b': second, 'saved_a': first[:3], 'saved_b': second[:3]})
    records = list(range(4001))
    require(len(records[:4000]) == 4000 and records[-1] not in records[:4000], 'Truncation test failed')
    save('all_first_4000_is_not_all', {'records': len(records), 'saved': len(records[:4000])})

    # Direct reproduction of the displayed research/14 certificate, not a new theorem.
    aa: Matrix = ((0, 1), (4, 2)); bb: Matrix = ((0, 2), (2, 3))
    generators = {'a': aa, 'A': inv(aa), 'b': bb, 'B': inv(bb)}
    r = 'aabbbaBAABabbbaabABBBAb'
    u = 'BabA'
    v = 'BBABabbbaBABabbbaBAA'
    er, eu, ev = [evaluate(w, generators) for w in (r, u, v)]
    group = sl2()
    require(er == I and len(group) == 120 and (trace(eu), trace(ev)) == (1, 4),
            'Saved finite-group certificate failed')
    save('existing_annulus_finite_group_certificate_reproduced',
         {'presentation_relator': r, 'axis_words': [u, v], 'a': aa, 'b': bb,
          'relator_image': er, 'axis_images': [eu, ev], 'traces_mod_5': [trace(eu), trace(ev)]},
         'REPRODUCTION_OF_EXISTING_ALGEBRA')
    for target, label in ((ev, 'v'), (inv(ev), 'inverse_v')):
        conjugators = [g for g in group if mul(mul(inv(g), eu), g) == target]
        require(not conjugators, 'Found unexpected finite-group conjugacy')
        save('exhaustive_SL2F5_no_conjugator_' + label,
             {'matrices_examined': len(group), 'conjugators': conjugators},
             'REPRODUCTION_OF_EXISTING_ALGEBRA')
    conjugate_u = mul(mul(inv(bb), eu), bb)
    require(any(mul(mul(inv(g), eu), g) == conjugate_u for g in group), 'Positive conjugacy control failed')
    save('SL2F5_positive_conjugacy_control', {'known_conjugator': bb}, 'EXACT_CONTROL')
    # Tampering must be detected; no assertion that a new target is obstructed.
    require(evaluate(r + 'a', generators) != I, 'Tampered relator was unexpectedly accepted')
    save('SL2F5_tamper_rejection_control', {'tampered_relator': r + 'a'}, 'EXACT_CONTROL')

    return {'status': 'ALL_CHECKS_PASS', 'counterexample_found': False,
            'generated_utc': datetime.now(timezone.utc).isoformat(),
            'python': platform.python_version(), 'platform': platform.system(),
            'dependencies': 'Python standard library only', 'checks': checks,
            'check_count': len(checks),
            'limits': ['No SnapPy calculation was run.',
                       'No actual census pair was demonstrated to be misclassified.',
                       'No sweep JSONL or live process state was retrieved from the remote /tmp directory.',
                       'Finite-group words were copied from the cited research note, not independently extracted from a diagram.',
                       'The exact finite-group result only excludes the specified axis annulus in the specified product-disk exterior.',
                       'No new slice disk, concordance, or global nonribbon obstruction was found.']}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run()
    text = json.dumps(result, indent=2) + '\n'
    if args.output:
        # Exclusive creation: never overwrite previous evidence.
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x', encoding='utf-8') as f:
            f.write(text)
    print(text)


if __name__ == '__main__':
    main()
