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

`8_9`, `8_20`, `9_27` must **not** be run: they are fibered, and adding a
fibered ribbon `J` leaves `K_0` and `-K_1` unpaired among the fibered prime
summands, so Miyazaki still gives non-ribbon and no certificate can exist.

After those, the non-fibered ribbon knots of at most 10 crossings are
exhausted. The lane runs out of tractable partners rather than failing.

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

## 4. The untried crossing that needs files outside this clone

`research/20` §4. An `r = 0` RBG pair has diffeomorphic 0-traces, so a ribbon
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

## 5. Astra's lemma still needs one citation

`research/19` §5. The step "generic Alexander rank is a link-concordance
invariant" is asserted, not cited, and is not multivariable Fox-Milnor. Every
rank-based exclusion is conditional until a primary source is in the ledger.

Lower priority than it looked: §8 of the same note shows the screen is
**exactly redundant** with research/17's existing filter on J25533 (set
equality, band for band), so nothing currently rests on it.

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

`research/20`. Every route-B non-ribbon certificate (Miyazaki fibered pairing,
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
is a split knot-plus-unknot pair. See `research/19` §8.
