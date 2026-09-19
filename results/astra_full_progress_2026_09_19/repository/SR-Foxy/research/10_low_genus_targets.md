# Restrictions on a common upper target for the stored Abe–Tagami pair

Research date: 12 September 2026. **No counterexample is established.** Write
`K <= J` for a smooth ribbon concordance with births and fusions going from K
to J. J is a successor under ribbon concordance; J itself is not assumed ribbon.
In fact J is concordant to the nonslice knot 6_3 and therefore cannot be ribbon.

The exact question is whether the stored K0 and K1 admit a common J. A pair of
verified oriented movies, with a verified common endpoint, would give a smooth
concordance K0 ~ K1 and a smooth disk for D01 in standard B4. The separately
audited Abe–Tagami nonribbonness implication would then make D01 a counterexample.

## Necessary algebra, with genus qualifications

Normalize Alexander polynomials symmetrically with value 1 at t=1, and put

`d(t) = t^2 - 3t + 5 - 3t^-1 + t^-2`.

Ribbon concordance implies d divides Δ_J. Concordance and Fox–Milnor imply
`Δ_J d = h(t)h(t^-1)`. Unique factorization, together with irreducibility and
reciprocity of d, lets us cancel d squared from this norm: hence
`Δ_J = d f(t)f(t^-1)` for an integral Laurent polynomial f with f(1)=±1.
Indeed, a reciprocal irreducible factor occurs to even exponent in a norm;
every nonreciprocal factor is paired with its reciprocal. After removing d²,
the same conditions hold for the integral quotient. No assertion about a
geometric realization of f is being made.

Zemke's bigraded injection theorem forces HFK(J) to dominate the maximum of
the two source rank tables, separately in each (A,M) grading. That envelope has
rank 21 and Euler polynomial

`e(t) = 2t^2 - 5t + 7 - 5t^-1 + 2t^-2`.

It is not an allowable Alexander polynomial for J. For any specified Δ_J, a
necessary rank bound is

`rank HFK(J) >= 21 + sum_A |[t^A](Δ_J - e)|`.

Each extra generator changes one Euler coefficient by only ±1, which proves
the inequality. It is an optimistic algebraic lower bound, not a realization
theorem or a claim that a knot attains it.

* **Genus two:** Δ_J=d, since divisibility and the degree bound leave only a
  constant quotient. The rank bound is **29**, not merely 21. Its top Alexander
  grading must contain both source generators, so J cannot be fibered.
* **Genus three, Δ_J=d:** the bound improves to **33**. Genus detection requires
  nonzero HFK at A=±3, and the zero Euler coefficients there require at least two
  generators at each end, in addition to the rank-29 bound.
* **Genus three, nonconstant quotient:** f has breadth one. After multiplying
  by a unit, write f=at+b with a+b=±1. Its norm is
  `c(t+t^-1)+(1-2c)`, where c=ab. Nonzero c belongs to {-2,-6,-12,...}; c=-1
  is impossible. Its signs alternate with those of d, so the coefficient
  absolute sum is `13(1-4c) >= 117`. Thus **rank at least 117** is necessary.
* **No fibered common target has genus at most three.** Genus two was excluded
  above. At genus three a fibered target has Alexander breadth six and leading
  coefficient ±1, which would require |c|=1 in the preceding calculation.
* **Fibered genus four:** the norm quotient has breadth four and leading
  coefficient ±1. Normalize f to a monic quadratic with constant ±1. The
  condition f(1)=±1 leaves exactly three distinct norm quotients:

| Norm quotient | det(J) | Necessary rank bound |
|---|---:|---:|
| `3-t^2-t^-2` | 13 | 45 |
| `t^2-2t+3-2t^-1+t^-2` | 117 | 117 |
| `t^2-6t+11-6t^-1+t^-2` | 325 | 325 |

`scripts/low_genus_successor_bounds.py` checks the arithmetic and finite
quadratic enumeration, using the actual stored input PDs. Results are in
`results/low_genus_successor_bounds.json`.

## What this changes in the search

The new coupled-birth target at K0 batch-1 index 10187 is fibered of genus four,
has total HFK rank 149, and occupies the determinant-117 row. Both sources pass
the quotient-chain injection and homotopy-retraction tests against it. These
are algebraic passes, not a second movie. Its 26-crossing PD and K0 movie are
saved in `results/coupled_K0_batch1.jsonl.gz` and the selected-target file.

A proposed shortcut is to pin J=K0#R for ribbon R. This supplies the K0 arrow,
but ordinary connected sums are restrictive here. Since K0 is δ=M−A thin at
zero, any δ-thin R at zero makes J thin and immediately excludes the K1 arrow.
The script checks the small stabilizer names already considered in the
repository. All listed small examples fail the K1 injection test, including
11n42 (its δ-support is {0,1}). This is a rejection of these pinned endpoints,
**not** a rejection of Teichner stabilization of D01 by the same R. Those are
different constructions. Ribbonness of the named R is not needed for the
rank rejection and is not newly certified by this test.

## Primary sources and confidence

* Ian Zemke, *Knot Floer homology obstructs ribbon concordance*, Annals of
  Mathematics 190 (2019), 931–947; [arXiv:1902.04050](https://arxiv.org/abs/1902.04050),
  Theorem 1.2: grading-preserving injection for a ribbon concordance.
* Stefan Friedl and Mark Powell, *Homotopy ribbon concordance and Alexander
  polynomials*, Archiv der Mathematik (2020), DOI
  [10.1007/s00013-020-01517-5](https://doi.org/10.1007/s00013-020-01517-5);
  [arXiv:1907.09031](https://arxiv.org/abs/1907.09031), Theorem 1.1:
  Alexander divisibility, with the larger knot at the ribbon-concordance top.
* Anthony Conway, *Algebraic concordance and Casson–Gordon invariants*, author
  [lecture notes](https://www.unige.ch/math/folks/conway/Notes/AlgebraicConcordanceCassonGordon.pdf),
  undated here: Fox–Milnor norm condition for slice knots. Applied to J#(-K0).

The rank tables depend on the HFK implementation. The bounds above are exact
deductions conditional on those tables and the cited standard theorems. They
do not exclude higher-genus targets, nor nonfibered targets in the allowed rows.
The most useful next geometric test is a directed reverse search from the
smallest surviving target, retaining linked intermediate stages.
