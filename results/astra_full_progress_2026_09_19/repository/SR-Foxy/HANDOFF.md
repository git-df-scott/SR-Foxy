# Handoff for Astra — 15 September 2026, everything folded into one place

**No counterexample found.** Nothing below changes that, and nothing below is a
new obstruction to slice-ribbon.

What is new is bookkeeping: this branch carries every line of work that exists
in this repository. It folds #2 (`claude/pensive-hopper-3rh6p4`) and #4
(`claude/inspiring-cray-3mvttt`), and merges `main`, which merged #3
(`claude/counterexample-search-ungpe2`) itself at 13:55Z on 15 September and
then added a further session on top. Read this section before the historical
handoffs below it; they are each true about their own session and none of them
is true about the whole board.

**Updated 15 September.** `main` moved after this fold was first written, and
#4 gained four more commits. Three things below changed as a result and are
marked **[15 Sep]**: the note numbering is now genuinely ambiguous *on `main`*
and fixed here; the Teichner planning advice in §4 was **wrong** and is
corrected; and `UNFINISHED.md` is now the live list of open threads — read it
alongside this, not instead of it.

## 0. Read these first

| you want | read |
|---|---|
| why route B is the only non-circular construction, and where it runs out | `research/24_why_route_b_is_circular.md` |
| why route B is *strictly harder* than the conjecture | `research/22_where_a_counterexample_can_come_from.md` §2 |
| the first invariant that separates the Abe-Tagami family | `research/21_branched_double_covers.md` |
| the audit of your own prefix-annulus lemma, and a retraction | `research/23_prefix_annulus_lemma_audit.md` §3, §8 (read §5 with §3 of this handoff) |
| the constructive frontier on D01 | `research/20_next_construction_plan.md` (yours, unchanged) |
| **what is still open and running** | `UNFINISHED.md` **[15 Sep]** |
| why most "wider" band searches here were no-ops | `results/band_generator_saturation.json` **[15 Sep]** |

## 1. Renumbering, because two sessions used the same numbers

PR #3 was opened against `0c535ca` and published `research/19_prefix_annulus_lemma_audit.md`
and `research/20_why_route_b_is_circular.md` while `main` independently
published `research/19_link_concordance_completion_gate.md` and
`research/20_next_construction_plan.md`. Git did not conflict — different
filenames — but the numbering did. On fold, PR #3's two notes were renumbered:

* `research/19_prefix_annulus_lemma_audit.md` → **`research/23_...`**
* `research/20_why_route_b_is_circular.md` → **`research/24_...`**

Your 19 and 20 are untouched and keep their numbers. References in
`scripts/alexander_rank_screen.py` and `SESSION_2026-09-14.md` were updated to
match. References to `research/20` in `scripts/teichner_mirror_partners.py` and
in the `teichner_mirror_*.json` scope strings point at *your* note 20 (the
mirror-partner lead) and are correct as written — do not "fix" them.

`research/09` is duplicated as well (`09_full_ring_floer_audit.md`,
`09_turaev_grid.md`). That predates all of this and was left alone.

The next free number is **25**.

**[15 Sep] This got worse before it got better.** When `main` merged #3 on 15
September it took that branch's files as they stood, so **`main` itself now
carries two notes numbered 19 and two numbered 20**. That ambiguity is live in
its text: `UNFINISHED.md` §5 and §7 say "research/19" and "research/20" meaning
the prefix-annulus and route-B notes, while the historical `HANDOFF` sections
say the same strings meaning the completion-gate and construction-plan notes.

This branch resolves it. Git's rename detection carried the 23/24 renames
through the merge, so no duplicates came back, and the references in `main`'s
new files are repointed: `UNFINISHED.md` §5, §7 and its standing cautions, and
`SESSION_2026-09-15.md`'s header and strategic picture. References that mean
`main`'s own notes are deliberately left alone.

## 2. The one result that could have invalidated other work, and does not

`Link.simplify('global')` **deletes split unknot components.** A trefoil with a
split unknot has Alexander-module order 0 and two components; after
`simplify('global')` it is the bare trefoil, order `a^2 - a + 1`, one component.
Any test whose intended pass is "split knot plus unknot" is inverted by this.

This produced a published false claim — that both of research/17's survivors on
J25533 fail a necessary condition — which is **retracted** in
`research/23` §8 rather than edited away. Corrected: 29 of 61 first-stage links
have positive rank, the known-good control `1918_0_-1` passes, and **both
research/17 survivors pass**. Nothing on 25533 is eliminated. On that target the
rank screen is exactly redundant with your component filter, 29 and 29.

I audited `main` for the same defect. Five scripts call `simplify('global')`:
`audit_failed_identifications.py`, `concordance_search.py`,
`teichner_bounded_probe.py`, `teichner_certify.py`, `teichner_mixed_frontier.py`.
**None of them is affected.** The three Teichner scripts simplify a connected
sum, which is a knot, so there is nothing to delete.
`concordance_search.py` reads `unlinked_unknot_components` immediately after,
with a comment saying exactly why. `teichner_mixed_frontier.py` measures its
ranks at line 58 and simplifies at line 60, in that order. That is the right
order and it should stay that way.

Your rank-zero result on the 1,092 normalized matches also reproduces
independently, by link-exterior Alexander order rather than triangulation
groups: 1,092 examined, 0 positive rank, 0 errors, identical before and after
the fix, because those links are certified nonsplit and carry no unknot
component to delete.

The lesson is the calibration, not the target: a screen whose intended pass is
"split knot plus unknot" must be calibrated on a link that has one, and must
carry a positive control drawn from a movie known to exist. Both are now
enforced in `scripts/alexander_rank_screen.py`, which refuses to report if
either fails.

## 3. The open item on your lemma: mostly closed, and PR #3 did not know it

`research/23` audits the connected planar prefix lemma. The geometry is
correct. Genus zero is redundant given connectedness. One configuration — a
complementary annulus joining the two components of `L`, with a disk bounding
`K'` — is excluded only by connectedness of the concordance and not by the
Euler count, so the statement needs that said out loud. Those three findings
stand.

Its §5 does not. **`research/23` §5 says the load-bearing step, "generic
Alexander rank is a link-concordance invariant", is asserted rather than cited.
That was true when PR #3 was written and it is no longer true.** Your
`research/19` carries the primary source — Tim Cochran and Shelly Harvey,
*Homology and derived series of groups*, Geometry & Topology 9 (2005),
2159–2191, Corollary 3.3 and the following paragraph, pp. 2169–2170 — and
`research/20` §1(2) records it re-checked on 14 September 2026 UTC. PR #3 was
branched at `0c535ca`, before either landed, so its author could not see them.
I have left §5 standing in the note rather than editing it, on this
repository's own convention about retractions, but **read it with this
paragraph next to it.**

**[15 Sep]** `UNFINISHED.md` §5, written after PR #3 merged, repeated the same
"asserted, not cited" claim. It now carries this correction inline, and its
heading is changed from "still needs one citation" to "needs one citation
*registered*, not found".

What is genuinely still open is smaller: **Cochran-Harvey has no `[Sxx]` entry
in `SOURCES.md`.** The verification register is where this repository decides
what counts as cited, and a load-bearing theorem that only appears inside two
research notes is not registered. Adding that row, with theorem number and
hypotheses, is a ten-minute job and it is the cheapest open item here.

Note also that the citation covers the *algebraic* half only. The geometric
completion lemma still requires an actual connected annulus and a fixed
connected prefix, as `research/20` says.

Terminology, so it is not rediscovered a third time: SnapPy's
`Manifold.alexander_polynomial()` on a link exterior returns the **order of the
Alexander module**, not the classical multivariable `Δ_L`. Vanishing still means
positive module rank, which is the condition actually wanted. PR #3 read the
Whitehead link's `a^2 b^3 - a b^2 - a b + 1` as violating Torres; your
`research/20` §1(3) answers that this is a meridian-basis mismatch — the
meridians abelianize as `ab` and `ab^2`, and in those variables it factors
correctly. **Your reading is the right one.** The practical conclusion is the
same either way, so the terminology correction in `research/23` §5a is
harmless, but it is not a correction.

## 4. Where each lane stands after the fold

### Teichner lane — the only constructive lane, and it is running out of partners

`D_{0,1}` is certified non-ribbon, so a verified ribbon certificate for
`D_{0,1} # J` with `J` ribbon is a counterexample outright, with nothing left to
prove. That is why the compute goes here.

Measured cost, same box throughout (`max_bands = 2`, `max_band_len = 5`):

| partner | sum crossings | wall time | finished | result |
|---|---:|---:|---|---|
| `6_1` | 31 | 4.21 h | yes | no certificate |
| `8_8` | 33 | 7.96 h | yes | no certificate, 10,023-link frontier preserved |
| `10_3` | 35 | > 12 h | **no** | killed at budget, supports no conclusion |

**Cost roughly doubles per two crossings. Do not extrapolate linearly.** Budget
a 35-crossing sum at 24 h, not 5. The two earlier 5 h kills left *no record at
all*; `teichner_certify.py` now writes an `in_progress` heartbeat before the
long call, which is the only reason the `10_3` overrun exists as a file.

`6_1` is the smallest ribbon knot, so **31 crossings is the hard floor** for any
Teichner sum on `D_{0,1}`, and that partner is done and negative. `D_{0,1}`
itself will not shrink: `simplify('global')` plus backtracking holds at 25
crossings over 120 seeds, and `K_1` at 19 over 400 seeds, and since
`D_{0,1} = 6_3 # (-K_1)` is `6 + 19`, all of its size is `K_1`
(`results/teichner_lane_size_floor.json`; a negative search, not a proof of
crossing number).

~~The fibered partners `8_9`, `8_20`, `9_27` must **not** be run: adding a fibered
ribbon `J` leaves `K_0` and `-K_1` unpaired among the fibered prime summands, so
Miyazaki still returns non-ribbon for the sum and no certificate can exist.~~

**[16 Sep] WITHDRAWN — see `ERRATA_2026-09-16.md` (E16-1).** Miyazaki Thm 5.5
requires *every* prime fibered summand to be minimal in the homotopy-ribbon
order or to have no nonunit norm factor of `Delta`. A nontrivial ribbon `J`
fails **both**: it is above the unknot in the ribbon order, and Fox-Milnor makes
`Delta_J` itself a nonunit norm. So the theorem does not apply to `D_{0,1} # J`
and cannot obstruct any Teichner sum. `8_9`, `8_20`, `9_27` are legitimate
partners at 33, 33 and 34 crossings, and are running
(`results/teichner_D01_fibered_partners.json`). The correct rule is that the sum
is excluded iff **every prime summand of `J`** satisfies an alternative — which
rules out `J = L # (-L)`, e.g. the square knot, and never rules out a prime
fibered ribbon `J`.


What remains is `9_41`/`9_46` at 34 (yours, and no result came back) and
`10_3`/`10_22`/`10_87` at 35, of which `10_22` and `10_87` were killed by
container reclamation and never rerun. After those, the non-fibered ribbon
knots up to 10 crossings are exhausted and the next partners are 11-crossing,
i.e. 36-crossing sums at 24-48 h each.

**[15 Sep] I gave you bad advice here and am withdrawing it.** The first
version of this section said that if the remaining partners come back negative,
*widening the box* on `6_1` beats climbing to 11-crossing partners. The
instinct was right; the parameter was wrong, and `results/band_generator_saturation.json`
shows why:

> **`max_band_len` saturates.** On `D_{0,1} # 6_1` at `paths='shortest'`,
> `max_twists=2`, the band count is 6,175 at length 4, 9,301 at 5, 10,145 at 6
> — and *exactly* 10,145 at length 8 and at length 14. Past 6, raising the
> length adds no bands at all.

So "widen the box" in the sense this campaign has always meant it — longer
bands — is a **no-op**, and the historical runs recorded at "length ≤ 8" and
"length ≤ 10" explored nothing beyond length 6. One run of that session at
length 14 was an exact duplicate of its length-8 sibling and was killed once
measured.

Three dials are genuinely untouched, and these are what "widening" should mean
from now on:

* **`paths='simple'`** — about **75x** the band set at saturation on the
  control. Note it is *not* a superset of `shortest` at small lengths, so
  neither subsumes the other and both are needed.
* **`max_twists`** — no saturation, roughly linear (tw=4 about 1.8x tw=2,
  tw=6 about 2.5x), and pinned at 2 in **every run this campaign has done**.
* **diagram choice** — one diagram per Teichner run, always. Four shaken seeds
  of the same 31-crossing `D_{0,1} # 6_1` give 10,071 / 10,271 / 10,356 /
  11,664 bands: same knot, same box, different band sets.

`teichner_certify.py` now exposes all three. One run of each was launched and
**none finished** — see `UNFINISHED.md` §1. The same three dials have never
been applied to the r = 0 RBG sweeps either, whose 304 and 333 two-band
survivors were all `shortest`, twists 2, at or below saturation.

**Operational rule from the same session:** observed container lifetime is
about 26 h, so a 24 h budget does not fit inside one container once startup and
other work are counted. Budget long searches at **20 h or less, and prefer a
box that finishes to a box that is merely larger.** Four searches with 24 h
budgets died mid-flight with zero partner runs completed; only the heartbeat in
`teichner_certify.py` kept a record of them at all
(`results/container_reclamation_2026-09-15.json`). Also: the rebuilt container's
first K_B calibration reads 2.96 s, which is cold-start only — repeated runs
settle at 0.52-0.71 s. Do not re-budget from a cold first measurement.

One calibration worth not re-deriving, in `TOOLING.md`: `max_bands` is **not**
the fusion number and is **not** bounded below by the genus. One band reaches
the unknot for every small ribbon knot through genus 3, because the search
recognises ribbon links through its cache. So the tempting argument that a
2-band search on a genus-6 connected sum is futile by construction is **false**,
and the existing 2-band runs are genuine coverage. That hypothesis was raised
and discarded before anything was written on its strength.

Mirror partners (PR #4): both chiralities of all seven partners were swept at
`max_band_len` 4, 6 and 8 with per-case caps of 60/120/900 s. `certified_slice`
is false everywhere. A timed-out case is **UNKNOWN, never a negative**, and
`teichner_mirror_partners_interrupted_cap420.json` is a preserved interrupted
attempt, not coverage. Your caution stands: both `6_1` and `D_{0,1}` are chiral
by Jones, so do not drop mirrored partners by assuming amphichirality.

### r = 0 RBG lane — new ground, first searches complete, no hit

The one super-special `r = 0` pair outside the Dunfield-Gong census,
`K(0,0,0,-1,2,1)`, recorded in the ledger as never searched. Now searched
(`research/18`):

| search | box | survivors | unknot |
|---|---|---:|---|
| `K_G`, 1 band, 6 diagrams | | 72 | none |
| `K_B`, 1 band, 6 diagrams | | 72 | none |
| `K_G`, 2 bands, 6 diagrams | len 5, complete, 20,190 s | **304** | none |
| `K_B`, 2 bands, 6 diagrams | len 5, complete, 38,345 s | **333** | none |

Coverage of those boxes and nothing more. Neither knot is known to be slice, so
a negative is the expected outcome and carries no information either way.

The structural fact worth carrying: **the frontier grows**, 13 to 60 from one
band to two. For `K_DG = 18nh00000601` the comparable search left only trivial
bands, which is why no two-band search could start there. This lane has real
input, and that is the whole reason to spend on it.

**[15 Sep] The strongest known killer does not fire.** Rasmussen's `s` is what
Nakamura used to kill Manolescu-Piccirillo's five topologically slice knots
(arXiv:2203.14270) and, via Dunfield-Gong Thm 5.10, 25 further RBG knots, and
`research/03` records it as obstructing both `K_B` and `K_G`. It had **never**
been computed for any RBG knot here — KnotJob was only ever pointed at
Abe-Tagami. Now it has been, for both r = 0 pairs:
`s_Q = s_{F2} = s_{F3} = 0` on `MP_KB/KG(0,0,0,-1,2,1)`, and `s_Q = 0` on
`MP_KB/KG(0,0,0,1,2,-1)` (`results/RBG_r0_s_invariant.json`). Two-sided
controls: the positive trefoil fires at 2, ribbon `6_1` returns 0. A control
that only confirmed `s = 0` would be worthless here, since `s = 0` is the
outcome being hunted.

Read this correctly: **`s = 0` is survival, not evidence.** It means the
cheapest available obstruction fails to kill these knots, which is what a live
candidate looks like — and what a slice knot looks like, and what plenty of
non-slice knots look like too.

`research/24` §4 proposes the crossing nobody has tried: an `r = 0` pair has
diffeomorphic 0-traces, so `K_B` ribbon **and** `K_G` certified non-ribbon is a
counterexample **with no concordance coincidence needed anywhere** — the only
route on this board that escapes the missing-object problem of §1 of that note.
Two blockers, both recorded rather than worked around: all ten stored MP
exteriors are hyperbolic, hence prime and not satellites, so none can carry a
Miyazaki certificate; and the MP DT-code transpiler (`../mma.py`, `../mp_auto.py`)
lived beside the original macOS clone and is in no container here. The filter is
cheap and has never been applied. It is not a theorem that the lane is
non-empty.

### Branched double covers — genuinely new data, not an obstruction

`Σ₂(K_0) = L(13,5)` (`6_3` is the two-bridge knot `S(13,5)`; `π₁ = <a | a^13>`).
`Σ₂(K_1)` has three subgroups of index 5, so its `π₁` is not cyclic and the two
are not homeomorphic; `Σ₂(K_1) ≇ Σ₂(K_2)` as well. The separating invariant is
low-index subgroup enumeration — exact and combinatorial, which matters because
SnapPy finds no positively oriented solution for either target and verified
volume fails on both. Controls `3_1`, `4_1`, `6_3` and the granny knot all
return their known answers.

**This is the first invariant in this repository that separates members of the
Abe-Tagami family. It is NOT a concordance obstruction and it changes no ledger
status.** Distinct branched double covers say nothing about `[K_0] = [K_1]`.

Construction warning: build `Σ₂` by `(2,0)` orbifold filling *then* the cyclic
double cover, letting the cover carry the induced filling. Taking the cover
first and guessing a slope fails silently — `H_1` of the cover is `Z/13 + Z`
with the longitude lift torsion, so eighteen different short slopes all return
`Z/13` and homology cannot pick the right one. Also: Regina's manifold
recognition from a SnapPy triangulation string drops the Dehn fillings and
returns coincident isosigs for non-homeomorphic manifolds. Do not use that path.

The gate this opens, offered for a second reader and **not asserted**
(`research/21` §3): `D01` smoothly slice forces the thirteen d-invariants of
`Σ₂(K_1)` to equal `d(L(13,5)) = {0, ±2/13, ±2/13, ±6/13, ±6/13, ±8/13, ±8/13}`
exactly. A mismatch proves `[K_0] ≠ [K_1]` and closes the primary lane. That is
a finite falsifiable test on one 21-tetrahedron manifold, which is a sharper
target than another band box. The cheap route to the other half is closed: forty
randomised diagrams of `K_1` (rank-9 Goeritz) and `K_2` (rank-18) are all
indefinite, so no definite filling and no lattice shortcut. It needs real
Heegaard Floer for a closed hyperbolic QHS³ and **no tool in the recorded
environment does this.** Finding or building one is a concrete task.

### WS5 is vacuous as written — close it by argument, not by running it

`CAMPAIGN_PLAN.md` WS5 proposes computing `null V(L_{3,1})` for GST's slice
link, "one afternoon of computation; expected to vanish". It is worse than
expected to vanish: it **cannot fire**. A slice link with `n ≥ 2` has `Δ(L) = 0`
(Eisermann, Remark 3.6), hence `det(L) = 0`, hence `null V(L) ≥ 1`; Lemma 1 caps
`null V(L) ≤ n-1`. At `n = 2` the bounds meet, so `null V = 1 = n-1` holds
automatically for *every* 2-component slice link. `L_{3,1}` has two components.

Still live: Eisermann **Theorem 2** on `L_{3,1}`
(`det V(L) ≡ det(K_1)det(K_2) mod 32`, not implied by `Δ(L) = 0`), and
**Theorem 1 on a slice link with `n ≥ 3`**, where slice gives only `null V ≥ 1`
while ribbon demands `n-1 ≥ 2` and the bounds no longer meet. Both need
`L_{3,1}`, which **is not in this repository**: Regina's `ExampleLink.gst()`
gives the 48-crossing band-sum *knot* `B_{3,1}`, and a band sum cannot be
reversed without its band. Building `L_{n,k}` from GST Figure 1 is the gating
task for the whole link lane.

**[15 Sep] The test is now pre-registered, and Theorem 2 has teeth.** Of 75
tabulated 2-component links scanned, only `L9n18` and `L9n19` have `null V = 1`
at all; every other fails Theorem 1 outright. On both of those, Theorem 2
**fails** — `det V = 9` and `25` against a component-determinant product of 1.
Neither is slice (linking number 4, signatures −6 and −4), so that is
calibration rather than a candidate, but it shows a link can pass Theorem 1 and
be caught only by Theorem 2, which is exactly the shape of the `L_{3,1}` test.

From GST Figure 1 and §7: `L_{n,1}` is the square knot `Q` interleaved with
`V_n = T_{n,n+1} # mirror(T_{n,n+1})`, components algebraically unlinked and
0-framed, and §8 proves the link slice. Both components are `K # −K`, hence
ribbon, with `det(Q) = det(V_3) = 9`. So the whole test is one congruence:

> **if `L_{3,1}` is ribbon then `det V(L_{3,1}) ≡ 81 ≡ 17 (mod 32)`.**

A different residue makes `L_{3,1}` slice and not ribbon.

**The blocker is honest and it is a figure.** GST describe each summand as "an
n-stranded spiral, with a full ±1 twist added relative to the plane of the
paper", interleaved. That is a picture, not a combinatorial description, and
guessing it risks a *false* counterexample — the worst available outcome.
Diao-Pan-Yan (arXiv:2604.17737) implement an algorithm for these links but
defer the details and publish no PD codes, braid words or data. Recovering
`L_{3,1}` as a band fission of the GST knot was tried instead: all three
nominations are **rejected** against the genus/fiberedness/determinant profile
of `Q` and `V_3`, and widening to length 8 and twists 3 adds none
(`results/L31_candidate_verification.json`, `results/gst_L31_*`). So the gating
task is still reading GST Figure 1 itself.

Honest limit: a link-level counterexample would not settle Fox's Problem 25,
which is about knots. It would be the first slice-not-ribbon object of any kind.

The three-line argument in `research/22` §3.1 should be checked by a second
reader before WS5 is struck from `CAMPAIGN_PLAN.md`. I have not struck it.

### J149 — terminated, and the reason generalises

Four disjoint shards, 28,520 first bands, 5,300 linking rejections, 1,355 rank
rejections, 433 intermediates, 858,930 second bands, 4 endpoints — **every one
of them K0**, the saved positive control, recovered once per shard. That is the
search recognising a movie already in the repository. Every `shard*.json` has
`complete: false`; they are partial coverage records, not completed runs.

It was stopped on purpose, and the reason is worth generalising: `research/11`
establishes that K0 and K1 share an involutive knot-Floer local equivalence
class, and the filters steering this search — HFK rank injection, the Zemke
chain-retraction condition, the quotient chain maps — **all factor through that
class**. So the guidance is blind to the distinction it is trying to resolve: it
can neither reject a wrong candidate for the right reason nor confirm a right
one. Enlarging the box does not repair that. Separately, K0 and K1 are not
related by bands at all — they are the `(n+1,n)` and `(n-1,n)` fillings of the
single 3-cusped exterior in `data/knots/AbeTagami_L_63_c1_c2.json`, and this
search discards that structure to shake bands on the filled diagrams.

Not a proof that no common successor exists. Not evidence that one does.

### `graph-reconstruction/` — a separate project living in this repo

PR #2 also carried a self-contained side project on the Kelly-Ulam
reconstruction conjecture: a nauty-backed exact deck engine (canonical forms,
not hashes, so a reported collision is real), exhaustive deficit measurements
through `n = 9`, and a reading of Ivanov [arXiv:2608.11930] separating
common-card *fraction* from *absolute deficit* — the fraction tends to `1 - 1/r`
while the deficit diverges. **No counterexample found; Kelly-Ulam stands.**
Cai-Furer-Immerman pairs share 0 cards out of `n` over eight bases, so that axis
is closed. `python-igraph 1.0.0`'s `canonical_permutation()` is broken and must
not be used for this.

It is unrelated to slice-ribbon and it is folded in because it existed, not
because it belongs. **If you would rather it lived in its own repository, say
so and it lifts out cleanly** — it is one self-contained directory with no
imports into the knot code.

Two dangling references in it, found on fold and **not** papered over.
`graph-reconstruction/RESULTS.md` and `graph-reconstruction/deck.py` both point
at `tests/test_deck.py`, which was never committed — the only file in `tests/`
is `test_research_audit.py`. So the claim that python-igraph 1.0.0's
`canonical_permutation()` is broken has no test in this repository backing it;
it is an assertion in a comment. And the reproduce block's `python3
margin.py_driver` is not a runnable command. I did not invent a test file to
close the gap. Either write the test or strike the pointers.

## 5. What I did not do

* **No new mathematics.** This session read, folded, renumbered and audited. The
  only original work is the `simplify('global')` audit of `main` in §2, the
  numbering resolution in §1, and the correction to `UNFINISHED.md` §5.
* **[15 Sep] I did not run any of the three untouched dials**, or restart any of
  the four Teichner searches that container reclamation killed. They are listed
  in `UNFINISHED.md` §1 and they stay listed.
* **No search was started, stopped or resumed**, and no running job was touched.
* **No ledger status changed.** `CANDIDATE_LEDGER.md`, `OBSTRUCTION_MATRIX.md`
  and their CSVs are untouched, including for the branched-cover separation,
  which is not a concordance fact.
* **WS5 is still in `CAMPAIGN_PLAN.md`**, unstruck, pending the second reader.
* **Nothing was verified by re-running it.** Every number in §4 is read from
  the committed result files and the notes, not recomputed. Neither `snappy`
  nor `pytest` is installed in this container and I did not build the
  environment, so `tests/test_research_audit.py` was **not** run. What I did
  check: all three merges are conflict-free, every script added by the fold
  byte-compiles, the one auto-merged file (`scripts/two_fission_target.py`,
  where `main`'s overpassing-component fix and PR #2's sharding touch different
  hunks) reads correctly after the merge, and every path referenced from
  `README.md`, `MANIFEST.md` and this handoff resolves — except the two
  dangling `graph-reconstruction` pointers called out above.
* No budget was consumed on the shared Codex meter and **nothing here authorises
  a restart.**

## 6. Ranked next actions

Reordered **[15 Sep]** now that saturation is known: the cheap repeat of an
already-run box is gone, and two items moved up because the dials are new.

1. **Turn one of the three untouched dials on a box that already finished.**
   `paths='simple'` on `D_{0,1} # 6_1` is the single highest-value run
   available — about 75x the band set, on the cheapest sum, in a lane where a
   hit is a proof. Budget ≤ 20 h. Then `max_twists`, then diagram seeds. Apply
   the same three to the r = 0 sweeps, which have never seen any of them.
2. **Finish the four killed Teichner searches** (`UNFINISHED.md` §1) and the
   partners that never ran: `9_41`, `9_46`, `10_22`, `10_87`. Not at 24 h —
   see the container rule in §4.
3. **Register Cochran-Harvey in `SOURCES.md`** with a `[Sxx]` number, theorem
   number and hypotheses (§3). Ten minutes, and it is what makes the
   rank-based exclusions cited rather than merely correct.
4. **Compute `s(D_{0,2})` on a bigger machine.** It failed twice on memory at
   47 crossings (`-Xmx3g` and `-Xmx5g` with four band searches resident on a
   15 GB container) and `s(D_{1,2})` at 60 was never attempted. `s(K_2) = 0` did
   land. A nonzero `s(D_{0,2})` proves `D_{0,2}` not slice, hence `K_0` not
   concordant to `K_2`, killing that pair outright. That is a real kill
   condition, not another coverage run.
5. **Read GST Figure 1 and build `L_{3,1}`.** Gates the only computable
   ribbon-only obstruction family in the catalog, and the test is now a single
   pre-registered congruence (§4). Do not guess the spiral.
6. **Find or build a Heegaard Floer tool for a closed hyperbolic QHS³** and run
   the `d(Σ₂(K_1))` test. Finite, falsifiable, and it closes the primary lane
   either way.
7. **Get a second reader on `research/22` §3.1** before striking WS5.
8. **Apply the `research/24` §4 filter** — prime-summand decomposition and
   fiberedness on `r = 0` realizations, selecting the side that is already
   certified non-ribbon. Needs `../mma.py` and `../mp_auto.py`, which no
   container here has.
9. Re-audit any older script that simplifies a link before measuring an
   invariant. I covered `scripts/`; I did not audit the notebooks or anything
   outside this repository.

One lead nobody has picked up, from `UNFINISHED.md` §8 and worth repeating: the
**Abe-Tagami monodromy is explicit** — `t_{c'_1}^{-n} t_{c'_2}^{n} t_d^{-1} t_b
t_c^{-1} t_a` on a genus-2 once-punctured fiber, in
`data/knots/AbeTagami_K_n_NOTES.json` — and has never been used
computationally in this repository. Whether it gives any purchase on
concordance is unknown, which is exactly why it is interesting.

## 7. Standing cautions, unchanged

Every search here is coverage, never an obstruction. A timed-out case is
UNKNOWN, never a negative, and **an unfinished search supports no conclusion at
all**. A "wider" box is not wider if the generator has saturated. `s = 0` is
survival, not evidence. Component Jones equality does not identify a knot. A
polynomial coefficient distance is a sorting heuristic and nothing else. Passing
a determinant filter proves no sliceness. Positive endpoints need oriented
peripheral identification, orientation checks and a replayable movie before they
are anything at all. Never treat a deficient finite specialization as generic
rank. For K_G and GST, sliceness and global non-ribbonness are separate
obligations. The explicit Hom-Park member is already obstructed from sliceness
and should not be reopened.

---

## Historical session checkpoints — all superseded by the fold above

Each section below is true about its own session and about no other. Branch
names, schedules, budgets and "work remains on `main`" statements in them are
historical; every branch named below is now merged into `main` and deleted.

# Session checkpoint — 14 September 2026, PR #4 (branched double covers)

**No counterexample found.** Read `research/21_branched_double_covers.md`,
`results/branched_double_cover_gate.json` and `results/lens_d_invariants.json`.
Work is on branch `claude/inspiring-cray-3mvttt`; `main` was not touched and no
running job was interrupted.

This session supplied the branched-cover data every previous handoff recorded as
missing. It is new data, not progress toward a disk.

**Rigorous new facts.** Sigma_2(K_0) = L(13,5) (6_3 is the two-bridge knot
S(13,5); computed pi_1 = <a | a^13>). Sigma_2(K_1) has three subgroups of
index 5, so its pi_1 is not cyclic and Sigma_2(K_0) is not homeomorphic to
Sigma_2(K_1). Sigma_2(K_1) is not homeomorphic to Sigma_2(K_2) either. The
separating invariant is low-index subgroup enumeration: exact and combinatorial,
with no numerical geometry — which matters, because SnapPy finds no positively
oriented solution for either target and verified volume fails on both. Controls
(3_1, 4_1, 6_3, and the granny knot as a non-cyclic positive control) all return
their known answers, and every profile was replayed from an independently
simplified diagram. **This is the first invariant in this repository that
separates members of the Abe-Tagami family. It is NOT a concordance obstruction
and does not change any ledger status.**

**Construction warning.** Build Sigma_2 by (2,0) orbifold filling followed by the
cyclic double cover, letting the cover carry the induced filling. Taking the
cover first and guessing a slope fails silently: H_1 of the cover is Z/13 + Z
with the longitude lift torsion, so eighteen different short slopes all return
Z/13 and homology cannot pick the right one.

**The gate this opens.** Because Sigma_2(K_0) is a lens space, half the
d-invariant obstruction is now computed: d(L(13,5)) = {0, +-2/13, +-2/13,
+-6/13, +-6/13, +-8/13, +-8/13}, symmetric under negation because 6_3 is
negative amphichiral and 5*8 = 1 mod 13, so no orientation convention is
load-bearing. The claim written out in research/21 section 3 — offered for a
second reader, not asserted — is that D01 smoothly slice forces the thirteen
d-invariants of Sigma_2(K_1) to equal that multiset exactly. A mismatch proves
[K_0] != [K_1] and closes the primary lane. This is a finite, falsifiable test
on one 21-tetrahedron manifold, which is a sharper target than another band box.

**The cheap route to the other half is closed.** Forty randomized diagrams of
K_1 (rank-9 Goeritz forms) and K_2 (rank-18) are all indefinite, so there is no
definite filling and no lattice shortcut; 6_3 returns a negative definite rank-3
form of determinant 13 on the first try. Computing d(Sigma_2(K_1)) needs real
Heegaard Floer for a closed hyperbolic QHS^3. No tool in the recorded
environment does this. Finding or building one is the next concrete task.

**Environment.** The documented stack reproduces from a bare container with
`pip install snappy regina passagemath-standard sympy z3-solver`: SnapPy 3.3.2,
Regina 7.4.1, passagemath 10.8.11 (sage-backed), knot_floer_homology present.
Regina's manifold recognition from a SnapPy triangulation string dropped the
Dehn fillings and returned coincident isosigs for non-homeomorphic manifolds;
do not use that path.

No budget was recorded for this session and none was consumed on the shared
Codex meter. Nothing here authorizes a restart.

---

# Current handoff — late 13 September MDT / 14 September UTC

**STOPPED: no overnight Codex session. No counterexample found.** Read
`research/20_next_construction_plan.md`. Scott requested planning and an audit,
leaving Opus undisturbed; no Claude message or job change was made.

New endpoint component screening: **96 D01 paths -> 95 unresolved**;
**71 Opus K_G paths -> 70 unresolved**. The excluded paths are zero-based
D01 index 49 (Fox–Milnor) and K_G index 2 (computed tau -1). Full Alexander
polynomials were checked independently. **D01 index 73 has inconsistent HFK
output and remains UNKNOWN.** See `results/september14_frontier_components.json`
and `results/september14_frontier_validation.json`.

The claimed missing rank-invariance citation already exists. Opus's Whitehead
Torres mismatch was a meridian-basis mismatch, verified exactly. His new
start record does not preserve unfinished searches or the partner certificate
before the long call. Do not interrupt his ongoing jobs to fix that.

Tomorrow's priority: audit any completed Opus certificate, then resolve the
oriented whole-link mirror(6_1) stabilization and search its disk completions.
Neither this plan nor time passing authorizes an automatic restart.

---

# Current handoff — 13 September 2026, evening

**No counterexample found.** Read `research/19_link_concordance_completion_gate.md`, `results/evening_session_validation.json`, and `results/teichner_frontier_validation.json`. Work remains on main. Research note number 18 is reserved by Claude PR #3; no branch was created, removed or merged here.

**Construction priority:** Teichner certificates for D01 # J with J ribbon.
No sum certificate has been found. New partners 9_41 and 9_46 have separately
replayed ribbon certificates. Mixed-attachment and third-band searches save
full paths. Native Sage/Singular Fox-Milnor minors segfaulted; preserve the
logs and use the local conservative replacement, not an environment change.

**Current frontier (supersedes intermediate 350-path count):** A Miyazaki
component gate rejects 74 of 587 initial saved links, or 237 with inherited
prefix exclusions. Later component slice checks reject 803 of 805 remaining
and deeper paths by nonsquare component determinants. All 392 distinct
determinants agree independently with Regina Jones. Two first-stage paths
remain, both under 9_46: `78685a_1_-2`, `00676e_0_-2`. Continuing them across
the selected full shortest-band box tests 24,359 moves and saves **96 unknown
paths**, no ribbon certificate. Start with
`results/teichner_D01_J946_component_filtered_continuation.json` and its
validation; this is the constructive frontier, not the earlier unfiltered list.

**Missing partner orientation:** The second surviving knot component is
matched to the unoriented factors of D01 # mirror(6_1) after seeded
simplification. The signatures allow reversing factor orientations; a full
oriented connected-sum identification is not certified. The first has recognized
K0 and mirror(6_1), with its 19-crossing factor still unknown. The old 4.2-hour
run used 6_1, not its mirror. Both 6_1 and D01 are chiral by Jones, so do not
drop mirrored partners merely by assuming the target is amphichiral.
The 96 latest paths still require tau/Fox-Milnor and ribbon-specific screening;
passing their current determinant filter proves no sliceness.

**Validation:** 587 initial raw moves, 455 third-band moves, and 96 final
continuation moves are separately checked. 84 factor records support the
Miyazaki gate; all factor calculations finish, and Seifert evaluations agree
with HFK Alexander data. A component that cannot be ribbon blocks every
pure-fission ribbon-disk continuation of that prefix. This is not an
obstruction to an arbitrary smooth slice disk for D01.

**Link concordance gate:** All 1,092 normalized matches from research/17
have generic multivariable Alexander H1 rank zero; all are independently
checked using triangulation-derived groups and exact integer minors.
A split knot/unknot pair has rank one and link concordance preserves it.
The connected planar prefix completion lemma is proved in research/19;
it rules out arbitrary annular completions of a fixed prefix, not all
possible endpoint concordances. The proposed independent Claude review
was not confirmed delivered through the app. The 61 older first links
have 32 additional colored-rank exclusions; the two Kh survivors remain.
Never treat a deficient finite specialization as generic rank.

**Other completed checks:** New embedded band cores may return to a face
but cannot cross an original edge twice; face chords must not interleave.
35,930 samples yield 35,521 rank exclusions and 409 unknown retained
links, all replayed. No opposite-source Jones match and no known-source
return in this restricted sample. Preserve that missing positive control.
Rational odd Kh (Migdail–Wehrli 2607.04018v1 Thm 8, preprint) passes
J25533/J25541 and C2/C4. KnotJob returns reduced odd Kh; reconstruct
unreduced by quantum shifts +1 and -1. Do not use arbitrary odd primes
with that theorem. Eight Euler checks and the K1 mirror check pass.

**Coordination:** Scott pasted Claude's report. PR #3 at 579abda was
inspected read-only; its RBG survivor counts are not independently rerun.
Preserve `claude/counterexample-search-ungpe2` and its jobs. The existing
Claude configuration was unchanged. Computer Use inserted a coordination
prompt but did not confirm submission; do not claim a reply was received.

**Budget:** this is the authorized 17:30 MDT session, fresh shared-meter
baseline 38%, target 47%, hard ceiling 48%, stop by 22:30. The local
`work/slice_ribbon_budget.json` outside the repository records final
accounting. Pause the one-session heartbeat when checkpointed. Unused
allowance does not roll over, and the end of a window authorizes no new work.

---

## Historical checkpoints — priorities and schedules below are superseded

# Current handoff — 13 September 2026, extra afternoon session

**No counterexample found.** Read `research/17_fission_ancestry_and_linking.md`
and `results/component_session_validation.json` first. Work remains on `main`.

The key new deduction is component ancestry in a reverse movie with only
fissions, isotopies and split unknot deaths: one intermediate component must
be ribbon-concordant above K1 and every other component must be ribbon.
The proof and exact restrictions are written in research/17. It is NOT a
condition for movies with later fusion saddles or births. Do not demand that
the distinguished component already equal K1 before its last fission.

Applied to the 61 saved intermediates of J25533, determinant/HFK tests retain
15, and full graded F2 Kh retains only two first bands:
`6267660c_0_0` and `2b2a271f_1_0`. All eight relevant component Kh computations
finish (three reused by exact diagram signature), with checked Euler polynomials.
The 59 exclusions apply to every pure-fission completion of those particular
intermediates. A second-saddle search on the two survivors tested 39,176
zero-linking fissions without a K1/U/U component Jones match.

`results/component_guided_K1_to_K0.json` contains 239 retained component
Jones/HFK matches on five K1-built upper knots, all nonsplit by whole-link
Jones. `results/normalized_component_neighborhoods.json` removes the twist
parameter and varies up to two crossing choices: 6,623 normalized bands,
1,092 retained matches, all zero-linking and provably nonsplit. Of these,
156 have explicitly matching K0 and unknot component diagrams. Counts are
diagrams, not isotopy classes. K0-built survivors produced no K1 component match.

A full twist preserves the component knot types of a fission while changing
coherently oriented linking by one. The library may reverse orientations on
rebuilding: the original signed-slope pilot failed. The preserved regression
is in `results/fission_twist_orientation_regression.json`. The correction
tries both signs and directly verifies linking zero. Never silently ignore
the failed pilot, equate polynomial equality with splitness, or treat a
polynomial coefficient score as a geometric distance.

**Next construction:** change band attachments and paths, with explicit split
K0/U as a boundary condition, while tracking the known K1 birth-and-band
presentation. Explore simultaneous moves of the two presentations, not only
more twists on the same core. This proposed construction is not implemented
and is not guaranteed. Continue to screen new common upper knots by HFK/Kh.

The next session is **17:30 MDT today**, replacing 17:50, with a fresh shared
usage baseline, at most ten additional percentage points, a buffer, and a
22:30 stop. No unused allowance rolls over. Read the local budget ledger and
latest user instructions before starting. Claude's audit prompt is saved in
the local outputs directory, but was NOT sent: Computer Use found the Mac
locked. Existing Claude setup and remote branches were left unchanged.

---

## Historical earlier afternoon checkpoint — superseded priorities and schedule

# Handoff — 13 September 2026, afternoon

**No counterexample found.** Start with
`research/16_nonfibered_khovanov_gate.md` and
`results/nonfibered_session_validation.json`.

New computational obstruction: graded unreduced Khovanov homology over F2
excludes 46 of the 48 nonfibered targets in the 60-entry K0 wider pool.
The other 12 entries are fibered, not nonfibered. Only indices **25533 and
25541** survive. Both also pass Q and F3; the full sl3 target calculations
remain inconclusive after 60-second timeouts. All completed Kh Euler
characteristics agree with independently computed Regina Jones polynomials.

The known K0 -> J movies pass their Kh positive controls. K0's F2 Kh ranks
are bounded by K1's in every bigrading, so K1-built genuine ribbon upper
knots automatically pass this particular Kh test for both sources. The
existing K1 threaded archive has 1,111 nonfibered HFK-envelope survivors.
Five 25-crossing candidates were selected in `results/K1_nonfibered_shortlist.json`.

Focused one-fission searches tested 119,242 bands on the two K0 survivors
and 128,369 on those five K1 targets. Known-source diagram controls return;
no opposite-source HFK match was found. A two-fission pilot on 25533 also
returns only K0. These are incomplete geometric searches, not concordance
obstructions. Broad searches were stopped after the Kh filter; their partial
checkpoints and failed pilot are preserved.

The Alexander-rank helper now accounts for wholly overpassing components,
which `_pieces()` omitted. The real missing-generator regression and a
rejected, nonplanar hand-built test fixture are recorded. The latter was
replaced by a planar control. Do not treat failed checks as discarded data.

**Next:** use the combined HFK/Kh gate before searching a target; do not
resume the 46 excluded targets or fibered J149 by default. Develop a
component-guided two-stage search: distinguish wrong component knots from
correct components that remain linked, and preserve those near-matches.
Explore alternative diagrams and longer edge paths before increasing the
same shortest-first caps. Prove every geometric implication before claiming
an annulus in S3 x I or a disk in standard B4.

Session accounting is in the local `work/slice_ribbon_budget.json`, outside
this repository. The separate **17:50 MDT** wakeup remains scheduled with a
fresh shared-usage baseline and a maximum of ten additional percentage
points. Unused first-session allowance does not roll over. The old budgets
and priorities below are historical. Work in this session stays on `main`;
no branch was created or deleted.

---

## Historical morning checkpoint — superseded priorities and budget

# Current handoff — 13 September 2026

**No counterexample found.** Read `research/15_infection_target_compatibility.md`
first: zero-winding infection cannot preserve the fibered target if an infection
torus remains incompressible; adding meridians changes its Alexander polynomial
for nontrivial fibered companions. Keep infection and annulus twisting distinct.
The preceding exact audit is `research/14_marked_annulus_audit.md`. These supersede the priorities in the
historical handoff below. This session's changes remain on `main`; no branch
was created. The final remote check found `claude/pensive-hopper-3rh6p4`
with eight unmerged commits through f15e803, including a terminated J149
search and separate graph-reconstruction work. That concurrent work was
preserved, not merged or deleted. Do not assume the remote has only one branch.

New exact result: the fixed surgery circles have images of trace 1 and 4 in
SL(2,F5), with orders 6 and 3. They cannot cobound even a mapped annulus in
the standard product-disk exterior. Four triangulation seeds, geometric and
simplified relators, peripheral conjugators, and a standalone checker are
saved in `results/annulus_group*` and the corresponding scripts.

The fixed two-handle trace exterior has full group Z: its compact presentation
reduces after killing a generator commutator. Its equivariant intersection
determinant is Delta(t)^2 up to a Laurent unit, by the written duality proof.
It cannot lose a disjoint S2xS2 summand while preserving the annulus and become
a standard-product concordance. This does not obstruct the endpoints from
being concordant by a different annulus. See the n=-1 endpoint control.

**Next constructive task:** specify mixed band sums of the four circles in
`data/knots/AbeTagami_marked_product_scaffold.json`. Seek actual based words
uv and vu, then identify the surgery link/framing and boundary knot before
attempting an embedded standard annulus. This is a proposed construction;
the saved five-component link is only an input scaffold. Nonribbonness must
remain independently certified for any resulting knot.

J149 is downgraded: the Agol–Ren claim after Question 1.15 concerns the genus
of the inputs, so a genus-four target does not escape it. Treat the preprint
claim as a priority warning until its argument is reconstructed, not as a
new certified discard. Do not resume broad J149 searches by default.

Today's allowance: seven additional shared weekly percentage points, baseline
26% at 09:49 Edmonton, ceiling about 33% with a buffer. This is a manual cap
for the authorized session, not seven points automatically every five hours.
The old reminder was updated to a one-time 13:33 MDT wakeup today, authorized
to resume only within the unused morning allowance after checking fresh usage
and the latest user messages. The extra light pass has baseline 28%, ceiling
30% with a buffer, within the morning allowance. No new allowance is granted
by the reminder or by the end of a five-hour window.

## Historical handoff — 12 September (priority recommendations superseded)

**No counterexample found.** Read `RESUMED_2026-09-12.md` and research notes
10–13 before planning more work. The target is D01=K0#(-K1). Its audited
nonribbonness remains applicable; its smooth sliceness in standard B4 is
unproved. The missing object is a smooth concordance K0→K1.

User authorization: push this repository, keep `main` as the sole branch,
and use Opus for critiques. Working clone:
`/Users/scottg/Documents/Codex/2026-09-12/hey/work/SR-Foxy`.
Do not switch to the stale saved checkout or overwrite its user changes.
Python from this clone: `../knot-venv/bin/python`.

The resumed session started at 14% on the shared weekly meter, with at most
13 additional percentage points authorized (cap 27%, planned wrap by 26%).
The user's mistaken 15% message was subsequently corrected with an instruction
to keep working. This is a cap for this resumed session, not authorization for
another automatic session. Automation `resume-slice-ribbon-research-at-4-30`
was PAUSED during the resumed session. Do not schedule another budget or
restart from the earlier 4:30 instructions. Check fresh usage and current
user authorization before any further session.

## Main new results

* New coupled-birth movies: both unknots exist before either fusion. Return
  loops and longer paths now reach an exactly verified nonsplit intermediate
  (K0 double-return first saddle 20). Its Jones value at q=2 mod101 is 29,
  versus 88 for a split product. The endpoint family is still incomplete.
* 32,768 main moves replayed, 2,518 HFK attempts, 2,436 completed, 82 unknown,
  228 common-rank passes. Combined indices have 267 and 1,962 records and no
  diagram/numerical/factor matches. Do not treat these as global knot counts.
* Concrete new target J149: K0 batch1 move 10187, first saddle 319, 26 crossings,
  fibered genus four, rank149, determinant117, torsion order1. It passes both
  sources' rank, quotient-chain-map and retraction filters. ONLY the K0 movie
  exists. Bounded one-fission/death search tried 7,130 bands without a K1 hit.
* Sharper necessary bounds: genus-two common successor rank≥29 and nonfibered;
  fibered common successor genus≥4. See note10 for qualifications.
* All 256 full mixed differentials are basis-conjugate. An independent checker
  verifies all 4,096 involutive local-projection cases. Conditional on the
  stored Floer inputs/lifting, both sources have the figure-eight involutive
  local-equivalence class. Repeating invariants factoring through that class
  cannot distinguish them. Branched-cover and satellite data are not covered.
* The (2,13) linking/character basis gap is resolved. Fox→Dehn→Goeritz gives
  B=[[9,2],[2,2]]; the two isotropic lines (1,3),(1,8) both have the explicit
  norm square in note13. A second shading and a ribbon control agree. This
  specific refinement does not obstruct D01.
* The torsion script's largest-entry shortcut was wrong. Exact Smith form plus
  independent binary ranks now gives K0=K1=J149=KG=KB=1 and GST=2. A finite
  fusion lower bound is not a global nonribbon obstruction.
* Isolated KnotJob results and failures are recorded; do not repeat jobs
  already finished or call timeouts zero. The session report gives the scope.
* Higher-cover HKL manifests preserve exact methods and timeouts. Advanced
  (4,3),(4,13),(8,3),(8,13), and direct (4,3),(8,3), all return no obstruction.

## Most valuable next work

Extend the new two-fission reverse search from J149, or search for a matching
K1 successor using longer/returning band paths. The 180-second reverse pilot
generated 2,207 first and 311,098 second candidates, retained 157 intermediate
diagrams after linking/Alexander filtering, and recovered only K0. See
`results/two_fission_J149.json`; almost all second stages hit their 2,000-band
cap. The Alexander filter has positive and negative controls. Do not require
intermediate vertices to satisfy final-target HFK bounds. The saved K0 movie
is a positive control for reversing both saddles. A local inverse of its last
saddle can be recovered by trying the four strand indices on each of the two
band-end crossings; crossing rotations matter. The new bounded two-fission search recovers K0 through a different saved
control (`0b06_0_0`, `1918_0_-1`), but does not provide a K1 movie or a geometric
certificate.

Every positive endpoint meeting still requires oriented peripheral knot
identification, orientation checks, and a replayable annulus movie. A numerical
isometry signature or algebraic chain map is only a nomination. For KG/GST,
sliceness and global nonribbonness are separate obligations. The explicit
Hom–Park input is already obstructed from sliceness and should not be reopened.

Before new edits, inspect status and fetch/check origin/main. Preserve all
raw archives and hash-referenced source complexes, especially the large
`results/chain_map_filter_wider.json`. No need to redo completed checks unless
inputs or implementation change.
