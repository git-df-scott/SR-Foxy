#!/usr/bin/env python3
"""Gauss-sum (Brown / Kawauchi-Kojima style) test of the Sigma_p linking-form
metabolizer gate, for p a prime and any finite abelian H_1.

If K is slice and p is a prime power then Sigma_p(K) bounds a rational homology
4-ball, so its linking form lambda is metabolic, and the Gauss sum

    GS(lambda) = sum_{x in H_1(Sigma_p)} exp(2 pi i lambda(x,x))

equals + |H_1|^{1/2}, a positive real number: the metabolizer contributes
|M| = |H_1|^{1/2} and everything else cancels.  For a difference
D = K_i # (-K_j) one has GS(lambda_D) = GS(lambda_i) * conj(GS(lambda_j)), so

    D slice  ==>  GS(lambda_i) = GS(lambda_j).

That is a computable necessary condition which does NOT require classifying
linking forms, and unlike the discriminant test it works when H_1 has 2-torsion
of exponent > 2.

lambda is read off the Kauffman-Taylor intersection form A_p of the p-fold
cyclic branched cover of B^4 over a pushed-in Seifert surface (block
tridiagonal in V+V^T, V^T, V), exactly as in
scripts/cyclic_cover_linking_form_gate.py: H_1 = coker(A_p), lambda = A_p^{-1}
mod 1.  All arithmetic is exact rational; the Gauss sum is returned as an exact
tally of N-th roots of unity as well as a float.

CONTROLS.  Ribbon knots must give GS = +|H_1|^{1/2} exactly.  Knots that are
not slice need not, and the trefoil at p=2 is the standard witness.

Usage: python3 scripts/cyclic_cover_gauss_sum_gate.py <out.json>
"""
import cmath, json, math, os, sys, time
from fractions import Fraction
import snappy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cyclic_cover_linking_form_gate import (branched_cover_form, int_det,
                                            smith_diag_and_U, rat_inv)

PRIMES = (2, 3, 5)
RIBBON_CONTROLS = ('6_1', '8_20', '9_46', '10_3')
NONSLICE_CONTROLS = ('3_1', '4_1', '6_3')


def linking_gram(V, p):
    """(invariant factors, Gram matrix of lambda as Fractions mod 1)."""
    A = branched_cover_form(V, p)
    if int_det(A) == 0:
        return None, None
    diag, U = smith_diag_and_U(A)
    idx = [i for i, d in enumerate(diag) if abs(d) != 1]
    if not idx:
        return [], []
    Ainv = rat_inv(A)
    Uinv = rat_inv(U)
    gens = [[Uinv[i][k] for i in range(len(A))] for k in idx]
    n = len(A)
    G = [[None] * len(gens) for _ in gens]
    for a in range(len(gens)):
        for b in range(len(gens)):
            v = sum(Fraction(gens[a][i]) * Ainv[i][j] * Fraction(gens[b][j])
                    for i in range(n) for j in range(n))
            G[a][b] = v - int(v // 1)
    return [abs(diag[i]) for i in idx], G


def gauss_sum(orders, G, cap=2000000):
    if not orders:
        return {'order': 1, 'tally': {0: 1}, 'N': 1, 'value': [1.0, 0.0],
                'abs': 1.0}
    total = 1
    for d in orders:
        total *= d
    if total > cap:
        return {'order': total, 'skipped': 'group too large'}
    N = 1
    for row in G:
        for v in row:
            N = N * v.denominator // math.gcd(N, v.denominator)
    k = len(orders)
    tally = {}
    x = [0] * k
    for _ in range(total):
        s = Fraction(0)
        for a in range(k):
            if x[a]:
                for b in range(k):
                    if x[b]:
                        s += x[a] * x[b] * G[a][b]
        num = int((s - int(s // 1)) * N) % N
        tally[num] = tally.get(num, 0) + 1
        for a in range(k):
            x[a] += 1
            if x[a] < orders[a]:
                break
            x[a] = 0
    z = sum(c * cmath.exp(2j * math.pi * r / N) for r, c in tally.items())
    return {'order': total, 'N': N, 'tally': {str(r): c for r, c in sorted(tally.items())},
            'value': [round(z.real, 9), round(z.imag, 9)], 'abs': round(abs(z), 9),
            'is_positive_real_sqrt_order':
                abs(z.imag) < 1e-7 and abs(z.real - math.sqrt(total)) < 1e-7}


def seifert(pd):
    return [[int(x) for x in r]
            for r in snappy.Link([tuple(c) for c in pd]).seifert_matrix()]


def record(V, p):
    orders, G = linking_gram(V, p)
    if orders is None:
        return {'degenerate': True}
    rec = {'invariant_factors': orders}
    rec.update(gauss_sum(orders, G))
    return rec


def main(out_path):
    if os.path.exists(out_path):
        sys.exit('refusing to overwrite %s' % out_path)
    t0 = time.time()
    out = {'snappy': snappy.version(), 'primes': list(PRIMES),
           'ribbon_controls': {}, 'nonslice_controls': {}, 'targets': {},
           'gates': {}}
    for nm in RIBBON_CONTROLS:
        V = seifert(snappy.Link(nm).PD_code())
        out['ribbon_controls'][nm] = {'p=%d' % p: record(V, p) for p in PRIMES}
        print('ribbon', nm, {p: out['ribbon_controls'][nm]['p=%d' % p].get(
            'is_positive_real_sqrt_order') for p in PRIMES}, flush=True)
    for nm in NONSLICE_CONTROLS:
        V = seifert(snappy.Link(nm).PD_code())
        out['nonslice_controls'][nm] = {'p=%d' % p: record(V, p) for p in PRIMES}
        print('nonslice', nm, {p: out['nonslice_controls'][nm]['p=%d' % p].get(
            'is_positive_real_sqrt_order') for p in PRIMES}, flush=True)
    for lab, f in (('K_0', 'AbeTagami_K_0_K_-1__6_3'), ('K_1', 'AbeTagami_K_1')):
        pd = json.load(open('data/knots/%s.json' % f))['pd_code_snappy_0indexed']
        V = seifert(pd)
        out['targets'][lab] = {}
        for p in PRIMES:
            out['targets'][lab]['p=%d' % p] = record(V, p)
            print(lab, 'p=%d' % p, out['targets'][lab]['p=%d' % p].get('invariant_factors'),
                  out['targets'][lab]['p=%d' % p].get('value'), flush=True)
    for p in PRIMES:
        a = out['targets']['K_0']['p=%d' % p]
        b = out['targets']['K_1']['p=%d' % p]
        g = {'K_0': a.get('value'), 'K_1': b.get('value'),
             'invariant_factors': [a.get('invariant_factors'),
                                   b.get('invariant_factors')]}
        if a.get('value') and b.get('value'):
            za = complex(*a['value']); zb = complex(*b['value'])
            prod = za * zb.conjugate()
            g['GS(D01)'] = [round(prod.real, 6), round(prod.imag, 6)]
            g['equal'] = abs(za - zb) < 1e-6
            g['OBSTRUCTION_FIRES'] = not g['equal']
        out['gates']['p=%d' % p] = g
        print('GATE p=%d' % p, json.dumps(g), flush=True)
    out['seconds'] = round(time.time() - t0, 1)
    with open(out_path, 'w') as fh:
        json.dump(out, fh, indent=1, sort_keys=True)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1
         else 'results/opus_2026_09_17/cyclic_cover_gauss_sum_gate.json')
