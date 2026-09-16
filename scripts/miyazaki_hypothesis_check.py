#!/usr/bin/env python3
"""Exact check of Miyazaki [S07, Thm 5.5] hypothesis (2) on the Teichner partners.

Hypothesis (2), verbatim from Abe-Tagami [S06] Appendix A (their restatement of
Miyazaki Thm 5.5):

    there is no f(t) in Z[t] \\ {+-t^k}_k such that f(t)f(t^{-1}) | Delta_{K_i}(t)

This script decides that condition exhaustively for a given Delta, over Z, with
no floating point anywhere.

Enumeration is complete, not a search:  if F(t) = f(t)*f*(t) divides Delta,
where f*(t) = t^{deg f} f(1/t) is the reverse of f, then f | Delta, hence
lead(f) | lead(Delta) and f(0) | Delta(0).  So it suffices to enumerate integer
polynomials whose leading and constant coefficients are (signed) divisors of
those two integers, over bounded degree and bounded middle coefficients, and
test exact divisibility.  A FAIL verdict is a positive certificate -- it exhibits
f -- and needs no completeness at all.  A PASS verdict is only as complete as
MIDDLE_BOUND, and is reported as such.

Run:  python3 scripts/miyazaki_hypothesis_check.py
"""
from itertools import product

# Alexander polynomials, normalised to Z[t] (monic, positive leading coeff),
# as coefficient lists low-degree-first.  Source: Knot Atlas knot pages,
# fetched 2026-09-16; each is cross-checked below against its determinant
# |Delta(-1)| taken from the same page.
KNOTS = {
    # J candidates: ribbon partners for the Teichner sum D_{0,1} # J
    '6_1':  ([2, -5, 2],                     9),   # non-monic => not fibered
    '8_8':  ([2, -6, 9, -6, 2],             25),   # non-monic => not fibered
    '8_9':  ([1, -3, 5, -7, 5, -3, 1],      25),
    '8_20': ([1, -2, 3, -2, 1],              9),
    '9_27': ([1, -5, 11, -15, 11, -5, 1],   49),
    # the target's own summands, which MUST satisfy the hypothesis
    'K_n = A_n(6_3)': ([1, -3, 5, -3, 1],   13),
    # controls: prime fibered non-slice knots that should PASS hypothesis (2)
    '3_1':  ([1, -1, 1],                     3),
    '4_1':  ([1, -3, 1],                     5),
}

MIDDLE_BOUND = 60   # generous; Landau-Mignotte for these degrees is far smaller


def evaluate(p, x):
    return sum(c * x ** i for i, c in enumerate(p))


def mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def divides(d, n):
    """Exact division test in Z[t]: does d divide n?  d has unit leading coeff."""
    n = list(n)
    dd = len(d) - 1
    while len(n) - 1 >= dd and any(n):
        while n and n[-1] == 0:
            n.pop()
        if len(n) - 1 < dd:
            break
        q, r = divmod(n[-1], d[-1])
        if r:
            return False
        shift = len(n) - 1 - dd
        for i, c in enumerate(d):
            n[i + shift] -= q * c
    while n and n[-1] == 0:
        n.pop()
    return not n


def reverse(f):
    return list(reversed(f))


def is_unit_monomial(f):
    nz = [i for i, c in enumerate(f) if c]
    return len(nz) == 1 and abs(f[nz[0]]) == 1


def signed_divisors(n):
    n = abs(n)
    out = []
    for d in range(1, n + 1):
        if n % d == 0:
            out += [d, -d]
    return out


def norm_factors(delta):
    """All f with f not +-t^k and f(t)f(1/t) | delta, as an exhaustive sweep.

    f | delta forces lead(f) | lead(delta) and f(0) | delta(0), which is what
    makes the leading/constant loops finite without assuming delta is monic.
    """
    hits, seen = [], set()
    top = len(delta) - 1
    leads = signed_divisors(delta[-1])
    consts = signed_divisors(delta[0])
    for d in range(1, top // 2 + 1):          # deg(f*f_rev) = 2d <= deg(delta)
        for lead in leads:
            for const in consts:
                for mid in product(range(-MIDDLE_BOUND, MIDDLE_BOUND + 1),
                                   repeat=max(0, d - 1)):
                    f = [const] + list(mid) + [lead]
                    if is_unit_monomial(f):
                        continue
                    if not divides(f, delta):
                        continue
                    F = mul(f, reverse(f))
                    if divides(F, delta):
                        key = tuple(F)
                        hits.append((f, F))
                        seen.add(key)
    return hits


def fmt(p):
    terms = []
    for i, c in enumerate(p):
        if not c:
            continue
        t = 't' if i == 1 else ('' if i == 0 else 't^%d' % i)
        terms.append(('%+d' % c) + ('*' + t if t else ''))
    return ' '.join(terms) or '0'


print('Miyazaki Thm 5.5 hypothesis (2): "no f in Z[t]\\{+-t^k} with f(t)f(1/t) | Delta"')
print('PASS = hypothesis (2) HOLDS (no nonunit norm factor) -> Miyazaki applicable')
print('FAIL = hypothesis (2) FAILS -> Miyazaki NOT applicable to any sum containing it')
print()
for name, (delta, det) in KNOTS.items():
    got = abs(evaluate(delta, -1))
    ctrl = 'det ok' if got == det else 'DET MISMATCH (%d vs %d)' % (got, det)
    monic = abs(delta[-1]) == 1 and abs(delta[0]) == 1
    hits = norm_factors(delta)
    if hits:
        verdict = 'FAIL (certified)'
    elif monic:
        verdict = 'PASS (no factor with |mid coeff| <= %d)' % MIDDLE_BOUND
    else:
        verdict = 'PASS (bounded); NOTE non-monic => not fibered => outside Thm 5.5'
    print('%-16s Delta = %-46s |Delta(-1)|=%-3d %-24s monic=%-5s -> %s'
          % (name, fmt(delta), got, ctrl, monic, verdict))
    for f, F in hits[:2]:
        print('%18s witness f = %-24s f(t)f(1/t) ~ %s' % ('', fmt(f), fmt(F)))
    if len(hits) > 2:
        print('%18s (+%d further witnesses, all sign/reversal variants)'
              % ('', len(hits) - 2))
print()
print('Controls: 3_1, 4_1 and K_n must read PASS (K_n has irreducible Delta, so')
print('Miyazaki IS applicable to it).  Every nontrivial slice J must read FAIL, by')
print('Fox-Milnor, with no exception -- that is the whole point, and the FAIL rows')
print('are certificates, independent of MIDDLE_BOUND.  6_1 and 8_8 are non-monic,')
print('hence not fibered, hence never inside Thm 5.5 whatever this column says.')
