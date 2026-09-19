# Census evidence recovery, reconciliation, and a bounded repair

18 September 2026, Opus night session. **CE: NO.**
**Smooth concordance `K_0 ~ K_1`: UNKNOWN. Slice-Ribbon CE: NO.**

This directory preserves the raw output of the 18 September census work, which
lived only in `/tmp/claude-0/` and would have died with the container. It also
reconciles every reported number against the stored data and records the defects
the night-session audit identified, with their actual consequences measured
rather than assumed.

Nothing here is a counterexample and nothing here obstructs one.

---

## 1. Process status — what finished, what did not

| run | status |
|---|---|
| `miyazaki_pair_sweep.py` | **FINISHED**, exit 0 |
| `zero_surgery_pair_search.py` | **FINISHED**, exit 0 — but its "0 confirmed" is **RETRACTED**: every pair threw `RuntimeError` |
| `zero_surgery_confirm.py` | **KILLED by PID** after 238 CPU-minutes without finishing 100 of 2352 pairs. **No final JSON exists** |
| `zero_surgery_hammer.py` | **KILLED**, superseded; its sample probe had already timed out |
| `zero_surgery_isometry_signature.py` | **STILL RUNNING** at archive time; the checkpoint here is **partial** |
| `common_upper_bound_search.py` | **STOPPED** at 20000/59937; its Zemke bigraded-domination filter admitted nothing; no final JSON |

A committed script is not a saved computation. The two runs with no final JSON
are recorded as incomplete, not as negative results.

`AUDIT.md` and `audit_regressions.py` from the preparation package are **not
present in this repository** and were not delivered to this container, so the 16
regression tests were **not run**. That is a gap, not a pass.

## 2. Reconciliation — `RECONCILIATION.json`

Every file is SHA-256 hashed. Counts reconciled:

| quantity | value |
|---|---|
| sweep JSONL rows | 16970 |
| sweep JSON reported `n_fibered_irreducible` | 16970 — **matches** |
| torn checkpoint lines | 0 |
| pairs reported | 35612 |
| pairs actually **stored** | 2000 |
| **pairs truncated out of the record** | **33612** |
| 0-surgery volume records | 14127 |
| usable geometric solutions | 14122 |
| **non-geometric / unusable** | **5** — outside coverage, **not excluded** |
| volume exceptions | 0 |
| unconfirmed pairs reported | 2352 |
| unconfirmed **stored** | 500 |
| **truncated out of the record** | **1852** |
| isometry signatures at archive time | 61 of 3486 (1 error) |
| matching signature groups so far | **none** |

Solution types across the 14127: 14061 all-positive, 61 with negatively oriented
tetrahedra, 4 unrecognized, 1 with flat tetrahedra. The last five are **UNKNOWN**,
not excluded.

## 3. The audit's defects, with consequences measured

The night-session audit named five defects in the 18 September scripts. All five
are real. Their consequences differ, and it matters which is which.

**(a) `try_isometry` returns on the first Boolean. — CONFIRMED DEFECT, unrepaired.**
SnapPy documents `is_isometric_to` returning True as rigorous but False as
possibly numerical. Returning on a low-precision False both ends escalation early
and records an uncertified exclusion. `DISTINCT_BY_ISO` verdicts from
`zero_surgery_confirm.py` are therefore **not certified**. Since that run was
killed before producing output, no such verdict was ever published — but the code
path is wrong and must be fixed before reuse.

**(b) Volume binning by `round(v/1e-6)` can drop pairs across a bin boundary. —
CONFIRMED DEFECT, consequence measured as NIL.**
`BIN_BOUNDARY_REPAIR.json`. Replacing the bins with a sorted-window comparison
(compare every pair whose volumes differ by at most `eps`, which cannot drop a
straddling pair) returns **exactly the same 2352 pairs** at both `eps = 1e-6` and
`eps = 1e-9`. Missed by binning: **0**. The criticism is methodologically correct
and the hole is real; on this dataset it swallowed nothing, because the volume
coincidences agree to about `1e-10` and there are no near-misses at the `1e-6`
scale. Recorded as measured, not assumed in either direction.

**(c) Rounded complex length spectra cannot certify DISTINCT. — CONFIRMED
DEFECT, unrepaired.** Six-place rounding of a Python `complex` is not interval
verification, and a `DISTINCT_BY_SPEC` verdict built on it is a heuristic, not a
proof. Multiplicities were also not preserved. Any future use must carry certified
lengths and enough completeness to exclude a matching multiset; agreement never
proves isometry in either direction.

**(d) The scientific record was truncated. — CONFIRMED, quantified above.**
33612 pairs and 1852 unconfirmed records were discarded by `[:2000]` and `[:300]`
slices, and the eight-entry fingerprint was stored as `fa[:3]`. The full JSONL
checkpoints preserved here are the durable record; the truncated JSON summaries
are not.

**(e) HFK exceptions silently skipped. — CONFIRMED DEFECT, unrepaired.**
`miyazaki_pair_sweep.py` used a bare `except Exception: continue` with no ledger,
so any knot whose HFK computation failed is silently absent from the 16970 rather
than counted. The reconciliation cannot recover how many, because nothing was
recorded. Future sweeps need an exception ledger.

## 4. What still stands

The 1589 volume-matched 0-surgery groups (2352 pairs) among prime fibered knots
with irreducible Alexander polynomial are **unaffected** by defects (a)-(e): they
come from volume agreement plus the sweep's own filters, and the sorted-window
repair reproduces them exactly. What is **not** established is whether any pair is
actually isometric. `is_isometric_to` never decided one, and the
`isometry_signature` run had signed 61 of 3486 at archive time with no matching
group yet.

Status of the pairing: **UNKNOWN**, in the strict sense — undecided, not empty.

## Files

* `raw/` — every surviving `/tmp/claude-0` artifact, gzipped, with the logs.
* `RECONCILIATION.json` — SHA-256 of each file, all reconciled counts, process
  status, and the defect list.
* `BIN_BOUNDARY_REPAIR.json` — the sorted-window recomputation and its nil delta.
