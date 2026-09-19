# Counterexample hunt, 19 September 2026 — IN PROGRESS, NO COUNTEREXAMPLE

**CE: NO.** Nothing in this directory is a counterexample. Most of it is a
running search; an unfinished search is not coverage of its box and supports no
conclusion.

## 1. The new lane: wild Miyazaki pairs as direct Teichner targets

`scripts/wild_pair_teichner_hunt.py`.

Let `J`, `J'` be distinct prime fibered knots sharing one **irreducible**
Alexander polynomial, and put `D = J # (-J')`.

* `D` is **not homotopy-ribbon**, hence not ribbon, by Miyazaki Thm 5.5: the
  prime fibered summands do not pair, and the second alternative holds because
  `Delta` is irreducible. Primality is free by Lemma P.
* Teichner: `K` is smoothly slice iff some ribbon `J0` has `K # J0` ribbon.

So a **verified** ribbon certificate for `D # J0` proves `D` slice, and `D`
slice + `D` not ribbon is a counterexample outright.

**Why this is new here.** `HANDOFF_2026_09_18_OPUS.md` §4 built this criterion
and then searched only for pairs whose **0-surgeries** agree (P1), as a proxy for
concordance; that search came back empty over the census
(`results/opus_2026_09_19_0700_*`). The Miyazaki certificate never needed the
0-surgery — it needs only distinct, prime, fibered, irreducible `Delta`. The band
search tests sliceness **directly**, so it applies to all 2,925 shared-`Delta`
buckets, not only the 0-surgery-matched ones. The Teichner machine had only ever
been pointed at `D_{0,1}`.

**Target list**, from `data/sweeps/miyazaki_pair_sweep.jsonl.gz` (16,970 fibered
irreducible-`Delta` knots): 2,925 shared-`Delta` buckets, **35,612 pairs** also
matching `tau`, `nu`, `eps` and genus. Cheapest is `K7a2 # -K10n4` at **17
crossings**, against `D_{0,1}`'s 25. Signature was checked on the 60 cheapest and
matches on all 60, so `sigma(D) = 0` there.

`data/sweeps/wild_pairs_volmatched.json` additionally records the **298
volume-matched** pairs among the 6,831 with `cr_sum <= 26` — mutant-like pairs,
where every invariant this repository can compute agrees. That is the sharpest
available prior for "not separated by anything we can check".

## 2. Controls, run before anything was counted

* `CONTROL partner 6_1 verified=True` on every shard — the band search **and**
  `verify_ribbon_to_unknot` both fire **positive** in this container, so a
  negative is real coverage rather than a broken toolchain.
* `sigma(K3a1) = 2`, `sigma(6_1) = 0` — the Sage-free signature fires correctly
  in both directions.

## 3. A correctness fix, and a question it raises about the older runs

`Link.connected_sum` leaves **tuple-valued crossing labels**. This repository
already records the fault (`min_len_bands` rejects a diagram whose crossing
labels are not renormalized), and `spherogram.links.bands.normalize_crossing_labels`
is the fix. It is applied in place in `wild_pair_teichner_hunt.py`.

**`scripts/teichner_certify_nosage.py` and `scripts/teichner_certify.py` do not
do this**, and every Teichner target in this campaign is a connected sum. Whether
the historical Teichner negatives were run on unnormalized diagrams is **open and
should be checked before any of them is cited as coverage.** Not asserted here —
flagged.

## 4. Measured cost, which is worse than a crossing count suggests

Predicted from this repository's own "cost roughly doubles per two crossings":
23-crossing sums should be ~16x cheaper than `D_{0,1} # 6_1` at 31. **That
estimate is wrong.** Measured on `K7a2 # -K10n4 # 6_1` (23 crossings):

| box | result |
|---|---|
| 1 band, len 2 | **> 110 s**, did not finish |
| 1 band, len 4 | **> 200 s**, did not finish |

The time is spent inside a C call that does not yield to a Python `SIGALRM`, so
it could not be profiled from inside. The likely reason the crossing heuristic
fails: `D` is a connected sum, so it and every intermediate link are composite,
never hyperbolic — the case this repository already documents as the slow and
unreliable one for SnapPy-backed isotopy decisions.

**Consequence: real throughput is a handful of targets, not thousands.** Claims
about sweeping the 35,612 should be discounted accordingly.

## 5. Files

| file | what |
|---|---|
| `wild_shard{0,1,2}.jsonl` | one row per finished target, flushed and fsync'd; resumable |
| `wild{0,1,2}.log` | heartbeats and controls |
| `A_6_1_simple_b2l4.json`, `A.log` | `D_{0,1} # 6_1`, 2 bands, len 4, **paths=simple** — the first `simple` run this campaign has gotten going (`UNFINISHED` §1 row 1) |
| `B_*.json`, `C_*.json` | **killed by me**, heartbeat only, `runs: []`. **No coverage. Not results.** Preserved rather than deleted, per this repository's convention |
| `SMOKE_6_1_b1l4.json` | killed control; its only output was `partner 6_1 verified=True` |

Empty `wild_shard*.jsonl` means no target has finished yet, not that targets
failed.
