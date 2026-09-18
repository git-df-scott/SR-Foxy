#!/usr/bin/env python3
"""Harden the identification of the stored K_1 with A_1(6_3).

Why this matters.  results/opus_2026_09_19_0000_geometry_free_certificate/ made
the Abe-Tagami NON-RIBBON certificate combinatorial: prime, fibered, distinct and
irreducible-Delta are all certified without geometry.  It also named the one
dependency left: the stored K_1 PD code is identified with A_1(6_3) only through
the construction card's numerical Dehn filling, checked with is_isometric_to.

That is the weakest call in the lane.  is_isometric_to has failed this campaign
twice tonight - it throws on closed manifolds, and a possibly-numerical False was
nearly recorded as a certified exclusion.

This pass replaces it with the ORIENTED isometry signature, computed from the
CANONICAL retriangulation.  Unlike the isoSig-after-random-simplify method
retracted in research/34, the canonical retriangulation depends only on the
isometry type, so equal signature means isometric.  ignore_orientation=False is
mandatory: the default returns the UNORIENTED invariant and gives a manifold and
its mirror byte-identical signatures.

Control built in: filling L at the n = 0 slopes (1,0), (-1,0) must return 6_3,
since the zero-fold annulus twist is the identity.  If that control failed, a
match at n = 1 would mean nothing.

By Gordon-Luecke a knot in S^3 is determined by its complement, so an oriented
isometry of exteriors identifies the knots.

RESIDUAL GAP, recorded rather than hidden: isometry_signature(verified=True)
raises SageNotAvailable in this container, so the canonical retriangulation is
found numerically.  This is a high-confidence identification, not a proof.

Exit 0 iff every check passes.
"""
import json
import os
import sys

import snappy
import spherogram

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
KN = os.path.join(REPO, "data", "knots")
checks = []


def check(name, ok, detail):
    checks.append({"name": name, "pass": bool(ok), "detail": str(detail)})
    return bool(ok)


def osig_from_pd(pd):
    M = snappy.ManifoldHP(spherogram.Link(pd).exterior())
    return M.isometry_signature(ignore_orientation=False)


def main():
    stored = {}
    for nm, f in [("K_0", "AbeTagami_K_0_K_-1__6_3"), ("K_1", "AbeTagami_K_1")]:
        stored[nm] = osig_from_pd(json.load(open(os.path.join(KN, f + ".json")))["pd_code"])

    L = json.load(open(os.path.join(KN, "AbeTagami_L_63_c1_c2.json")))
    check("L has the 3 components the card names", len(L["component_order"]) == 3,
          L["component_order"])
    check("card's n-fold slopes are (n+1,n) and (n-1,n)",
          L["slopes"]["n-fold annulus twist"] == {"c'_1": "(n+1, n)", "c'_2": "(n-1, n)"},
          L["slopes"])

    X = spherogram.Link(L["pd_code"]).exterior()
    check("L exterior has 3 cusps", X.num_cusps() == 3, X.num_cusps())

    filled = {}
    for n, slopes in [(0, [(1, 0), (-1, 0)]), (1, [(2, 1), (0, 1)])]:
        M = snappy.ManifoldHP(X)
        M.dehn_fill(slopes[0], 1)
        M.dehn_fill(slopes[1], 2)
        filled[n] = M.isometry_signature(ignore_orientation=False)

    # The control first: if this fails, the n = 1 match is worthless.
    check("CONTROL n=0: filling L at (1,0),(-1,0) returns 6_3",
          filled[0] == stored["K_0"], filled[0])
    check("n=1: filling L at (2,1),(0,1) returns the stored K_1",
          filled[1] == stored["K_1"], filled[1])
    check("K_0 and K_1 have different oriented signatures",
          stored["K_0"] != stored["K_1"], "")

    verified_available = True
    try:
        snappy.ManifoldHP(spherogram.Link(
            json.load(open(os.path.join(KN, "AbeTagami_K_1.json")))["pd_code"]
        ).exterior()).isometry_signature(verified=True, ignore_orientation=False)
    except Exception as e:
        verified_available = False
        verr = f"{type(e).__name__}: {e}"
    check("RESIDUAL GAP recorded: verified=True is unavailable here",
          not verified_available, verr if not verified_available else "available")

    n_pass = sum(1 for c in checks if c["pass"])
    out = {"all_checks_pass": n_pass == len(checks), "n_checks": len(checks),
           "n_pass": n_pass, "checks": checks,
           "signatures": {"stored_K_0": stored["K_0"], "stored_K_1": stored["K_1"],
                          "L_filled_n0": filled[0], "L_filled_n1": filled[1]},
           "conclusion":
               "The stored K_1 is identified with the n=1 annulus twist of 6_3 by"
               " matching ORIENTED isometry signatures of the canonical"
               " retriangulation, with the n=0 control returning 6_3. This"
               " replaces the construction card's is_isometric_to call, which is"
               " the weakest kind of check this campaign has relied on.",
           "residual_gap":
               "isometry_signature(verified=True) raises SageNotAvailable here, so"
               " the canonical retriangulation is computed numerically. This is a"
               " high-confidence identification, not a proof. Rerunning inside"
               " Sage with verified=True would close it.",
           "not_established_here": [
               "Nothing about sliceness or concordance.",
               "The PD code of L itself is taken as committed; this does not"
               " re-derive it from Abe-Tagami's figures, which remains the"
               " upstream dependency.",
               "Gordon-Luecke is cited, not reproved."]}
    print(json.dumps(out, indent=1))
    return 0 if out["all_checks_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
