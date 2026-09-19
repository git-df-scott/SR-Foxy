# SR-Foxy: September 18 night-session handoff

## Mission and repository discipline

Work toward a knot smoothly slice in the **standard** B4 and globally nonribbon. No counterexample is presently certified. Make the missing geometric implication the main work, not another list of invariant coincidences.

**DO NOT CREATE A BRANCH. DO NOT CREATE A BRANCH.** Use the existing checkout and branch. On Scott's Mac the research checkout is `/Users/scottg/Documents/ChatGPT/SR Foxy/work/research-2026-09-16`. Inspect status, branch, HEAD, recent commits, untracked files and diffs before writing. Preserve uncommitted work. Do not reset, clean, force-push, switch branches or automatically merge.

Astra's preparation session was on Linux and did not access that Mac or alter the repository. It observed main at `debd272ad3dc4e61bff643cfdcc544aa2e3912d1` and existing branch `claude/compassionate-carson-b6lxu8` at `5a4b38abffc43c6bb6cc4f15da5316c5424a4428`. These are pinned observations, not instructions to move HEAD. Reinspect actual state. The old baseline `b7ae7270ea6abc6976c0ec598067e2cac3602887` is not the latest state observed.

## Before discarding the old session: recover evidence

The census scripts write to `/tmp/claude-0/`, not automatically to tracked results. Preserve `miyazaki_pair_sweep.json`, `miyazaki_pair_sweep.jsonl`, `zero_surgery_volumes.jsonl`, `zero_surgery_pairs.json`, `zero_surgery_confirm.json`, and the actual logs/checkpoints present. Do not invent a missing final file. Record whether the process finished, failed, remains running or is inaccessible. A committed script is not a saved computation.

Write a separate result directory on the existing branch; hash inputs and archive full raw data. Inspect large JSON/JSONL programmatically. Reconcile input totals, valid outputs, exceptions, timeouts, skipped/nongeometric cases, pending cases and stored-versus-reported pair counts. Do not rerun the 59,937-knot sweep merely because the final report is incomplete.

## Short preliminary repair: no false negatives masquerading as proofs

Read `AUDIT.md` and run `python3 audit_regressions.py` from the accompanying preparation package. The 16 tests use synthetic numerical inputs and a fake isometry engine, plus a reproduction of the existing finite-group certificate. They are NOT a target census rerun or an integration-tested replacement script.

At commit 5a4b38a, `zero_surgery_confirm.py` returns immediately on the first Boolean from `is_isometric_to`. SnapPy documents True as rigorous but False as potentially numerical. A low-precision False therefore must not become a certified exclusion or prevent escalation. RuntimeError is UNKNOWN, not a negative.

Both zero-surgery scripts group volumes by `round(volume/1e-6)`. This drops close pairs across bin boundaries; the preparation package gives an explicit example. Neighbor-bin or sorted-window comparison repairs that particular heuristic hole, not the absence of rigorous error bounds. Without certified separation, missing-volume and nonhyperbolic/undecided cases remain outside coverage, not excluded.

Rounded numerical complex length spectra may prioritize comparisons, not certify DISTINCT. The current conversion to Python complex and six-place rounding is not interval verification. Preserve multiplicities and the entire compared spectrum if used. A proof from spectra needs certified lengths and sufficient completeness to exclude a matching multiset. Agreement is not an isometry proof.

Use durable per-pair JSONL with a verdict, basis, precision, seeds, exact inputs, errors and witness. Do not truncate the scientific record to `all[:4000]`, `unknown[:300]` or three entries from an eight-entry fingerprint. Add HFK output validity checks and an exception ledger; the initial sweep silently skips HFK exceptions. Distinguish certification from search heuristics.

Controls must include a known same-zero-surgery pair after verifying its diagrams, a certified distinct pair, and a nonhyperbolic/undecided case, not just self-isometry. Save positive isometry witnesses and orientation information when available. An isometry of closed 0-surgeries is not a knot identification or a concordance.

Cap this repair and recovered-hit triage at a small minority of the session. Preserve genuine positive returns; do not relabel them as unreliable merely because the negative tests were defective. Do not expand the census tonight.

## Main work: boundary-compatible mixed-annulus construction for D01

The main goal remains D01 = K0 # (-K1), with - the concordance inverse, and an actual disk in standard B4. First read the seven requested checkpoint files, the old `claude_response.json` alongside its audit, `data/knots/AbeTagami_CONSTRUCTION.md`, research/12, /14, /15, /33 and /34, and the current collar/boundary and dual-path reports. Track which sections and datasets you actually inspect.

Verify the theorem/diagram chain. Abe–Tagami Corollary 4.3 applies to distinct fibered knots with irreducible Alexander polynomial; Section 2 and Figures 1, 4–5 supply the intended pair. Audit the oriented marked surgery link, cusp order, annulus versus Seifert framings, filling slopes and boundary identifications. The construction card's numerical consistency checks alone are not an independent correspondence proof with the paper.

Do **not** restart either of these old constructions:

* An annulus joining the original two marked axes in the standard product-disk exterior. The displayed SL(2,F5) representation has axis traces 1 and 4, excluding conjugacy even after inversion. Astra reproduced this algebra independently, but did not re-extract the words from the PD.
* Removing a disjoint punctured S2 x S2 summand while keeping the fixed trace annulus. Research/14's cyclic-exterior argument excludes this particular relative destabilization, not all concordances between the endpoints. A changed surface/complement is outside that conclusion.

The latest main report keeps the first mixed band and the second band's endpoints fixed. It records a completed 88-case short box and 2,839/3,288 expanded assignments, with 449 untested. All 435 expanded trace survivors have the wrong surgery Alexander polynomial. This is a bounded report, not a universal identity; Astra did not re-audit its full generated dataset during preparation.

**Selected next experiment:** redesign the pair of mixed bands jointly, including attachment positions, instead of extending only the second path. Derive their routing from the annulus presentation and intended boundary cancellation. Before enumerating, write down the proposed local cancellation and explain why it changes a feature held fixed in the previous box. Use a small explicit finite box, deterministic order and fixed seeds; record all band attachments, paths, over/under choices and twists. Do not use an unverified identification of the product-disk group to discard states.

Apply gates in this order:

1. Check diagram planarity, oriented components, marked-axis words and necessary conjugacy conditions under a geometrically justified disk-exterior map. Unequal exact traces can reject; equal traces cannot certify an annulus. A failed test under one tentative collar map is not a universal obstruction.
2. Check framing, the full auxiliary link and boundary surgery. Compute the exact resulting boundary polynomial as a cheap necessary check against D01, then retain actual boundary-identification data. Matching the polynomial is not knot identification. A determinant-one linking matrix does not certify S3.
3. For a surviving geometric design, stop enumeration and construct the embedded modifying annulus, disjoint from the chosen slice disk. Apply Park's full standard-annulus hypotheses, not only existence of an annulus. Definition 2.1, Section 3's l-standard definition and Theorem 3.3 separate an exotic-ball conclusion from standard-B4 sliceness. Alternatively give explicit standardizing Kirby moves with the boundary knot tracked.
4. Identify the resulting knot with D01, or define a genuinely different knot and prove an applicable global nonribbon theorem for it. Do not transfer D01's theorem to an unidentified output.

For any direct movie, track orientation, connectedness, genus and the ambient manifold. A disk from the empty link needs b-s+d=1. A concordance annulus needs relative b-s+d=0. Counts do not certify realizability, split deaths, or an embedded surface. A component that is individually an unknot cannot be capped just because its knot type is trivial.

**Stop rule:** if the redesigned finite box supplies no boundary-compatible design, archive the exact scope and failed construction. Do not expand it automatically and do not present additional trace survivors as progress toward a disk.

## One constructive contingency: targeted ribbon stabilization

If the mixed-annulus design reaches a concrete impasse, make one reasoned pivot to a ribbon stabilizer J derived from the failed local cancellation or a verified saved interface. The target is a pair of certificates: J ribbon and D01#J ribbon. Do not hunt a ribbon disk directly for D01 while retaining its nonribbon premise.

The implication is exact: [J]=0=[D01#J] in smooth concordance, hence [D01]=0. This uses standard ribbon disks and does not rely on a homotopy ball. Dunfield–Gong Section 2.6 also states the converse existence result, citing Teichner; it gives no useful finite bound on J or the bands.

Read the earlier stabilization attempts before choosing the partner. Do not revive square-knot/other summand choices already ruled out by an applicable Miyazaki pairing argument. Conversely, do not resurrect the retracted blanket ban on prime fibered ribbon partners. Record each prime summand's actual hypothesis status.

Prioritize a partner placement whose bands change the K0/K1 interface. If the movie merely replaces one known ribbon partner by another while leaving D01 untouched, preserve it but do not count it as a new solution mechanism. Search only the new specified family with a resumable checkpoint. J149 is not a fresh proposal: read the later priority warning and distinguish an unproved remark from a theorem.

## KDG comparison: reserve, not a second broad search

Oliveira-Smith's preprint identifies 18nh00000601 and gives standard-B4 sliceness (Theorem 1.1, Corollary 1.1.1); handle-ribbonness in Theorem 1.2 is not ribbonness. Match the stored PD to the stated knot before use.

Only two genuinely different nonribbon routes merit comparison here. First, a proved ribbon satellite pattern P together with an exact failure of an Eisermann necessary condition on P(KDG). Prove P(U) ribbon and track zero framing; the previously passing 3-parallel is not a fresh test. Establish a reason the chosen test is not already forced on all slice inputs before a substantial computation. Non-concordance-invariance alone is insufficient. Eisermann's Questions 7.1/7.8 are questions in that paper, not proofs of either usefulness or vacuity, nor a claim about their current resolution.

Second, a global obstruction to an unlink derivative. Miller–Zupan Proposition 1.1 quantifies over a derivative on some Seifert surface, with no minimal-genus restriction. A finite list on the known fiber cannot prove nonribbonness without a theorem controlling all surfaces/stabilizations. Do not label handle-ribbonness or failure to simplify one R-link a global obstruction.

Neither presently supplies a more concrete finite certificate target than the selected D01 construction. Keep them in reserve unless an actual missing theorem is proved.

## Execution and final report

Use at most one substantial computation at a time. Keep the memory footprint appropriate for the 8 GB Mac, use subprocess limits and explicit checkpoints, and retain interrupted jobs as UNKNOWN. Small unit checks do not replace independent target validation.

If a possible CE appears, stop expanding searches. Independently attack the knot identity, disk in standard B4 and global nonribbon argument, including every dependency and every movie transition.

Finish with: CE yes/no; strongest genuinely new verified result, separated from reproduction and heuristics; exact remaining implication; artifact paths and commit/push status; one next action. Do not promise that an unattended process will survive a session reset. No new branch.
