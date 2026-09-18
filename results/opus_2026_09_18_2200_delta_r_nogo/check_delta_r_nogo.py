#!/usr/bin/env python3
"""Verify Delta_r algebra; exclude only Miyazaki's norm-free alternative.

See README.md.  Standard library + sympy only.  Exit 0 iff every check passes.
"""
import json
import sys

import sympy as sp

t, r = sp.symbols("t r")
DELTA = t**4 - 3*t**3 + 5*t**2 - 3*t + 1
DUAL_PATH = (t**8 - 6*t**7 + 18*t**6 - 36*t**5 + 47*t**4
             - 36*t**3 + 18*t**2 - 6*t + 1)
RANGE = range(-6, 7)
checks = []


def check(name, ok, detail):
    checks.append({"name": name, "pass": bool(ok), "detail": str(detail)})
    return bool(ok)


def star(p):
    """Reciprocal t^4 p(1/t) of a degree-4 polynomial."""
    return sp.expand(t**4 * p.subs(t, 1/t))


def main():
    Dr = sp.expand(DELTA**2 - r**2 * t**2 * (t**2 - 1)**2)
    f = DELTA + r*(t**3 - t)

    check("A1 Delta_r = f_r(t) t^4 f_r(1/t) identically in Z[r,t]",
          sp.expand(Dr - sp.expand(f * star(f))) == 0, "symbolic in r")
    check("A2 dual-path survivors' polynomial equals Delta_1",
          sp.expand(Dr.subs(r, 1) - DUAL_PATH) == 0, "exact")
    check("A3 det = |Delta_r(-1)| = 169 for every r",
          sp.simplify(Dr.subs(t, -1) - 169) == 0, "symbolic in r")
    check("A4 f_r(-1) = 13 for every r",
          sp.simplify(f.subs(t, -1) - 13) == 0, "symbolic in r")

    # Delta is fixed and t^3 - t is negated by the DEGREE-4 reciprocal p -> t^4 p(1/t),
    # which is the involution that matters here.  (A degree-3 coefficient reversal is
    # the wrong test: t^3 - t has coeffs [1,0,-1,0] and is anti-palindromic only with
    # respect to the degree-4 reciprocal.)
    check("B1 Delta is fixed by the degree-4 reciprocal",
          sp.expand(star(DELTA) - DELTA) == 0, "star(Delta) = Delta")
    check("B2 t^3 - t is negated by the degree-4 reciprocal",
          sp.expand(star(t**3 - t) + (t**3 - t)) == 0, "star(t^3-t) = -(t^3-t)")
    check("B3 hence star(f_r) = Delta - r(t^3-t), so f_r is not symmetric for r != 0",
          sp.expand(star(f) - (DELTA - r*(t**3 - t))) == 0, "symbolic in r")

    for rv in RANGE:
        fr = sp.Poly(f.subs(r, rv), t)
        fs = sp.Poly(star(f.subs(r, rv)), t)
        c = fr.all_coeffs()
        drc = sp.Poly(Dr.subs(r, rv), t).all_coeffs()
        check(f"C1 r={rv}: Delta_r symmetric", drc == drc[::-1], "")
        check(f"C2 r={rv}: f_r irreducible", fr.is_irreducible, "")
        check(f"C3 r={rv}: f_r^* irreducible", fs.is_irreducible, "")
        if rv != 0:
            check(f"C4 r={rv}: f_r NOT symmetric", c != c[::-1], c)
            check(f"C5 r={rv}: f_r and f_r^* are not associates",
                  sp.expand(fr.as_expr() - fs.as_expr()) != 0, "")
            # The only reciprocal-closed subsets of {f_r, f_r*} are {} and both,
            # so the only symmetric divisors of Delta_r are 1 and Delta_r.
            syms = []
            for sub, poly in (("1", sp.Integer(1)), ("f_r", fr.as_expr()),
                              ("f_r*", fs.as_expr()),
                              ("Delta_r", sp.expand(fr.as_expr()*fs.as_expr()))):
                cc = sp.Poly(poly, t).all_coeffs() if poly != 1 else [1]
                if cc == cc[::-1]:
                    syms.append(sub)
            check(f"C6 r={rv}: symmetric divisors are exactly 1 and Delta_r",
                  syms == ["1", "Delta_r"], syms)
        else:
            check("C4 r=0: Delta_0 = Delta^2, the campaign's target",
                  sp.expand(Dr.subs(r, 0) - DELTA**2) == 0, "")

    # Only the norm-free alternative is ruled out; minimality remains open.
    check("D1 alt.2 fails for every r != 0: Delta_r IS the norm f_r f_r^*",
          sp.expand(Dr-f*star(f)) == 0 and sp.Poly(f,t).degree() == 4,
          "f_r is monic of degree four with constant one, hence not a Laurent unit")

    n_pass = sum(1 for c in checks if c["pass"])
    out = {"all_checks_pass": n_pass == len(checks), "n_checks": len(checks),
           "n_pass": n_pass, "checks": checks,
           "conclusion": "The norm-free alternative of Miyazaki 5.5 fails."
                         " The independent minimality alternative is unresolved.",
           "scope": "POLYNOMIAL_CHECKS_NOT_A_BLANKET_MIYAZAKI_EXCLUSION",
           "not_established_here": [
               "Nothing about whether any B_r is slice or minimal.",
               "No knot identification of B_r; a polynomial match is not a knot.",
               "Finite irreducibility checks here cover |r| <= 6; research/36"
               " supplies a separate all-integer proof.",
               "Non-symmetry alone would not imply the symmetric-divisor claim"
               " without the irreducibility argument."],
           "sympy_version": sp.__version__,
           "python_version": sys.version.split()[0]}
    print(json.dumps(out, indent=1))
    return 0 if out["all_checks_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
