# SR-Foxy counterexample research: next session

Prepared at Scott's explicit request on 20 September 2026. No counterexample has been established. Be a skeptical collaborator; preserve exact inputs and failures. A successful counterexample requires a smooth slice disk in standard B4 and a global nonribbonness proof for the same precisely identified knot.

## Budget and authorization

Latest user asks for a handoff to a new session after completing the D test. This is NOT a new percentage allowance. Most recent displayed weekly usage is 26%, reset 1790432260/1790432261. The last explicit allowance was three additional points from 24%, absolute ceiling 27%, with a buffered research stop at 26%. The subsequent specific D test was authorized and completed while usage still displayed 26%. Prepare to continue, but do not silently treat the new session as a fresh budget or launch another research campaign. No reminders, recurring check-ins, or long remote jobs. Automation `slice-ribbon-next-5-session-at-4-pm` and GitHub run 35455048082 remain paused.

## Location and read order

Actual research checkout: `/Users/scottg/Documents/ChatGPT/SR Foxy/work/research-2026-09-16` (the saved project root is its parent). Important results are uncommitted and may not be copied into a new worktree. Read these original absolute paths; do not assume a fresh checkout contains them.

1. `results/astra_D_test_2026_09_20/RESULT.md` and `CERTIFICATE.json`: latest decisive result.
2. `results/astra_additional_3pct_2026_09_20/SMALL_DIFFERENCE_PROOF.md`: three other exclusions. Its HANDOFF's surviving-D status is now superseded.
3. `results/astra_seven_hour_2026_09_20/CHECKPOINT_03_FINAL.md`, `SAME_SIGN_CABLE_FILTER.md`, and `HANDOFF.md`: earlier campaign outputs.
4. `results/astra_gst_five_hour_2026_09_19/HANDOFF.md` and `results/astra_2026_09_19_counterexample_plan/PLAN.md`: GST source and reconstruction issues; older time/budget instructions are superseded.

Consult repository AGENTS instructions. Preserve all concurrent modifications; do not reset, merge or overwrite them. No push was made by the latest test.

## Decisive result: D is excluded

D=K9n4#(-K14n282), minus the concordance inverse. The earlier unmarked twisted-polynomial matches were real but irrelevant to sliceness because they do not respect the linking form.

In a common marked Wirtinger/Fox/Dehn/Goeritz construction, the dual linking coefficients are 6 and 3 modulo 7. Isotropic character lines for D require b=±3a. The polynomial matches instead have b=±2a. For a=1,b=±3, prime-13 reduction gives `(t-1)^2` and `t^2+3t+1`. The latter has nonsquare discriminant 5, and its roots in F169 are fixed under conjugate reciprocity. Odd multiplicity gives a non-norm for a character on EACH possible metabolizer. Exact cyclotomic coefficients are integral and monic, so good reduction provides the characteristic-zero obstruction. This excludes locally flat sliceness and therefore smooth sliceness, subject to independent review of the reproducible implementation and theorem conventions.

Controls: exact marked polynomials reproduce earlier unmarked values; all base-face choices and both checkerboards give the same pairing; mirror and crossing-reordering controls pass, including an explicit changed character scale for the second mirror. Published sources are recorded with precise theorem/section references. No disk search for D unless a concrete error in this argument is found.

Three other small genus-two prime-determinant differences were previously excluded by all-character non-norm witnesses: K7a2#(-K10n4), K8a5#(-K12n13), K11n91#(-K13n16). The trefoil cable (-9,-3) candidate and the earlier same-sign family were also excluded by previous Casson–Gordon deductions. Do not keep recommending them.

## Remaining directions, once funded

1. Apply the marked Goeritz refinement to further distinct fibered knot pairs with irreducible Alexander polynomial, filtering cheap concordance obstructions first. Unlike the old screen, restrict to actual metabolizers BEFORE interpreting polynomial matches as survivors. The full saved census is `results/opus_2026_09_18_2100_census_evidence/raw/miyazaki_pair_sweep.json.gz`; its `rows` array has 16,970 records, but its `pairs` array is truncated to 2,000 and is not exhaustive. Do not expand blindly: prioritize small prime determinant, short presentations and already matched Floer invariants. Generalize and verify q rather than reusing hardcoded 7.
2. The 10_17 cable lead has only inconclusive finite-field screens. Earlier tests cover 212 scalar-character orbits for specified cyclic covers; do not repeat them. Exact higher-cover character structure and additional sliceness obstructions are more valuable than extending the same random screen. Check source hypotheses; existing cable obstruction theorems have exceptions relevant to 10_17.
3. GST still has two distinct gaps: a source-certified knot construction/peripheral marking and a global knot nonribbon obstruction. Link obstructions, group identities and invariant matching do not fill those gaps. The diagram bridge remained unfinished; use the earlier detailed handoffs instead of improvising an identification.

Most valuable methodological improvement from this session: character-compatible linking forms can eliminate apparent exact twisted-polynomial survivors. This is a reusable filter, not itself a source of slice disks.

## Runtime and reproducibility

Python `/tmp/sr-foxy-20260919-leads-venv/bin/python`; SnapPy 3.3.2, Spherogram 2.4.1, Regina 7.4, Sympy, python-flint 0.9.0. No Sage or NumPy in this environment. The marked test scripts depend on `results/astra_seven_hour_2026_09_20/metabelian_probe.py` and the exact function in `results/astra_additional_3pct_2026_09_20/EXACT_FUNCTION.py`. No calculations are left running.

No subagents were used or authorized. Do not send messages to outside collaborators. State clearly what is a published theorem, our computation, an unverified deduction, or an open proof obligation. Scott wants progress and direct answers, not claims that persistence alone can guarantee a counterexample.
