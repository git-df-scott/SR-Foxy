# Final checkpoint — usage stop, no counterexample

20 September2026. The new user instruction was to keep working to the limit.
Displayed weekly usage reached24%, the saved operational stop before25%.
The amended baseline was20%, allowance five points; reset1790432260/61.
The automation is now PAUSED and the two pending continuation wakes must
not resume spending. No local jobs remain. All paused remote searches,
including GitHub35455048082, stayed paused. New work requires authorization.

## The surviving cable candidate

The precisely stored (2,1)-cable of10_17 remains unexcluded by this pass.
Its nonribbonness is source-backed, while standardB4 sliceness is unproved.
The trefoil same-sign exclusion does not apply to this companion.

CABLE_COVER_AUDIT.json checks ten cyclic-cover homology groups by two
methods: the companion-derived integral cable monodromy and SnapPy cyclic
exterior-cover torsion. All agree. Notably H1 of the four- and five-fold
covers is (Z/41)^2, the seven-fold cover is (Z/29)^2, the eleven-fold is
(Z/397)^2 and the thirteen-fold is (Z/1873)^2. These character primes were
outside the previous broad basic HKL run's saved ranges.

A new finite-field metabelian Fox implementation tested212 character
orbits across those five cover/prime pairs. Each of the two scalar deck
eigenspaces was tested on all nonzero characters, modulo deck conjugation
and sign. All passed the necessary norm screen at the listed reduction
prime. This does not test arbitrary sums of the two eigenspaces, prove the
characteristic-zero polynomial is a norm, or establish sliceness.

Controls: every representation relator and Fox chain identity checked;
K12n813 gives the expected non-norms; the K12n224 result agrees with the
published HKL Section10.6 polynomial up to Galois conjugacy/reversal;
ribbon controls6_1 and8_8 pass. METABELIAN_CONTROLS.json and
ALL_CHARACTER_SCREEN.json preserve full inputs and factorizations.

## A possible exclusion of the smaller difference

For D*=K7a2#-K10n4, both double covers have cyclic prime19 homology.
Every metabolizer of their orthogonal sum must meet both coordinates
nontrivially: a coordinate axis cannot be isotropic for a nondegenerate
one-dimensional linking form. Thus an annihilating nonzero character is
nonzero on both summands. We tested all81 pairs modulo independent signs,
without restricting to a convenient metabolizer or guessed linking isometry.

Successive finite-field norm screens over quadratic extensions of
F37, F113, F227 and F379 left respectively12,8,2,0 pairs. All these primes
are -1 modulo19, so Frobenius agrees with conjugation on the chosen
primitive nineteenth root. Generator, relator, abelianization and character
markings were checked consistent across all four reduction rounds.

This is strong evidence of nonsliceness, requiring a final proof audit.
It should not yet be presented as a finished exclusion. After the screen,
we completed exact Fox calculations over Q(zeta19) for one generator of
each summand's character line. Both reduced polynomials are monic integral
quadratics with constant term1. Their complete coefficient vectors are in
EXACT_SMALL_DIFFERENCE_v2.json; all other characters are Galois conjugates.

The final task not completed before the usage stop is to compare every
finite-field polynomial with the reduction of the appropriate exact
Galois conjugate, checking character identifications if simplified group
presentations differ. Then write out the good-reduction implication and
the connected-sum/inverse convention. A monic integral polynomial that is
a norm over the cyclotomic field reduces to a norm at conjugation-stable
primes: its monic factors remain integral, their degrees persist, and
conjugation reduces to Frobenius. Here the computed monic integral
quadratics make this route concrete. A final independent implementation or
review would strengthen the resulting computational proof.

If that audit succeeds, D* is not even topologically slice, so no smooth
concordance between these two precisely identified knots exists. Do not
spend on its disk/common-upper search before resolving this screen.

## Failures and implementation repairs retained

1. Initial finite-field controls falsely failed the Fox identity because
   FLINT fq_default(0) is truthy. Explicit equality with0 fixes sparse-zero
   deletion. Original failure JSONs remain in metabelian/; corrected outputs
   have v2 suffixes.
2. The first independent published-polynomial comparison had a transcribed
   sign error in the expected linear coefficient. The expected formula was
   corrected against SnapPy's quoted HKL example; the implementation itself
   was unchanged. METABELIAN_PUBLISHED_CONTROL_FAILED.json is preserved.
3. The first exact-field attempt stopped on an assertion: SymPy ANP equality
   to Python1/0 does not coerce as FLINT does. The generated exact function
   uses the domain unit and algebraic-number truth values. The failed and
   successful exact outputs are both preserved.
4. The initial pip command was unavailable; python-flint0.9.0 was installed
   with uv into the existing isolated scratch environment only.

## Source ledger and limits

Dai, Kang, Mallick, Park, Stoffregen, The (2,1)-cable of the figure-eight knot
is not smoothly slice, arXiv2207.14187v2 (2024), Theorem1.2 and following
paragraph: the Floer-thin/Arf1 result does not include10_17.
https://arxiv.org/html/2207.14187

Kang, Park, Taniguchi, Smooth concordance of cables of the figure-eight knot,
arXiv2505.03720, Theorem5.2: a newer obstruction requires a specific pair
of full-negative-twist disks. No such construction for10_17 was certified.
https://arxiv.org/html/2505.03720

Dunfield, Gong, Ribbon concordances and slice obstructions: experiments and
examples, arXiv2512.21825v1 (2025), Theorem3.3: for a slice knot an invariant
metabolizer exists for which all annihilating odd-prime-power characters
have norm twisted polynomials. Sections3.2–3.11 specify conventions.
https://arxiv.org/pdf/2512.21825

Allen, Livingston, Unknotting with a single twist, Enseign.Math.66 (2020),
541–589, DOI10.4171/LEM/66-3/4-10, Section6: determinant/Arf conventions.
Our exact companion determinant41 gives Arf(10_17)=0. No general two-disk
Arf theorem was established in this pass.
https://arxiv.org/html/2005.10717

All sources checked20September2026. These papers do not assert our new
D* screen as a published result. The exact polynomial calculations and
finite-field comparisons are our computations, not peer review.

GST status remains checkpoint02: source-qualified GST1–3 pass exact
Suzuki(2,2); the global knot obstruction and literal source-band transport
remain missing. The192-dart bridge is still an attachment-retrieval gap.
Concurrent research50 describes repaired nullhomotopy markings but still
lacks clean framed compression disks; word identities do not supply them.

Highest-value next authorized step: finish the exact-to-modular audit of
D*, then choose between the still-live10_17 cable and literal GST geometry.
No counterexample, slice disk or global GST knot nonribbon proof was found.
