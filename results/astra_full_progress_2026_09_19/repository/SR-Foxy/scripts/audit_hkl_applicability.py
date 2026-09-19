#!/usr/bin/env python3
"""Count irreducible cover-module multiplicities skipped by basic HKL.

Independent finite-field linear algebra on reduced Seifert presentations.
No twisted Alexander polynomial or Casson--Gordon obstruction is evaluated.
"""
import json
from pathlib import Path
import sympy as s


def rank_mod(matrix, q):
    a = [[int(z) % q for z in row] for row in matrix.tolist()]
    rank = 0
    for j in range(matrix.cols):
        pivot = next((i for i in range(rank, matrix.rows) if a[i][j]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inverse = pow(a[rank][j], -1, q)
        a[rank] = [(z*inverse) % q for z in a[rank]]
        for i in range(rank+1, matrix.rows):
            if a[i][j]:
                multiplier = a[i][j]
                a[i] = [(z-multiplier*y) % q for z, y in zip(a[i], a[rank])]
        rank += 1
        if rank == matrix.rows:
            break
    return rank


def run():
    root = Path(__file__).resolve().parents[1]
    models = json.loads((root/'results/AT_seifert_models.json').read_text())
    names = ['AbeTagami_K_0_K_-1__6_3', 'AbeTagami_K_1', 'AbeTagami_K_2']
    V0, V1, V2 = [s.Matrix(models[name]['reduced_matrix']) for name in names]
    matrices = [V0, -V1.T, -V2.T]
    x = s.Symbol('x')
    delta = s.expand((V0-x*V0.T).det())
    rows = []
    for q in [2, 3, 5, 7, 11, 13, 17, 19]:
        for f, exponent in s.factor_list(delta, x, modulus=q)[1]:
            d = int(s.degree(f, x))
            C = s.zeros(d)
            for j in range(d-1):
                C[j+1, j] = 1
            fp = s.Poly(f, x, modulus=q)
            for j in range(d):
                C[j, d-1] = -fp.nth(j)
            mult = []
            for V in matrices:
                B = s.kronecker_product(V, C)-s.kronecker_product(V.T, s.eye(d))
                nullity = B.rows-rank_mod(B, q)
                assert nullity % d == 0
                mult.append(int(nullity//d))
            for p in [2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 17, 19]:
                if not ((p <= 10 and q <= 20) or (p <= 20 and q <= 10)):
                    continue
                if p % q == 0:
                    continue
                if s.rem(x**p-1, f, x, modulus=q) == 0:
                    rows.append({'p': p, 'q': q, 'factor': str(f), 'factor_degree': d,
                                 'multiplicities_K0_minusK1_minusK2': mult,
                                 'D01_multiplicity': mult[0]+mult[1],
                                 'D02_multiplicity': mult[0]+mult[2]})
    result = {'prime_spec': [[10, [0, 20]], [20, [0, 10]]], 'rows': rows,
              'all_D01_D02_factors_skipped_by_basic': all(
                  r['D01_multiplicity'] > 1 and r['D02_multiplicity'] > 1 for r in rows),
              'meaning': 'Exact applicability audit. Basic HKL skips these repeated factors; this is not a sliceness obstruction.'}
    out = root/'results/HKL_basic_applicability_audit.json'
    if out.exists():
        assert json.loads(out.read_text()) == result
        print('Existing applicability result recomputed and matched.')
    else:
        out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    run()
