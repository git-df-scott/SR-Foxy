#!/usr/bin/env python3
"""Among prime fibered knots with irreducible Alexander polynomial, find PAIRS
whose 0-surgeries agree.

WHY THIS PAIRING AND NOT ANOTHER.  By the Miyazaki criterion recorded in
scripts/miyazaki_pair_sweep.py, any two DISTINCT prime fibered knots with
irreducible Alexander polynomials have a connected sum that is never homotopy
ribbon, hence never ribbon.  So a concordance between any such pair refutes the
slice-ribbon conjecture.  The previous sweep found 35612 pairs passing
Delta/tau/nu/epsilon, which only measures how coarse those invariants are -
virtually none of those pairs is concordant, and none of the filters is
decidable.

Sharing a 0-surgery is different on both counts.  It is the ONLY known machine
that produces distinct prime fibered knots plausibly concordant to one another -
it is exactly the Abe-Tagami mechanism, and the Akbulut-Kirby conjecture asserted
(falsely in general, Yasui) that it forces concordance.  And unlike "tau agrees",
it is DECIDABLE: SnapPy can test the two closed 0-surgeries for isometry.

The earlier census sweep recorded in data/knots/AbeTagami_K_n_NOTES.json compared
every census knot's 0-surgery against 6_3's only.  This compares all qualifying
pairs against each other.

SOUNDNESS OF THE RESTRICTION.  The 0-surgery determines the Alexander polynomial,
so knots with homeomorphic 0-surgeries necessarily share Delta.  Restricting the
comparison to the Delta-buckets of the previous sweep is therefore lossless.

WHAT A HIT IS AND IS NOT.  A confirmed isometry gives an Abe-Tagami-type
CANDIDATE pair, not a concordance.  Yasui disproved Akbulut-Kirby, so a shared
0-surgery does not imply concordance.  Volume agreement alone is only necessary;
is_isometric_to is the check, and any failure of it is recorded as UNKNOWN rather
than as an exclusion.  Orientation conventions are not audited here.

SCOPE.  Hyperbolic knots of at most 14 crossings that are fibered with
irreducible Delta, as collected by scripts/miyazaki_pair_sweep.py.  A null result
is a bounded negative, not a theorem.
"""
import json
import os
import sys
import time
from collections import defaultdict

import snappy

SRC = "/tmp/claude-0/miyazaki_pair_sweep.jsonl"
CKPT = "/tmp/claude-0/zero_surgery_volumes.jsonl"
OUT = "/tmp/claude-0/zero_surgery_pairs.json"
TOL = 1e-6


def load_rows():
    rows = []
    with open(SRC) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if r.get("_scanned_through") is None:
                rows.append(r)
    return rows


def main():
    rows = load_rows()
    print("qualifying knots (fibered, irreducible Delta):", len(rows))

    # Only knots sharing a Delta can share a 0-surgery, so restrict to buckets
    # of size >= 2.  This is lossless: the 0-surgery determines Delta.
    buckets = defaultdict(list)
    for r in rows:
        buckets[tuple(r["delta"])].append(r)
    todo = [r for v in buckets.values() if len(v) > 1 for r in v]
    print("knots in shared-Delta buckets:", len(todo),
          "across", sum(1 for v in buckets.values() if len(v) > 1), "buckets")
    sys.stdout.flush()

    done = {}
    if os.path.exists(CKPT):
        with open(CKPT) as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                done[d["i"]] = d
        print("resuming with", len(done), "0-surgery volumes already computed")
        sys.stdout.flush()

    census = snappy.HTLinkExteriors(cusps=1)
    ck = open(CKPT, "a", buffering=1)
    t0 = time.time()
    for k, r in enumerate(todo):
        if r["i"] in done:
            continue
        if k and k % 1000 == 0:
            print(f"  {k}/{len(todo)}  {time.time()-t0:.0f}s")
            sys.stdout.flush()
        rec = {"i": r["i"], "name": r["name"], "delta": r["delta"], "vol": None}
        try:
            M = census[r["i"]]
            M.dehn_fill((0, 1))
            v = M.volume()
            sol = str(M.solution_type())
            # Only a genuine geometric solution is usable.
            if sol.startswith("all tetrahedra positively oriented") or \
               sol.startswith("contains negatively oriented"):
                rec["vol"] = float(v)
            rec["solution_type"] = sol
        except Exception as e:
            rec["error"] = f"{type(e).__name__}: {e}"
        done[r["i"]] = rec
        ck.write(json.dumps(rec) + "\n")
    ck.close()
    print(f"0-surgery volumes computed ({time.time()-t0:.0f}s)")

    usable = [d for d in done.values() if d.get("vol") is not None]
    print("with a usable geometric solution:", len(usable),
          " unusable/failed:", len(done) - len(usable))

    # Group by (Delta, volume) and confirm with is_isometric_to.
    groups = defaultdict(list)
    for d in usable:
        groups[(tuple(d["delta"]), round(d["vol"] / TOL))].append(d)
    cand = [v for v in groups.values() if len(v) > 1]
    print("volume-matched groups inside a shared Delta:", len(cand))
    sys.stdout.flush()

    confirmed, unknown = [], []
    for g in cand:
        for a in range(len(g)):
            for b in range(a + 1, len(g)):
                A, B = g[a], g[b]
                try:
                    MA, MB = census[A["i"]], census[B["i"]]
                    MA.dehn_fill((0, 1))
                    MB.dehn_fill((0, 1))
                    iso = MA.is_isometric_to(MB)
                    rec = {"a": A["name"], "b": B["name"], "vol": A["vol"],
                           "delta": A["delta"], "isometric": bool(iso)}
                    (confirmed if iso else unknown).append(rec)
                except Exception as e:
                    unknown.append({"a": A["name"], "b": B["name"],
                                    "vol": A["vol"], "delta": A["delta"],
                                    "isometric": "UNKNOWN",
                                    "error": f"{type(e).__name__}: {e}"})

    print("CONFIRMED isometric 0-surgery pairs:", len(confirmed))
    print("volume-matched but not confirmed (incl. UNKNOWN):", len(unknown))
    with open(OUT, "w") as fh:
        json.dump({"qualifying_knots": len(rows), "in_shared_delta_buckets": len(todo),
                   "usable_geometric_solutions": len(usable),
                   "volume_matched_groups": len(cand),
                   "confirmed_pairs": confirmed, "unconfirmed": unknown[:500],
                   "n_confirmed": len(confirmed), "n_unconfirmed": len(unknown),
                   "caveats": [
                       "A shared 0-surgery does NOT imply concordance;"
                       " Yasui disproved the Akbulut-Kirby conjecture.",
                       "is_isometric_to failures are recorded as UNKNOWN, never"
                       " as exclusions.",
                       "Orientation conventions are not audited here.",
                       "Scope: hyperbolic knots of at most 14 crossings."]}, fh,
                  indent=1)
    for c in confirmed[:60]:
        print("   *** ", c)
    return 0


if __name__ == "__main__":
    sys.exit(main())
