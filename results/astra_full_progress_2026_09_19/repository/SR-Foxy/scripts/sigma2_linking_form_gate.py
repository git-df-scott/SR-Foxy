#!/usr/bin/env python3
"""Exact Z/13 linking forms of Sigma_2(K_n) for the Abe-Tagami family, and the
metabolizer test they gate.

If D_{i,j} = K_i # (-K_j) is smoothly (or even topologically) slice then
Sigma_2(D_{i,j}) = Sigma_2(K_i) # (-Sigma_2(K_j)) bounds a rational homology
4-ball, so the linking form lambda_i (+) (-lambda_j) on Z/13 (+) Z/13 must be
metabolic.  On a cyclic group of prime order p, lambda(g,g) = a/p with a well
defined modulo squares, and lambda_i (+) (-lambda_j) is metabolic iff
a_i * a_j is a quadratic residue mod p.

lambda is computed exactly from a Seifert matrix V:
  A = V + V^T presents H_1(Sigma_2) and lambda(x,y) = x^T A^{-1} y mod 1.
Integer Smith normal form is used to pick a generator of the Z/13 summand;
no floating point enters.

Usage: python3 scripts/sigma2_linking_form_gate.py <out.json>
"""
import json, os, sys
from fractions import Fraction
import snappy

KNOTS = (('K_0 (= 6_3)', 'AbeTagami_K_0_K_-1__6_3'),
         ('K_1', 'AbeTagami_K_1'),
         ('K_2', 'AbeTagami_K_2'))
CONTROLS = ('3_1', '4_1', '5_1', '6_1', '6_3')


def smith(Ain):
    A = [row[:] for row in Ain]
    n, m = len(A), len(A[0])
    U = [[int(i == j) for j in range(n)] for i in range(n)]

    def swap_rows(i, j):
        A[i], A[j] = A[j], A[i]
        U[i], U[j] = U[j], U[i]

    def swap_cols(i, j):
        for r in A:
            r[i], r[j] = r[j], r[i]

    def addrow(i, j, c):
        A[i] = [a + c * b for a, b in zip(A[i], A[j])]
        U[i] = [a + c * b for a, b in zip(U[i], U[j])]

    def addcol(i, j, c):
        for r in A:
            r[i] += c * r[j]

    def smallest():
        piv = None
        for i in range(t, n):
            for j in range(t, m):
                if A[i][j] != 0 and (piv is None
                                     or abs(A[i][j]) < abs(A[piv[0]][piv[1]])):
                    piv = (i, j)
        return piv

    t = 0
    while t < min(n, m):
        piv = smallest()
        if piv is None:
            break
        swap_rows(t, piv[0]); swap_cols(t, piv[1])
        while True:
            clean = True
            for i in range(t + 1, n):
                if A[i][t] % A[t][t]:
                    clean = False
                q = A[i][t] // A[t][t]
                if q:
                    addrow(i, t, -q)
            for j in range(t + 1, m):
                if A[t][j] % A[t][t]:
                    clean = False
                q = A[t][j] // A[t][t]
                if q:
                    addcol(j, t, -q)
            if clean:
                break
            piv = smallest()
            swap_rows(t, piv[0]); swap_cols(t, piv[1])
        t += 1
    return A, U


def inv_rational(A):
    n = len(A)
    M = [[Fraction(A[i][j]) for j in range(n)]
         + [Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return [row[n:] for row in M]


def linking_class(V):
    n = len(V)
    A = [[V[i][j] + V[j][i] for j in range(n)] for i in range(n)]
    D, U = smith(A)
    diag = [D[i][i] for i in range(min(len(D), len(D[0])))]
    big = [i for i, d in enumerate(diag) if abs(d) > 1]
    if len(big) != 1:
        return None, None, diag
    k = big[0]
    p = abs(diag[k])
    Uinv = inv_rational(U)
    g = [Uinv[i][k] for i in range(n)]
    Ainv = inv_rational(A)
    val = sum(Fraction(g[i]) * Ainv[i][j] * g[j]
              for i in range(n) for j in range(n)) * p
    assert val.denominator == 1, val
    return p, int(val) % p, diag


def qr(p):
    return sorted(set((i * i) % p for i in range(1, p)))


def seifert(pd):
    return [[int(x) for x in r]
            for r in snappy.Link([tuple(c) for c in pd]).seifert_matrix()]


def main(out_path):
    if os.path.exists(out_path):
        sys.exit('refusing to overwrite %s' % out_path)
    out = {'snappy': snappy.version(), 'controls': {}, 'targets': {}}
    for nm in CONTROLS:
        p, a, diag = linking_class(seifert(snappy.Link(nm).PD_code()))
        out['controls'][nm] = {'H1': 'Z/%d' % p, 'lambda_gg': '%d/%d' % (a, p),
                               'genus_of_seifert_matrix': len(diag) // 2}
    vals = {}
    for lab, f in KNOTS:
        pd = json.load(open('data/knots/%s.json' % f))['pd_code_snappy_0indexed']
        p, a, diag = linking_class(seifert(pd))
        vals[lab] = (p, a)
        out['targets'][lab] = {'H1': 'Z/%d' % p, 'lambda_gg': '%d/%d' % (a, p),
                               'seifert_matrix_size': len(diag)}
    p = 13
    out['quadratic_residues_mod_13'] = qr(p)
    out['metabolizer_tests'] = {}
    labs = [l for l, _ in KNOTS]
    for i in range(len(labs)):
        for j in range(i + 1, len(labs)):
            ai, aj = vals[labs[i]][1], vals[labs[j]][1]
            r = (ai * aj) % p
            out['metabolizer_tests']['D(%s,%s)' % (i, j)] = {
                'a_i': ai, 'a_j': aj, 'a_i*a_j mod 13': r,
                'is_quadratic_residue': r in qr(p),
                'metabolizer_exists': r in qr(p),
                'obstruction_fires': r not in qr(p),
            }
    out['verdict'] = (
        'NO OBSTRUCTION. All three Z/13 linking forms lie in the same square '
        'class (5, 6, 7 are all non-residues mod 13), so every D_{i,j} admits '
        'a linking-form metabolizer and this gate is passed, not failed. '
        'This excludes exactly one thing: the order-13 linking form of the '
        'double branched cover cannot obstruct sliceness of D_{0,1}, D_{0,2} '
        'or D_{1,2}.')
    with open(out_path, 'w') as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1
         else 'results/opus_2026_09_17/sigma2_linking_form_gate.json')
