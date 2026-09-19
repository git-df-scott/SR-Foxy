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

## 3. RETRACTED: the historical Teichner runs were NOT degraded

**This section previously flagged a possible defect in every historical Teichner
run. That flag is wrong and is withdrawn.**

What is true: `Link.connected_sum` leaves tuple-valued crossing labels, and
`crossing_labels_are_normalized(D_{0,1} # 6_1)` is `False` as
`scripts/teichner_certify_nosage.py` builds it. Calling `min_len_bands` on it
directly raises `ValueError('Link needs normalized crossing labels')` -- it
fails loudly, it does not silently return a smaller band set.

What I did not check before flagging it: **the caller.**
`spherogram.links.bands.search.ribbon_concordant_links` calls
`normalize_crossing_labels(link)` itself, on its own copy, before any band
generation, on both the `shortest` and `simple` paths. So every Teichner run in
this repository has been searching a properly labelled diagram, and the
historical negatives stand as the coverage they claim.

Two pieces of evidence were already in hand and contradicted the flag: run `A`
here is executing normally from exactly that unnormalized input, and the
completed 4.21 h and 7.96 h partner runs returned times and endpoint sets rather
than a traceback.

The `normalize_crossing_labels` call in `wild_pair_teichner_hunt.py` is
therefore **redundant, not a fix**. It is left in place as belt and braces and
costs nothing.

*Failure mode, for the record: a bounded observation ("these labels are not
normalized, and this one function rejects that") generalised into a claim about
every historical run, without checking the caller that was one `inspect.getsource`
away. This is the same pattern `ERRATA_2026-09-18_OPUS.md` records three times.*

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

---

## 6. Levine-Tristram filter (`scripts/wild_pair_lt_filter.py`)

`lt_filter_full.json`. **Controls pass.** 232 roots of unity at prime-power
orders up to 31.

`sigma_omega` is a **concordance invariant** vanishing on slice knots, so
`J ~ J'` forces `sigma_omega(J) = sigma_omega(J')` wherever both are defined.
A mismatching `omega` therefore **proves** the pair non-concordant, hence proves
`D = J # (-J')` not slice. That is an obstruction, not a heuristic — unlike
`Delta`, `tau`, `nu`, `eps` and genus, which agree across this list by
construction or coarseness.

| | |
|---|---|
| pairs in | 35,612 |
| **proved non-concordant** | **140** |
| surviving (undecided) | 35,472 |
| Seifert-matrix failures | 0 |

**Honest accounting of what the machinery bought.** Of the 140 kills, **127
would have fallen to the ordinary signature at `omega = -1` alone**; only **13**
needed `omega != -1`. So the full Levine-Tristram apparatus added 13 pairs over
a plain signature check.

The more useful half of that number is the other one: **127 pairs in the
published 35,612 fail the ordinary knot signature**, which means the existing
pair filter (`Delta`, `tau`, `nu`, `eps`, genus — `HANDOFF` §4) never applied the
most classical slice obstruction there is. Those 127 were never candidates.

### Mirror orientation, which the earlier target list got wrong

A census entry names a knot only **up to mirror** (a knot and its mirror share
an exterior and one census entry), so both `D = J # (-J')` and `D = J # J'` are
legitimate Miyazaki targets and both must be tested. Levine-Tristram resolves
this for free, since `sigma_omega(mirror K) = -sigma_omega(K)`:

| surviving orientations | pairs |
|---|---|
| `J # (-J')` only | 21,723 |
| both | 12,790 |
| **`J # J'` only** | **959** |

`scripts/wild_pair_teichner_hunt.py` builds `J # (-J')` unconditionally, so for
those **959 pairs it was searching the wrong knot**.

## 7. Time-boxed breadth probe (`scripts/wild_pair_breadth_probe.py`)

The depth-first shards of §1 ran 30 minutes and completed **zero** targets, which
is what the §4 cost measurement predicted. They were stopped.

A ribbon disk, when one exists, is usually found fast — this repository's own
calibration found `K_B`'s in 0.87 s, and DG report most disks at <= 2 bands.
What is expensive is *exhausting* a box to prove absence, and absence is not what
this lane wants: a counterexample needs one hit. So the probe spends a fixed
budget per target in a subprocess (the search is a C call that ignores
`SIGALRM`, so an external timeout is the only way to bound it) and moves on.

**Labelling.** `timeout` is **not** coverage of its box and supports no
conclusion — not that `D` is non-slice, not that the box is empty. Only
`completed` rows are coverage; only `certificate_verified` is a result.
