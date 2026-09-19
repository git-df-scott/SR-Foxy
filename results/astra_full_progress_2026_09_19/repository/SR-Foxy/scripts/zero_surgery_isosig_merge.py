#!/usr/bin/env python3
"""Merge ALL zero-surgery isometry-signature shard checkpoints and group ONCE.

Why this exists
---------------
`zero_surgery_isometry_signature.py --shard=k --of=N` distributes knots by
index mod N and each shard prints its own "ISOMETRIC 0-SURGERY GROUPS" line at
the end.  Three defects in those self-reports:

  1. every shard writes the same OUT path, so the last one to finish silently
     overwrites the others' analyses;
  2. each shard groups over the `done` dict it loaded AT STARTUP, so its
     grouping is computed on partial data;
  3. worst: two members of a volume-group generally land in DIFFERENT shards,
     and no shard's `done` ever contains a sibling's later result, so a genuine
     isometric pair can be missed by every shard's own report.

The per-record JSONL checkpoints are unaffected by all three -- they are the
durable record.  This script is the only correct readout: it reads every
checkpoint, dedupes by knot index, and groups across the whole population.

A group here means: same Alexander polynomial AND same ORIENTED
isometry_signature of the 0-surgery.  It does NOT mean concordant, and it does
not by itself mean the knots are distinct -- both are separate checks.

Usage:  python3 scripts/zero_surgery_isosig_merge.py [--out PATH]
Exit 0 always; this is a reporter, not a gate.
"""
import glob, json, sys
from collections import defaultdict

CKPT_GLOB = "/tmp/claude-0/zero_surgery_isosig*.jsonl"
DEFAULT_OUT = "/tmp/claude-0/zero_surgery_isosig_MERGED.json"


def load():
    """Every record from every shard checkpoint, deduped by knot index."""
    done, files = {}, sorted(glob.glob(CKPT_GLOB))
    for f in files:
        for line in open(f):
            try:
                r = json.loads(line)
            except ValueError:
                continue          # a torn final line from a live shard
            if "i" in r:
                done[r["i"]] = r
    return done, files


def main():
    out = DEFAULT_OUT
    for a in sys.argv[1:]:
        if a.startswith("--out="):
            out = a.split("=", 1)[1]

    done, files = load()
    print(f"checkpoints read: {len(files)}")
    for f in files:
        print("   ", f)

    ok = [r for r in done.values() if r.get("sig")]
    err = [r for r in done.values() if not r.get("sig")]
    print(f"records: {len(done)}   signed: {len(ok)}   "
          f"failed/UNKNOWN: {len(err)}")

    # Failures are UNKNOWN, never exclusions.  Tally the reasons so a silent
    # systematic failure cannot be mistaken for an empty search.
    reasons = defaultdict(int)
    for r in err:
        reasons[r.get("error", "no error recorded").split(":")[0]] += 1
    for k, v in sorted(reasons.items(), key=lambda x: -x[1]):
        print(f"    UNKNOWN  {v:5d}  {k}")

    bysig = defaultdict(list)
    for r in ok:
        bysig[(tuple(r["delta"]), r["sig"])].append(r)
    hits = [v for v in bysig.values() if len(v) > 1]

    print(f"\nISOMETRIC 0-SURGERY GROUPS (merged, all shards): {len(hits)}")
    report = []
    for v in sorted(hits, key=lambda v: -len(v)):
        names = [r["name"] for r in v]
        print(f"   {len(v)}  {names}  vol={v[0]['vol']:.10f}")
        report.append({"n": len(v), "names": names, "vol": v[0]["vol"],
                       "delta": v[0]["delta"], "sig": v[0]["sig"]})

    json.dump({"records": len(done), "signed": len(ok), "unknown": len(err),
               "unknown_reasons": dict(reasons),
               "groups": len(hits), "hits": report},
              open(out, "w"), indent=1)
    print(f"\nwrote {out}")
    print("REMINDER: a shared 0-surgery does NOT imply concordance "
          "(Yasui disproved Akbulut-Kirby).  Failures above are UNKNOWN.")


if __name__ == "__main__":
    main()
