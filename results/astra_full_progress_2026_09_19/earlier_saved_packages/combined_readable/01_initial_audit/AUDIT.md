# Preparation audit — 18 September 2026

No slice–ribbon counterexample was found. No new slice disk or concordance was constructed. The new verified results below concern the safety of the sweep's inference rules. A pre-existing geometric obstruction was also independently reproduced at the algebraic level.

## Scope

Repository main was inspected at debd272ad3dc4e61bff643cfdcc544aa2e3912d1 and the three Opus sweep scripts at 5a4b38abffc43c6bb6cc4f15da5316c5424a4428. See coverage.json for complete versus partial reads. The 59,937-knot raw HFK/surgery outputs and any live confirmation run in /tmp/claude-0 were not available in this Linux session. Accordingly, none of their tallies was independently recomputed, no actual census pair was proved misclassified, and no claim is made that the sweep finished.

The preparation session did not edit the Mac checkout, create a branch, commit or push. It produced this standalone package. The container lacked SnapPy, Spherogram and Regina; the executed checks use Python's standard library, not a simulated claim of running those libraries.

## A1. Low-precision False short-circuits the promised escalation

Source: scripts/zero_surgery_confirm.py at 5a4b38a, try_isometry.

The first Boolean from A.is_isometric_to(B) is returned immediately, including False. The higher-precision loop is reached only when prior attempts raise exceptions. Official SnapPy 3.3.2 documentation explicitly distinguishes rigorous True from potentially erroneous False caused by numerical canonical-triangulation errors. The label DISTINCT_BY_ISO therefore overstates this negative result.

A fake-engine regression returns False at ordinary precision and True at higher precision. The current control flow returns False after one call. A fail-closed semantic repair reaches the positive call; all-False and exception controls remain UNKNOWN. This is a control-flow counterexample, not a real manifold pair or a production implementation.

## A2. Rounded volume buckets can lose tolerance-neighbor pairs

Sources: scripts/zero_surgery_pair_search.py and scripts/zero_surgery_confirm.py, grouping by (Delta, round(volume/TOL)), TOL=1e-6.

Take a=1.000000499999 and b=1.000000500001. Their difference is exactly 2/10^12 as rationals, less than the tolerance by a factor of 500,000, but their bucket indices are 1000000 and 1000001. With identical Delta they are never compared.

Moreover, radius-10^-12 intervals around a and b share the exact point 1.0000005. Thus the observed numbers are consistent with one true volume. This proves a hole in a claimed lossless tolerance-neighbor filter. It does not prove an actual missed isometric pair in the census.

Comparing adjacent buckets or a sorted sliding window fixes this arithmetic boundary defect only. Certified exclusion by volume also needs verified hyperbolic structures and disjoint rigorous volume intervals. A failed or nonhyperbolic filling has no certified negative result from this filter.

## A3. Rounded spectra are heuristics, not certified distinctness

Source: scripts/zero_surgery_confirm.py, _clen and fingerprint.

The routine converts lengths to Python complex, rounds real length and absolute imaginary part to six decimals, sorts, and retains eight entries. A numerical mismatch becomes DISTINCT_BY_SPEC. Two approximate lengths 0.700000499999 and 0.700000500001 produce different rounded values although their radius-10^-12 intervals intersect. The example is below the script's 1.2 cutoff; no cutoff-edge complication is needed.

This exhibits why raw numerical inequality cannot certify inequality of exact spectra. Equal fingerprints also cannot certify isometry. Discarding sign of the imaginary part, multiplicities or most of the spectrum can weaken discrimination; sorting uncertain ties and the cutoff require care. Do not claim every such omission alone creates a false distinctness verdict. The decisive issue is that the claimed proof does not carry verified enclosures and completeness guarantees.

The routine additionally saves only the first three entries of each compared eight-entry fingerprint. The regression includes a mismatch at the sixth entry with identical saved prefixes. The displayed record can therefore omit its own numerical witness.

## A4. Completion and durability need separate auditing

The three scripts use /tmp/claude-0 outputs. The confirmer writes after its entire loop and truncates all to 4,000 and unknown to 300. The initial pair report truncates its unconfirmed list, and the HFK sweep retains only the first 2,000 summarized pairs, although saved rows could reconstruct the rest. These limits do not prove data were actually lost in the particular completed run; inspect the actual files and counts.

The HFK sweep silently skips exceptions and sets searched to the census size. It also lacks the existing campaign's invariant-output validation checks. Consequently the summary alone cannot establish valid classification of every census input. Missing invariant keys must not be treated as equal validated invariants.

Use complete per-input/per-pair JSONL, durable checkpoints, pending/error states and exact input identity. Preserve current raw records before changing the code. Do not classify an inaccessible temporary directory as an empty search.

## A5. Algebraic reproduction of the fixed-axis obstruction

Source: research/14_marked_annulus_audit.md at pinned main, Section 2.

For r=aabbbaBAABabbbaabABBBAb, u=BabA and v=BBABabbbaBABabbbaBAA, the matrices

a -> [[0,1],[4,2]], b -> [[0,2],[2,3]] over F5

satisfy r=I. The images of u and v have traces 1 and 4. Directly checking all 120 matrices in SL(2,F5) finds no conjugator from the image of u to the image of v or v^-1. A known conjugate passes and a tampered relator fails.

This independently reproduces the displayed arithmetic with new standard-library code. It is NOT a new theorem and does NOT independently establish the PD-to-marked-word identification. Conditional on that identification, it rules out an annulus joining these axes in this product-disk exterior. It says nothing about a changed disk, changed axes, or arbitrary concordances between K0 and K1.

## Consequence for tonight

Recover and repair the census briefly, but do not enlarge it. Its positives may nominate new pairs; none constructs a concordance. The main task should be a boundary-compatible redesign of the mixed-annulus construction, changing both bands rather than repeating the latest fixed-first-band box. Retain ribbon stabilization as one explicitly scoped constructive contingency.

The current main report's counts and polynomial results were read, not recomputed here. The 449 untested expanded assignments stay untested; finite repetitions do not establish a polynomial identity for all band routings.

## Reproduce

`python3 audit_regressions.py` prints the complete result without writing. To save a fresh result, use `python3 audit_regressions.py --output /a/new/path/results.json`. The script refuses to overwrite an existing output. The delivered results.json and run.log contain 16 passing checks, with their evidence and limitations. There is no continuing background computation.
