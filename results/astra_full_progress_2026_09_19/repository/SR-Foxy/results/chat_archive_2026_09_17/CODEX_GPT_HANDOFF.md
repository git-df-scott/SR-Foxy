# Codex / GPT continuation handoff — consolidated SR-Foxy

## Immediate mission: finish publishing before new research

The user authorized preservation of all work from this chat on **existing main only**, with no new branch and no missed recovered attachment. This bundle has not yet been pushed at creation. Complete that specific publication task first, verify it, and report the actual result. Do not substitute a new experiment for an unfinished backup.

Repository: https://github.com/git-df-scott/SR-Foxy
Last verified main: `5448376b6ef3b2d5551836bd1479200588cd24be`.
PR #9 is merged at that commit; its preserved parents include Astra `fd15281e...` and Opus `27136b2...`. The former Claude branch need not be merged again.

The wrapper contains `publish_main.py`, `repository_payload/`, a manifest verifier and outer checksums. Read the publisher before using it. In an existing clean checkout already on main:

```sh
python3 /path/to/extracted/SR_Foxy_chat_consolidation_2026_09_17/publish_main.py /path/to/SR-Foxy --push
```

The script checks the archive, repository identity and branch, fast-forwards only, adds a fresh archive directory, creates a local commit and makes a non-force push only to refs/heads/main. It verifies every manifested file from fetched remote main. If anything fails, report the failure and actual local/remote state. No hidden recovery via resets, stashes, force, branch creation or permission changes. Use existing authentication; no credential appears in this bundle, and do not recover pasted tokens from old conversation messages.

The payload target is `results/chat_archive_2026_09_17/`. Its original ZIPs/patches are historical artifacts: **do not apply their old patches on top of current main**. The payload is itself additions-only and preserves all original versions without changing scientific files.

## Scope of archival assurance

All 24 files named in SOURCE_INVENTORY.json were physically present and copied byte-for-byte; all 207 non-directory entries of the 10 ZIPs were extracted and verified. The manifest checks these recovered files, not inaccessible files from past containers or the user's Mac. CONVERSATION_LEDGER.md is a scientific/operational summary, not a verbatim export. State this limitation honestly instead of promising universal completeness.

The current runtime lacked a write action and direct network DNS. That is not a claim about your runtime. Discover and test your authorized tools once; do not repeatedly claim an unattempted action succeeded.

## Research acceptance criterion

CE means an exactly identified knot in S3 with BOTH (a) a smooth properly embedded disk in STANDARD B4, and (b) a global proof that no ribbon disk exists. NO CE has been established. A disk in an unknown homotopy ball, equality of group words, a stabilization, matching surgery boundaries, numerical identification, passing invariants or bounded ribbon-search failure is insufficient.

D01 = K0 # (-K1), Kn=A_n(6_3), has the intended Abe-Tagami/Miyazaki nonribbon implication subject to exact knot and theorem hypotheses. Its missing ingredient is a smooth concordance in standard S3 x I, or the equivalent standard-B4 disk. KDG=18nh00000601 uses Trevor Oliveira-Smith's standardness/sliceness preprint; its missing ingredient is global nonribbonness. Do not swap those missing proofs.

## Most advanced concrete construction

Read the current versions of:
- scripts/build_marked_product_scaffold.py and the marked scaffold data;
- research/12, research/14, research/15, research/20;
- results/astra_2026_09_17_overnight/pass05_2357_cross_band_genus_gate/;
- pass06_0055_explicit_unlink_bands/, pass07_0123_relative_r3_r2/, pass08_0202_whisker_branch_gate/;
- results/astra_2026_09_17_afternoon/pass09_product_collar/;
- this archive's expanded/SR_Foxy_pass09_product_collar_2026_09_17/pass09_product_collar/ for the COMPLETE producer and logs.

The bands are `a40a423e_0_0` and `d0826c36_0_0`. The original twice-banded annuli give genus one, not genus zero. Pass07 corrects the first presumed relative-R blockage with a real RIII+RII sequence. Its bounded depth-four failure is not a global isotopy obstruction.

Pass08's SL(2,F5) results concern representations of the boundary knot group. Exactly which factor through the intended product-disk exterior was not fixed. The 24/12 split within 36 witness/witness realizations is not a probability or permission to choose a branch.

Pass09 specifies one candidate Dehn-region above/below collar map, with base sector (0,2), source region equation D_L=x^-1 D_R, lower-meridian candidate y=D_L^-1 D_R and explicit crossing/arc images. Under that map, actual band-axis words of lengths 70 and 48 are equal in the full source presentation. The independent saved-proof checker verifies the relator certificate. **The candidate map has NOT been geometrically matched to the intended product-disk boundary parametrization.** This is the immediate research gap, not a completed branch selection.

After archival completion, the single highest-value research action is to realize or falsify that exact collar map by an explicit product/twist-product parametrization carrying the original four circles AND both bands. Do not just check the old corresponding axes. If the geometric identification succeeds, group equality still leaves a framed nonseparating compression disk or another disjoint embedded annulus, Park standardness hypotheses, surgery coefficients and exact nonribbon boundary identification to prove. If it fails, name the geometric mismatch and preserve the certificate's limited algebraic meaning.

## Do not repeat completed work

The KDG 3-/4-parallel quotients 6601/106081, nullities 2/3, pass. D01 2-/3-parallel quotients -47/-27911, nullities 1/2, both have direct completed evaluations in the later centered-proof checkpoint. K0 and K1 2-/3-parallel values agree at -23/-1067, not a concordance proof. No automatic KDG p5, D01 p4, large band sweep, ordinary-s repeat, HKL(2,13) repeat or recorded Floer repeat.

The corrected all-degree transfer proof uses L_n((r+1)^n), not the false L_n(r^n). Read the current corrected file only if a concrete new objection makes it necessary; the old draft is preserved as history. Its scope is two Eisermann numerical tests on ribbon-pattern satellites of smooth slice companions, not all quantum obstructions. It remains internally audited, not externally reviewed.

## Opus material now in main

The merge preserves research/33 and /34, results/opus_2026_09_17/, the trace-cap gate and later Agol-Ren reframing. Preserve reported/verified/unverified distinctions. The archive is not an endorsement of every PR sentence.

The old slope/isometry audit has unresolved marking points: normalize opposite slope signs; record actual cusp covering maps and orientation; do not infer deck pairing from equal numeric coordinates. Equal compatible full isoSigs prove triangulation isomorphism, while unequal ones are inconclusive. Old unpinned slopes are not rescued by that logical correction. Finite coordinate boxes and volume filters do not turn misses into global exclusions. An arbitrary positive boundary filling is not the actual branched trace.

The proposed actual branched trace plus plumbing negative-definite strategy was rejected by the recorded degree-two pullback 2H subspace. Do not rerun it as a new opportunity. D01 slice would give a rational homology cobordism Y0 to Y1, not a rational homology ball for Y1. Any alternative Donaldson or Floer application requires complete caps, orientation, rank, theorem hypotheses and actual additional inputs; a linking matrix alone is not a general Floer calculation.

The newest merged Agol-Ren source/minimality discussion was not independently rechecked in the archive turn. In particular do not promote its flagged unverified divisibility step or a reformulation of an open relation to a new CE proof.

## Operational rules

No new branch, force push, reset, deletion, overwritten research file, interference with another worker, external paid API, new infrastructure or secret in files/logs. Prefer a fresh timestamped directory for new results. Do not modify the user's Mac unless actually connected and expressly authorized. Previous runtime paths are historical, not evidence of present access.

Historical usage instructions allowed a TOTAL 5 percentage points that morning and a 3-point exceptional-certificate reserve, with further afternoon work subject to authorization. Those are not fresh per-session grants. No live meter was available. The present request authorizes finishing the archive; do not start new automated research or claim continuous computation. No research invariants need rerunning to publish the archive.

## Final response format

State: publication completed or not; verified main commit; recovered files and ZIP-member counts; handoff path; limitations (not verbatim chat / no unseen-file guarantee); CE status; and only one next research action. Link the verified manifest/report, not an invented sandbox or remote path. Never describe an attempted push as completed.
