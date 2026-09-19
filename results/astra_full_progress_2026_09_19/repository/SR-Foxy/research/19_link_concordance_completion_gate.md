# A completion obstruction, odd Khovanov tests, and direct Teichner probes

13 September 2026, evening. **No counterexample found.** The objective is a
smoothly embedded disk in standard B4 for a knot with a separate proof of
nonribbonness. For D01 = K0 # (-K1), the latter is recorded in the existing
Abe–Tagami/Miyazaki audit; sliceness remains unknown.

## Exact link computation

All **1,092** saved zero-linking, component-Jones matches in
`results/normalized_component_neighborhoods.json` have generic multivariable
Alexander-module rank zero. This includes all **156** recognized K0/unknot
component pairs. The independent triangulation-group computation confirms
every case. These are counts of saved diagrams, not isotopy classes.

Put F = Q(t1,t2) and beta(L) = dim_F H1(S3 minus L; F), with the meridian
of component i acting by ti. Link concordance preserves beta. A split pair
of knots has beta = 1, so none of these links is link-concordant to any
split knot/unknot pair. This improves the earlier *three-dimensional*
nonsplitting result; it is not nonconcordance of the original knots.

**Primary source:** Tim Cochran and Shelly Harvey, *Homology and derived
series of groups*, Geometry & Topology 9 (2005), 2159–2191, published
22 November 2005. [Author PDF](https://math.rice.edu/~shelly/publications/Stallings.pdf),
Corollary 3.3 and the paragraph following its proof, pp. 2169–2170.
Read 13 September 2026. The exterior of a link concordance is a homology
cobordism, and the Alexander-module rank is concordance invariant.

The split-pair value can also be checked directly: its group is the free
product of the two knot groups. Each knot's Alexander H1 vanishes over F;
the Mayer–Vietoris sequence for the wedge contributes a single F from
H0 of the intersection point, since both twisted H0 groups vanish.

### Why the finite computations certify generic rank

For n generators, the colored Fox matrix has rank at most n-1: its rows
annihilate the nonzero vector whose entries are each generator's monomial
minus one. A nonzero (n-1)-minor modulo a prime at nonzero component values
proves that the corresponding integral Laurent polynomial is nonzero.
Consequently its rank over F is exactly n-1 and beta = n-1-(n-1) = 0.
We never identify rank at one finite evaluation with a concordance invariant.

The first nonzero witnesses occur at:

| evaluation | modulus | cases |
|---|---:|---:|
| (2,2) | 101 | 925 |
| (3,3) | 103 | 165 |
| (2,3) | 101 | 2 |

Failure at a specialization is **unknown**, not proof of a zero polynomial.
The last two cases do not establish identically zero diagonal polynomials.

`colored_link_rank.py` uses Wirtinger arcs; `check_colored_link_rank.py`
uses the group from a combinatorial exterior triangulation and solves its
meridian abelianization independently. SymPy exact integer determinants
recheck all advertised minors. No numerical hyperbolic isometry claim is
needed. Controls include a split K0/unknot pair, a Whitehead component sum,
and an explicitly constructed nonsplit link ribbon-concordant to a split
pair. The last control prevents confusing nonsplitting with nonconcordance.

## Completion lemma: an elementary deduction to audit

**Claim, with a self-contained argument; not claimed as a new published
result.** Let P be a connected, oriented, genus-zero embedded movie prefix
in S3 x [0,a], with one incoming knot and two outgoing components L. If P
extends, unchanged, to a smooth embedded annulus in S3 x [0,1], then L is
link-concordant to a split knot/unknot pair. There is no restriction on the
critical points of the proposed continuation.

1. As an abstract surface, P is a pair of pants. Its complement Q in the
   final annulus has Euler characteristic 1 and three boundary circles:
   the two circles L and the final knot. Every component of Q is planar.
   If Q has c components, chi(Q) = 2c-3, so c=2. There are no closed
   components. Its boundary distribution is therefore 2+1.
2. The final knot cannot be the boundary of the disk component: that would
   make the final annulus disconnected. Thus Q consists of an annulus
   from one component of L to the final knot and a disjoint disk bounded
   by the other component of L. The disk need not be ribbon.
3. Choose an embedded arc in the remaining four-dimensional product from
   an interior point of the disk to a point on the final S3 away from the
   final knot. General position lets its interior avoid both surfaces.
   Remove a small disk around its starting point and extend the new circle
   along a thin tube around the arc to the final boundary. The tube can be
   chosen disjoint from the other annulus and the rest of the disk; the
   normal bundle along an interval is trivial. Smooth the joins.
4. The punctured disk plus tube is an annulus ending in a small unknot
   contained in a ball disjoint from the final knot. Together with the
   other annulus, it gives the required link concordance in the unchanged
   standard product.

Therefore beta(L)=0 prevents **every annular completion of that fixed
prefix**, even completions with more births, fusions and deaths. It does
not prevent a different prefix from succeeding. It also does not upgrade
the componentwise HFK/Kh ancestry tests to arbitrary continuations: those
still require the relevant annuli to be ribbon.

The genus-zero and connected-prefix hypotheses matter. A genus-one
continuation is not covered. A nonsplit but link-concordant-to-split link
is allowed, as the positive control demonstrates. The general m-component
version has one complementary annulus and m-1 disks, hence beta=m-1;
a specialization with H1 dimension below m-1 obstructs such a completion.
An adversarial Claude prompt was prepared through Computer Use. The app
did not confirm submission; no independent Claude review is claimed.

## A broader embedded-band family

The previous reverse sampler forbade returning to a face. The new sampler
allows face returns but forbids reuse of an original diagram edge. Within
each face it checks cyclic chord endpoints for interleaving, ensuring the
projected core can be embedded. These conditions still omit self-crossing
projections and many other bands; there is no exhaustive claim.

Seven targets, seed 20260919 plus target index, length at most 14, and
45-second per-target bounds produced **35,930** normalized zero-linking
bands. The rank test rejected **35,521**; **409** retained diagrams remain
unknown. None matches the opposite source's component Jones polynomials.
All 409 raw bands, face-chord certificates and saved invariants replay.
This restricted face-return sample recovered **zero known-source returns**;
it has no positive source-recovery calibration. Do not advertise its
negative result as a powerful exclusion of unseen band classes.

## Rational odd Khovanov test

**Primary source, preprint:** Jacob Migdail and Stephan Wehrli, *A module
structure on odd Khovanov homology and the odd invariant for ribbon 2-knots*,
[arXiv:2607.04018v1](https://arxiv.org/html/2607.04018v1), header dated
4 July 2026, internal date 24 August 2026; read 13 September 2026.
Theorem 8 supplies ribbon-concordance injectivity over Q and Z/(2^k).
We use Q only. Remark 21 expresses unreduced odd Kh as two quantum shifts
of reduced odd Kh. KnotJob's `-ko1` computes the reduced version, so the
comparison explicitly reconstructs the unreduced groups with shifts +1,-1.
The theorem is formulated in R3 x I. A compact smooth surface in S3 x I
avoids some vertical point-line after choosing a point outside its
2-dimensional projected image, so this necessary existence test applies.
We do not assert functoriality under all S3 x I isotopies.

| knot | reduced Q rank | unreduced Q rank | K1 injection deficit |
|---|---:|---:|---|
| K0 | 13 | 26 | not a target |
| K1 | 29 | 58 | identity |
| J25533 | 125 | 250 | none |
| J25541 | 125 | 250 | none |
| C2 | 125 | 250 | none |
| C4 | 125 | 250 | none |

The four target bigraded tables agree. Both known K0-to-J movies pass.
Eight inputs, including trefoil and ribbon 6_1, pass independent Regina
Jones/Euler checks. Reflecting K1 reverses both gradings as required.
These controls do not formally verify the homology implementation.
No new target is excluded by this test.

## Failures preserved, not converted into negative results

- An initial Fox pilot treated `_pieces()` tuples as strand objects; fixed
  before obtaining results.
- The first independent audit chose two fresh evaluations that happened
  to be roots of a nonzero polynomial. Both implementations agree there
  and at a nonzero witness. The halted partial audit and regression are saved;
  the completed audit verifies each case's actual nonzero witness.
- `Link.copy()` drops detached-unknot bookkeeping. The face-return run
  stopped at this issue; its partial output is preserved. Inspection now
  starts from the raw PD with both components explicit. A split K0/unknot
  regression reproduces 2 components becoming 1 under the bad copy path.
- The geometry checker initially compared JSON lists with tuples, then
  demanded identical crossing order after simplification. It now checks
  exact raw band replay, diagram signatures and the saved invariants.
- Native Sage/Singular multivariate minors segfaulted in both initial
  Teichner sum probes after partner verification. Logs are saved. The
  replacement uses a weaker necessary Alexander-rank filter and does not
  change installed libraries. Timeouts remain UNKNOWN.

## Direct certificate target following Claude's update

Scott supplied Claude's report of 72 one-band survivors per RBG side and
running D01 partners 8_8,10_3. PR #3 at 579abda was inspected read-only;
its branch and running cloud jobs are preserved. The RBG numbers are
Claude's reported coverage, not independently repeated here. No certificate
for D01 appears in that report or the inspected PR.

The local probes add J=9_41 and 9_46. Each J's ribbon certificate is
separately replayed. A ribbon certificate for D01#J would imply [D01]=0
in smooth concordance, since [J]=0; gluing the corresponding disks and
concordances stays in standard B4. Together with the existing global
nonribbonness argument this would be a counterexample. Passing a slice
filter proves neither required certificate.

Teichner's own [14 March 2010 explanation](https://mathoverflow.net/questions/7052/what-would-the-slice-ribbon-conjecture-imply)
states the converse as well: every slice knot admits such a ribbon partner.
The needed forward implication also follows directly from the concordance
group calculation above. No claim is made that the constructed disk
necessarily requires 3-handles or cannot admit another presentation.

See `results/teichner_D01_J941_probe.json` and
`results/teichner_D01_J946_probe.json` for bounded-run status; each has a
180-second cap. A generated-band count is not completed coverage of the
search tree. The most valuable next experiment is to save and resume the
actual surviving first-stage movies, rank-filter their descendants, and
verify any terminal ribbon-link cache certificate all the way to an unlink.

The 61 older J25533 intermediates were also checked at three colored
specializations: 32 have independently confirmed rank zero. The two
Kh-surviving first bands remain unknown under this test. The completed
record is `results/ancestry_link_rank_25533.json`.

The first capped Teichner probes checkpointed at least 6,100 (9_41) and
6,500 (9_46) generated bands before timeout; neither completed its box.
The later mixed-attachment pass tested 41,167 and 41,855 bands respectively,
including subsequent unrestricted second fissions. It saved 217 and 370
retained diagram paths and found no terminal ribbon certificate. Each pass
had a 150-second soft cap. The first band attaches across the original
connected-sum factors; this is a search preference, not an exhaustive
normal form. All retained paths are in `results/teichner_D01_J*_mixed.json`.

## A ribbon-only gate inside the Teichner search

**Primary source:** Tetsuya Abe and Keiji Tagami, *Fibered knots with the same
0-surgery and the slice-ribbon conjecture*, arXiv:1502.01102v3, 4 April 2015,
[Corollary 4.3](https://arxiv.org/html/1502.01102v3), read 13 September 2026.
It states that fibered knots with irreducible Alexander polynomials can
have ribbon difference only when the knots agree. Apply it to two visible
summands A,B of a current component: distinct Jones polynomials for A and
mirror(B) exclude ribbonness of A#B. A strongly ribbon link must have ribbon
components, by forgetting the other disjoint ribbon disks.

This is a ribbon obstruction **within the auxiliary ribbon-disk search**,
not a sliceness obstruction on D01. HFK establishes the computed fiberedness
and Alexander data; exact Seifert evaluations at -1,1,2,3 agree. All 84
unique factors finish, with no failed factor calculation. Equality of Jones
polynomials does not establish isotopy and causes no exclusion.

| partner | saved links | direct exclusions | direct or inherited exclusions | retained unknown |
|---|---:|---:|---:|---:|
| 9_41 | 217 | 31 | 108 | 109 |
| 9_46 | 370 | 43 | 129 | 241 |

A forbidden first prefix rules out its descendants in the same pure-fission
ribbon-disk search. All 587 raw band moves, factor decompositions used for
exclusions, rank checks, and both partner certificates replay. The pairing
test retains K0#mirror(K0) and rejects the stored D01 control. The checker
initially demanded a fixed ordering of connected-sum factors; it was
corrected to compare the unordered pair. No mathematical exclusion depended
on that ordering. The 350 retained paths include 21 first-stage paths.

The depth-three continuation tested 50,767 further bands for 9_41 and
50,845 for 9_46, saving 209 and 246 retained paths. Neither run found a
terminal ribbon certificate. Each used a 150-second soft cap and continued
saved depth-two prefixes, with the cached factor obstruction available.
These additional paths are in `results/teichner_D01_J*_third_band.json`.

## Final narrowing and a missing mirror partner

The conservative replacement for the crashing native filter omitted cheap
component sliceness tests. Restoring these on all 805 live/more deeply
extended paths rejects 803; all these exclusions already follow from a
component having nonsquare determinant. All 392 distinct component
determinants agree independently between Seifert matrices and Regina Jones
polynomials. The remaining computed HFK, tau, and explicit Fox–Milnor norm
factorizations pass; no component calculation timed out.

Only two first-stage 9_46 paths survive: `78685a_1_-2` and `00676e_0_-2`.
They have a 32-crossing nontrivial component and an unknot component;
these statements alone do not assert splitness. After visible connected-sum
decomposition and seeded simplification, the second path's knot component
has the same unoriented factor diagram signatures as **D01 # mirror(6_1)**.
The signatures permit reversing individual factor orientations; a complete
orientation-preserving identification of the connected sum is not certified here.
For the first path, K0 and mirror(6_1) are recognized but the remaining
19-crossing factor is still unrecognized. No identity is inferred merely
from its matching polynomials.

This exposes a genuine coverage gap: the old logged 4.2-hour Teichner run
used **6_1**, whereas this return uses **mirror(6_1)**. Both that partner and
D01 are chiral by their Jones polynomials, so reflecting only the partner
is not dismissed by amphichirality of the target. This does not prove the
two sum diagrams are distinct in every other possible way, or that the
mirrored partner is more likely to succeed. It is an explicit untried input
in the old coverage ledger, reached constructively from the new search.

Continuing both surviving first-stage paths exhausts the selected shortest
band family (length <=6, twists <=2): 24,359 generated moves, no ribbon
certificate, and 96 retained paths after linking, generic-rank and component
determinant tests. These are *unknown paths*, not certified slice links.
They are saved in `results/teichner_D01_J946_component_filtered_continuation.json`.
The next constructive work should screen and extend these explicit paths,
and deliberately include mirrored nonfibered partners. Repeating a names-only
partner list or the original failed first-stage sweeps loses this information.
