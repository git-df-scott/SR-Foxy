#!/usr/bin/env python3
"""The Manolescu-Piccirillo RBG survivors cannot carry a Miyazaki or Hom-Park
non-ribbon certificate: all ten are NON-FIBERED.

Context.  research/24 section 4 identifies an r = 0 super-special RBG pair
(K_B, K_G) as a counterexample generator: the traces are diffeomorphic, so a
ribbon disk for one certifies the other slice, and if that other side carries a
non-ribbon certificate the pair is a slice-ribbon counterexample "with no
concordance coincidence needed anywhere".  It asks whether the lane is live or
"empty for a stupid reason", notes the four r = 0 knots then in data/knots all
have Delta = 1, and concludes "the lane is live, and empty only of the examples
we happen to have built."

New input.  Gukov-Halverson-Manolescu-Ruehle, "Searching for Ribbons with
Machine Learning" (https://web.stanford.edu/~cm5/sliceML.pdf), Section 6, report
the exhaustion of Manolescu-Piccirillo's 3375-pair RBG family: 2522 pairs shown
non-slice, 843 shown ribbon by their Bayesian random walker, 5 more resolved by
other methods, leaving exactly FIVE pairs - ten knots - whose ribbon status is
unknown.  They name them, and observe that the three with r = 0,

    K_{B/G}(0,0,0,1,2,-1),  K_{B/G}(0,0,0,-1,2,1),  K_{B/G}(0,0,-2,0,0,1),

cannot give SPC4 counterexamples but "might produce counterexamples to the
Slice-Ribbon Conjecture".  That is exactly research/24's lane, with the
candidates named.

All ten are already committed in data/knots/ as MP_KB_* and MP_KG_*.

Result.  Every one of the ten is NON-FIBERED, with tau = nu = epsilon = 0.
Both non-ribbon certificates this campaign can apply - Miyazaki Thm 5.5 and
Hom-Park Thm 1.1 - quantify over FIBERED knots.  Neither can reach any of them.
So the lane is empty across the whole MP family, not merely across the examples
previously built.  The three r = 0 pairs additionally all have Delta = 1, so
even the fibered case would collapse: a fibered knot with trivial Alexander
polynomial is the unknot.

This does NOT show the ten are ribbon, or not ribbon, or not slice.  tau, nu and
epsilon all vanish, so no Floer obstruction to sliceness is found here either.
They remain open; they simply cannot be certified non-ribbon by the tools this
campaign has.

Exit 0 iff every check passes.  spherogram + sympy only.
"""
import glob
import json
import os
import sys
from collections import defaultdict

import spherogram
import sympy as sp

t = sp.Symbol("t")
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
R0 = {"0_0_0_1_2_-1", "0_0_0_-1_2_1", "0_0_-2_0_0_1"}   # GHMR: these have r = 0
checks = []


def check(name, ok, detail):
    checks.append({"name": name, "pass": bool(ok), "detail": str(detail)})
    return bool(ok)


def main():
    rows = {}
    for f in sorted(glob.glob(os.path.join(REPO, "data", "knots", "MP_K*.json"))):
        nm = os.path.basename(f)[:-5]
        d = json.load(open(f))
        h = spherogram.Link(d["pd_code"]).knot_floer_homology()
        ranks = dict(h["ranks"])
        poly = defaultdict(int)
        for (A, M), r in ranks.items():
            poly[A] += ((-1) ** M) * r
        # Delta = 1 means the graded Euler characteristic collapses to a single
        # unit, so count the NONZERO coefficients, not the gradings present.
        nz = {A: c for A, c in poly.items() if c != 0}
        delta_trivial = (len(nz) == 1 and abs(next(iter(nz.values()))) == 1)
        rows[nm] = {"crossings": len(d["pd_code"]), "fibered": h["fibered"],
                    "genus": h["seifert_genus"], "tau": h["tau"], "nu": h["nu"],
                    "eps": h["epsilon"], "total_rank": sum(ranks.values()),
                    "delta_is_one": delta_trivial,
                    "euler_char": {str(A): c for A, c in sorted(poly.items()) if c != 0},
                    "params": nm.split("_", 2)[2]}

    check("all ten MP/RBG survivors are present", len(rows) == 10, sorted(rows))
    for nm, r in rows.items():
        check(f"{nm}: NON-fibered", r["fibered"] is False, r["fibered"])
        check(f"{nm}: tau = nu = epsilon = 0",
              r["tau"] == 0 and r["nu"] == 0 and r["eps"] == 0,
              f"{r['tau']},{r['nu']},{r['eps']}")
    r0 = {k: v for k, v in rows.items() if v["params"] in R0}
    check("the six r=0 knots are identified", len(r0) == 6, sorted(r0))
    check("every r=0 knot has Delta = 1",
          all(v["delta_is_one"] for v in r0.values()),
          {k: v["delta_is_one"] for k, v in r0.items()})
    check("no MP survivor can carry a Miyazaki or Hom-Park certificate",
          all(v["fibered"] is False for v in rows.values()),
          "both theorems quantify over fibered knots")

    n_pass = sum(1 for c in checks if c["pass"])
    out = {"all_checks_pass": n_pass == len(checks), "n_checks": len(checks),
           "n_pass": n_pass, "checks": checks, "knots": rows,
           "conclusion":
               "All ten Manolescu-Piccirillo RBG survivors are non-fibered, so"
               " neither Miyazaki Thm 5.5 nor Hom-Park Thm 1.1 can certify any of"
               " them non-ribbon. research/24 section 4's lane is empty across the"
               " whole MP family, not merely across previously built examples.",
           "not_established_here": [
               "Nothing about whether any of the ten is ribbon, non-ribbon, or"
               " slice; tau, nu and epsilon all vanish, so no Floer obstruction to"
               " sliceness is found either. They remain open.",
               "Only the two non-ribbon certificates this campaign can apply are"
               " considered; another theorem could still reach them.",
               "The PD codes are taken from data/knots as committed."],
           "source": "Gukov-Halverson-Manolescu-Ruehle, Searching for Ribbons with"
                     " Machine Learning, https://web.stanford.edu/~cm5/sliceML.pdf,"
                     " Section 6",
           "spherogram_version": spherogram.__version__}
    print(json.dumps(out, indent=1))
    return 0 if out["all_checks_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
