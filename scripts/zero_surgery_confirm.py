#!/usr/bin/env python3
"""Robustly decide the volume-matched 0-surgery pairs left UNKNOWN by SnapPea.

scripts/zero_surgery_pair_search.py found 1589 volume-matched groups inside a
shared Alexander polynomial and reported 0 confirmed isometric pairs.  That was
NOT a mathematical result: every sampled unconfirmed pair carried

    RuntimeError: The SnapPea kernel was not able to determine if the manifolds
    are isometric.

The kernel simply could not decide, which the campaign's standing rule forbids
recording as an exclusion.  Controls confirm the test itself works: a 0-surgery
compared with an independently constructed copy of itself returns True, and still
returns True after randomize().

This pass re-decides each volume-matched pair with three escalations:

  1. ManifoldHP (double-double precision) instead of Manifold;
  2. several randomize() retries on both sides, since the kernel's failure is
     triangulation-dependent;
  3. an independent fingerprint - the initial COMPLEX geodesic length
     spectrum (Chern-Simons is unavailable for these filled manifolds) -
     which cannot prove isometry but can separate
     manifolds the kernel leaves undecided, turning UNKNOWN into a justified NO.

Outcomes are recorded as one of

  ISOMETRIC          - is_isometric_to returned True on some attempt
  DISTINCT_BY_ISO    - is_isometric_to returned False on some attempt
  DISTINCT_BY_SPEC   - kernel undecided, complex length spectra differ
  UNKNOWN            - still undecided; NOT an exclusion

Only ISOMETRIC is a hit.  UNKNOWN is reported as UNKNOWN.
"""
import json
import os
import sys
import time
from collections import Counter, defaultdict

import snappy

VOLS = "/tmp/claude-0/zero_surgery_volumes.jsonl"
OUT = "/tmp/claude-0/zero_surgery_confirm.json"
TOL = 1e-6
RETRIES = 6
SPEC_CUTOFF = 1.2


def filled(index, hp=False):
    census = snappy.HTLinkExteriors(cusps=1)
    M = census[index]
    name = M.name()
    if hp:
        M = snappy.ManifoldHP(M)
    M.dehn_fill((0, 1))
    return M, name


def try_isometry(ia, ib):
    """Return True / False / None (undecided) after escalating attempts."""
    for hp in (False, True):
        try:
            A, _ = filled(ia, hp)
            B, _ = filled(ib, hp)
        except Exception:
            continue
        for k in range(RETRIES):
            try:
                return bool(A.is_isometric_to(B))
            except Exception:
                pass
            try:
                A.randomize()
                B.randomize()
            except Exception:
                break
    return None


def _clen(g):
    """Complex length of a geodesic, as a rounded (real, imag) pair.

    The Chern-Simons invariant is not available for these filled manifolds
    ("The Chern-Simons invariant isn't currently known"), so the COMPLEX length
    spectrum - length together with torsion - carries the whole fingerprint.
    It is strictly stronger than real lengths alone.
    """
    z = complex(g.length)
    return (round(z.real, 6), round(abs(z.imag), 6))


def fingerprint(index):
    try:
        M, _ = filled(index, hp=True)
        spec = sorted(_clen(g) for g in M.length_spectrum(SPEC_CUTOFF))
        if not spec:
            return None
        return tuple(spec[:8])
    except Exception:
        return None


def main():
    vols = {}
    with open(VOLS) as fh:
        for line in fh:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("vol") is not None:
                vols[d["i"]] = d

    groups = defaultdict(list)
    for d in vols.values():
        groups[(tuple(d["delta"]), round(d["vol"] / TOL))].append(d)
    cand = [v for v in groups.values() if len(v) > 1]
    pairs = [(g[a], g[b]) for g in cand
             for a in range(len(g)) for b in range(a + 1, len(g))]
    print("volume-matched groups:", len(cand), " pairs to decide:", len(pairs))
    sys.stdout.flush()

    fp_cache = {}
    results = []
    t0 = time.time()
    for k, (A, B) in enumerate(pairs):
        if k and k % 100 == 0:
            print(f"  {k}/{len(pairs)}  {time.time()-t0:.0f}s  "
                  f"{Counter(r['verdict'] for r in results)}")
            sys.stdout.flush()
        rec = {"a": A["name"], "b": B["name"], "vol": A["vol"],
               "delta": A["delta"], "ia": A["i"], "ib": B["i"]}
        iso = try_isometry(A["i"], B["i"])
        if iso is True:
            rec["verdict"] = "ISOMETRIC"
        elif iso is False:
            rec["verdict"] = "DISTINCT_BY_ISO"
        else:
            for idx in (A["i"], B["i"]):
                if idx not in fp_cache:
                    fp_cache[idx] = fingerprint(idx)
            fa, fb = fp_cache[A["i"]], fp_cache[B["i"]]
            if fa is None or fb is None:
                rec["verdict"] = "UNKNOWN"
            elif fa != fb:
                rec["verdict"] = "DISTINCT_BY_SPEC"
                rec["spec"] = [list(map(list, fa[:3])), list(map(list, fb[:3]))]
            else:
                rec["verdict"] = "UNKNOWN"
                rec["note"] = "complex length spectra agree; kernel undecided"
        results.append(rec)

    tally = Counter(r["verdict"] for r in results)
    print("VERDICTS:", dict(tally))
    hits = [r for r in results if r["verdict"] == "ISOMETRIC"]
    hard = [r for r in results if r["verdict"] == "UNKNOWN"]
    print("ISOMETRIC 0-surgery pairs:", len(hits))
    print("still UNKNOWN (NOT an exclusion):", len(hard))
    with open(OUT, "w") as fh:
        json.dump({"n_pairs": len(pairs), "tally": dict(tally),
                   "isometric": hits, "unknown": hard[:300],
                   "all": results[:4000],
                   "caveats": [
                       "UNKNOWN means the kernel could not decide and the"
                       " fingerprints agreed; it is not an exclusion.",
                       "A shared 0-surgery does not imply concordance"
                       " (Yasui disproved Akbulut-Kirby).",
                       "Chern-Simons and length spectra can only SEPARATE;"
                       " agreement never proves isometry.",
                       "Scope: hyperbolic knots of at most 14 crossings."]}, fh,
                  indent=1)
    for h in hits[:60]:
        print("   *** ISOMETRIC:", h)
    return 0


if __name__ == "__main__":
    sys.exit(main())
