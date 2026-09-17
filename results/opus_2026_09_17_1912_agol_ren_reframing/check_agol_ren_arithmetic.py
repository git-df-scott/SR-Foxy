#!/usr/bin/env python3
"""Check the arithmetic behind the Agol-Ren reframing. Exit 0 iff all pass."""
import sys
import sympy

ok = True
t = sympy.symbols('t')
D63 = t**4 - 3*t**3 + 5*t**2 - 3*t + 1


def check(name, got, want):
    global ok
    good = (got == want)
    ok = ok and good
    print('%-56s %-20s %s' % (name, got, 'OK' if good else 'FAIL want %s' % (want,)))


check('Delta(6_3) irreducible over Q', sympy.Poly(D63, t).is_irreducible, True)
det = abs(D63.subs(t, -1))
check('det(6_3) = |Delta(-1)|', det, 13)
check('  is a perfect square (Fox-Milnor test for slice)',
      sympy.sqrt(det).is_Integer, False)

# genus-1 fibered knots are exactly the two trefoils and the figure eight
for nm, p in (('3_1 / m3_1', t**2 - t + 1), ('4_1', t**2 - 3*t + 1)):
    _, rem = sympy.div(D63, p, t)
    check('Delta(%s) divides Delta(6_3)' % nm, sympy.simplify(rem) == 0, False)

roots = [complex(x) for x in sympy.Poly(D63, t).nroots()]
lam_lower = max(abs(x) for x in roots)
check('homological lower bound for lambda(6_3), rounded',
      round(lam_lower, 6), 1.722084)
check('  bound attained by a NON-real root (foliations not orientable)',
      any(abs(abs(x) - lam_lower) < 1e-9 and abs(x.imag) > 1e-9 for x in roots),
      True)
check('lambda(4_1) = (3+sqrt5)/2, rounded', round((3 + 5 ** 0.5) / 2, 6), 2.618034)
print('  -> 1.722084 < 2.618034, but 1.722084 is only a LOWER bound for '
      'lambda(6_3), so 4_1 is NOT excluded by dilatation: UNKNOWN')

print()
print('ALL CHECKS PASS' if ok else 'SOME CHECKS FAILED')
sys.exit(0 if ok else 1)
