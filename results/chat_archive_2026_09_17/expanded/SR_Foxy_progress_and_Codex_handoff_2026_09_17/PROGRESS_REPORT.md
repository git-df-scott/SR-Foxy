# SR-Foxy progress report — 17 September 2026, morning

## Bottom line

**No counterexample, no new smooth concordance K0 -> K1, and no global nonribbon proof for KDG.** The campaign has two principal targets with opposite missing certificates. Construction-level exclusions, matching invariants, finite-group survivors and failed searches must not be promoted into either missing certificate.

This handoff checks the current remote heads and selected checkpoint text; it does not repeat computations or constitute an exhaustive repository or independent theorem audit.

## Repository state checked for this handoff

- `main`: `f7ba2516304c0553a3180570abb6e257f4a68094`.
- Existing Opus branch: `claude/compassionate-carson-b6lxu8` at `6c02acb15104055ca2fcf58a5fff319e5ce40b13`.
- Its preceding research commit: `4516e3d6dfd26fb9284aae9d931087c2273bdf32`.

These heads were separately read. Do not assume that reading main includes the latest Opus work; inspect ancestry and differences. No merge, repository edit, new branch, compute job or new agent session was started for this handoff. Local checkout cleanliness and Opus process liveness were not independently checked here.

## 1. Candidate ledger

### D01: intended nonribbon knot, sliceness unknown

`D01 = K0 # (-K1)`, where `-K` is the concordance inverse, `K0=6_3`, and `K1` is the repository's fixed Abe–Tagami annulus twist. The intended summands are distinct genus-two fibered knots with irreducible Alexander polynomial

`Delta(t)=t^4-3t^3+5t^2-3t+1`.

Abe–Tagami/Miyazaki supplies the intended nonribbon implication subject to exact diagram identification and theorem hypotheses. The missing certificate is a smooth disk in STANDARD B4, equivalently a smooth concordance between the summands in STANDARD S3 x I. Common zero-surgery is not that certificate.

A valid stabilization construction would give ribbon disks for BOTH J and D01#J; then D01 is slice by cancellation in smooth concordance. Neither needed pair of disks has been found.

### KDG: intended standard-B4 slice knot, ribbonness unknown

`KDG = 18nh00000601`. The campaign uses Trevor Oliveira-Smith's preprint, *A Dunfield–Gong 4-Sphere is Standard*, for its standard-B4 sliceness. It is handle-ribbon; that is not a ribbon disk. The missing result is a GLOBAL obstruction to ribbonness. Exact identification and the source's standardness argument remain final-certificate dependencies.

## 2. Completed search and reliability work

The earlier Astra batches generated 138,565 band moves with no certificate. These were bounded searches, with timeouts. The 307 distinct exact PD encodings in the prepared deeper-survivor queue are intermediate diagrams, not 307 counterexample candidates or necessarily 307 distinct links. Do not relaunch the queue merely because it exists.

Reliability work includes saved full move paths, input/code/runtime fingerprints, deterministic seeds, raw replay, unknown/error retention, exact integer determinant screening and validation of knot Floer output. Inconsistent HFK output was correctly retained as unknown. These repairs make results more trustworthy; they do not create a slice disk.

Ordinary s over Q and F2 vanishes on K0,K1,K2, so the differences' ordinary s values follow by additivity. D01 HKL(2,13) advanced/direct calculations returned null, which is inconclusive. Recorded full/involutive Floer conclusions have explicit input/lifting dependencies. Do not repeat these tests or interpret null as equality of twisted invariants.

## 3. Completed Jones work and proof correction

The stored exact cable results include:

| Object | Parallel multiplicity | Reduced Jones determinant | Normalized nullity |
|---|---:|---:|---:|
| KDG | 3 | 6601 | 2 |
| KDG | 4 | 106081 | 3 |
| D01 | 2 | -47 | 1 |
| D01 | 3 | -27911 | 2 |

All pass the tested mod-32 congruences. D01 p=2 and p=3 are now BOTH direct diagram evaluations (112 and 252 crossings), not only predictions. Earlier statements that its p=3 value was merely derived are superseded. K0 and K1 have matching recorded e2=-23 and e3=-1067; these few equalities do not prove concordance or equality of all quantum invariants.

A portable C++ frontier evaluator and Python PD cabler bypassed missing topology libraries. Exact characteristic-zero divisibility, small state-sum comparisons, diagram checks and separate connected-sum identities support the calculations; there is no independent full-polynomial computation of each large target.

A proposed all-degree transfer theorem would make THESE TWO Eisermann conditions automatic for ribbon-pattern satellites of smooth slice companions. Its displayed moment identity was wrong: `L_n(r^n)` must be replaced by `L_n((r+1)^n)`. The corrected proof is on main in pass04, with 2792 cleared-denominator checks through degree 20. It remains an internally audited research derivation, not an externally reviewed theorem. Do not re-audit it without a specific objection; do not infer it settles arbitrary slice links, all colored-Jones restrictions or every satellite obstruction.

Turaev-H and plain-parallel Suzuki limitations have already been documented. Do not spend another pass rediscovering those restrictions or automatically launch KDG p=5/D01 p=4.

## 4. Constructive geometry: actual advances and exact missing step

### Original axes

For the standard product disk of K0#(-K0), the original marked modifying circles are nonconjugate up to inversion in the recorded exterior group. Exact finite-group and free-by-cyclic certificates support this. Local knotting cannot repair those FIXED axes when the modified exterior retracts to the original group preserving the marked images. This does not exclude arbitrary disks, nonlocal changes or new axes.

Opus reports a fresh extraction over six triangulation seeds. It helps check the original PD-to-group computation; it does NOT identify the new crossed-axis lower-to-upper based gluing map, or prove the original marked PD is the paper's figure.

### Crossed axes

The exact saved bands are

`a40a423e_0_0` and `d0826c36_0_0`.

They are based on `data/knots/AbeTagami_marked_product_scaffold.json` and `scripts/build_marked_product_scaffold.py`. Prior passes constructed and replayed these bands. A relative Reidemeister-III followed by Reidemeister-II removes a previously claimed obstruction while keeping R fixed. That correction matters: a pictured strand passing through a projected bigon is not enough to reject the move without checking crossing heights.

The twice-banded pair of product annuli is a connected genus-one surface with two boundary components, NOT an annulus. An actual nonseparating compression disk with correct framing/disjointness, or a different embedded annulus, remains needed.

### Latest finite-group gate (pass08)

There are 49 SL(2,F5) colorings of the doubled boundary knot with the selected meridian image. Of these, 36 carry the original nonabelian witness data on both ends and pass the old corresponding-circle free-conjugacy controls. For the ACTUAL new axes, these split into six equal types: 24 colorings separate the axes, and 12 do not.

These are representations of the boundary-knot quotient; the crucial missing certificate is which representations factor through the actual product-disk exterior under its based lower-to-upper gluing map. One cannot select a convenient separating representation to kill the candidate, select a surviving representation to certify it, or interpret 24/36 as a success probability. Even a surviving finite quotient does not prove conjugacy in the full group or existence of an annulus.

**Best concrete next task: derive the based group map induced by the stored corresponding-endpoint product gluing, transport the actual band whiskers, and identify the extendable representations.** Only then return to compression/annulus geometry for this fixed candidate.

## 5. Latest Opus work: committed claims, not newly re-proved here

Opus's existing branch records the following:

- A claimed closure of the ordinary branched-cyclic-cover linking-form test for the family at odd primes below 60, with p=5 handled separately. This does not settle d-invariants or Casson–Gordon. An audit must check actual group structure and deck action, not infer elementary-abelian structure from the resultant/order alone.
- Theorem A-prime: the assumed one-fold annulus-twist trace has `Q_k=[[k+1,k],[k,k-1]]`, determinant -1, signature zero, even exactly for odd k. The branch distinguishes its claimed smooth k=1 argument from the general-k discussion. Unimodularity alone is not S3 recognition or smooth ambient standardness.
- A six-seed fresh original marked-group extraction, explicitly leaving the paper-to-PD identification unverified and its unsuccessful Alexander cross-check as not obtained.
- A new lifted-surgery description search. Opus reports a degree-two cover with five cusps before the carried filling, 34 tetrahedra and H1=Z^4, leaving four free lifted surgery cusps. It reports 320 of 65,536 sampled filling vectors recognized by Regina as L(13,5). Those counts and the precise filling conventions have not been independently reproduced in this handoff.

The alleged Sigma2(K1) slope vector `(-1,-1),(1,1),(-2,1),(2,-1)` was WITHDRAWN. It is not usable input. The correction is committed at 6c02acb. The replacement search was reported running by Opus; no current process or completed slope artifact was verified here. The K2 geometry attempt timed out and is not a mathematical result.

### Important correction to the correction

Regina documents that matching FULL isomorphism signatures, for the same dimension/type/encoding, imply combinatorially isomorphic triangulations. Exact matching signatures can therefore certify the unmarked manifold identification. DIFFERENT signatures cannot certify different manifolds. Randomized simplification can create false negatives, but does not by itself invalidate an actual exact positive match. Orientation, peripheral markings and saved source triangulations are separate obligations. The old slopes remain withdrawn until those data are recovered and checked; this observation does not reinstate them.

Do not accept the next slogan "if the branched trace is definite, Donaldson kills D01." First require the precise capped/glued smooth closed manifold, orientation, appropriate theorem hypotheses and the actual lattice contradiction. Likewise, a form alone is not a completed d-invariant computation; the relevant Spin-c structures, maps and applicable formula must be stated. These are audit gates, not results obtained here.

## 6. Budget, delegation and operational state

Scott reports 60% used / 40% remaining. The TOTAL allowance until noon on Thursday, September 17 is 5 percentage points, including ongoing conversation. An additional 3 points is exceptional reserve ONLY for a concrete promising certificate needing verification. No live usage meter is available here; do not claim an enforced percentage cap. Afternoon work is not yet authorized by the morning plan. Reset is user-reported for Saturday, September 19 around 7 a.m. Edmonton time; earlier discussion gave 7:33 a.m., so verify the actual display before treating either as exact.

Opus is to do heavy construction; Astra/Codex should audit only decisive evidence. There is an existing one-time morning audit scheduled around 11 a.m. Edmonton time. Do not add overlapping sessions or automated loops. No new cloud session or Mac control was launched in preparing this handoff. A computer-control connection was requested earlier, but successful access/delegation was not established.

## Source / checkpoint register

Remote heads and newest texts checked for this handoff:

- https://github.com/git-df-scott/SR-Foxy/tree/f7ba2516304c0553a3180570abb6e257f4a68094
- https://github.com/git-df-scott/SR-Foxy/commit/6c02acb15104055ca2fcf58a5fff319e5ce40b13
- https://github.com/git-df-scott/SR-Foxy/commit/4516e3d6dfd26fb9284aae9d931087c2273bdf32
- https://github.com/git-df-scott/SR-Foxy/blob/f7ba2516304c0553a3180570abb6e257f4a68094/results/astra_2026_09_17_overnight/pass08_0202_whisker_branch_gate/README.md
- https://github.com/git-df-scott/SR-Foxy/blob/f7ba2516304c0553a3180570abb6e257f4a68094/results/astra_2026_09_17_overnight/pass04_0515_centered_proof_and_D01/README.md
- Regina, Triangulation<3>, isoSig and fromIsoSig: https://regina-normal.github.io/engine-docs/classregina_1_1Triangulation_3_013_01_4.html

Other campaign checkpoints, retained from the completed handoff history; inspect before extending their conclusions:

- `results/astra_2026_09_16/summary.json`
- `results/astra_2026_09_16_followup/summary.json` and `claude_review_audit.json`
- `results/astra_2026_09_17_annulus_gate/`
- `results/astra_2026_09_17_satellite_plan/`
- `results/astra_2026_09_17_overnight/pass02_0410_four_parallel/`
- `results/astra_2026_09_17_overnight/pass05_2357_cross_band_genus_gate/`
- `results/astra_2026_09_17_overnight/pass07_0123_relative_r3_r2/`
- Geometry notes `research/12`, `research/14`, `research/15`, `research/20` (resolve complete filenames by repository listing).

Primary mathematical dependencies are indexed in those checkpoints: Abe–Tagami arXiv:1502.01102, Park arXiv:1512.00401, Eisermann arXiv:0802.2287, Oliveira-Smith arXiv:2603.23717, and Miller–Zupan arXiv:2005.11243. Recheck exact versions, statements and hypotheses when using them in a NEW implication; their mention here is not an additional source audit.
