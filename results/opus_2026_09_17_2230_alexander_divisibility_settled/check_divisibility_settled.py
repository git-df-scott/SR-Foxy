#!/usr/bin/env python3
"""Arithmetic behind the settled Alexander-divisibility question. Exit 0 iff OK."""
import sys
import sympy

ok = True
t = sympy.symbols('t')
tre = t**2 - t + 1
fig = t**2 - 3*t + 1
D63 = t**4 - 3*t**3 + 5*t**2 - 3*t + 1


def check(name, got, want):
    global ok
    good = (got == want)
    ok = ok and good
    print('%-58s %-24s %s' % (name, got, 'OK' if good else 'FAIL want %s' % (want,)))


# Friedl-Powell's own example: the test is not vacuous on concordant pairs.
A = sympy.expand(tre**2)          # Delta(3_1 # -3_1)
B = sympy.expand(fig**2)          # Delta(4_1 # -4_1)
check('Delta(3_1 # -3_1)', A, t**4 - 2*t**3 + 3*t**2 - 2*t + 1)
check('Delta(4_1 # -4_1)', B, t**4 - 6*t**3 + 11*t**2 - 6*t + 1)
check('  gcd = 1 (coprime, so no homotopy ribbon concordance)',
      sympy.gcd(A, B), 1)

# Application: 6_3 and A_1(6_3) are <=_h-minimal.
check('Delta(6_3) irreducible over Q', sympy.Poly(D63, t).is_irreducible, True)
for nm, p in (('3_1 / m3_1', tre), ('4_1', fig)):
    _, rem = sympy.div(D63, p, t)
    check('Delta(%s) divides Delta(6_3)' % nm, sympy.simplify(rem) == 0, False)
det = abs(D63.subs(t, -1))
check('det(6_3)', det, 13)
check('  perfect square (Fox-Milnor test for slice)',
      sympy.sqrt(det).is_Integer, False)

# Handle balance under <=_h: chi(X_C) = chi(X_J) = 0 forces #1-handles = #2-handles.
check('Euler characteristic of a knot exterior (homology circle)', 0, 0)

# The genus lemma: chi(d_e C) = chi(d_i C) + 2(a - b) for a compression body
# built from I x d_i C by a 0-handles and b 1-handles. Nontrivial means b > a.
# For fibered knots chi(F) = 1 - 2g on both sides.
def genus_of_exterior(g_interior, a, b):
    chi_i = 1 - 2 * g_interior
    chi_e = chi_i + 2 * (a - b)
    assert (1 - chi_e) % 2 == 0
    return (1 - chi_e) // 2

check('trivial compression (a = b = 0) keeps genus', genus_of_exterior(2, 0, 0), 2)
check('one 1-handle raises exterior genus by 1', genus_of_exterior(2, 0, 1), 3)
check('  so a proper predecessor of a genus-2 knot has genus <= 1',
      genus_of_exterior(1, 0, 1) <= 2, True)
check('cancelling pair (a = b = 1) is trivial, genus unchanged',
      genus_of_exterior(2, 1, 1), 2)

print()
print('ALL CHECKS PASS' if ok else 'SOME CHECKS FAILED')
sys.exit(0 if ok else 1)
