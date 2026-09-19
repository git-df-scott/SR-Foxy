# SR-Foxy pass04: corrected transfer algebra, D01 gates, direct marked-PD certificate

**NO COUNTEREXAMPLE. No new smooth disk or concordance.**

This pass followed the user's request to continue working, within the existing
hourly overnight task. It did not create a new task or guarantee three hours
of uninterrupted live execution. Computations ran in the Linux container,
not on the user's Mac. No account usage meter was available.

## Strongest new verified work

A direct finite-group certificate now verifies the original fixed-axis
nonconjugacy starting from the 27-crossing marked PD, without depending on the
saved SnapPy group presentation or longitude words. All original crossing
relations hold after filling the two auxiliary meridians. The two axis images
have traces 1 and 4 modulo 5 (orders 6 and 3), so they cannot be conjugate in
either orientation. A separate checker replays the diagram and matrix data.
This independently verifies an EXISTING obstruction for that fixed diagram;
it is not a new obstruction to D01's sliceness. See `DIRECT_PD_CERTIFICATE.md`.

A real error in the proposed all-degree transfer proof was also found and
repaired: the centered identity is about `(r+1)^n`, not `r^n`. The old formula
fails already at n=1. `MOMENT_CORRECTION.md` proves the corrected identity for
all degrees and explains why the intended kernel argument survives. This is
same-assistant adversarial checking, not an outside mathematician's review.

Finally, new exact computations tested the low-degree D01 route. K0 and K1
have the same values e2=-23 and e3=-1067. The derived D01 values are e2=-47
and e3=-27911; the two-parallel was independently computed on the stored D01
PD and agrees. Both tested congruences pass. Agreement is not positive
concordance evidence. `D01_JONES_GATE.md` gives a short standalone derivation
of the two necessary conditions that does not rely on the all-degree lemma.

## Execution and validation

Seven direct cable evaluations were completed serially. Three were explicitly
normalization/known-value controls, and the remaining calculations are labeled
in the report. The largest contraction was K1's 198-crossing three-parallel:
about 10.17 seconds, at most 170993 states, arbitrary-precision integers,
2 GiB memory bound, 30-second time bound. No fifth KDG cable was attempted.

The new centered-moment checker passed 7602 elementary arithmetic checks
through degree 48, explicitly rejecting the old formula. The new direct-PD
checker passed 322 elementary checks, including all 27 original Wirtinger
relations, 240 finite conjugacy comparisons, and tampered-input controls.
Neither count is a count of knots or a replacement for the written proofs.

## Reproduce without network, SnapPy, Sage, or the Mac

The moment and marked-PD checkers require only Python 3:

```
python3 check_centered_moments.py --output NEW_MOMENTS.json
python3 marked_pd_certificate.py --output NEW_PD_CERTIFICATE.json
python3 check_marked_pd_certificate.py --certificate NEW_PD_CERTIFICATE.json --output NEW_PD_REPLAY.json
```

The direct Jones calculations require a C++17 compiler, Boost headers, and
Python with SymPy. Build the archived prior engine locally:

```
g++ -O3 -std=c++17 -DEXACT upstream/dependencies/pass02/frontier_jet.cpp -o jet_exact
python3 run_summand_jets.py K1 3 NEW_K1_THREE_PARALLEL --reverse --timeout 30
```

Every runner refuses to overwrite result directories. The `direct/` folder
contains exact diagrams/orders and original logs. `check_d01_gates.py` checks
those saved results and the symbolic connected-sum law:

```
python3 check_d01_gates.py --output NEW_D01_GATE_CHECK.json
```

For an independent replay of the *saved* finite certificate, no finder run is
needed: use its path as `--certificate marked_pd_certificate.json`.

## Remaining mathematical gap and next action

D01 still needs a smooth disk in standard B4; KDG still needs global
nonribbonness. The direct marked-PD certificate removes one computational
extraction dependency only. It does not verify the source paper's marked
figure-to-PD correspondence or exclude changed axes/nonlocal disks.

The single next target is ONE concrete changed-axis surgery presentation with
actual band paths, markings, framings and boundary identification. Apply the
direct diagram-level group check to it before attempting an annulus/standard
ambient proof. Do not repackage the original fixed axes with local knotting,
redo the settled D01 gates, or count another passing KDG cable as a lead.
Any actual new Opus disk/handle construction takes priority over this plan.

## Publication and coverage

Main was observed at `7a74678daccd9f3148b25a22a3f84a82eb1d374b` at both reads.
The present GitHub connection exposed read tools but no create/write action;
plugin discovery found the existing installed GitHub integration, not another
usable write action. Direct container GitHub DNS also remained unavailable.

**This package is local and NOT PUSHED.** Its additions-only patch targets
`results/astra_2026_09_17_overnight/pass04_0515_centered_and_marked_audit/`.
No new branch was created, no existing repository file was changed, and no
Mac or Opus process was touched. The original proof is archived unchanged;
a separately labeled corrected working copy is included. `coverage.json`
lists actual reading scope; no exhaustive repository review is claimed.
