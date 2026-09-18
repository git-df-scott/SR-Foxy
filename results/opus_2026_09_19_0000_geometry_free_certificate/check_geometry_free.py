#!/usr/bin/env python3
"""The Abe-Tagami non-ribbon certificate needs no geometry at all.

Miyazaki Thm 5.5 and Agol-Ren Thm 1.13 both quantify over PRIME FIBERED knots,
and the campaign's use of them also needs K_0 != K_1 and an irreducible Alexander
polynomial.  Until now three of those four facts rested on SnapPy's numerical
hyperbolic geometry - volume comparisons and is_isometric_to - with primality
inferred from "hyperbolic implies prime".  verify_hyperbolicity(), which would
make that rigorous, requires Sage and is unavailable in this container.

It is not needed.  Every hypothesis can be certified combinatorially.

  LEMMA P.  A fibered knot with irreducible Alexander polynomial is prime.
  If K = K1 # K2 is fibered then both summands are fibered and
  Delta_K = Delta_K1 * Delta_K2.  Irreducibility forces some Delta_Ki = 1; a
  fibered knot has deg Delta = 2g, so that summand has g = 0 and is the unknot.
  The decomposition is therefore trivial.  []

  FIBEREDNESS is combinatorial by Ni's theorem (Ghiggini in genus 1): K is
  fibered iff HFK-hat(K, g(K)) has rank 1.  Checked directly here, not taken
  from the calculator's summary flag.

  DISTINCTNESS is combinatorial: the bigraded HFK groups differ, so no volume
  comparison or isometry test is involved.

Exit 0 iff every check passes.  spherogram + sympy only; no geometry, no Sage.
"""
import json
import os
import sys
from collections import defaultdict

import spherogram
import sympy as sp

t = sp.Symbol("t")
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TARGETS = [("K_0", "AbeTagami_K_0_K_-1__6_3"), ("K_1", "AbeTagami_K_1")]
checks = []


def check(name, ok, detail):
    checks.append({"name": name, "pass": bool(ok), "detail": str(detail)})
    return bool(ok)


def alexander(ranks):
    poly = defaultdict(int)
    for (A, M), r in ranks.items():
        poly[A] += ((-1) ** M) * r
    lo = min(poly)
    c = sp.Poly(sum(v * t ** (A - lo) for A, v in poly.items()), t).all_coeffs()[::-1]
    while c and c[0] == 0:
        c = c[1:]
    if sum(c) < 0:
        c = [-x for x in c]
    return sp.Poly(sum(int(v) * t**k for k, v in enumerate(c)), t)


def main():
    data = {}
    for name, stem in TARGETS:
        with open(os.path.join(REPO, "data", "knots", stem + ".json")) as fh:
            pd = json.load(fh)["pd_code"]
        h = spherogram.Link(pd).knot_floer_homology()
        ranks = dict(h["ranks"])
        g = h["seifert_genus"]
        top = sum(r for (A, M), r in ranks.items() if A == g)
        P = alexander(ranks)
        data[name] = {"genus": g, "top_rank": top, "irreducible": bool(P.is_irreducible),
                      "degree": P.degree(), "delta_levels": sorted({M - A for (A, M) in ranks}),
                      "ranks": {f"{A},{M}": r for (A, M), r in sorted(ranks.items())},
                      "alexander": str(P.as_expr())}
        d = data[name]
        check(f"{name}: fibered by Ni (rank 1 at top Alexander grading)", top == 1, top)
        check(f"{name}: deg Delta = 2g", d["degree"] == 2 * g, f"{d['degree']} vs {2*g}")
        check(f"{name}: Delta irreducible over Q", d["irreducible"], d["alexander"])
        check(f"{name}: PRIME by Lemma P", top == 1 and d["irreducible"],
              "fibered + irreducible Delta => prime, with no geometry")

    check("K_0 != K_1 by bigraded HFK alone",
          data["K_0"]["ranks"] != data["K_1"]["ranks"],
          f"delta levels {data['K_0']['delta_levels']} vs {data['K_1']['delta_levels']}")
    check("the two Alexander polynomials agree",
          data["K_0"]["alexander"] == data["K_1"]["alexander"], data["K_0"]["alexander"])
    # Miyazaki's alternative 2 for each summand.
    check("Miyazaki alternative 2 holds for each summand",
          data["K_0"]["irreducible"] and data["K_1"]["irreducible"],
          "irreducible Delta admits no f with f(t)f(1/t) | Delta")

    n_pass = sum(1 for c in checks if c["pass"])
    out = {"all_checks_pass": n_pass == len(checks), "n_checks": len(checks),
           "n_pass": n_pass, "checks": checks, "data": data,
           "conclusion":
               "Every hypothesis the Abe-Tagami non-ribbon certificate needs -"
               " prime, fibered, distinct, irreducible Delta - is certified"
               " combinatorially. The certificate no longer depends on SnapPy"
               " volumes, is_isometric_to, or hyperbolicity.",
           "gap_recorded":
               "verify_hyperbolicity() requires Sage and is unavailable here, so"
               " the hyperbolicity claims elsewhere in the repository remain"
               " numerical. They are not needed for this certificate.",
           "not_established_here": [
               "Nothing about whether D_{0,1} is slice; only the non-ribbon half.",
               "Ni's theorem and Miyazaki Thm 5.5 are cited, not reproved.",
               "The PD codes are taken from data/knots as committed."],
           "spherogram_version": spherogram.__version__,
           "sympy_version": sp.__version__}
    print(json.dumps(out, indent=1))
    return 0 if out["all_checks_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
