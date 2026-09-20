# Checkpoint 3 — exact source moves, stronger controls, bounded family tests

2026-09-20, 00:50 UTC. **No Slice–Ribbon counterexample. Campaign remains active.** The user added seven percentage points to the original allowance: total 14 additional points from baseline 7%, same reset epoch 1790432260/61, operational stop at displayed 20%. Latest checked usage 12%. Deadline remains 2026-09-20 04:41:43 UTC / September 19 10:41:43 PM MDT. Earlier checkpoint budget statements are historical and superseded.

Success still requires a precisely identified knot, a smooth disk in standard B4, and independent global nonribbonness of that same knot. No link result, finite search, group presentation, numerical isometry, or invariant match replaces these obligations.

## 1. New exact connection between two source transcriptions

`search_source_movie.py` found elementary Reidemeister sequences relating our Figure `example` and Figure `gompf6` transcriptions for n=1,2,3, k=1. `replay_source_movie.py` replays each native Regina move, checks four components persist, and verifies the terminal component-coloured planar dart maps. Directed rotation and over/under parity are preserved, with an allowed 3D diagram rotation at the first endpoint; no mirror reflection is allowed. The component order follows the ordered Regina input components. These are certificates between the encoded diagrams, conditional on the original paper-to-diagram transcription.

| n | total moves, both paths | endpoint crossings | result |
|---|---:|---:|---|
| 1 | 115 | 16 | PASS |
| 2 | 306 | 20 | PASS |
| 3 | 200 | 24 | PASS |

Inputs and move paths: `MOVIE_SEARCH_n{1,2,3}_rot.json`. Verifier outputs and explicit dart bijections: `SOURCE_MOVIE_CERTIFICATE_n{1,2,3}.json`. Deliberately invalid crossing indices were rejected. The two traces share braid helpers and conventions; this is not total independence. Integer surgery coefficients on the labelled red components are retained under ambient isotopy with preferred longitudes. Initial 60-second n=1 search without allowing endpoint rotation found no hit after 695003 iterations; preserved separately in `MOVIE_SEARCH_n1.json`. That failure did not mean different links.

## 2. Concurrent repo correction agrees with the earlier discrepancy

origin/main is 2a071282514b448da4b5f0ab44afcc3308fee562; checkout remains 3e4461e23fce6687293f6abef963011b37677c55. The new remote `results/opus_2026_09_19_session_L11_built/RETRACTION_IT_IS_L01.md` withdraws the old claimed L11 and explains a lost spiral turn. It identifies the stored diagram with ribbon census L10n36. Precise source-index identification still needs a Kirby/diagram certificate, as that retraction itself notes. This independently supports our previously recorded mismatch; it does not by itself certify every new source input.

The external GHMR paper describes an 18-crossing L11 diagram and a 40-crossing L21 diagram. Our n=1 has 18 crossings, but such counts and Jones matches are not identification proofs. The checked GHMR repository/examples supplied no named GST PD data. Source files are in `sources/ghmr/`; do not repeat this as an untried route.

## 3. A real nonribbon control with ribbon components — but not slice

`build_square_pair_control.py` starts with census L14n38935, checks both its components simplify to trefoils, and ties a mirror of each component locally into that component. The resulting 20-crossing link has two actual square-knot components, linking number zero, Jones nullity one, and det V = 225. Ribbonness would require det V congruent to 9*9 = 81 modulo32. Instead the residues are 1 versus17, so Eisermann obstructs ribbonness of the whole link. Full Regina and independent skein Jones calculations agree.

This is **not** a counterexample: `check_square_pair_alexander.py` certifies a nonzero 19-by-19 Alexander minor at t1=t2=2 modulo101, determinant83, independently checked with SymPy. Thus the link is not strongly slice. See `SQUARE_PAIR_NONRIBBON_CONTROL.json` and `SQUARE_PAIR_ALEXANDER_CERTIFICATE.json`. This control demonstrates that the Jones test can obstruct a link even when every component is ribbon; it does not provide a way around the sliceness requirement.

## 4. Signed normalization clarifies the empirical mod16 observation

For positive knot determinant D, the signed normalization is D when D=1 mod4 and -D when D=3 mod4: a symmetric Alexander polynomial normalized to Delta(1)=1 has Delta(-1)=1 mod4. `screen_signed_mod16.py` reproduces the census screen with this convention. All 439 stored examples have det V minus the product of signed component determinants divisible by16. This is finite evidence, **not a theorem**.

There are 159 signed modulo32 violations in that population. `screen_signed_violators.py` finds nonzero maximal Alexander minors for **all 159**, already at the first specialization (2,2) modulo101. No candidate survives the classical sliceness test. These calculations close only these census records, not Eisermann's question about slice links or GST. The old square-determinant-only screen was insufficient to characterize the actual population.

## 5. Additional source-family cases and resource failures

`family_case.py` constructs explicit pre-surgery n,k inputs, verifies the red sublink simplifies to the unlink, fills its labelled slopes, reconstructs a link with surviving meridians, and saves every input/output. The k extension remains exploratory under the shared twist convention.

| n,k | output crossings | component D | det V or residue | Jones gate |
|---|---:|---|---|---|
| 3,-1 | 100 | 9,25 | 193 | passes |
| 3,0 | 26 | 9,1 | 73 | passes |
| 4,1 | 92 | 25,9 | -383 | passes |
| 2,2 | see saved PD | 9,49 | 25 mod32 (root jet) | no obstruction |

Full-polynomial jobs (2,2), (3,2), (3,-2) hit 120-second limits; (2,-2) exited -9 for an unconfirmed reason. The last large job (3,3) was deliberately terminated (-15) after memory use grew and the prior -9 failure. These are resource failures, not mathematical negatives. Initial import failures were fixed and preserved in `family/INITIAL_IMPORT_FAILURES.json`.

`bounded_root_jet.py` instead uses the existing quotient-ring method modulo32 and a 100000-state cap. Controls passed for ribbon L10n36, the new nonribbon square-pair control, and provisional n=3,k=1. It recovered the (2,2) result using 15104 states. Cases (3,-2), (2,-2) hit the state cap; (3,2), (3,3) hit 60-second limits. Saved PDs survive for a different bounded method. No jobs remain intentionally running. An initial missing Jones ring initialization was corrected by installing the sage-free Jones adapter; do not regard that exception as a mathematical result.

## 6. New route from the source link to the target knot

`probe_preblow_fusion.py` fuses only the two black components in the four-component n=3,k=1 source **before** red surgery. Original red components are identified after each band by their exact original crossing-label occurrence multisets. This avoids assuming post-band component order. The red slopes +1 and -1 are then filled. It is a distinct route from the paused 433348-case inverse band search on the 48-crossing knot.

All 27 same-face black-component bands with twist counts -2 through2 satisfying orientation parity were constructed. None numerically matched the target volume 23.84489979556321 from `data/knots/GST_B31_regina.json`; the closest difference was about0.6305. Some triangulations had negative tetrahedra, so this is explicitly a numerical screen rather than certified exclusion. Exact band specifications, surgery labels and all PDs are in `preblow_fusion/RESULT.json`.

**Most valuable next step:** allow one crossed diagram edge in the pre-surgery band core, retaining exact red-component tracking, and seek a peripheral-preserving equivalence with the independently traced Figure2 knot. Use a strictly bounded local search. A positive numerical match must be upgraded to an explicit move/Kirby certificate. If no match, follow the literal dotted band through the source isotopies rather than expand an unbounded search. This could strengthen slice provenance but supplies no global nonribbon proof by itself. In parallel conceptually, pursue ribbon-preserving satellite obstruction transfer only with its universal implication proved; the old blanket lane closure was retracted.

## Sources checked and reproducibility

- R. Gompf, M. Scharlemann, A. Thompson, *Fibered knots and potential counterexamples to the Property 2R and Slice-Ribbon Conjectures*, Geometry & Topology14 (2010),2305–2347; arXiv:1103.1601v1 (2011-03-08), https://arxiv.org/html/1103.1601v1. Figures `example`, `gompf6`, and the standard-B4 sliceness construction. Source PDFs/EPS/Text.tex preserved.
- M. Eisermann, *The Jones polynomial of ribbon links*, Geometry & Topology13 (2009),623–660, https://pnp.mathematik.uni-stuttgart.de/igt/eiserm/publications/ribbonlinks.pdf. Corollary6.9 supplies the ribbon-link congruence; Remark3.6 states the vanishing Alexander polynomial for slice links with at least two components. Question7.1 is a question in this paper, not a theorem we can assume.
- S. Gukov, J. Halverson, C. Manolescu, F. Ruehle, *Searching for ribbons with machine learning*, arXiv:2304.09304v2 (2025-06-13), https://arxiv.org/html/2304.09304v2. Reported GST small-case diagrams and ribbon-search limitations. Associated repo checked at33335b26fdbfa9c503fa7813369c0de2a8312876.
- N. Dunfield, M. Obeidin, C. Rudd, *Computing a Link Diagram from its Exterior*, arXiv:2112.03251, https://arxiv.org/abs/2112.03251; implementation https://snappy.computop.org/triangulation.html#snappy.Triangulation.exterior_to_link. Prescribed meridians are essential.

Primary-source checks performed September19 MDT / September20 UTC2026. Python runtime `/tmp/sr-foxy-20260919-leads-venv/bin/python`: SnapPy3.3.2, Spherogram2.4.1, Regina versionString7.4. Scripts, exact input PDs, moves, failures and outputs are preserved here. Keep remote run35455048082 and other explicitly paused remote searches paused. Preserve concurrent files. Never restart the usage allowance on a wake.
