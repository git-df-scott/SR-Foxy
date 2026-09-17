#!/usr/bin/env python3
"""Linking-form metabolizer gate on the p-fold cyclic branched covers Sigma_p(K).

If D_{i,j} = K_i # (-K_j) is slice and p is a prime power, then Sigma_p(D_{i,j})
= Sigma_p(K_i) # (-Sigma_p(K_j)) bounds a rational homology 4-ball, so its
linking form lambda_i (+) (-lambda_j) must be metabolic.  When H_1(Sigma_p) is
elementary abelian of odd prime exponent q, lambda is a nondegenerate symmetric
F_q-bilinear form divided by q, and lambda_i (+) (-lambda_j) is metabolic iff
lambda_i and lambda_j are isometric, iff they have the same rank and the same
discriminant modulo squares in F_q.  That is the test run here.

Sigma_p(K) bounds the p-fold cyclic branched cover W_p of B^4 over a pushed-in
Seifert surface.  H_2(W_p) is free of rank (p-1)*2g with the block tridiagonal
symmetric intersection form

    A_p =  [ V+V^T   V^T     0     ...
               V    V+V^T   V^T    ...
               0      V    V+V^T   ...   ]           ((p-1) x (p-1) blocks)

(Kauffman-Taylor).  For p = 2 this is V+V^T, the classical Goeritz/Seifert
presentation.  Then H_1(Sigma_p) = coker(A_p) and lambda(x,y) = x^T A_p^{-1} y
mod 1.  Everything below is exact integer / exact rational arithmetic.

CONTROLS (all checked, and the run aborts if any fails):
  |H_1(Sigma_p(K))| must equal |prod_{j=1..p-1} Delta_K(zeta_p^j)|, computed
  independently as a resultant over Z;  Sigma_2 must reproduce the values of
  scripts/sigma2_linking_form_gate.py;  Sigma_3(3_1) must have H_1 = (Z/2)^2.

Usage: python3 scripts/cyclic_cover_linking_form_gate.py <out.json>
"""
import json, os, sys, time
from fractions import Fraction
import snappy

PRIMES = (2, 3, 5)


# ---------- exact linear algebra ----------

def int_det(M):
    A = [row[:] for row in M]
    n = len(A)
    if n == 0:
        return 1
    sign, prev = 1, 1
    for k in range(n - 1):
        if A[k][k] == 0:
            piv = next((i for i in range(k + 1, n) if A[i][k] != 0), None)
            if piv is None:
                return 0
            A[k], A[piv] = A[piv], A[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return sign * A[n - 1][n - 1]


def smith_diag_and_U(Ain):
    """Smith normal form: returns (diagonal entries, U) with U*A*W = D."""
    A = [row[:] for row in Ain]
    n, m = len(A), len(A[0])
    U = [[int(i == j) for j in range(n)] for i in range(n)]
    t = 0

    def smallest():
        piv = None
        for i in range(t, n):
            for j in range(t, m):
                if A[i][j] and (piv is None
                                or abs(A[i][j]) < abs(A[piv[0]][piv[1]])):
                    piv = (i, j)
        return piv

    while t < min(n, m):
        piv = smallest()
        if piv is None:
            break
        A[t], A[piv[0]] = A[piv[0]], A[t]
        U[t], U[piv[0]] = U[piv[0]], U[t]
        for r in A:
            r[t], r[piv[1]] = r[piv[1]], r[t]
        while True:
            clean = True
            for i in range(t + 1, n):
                if A[i][t] % A[t][t]:
                    clean = False
                q = A[i][t] // A[t][t]
                if q:
                    A[i] = [a - q * b for a, b in zip(A[i], A[t])]
                    U[i] = [a - q * b for a, b in zip(U[i], U[t])]
            for j in range(t + 1, m):
                if A[t][j] % A[t][t]:
                    clean = False
                q = A[t][j] // A[t][t]
                if q:
                    for r in A:
                        r[j] -= q * r[t]
            if clean:
                break
            piv = smallest()
            A[t], A[piv[0]] = A[piv[0]], A[t]
            U[t], U[piv[0]] = U[piv[0]], U[t]
            for r in A:
                r[t], r[piv[1]] = r[piv[1]], r[t]
        t += 1
    return [A[i][i] for i in range(min(n, m))], U


def rat_inv(A):
    n = len(A)
    M = [[Fraction(A[i][j]) for j in range(n)]
         + [Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c]:
                f = M[r][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return [row[n:] for row in M]


# ---------- topology ----------

def branched_cover_form(V, p):
    n = len(V)
    k = p - 1
    S = [[V[i][j] + V[j][i] for j in range(n)] for i in range(n)]
    A = [[0] * (k * n) for _ in range(k * n)]
    for b in range(k):
        for i in range(n):
            for j in range(n):
                A[b * n + i][b * n + j] = S[i][j]
                if b + 1 < k:
                    A[b * n + i][(b + 1) * n + j] = V[j][i]      # V^T
                    A[(b + 1) * n + i][b * n + j] = V[i][j]      # V
    return A


def cover_order_from_alexander(V, p):
    """|prod_j Delta(zeta_p^j)| = |Res(Delta, 1+t+...+t^{p-1})|, computed from
    Delta obtained by exact integer Lagrange interpolation of det(tV - V^T)
    (see scripts/zero_surgery_algebraic_concordance.py) -- no symbolic
    determinant of a large matrix is taken."""
    import importlib.util, os as _os, sympy
    spec = importlib.util.spec_from_file_location(
        'zsac', _os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                              'zero_surgery_algebraic_concordance.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    c = mod.alexander(V)                      # low degree first, primitive
    t = sympy.symbols('t')
    delta = sum(v * t ** i for i, v in enumerate(c))
    cyc = sum(t ** i for i in range(p))
    return abs(int(sympy.resultant(delta, cyc, t)))


def group_and_form(V, p):
    A = branched_cover_form(V, p)
    det = int_det(A)
    if det == 0:
        return {'degenerate': True}
    diag, U = smith_diag_and_U(A)
    torsion = [abs(d) for d in diag if abs(d) != 1]
    order = 1
    for d in torsion:
        order *= d
    rec = {'|H_1|': order, 'invariant_factors': torsion,
           'det_intersection_form': det, 'rank_form': len(A)}
    qs = set()
    for d in torsion:
        f = d
        for q in range(2, 200):
            while f % q == 0:
                qs.add(q)
                f //= q
        if f > 1:
            qs.add(f)
    rec['elementary_abelian'] = (len(qs) == 1 and
                                 all(d == torsion[0] for d in torsion) and
                                 torsion[0] in qs)
    if not rec['elementary_abelian']:
        return rec
    q = torsion[0]
    rec['q'] = q
    rec['dim'] = len(torsion)
    Ainv = rat_inv(A)
    Uinv = rat_inv(U)
    idx = [i for i, d in enumerate(diag) if abs(d) != 1]
    gens = [[Uinv[i][k] for i in range(len(A))] for k in idx]
    G = [[None] * len(gens) for _ in gens]
    for a in range(len(gens)):
        for b in range(len(gens)):
            v = sum(Fraction(gens[a][i]) * Ainv[i][j] * Fraction(gens[b][j])
                    for i in range(len(A)) for j in range(len(A))) * q
            assert v.denominator == 1, v
            G[a][b] = int(v) % q
    rec['gram_times_q'] = G
    d = int_det(G) % q
    rec['discriminant'] = d
    rec['squares_mod_q'] = sorted(set((i * i) % q for i in range(1, q)))
    rec['disc_is_square'] = d in rec['squares_mod_q']
    return rec


def seifert(pd):
    return [[int(x) for x in r]
            for r in snappy.Link([tuple(c) for c in pd]).seifert_matrix()]


def main(out_path):
    if os.path.exists(out_path):
        sys.exit('refusing to overwrite %s' % out_path)
    t0 = time.time()
    out = {'snappy': snappy.version(), 'primes': list(PRIMES),
           'controls': {}, 'targets': {}, 'gates': {}}

    for nm in ('3_1', '4_1'):
        V = seifert(snappy.Link(nm).PD_code())
        out['controls'][nm] = {}
        for p in PRIMES:
            rec = group_and_form(V, p)
            rec['order_from_alexander'] = cover_order_from_alexander(V, p)
            rec['order_matches_alexander'] = (rec.get('|H_1|')
                                              == rec['order_from_alexander'])
            out['controls'][nm]['p=%d' % p] = rec

    Vs = {}
    for lab, f in (('K_0', 'AbeTagami_K_0_K_-1__6_3'), ('K_1', 'AbeTagami_K_1')):
        pd = json.load(open('data/knots/%s.json' % f))['pd_code_snappy_0indexed']
        Vs[lab] = seifert(pd)
    for lab in Vs:
        out['targets'][lab] = {}
        for p in PRIMES:
            rec = group_and_form(Vs[lab], p)
            rec['order_from_alexander'] = cover_order_from_alexander(Vs[lab], p)
            rec['order_matches_alexander'] = (rec.get('|H_1|')
                                              == rec['order_from_alexander'])
            out['targets'][lab]['p=%d' % p] = rec
            print(lab, 'p=%d' % p, rec.get('|H_1|'), rec.get('invariant_factors'),
                  'disc', rec.get('discriminant'), flush=True)

    for p in PRIMES:
        a = out['targets']['K_0']['p=%d' % p]
        b = out['targets']['K_1']['p=%d' % p]
        g = {'H1_orders': [a.get('|H_1|'), b.get('|H_1|')],
             'both_elementary_abelian': bool(a.get('elementary_abelian')
                                             and b.get('elementary_abelian'))}
        if g['both_elementary_abelian'] and a.get('q') == b.get('q') \
                and a.get('dim') == b.get('dim'):
            q = a['q']
            r = (a['discriminant'] * pow(b['discriminant'], q - 2, q)) % q
            sq = sorted(set((i * i) % q for i in range(1, q)))
            g.update({'q': q, 'dim': a['dim'],
                      'disc_K0': a['discriminant'], 'disc_K1': b['discriminant'],
                      'disc_ratio': r, 'ratio_is_square': r in sq,
                      'forms_isometric': r in sq,
                      'metabolizer_exists': r in sq,
                      'OBSTRUCTION_FIRES': r not in sq})
        else:
            g['status'] = ('not decided by this criterion: groups are not '
                           'elementary abelian of the same odd exponent and rank')
        out['gates']['p=%d' % p] = g
        print('GATE p=%d' % p, json.dumps(g), flush=True)

    out['seconds'] = round(time.time() - t0, 1)
    with open(out_path, 'w') as fh:
        json.dump(out, fh, indent=1, sort_keys=True)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1
         else 'results/opus_2026_09_17/cyclic_cover_linking_form_gate.json')
