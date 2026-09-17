#!/usr/bin/env python3
"""One-command check of every arithmetic fact the trace-cap lemma rests on.

Standard library only.  Exit status 0 iff all checks pass.
Run:  python3 results/opus_2026_09_18_trace_cap_gate/check_trace_cap_gate.py
"""
from fractions import Fraction as F
import sys

ok = True


def check(name, got, want):
    global ok
    good = got == want
    ok = ok and good
    print('%-58s %-22s %s' % (name, got, 'OK' if good else 'FAIL want %s' % (want,)))


def det(M):
    M = [[F(x) for x in r] for r in M]
    n = len(M)
    s = F(1)
    for k in range(n):
        p = next((i for i in range(k, n) if M[i][k] != 0), None)
        if p is None:
            return F(0)
        if p != k:
            M[k], M[p] = M[p], M[k]
            s = -s
        for i in range(k + 1, n):
            f = M[i][k] / M[k][k]
            M[i] = [M[i][j] - f * M[k][j] for j in range(n)]
    for k in range(n):
        s *= M[k][k]
    return s


def negcf(p, q):
    out = []
    while q:
        a = -((-p) // q)          # ceiling
        out.append(a)
        p, q = q, a * q - p
    return out


def evalcf(cf):
    x = F(cf[-1])
    for a in reversed(cf[:-1]):
        x = a - 1 / x
    return x


# --- the trace form of the n=1 annulus twist -------------------------------
QW = [[2, 1], [1, 0]]
check('det Q_W  (unimodular)', det(QW), F(-1))
check('det 2*Q_W  (<0 so signature (1,1))',
      det([[2 * x for x in r] for r in QW]), F(-4))

# --- the plumbing that was proposed as the cap -----------------------------
cf = negcf(13, 5)
check('negative continued fraction of 13/5', cf, [3, 3, 2])
check('  it evaluates back to 13/5', evalcf(cf), F(13, 5))
n = len(cf)
P = [[0] * n for _ in range(n)]
for i, a in enumerate(cf):
    P[i][i] = -a
    if i + 1 < n:
        P[i][i + 1] = P[i + 1][i] = 1
check('plumbing matrix P(-3,-3,-2)', P, [[-3, 1, 0], [1, -3, 1], [0, 1, -2]])
check('det P  (|det| = 13 = |H_1(L(13,5))|)', det(P), F(-13))
minors = [det([row[:k + 1] for row in P[:k + 1]]) for k in range(n)]
check('P negative definite (alternating leading minors)',
      all((-1) ** (k + 1) * m > 0 for k, m in enumerate(minors)), True)

# --- orientation gate: L(13,5) is amphichiral ------------------------------
check('5^2 mod 13  (= -1, so L(13,5) = -L(13,5))', 5 * 5 % 13, 12)
check('5 * 8 mod 13  (so 8 = 5^-1 and L(13,5) = L(13,8))', 5 * 8 % 13, 1)

# --- G-signature cross-check ----------------------------------------------
# sigma(W2) = 2 sigma(W) - [C]^2 / 2, with sigma(W) = 0 and [C]^2 = 0.
sigma_W = 0          # Q_W has det < 0 and rank 2, hence signature 0
C_self = 0           # product annulus K_0 x I has a product normal framing
check('sigma(W_2) by G-signature', 2 * sigma_W - F(C_self, 2), F(0))

print()
print('ALL CHECKS PASS' if ok else 'SOME CHECKS FAILED')
sys.exit(0 if ok else 1)
