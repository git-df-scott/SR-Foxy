# Positive K0/K1 complement identification

Read `research/44_positive_combinatorial_K1_identification.md` for the exact
claim and software trust boundary. This package is not a hyperbolicity or
non-homeomorphism certificate.

The saved final triangulations have explicit orientation-preserving simplicial
isomorphisms. The integer-only checker parses the saved SnapPea files and
checks every face identification independently of SnapPy. It does not verify
the preceding kernel moves or the paper's diagram transcription.

Run from repository root:

```sh
python3 results/night_2026_09_18_positive_identification/check_certificate.py
```

Rebuild into a new directory, preserving saved evidence:

```sh
/tmp/sr-foxy-night-venv/bin/python results/night_2026_09_18_positive_identification/build_certificate.py --output /tmp/sr-positive-identification-fresh
python3 results/night_2026_09_18_positive_identification/check_certificate.py /tmp/sr-positive-identification-fresh
```

Producer environment: Python 3.14, SnapPy 3.3.2, Spherogram 2.4.1; random seed
18092026; 45-second CPU cap. The temporary virtual environment is disposable.
Combinatorial numbering can vary across platforms; replay the newly generated
map against its own saved triangulations rather than requiring byte equality
of numerically selected triangulations. No negative result is promoted to a
non-homeomorphism claim.

`replay.json` records 72 directed face checks across the two positive cases
and four rejected mutations. Ten `.tri` files preserve the intermediate states.
