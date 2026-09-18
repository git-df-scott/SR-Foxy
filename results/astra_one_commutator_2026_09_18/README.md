# Astra: the full correction is one commutator

Published at Scott's request on existing `main`. No new branch; no Mac checkout access. This is an additive publication, not a new counterexample claim.

## Start here

`REPORT.md` states and proves the new algebraic result. The original 104-letter boundary correction is `[A,B]`, with one-based signed boundary words:

```text
A = [4,-3,-3,1]
B = [4,-9,-1,3,-1,8,-5,-8,1,1]
```

Both have meridional exponent zero. An exact finite representation proves the correction nontrivial, so its commutator length in the recorded group's commutator subgroup is exactly one. The geometric next step is a single marked genus-one realization of the full correction, followed by a framed surgery-boundary check. No embedded annulus or standard-B4 slice disk has been produced.

## Complete reproducible bundle

`BUNDLE.tar.xz` preserves **all 27 original files**, byte for byte, from the conversation's `SR_Foxy_One_Commutator_2026-09-18.zip`. Only archive compression and metadata differ. It includes the full proof certificate, producer, independent JavaScript verifier, original inputs, finite witnesses, one-handle recipe, failed attempt, source and coverage registers, and original README and manifest. No scientific artifact was omitted.

`ARCHIVE_MANIFEST.json` is an unchanged copy of the original manifest; its paths refer to files INSIDE the bundle. `SUMMARY.json`, `INDEPENDENT_CHECK.json`, and `REPORT.md` are unchanged convenience copies. Statements in those original files that nothing was pushed describe the earlier research session, before this authorized publication.

Bundle SHA-256:

```text
5a1e64010dabcf469bba33a8a4e35b318403c84424cf37835bc73ea7f72aa6f7
```

Publication replays are in `PUBLICATION_RECHECK.json`. All 26 files listed in the original manifest matched their hashes; the 27th file is the manifest itself. Every bundle member was also compared byte for byte against the original ZIP. The Python producer, optimized Python producer, finite-witness producer, and independent JavaScript checker all reproduced their saved outputs exactly. Eight deliberately corrupted certificates were rejected by the independent checker.

## Reproduce without modifying the checkout

From the repository root, extract into a fresh temporary directory. Python 3.10+ and Node.js 18+ suffice:

```sh
work=$(mktemp -d "${TMPDIR:-/tmp}/sr-commutator.XXXXXX")
tar -xJf results/astra_one_commutator_2026_09_18/BUNDLE.tar.xz -C "$work"
cd "$work/astra_one_commutator_2026_09_18"
python3 build_certificate.py > ../python_recheck.json
cmp CERTIFICATE.json ../python_recheck.json
python3 -O build_certificate.py > ../optimized_recheck.json
cmp CERTIFICATE.json ../optimized_recheck.json
python3 finite_witness.py > ../finite_recheck.json
cmp finite_witness.json ../finite_recheck.json
node check_independent.mjs > ../independent_recheck.json
cmp INDEPENDENT_CHECK.json ../independent_recheck.json
```

The optional `verify_against_checkout.py` compares transcribed integer inputs with source commit `19cddf9f527f8d3487943b98bba2c7f355629426`; it is included but was not run against the user's Mac. The geometric q0 identification, actual surgery boundary, embedded modifying annulus, standard ambient ball, and nonribbonness for that same boundary remain separate obligations.
