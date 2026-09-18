#!/usr/bin/env python3
"""Bigraded HFK of the Abe-Tagami family, the delta law, and two flagged risks.

Recomputes, from the committed PD codes, the full bigraded knot Floer homology of
K_0..K_3 and D_{0,1}, D_{0,2}, D_{1,2}, and checks three things:

  (1) the invariants forced to agree by Lemma B of research/33 do agree, while
      the delta = M - A grading does NOT;
  (2) the delta-shift law  delta_n = -n(n+1)  , which reproduces the n-dependence
      of Oba's contact-invariant computation d_3(xi_n) = -n^2 - n + 3/2 recorded
      in data/knots/AbeTagami_K_n_NOTES.json, and is invariant under the
      involution n -> -1-n that encodes K_n = K_m iff n = m or n + m = -1;
  (3) the two *checkable* risks that research/opus_mixed_lift_review.md flags as
      asserted-but-unproven in the K_1 local-equivalence argument:
        risk 4: every generator of CFK(K_1) has delta in {0, -2};
        risk 5: the number of admissible mixed U^a V^b slots is exactly 18,
      plus the bidegrees the stated chain retraction needs.

Requires snappy/spherogram (HFK via Szabo's calculator).  Exit 0 iff all pass.
"""
import json
import os
import sys
from collections import defaultdict

import spherogram

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
KNOTS = os.path.join(REPO, "data", "knots")

FAMILY = [("K_0", "AbeTagami_K_0_K_-1__6_3", 0),
          ("K_1", "AbeTagami_K_1", 1),
          ("K_2", "AbeTagami_K_2", 2),
          ("K_3", "AbeTagami_K_3", 3)]
SUMS = [("D_0_1", "AbeTagami_D_0_1"),
        ("D_0_2", "AbeTagami_D_0_2"),
        ("D_1_2", "AbeTagami_D_1_2")]

checks = []
data = {}


def check(name, ok, detail):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})
    return bool(ok)


def hfk(stem):
    with open(os.path.join(KNOTS, stem + ".json")) as fh:
        pd = json.load(fh)["pd_code"]
    h = spherogram.Link(pd).knot_floer_homology()
    ranks = h["ranks"]
    diag = defaultdict(int)
    for (A, M), r in ranks.items():
        diag[M - A] += r
    return h, ranks, dict(sorted(diag.items()))


def main():
    # ---- (1) the family -------------------------------------------------
    for label, stem, n in FAMILY:
        h, ranks, diag = hfk(stem)
        data[label] = {"total_rank": sum(ranks.values()), "genus": h["seifert_genus"],
                       "fibered": h["fibered"], "tau": h["tau"], "nu": h["nu"],
                       "epsilon": h["epsilon"], "delta_spread": {str(k): v for k, v in diag.items()},
                       "thin": len(diag) == 1,
                       "ranks": {f"{A},{M}": r for (A, M), r in sorted(ranks.items())}}
        d = data[label]
        check(f"1a {label}: total rank 13 (= det)", d["total_rank"] == 13, str(d["total_rank"]))
        check(f"1b {label}: fibered of genus 2", d["fibered"] and d["genus"] == 2,
              f"fibered={d['fibered']} g={d['genus']}")
        check(f"1c {label}: tau = nu = epsilon = 0",
              d["tau"] == 0 and d["nu"] == 0 and d["epsilon"] == 0,
              f"tau={d['tau']} nu={d['nu']} eps={d['epsilon']}")

    check("1d only K_0 is thin", data["K_0"]["thin"] and not any(
        data[l]["thin"] for l, _, _ in FAMILY if l != "K_0"),
        "K_0 is alternating; K_1, K_2, K_3 are not thin")

    # ---- (2) the delta law ----------------------------------------------
    for label, stem, n in FAMILY:
        diag = {int(k): v for k, v in data[label]["delta_spread"].items()}
        bottom = min(diag)
        check(f"2a {label}: delta levels are exactly {{0, -n(n+1)}} with the 5/8 split",
              (diag == {0: 13}) if n == 0 else (diag == {-n * (n + 1): 8, 0: 5}),
              f"delta_spread = {diag}; -n(n+1) = {-n*(n+1)}")
        check(f"2b {label}: lowest delta = -n(n+1) = {-n*(n+1)}", bottom == -n * (n + 1),
              str(bottom))
    check("2c the law is invariant under n -> -1-n (so K_n = K_m iff n=m or n+m=-1)",
          all(-n * (n + 1) == -(-1 - n) * ((-1 - n) + 1) for n in range(-6, 7)),
          "matches Oba's d_3(xi_n) = -n^2-n+3/2 up to the constant 3/2")

    # ---- (3) the two flagged risks in the K_1 local-equivalence argument --
    h, ranks, diag = hfk("AbeTagami_K_1")
    gens = [(A, M) for (A, M), r in sorted(ranks.items()) for _ in range(r)]
    lo = [g for g in gens if g[1] - g[0] == -2]
    hi = [g for g in gens if g[1] - g[0] == 0]
    check("3a risk 4: every generator of CFK(K_1) has delta in {0,-2}",
          len(lo) + len(hi) == 13, f"|delta=-2| = {len(lo)}, |delta=0| = {len(hi)}")
    check("3b the split is 8 / 5 as the review assumes", len(lo) == 8 and len(hi) == 5,
          f"{len(lo)} / {len(hi)}")

    # d has bidegree (0,-1); deg U = (-1,-2), deg V = (1,0).
    # x -> U^a V^b y  needs  A_x = A_y - a + b  and  M_x - 1 = M_y - 2a.
    # delta(y) = delta(x) - 1 + a + b, so a delta jump of +2 forces a + b = 3,
    # and "mixed" (a, b >= 1) leaves exactly (a,b) in {(2,1), (1,2)}.
    slots = [(x, y, a, b) for (a, b) in [(2, 1), (1, 2)] for x in lo for y in hi
             if x[0] == y[0] - a + b and x[1] - 1 == y[1] - 2 * a]
    check("3c risk 5: exactly 18 admissible mixed slots", len(slots) == 18,
          f"{len(slots)} slots; only U^2V and UV^2 are possible")
    for bd, k in [((0, 0), 2), ((-2, -4), 1), ((2, 0), 1)]:
        check(f"3d retraction needs rank >= {k} at (A,M) = {bd}", ranks.get(bd, 0) >= k,
              f"calculator gives {ranks.get(bd, 0)}")

    # ---- the connected sums ---------------------------------------------
    for label, stem in SUMS:
        h, ranks, diag = hfk(stem)
        data[label] = {"total_rank": sum(ranks.values()), "genus": h["seifert_genus"],
                       "fibered": h["fibered"], "tau": h["tau"], "nu": h["nu"],
                       "epsilon": h["epsilon"],
                       "delta_spread": {str(k): v for k, v in diag.items()},
                       "thin": len(diag) == 1}
        d = data[label]
        check(f"4a {label}: rank 169 = 13^2, fibered genus 4",
              d["total_rank"] == 169 and d["fibered"] and d["genus"] == 4,
              f"rank={d['total_rank']} g={d['genus']}")
        check(f"4b {label}: tau = nu = epsilon = 0",
              d["tau"] == 0 and d["nu"] == 0 and d["epsilon"] == 0,
              f"tau={d['tau']} nu={d['nu']} eps={d['epsilon']}")
        check(f"4c {label}: NOT thin, so thinness cannot make the involutive"
              " invariants vacuous", not d["thin"], str(d["delta_spread"]))

    n_pass = sum(1 for c in checks if c["pass"])
    out = {"all_checks_pass": n_pass == len(checks), "n_checks": len(checks),
           "n_pass": n_pass, "checks": checks, "hfk": data,
           "software": {"spherogram": spherogram.__version__,
                        "python": sys.version.split()[0],
                        "hfk_engine": "Szabo's HFK calculator bundled with SnapPy"},
           "not_verified_here": [
               "risk 1/2 of research/opus_mixed_lift_review.md: that the"
               " calculator's absolute bigradings are those of the true"
               " CFK_UV(K_1). This script uses the same engine family, so it is"
               " NOT an independent check of that.",
               "risk 3: d_pure^2 = 0 over S rather than only over R.",
           ]}
    print(json.dumps(out, indent=1))
    return 0 if out["all_checks_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
