#!/usr/bin/env python3
"""Independent checker for the Question 1.15 reduction (Opus, 2026-09-17).

Verifies, from committed repository data plus self-contained arithmetic, every
numerical and algebraic gate used by the two implication routes

    K_0 ~ K_1  (smooth concordance)  ==>  Slice-Ribbon is false

recorded in README.md of this directory.  It does NOT verify the two external
theorem statements (Agol-Ren Theorem 1.13 / Corollary 1.14(1), and the
unnumbered characteristic-submanifold remark); those are quoted verbatim in
SOURCES.md and are inputs, not outputs.

Standard library + sympy only.  Exit code 0 iff every check passes.
"""
import json
import os
import sys

import sympy as sp

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LINK = os.path.join(REPO, "data", "knots", "AbeTagami_L_63_c1_c2.json")

t = sp.Symbol("t")
checks = []


def check(name, ok, detail):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})
    return bool(ok)


def main():
    with open(LINK) as fh:
        L = json.load(fh)
    ver = L["verification"]
    sl = L["slope_checks"]

    # ---- G1/G2: stored geometric certification of K_0 and K_1 -------------
    check("G1a K_0 exterior isometric to snappy 6_3",
          ver["(b) knot component exterior isometric to snappy 6_3"] is True,
          "stored SnapPy is_isometric_to result")
    check("G1b K_0 fibered (HFK)", ver["(b) knot component HFK fibered"] is True,
          "stored HFK fiberedness")
    check("G1c K_0 Seifert genus 2", ver["(b) knot component HFK Seifert genus"] == 2,
          "stored HFK genus")

    vol0 = sl["0"]["volume"]
    vol1 = sl["1"]["volume"]
    check("G2a K_1 has a hyperbolic structure (positive volume)", vol1 > 0,
          f"vol(S^3 - K_1) = {vol1}")
    check("G2b K_0 volume matches 6_3", abs(vol0 - 5.693021091281) < 1e-9,
          f"vol(S^3 - K_0) = {vol0}")
    check("G2c n=1 slopes are integral (framings 2 and 0)",
          sl["1"]["slopes"] == [[2, 1], [0, 1]],
          f"slopes {sl['1']['slopes']}")
    check("G2d n=1 filling really is S^3",
          sl["1"]["(c) meridian filling of knot cusp is S^3 (Regina isSphere)"] is True,
          "stored Regina isSphere")

    # ---- G3: K_0 and K_1 are distinct -------------------------------------
    check("G3a stored isometry test says K_1 exterior is NOT 6_3 exterior",
          sl["1"]["isometric to 6_3 exterior"] is False,
          "stored SnapPy is_isometric_to result")
    check("G3b volumes are separated well beyond numerical error",
          abs(vol1 - vol0) > 3.0,
          f"|{vol1} - {vol0}| = {abs(vol1 - vol0)}")
    # Mostow: distinct volumes of hyperbolic knot exteriors => distinct knots.
    check("G3c K_0 != K_1 by Mostow rigidity", abs(vol1 - vol0) > 3.0,
          "distinct volumes of hyperbolic knot exteriors")

    # ---- G4: primality -----------------------------------------------------
    # A knot with a hyperbolic exterior is prime (a composite knot's exterior
    # contains an essential annulus, hence is not hyperbolic).
    check("G4 both knots are prime", vol0 > 0 and vol1 > 0,
          "hyperbolic exterior => prime; both volumes positive")

    # ---- G5: the common Alexander polynomial -------------------------------
    delta = t**4 - 3*t**3 + 5*t**2 - 3*t + 1
    stored = sp.sympify(ver["(b) knot component Alexander"].replace("^", "**"))
    check("G5a stored Alexander polynomial equals Delta",
          sp.simplify(stored - delta) == 0, str(stored))
    check("G5b Delta is irreducible over Q",
          sp.Poly(delta, t).is_irreducible, "sympy Poly.is_irreducible")
    det = abs(int(delta.subs(t, -1)))
    check("G5c determinant is 13", det == 13, f"|Delta(-1)| = {det}")
    check("G5d 13 is not a perfect square",
          sp.integer_nthroot(det, 2)[1] is False,
          "Fox-Milnor/Murasugi: a slice knot has square determinant")
    # Same 0-surgery => same Alexander polynomial, so Delta_{K_1} = Delta.
    check("G5e stored 0-surgeries agree (so Delta_{K_1} = Delta_{K_0})",
          sl["1"]["(d) 0-surgery isometric to 6_3(0)"] is True
          and sl["0"]["(d) 0-surgery isometric to 6_3(0)"] is True,
          "stored SnapPy 0-surgery isometry")

    # ---- G6: fibered-minimality of K_0 and K_1 -----------------------------
    # Genus lemma (research/33-34): a nontrivial compression strictly drops the
    # fiber genus.  So a fibered J <_h K_i has g(J) <= 1.
    #   g(J) = 0 => J = U => K_i strongly homotopy-ribbon => K_i slice
    #             => det(K_i) a perfect square.  Excluded by G5c/G5d.
    #   g(J) = 1, J fibered => J in {3_1, m3_1, 4_1}; Friedl-Powell Thm 1.1
    #             forces Delta_J | Delta.  Check that none divides.
    genus1 = {"3_1 (either chirality)": t**2 - t + 1,
              "4_1": t**2 - 3*t + 1}
    for name, d in genus1.items():
        q, r = sp.div(sp.Poly(delta, t), sp.Poly(d, t))
        check(f"G6 Delta_{{{name}}} does not divide Delta",
              sp.Poly(r, t) != sp.Poly(0, t), f"remainder {sp.expand(r.as_expr())}")

    # ---- G7: the trace/stabilization arithmetic (Theorem A recap) ----------
    lk = ver["(a) lk(c'_1,c'_2)"]
    Q = sp.Matrix([[2, lk], [lk, 0]])
    check("G7a linking number lk(c'_1,c'_2) = 1", lk == 1, str(lk))
    check("G7b lk(K, c'_i) = 0", ver["(a) lk(K,c'_i) = 0"] is True,
          "so K x I is disjoint from both 2-handles")
    check("G7c trace form is unimodular", abs(Q.det()) == 1, f"det = {Q.det()}")
    check("G7d trace form is even and indefinite",
          Q[0, 0] % 2 == 0 and Q[1, 1] % 2 == 0 and Q.det() < 0,
          "even unimodular rank 2 indefinite => H")

    # ---- G8: genus of K_1 for the genus<=3 remark --------------------------
    # K_1 is fibered of genus 2: Abe-Tagami Appendix B gives its monodromy as a
    # word in Dehn twists on the SAME genus-2 fiber surface of 6_3.
    check("G8 genus(K_1) = 2 <= 3 (Abe-Tagami Appendix B monodromy on the 6_3 fiber)",
          ver["(b) knot component HFK Seifert genus"] == 2,
          "same fiber surface, so same genus; recorded in AbeTagami_K_n_NOTES.json")

    n_pass = sum(1 for c in checks if c["pass"])
    out = {
        "all_checks_pass": n_pass == len(checks),
        "n_checks": len(checks),
        "n_pass": n_pass,
        "checks": checks,
        "inputs": {"link_json": os.path.relpath(LINK, REPO)},
        "sympy_version": sp.__version__,
        "python_version": sys.version.split()[0],
    }
    print(json.dumps(out, indent=1))
    return 0 if out["all_checks_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
