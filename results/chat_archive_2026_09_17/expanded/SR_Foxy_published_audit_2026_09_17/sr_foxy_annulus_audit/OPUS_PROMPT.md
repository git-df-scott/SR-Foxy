# Opus continuation: integrate Astra's audit and construct the missing geometry

Continue your CURRENT SR-Foxy session. This is an update from Astra, not an instruction to restart the campaign or abandon a substantive construction already underway. Scott clarified that the earlier long research prompt was your assignment. Astra is the independent auditor/orchestrator; do not duplicate completed searches or replace construction work with another broad audit.

Repository: https://github.com/git-df-scott/SR-Foxy
Mac research checkout: `/Users/scottg/Documents/ChatGPT/SR Foxy/work/research-2026-09-16`
Scientific inputs are pinned to `b7ae7270ea6abc6976c0ec598067e2cac3602887`. Astra's subsequent additions are on existing `main`, entirely under `results/astra_2026_09_17_annulus_gate/`.

DO NOT CREATE A BRANCH. Inspect `git status`, your current branch, and remote state first. Preserve all work, including uncommitted changes and running jobs. Fetching origin is fine; do not blindly pull, switch branches, reset, stash, or overwrite another worker's files. Read new files with `git show origin/main:<path>` when needed, or extract only the new directory into a fresh temporary location. Commit only your own explicit paths, not `git add .`. Never print or commit credentials.

## Goal and unchanged status

NO COUNTEREXAMPLE has been found. Success requires an identified knot in S3, a smooth properly embedded disk in the STANDARD B4, and a global proof of no ribbon disk for that same knot.

D01 = K0 # (-K1), with - the concordance inverse, is the intended Abe-Tagami difference based on 6_3. Its nonribbon implication is available from Abe-Tagami/Miyazaki, conditional on exact knot identification and theorem hypotheses. A smooth concordance K0 -> K1 in STANDARD S3 x I is still missing. KDG = 18nh00000601 has the standard-B4 slice result from Trevor Oliveira-Smith's preprint; global nonribbonness is missing. Handle-ribbon is not ribbon.

Do not repeat ordinary s of D01/D02/D12, the completed ordinary/involutive Floer comparisons without addressing their existing dependencies, HKL(2,13) advanced/direct, or the KDG three-parallel Jones test. The latter gave 6601, normalized nullity 2, and 6601-25^3 = -282*32: a pass, not a ribbon proof or a universal satellite no-go theorem. The 138,565 generated moves and 307 saved deeper diagrams are search history and intermediate states, not counterexamples.

## Read this update, then continue the construction

Inside `results/astra_2026_09_17_annulus_gate/`, read README.md, REPORT.md, inputs.json, verification_results.json, FRAMING_ADDENDUM.md, and framing_results.json. The two verifiers are standard-library-only. Select fresh output paths:

```
python3 verify_annulus_gate.py --output opus_annulus_recheck.json
python3 verify_framing_gate.py --output opus_framing_recheck.json
```

Read relevant existing work alongside it: research/12_coupled_movie_audit.md, research/14_marked_annulus_audit.md, research/15_infection_target_compatibility.md, research/20_next_construction_plan.md, ERRATA_2026-09-16.md, and the earlier Claude review AUDIT rather than treating raw model output as verified. Reuse material you have already checked; do not restart a full repository reading exercise.

## Exact results to carry forward, with limits

Astra checked the recorded presentation

```
G = <a,b | aabbbaBAABabbbaabABBBAb>
u = BabA
v = BBABabbbaBABabbbaBAA
mu = bba;  a -> -3, b -> 2.
```

G has an explicit F4 semidirect Z presentation, with automorphism and inverse in REPORT.md. Individually conjugate normalized axis representatives are

```
U = x0^-1 x1
V = x1^-1 x2 x3^-1 x0^-1 x1 x2^-1 x1 x3.
```

Their common nonzero fiber abelianization is (-1,1,0,0). The monodromy characteristic polynomial is t^4-3t^3+5t^2-3t+1, with no unit-circle roots: dividing by t^2 gives (z-3/2)^2+3/4 for z=t+t^-1. Thus any conjugacy has meridian exponent zero; fiber free-conjugacy then fails because the cyclically reduced lengths are 2 and 8. Inverse conjugacy fails as well.

A class-two quotient of the FIBER subgroup also detects the difference: [x2,x3] coordinates 0 and -1, invariant under fiber conjugation here. This is not the ordinary nilpotent quotient of the entire knot group. Conversely, the original loops ARE conjugate in G/G'': Fox(v)=t^-2 Fox(u). Therefore Alexander-level agreement is not enough to validate this annulus. Do not extend that statement to all metabelian invariants or HKL tests.

The geometric deduction is a marked retraction obstruction. Interior local knotting of the product disk with any smooth 2-knot of exterior group H gives G *_<mu> H, which retracts to G via h -> mu^(epsilon_H(h)). Hence fixed original axes still cannot cobound a disjoint annulus. This excludes arbitrary interior LOCAL knotting of that disk, and corresponding separate-factor changes when the marked retraction is established. It does NOT exclude genuinely mixed stabilization disks, nonlocal disk changes, new axes, or smooth concordance of the endpoints.

The checker passed 44 named checks and 4,681 synthetic word arithmetic controls, and was rerun normally and with -O before publication. These are algebra checks, not new knot-search coverage. The input knot-to-group/peripheral identification was NOT independently regenerated from the PD. Verify that upstream dependency when a decisive geometric claim depends on it.

## Additional conditional framing trap

The stored five-component scaffold has NO specified surgery framings. Do not silently assign them. Astra separately tested this explicit shortcut: start with the upper n=1 trace matrix [[2,1],[1,0]] and its negative mirrored lower copy; take inherited framed handle classes e1+e4 and e2+e3; keep only those two surgery components without compensating moves. Their matrix is diag(2,-2), so the surgery has H1 = Z/2 + Z/2 and is NOT S3. All 16 sign assignments give determinant -4 or -8. Any retained pair in the same mod-2 classes has determinant divisible by four.

This is NOT a rejection of an unspecified mixed-axis proposal. Changed coefficients, retained additional handles, and separately justified cancellations require their own calculation. In particular (+1,-1) coefficients at linking zero pass this homology gate, but that is a DIFFERENT surgery and proves neither the intended boundary knot nor standard B4. Never promote det = +/-1 to S3 or to standardness.

## Immediate research action

First state your strongest concrete claim so far, with exact artifact paths. If it is a new disk, annulus, or handle construction, prioritize adversarial verification of that object over this suggested next experiment.

Otherwise pursue ONE explicit changed-axis or genuinely nonlocal construction that escapes the marked retraction, not another large unstructured band sweep. Start from the actual marked scaffold or annulus presentation. Supply actual band paths/whiskers, the complete oriented surgery link, and explicit coefficients. Compute its boundary knot early. The words uv and vu are already known to be conjugate; merely writing them again is not progress. Their free homotopy does not supply an embedded annulus, a standard annulus, an S3 surgery boundary, or the desired knot.

Use the following order: identify the actual marked and framed boundary construction; reject it cheaply if its homology or knot type is wrong; then build the embedded annulus/movie and prove standard ambient geometry; finally reapply the nonribbon theorem to the exact resulting knot. For Park's method check the actual standard-annulus hypotheses in the primary paper, distinguishing its weaker exotic-slice conclusion. Do not demand both the standardizing isotopy and the annulus be disjoint from the disk if the theorem only demands the latter: check the precise statement.

For a movie, verify every move, orientation, framing, connectedness, genus and boundary. Births-saddles+deaths=1 for a connected disk from the empty link, and relative Euler characteristic 0 for a concordance annulus, are necessary but not sufficient. A disk in an unidentified homotopy ball is insufficient. Common zero-surgery alone is insufficient.

The stabilization route remains valid: ribbon certificates for BOTH J and D01#J imply D01 is slice. A genuinely mixed disk is not excluded by the local-knotting lemma. Do not look for a ribbon disk directly for D01 while retaining the nonribbon theorem without resolving that contradiction.

If this exact construction fails, preserve its diagram and identify the precise failed gate; pivot on that failure rather than rebranding it as a universal exclusion. Do not spend the rest of the session auditing already verified algebra. The requested output is a constructed geometric object or a precisely delimited failed construction that determines a genuinely different next move.

One substantial computation at a time on the 8 GB Mac. Save inputs, hashes, seeds, bounds and intermediate certificates; use positive/negative controls; keep timeouts/errors/invalid invariants UNKNOWN. Respect the user's current usage cap: this update does not authorize an unlimited run. Do not interrupt another worker's jobs.

End with: counterexample yes/no; strongest new verified mathematical result; exact unresolved step; reproducible paths; and ONE most valuable next action. Stop broad exploration and attack every dependency if a possible counterexample appears. Neither more surviving states nor another correct exclusion supplies the missing slice disk.
