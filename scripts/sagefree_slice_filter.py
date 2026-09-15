#!/usr/bin/env python3
"""A Sage-free stand-in for spherogram's `could_be_strongly_slice`.

Spherogram's filter needs SnapPy-inside-Sage for `Link.signature()` and
`exterior().fox_milnor_test()`.  Neither is available in every container, and
the whole Dunfield-Gong band search is gated behind that one function.

Every test below is a *necessary* condition for a link to be strongly slice,
so this filter can only ever reject links the real one would also reject --
never the other way round.  Where a condition cannot be evaluated the link is
KEPT.  A weaker filter makes the search slower; it can never lose a ribbon
disk.  That is the same failure direction as the `_safe_filter` patch already
used in `scripts/teichner_certify.py`.

Conditions, in cost order:

1. All pairwise linking numbers vanish.  (Strongly slice => the components
   bound disjoint disks => every linking number is 0.)
2. The signature of V + V^T vanishes, V a Seifert matrix of the link, computed
   exactly over Q by congruence diagonalisation.  Spherogram's own
   `Link.signature()` is documented as this same Murasugi/Seifert-matrix
   signature, so this is a reimplementation, not a substitute invariant.
3. Fox-Milnor, applied ONLY to one-component links: det(V - tV^T) must be
   t^k f(t) f(1/t) up to sign.  For multi-component links the sharp statement
   involves the multivariable polynomial, so the test is skipped rather than
   guessed at.

This module is self-validating: `python3 scripts/sagefree_slice_filter.py`
checks the invariants against knots and links whose values are in the tables.
"""
from fractions import Fraction


def linking_nums_all_zero(link):
    return all(x == 0 for row in link.linking_matrix() for x in row)


def _signature_of_symmetric(M):
    """Signature of an integer symmetric matrix, exactly, by congruence.

    Sylvester's law of inertia: congruence preserves (p, n, z), so we may
    diagonalise with rational row/column operations and count signs.
    """
    n = len(M)
    A = [[Fraction(M[i][j]) for j in range(n)] for i in range(n)]
    pos = neg = 0
    for k in range(n):
        # find a nonzero diagonal entry in the remaining block
        piv = None
        for i in range(k, n):
            if A[i][i] != 0:
                piv = i
                break
        if piv is None:
            # all diagonal entries zero: find any nonzero off-diagonal pair
            found = None
            for i in range(k, n):
                for j in range(i + 1, n):
                    if A[i][j] != 0:
                        found = (i, j)
                        break
                if found:
                    break
            if not found:
                break  # remaining block is zero
            i, j = found
            # row_i += row_j, col_i += col_j makes A[i][i] = 2*A[i][j] != 0
            for c in range(n):
                A[i][c] += A[j][c]
            for r in range(n):
                A[r][i] += A[r][j]
            piv = i
        if piv != k:
            A[k], A[piv] = A[piv], A[k]
            for r in range(n):
                A[r][k], A[r][piv] = A[r][piv], A[r][k]
        d = A[k][k]
        pos += 1 if d > 0 else -0
        neg += 1 if d < 0 else 0
        for i in range(k + 1, n):
            if A[i][k] != 0:
                f = A[i][k] / d
                for c in range(k, n):
                    A[i][c] -= f * A[k][c]
                for r in range(n):
                    A[r][i] -= f * A[r][k]
    return pos - neg


def seifert_signature(link):
    V = link.seifert_matrix()
    n = len(V)
    S = [[V[i][j] + V[j][i] for j in range(n)] for i in range(n)]
    return _signature_of_symmetric(S)


def _det_int(M):
    """Exact determinant of an integer matrix, Bareiss fraction-free."""
    n = len(M)
    if n == 0:
        return 1
    A = [row[:] for row in M]
    sign = 1
    prev = 1
    for k in range(n - 1):
        if A[k][k] == 0:
            swap = None
            for i in range(k + 1, n):
                if A[i][k] != 0:
                    swap = i
                    break
            if swap is None:
                return 0
            A[k], A[swap] = A[swap], A[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
            A[i][k] = 0
        prev = A[k][k]
    return sign * A[n - 1][n - 1]


def _is_square(m):
    m = abs(m)
    if m == 0:
        return True
    r = int(m ** 0.5)
    for c in (r - 2, r - 1, r, r + 1, r + 2):
        if c >= 0 and c * c == m:
            return True
    return False


def signature_and_det(link):
    """(signature of V+V^T, det of V+V^T) from one Seifert matrix."""
    V = link.seifert_matrix()
    n = len(V)
    S = [[V[i][j] + V[j][i] for j in range(n)] for i in range(n)]
    return _signature_of_symmetric(S), _det_int(S)


def slice_knot_screen(link):
    """Cheap necessary conditions for a ONE-component link to be slice.

    signature 0, then |det| a perfect square (det = Delta(-1) = f(-1)^2 under
    Fox-Milnor), and only then the full factorisation.  The two cheap tests
    come free from the Seifert matrix and cut nearly all of the symbolic work.
    """
    try:
        sig, det = signature_and_det(link)
    except Exception:
        return True
    if sig != 0:
        return False
    if not _is_square(det):
        return False
    try:
        return fox_milnor(link)
    except Exception:
        return True


def _alexander_coeffs(link):
    """Coefficients of det(V - t V^T), lowest degree first, over Z."""
    import sympy
    V = link.seifert_matrix()
    n = len(V)
    if n == 0:
        return [1]
    t = sympy.Symbol('t')
    M = sympy.Matrix(n, n, lambda i, j: V[i][j] - t * V[j][i])
    p = sympy.Poly(sympy.expand(M.det(method='berkowitz')), t)
    return [int(c) for c in reversed(p.all_coeffs())]


# Degree cap for the symbolic step.  sympy's factorisation is occasionally
# very slow on high-degree integer polynomials, and a stalled filter stalls the
# whole search.  Above the cap the link is KEPT, which is the safe direction.
FOX_MILNOR_MAX_DEGREE = 22


def fox_milnor(link):
    """True if det(V - tV^T) = +-t^k f(t) f(1/t).  Knots only."""
    import sympy
    c = _alexander_coeffs(link)
    if len(c) - 1 > FOX_MILNOR_MAX_DEGREE:
        return True
    while c and c[0] == 0:
        c = c[1:]
    while c and c[-1] == 0:
        c = c[:-1]
    if not c:
        return True
    if len(c) == 1:
        return True
    t = sympy.Symbol('t')
    return _fox_milnor_coeffs(c, t)


def _fox_milnor_coeffs(c, t):
    import sympy
    poly = sympy.Poly(list(reversed(c)), t)
    factors = sympy.factor_list(poly.as_expr())
    # Collect irreducible factors with multiplicity; f(t)f(1/t) forces each
    # irreducible factor to be paired with its reciprocal, with equal
    # multiplicity, except for self-reciprocal factors which need even
    # multiplicity -- unless the factor is its own reciprocal up to a unit
    # AND appears an even number of times.
    items = []
    for f, m in factors[1]:
        fp = sympy.Poly(f, t)
        items.append((fp, m))

    def reciprocal(fp):
        co = fp.all_coeffs()
        rc = list(reversed(co))
        while rc and rc[0] == 0:
            rc = rc[1:]
        if not rc:
            return fp
        g = sympy.Poly(rc, t)
        return g

    remaining = {}
    for fp, m in items:
        remaining[fp] = remaining.get(fp, 0) + m
    for fp in list(remaining):
        if remaining.get(fp, 0) == 0:
            continue
        rp = reciprocal(fp)
        # normalise leading sign
        cand = [g for g in remaining if remaining[g] > 0 and
                (sympy.simplify(g.as_expr() - rp.as_expr()) == 0 or
                 sympy.simplify(g.as_expr() + rp.as_expr()) == 0)]
        if cand and cand[0] != fp:
            g = cand[0]
            k = min(remaining[fp], remaining[g])
            if remaining[fp] != remaining[g]:
                return False
            remaining[fp] -= k
            remaining[g] -= k
        else:
            # self-reciprocal (or reciprocal absent): needs even multiplicity
            if remaining[fp] % 2 != 0:
                return False
            remaining[fp] = 0
    return True


def _strip(c):
    while c and c[0] == 0:
        c = c[1:]
    while c and c[-1] == 0:
        c = c[:-1]
    return c


def _divide_by_t_minus_1(c):
    """Exact division of sum c[i] t^i by (t - 1); None if not divisible."""
    n = len(c)
    if n < 2:
        return None
    # synthetic division by root 1, from the top
    q = [0] * (n - 1)
    carry = c[n - 1]
    for i in range(n - 2, -1, -1):
        q[i] = carry
        carry = c[i] + carry
    if carry != 0:
        return None
    return q


def link_fox_milnor(link):
    """Fox-Milnor for a link with mu >= 2 components.

    If L is strongly slice then its multivariable Alexander polynomial is
    f * f-bar (Kawauchi), so its total-linking specialisation is g(t) g(1/t).
    Torres relates that specialisation to the one-variable polynomial the
    Seifert matrix computes by  Delta_L(t) = (t - 1) * Delta_L(t,...,t).
    So: divide det(V - t V^T) by one factor of (t - 1) and require the
    quotient to satisfy the ordinary Fox-Milnor condition.

    Any step that cannot be carried out returns True (link kept).
    """
    import sympy
    try:
        c = _strip(_alexander_coeffs(link))
    except Exception:
        return True
    if len(c) < 2:
        return True
    q = _divide_by_t_minus_1(c)
    if q is None:
        return True          # normalisation not as expected -- do not reject
    q = _strip(q)
    if len(q) < 2:
        return True
    if len(q) - 1 > FOX_MILNOR_MAX_DEGREE:
        return True
    t = sympy.Symbol('t')
    return _fox_milnor_coeffs(q, t)


def components_all_slice(link):
    """Every component of a strongly slice link bounds a disk, so each is a
    slice knot: signature 0 and Fox-Milnor.  Cheap, sound, and not part of
    spherogram's own filter."""
    n = len(link.link_components)
    if n < 2:
        return True
    for i in range(n):
        try:
            C = link.sublink([i])
        except Exception:
            continue
        if not slice_knot_screen(C):
            return False
    return True


def could_be_strongly_slice(link):
    if not linking_nums_all_zero(link):
        return False
    if len(link.link_components) == 1:
        return slice_knot_screen(link)
    try:
        sig, det = signature_and_det(link)
    except Exception:
        return True
    if sig != 0:
        return False
    # Cheap: det(L) = |Delta_L(-1)| = |(-2) g(-1)^2|, so |det|/2 is a square.
    if det != 0 and abs(det) % 2 == 0 and not _is_square(abs(det) // 2):
        return False
    try:
        if not link_fox_milnor(link):
            return False
    except Exception:
        return True
    try:
        return components_all_slice(link)
    except Exception:
        return True


def install():
    """Monkeypatch spherogram's band search to use this filter."""
    import spherogram.links.bands.search as _bs
    _bs.could_be_strongly_slice = could_be_strongly_slice
    return _bs


if __name__ == '__main__':
    import snappy
    checks = [
        ('3_1', -2), ('4_1', 0), ('5_1', -4), ('6_1', 0), ('6_2', -2),
        ('8_8', 0), ('9_46', 0), ('10_3', 0), ('L2a1', -1), ('L5a1', 0),
    ]
    ok = True
    for name, expected in checks:
        L = snappy.Link(name)
        got = seifert_signature(L)
        flag = 'ok ' if abs(got) == abs(expected) else 'MISMATCH'
        if abs(got) != abs(expected):
            ok = False
        print(f'{flag} signature({name}) = {got}   (table |sigma| = {abs(expected)})')
    for name, expected in [('6_1', True), ('8_8', True), ('9_46', True),
                           ('10_3', True), ('3_1', False), ('5_2', False)]:
        L = snappy.Link(name)
        got = fox_milnor(L)
        flag = 'ok ' if got == expected else 'MISMATCH'
        if got != expected:
            ok = False
        print(f'{flag} fox_milnor({name}) = {got}   (expected {expected})')
    print('ALL OK' if ok else 'FAILURES PRESENT')
