#!/usr/bin/env python3
"""Decide the volume-matched 0-surgery pairs with SnapPy's isometry_signature.

WHY THIS AND NOT is_isometric_to.  On these closed 0-surgeries the SnapPea kernel
usually throws "The SnapPea kernel was not able to determine if the manifolds are
isometric", so is_isometric_to leaves almost every pair undecided.  Recording
that as "no pairs" would be turning a failure into a result; it was reported that
way once in this campaign and retracted.

WHY THIS IS NOT THE RETRACTED isoSig METHOD.  research/34 retracted an
identification based on comparing Regina isoSigs after a RANDOMISED simplify():
an isoSig is canonical for a TRIANGULATION, not for a manifold, so two
triangulations of the same manifold can disagree.  SnapPy's isometry_signature()
is different in exactly the way that matters - it first computes the CANONICAL
retriangulation (the canonical cell decomposition of the hyperbolic structure)
and takes the isosig of that.  It therefore depends only on the isometry type.
Equal signature means isometric.

Controls, run before trusting it: the signature of a 0-surgery is reproducible
across independent constructions, and two different knots' 0-surgeries give
different signatures.

CAVEAT ON RIGOUR.  Called without verified=True the canonical retriangulation is
found numerically, so a signature is high-confidence but not a proof.  Hits are
re-run with verified=True, which is rigorous but slower, and the verified status
of every hit is recorded.  Failures are recorded as UNKNOWN, never as exclusions.

WHAT A HIT MEANS.  The two knots are distinct prime fibered knots with irreducible
Alexander polynomial, so by Miyazaki Theorem 5.5 their connected sum is never
homotopy-ribbon, hence never ribbon.  If they were also smoothly concordant, that
connected sum would be slice and not ribbon, refuting slice-ribbon.  A shared
0-surgery does NOT imply concordance - Yasui disproved Akbulut-Kirby - so a hit is
an Abe-Tagami-type CANDIDATE with two explicit diagrams, not a counterexample.
"""
import glob
import json
import os
import sys
import time
from collections import Counter, defaultdict

import snappy

VOLS = "/tmp/claude-0/zero_surgery_volumes.jsonl"
CKPT_GLOB = "/tmp/claude-0/zero_surgery_isosig*.jsonl"
CKPT = "/tmp/claude-0/zero_surgery_isosig.jsonl"
OUT = "/tmp/claude-0/zero_surgery_isosig.json"
TOL = 1e-10

_C = None


def census():
    global _C
    if _C is None:
        _C = snappy.HTLinkExteriors(cusps=1)
    return _C


def signature(i, verified=False):
    """ORIENTED isometry signature of the 0-surgery.

    ignore_orientation MUST be False.  SnapPy's default returns the UNORIENTED
    invariant, which gives a manifold and its mirror the identical signature
    (checked directly: they agree with the default and differ with it off).
    A shared 0-surgery in the Abe-Tagami sense needs an ORIENTATION-PRESERVING
    homeomorphism, so the default would have counted mirror pairs as hits.
    """
    M = snappy.ManifoldHP(census()[i])
    M.dehn_fill((0, 1))
    return M.isometry_signature(verified=verified, ignore_orientation=False)


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
    todo = [d for v in groups for d in v]
    print(f"volume-matched groups at tol {TOL:g}: {len(groups)}"
          f"  knots to sign: {len(todo)}")
    sys.stdout.flush()

    # Shard across cores: shard k of n handles the indices congruent to k mod n.
    # Every shard reads EVERY checkpoint file, so work already done by the
    # original single run (or by a sibling shard) is never repeated.
    shard, nshard = 0, 1
    for a in sys.argv[1:]:
        if a.startswith("--shard="):
            shard = int(a.split("=")[1])
        elif a.startswith("--of="):
            nshard = int(a.split("=")[1])
    ckpt = CKPT if nshard == 1 else CKPT.replace(".jsonl", f"_s{shard}.jsonl")

    done = {}
    for f in sorted(glob.glob(CKPT_GLOB)):
        for line in open(f):
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if "i" in r:
                done[r["i"]] = r
    print(f"shard {shard}/{nshard}: resuming with {len(done)} signatures already known")
    sys.stdout.flush()

    todo = [d for j, d in enumerate(todo) if j % nshard == shard]
    print(f"shard {shard}: {len(todo)} knots in this shard")
    sys.stdout.flush()

    ck = open(ckpt, "a", buffering=1)
    t0 = time.time()
    for k, d in enumerate(todo):
        if d["i"] in done:
            continue
        if k and k % 100 == 0:
            print(f"  {k}/{len(todo)}  {time.time()-t0:.0f}s")
            sys.stdout.flush()
        rec = {"i": d["i"], "name": d["name"], "delta": d["delta"],
               "vol": d["vol"], "sig": None}
        try:
            rec["sig"] = signature(d["i"])
        except Exception as e:
            rec["error"] = f"{type(e).__name__}: {e}"
        done[d["i"]] = rec
        ck.write(json.dumps(rec) + "\n")
    ck.close()
    print(f"signatures computed ({time.time()-t0:.0f}s)")

    ok = [r for r in done.values() if r.get("sig")]
    print("with a signature:", len(ok), " failed (UNKNOWN):", len(done) - len(ok))

    bysig = defaultdict(list)
    for r in ok:
        bysig[(tuple(r["delta"]), r["sig"])].append(r)
    hits = [v for v in bysig.values() if len(v) > 1]
    print("ISOMETRIC 0-SURGERY GROUPS:", len(hits))

    report = []
    for v in hits:
        entry = {"delta": v[0]["delta"], "vol": v[0]["vol"],
                 "sig": v[0]["sig"], "knots": [x["name"] for x in v],
                 "indices": [x["i"] for x in v]}
        try:
            entry["verified_sig"] = signature(v[0]["i"], verified=True)
            entry["verified_all_agree"] = all(
                signature(x["i"], verified=True) == entry["verified_sig"]
                for x in v[1:])
        except Exception as e:
            entry["verified_error"] = f"{type(e).__name__}: {e}"
        report.append(entry)
        print("   *** ", entry)
        sys.stdout.flush()

    json.dump({"groups_checked": len(groups), "knots_signed": len(ok),
               "failed_unknown": len(done) - len(ok),
               "n_isometric_groups": len(hits), "isometric_groups": report,
               "caveats": [
                   "isometry_signature uses the CANONICAL retriangulation, so"
                   " equality means isometric; this is not the retracted"
                   " isoSig-after-random-simplify method.",
                   "Unverified signatures are numerical; every hit is re-run"
                   " with verified=True and the outcome recorded.",
                   "A shared 0-surgery does not imply concordance"
                   " (Yasui disproved Akbulut-Kirby).",
                   "Failures are UNKNOWN, never exclusions.",
                   "Scope: hyperbolic knots of at most 14 crossings."]},
              open(OUT, "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
