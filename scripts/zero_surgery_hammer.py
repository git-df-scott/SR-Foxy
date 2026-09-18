#!/usr/bin/env python3
"""Hammer a sample of volume-matched 0-surgery pairs to see if ANY confirm.

Context.  Among prime fibered knots with irreducible Alexander polynomial (so
that the Miyazaki criterion applies to their connected sums), 1589 groups have
0-surgeries of equal volume inside a shared Alexander polynomial, giving 2352
pairs.  Those groups do NOT split as the tolerance tightens from 1e-6 to 1e-10,
so the coincidences are real rather than rounding.

Note that a knot and its mirror share an exterior and so occupy a single census
entry; these are genuinely different knots.

SnapPea's is_isometric_to on the closed 0-surgeries usually throws
    RuntimeError: The SnapPea kernel was not able to determine ...
and that failure is triangulation-dependent, so this pass retries hard: high
precision only (the Dirichlet construction fails outright at normal precision)
with many randomize() retries, under a per-pair wall-clock budget.

Verdicts: ISOMETRIC, DISTINCT, or UNDECIDED.  UNDECIDED is never an exclusion.
A confirmed isometry yields an Abe-Tagami-type CANDIDATE pair, not a concordance:
Yasui disproved the Akbulut-Kirby conjecture, so a shared 0-surgery does not imply
concordance.
"""
import json
import sys
import time
from collections import Counter, defaultdict

import snappy

VOLS = "/tmp/claude-0/zero_surgery_volumes.jsonl"
OUT = "/tmp/claude-0/zero_surgery_hammer.json"
TOL = 1e-10
RETRIES = 25
BUDGET = 20.0          # seconds per pair
SAMPLE = int(sys.argv[1]) if len(sys.argv) > 1 else 60

_C = None


def census():
    global _C
    if _C is None:
        _C = snappy.HTLinkExteriors(cusps=1)
    return _C


def surgery(i):
    M = snappy.ManifoldHP(census()[i])
    M.dehn_fill((0, 1))
    return M


def decide(ia, ib):
    t0 = time.time()
    A, B = surgery(ia), surgery(ib)
    for _ in range(RETRIES):
        if time.time() - t0 > BUDGET:
            return None, time.time() - t0
        try:
            return bool(A.is_isometric_to(B)), time.time() - t0
        except Exception:
            pass
        try:
            A.randomize()
            B.randomize()
        except Exception:
            break
    return None, time.time() - t0


def main():
    vols = {}
    for line in open(VOLS):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("vol") is not None:
            vols[d["i"]] = d
    g = defaultdict(list)
    for d in vols.values():
        g[(tuple(d["delta"]), round(d["vol"] / TOL))].append(d)
    groups = [v for v in g.values() if len(v) > 1]
    pairs = [(x[a], x[b]) for x in groups
             for a in range(len(x)) for b in range(a + 1, len(x))]
    print(f"volume-matched groups at tol {TOL:g}: {len(groups)}  pairs: {len(pairs)}")
    print(f"hammering a sample of {min(SAMPLE, len(pairs))}")
    sys.stdout.flush()

    # Spread the sample across the list rather than taking a prefix, so it is
    # not dominated by one Alexander polynomial.
    step = max(1, len(pairs) // SAMPLE)
    sample = pairs[::step][:SAMPLE]

    out, tally = [], Counter()
    t0 = time.time()
    for k, (A, B) in enumerate(sample):
        verdict, dt = decide(A["i"], B["i"])
        v = "ISOMETRIC" if verdict is True else (
            "DISTINCT" if verdict is False else "UNDECIDED")
        tally[v] += 1
        rec = {"a": A["name"], "b": B["name"], "vol": A["vol"],
               "delta": A["delta"], "verdict": v, "seconds": round(dt, 1)}
        out.append(rec)
        if v == "ISOMETRIC":
            print("   *** ISOMETRIC:", rec)
            sys.stdout.flush()
        if k and k % 10 == 0:
            print(f"  {k}/{len(sample)}  {time.time()-t0:.0f}s  {dict(tally)}")
            sys.stdout.flush()
    print("TALLY:", dict(tally))
    json.dump({"sampled": len(sample), "total_pairs": len(pairs),
               "total_groups": len(groups), "tally": dict(tally), "results": out,
               "caveats": [
                   "UNDECIDED is not an exclusion.",
                   "A shared 0-surgery does not imply concordance"
                   " (Yasui disproved Akbulut-Kirby).",
                   "Scope: hyperbolic knots of at most 14 crossings."]},
              open(OUT, "w"), indent=1)
    for r in out:
        if r["verdict"] == "ISOMETRIC":
            print("ISOMETRIC:", r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
