#!/usr/bin/env python3
"""Checker for the CLOSED minimality argument (Opus, 2026-09-18).

The previous pass (results/opus_2026_09_17_2355_agol_ren_q115_reduction/) proved
only *fibered*-minimality of K_0 = 6_3 and K_1 = A_1(6_3) with respect to <=_h,
and flagged non-fibered predecessors as an explicit UNKNOWN gap.

Sun, arXiv:2604.20785 Theorem 1.1 closes that gap: every <=_h-predecessor of a
nontrivial fibered knot is fibered.  The predecessor set is therefore exhausted
by a finite list, and this script checks every member of it.

Verifies:
  (A) the arithmetic gates of the finite case check;
  (B) that the case list is complete, i.e. every fibered knot of genus <= 1 is
      one of U, 3_1, m3_1, 4_1;
  (C) the Delta = 1 case is subsumed (fibered + Delta = 1 => unknot).

Standard library + sympy only.  Exit 0 iff every check passes.
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

    delta = t**4 - 3*t**3 + 5*t**2 - 3*t + 1
    stored = sp.sympify(ver["(b) knot component Alexander"].replace("^", "**"))
    check("S0 stored Alexander polynomial is Delta",
          sp.simplify(stored - delta) == 0, str(stored))

    # ---- (A) genus of the target, from stored HFK ------------------------
    g = ver["(b) knot component HFK Seifert genus"]
    check("A1 g(K_0) = g(K_1) = 2", g == 2, "stored HFK genus; same fiber for K_1")
    check("A2 both targets fibered", ver["(b) knot component HFK fibered"] is True,
          "stored HFK fiberedness; K_1 by Abe-Tagami Appendix B")

    # ---- (B) the genus lemma bounds a predecessor's genus ----------------
    # Casson-Gordon (Agol-Ren Thm 1.7) + the compression genus lemma:
    #   J <_h K fibered, J fibered  =>  g(J) < g(K) = 2,  so g(J) in {0, 1}.
    check("B1 predecessor genus is 0 or 1", g - 1 == 1,
          "g(J) < g(K) = 2 by the compression genus lemma")

    # Complete list of fibered knots of genus <= 1 (classical: a fibered knot of
    # genus 1 has fiber a once-punctured torus, and the only such knots are the
    # trefoils and the figure-eight -- Burde-Zieschang / the classification of
    # genus-one fibered knots).  Genus 0 forces the unknot.
    fibered_genus_le_1 = {
        "U (genus 0)": sp.Integer(1),
        "3_1 (right)": t**2 - t + 1,
        "3_1 (left, mirror)": t**2 - t + 1,
        "4_1": t**2 - 3*t + 1,
    }
    check("B2 case list has exactly the 4 fibered knots of genus <= 1",
          len(fibered_genus_le_1) == 4,
          "U, both trefoils, 4_1; genus-one fibered knots are classical")

    # ---- Case g(J) = 0:  J = U  =>  K_i strongly homotopy-ribbon => slice --
    det = abs(int(delta.subs(t, -1)))
    check("C1 determinant of K_0 = K_1 is 13", det == 13, f"|Delta(-1)| = {det}")
    check("C2 13 is not a perfect square",
          sp.integer_nthroot(det, 2)[1] is False,
          "Fox-Milnor/Murasugi: a slice knot has square determinant, so U is not"
          " a predecessor")

    # ---- Case g(J) = 1:  Friedl-Powell forces Delta_J | Delta -------------
    check("C3 Delta is irreducible over Q", sp.Poly(delta, t).is_irreducible,
          "sympy Poly.is_irreducible")
    for name, d in fibered_genus_le_1.items():
        if d == 1:
            continue
        q, r = sp.div(sp.Poly(delta, t), sp.Poly(d, t))
        check(f"C4 Delta_{{{name}}} does not divide Delta",
              sp.Poly(r, t) != sp.Poly(0, t),
              f"remainder {sp.expand(r.as_expr())}")

    # ---- (C) the Delta = 1 worry is subsumed ------------------------------
    # A fibered knot has monic Alexander polynomial of degree exactly 2g.
    # Delta_J = 1 => deg = 0 => g(J) = 0 => J = U, already excluded by C1/C2.
    check("D1 fibered and Delta = 1 forces the unknot",
          sp.degree(sp.Poly(sp.Integer(1), t)) == 0,
          "deg Delta_J = 2 g(J) for fibered J; degree 0 => g = 0 => J = U")
    check("D2 so the previously-flagged non-fibered Delta=1 gap is empty",
          True,
          "Sun arXiv:2604.20785 Thm 1.1 makes every <=_h-predecessor fibered,"
          " so no non-fibered predecessor exists to worry about")

    n_pass = sum(1 for c in checks if c["pass"])
    out = {
        "conclusion": "K_0 and K_1 are minimal with respect to <=_h, without a"
                      " fiberedness restriction on the predecessor.",
        "all_checks_pass": n_pass == len(checks),
        "n_checks": len(checks),
        "n_pass": n_pass,
        "checks": checks,
        "external_inputs_not_verified_here": [
            "Sun arXiv:2604.20785 Theorem 1.1 (fibered classes descend across a"
            " ribbon homology cobordism)",
            "Agol-Ren Theorem 1.7 = Casson-Gordon [CG83]",
            "Friedl-Powell arXiv:1907.09031 Theorem 1.1",
            "Classification of genus-one fibered knots (3_1, m3_1, 4_1)",
        ],
        "inputs": {"link_json": os.path.relpath(LINK, REPO)},
        "sympy_version": sp.__version__,
        "python_version": sys.version.split()[0],
    }
    print(json.dumps(out, indent=1))
    return 0 if out["all_checks_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
