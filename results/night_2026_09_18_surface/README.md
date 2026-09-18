# Explicit mapped-surface certificate

See `research/40_explicit_boundary_commutators_and_mapped_surface.md` for the
question, proof, source ledger, and limits.

New output: a 26-letter boundary correction (64 rewrites), an integral Fox
2-chain for it, and thirteen explicit commutators of exponent-zero boundary
words. This specifies a mapped surface, not an embedded geometric move.

Reproduce from repository root:

```sh
python3 results/night_2026_09_18_surface/shorten_boundary.py > /tmp/sr-short-boundary.json
/tmp/sr-foxy-night-venv/bin/python results/night_2026_09_18_surface/integral_short_boundary.py > /tmp/sr-short-integral.json
/tmp/sr-foxy-night-venv/bin/python results/night_2026_09_18_surface/factor_surface.py > /tmp/sr-surface-certificate.json
python3 results/night_2026_09_18_surface/check_surface.py
```

The producer uses Python 3.14 and SymPy 1.14; the checker needs only Python's
standard library. Producers read the saved upstream-stage JSON beside their
scripts. Compare regenerated outputs with those files; the commands above
preserve the saved evidence. The integral solver has a 60-second CPU cap;
rewriting has a 10,000-step cap. The tiny commutator factorization terminates
by decreasing residual length by at least four per step. No random seed or
unbounded search is used.

`surface_certificate.json` lists the relator product, Schreier dictionary,
balanced word, and every pair of boundary handle words. `replay.json` records
the independent verification and two rejected mutations. The checker validates
the substantive identity directly without trusting any symbolic-algebra output.
