#!/usr/bin/env python3
"""Integer certificate for all-multiplicity parallel-link Jones gates.
The analytic proof is in REPORT.md. This checks the finite arithmetic in it.
No topology library, numerical root substitution, or knot census is used.
"""
from pathlib import Path
import json


def sk_coefficients(k: int) -> list[int]:
    """S_k at q=-1 in the even irreducible basis V_0,V_2,... ."""
    if k < 0:
        raise ValueError('k must be nonnegative')
    a = [1]
    for r in range(1, k + 1):
        b = [0] * (len(a) + 1)
        for j, c in enumerate(a):
            b[j + 1] += c
            if j:
                b[j] += c
                b[j - 1] += c
            b[j] -= (1 + 2 * (-1)**r) * c
        a = b
    return a


def kernel(n: int, k: int) -> int:
    if n < 0:
        raise ValueError('n must be nonnegative')
    a = sk_coefficients(k)
    phase = (-1)**(k * (k + 3) // 2)
    return phase * sum(c * (-1)**j * ((-1)**j * (2*j + 1))**n
                       for j, c in enumerate(a))


def main() -> dict:
    if not __debug__:
        raise RuntimeError('Run with assertions enabled')
    checks = 0
    for k in range(15):
        for n in range(k):
            assert kernel(n, k) == 0
            checks += 1
    for n in range(50):
        assert kernel(n, 0) == 1
        assert kernel(n, 1) == 1 - (-3)**n
        checks += 2
        for k in range(2, 16):
            assert kernel(n, k) % 32 == 0
            checks += 1
    # Period eight and exact triangular vanishing are proved in REPORT.md.
    # Only 2 <= k <= r <= 7 are needed for the infinite-parameter conclusion.
    finite = [[kernel(r, k) for k in range(8)] for r in range(8)]
    for r in range(8):
        for k in range(2, r + 1):
            assert finite[r][k] % 32 == 0
            checks += 1
    for n in range(8):
        for c in range(8):
            assert (1 + (1 - (-3)**n)*c - (1 + 4*c)**n) % 32 == 0
            checks += 1
    independent = 0
    path = Path(__file__).with_name('PARALLEL_KERNELS.json')
    if path.exists():
        for n, row in json.loads(path.read_text()).items():
            for k, v in enumerate(row['evaluated_universal_kernels']):
                assert kernel(int(n), k) == v
                independent += 1
    out = {
        'status': 'PASS', 'arithmetic_checks': checks,
        'independent_rational_kernel_checks': independent,
        'finite_table_H_rk': finite,
        'finite_table_mod32': [[a % 32 for a in row] for row in finite],
        'theorem_scope': 'Every knot K, every positive multiplicity n, zero-framed parallel C_n(K). Jones determinant is signed J_K(V1)/delta at x=i. No historical novelty claimed.',
        'conclusion': 'null V(C_n(K))=n-1; detV(C_n(K)) congruent detV(K)^n modulo 32.',
        'all_parameter_reason': 'H_nk is an integral linear combination of odd integer powers lambda_j^n, hence eight-periodic modulo 32. H_rk=0 for k>r by the exact Habiro truncation. The 8x8 table and 64 residue checks suffice.'
    }
    Path(__file__).with_name('ALL_PARALLELS_CERTIFICATE.json').write_text(
        json.dumps(out, indent=2) + '\n')
    return out


if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
