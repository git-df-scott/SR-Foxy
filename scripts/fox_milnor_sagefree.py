"""Fox-Milnor test, Sage-free: Delta from the HFK Euler characteristic, factored over Z.

Delta_K(t) = sum_{A,M} (-1)^M rank HFK(K; A, M) t^A   (Ozsvath-Szabo), so snappy's
knot_floer_homology gives Delta exactly, with no Seifert matrix and no Sage.

Fox-Milnor: K slice => Delta_K(t) = +- t^k f(t) f(t^-1).  On the factorisation into
irreducibles over Z this is exactly: every irreducible factor p with p not associate
to its own reverse p* pairs with p* at equal multiplicity, and every self-reciprocal
irreducible factor occurs to even multiplicity.
"""
import sympy
from sympy import symbols, Poly, ZZ
t = symbols('t')

def delta_from_hfk(h):
    poly = {}
    for (A, M), r in h['ranks'].items():
        poly[A] = poly.get(A, 0) + ((-1) ** M) * r
    lo = min(poly)
    # normalise to Z[t] by clearing the t^lo, then fix the sign to be positive on top
    e = sympy.expand(sum(c * t ** (A - lo) for A, c in poly.items()))
    p = Poly(e, t, domain=ZZ)
    # Strip any leftover power of t.  Delta is only defined up to +- t^k, and the
    # shift above can leave one when the lowest Alexander grading has Euler
    # coefficient zero (it does for non-fibered knots).  Leaving it in would put a
    # spurious irreducible factor 't' into the factorisation, which has no reverse
    # and would make every such knot fail Fox-Milnor.  That is a bug, not a result.
    c = p.all_coeffs()
    while len(c) > 1 and c[-1] == 0:
        c = c[:-1]
    p = Poly(c, t, domain=ZZ)
    if p.LC() < 0:
        p = -p
    return p

def reverse(p):
    c = p.all_coeffs()
    return Poly(list(reversed(c)), t, domain=ZZ)

def associate(a, b):
    return a == b or a == -b

def fox_milnor(p):
    """Return (is_norm, explanation, factor_table)."""
    cont, facs = p.factor_list()
    table = [(Poly(f, t, domain=ZZ), e) for f, e in facs]
    unpaired = []
    used = [False] * len(table)
    for i, (f, e) in enumerate(table):
        if used[i]:
            continue
        fr = reverse(f)
        if associate(f, fr) or associate(f, Poly(-fr.as_expr(), t, domain=ZZ)):
            if e % 2:
                unpaired.append(('self-reciprocal %s has ODD multiplicity %d' % (f.as_expr(), e)))
            used[i] = True
            continue
        for j, (g, e2) in enumerate(table):
            if j != i and not used[j] and (associate(g, fr)):
                if e != e2:
                    unpaired.append('%s and its reverse have multiplicities %d != %d'
                                    % (f.as_expr(), e, e2))
                used[i] = used[j] = True
                break
        else:
            unpaired.append('%s has no reverse among the factors' % f.as_expr())
            used[i] = True
    # content must also be a square up to sign for a genuine norm
    if abs(cont) != 1:
        import math
        r = int(math.isqrt(abs(cont)))
        if r * r != abs(cont):
            unpaired.append('content %d is not a perfect square' % cont)
    return (not unpaired), unpaired, table, cont
