# Follow-up on Opus 79fe4bc: audit and constructive correction

18 September 2026. **No Slice--Ribbon counterexample.**
Report: [research/38](../../research/38_geometry_free_audit_and_integral_word_repair.md).
All work is on the user's requested existing main branch.

## Verified results

- Recomputed the two stored HFK tables. Both match Opus exactly; independent
  Fox minors give the same irreducible degree-four Alexander polynomial.
- Made F2 coefficients explicit and supplied the UCT/Juhasz rank-one argument
  instead of conflating field dimension one with an integral group Z.
- Found integral Laurent 2-chains for the correction in both the source and
  boundary presentations. This proves membership in G'', strengthening the
  prior rational Alexander-module statement.
- Reduced the source correction from 104 to 20 letters using 73 recorded
  relator/free reductions. This is not a shortest-word search or a band diagram.
- Independently replayed integral certificates and rewrites using only the
  Python standard library, with coefficient and rewrite mutation controls.

## Reproduction

Python 3.14.6; SymPy 1.14.0; Spherogram 2.4.1; knot_floer_homology 1.2.2.
Installed into the existing disposable `/tmp/sr-foxy-night-venv`, not the repo.

```sh
python audit_geometry_free.py
python integral_correction.py
python3 shorten_correction.py
python3 check_integral_and_rewrite.py
python ../opus_2026_09_19_0000_geometry_free_certificate/check_geometry_free.py
```

Scripts print outputs rather than silently replacing archived results. Run
with assertions enabled. The two algebra producers have 60/90 CPU-second
limits; the HFK/Fox audit also has a 30-second per-knot alarm and matrix-size
guards. Both HFK audits completed in approximately one second locally. The
rewrite has a 10,000-step guard, terminated after 73 moves, and never increases
word length. No census, path enumeration, or long symbolic completion ran.

`geometry_free_audit.json` is the fresh HFK/Fox check.
`geometry_free_producer_recheck.json` records 11/11 for the revised Opus checker;
its historical RESULTS.json remains untouched. `integral_correction.json`
records words, relators, and coefficients. `shortened_correction.json` records
every rewriting move; `integral_replay.json` records the independent replay.
`theorem_audit.md` contains the Luna primary-source audit, the coefficient
resolution, and review of the integral Fox implication.

## Scope and failures

The mathematical checks passed. The first attempt to read research/14 used
an incorrect filename; the actual marked-annulus note was then read. The
original AMS Miyazaki PDF was inaccessible to the literature audit, so its
statement was checked via Abe--Tagami's explicitly labelled restatement.
No direct reading of that AMS PDF is claimed.

The HFK rerun shares Opus's Floer implementation. The Fox control shares the
archived diagram extractor used earlier in this campaign. Neither identifies
the PD with a paper figure. The upper word correction is not a drawn band,
and G'' membership supplies neither a nullhomotopy nor an embedded annulus.
Full longitude response, actual collar identification, ambient standardness,
and target boundary identification remain open.

During integration, upstream `03833e5` added the MP/RBG note. Its cited GHMR
Section 6 was checked: the counts and ten named survivors refer to the finite
3375-pair census. Both partners were shown ribbon in the 843+5 resolved cases.
This does not exhaust all RBG links or all parameters. That incoming checker
was read but not independently rerun in this pass; it was preserved unchanged.
Primary source: Gukov--Halverson--Manolescu--Ruehle,
[*Searching for Ribbons with Machine Learning*, Section 6](https://web.stanford.edu/~cm5/sliceML.pdf).

## Next constructive step

The integral correction is a concrete candidate for a local null-homologous
clasper/surface realization. Specify the marked move, then compute the full
equivariant response E and track an actual embedded annulus. The checked
null-move/S-equivalence literature only supports the algebraic motivation; it
does not supply those relative geometric conclusions.
