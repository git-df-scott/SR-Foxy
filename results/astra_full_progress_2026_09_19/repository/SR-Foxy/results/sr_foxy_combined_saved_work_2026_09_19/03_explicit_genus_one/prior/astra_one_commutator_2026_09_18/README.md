# Astra: one-commutator correction certificate

No Slice–Ribbon counterexample. The new exact result is in `REPORT.md`.

The original 104-letter boundary correction equals [A,B], where

```
A = [4,-3,-3,1]
B = [4,-9,-1,3,-1,8,-5,-8,1,1]
```

These are one-based signed **boundary** generators. Both have exponent zero. A finite representation proves the correction nontrivial, so its commutator length inside G' is exactly one.

## Reproduce without Sage or a knot package

Python 3.10+ and Node.js 18+ suffice. Use fresh output paths:

```sh
python3 build_certificate.py > /tmp/astra_commutator_recheck.json
cmp CERTIFICATE.json /tmp/astra_commutator_recheck.json
python3 finite_witness.py > /tmp/astra_finite_recheck.json
cmp finite_witness.json /tmp/astra_finite_recheck.json
node check_independent.mjs > /tmp/astra_independent_recheck.json
cmp INDEPENDENT_CHECK.json /tmp/astra_independent_recheck.json
```

The independent checker does not import producer code. Its saved output records eight rejected corruptions. `OPTIMIZED_REPLAY.json` is the identical `python -O` replay of the producer.

To compare selected integer inputs with the frozen repository commit, run the OPTIONAL read-only checker in an environment containing that commit:

```sh
python3 verify_against_checkout.py '/Users/scottg/Documents/ChatGPT/SR Foxy/work/research-2026-09-16'
```

It uses only `git show` and never checks out, fetches, resets, or creates a branch. This checkout comparison has not been run in this session.

`ONE_HANDLE_RECIPE.json` is an algebraic input and insertion-order recipe, not a diagram or embedded-annulus certificate. Research/42's geometric construction remains a dependency of the E/unlink interpretation.

The exploratory scripts and intermediate results are retained. They write only their named local scratch outputs. The failed direct-rewrite shortcut is explicitly inconclusive. No old repository artifacts have been overwritten.
