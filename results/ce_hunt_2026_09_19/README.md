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

## 8. The real bottleneck: the slice filter, not the crossing number

The first breadth probe returned **15 timeouts out of 15** at 2 bands / len 4
with a 120 s budget — zero completions, which is zero information. Diagnosing
that, on `K7a2 # -K10n4 # 6_1` (23 crossings), 1 band at len 2:

| filter | time | endpoints |
|---|---|---|
| `sagefree_slice_filter.could_be_strongly_slice` (the default here) | **> 110 s**, did not finish | — |
| none (`filter_for_plausibly_slice=False`) | **8.3 s** | 460 |
| **linking numbers only** | **2.3 s** | **111** |

Two things ruled out on the way: `use_ribbon_link_cache=False` changed nothing,
and the crossing count was never the driver.

The cost is `could_be_strongly_slice` building a **Seifert matrix for every
candidate band**, via spherogram's isotopy-to-a-braid. The linking-number test
alone is ~48x faster **and still prunes 460 endpoints to 111**, because most
bands produce a link with nonzero linking number.

**Soundness.** Linking numbers all zero is a *necessary* condition for a link to
be strongly slice — it is condition 1 of `sagefree_slice_filter`'s own cost-ordered
list. A weaker filter keeps more links, so it can only make the search larger and
slower; it can never lose a ribbon disk. Same failure direction as the existing
`_safe_filter` patch. `PROBE_FILTER=cheap|full` selects it.

This does not make 2-band searches cheap — the frontier still squares at the
second band, and every endpoint is composite, so the isometry-based endpoint
deduplication is working in the case this repository already documents as
SnapPy's slow one. It improves the constant factor, it does not change the shape.

## 9. Two self-inflicted errors, recorded

Both are the trap `HANDOFF_2026_09_18_OPUS.md` §6 already documents verbatim —
*"`pkill -f <script>` killed its own parent (exit 144) ... Use `ps aux | grep
"[p]ython3"` and kill by PID."*

1. `pkill -f "breadth2"` matched the shell running it **and the Monitor watching
   the logs**, whose command string contained the same word. Exit 144, monitor
   dead.
2. `ps ... | grep "[p]ython3 -c  import json" | xargs kill` matched its own
   shell for the same reason, killing both probe parents and orphaning their
   worker subprocesses, which then had to be reaped by hand.

Having read that warning earlier in the same session did not stop me making the
mistake twice. Explicit PIDs from a prior `ps`, never a pattern.

## 10. The diagram floor, and why the tool had to change

`K7a2 # -K10n4 # 6_1` holds at **23 crossings over 60 shaken seeds** — no seed
beat the canonical diagram. That is exactly `7 + 10 + 6`, so crossing number is
additive here and the floor is structural, not a simplifier weakness. There is
no diagram trick to make this lane cheaper.

Combined with §8, the position is: the cheapest target in the whole lane sits at
a 23-crossing floor; a 2-band search on it exceeds 420 s even with the cheap
filter; and there are ~48,000 targets (35,472 surviving pairs, most with two
orientations). **Exhaustive band search cannot sample this lane at any useful
rate, and that is a tooling limit rather than a compute limit.**

The measured failure mode is specific: exhausting a box is expensive, while a
hit — when one exists — is found fast. That is precisely the problem a
stochastic searcher solves, and one exists.

## 11. GHMR's random walker now runs here (first time)

<https://github.com/ruehlef/ribbon> — the Bayesian-optimised random walker of
Gukov-Halverson-Manolescu-Ruehle. `ASTRA_BRIEF_2026_09_19.md` §7 lists running it
against our candidates as item 1, "cheap and has never been done here".

It ships a prebuilt `rw.cpython-311-x86_64-linux-gnu.so`, matching this
container's Python and platform exactly. The only obstacle was `ribbon.visualizer`
importing `tkinter`, which is absent (and `apt-get install python3-tk` installs it
for 3.12, not the 3.11 we run). The visualizer only draws the band picture and is
never used by the search, so it is satisfied by a stub `tkinter` package on
`PYTHONPATH`.

**Controls, both directions, run before anything was counted:**

| control | expected | got |
|---|---|---|
| `K6a3` (= `6_1`, ribbon) | finds bands | **found** |
| `K3a1` (trefoil, not slice) | fails | **failed, 3000 tries** |
| `K4a1` (figure-8, not slice) | fails | **failed, 3000 tries** |

So the walker fires positive on a ribbon knot and does **not** fire on non-slice
knots in this container.

### The 90 targets (`rw_targets_pd.txt`, `rw_targets_meta.json`)

**(a) The flagship AT lane, all ten partners at once** — `D_{0,1} # J` for
`J` in `6_1, 8_8, 9_41, 9_46, 10_3, 8_9, 8_20, 9_27, 10_22, 10_87`. This includes
the three fibered partners restored by `ERRATA_2026-09-16.md` E16-1 and the two
(`10_22`, `10_87`) that container reclamation killed and that were never rerun.
Exhaustive search spent 4.21 h and 7.96 h on two of these boxes; the walker has
never been pointed at any of them.

**(b) 80 wild Miyazaki targets** — the cheapest Levine-Tristram survivors, in
each surviving mirror orientation.

`D_{0,1}` and every wild `D` are certified **not ribbon**, so a verified ribbon
certificate for any of these 90 is a counterexample outright.

**A walker hit would be a candidate, not a result.** It must be replayed through
`spherogram.links.bands.search.verify_ribbon_to_unknot` before it is anything at
all — this repository's standing rule, and the walker's band sequence is exactly
the replayable movie that rule asks for.

## 12. Manual verification of the live run

Done by hand against the running processes and files, not from a summary.

**Processes.** Three walker shards plus run `A` (`D_{0,1} # 6_1`, `paths=simple`,
now past 75 min). Memory 3 GB of 15 GB, disk 9.9 GB of 252 GB — both far from
the ~11.8 GB pressure point that has taken down containers here before.

**The walker is really searching our knots.** Its logs were empty apart from the
`plink` tkinter warning, which looks like a dead run. It is not: at `verbose 1`
the walker prints only when a knot finishes, and 20,000 tries on a 31-crossing
knot is long. Re-run by hand at `verbose 2` on the first target it prints the
full 31-crossing PD code, attaches bands, tracks `<Link: 2 comp; 31 cross>` down
to `30 cross`, and rejects candidates with `Band does not preserve orientation`.
It is working.

**Target integrity: 90/90.** `rw_targets_meta.json` and `rw_targets_pd.txt` are
aligned row for row; every PD code rebuilds in spherogram with the recorded
crossing number and exactly one component. The three shards reassemble byte
identical to `targets.txt` with **zero** duplicated lines, so coverage has no gap
and no overlap.

**All ten AT targets have `sigma = 0`**, recomputed here — the necessary
condition for a slice candidate holds on each.

**Miyazaki hypothesis, independently recomputed.** For the six cheapest queued
wild pairs, from Seifert matrices rather than the stored census field:

| J | J' | distinct | `Delta` equal | `Delta` irreducible | `deg Delta` |
|---|---|---|---|---|---|
| K7a2 | K10n4 | yes | yes | yes | 4 |
| K7a1 | K11n28 | yes | yes | yes | 4 |
| K8a15 | K10n32 | yes | yes | yes | 6 |
| K8a14 | K11n53 | yes | yes | yes | 6 |
| K8a15 | K11n58 | yes | yes | yes | 6 |
| K9a19 | K10n11 | yes | yes | yes | 6 |

`deg Delta = 2 * genus` in every row, which re-confirms fiberedness
independently. So Miyazaki Thm 5.5 does apply to these `D`, and each really is
certified not ribbon.

### A false alarm, and what caused it

The first pass of that table reported **`Delta` equal = False and irreducible =
False on every pair**, which would have meant the whole queue was built on a
broken hypothesis. It was **my check that was wrong, not the data.**

`Link.seifert_matrix()` returns a Seifert matrix from Seifert's algorithm on the
given *diagram*, whose surface need not be minimal genus. So
`det(V - tV^T)` is `Delta` only **up to a unit `+-t^k`** of `Z[t^+-1]`. I compared
raw coefficient lists without stripping that unit: hence `deg = 5` for a genus-2
knot (a stray factor of `t`), hence "not equal", and hence "reducible", since
`t * f(t)` factors trivially. Stripping the sign and the `t^k`, and allowing the
reversal, every row is clean.

Worth stating plainly: the tell was visible in the output — `deg = 5` for a knot
recorded at `genus 2` is impossible for a real Alexander polynomial, since
`deg Delta = 2g` for a fibered knot. The inconsistency was in the same table as
the alarming result.
