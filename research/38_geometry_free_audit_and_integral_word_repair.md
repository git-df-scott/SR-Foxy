# Audit of 79fe4bc and an integral certificate for the correction

18 September 2026. **CE: NO. Smooth sliceness is still unknown.**
This follows the user's request to audit Opus's `79fe4bc` and continue hunting.
That hash is a merge commit; the new certificate itself is in `0caaff6`.

## Questions and success criteria

1. Does the new certificate really establish prime, fibered, distinct knots
   from the stored K0 and K1 diagrams without numerical hyperbolic geometry?
2. Can the constructive correction from research/37 be strengthened and
   simplified enough to guide a geometric realization?

An audit success is a reproducible check with correctly scoped theorem inputs.
A counterexample would require a disk in standard B4 for a knot covered by a
valid nonribbon theorem. No algebraic gate below replaces that disk.

## 1. The mathematical core of Opus's audit is sound

If a fibered knot is a connected sum, its summands are fibered. Alexander
polynomials multiply, and a fibered knot has Alexander breadth twice its genus.
An irreducible polynomial therefore forces one summand to have polynomial 1
and genus zero. It is the unknot. Thus a fibered knot with irreducible Alexander
polynomial is prime; no hyperbolicity is needed.

We recomputed HFK over F2 directly from the two stored PD codes using
Spherogram 2.4.1 and knot_floer_homology 1.2.2. The complete bigraded rank tables
agree with Opus. We checked positive integral ranks, the grading symmetry,
genus from the extremal Alexander support rather than just the summary flag,
and rank one at Alexander grading 2 for both knots. Their delta supports are
different: {0} versus {-2,0}. This proves distinctness for these PD knots;
it does not identify them with a particular figure in a paper.

As an independent Alexander calculation, the archived integer PD/Wirtinger
extractor followed by exact Fox calculus gives, for **both** diagrams,

    d=t^4-3t^3+5t^2-3t+1.

The 5-by-5 and 18-by-18 Fox minors each reduce to one entry by Laurent-unit
pivots. Their polynomials equal the integral HFK Euler characteristics. The
mod-2 polynomial t^4+t^3+t^2+t+1 is irreducible: it has no F2 root and is not
divisible by t^2+t+1, the only monic irreducible quadratic. Thus d is irreducible
over Q. This proves the arithmetic without numerical root finding.

The intended Miyazaki norm-free condition excludes **nonunit** f with ff*
dividing d. The literal wording "no f" in the original report needs that
qualification, since f=1 always divides. For f of positive Laurent breadth,
irreducibility excludes the product because both factors are nonunits over Q.
The remaining integer nonunits c*t^k with |c|>1 are excluded by primitivity of
d, since their norm is c^2.

**Audit verdict:** the core computation and primality argument pass for the
stored PD knots. The HFK recomputation uses the same backend as Opus, not an
independent Floer implementation. The Fox calculation is a separate invariant
calculation, not a substitute proof of fiberedness. This remains a
computer-assisted certificate rather than formally verified software.

The backend version matters: the maintainers removed a faulty alternating-knot
shortcut in the 1.2 release history. The installed 1.2.2 package is past that
fix. Primary implementation and release records, checked 18 September 2026:
[HFK calculator wrapper](https://github.com/3-manifolds/knot_floer_homology),
[release history](https://github.com/3-manifolds/knot_floer_homology/releases).
The [Spherogram documentation](https://snappy.computop.org/spherogram.html)
specifies the (Alexander, Maslov) rank indexing and default F2 coefficients.

The figure-to-PD and recovered-surgery identification remains separate. An
eventual disk construction for the exact stored connected sum would not need
that knot to bear the Abe--Tagami name. A construction starting from the paper's
marked annulus would still need a rigorous bridge to the stored endpoint.

The primary theorem audit is in
`results/night_2026_09_18_followup/theorem_audit.md`.

**Coefficient issue resolved explicitly.** Ni's printed statement uses an
integral top group Z; F2 dimension one alone does not exclude odd integral
torsion. Juhasz's rank-one formulation suffices instead. UCT bounds the
integral free rank by the F2 dimension; the top Euler coefficient 1 forces
free rank at least one. Hence the rank is exactly one. For genus, the
Alexander breadth gives g>=2, while top free nonvanishing for a minimal
Seifert surface would force F2 support at any larger actual genus. Thus g=2.
These facts use Juhasz, *Floer homology and surface decompositions*, Geometry
& Topology 12 (2008), 299--350, Theorems 1.4, 1.5 and 9.11,
DOI [10.2140/gt.2008.12.299](https://doi.org/10.2140/gt.2008.12.299),
[published paper](https://msp.org/gt/2008/12-1/gt-v12-n1-p07-p.pdf).
The producer now records this bridge, F2, and the backend version; it also
uses parity for exact Euler signs and explicitly excludes nonunit f.
Historical RESULTS.json was not overwritten.

## 2. The correction now has an integral second-derived certificate

Let G denote either the saved source presentation or the boundary Wirtinger
presentation. All meridians are identified by the abelianized relators, so
G_ab=Z. Let Lambda=Z[t,t^-1] and let X_tilde be the infinite cyclic cover of
the presentation complex. Its fundamental group is G', and

    H1(X_tilde;Z) = G'/G''.

For an exponent-zero word delta, its lifted cellular 1-cycle is the full
abelianized Fox derivative vector F(delta). The boundary of a lifted relator
2-cell is F(r_i). We found **integral Laurent polynomials** c_i such that

    F(delta) = sum_i c_i F(r_i),

in every generator column, for both saved words: the source correction and
its upper-boundary lift. This makes the lifted cycle an integral cellular
boundary and proves delta belongs to G'' in each presented group. The proof
does not require a faithful matrix representation, fiberedness, torsion-freeness
of the Alexander module, or an inference from rational vanishing.

For the boundary presentation the certificate is particularly small. With
relators indexed from 0 exactly as in the earlier collar certificate, only
five coefficients are nonzero:

    c2=(t-1)^2,       c3=t(t-1)^2,       c4=-t(t-1),
    c7=-(t-1)/t,     c8=-(t-1).

All five supported relators are from upper-half crossings. The source's
nine coefficients are

    [(t-1)/t, (t-1)/t, (t^3-2t^2+2t-1)/t,
     t^3-2t^2+2t-1, -(t-1)^2, t-1, (t-1)/t, 0, 0].

A separate standard-library verifier parses these as integer Laurent
polynomials, reconstructs Fox derivatives without SymPy, validates the exact
relator provenance and abelianization, checks every column, and rejects a
mutated coefficient. The certificates are in `integral_correction.json`.

This discharges a limitation deliberately retained in research/37. It proves
integral second-derived membership of this particular word. It still does not
prove nullhomotopy: a word can lie in G'' and be nontrivial, as this one does
under the inherited nonabelian obstruction.

## 3. From 104 letters to 20, with every move recorded

A deterministic rewriting pass uses only cyclic permutations of the original
source relators and their inverses, plus free cancellations. Each replacement
strictly decreases shortlex order and never increases length. No group-word
enumeration, completion procedure, or claim of shortest length is used.

After 73 moves the 104-letter source correction becomes

    [-3,-2,5,5,-6,5,8,-3,-8,3,7,1,-2,5,-4,-6,4,2,-6,-6].

All indices are the original one-based source generators. The independent
checker replays each move against the original relators and rejects a mutated
replacement. This word equals the old source correction **in the presented
group**, whereas the old 104-letter word retained a literal free-word identity
under substitution. The shorter word uses more source generators, so it is not
automatically a shorter boundary connector with the old three-letter lift
dictionary. This is a group-word simplification, not a minimal band diagram.

The exact repair remains

    b' = delta b,       q0(b') = mu^-1 q0(a) mu,

with [b']=[b] in the **integral** boundary Alexander module. Consequently the
new certificate strengthens the earlier rational preservation statement. It
does not fix the Laurent ambiguity in the longitude response or prove that
the earlier zero response E=0 is retained by a geometric realization.

## 4. A literature-supported geometric direction, with a specific gap

Membership in G'' means delta is a finite product of commutators of elements
in G'. This suggests looking for a clasper description with null-homologous
leaf curves, instead of adding more meridional windings. It is a proposed
realization strategy, not a produced clasper or a theorem about this word.

Garoufalidis--Rozansky, *The loop expansion of the Kontsevich integral, the
null-move and S-equivalence*, Topology 43 (2004), 1183--1210,
DOI [10.1016/j.top.2004.01.002](https://doi.org/10.1016/j.top.2004.01.002),
define null claspers by null-homologous leaves and prove preservation of
Blanchfield forms (Section 1.3, Lemma 1.3).
[Author-hosted published paper](https://people.mpim-bonn.mpg.de/stavros/publications/printed/the_loop_expansion_of_the_kontsevich_integral_the_null_move_and_Sequivalence.pdf).
Naik--Stanford's *A move on diagrams that generates S-equivalence of knots*
gives doubled-delta moves generating S-equivalence:
[original preprint](https://arxiv.org/abs/math/9911005).

These theorems do not state that a prescribed correction of marked auxiliary
curves fixes their equivariant longitude representatives, preserves an unlink
diagram, extends over a slice-disk complement, or supplies an embedded annulus.
Those relative conditions must be established in a concrete construction.
The productive next attempt is to realize the displayed correction with a
specified local surface/clasper move and compute its full response E. A
generic appeal to S-equivalence would leave the central gap untouched.

## Evidence ledger and remaining work

| Claim | Evidence | Limitation |
|---|---|---|
| Opus's stored-PD hypotheses | Fresh HFK and independent Fox agreement | Same Floer backend; cited detection theorems |
| Integral correction in G'' | Full integer Laurent 2-chain, independently replayed | No nullhomotopy or embedding |
| 20-letter source representative | 73 exact relator/free rewrites | No minimality or geometric connector claim |
| Clasper realization might preserve algebraic data | Precise primary null-move theorems | Required relative realization is unproved |

Reproduction scripts, versions, hashes, caps, and raw certificates are in
`results/night_2026_09_18_followup/`. The main unresolved goal remains a
standard-B4 slice disk for a certified nonribbon boundary.
