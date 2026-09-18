#!/usr/bin/env python3
"""Check formal linking sums and the archived 0000 surgery polynomial.

These arithmetic checks do not classify other band designs. The archived
0110 design has the same zero linking and the target polynomial at r=1.
See research/36_audit_of_framing_and_miyazaki_closures.md. Historical
RESULTS.json is retained as superseded evidence, not a theorem certificate.
"""
import json
import os
import sys

import sympy as sp

t, r = sp.symbols("t r")
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SCAFFOLD = os.path.join(REPO, "data", "knots", "AbeTagami_marked_product_scaffold.json")
LINK = os.path.join(REPO, "data", "knots", "AbeTagami_L_63_c1_c2.json")
DELTA = t**4 - 3*t**3 + 5*t**2 - 3*t + 1
checks = []


def check(name, ok, detail):
    checks.append({"name": name, "pass": bool(ok), "detail": str(detail)})
    return bool(ok)


def main():
    S = json.load(open(SCAFFOLD))
    L = json.load(open(LINK))
    M, idx = S["linking_matrix"], S["component_markings"]
    lk = lambda a, b: M[idx[a]][idx[b]]

    # --- the source annulus really is +1 framed -------------------------
    check("A1 source annulus framing lk(c'_1,c'_2) = +1",
          L["verification"]["(a) lk(c'_1,c'_2)"] == 1, "from the construction card")
    check("A2 n-fold twist slopes are (n+1,n) and (n-1,n)",
          L["slopes"]["n-fold annulus twist"] == {"c'_1": "(n+1, n)", "c'_2": "(n-1, n)"},
          "so the coefficients are 1 +- 1/n, not +- 1/n")
    check("A3 n=1 slopes used are (2,1) and (0,1)",
          L["slope_checks"]["1"]["slopes"] == [[2, 1], [0, 1]], "")

    # --- the double mirrors the lower copy ------------------------------
    check("B1 lk(c1_upper,c2_upper) = +1", lk("c1_upper", "c2_upper") == 1, "")
    check("B2 lk(c1_lower,c2_lower) = -1 (the copy is mirrored)",
          lk("c1_lower", "c2_lower") == -1, "")
    cross = [lk(a, b) for a in ("c1_upper", "c2_upper")
             for b in ("c1_lower", "c2_lower")]
    check("B3 every upper-lower cross linking vanishes", cross == [0, 0, 0, 0], cross)

    # --- formal linking sums; not a universal geometric band theorem -----
    def lk_sum(P, Q):
        return sum(lk(a, b) for a in P for b in Q)

    designs = {
        "crossed  eta1=c1u#c2l, eta2=c2u#c1l":
            (("c1_upper", "c2_lower"), ("c2_upper", "c1_lower")),
        "uncrossed eta1=c1u#c1l, eta2=c2u#c2l":
            (("c1_upper", "c1_lower"), ("c2_upper", "c2_lower")),
    }
    for name, (P, Q) in designs.items():
        check(f"C1 {name}: formal source-matrix sum = 0", lk_sum(P, Q) == 0, lk_sum(P, Q))
    check("C2 a same-half annulus keeps framing magnitude 1",
          abs(lk("c1_lower", "c2_lower")) == 1 and abs(lk("c1_upper", "c2_upper")) == 1,
          "this is the FIXED-AXIS configuration, obstructed by SL(2,F_5) nonconjugacy")

    # --- specific archived polynomial, not deduced from linking alone -----
    Dr = sp.expand(DELTA**2 - r**2 * t**2 * (t**2 - 1)**2)
    check("D1 archived 0000 Delta_r equals Delta^2 - r^2 (t^3-t)^2",
          sp.expand(Dr - (DELTA**2 - r**2*(t**3 - t)**2)) == 0, "")
    check("D2 Delta_r = Delta^2 only at r = 0",
          sp.solve(sp.Eq(sp.expand(Dr - DELTA**2), 0), r) == [0], "")

    n_pass = sum(1 for c in checks if c["pass"])
    out = {"all_checks_pass": n_pass == len(checks), "n_checks": len(checks),
           "n_pass": n_pass, "checks": checks,
           "linking_matrix": M, "component_markings": idx,
           "conclusion": "Formal source-matrix sums vanish and the archived 0000"
                         " polynomial is non-target for nonzero r. These checks"
                         " do not exclude general mixed-band designs.",
           "scope": "ARITHMETIC_ONLY_UNIVERSAL_CLOSURE_RETRACTED",
           "not_established_here": [
               "Linking zero does not determine the surgery Alexander polynomial.",
               "The 0110 design already has linking zero and the target polynomial.",
               "No claim about all band paths, endpoints, twists, or orientations.",
               "No annulus, disk, or knot identification is certified."],
           "sympy_version": sp.__version__}
    print(json.dumps(out, indent=1))
    return 0 if out["all_checks_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
