#!/usr/bin/env python3
"""Check the stored Abe-Tagami PD codes against the PRIMARY SOURCE, figure-free.

Abe-Tagami, "Fibered knots with the same 0-surgery and the slice-ribbon
conjecture", arXiv:1502.01102, Math. Res. Lett. 23 (2016) 303-323, proof of
Theorem 1.6, states two things about K_0 = 6_3 and K_1 = A(K_0) that are
checkable WITHOUT reading a figure:

  (i)  "K_0 and K_1 have the same irreducible Alexander polynomial
        Delta_{K_0}(t) = Delta_{K_1}(t) = 1 - 3t + 5t^2 - 3t^3 + t^4"
  (ii) "K_0 is the fibered knot 6_3 ... By Gabai's theorem in [20], K_1 is also
        fibered"

Everything the stored construction card asserts about L and its fillings rests
on a PD code taken as committed from the paper's figures.  This script does not
re-derive that PD code -- it cannot, the figures are pictures -- but it checks
the stored knots against every numerical claim the paper makes in words.

Delta is computed Sage-free as the HFK Euler characteristic (Ozsvath-Szabo),
via scripts/fox_milnor_sagefree.delta_from_hfk.

WHAT THIS DOES NOT SHOW: matching Delta does NOT identify K_1 with A_1(6_3).
Many knots share an Alexander polynomial.  This is a necessary condition that
passes, not an identification.  The identification remains the oriented
isometry signature of results/opus_2026_09_19_0300_k1_identification/.
"""
import json, os, sys, sympy, snappy

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from fox_milnor_sagefree import delta_from_hfk, t          # noqa: E402

# Verbatim from arXiv:1502.01102, proof of Theorem 1.6.
STATED_DELTA = 1 - 3*t + 5*t**2 - 3*t**3 + t**4

KNOTS = [("K_0 (=6_3)", "AbeTagami_K_0_K_-1__6_3.json"),
         ("K_1",        "AbeTagami_K_1.json"),
         ("K_2",        "AbeTagami_K_2.json"),
         ("K_3",        "AbeTagami_K_3.json")]


def pd_of(fn):
    d = json.load(open(os.path.join(ROOT, "data", "knots", fn)))
    for k in ("pd_code_snappy_0indexed", "pd_code"):
        if k in d:
            return d[k]
    raise KeyError(fn)


def main():
    checks, results = [], {}
    for tag, fn in KNOTS:
        pd = pd_of(fn)
        h = snappy.Link(pd).knot_floer_homology()
        delta = delta_from_hfk(h).as_expr()
        rec = {
            "crossings": len(pd),
            "delta": str(delta),
            "fibered": bool(h.get("fibered")),
            "seifert_genus": h.get("seifert_genus"),
            "matches_stated_delta": sympy.expand(delta - STATED_DELTA) == 0,
            "delta_irreducible_over_Z": len(sympy.factor_list(delta)[1]) == 1,
        }
        results[tag] = rec
        print(f"{tag:12s} crossings={rec['crossings']:3d} "
              f"fibered={rec['fibered']} genus={rec['seifert_genus']}")
        print(f"             Delta = {delta}")

        checks.append((f"{tag}: Delta equals the polynomial stated in "
                       f"arXiv:1502.01102", rec["matches_stated_delta"]))
        checks.append((f"{tag}: Delta irreducible over Z (paper calls it "
                       f"irreducible)", rec["delta_irreducible_over_Z"]))
        checks.append((f"{tag}: fibered (paper: 6_3 fibered, Gabai for the "
                       f"twists)", rec["fibered"]))
        # An annulus twist is supported in the complement of a fiber surface,
        # so it cannot change the genus.  Paper's Delta has degree 4 = 2g.
        checks.append((f"{tag}: Seifert genus 2, consistent with deg Delta = 4",
                       rec["seifert_genus"] == 2))

    # The family must be MUTUALLY consistent: same Delta across all n is the
    # paper's claim for K_0, K_1 and is forced for the rest by Gabai.
    deltas = {r["delta"] for r in results.values()}
    checks.append(("all stored K_n share one Alexander polynomial",
                   len(deltas) == 1))

    npass = sum(1 for _, ok in checks if ok)
    print()
    for name, ok in checks:
        print(("  PASS  " if ok else "  FAIL  ") + name)
    print(f"\n{npass}/{len(checks)}")

    json.dump({"source": "arXiv:1502.01102, Math. Res. Lett. 23 (2016) 303-323",
               "stated_delta": str(STATED_DELTA),
               "knots": results,
               "checks": [{"name": n, "pass": bool(o)} for n, o in checks],
               "passed": npass, "total": len(checks)},
              open(os.path.join(HERE, "RESULTS.json"), "w"), indent=1)
    return 0 if npass == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
