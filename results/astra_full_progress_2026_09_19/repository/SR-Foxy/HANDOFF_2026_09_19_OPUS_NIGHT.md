# Handoff — 19 September 2026, Opus night session

**NO COUNTEREXAMPLE.** Smooth concordance `K_0 ~ K_1`: UNKNOWN. Slice-Ribbon CE: NO.

Everything below is machine-checked in a named script or labelled with its
status. Read the retractions in §4 before relying on anything from earlier in
this session.

---

## 1. Lanes closed

| lane | verdict | where |
|---|---|---|
| **DG 0-friend mining** (`HANDOFF` P2 bullet 1) | **closed by a theorem** — Fox-Milnor makes the wild-pair population disjoint from every plausibly-slice census, at any crossing number. 0 of 158,174 rows have irreducible `Delta`, with controls that fire positive | `research/50` |
| **Infection as a construction** | closed, and `HANDOFF` §4's stated reason ("genus grows") is **wrong** — it fails when `eta` lies on the fiber. The real obstruction is that a fibered satellite has nonzero winding number | `research/51` |
| **`HANDOFF` P4, involutive Floer on `D_{0,1}`** | not a live lane. `[K_0] = [K_1]` in the involutive local-equivalence **group** forces `D_{0,1}` involutively trivial. Now on an independent footing (§2) | `research/51`, `opus_..._0900` |
| **Surgery route to `d(Sigma_2(K_1))`** | closed over all 28 drillable geodesics, slopes to `|a|,|b| <= 20`, control passing | `research/52` |
| **GST knot `B_{3,1}`** | unreachable: **non-fibered**, so Miyazaki and Hom-Park both miss it, and Eisermann degenerates to `det = 1 mod 8` which it satisfies | `research/53` |

## 2. The one real advance

**Risk 1/2 of `opus_mixed_lift_review` is closed independently for `K_0`, `K_1`.**
The graded Euler characteristic of the **stored** HFK bigradings equals `Delta`
computed with no Floer code and no Seifert surface — from the braid word via
reduced Burau (9/9 controls) — at `[1,-3,5,-3,1]` for both, with zero HFK
symmetry violations, support exactly `[-g,g]`, rank 1 at the top grading.

A relative Alexander error, a mirror flip or a `U <-> V` swap each break that
equality; none is present. It had stayed open only because every prior
recomputation used the same engine family.
Not closed: risk 3, the lift to a homogeneous minimal full complex, the
involution itself. `K_2`/`K_3` unfinished (161-letter braid on 16 strands).

## 3. The best lead, and it is cheap

`research/53`. Determinants multiply, so Eisermann's predicted residues in the
GST family are:

| link | predicted mod 32 | status |
|---|---|---|
| `L_{1,1}` (18 cr) | **9** | **known ribbon** |
| `L_{2,1}` (40 cr) | **17** | **known ribbon** |
| `L_{3,1}` | **17** | UNKNOWN — a different residue is the first slice non-ribbon object of any kind |

**`L_{2,1}` is a known-answer control at the identical residue `L_{3,1}` is
tested against.** That dissolves the objection that has blocked this lane all
campaign — that a hand-traced `L_{3,1}` could produce a wrong residue looking
exactly like a counterexample. Build `L_{1,1}` (must give 9), then `L_{2,1}`
(must give 17), and only then trace `L_{3,1}`. The first two steps are
**risk-free**: the answers are known, so they can only expose a broken tool.
Neither has ever been attempted.

**Step 0 is started and stuck** (`opus_..._1100`): validating the pipeline on
SnapPy's 12,184 certified `RibbonLinks`. 8 evaluated, **8/8 pass** both
theorems, 0 violations — but only 2 have knotted components and 65 of 73 inputs
died on `UnboundLocalError: 'start'` inside spherogram's Seifert path under
`Link.sublink([i])`. **Fix: take component determinants without `sublink`** —
from the PD code, or `|Delta(-1)|` via the Burau route in `opus_..._0900`,
which passes 9/9 controls and never touches that code path.

## 4. Retractions from this session — read these

1. **"Historical Teichner runs may be unnormalized."** WRONG, withdrawn.
   `ribbon_concordant_links` normalizes its own copy before band generation.
2. **"Wild pairs are ~16x cheaper than `D_{0,1}`."** WRONG. Measured: 1 band at
   len 2 on 23 crossings exceeds 110 s. Crossing count is not the driver.
3. **"`deg Delta = 2*genus` re-confirms fiberedness."** WRONG. 59 explicit
   counterexamples in DG's own table.
4. **"0 of 122 drillings"** would have overstated coverage fourfold — only 28
   are drillable; the denominator is 26 tested.
5. A **Fox-calculus** Alexander tool failed 4/8 controls (ignored crossing
   signs). Kept marked failing, used for nothing, replaced by Burau.
6. A drilling sweep used **`L(13,5)` as control** — a lens space, not
   hyperbolic, 0 dual curves, so that run decided nothing.

## 5. Searches finished, all negative

**160 target-runs of GHMR's random walker, 0 hits.** All six passes report
`Finished all links` / `Succeeded 0 times`: 90 targets at the GHMR default
weights, plus 60 re-runs at twist-heavy and crossing-heavy weights, plus the ten
`D_{0,1} # J` at start-heavy weights. Ten of the targets are `D_{0,1} # J` for
**every** partner this campaign has used, including the three fibered ones
restored by E16-1 and the two container reclamation killed.

Per `research/53` and the ce_hunt README §13 this is **weak** evidence about
ribbonness and **none** about sliceness: GHMR's own programs failed on `L_{1,1}`
and `L_{2,1}`, both known ribbon.

Also landed: a **Levine-Tristram filter** proving **140 of 35,612** wild pairs
non-concordant (127 of them fall to the ordinary signature, which the existing
pair filter never applied), and the mirror-orientation correction — 959 pairs
survive only as `J # J'`, for which the old driver built the wrong knot.

## 6. Honest standing

The wall is one sentence: **every route that gets concordance for free loses
fiberedness, and every route that keeps fiberedness gets its disk only in a
homotopy 4-ball.** Searching does not move it. The two things that might are
the GST link calibration in §3 and the `d(Sigma_2(K_1))` gate — now needing a
negative-definite filling or bordered Floer, the surgery route being closed.
