# First ribbon search on the unmined r = 0 RBG pair K(0,0,0,-1,2,1)

13 September 2026, evening session. **No counterexample found.** What this note
records is the first ribbon search ever run on the one super-special r = 0
Manolescu-Piccirillo pair that lies outside the Dunfield-Gong census, plus the
structural fact that separates it from K_DG = 18nh00000601.

## Why this pair

`CANDIDATE_LEDGER.md`, Tier-A generators, lists the r = 0 super-special RBG
pairs and records that `ERRATA_2026-09-11.md` corrected GHMR's three pairs to
two. The correction is reconfirmed here directly from the stored knots: exactly
three of the ten extracted Manolescu-Piccirillo knots per side have Alexander
polynomial 1, and their simplified crossing numbers are

| tuple (a,b,c,d,e,f) | K_B crossings | K_G crossings | in DG census? |
|---|---:|---:|---|
| (0,0,-2,0,0,1)  | 19 | 19 | yes, searched to 4 bands |
| (0,0,0,1,2,-1)  | 19 | 19 | yes, same pair as the above |
| **(0,0,0,-1,2,1)** | **27** | **26** | **no** |

All four knots of the two pairs have Alexander polynomial 1, Seifert genus 2,
and tau = nu = epsilon = 0. By Freedman they are topologically slice. Being
r = 0 they have diffeomorphic 0-traces, so a ribbon disk for either member of
a pair certifies its partner smoothly slice in standard B^4 **with no
inherited ribbon disk**: a fresh Tier-A candidate, not a counterexample.

The ledger recorded the (0,0,0,-1,2,1) pair as never searched. That is the
gap this note closes at one band.

## Toolchain calibration

Sage-backed SnapPy (`passagemath-standard` 10.8.11, SnapPy 3.3.2,
`snappy.sage_helper._within_sage` True) reproduces the repository's stored
calibration exactly: the Dunfield-Gong band search rediscovers the ribbon disk
of K_B, the 31-crossing 0-friend of K_DG, on the first diagram in **0.87 s**,
and `verify_ribbon_to_unknot` returns True. The historical record in
`PROGRESS.md` gives 0.9 s. Negatives reported below therefore come from a
filter that is known to fire on a positive of this size.

## The search and its outcome

Box, identical on both sides: 6 diagrams (the canonical `simplify('global')`
diagram plus five `backtrack(steps=25)` shaken diagrams under recorded seeds),
`max_bands = 1`, `max_twists = 2`, `max_band_len = 6`, shortest paths,
`filter_for_plausibly_slice = True`, `use_ribbon_link_cache = True`.

| knot | diagrams | crossings seen | plausibly-slice 1-band survivors | unknot | seconds |
|---|---:|---|---:|---|---:|
| K_G(0,0,0,-1,2,1) | 6 | 24-28 | 12, 11, 15, 10, 11, 13 = **72** | none | 1384.3 |
| K_B(0,0,0,-1,2,1) | 6 | 27-27 | 13, 17, 12, 6, 13, 11 = **72** | none | 1417.7 |

Raw records, with PD hashes, seeds and per-diagram timings, are in
`results/RBG_r0_KG_0_0_0_-1_2_1_bands1.json` and
`results/RBG_r0_KB_0_0_0_-1_2_1_bands1.json`.

**This is a coverage statement, not an obstruction.** It says only that no
single band of length at most 6 with at most 2 twists, on these six diagrams,
takes either knot to the unknot. It says nothing about whether either knot is
ribbon, or slice.

## The structural contrast worth keeping

The interesting number is 72, not 0.

`PROGRESS.md` records that for K_DG = 18nh00000601 the same class of search,
in a comparable box, left **2 survivors, both K_DG with a split unknot, i.e.
trivial bands**. The reading there was explicit: "no plausibly-slice one-band
move exists in this box, so no two-band search can start."

Here both members of the pair retain 72 nontrivial plausibly-slice one-band
intermediates across six diagrams, 6 to 17 per diagram. The Dunfield-Gong
filter (an intermediate link in a ribbon movie must itself be a ribbon link,
so it must pass linking number, signature and Fox-Milnor) does not collapse
this pair the way it collapses K_DG. So unlike the K_DG lane, a two-band
search on this pair has real input and is worth its cost. Two-band searches
are running on both sides at the time of writing.

This contrast is a statement about the search tree, not about ribbonness. A
large first-stage frontier is equally consistent with the knots being ribbon
and with their not being slice at all. Do not read 72 as evidence for either.

## Two bands

| knot | diagram | crossings | 2-band survivors | unknot | seconds |
|---|---:|---:|---:|---|---:|
| K_B(0,0,0,-1,2,1) | 0 (canonical) | 27 | **60** | none | 4174.7 |
| K_B(0,0,0,-1,2,1) | 1 (seed 1001) | 27 | **85** | none | 6142.3 |
| K_G(0,0,0,-1,2,1) | 0 (canonical) | 26-28 | not reached in 3 h at `max_band_len = 6` | - | - |
| K_G(0,0,0,-1,2,1) | 0 (canonical), `max_band_len = 5` | 24 | **71** | none | 11328.2 |
| K_G(0,0,0,-1,2,1) | 1 (seed 1001), `max_band_len = 5` | 26 | **32** | none | 2184.2 |
| K_G(0,0,0,-1,2,1) | 2 (seed 1002), `max_band_len = 5` | 24 | **72** | none | 4033.8 |
| K_G(0,0,0,-1,2,1) | 3 (seed 1003), `max_band_len = 5` | 26 | **42** | none | 3765.0 |
| K_G(0,0,0,-1,2,1) | 4 (seed 1004), `max_band_len = 5` | 24 | **44** | none | 2723.2 |
| K_G(0,0,0,-1,2,1) | 5 (seed 1005), `max_band_len = 5` | 24 | **43** | none | 3329.0 |
| K_B(0,0,0,-1,2,1) | 0-5, `max_band_len = 5` | 27 | 83, 71, 49, 29, 66, 35 = **333** | none | 38345.0 |

Records: `results/RBG_r0_KB_0_0_0_-1_2_1_bands2.json` and
`results/RBG_r0_KG_0_0_0_-1_2_1_bands2_len5.json`. Same box as the one-band
table except `max_bands = 2`, and `max_band_len = 5` on the K_G row that
completed. The K_G record carries all 103 frontier certificates, 71 and 32, as replayable
`[starting PD, band descriptor, endpoint]` triples; the K_B two-band numbers
predate that change and are counts only. That record is marked
`complete: false`: the run was killed at its budget after two diagrams, and the
per-diagram write is what preserved it. The same box is being retaken over more
diagrams.

Per-diagram cost varies by an order of magnitude at fixed box and crossing
number: 11328.2 s for the 24-crossing canonical diagram against 2184.2 s for
the 26-crossing shaken one. Do not budget these runs from crossing number.

A repeat of the same box over more diagrams
(`results/RBG_r0_KG_0_0_0_-1_2_1_bands2_len5_more.json`) reproduced the first
two rows band for band, 71 and 32 survivors against 71 and 32, at 4169.5 s and
2167.2 s. The `simplify('global')` randomness moves the crossing number around
(the canonical diagram came back at 26 rather than 24) without moving the
survivor count, which is a useful stability check on the search rather than on
the knots. **Both sides are now complete in the length-5 two-band box, with no ribbon
disk on either.** K_B: six diagrams, 83 + 71 + 49 + 29 + 66 + 35 = **333
survivors**, 38345.0 s, record
`results/RBG_r0_KB_0_0_0_-1_2_1_bands2_len5.json`, every frontier stored.
K_G: **304 survivors**, detailed next.

Per-diagram cost inside one box and one crossing number spans more than an
order of magnitude. On K_B, all six diagrams have 27 crossings, and they took
1685.9 s to 21582.1 s: a factor of 12.8 between the fastest and the slowest,
with the slowest being neither the largest nor the richest in survivors. Time
per diagram is not predictable from the diagram, so these runs need generous
budgets and per-diagram writes rather than a single end-of-run dump.

That run then **completed**: six diagrams, 71 + 32 + 72 + 42 + 44 + 43 =
**304 plausibly-slice two-band survivors, no unknot**, 20190.0 s total, every
one carrying a stored frontier certificate. This is a finished coverage
statement for K_G in the length-5 two-band box, not a truncated one.

Two things to carry forward. First, the frontier grows rather than collapses,
on **both** sides of the pair: 13 one-band survivors on the canonical K_B
diagram become 60 at two bands and 85 on the shaken diagram, and on K_G the
10-15 one-band survivors become 71 at two bands even in the smaller
`max_band_len = 5` box. The Dunfield-Gong filter is not closing this lane
the way it closed K_DG. Second, `max_band_len = 6` is out of budget for the
larger K_G diagrams, which reached no completed diagram in three hours; K_G
two-band coverage is being retaken at `max_band_len = 5`.

The K_B two-band record was recovered from stdout, because the driver then
dumped its structured record only after the whole loop and `timeout` killed it
first. That is fixed: `rbg_r0_search.py` now writes after every diagram, and
also stores the frontier itself rather than only its size.

## Scope and cautions

* Survivor counts are diagrams retained by the filter, not isotopy classes,
  and not distinct links.
* `simplify('global')` is randomized: the canonical K_G diagram came back at
  26 crossings in one run and 28 in another. Crossing numbers in the table are
  per-run, and the seeds are recorded so each row replays.
* Neither knot of this pair is known to be slice. A negative band search is
  the expected outcome for a non-slice knot and carries no information
  distinguishing the two cases.
* `scripts/rbg_r0_search.py` initially called `Link.backtrack(num_steps=...)`,
  which this spherogram build does not accept, so the first launch produced
  only its unshaken diagram before raising. The signature here is
  `backtrack(steps=10, prob_type_1=0.3, prob_type_2=0.3)`. The failure is
  recorded rather than quietly dropped; the canonical-diagram result it did
  produce (26 crossings, 16 survivors, no unknot, 269.4 s) is consistent with
  the completed run above and is superseded by it.

## Next

1. Finish the two-band searches on both sides and record their boxes.
2. If both are negative, widen band length before widening twists: the
   surviving first bands, not the twist parameter, are where the frontier is.
3. The census-scale item in the ledger, filtering Dunfield-Gong's 0-friend
   pairs for r = 0 realizations, remains unexecuted and needs their dataset,
   which is not in this repository.
