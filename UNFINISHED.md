# UNFINISHED

Open threads at the end of the 14-15 September sessions. **No counterexample to
the Slice-Ribbon Conjecture was found.** Everything below is either a search
that was still running when the session ended, a test that could not be run
here, or a lead that was identified but not executed.

Nothing in this file is a result. Results live in `results/` and `research/`.

---

## 1. Four Teichner searches, running and unfinished

All on `D_{0,1} = K_0 # (-K_1)`, which is certified non-ribbon, so a **verified
certificate for `D_{0,1} # J` with `J` ribbon is a counterexample outright**.
This is the only lane on the board where a hit is a proof rather than a
candidate.

| search | box | status |
|---|---|---|
| `6_1` | 2 bands, len 4, **paths=simple** | unfinished; first `simple` run ever here |
| `6_1` | 2 bands, len 6, **twists=4** | unfinished; strictly contains the completed len-5 run |
| `6_1` | 2 bands, len 6, **seed 3 diagram** | unfinished; first shaken-diagram run ever here |
| `10_3` | 2 bands, len 5 | unfinished; completes the partner sweep |

None had completed a partner search when the session ended. Each wrote a
heartbeat, so `results/teichner_killed_runs_archive.json` records the attempt.
**An unfinished search is not coverage of its box and supports no conclusion.**

Completed for comparison: `6_1` at len 5 (4.21 h, no certificate) and `8_8` at
len 5 (7.96 h, no certificate, 10,023-link frontier preserved in
`results/teichner_D01_8_8_frontier.json.gz`).

## 2. Partners not yet run

`9_41` and `9_46` (34-crossing sums) were left to Astra and no result came
back. `10_22` and `10_87` (35-crossing sums) were killed by container
reclamation and never rerun to completion.

~~`8_9`, `8_20`, `9_27` must **not** be run: they are fibered, and adding a
fibered ribbon `J` leaves `K_0` and `-K_1` unpaired among the fibered prime
summands, so Miyazaki still gives non-ribbon and no certificate can exist.~~

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

After those, the non-fibered ribbon knots of at most 10 crossings are
exhausted, but with the three above restored the lane has three more tractable
partners than this file claimed, in its cheapest crossing band.

## 3. `s(D_{0,2})` and `s(D_{1,2})` — could not be computed here

`scripts/run_knotjob.py` deliberately excluded the 41- and 47-crossing inputs
from its bounded pass, preserving them "for the larger follow-up session".
Partially picked up: **`s(K_2) = 0`** at 41 crossings, with the trefoil control
firing at 2.

`s(D_{0,2})` at 47 crossings **failed twice** on memory (`-Xmx3g` and `-Xmx5g`,
with four band searches resident on a 15 GB container), producing no output at
all. `s(D_{1,2})` at 60 crossings was not attempted. These are resource
failures, not results.

Worth finishing on a bigger machine: `s(D_{0,2}) != 0` would prove `D_{0,2}` not
slice, hence `K_0` not concordant to `K_2`, killing that pair outright.

**[16 Sep] Picked up, and the diagnosis was right: it was the heap.** KnotJob was
rebuilt **from source** under `javac 21` (the distributed jar needs Java 23, which
this container does not have; the author states the source is Java 11 compatible,
and it compiles clean). The full control set was re-run on the new build rather
than assumed equivalent: `s(+3_1) = +2`, `s(-3_1) = -2`, `s(4_1) = 0`,
`s(6_1) = 0`, all correct. On that build `s(K_2) = 0` **reproduces in 8 seconds**
at 41 crossings — the earlier session's decision to hold the 41-crossing input
"for the larger follow-up session" was over-cautious by three orders of
magnitude. `s(D_{0,1}) = 0` in 5 s.

`s(D_{0,2})` at 47 crossings is running at `-Xmx11g` and sits at 11.4 GB resident,
which is exactly why `-Xmx3g` and `-Xmx5g` produced no output at all: the heap was
the binding constraint, not the algorithm. It may still hit the ceiling. Log:
`results/s_D02_47cr_2026-09-16.log`. `s(D_{1,2})` at 60 crossings now has a
generated input (`data/knots/AbeTagami_D_1_2.json` -> 60-crossing PD) and is
queued behind it. **Until one of them prints a value these remain resource
failures, not results.**

## 4. The untried crossing that needs files outside this clone

`research/24` §4. An `r = 0` RBG pair has diffeomorphic 0-traces, so a ribbon
disk on one side certifies the other slice **with no inherited ribbon disk**.
The ledger uses this only to generate fresh Tier-A candidates. But if the
partner **already carries a non-ribbon certificate**, a ribbon disk on one side
is a counterexample outright, **needing no concordance coincidence anywhere**.
It is the only route on this board that escapes the reduction in §7 below.

It is not empty on arrival: `r = 0` does not force Alexander polynomial 1.

It cannot be run here. All ten stored MP exteriors are hyperbolic, hence prime
and non-satellite, so none can carry a Miyazaki certificate; and the transpiled
RBG generator lived at `../mma.py` and `../mp_auto.py` beside the original
macOS clone, which this container does not have. **Recover those two files and
the filter is cheap**: decompose each `r = 0` knot into prime summands, keep
those that are connected sums of prime fibered knots with a common irreducible
Alexander polynomial that do not pair, band-search the partner. Note it inverts
the usual taste, since MP and DG both steer toward hyperbolic knots.

## 5. Astra's lemma needs one citation *registered*, not found

`research/23` §5. The step "generic Alexander rank is a link-concordance
invariant" is asserted, not cited, and is not multivariable Fox-Milnor. Every
rank-based exclusion is conditional until a primary source is in the ledger.

**Correction, added on the 14-15 September fold.** The source is not missing.
`research/19` carries it — Tim Cochran and Shelly Harvey, *Homology and derived
series of groups*, Geometry & Topology 9 (2005), 2159-2191, Corollary 3.3 and
the following paragraph, pp. 2169-2170 — and `research/20` §1(2) records it
re-checked on 14 September 2026 UTC. `research/23` was branched at `0c535ca`,
before either landed, so its author could not see them; §5 is left standing
rather than edited, per this repository's convention on retractions.

What is actually open is narrower: **Cochran-Harvey has no `[Sxx]` row in
`SOURCES.md`.** The verification register is where this repository decides what
counts as cited, and a load-bearing theorem appearing only inside two research
notes is not registered. Adding that row, with theorem number and hypotheses,
is a ten-minute job. Note the citation covers the *algebraic* half only: the
geometric completion lemma still requires an actual connected annulus and a
fixed connected prefix.

Lower priority than it looked for a second reason too: §8 of `research/23`
shows the screen is **exactly redundant** with research/17's existing filter on
J25533 (set equality, band for band), so nothing currently rests on it.

## 6. Search dimensions opened but barely explored

`results/band_generator_saturation.json`. `max_band_len` **saturates** (at 6 on
`D_{0,1} # 6_1`), so the historical runs at "length <= 8" and "length <= 10"
explored nothing beyond length 6. Three dimensions were never touched:

* `paths='simple'` — 75x the band set at saturation on the control
* `max_twists` — no saturation, pinned at 2 in every run this campaign has done
* diagram choice — one diagram per Teichner run, always

`teichner_certify.py` now exposes all three. One run of each was launched and
none finished. **Caveat:** `simple` is not a superset of `shortest` at small
lengths, so neither subsumes the other and both are needed.

The same three dials have never been applied to the **r = 0 RBG sweeps**
either, whose 304 and 333 two-band survivors were all `shortest`, twists 2, at
or below saturation. That is a straightforward extension nobody has run.

## 7. The structural obstacle, unresolved

`research/24`. Every route-B non-ribbon certificate (Miyazaki fibered pairing,
Miyazaki Example 2, Hom-Park) reduces to the same missing object: **a pair of
distinct, concordant, fibered knots**. Satellite constructions cannot
manufacture one, because satelliting a ribbon concordance yields a ribbon
concordance and the difference comes out ribbon, not merely slice. Teichner is
the only constructive lane that escapes this.

The Abe-Tagami `K_n` remain the best candidate pair, and whether
`K_0` is concordant to `K_1` is exactly the open question. Nothing in these
sessions moved it.

## 8. Route A remains blocked by a theorem-shaped gap

`research/06`, `research/07`. For `K_DG = 18nh00000601` the gap is **exactly
Generalized Property R**, and all Milnor invariants of every R-link vanish, so
no nilpotent invariant can separate ribbon from handle-ribbon. Proving
non-ribbonness needs a non-nilpotent invariant of derivative links applied to
**every** derivative, which needs the fiber and monodromy explicitly. Not
available.

**[16 Sep] Before proposing a Floer computation on this pair, read
`research/26` §2.** `CFK^infinity` for `K_0` and `K_1` up to local equivalence is
**already computed** — `research/09` and `research/11`, 12 September — and the
answer is that they share the same *involutive* local-equivalence class, the
figure-eight's. So `tau`, `epsilon`, `nu`, `nu+`, `Upsilon` and the
Dai-Hom-Stoffregen-Truong `phi_{i,j}` **all agree**, and none of them can separate
the pair. Re-verified bit-for-bit on 16 September. Conditional on the same
input/lifting dependency `research/09` carries. Directly recomputed today for
completeness: `tau = nu = epsilon = 0` for `K_0`, `K_1` and `K_2` alike.

Note for whoever picks this up: the Abe-Tagami monodromy **is** explicit and is
recorded in `data/knots/AbeTagami_K_n_NOTES.json` as
`t_{c'_1}^{-n} t_{c'_2}^{n} t_d^{-1} t_b t_c^{-1} t_a` on a genus-2
once-punctured fiber. It has never been used computationally in this
repository. Whether it gives any purchase on concordance is unknown.

## 9. Housekeeping left undone

* The `s`-invariant sweep covers both `r = 0` pairs, `K_DG`, `K_B_0friend`,
  `K_2` and the Abe-Tagami knots. It does **not** cover the GST knot (48
  crossings) or the Hom-Park knot (88 crossings). Both are certified slice or
  algebraically slice, so `s = 0` is expected; computing it would be an audit,
  not a test, and both are large.
* The `s(GST)` audit is the cheapest remaining consistency check on a stored
  build.

---

## Standing cautions, carried forward

Every search here is coverage, never an obstruction. Component Jones equality
does not identify a knot. A polynomial coefficient distance is a sorting
heuristic and nothing else. An unfinished search supports no conclusion. A
positive endpoint needs oriented peripheral identification and a replayable
movie before it is anything at all.

And one correction that cost a published claim: `Link.simplify('global')`
**deletes split unknot components**, which inverts any test whose intended pass
is a split knot-plus-unknot pair. See `research/23` §8.
