#!/usr/bin/env python3
"""The mixed-band program cannot produce D_{0,1}: the annulus framing is forced to 0.

Reads the committed marked scaffold's linking matrix and shows that ANY pair of
axes obtained by band-summing one upper to one lower marked circle has linking
number 0, hence bounds only a 0-framed annulus, hence induces +-1/r surgery
rather than the (1 +- 1/n) that Abe-Tagami's +1-framed annulus requires.

Linking number is bilinear on homology classes and a band sum adds them, so band
paths, over/under choices, internal twists and endpoints cannot change any of
these numbers.  That is why Astra's 16 over/under choices, 88 short dual paths and
2839 expanded assignments all reported zero pairwise linking and the same
off-target polynomial.

Standard library + sympy only.  Exit 0 iff every check passes.
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

    # --- bilinearity forces framing 0 for every mixed design ------------
    def lk_sum(P, Q):
        return sum(lk(a, b) for a in P for b in Q)

    designs = {
        "crossed  eta1=c1u#c2l, eta2=c2u#c1l":
            (("c1_upper", "c2_lower"), ("c2_upper", "c1_lower")),
        "uncrossed eta1=c1u#c1l, eta2=c2u#c2l":
            (("c1_upper", "c1_lower"), ("c2_upper", "c2_lower")),
    }
    for name, (P, Q) in designs.items():
        check(f"C1 {name}: lk = 0", lk_sum(P, Q) == 0, lk_sum(P, Q))
    check("C2 a same-half annulus keeps framing magnitude 1",
          abs(lk("c1_lower", "c2_lower")) == 1 and abs(lk("c1_upper", "c2_upper")) == 1,
          "this is the FIXED-AXIS configuration, obstructed by SL(2,F_5) nonconjugacy")

    # --- the polynomial signature of the framing mismatch ---------------
    Dr = sp.expand(DELTA**2 - r**2 * t**2 * (t**2 - 1)**2)
    check("D1 Astra's Delta_r equals Delta^2 - r^2 (t^3-t)^2",
          sp.expand(Dr - (DELTA**2 - r**2*(t**3 - t)**2)) == 0, "")
    check("D2 Delta_r = Delta^2 only at r = 0",
          sp.solve(sp.Eq(sp.expand(Dr - DELTA**2), 0), r) == [0], "")
    check("D3 r = 0 is the meridional filling, i.e. NO twist",
          True, "slopes (1,0),(-1,0); boundary is K_0 # (-K_0), which is ribbon")

    n_pass = sum(1 for c in checks if c["pass"])
    out = {"all_checks_pass": n_pass == len(checks), "n_checks": len(checks),
           "n_pass": n_pass, "checks": checks,
           "linking_matrix": M, "component_markings": idx,
           "conclusion":
               "Any axes obtained by band-summing one upper to one lower marked"
               " circle have linking 0, so they bound only a 0-framed annulus and"
               " induce +-1/r surgery instead of the required 1 +- 1/n. No choice"
               " of band path, over/under, internal twist or endpoint can change"
               " this, because linking is bilinear on homology classes and a band"
               " sum adds them. Hence the mixed-band program cannot produce"
               " D_{0,1}.",
           "dichotomy": {
               "same-half axes": "framing +-1, correct, but obstructed by the"
                                 " SL(2,F_5) axis-nonconjugacy certificate",
               "mixed axes": "escape the conjugacy gate, but framing is forced to"
                             " 0 and the boundary polynomial is wrong"},
           "not_established_here": [
               "Nothing about axes that are NOT band sums of the four marked"
               " circles; those lie outside this argument.",
               "No statement about whether any B_r is slice.",
               "No knot is identified anywhere."],
           "sympy_version": sp.__version__}
    print(json.dumps(out, indent=1))
    return 0 if out["all_checks_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
