# Reproduce the September 12 audit

The recorded environment was Python 3.14.6 on macOS, with SnapPy 3.3.2, Spherogram 2.4.1, Regina distribution 7.4.1 (runtime reports 7.4), SymPy 1.14.0, passagemath-standard 10.8.11, knot_floer_homology 1.2.2, and matplotlib 3.11.2. The machine-readable environment record is authoritative. The full Sage-compatible runtime is required for the HKL calculations; the final rational non-norm verifier needs only Python's standard library. No GPU is used.

The session installed these into a separate virtual environment beside the clone. On a supported platform, install the recorded packages in a virtual environment, or use a compatible native Sage installation with the same SnapPy/Spherogram versions. Wheel availability is platform dependent. Replace `python` below with that environment's Python. Run commands from the repository root.

## Exact checks

The three algebraic audit scripts either create a missing result or recompute and compare with an existing result. They do not overwrite mismatched data.

```sh
python scripts/audit_seifert_model.py
python scripts/reproduce_at_models.py results/AT_seifert_models.json
python scripts/audit_hkl_applicability.py
python -m unittest discover -s tests -p test_research_audit.py -v
```

For experiments whose runtime and presentation may vary, use new output paths:

```sh
mkdir -p ../recheck
python scripts/verify_at_inputs.py ../recheck/AT_inputs.json
python scripts/reproduce_hp_obstruction.py ../recheck/HP_HKL.json
python scripts/verify_hp_norms.py ../recheck/HP_HKL.json ../recheck/HP_rational_check.json
```

The expected HKL answers are `(2,3)` for both advanced and direct methods, with four non-norm polynomials. Synthetic division certifies odd root multiplicities 1,3,3,1. The positive control K12n813 also returns `(2,3)` with the advanced method.

To rerun the meaningful but inconclusive Abe–Tagami checks:

```sh
python scripts/hkl_targeted.py data/knots/AbeTagami_D_0_1.json ../recheck/D01_a213.json --p 2 --q 13 --method advanced
python scripts/hkl_targeted.py data/knots/AbeTagami_D_0_1.json ../recheck/D01_a37.json --p 3 --q 7 --method advanced
python scripts/hkl_targeted.py data/knots/AbeTagami_D_0_1.json ../recheck/D01_a52.json --p 5 --q 2 --method advanced
python scripts/hkl_targeted.py data/knots/AbeTagami_D_0_1.json ../recheck/D01_d213.json --p 2 --q 13 --method direct
```

`null` means no obstruction in that calculation. In the last run 14 candidate subgroups were reduced to four, not eliminated. SnapPy's direct method enumerates subgroup candidates using their abstract structure; it does not in this routine impose the actual linking pairing. A useful further refinement is to intersect the surviving norm conditions with **actual isotropic metabolizers in the same homology basis**. The basis compatibility is an essential missing step, so no stronger conclusion is claimed here.

## Search and filter

```sh
python scripts/fusion_successors.py data/knots/AbeTagami_K_0_K_-1__6_3.json ../recheck/AT0.jsonl --length 6 --twists 2 --moves 100000 --seconds 150
python scripts/fusion_successors.py data/knots/AbeTagami_K_1.json ../recheck/AT1.jsonl --length 6 --twists 2 --moves 50000 --seconds 180
python scripts/fusion_successors.py data/knots/AbeTagami_K_0_K_-1__6_3.json ../recheck/AT0_detours.jsonl --length 9 --twists 3 --moves 40000 --seconds 150 --detours 16 --seed 20260912 --per-face-moves 3000
python scripts/filter_common_successors.py ../recheck/filter.json --inputs results/fusion_AT0_threaded.jsonl.gz results/fusion_AT1_threaded.jsonl.gz --sample 0
python scripts/compare_successors.py results/fusion_AT0_detours.jsonl.gz results/fusion_AT1_threaded.jsonl.gz ../recheck/comparison.json --left-filter results/fusion_HFK_filter_detours.json
```

Retain and probe the wider run’s targets:

```sh
python scripts/select_successor_targets.py results/fusion_AT0_wider.jsonl.gz results/fusion_HFK_filter_wider.json ../recheck/targets.json
python scripts/search_target_predecessor.py ../recheck/targets.json ../recheck/backward_probe.json --count 3
```

This backward probe starts from proposed **upper bounds** and looks for K₁ below them. It differs from the old, futile search for a knot below both original inputs.

Recorded per-run headers in `results/search_archive_manifest.json` contain the original bounds, seeds, and stop conditions. Time caps can change coverage on another machine. `per_face_moves` is itself a search cap: reaching every face does not exhaust every possible band. The later wider run uses length 10, twists 5, 24 detour attempts, seed 20260913, and 4,000 moves per face, capped at 32,000 moves.

All original JSONL logs are stored losslessly as gzip, with compressed and uncompressed SHA-256 checksums. Reader scripts accept both forms. The uncompressed originals were also retained outside the repository during this session. Early pilot logs retain failed designs; only the corrected threaded/detour generator is represented by the current source. Historical result metadata still names the original uncompressed paths.

The band replay checker uses Spherogram for both creation and replay. HFK injection and τ controls are additional sanity checks; neither replaces an independent movie verifier. Diagram signatures permit orientation reversal as a search index but not reflection. Numerical peripheral isometry comparisons preserve ambient orientation; a proposed hit would still require certified identification and a full orientation audit.

## Figures

```sh
python scripts/render_research_figures.py ../recheck/figures
```

The Floer figure uses exact recorded ranks. The knot figure uses stored PD codes and Spherogram's orthogonal layout, preserving under/over crossing assignments. It illustrates a rejected one-sided target, not a counterexample. Source-matrix checks, obstruction logs, and seven regression controls are retained under `results/`.
