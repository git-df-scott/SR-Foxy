#!/usr/bin/env python3
"""Exact algebraic S-reductions and saturated metabolizers; no fiber embedding claim."""
import json
from pathlib import Path
import sympy as s
from sympy.matrices.normalforms import smith_normal_decomp


def reduce_matrix(matrix):
    V = s.Matrix(matrix)
    steps = []
    while V.det() == 0:
        n = V.rows
        # Choose a primitive left-kernel vector as a new basis vector.
        candidates = V.T.nullspace()
        u = candidates[0]
        u *= s.ilcm(*[x.q for x in u])
        u /= s.igcd(*list(u))
        i = next((k for k in range(n) if abs(u[k]) == 1), None)
        if i is None:
            _, left_u, _ = smith_normal_decomp(u, domain=s.ZZ)
            P = left_u.inv()
            i = 0
        else:
            P = s.eye(n)
            P[:, i] = u
        assert abs(P.det()) == 1
        W = P.T*V*P
        assert W[i, :] == s.zeros(1, n)
        j = next((k for k in range(n) if abs(W[k, i]) == 1), None)
        if j is None:
            other = [k for k in range(n) if k != i]
            diagonal, left_col, _ = smith_normal_decomp(W[other, i], domain=s.ZZ)
            assert abs(diagonal[0, 0]) == 1
            R = s.eye(n)
            for a, row in enumerate(other):
                for b, col in enumerate(other):
                    R[row, col] = left_col.T[a, b]
            P = P*R
            W = R.T*W*R
            j = other[0]
        Q = s.eye(n)
        for k in range(n):
            if k not in (i, j):
                Q[j, k] = -W[k, i]/W[j, i]
        W = Q.T*W*Q
        assert abs(Q.det()) == 1
        assert all(W[k, i] == 0 for k in range(n) if k != j)
        keep = [k for k in range(n) if k not in (i, j)]
        reduced = W.extract(keep, keep)
        assert (reduced-reduced.T).det() == 1
        steps.append({'input_dimension': n, 'basis_change': (P*Q).tolist(),
                      'removed_indices': [i, j], 'reduced_matrix': reduced.tolist()})
        V = reduced
    return V, steps


def run():
    root = Path(__file__).resolve().parents[1]
    original = s.Matrix(json.loads((root/'data/knots/18nh00000601_seifert.json').read_text())['seifert_matrix'])
    V, steps = reduce_matrix(original)
    phi = V.T.inv()*V
    assert all(x.q == 1 for x in phi)
    t = s.Symbol('t')
    poly = s.Poly(phi.charpoly(t).as_expr(), t)
    removed_pairs = (original.rows - V.rows)//2
    for test_t in [-1, 1, 2, 3]:
        assert (original-test_t*original.T).det() == test_t**removed_pairs*(V-test_t*V.T).det()
    factors = s.factor_list(poly.as_expr())[1]
    assert len(factors) == 2 and all(s.degree(f, t) == 5 and e == 1 for f, e in factors)
    lattices = []
    for f, exponent in factors:
        A = s.zeros(V.rows)
        for coeff in s.Poly(f, t).all_coeffs():
            A = A*phi + coeff*s.eye(V.rows)
        D, left, right = smith_normal_decomp(A, domain=s.ZZ)
        assert D == left*A*right and abs(right.det()) == 1
        zero_indices = [j for j in range(V.rows) if D[j, j] == 0]
        basis = right[:, zero_indices]
        assert basis.cols == 5 and A*basis == s.zeros(V.rows, 5)
        assert basis.T*V*basis == s.zeros(5)
        lattices.append({'factor': str(f), 'saturated_kernel_basis': basis.tolist(),
                         'seifert_restriction_zero': True})
    result = {'original_dimension': original.rows, 'original_det': int(original.det()),
              'original_intersection_det': int((original-original.T).det()),
              'steps': steps, 'reduced_dimension': V.rows, 'reduced_det': int(V.det()),
              'reduced_matrix': V.tolist(), 'algebraic_monodromy': phi.tolist(),
              'characteristic_polynomial': str(poly.as_expr()), 'lattices': lattices,
              'meaning': 'Exact algebraic S-equivalent model with two saturated metabolizers. No embedded fiber, geometric cut system, ribbon disk, or non-ribbon certificate is supplied.'}
    out = root/'results/seifert_model_exact_audit.json'
    if out.exists():
        assert json.loads(out.read_text()) == json.loads(json.dumps(result, default=int))
        print('Existing result independently recomputed and matched, including determinant sanity checks.')
    else:
        out.write_text(json.dumps(result, indent=2, default=int)+'\n')
    print(json.dumps({k: result[k] for k in ['original_dimension', 'reduced_dimension', 'reduced_det', 'characteristic_polynomial', 'meaning']}))


if __name__ == '__main__':
    run()
