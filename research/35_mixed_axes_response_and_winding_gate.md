# The mixed axes have a nonzero interaction, not a twist-count problem

18 September 2026. **CE: NO. No slice disk, modifying annulus, or new knot
identification is certified.** Work started from main `91732d4`; the user
explicitly requested the existing main branch. No new branch was created.

## Question and scope

Can the archived crossed axes be repaired to give the boundary polynomial of
D01, before attempting an embedded annulus? Put

    d = t^4 - 3t^3 + 5t^2 - 3t + 1,
    q = t(t^2 - 1).

The original boundary R is K0 # (-K0), and the intended D01 has polynomial d^2.
Success ultimately requires a disk in standard B4, identification with D01,
and the global nonribbon argument. None is replaced by the calculations below.

This pass replaces one numeric surgery parameter by two symbolic parameters.
It also derives a winding constraint from the boundary Alexander module and
checks an explicitly defined word-level repair against the saved collar maps.
There was no census rerun or expanded band search.

## 1. Exact two-parameter response of the archived link

Use the exact two archived zero-twist bands in pass09, on the same marked
54-crossing scaffold. The resulting link has components R, eta1, eta2.
The auxiliary sublink is the unlink by the earlier pass06 RII certificate;
that input fact was read, not independently rederived in this pass.
Preferred-longitude linking sums are all zero.

Fill eta1 with slope (1,x) and eta2 with slope (1,y), for integers x,y.
Zero means meridional filling. Since the axes are the unlink, these surgeries
have ambient S3. The exact Alexander polynomial is

    F(x,y;t) = d(t)^2 + x y q(t)^2.

**Computer-assisted proof, with a specialization-safe certificate.** The
Wirtinger/Fox presentation has 64 rows and 61 columns after removing the
R-meridian reference column. Fifty-five pivots are Laurent units +/-t^j,
independent of x,y. They reduce it to a 7-by-6 matrix. Its seven maximal
minors, in row-subset order, are exactly

    0, 0, -F/t^6, F/t^6, -F/t^6, F/t^6, -F/t^5.

Consequently its order is F for **every** integer specialization x,y. This
is not interpolation from a finite list and does not interchange a generic
gcd with specialization. F is monic, has constant term 1, and F(1)=1.
The full reduced matrix and all minors are saved in
`results/night_2026_09_18/surgery_response.jsonl`.

A second exact calculation uses rational-function row reduction of the
unfilled-link relations, retaining the two auxiliary meridians as free
coordinates. The preferred longitudes have response matrix

    B(t) = [[0, h], [-h, 0]],    h = q/d.

Thus the surgery equations are `(I + diag(x,y) B) mu = 0`, and
`d^2 det(I + diag(x,y) B) = F`. The implementation checks all unfilled
relations against its solved meridian coordinates. It also verifies
`B(t) = B(t^-1)^T`, since h(t^-1)=-h(t).

These are different exact elimination calculations, but they share the
archived diagram/Fox extractor. They are not two independent identifications
of the diagram with Abe--Tagami's paper.

**Consequences.**

- Either single surgery (x=0 or y=0) preserves d^2.
- Every nonzero opposite twist x=n,y=-n gives `d^2-n^2 q^2`, hence misses D01.
- More strongly, if xy is nonzero, F is not even divisible by d: d is coprime
  to q, so `F mod d = xy q^2` is nonzero.
- The opposite-twist family always has the Fox--Milnor factorization
  `(d+nq)(d-nq)`, since `t^4(d+nq)(t^-1)=d-nq`. Its determinant remains 169.
  These necessary sliceness conditions do not prove sliceness.

The opposite-twist all-parameter formula was already proved in
`results/astra_2026_09_18_local_band_no_go/` (read late in this pass); it is a
reproduction, not a new result. The additions here are the **independent
two-parameter extension, rational response matrix, boundary-module coordinates,
and specified winding-word incompatibility**.
Changing only the surgery coefficient cannot repair this fixed link.

## 2. A general algebraic design constraint

Work over L=Q[t,t^-1] and its field F=L/(d). The polynomial d is irreducible:
modulo 2 it is t^4+t^3+t^2+t+1, with no linear factor and not divisible by
the only irreducible quadratic t^2+t+1.

Suppose a modified two-axis response is

    B' = P B P* + E,

where P and E are Laurent matrices and * is transpose plus t -> t^-1.
If P is invertible modulo d, no nonzero opposite surgery can retain the
factor d in its output polynomial under the response formula. Indeed,

    d^2 det(I + diag(n,-n) B')
       = det(d I + diag(n,-n)(q P J P* + d E)),
    J = [[0,1],[-1,0]].

Modulo d this is

    -n^2 q^2 det(P) det(P*),

which is nonzero in F. Thus **a target d^2 requires det(P)=0 modulo d**;
being unimodular, or merely invertible modulo d, cannot help. This is a
proof for the stated algebraic model, independently reviewed in
`results/night_2026_09_18/algebra_review.md`.

The geometric interpretation is via the Blanchfield pairing: equivariant
linking modulo Laurent polynomials depends only on the lifted axis classes.
Changing representatives adds an E term, while changing their classes gives
P. This motivates requiring the two new classes to be dependent in the
two-dimensional d-primary module. Applying this gate to a new physical
surgery link still requires identifying its lifted classes and peripheral
conventions. An arbitrary band change must not simply be declared a
unimodular P.

Primary background checked: Anthony Conway, Lisa Piccirillo and Mark Powell,
*4-manifolds with boundary and fundamental group Z*, Comment. Math. Helv.
100 (2025), 323--420, DOI 10.4171/CMH/587, Proposition 3.8 (equivariant linking
and Blanchfield pairing). Section 5.2 treats the surgery determinant formula.
[Published paper](https://ems.press/content/serial-article-files/50353).
A printed-hypothesis inconsistency in Theorem 5.8 is documented in
`results/night_2026_09_18/source_check.md`; it is not silently corrected or
used as an unchecked theorem here.
The exact archived-link formula in section 1 is proved directly from Fox
minors and does not depend on transferring their surgery theorem's hypotheses.

## 3. Explicit boundary classes reveal the required winding change

The boundary R has Alexander module `(L/(d))^2`. Using the marked boundary
Wirtinger presentation, reduce over F and take the native based classes of
c1_upper and c1_lower as basis e_U,e_L. The checked coordinates are

    c1_upper = e_U,              c2_upper = t^-1 e_U,
    c1_lower = e_L,              c2_lower = t^-1 e_L,
    eta1 = e_U - t^-1 e_L,      eta2 = t^-1 e_U - e_L.

The script verifies every relator vanishes in these quotient coordinates.
The displayed basis is independent over F. In particular the mixed axes
are independent: their determinant is `t^-2-1`, nonzero modulo d.
This computation uses the **boundary** group, not the tentative disk collar.

Here is a precise proposed repair, defined first at word level. In each
archived axis word isolate the contiguous original lower-circle segment L_i.
Write the word as U_i L_i V_i, including the two band-edge words in U_i,V_i.
Replace it by

    U_1 mu^k L_1 mu^-k V_1,
    U_2 mu^l L_2 mu^-l V_2,

where mu is boundary generator 5 (the saved seam meridian). The complete
segments are saved in `winding_trace.json`; k=l=0 recovers the actual input.
This proposes inserting windings into the lower connector of **both** bands.
It does not supply new planar band diagrams or prove an embedded annulus.

Because each L_i has exponent sum zero, Fox differentiation shows that
conjugating it by mu^k multiplies its Alexander class by t^k. The new vectors
are therefore

    (1,-t^(k-1)),    (t^-1,-t^l).

Their determinant vanishes in F precisely when `k-l=2`. To see that the
condition is exact over all integers, d has no root on the unit circle:
for a root t, z=t+t^-1 satisfies z^2-3z+3=0, whose roots are nonreal.
Thus a root of d cannot satisfy t^m=1 for any nonzero integer m.

This supplies a concrete cancellation to aim for, rather than a larger
second-band path cutoff. Dependence alone is only a necessary condition;
no polynomial match or geometric surface follows from it.

## 4. The pure-meridian repair conflicts with every saved collar map

Use exactly the q_n partial-conjugation maps from the prior collar audit:
upper images fixed, lower images conjugated by the seam meridian mu^n.
Use its exact representation over

    Q[z]/(z^6+3z^5+5z^4+4z^3+2z^2+z+1).

The defining degree-six polynomial is irreducible by the saved mod-2 check.
The seam image is unipotent, so powers are `I+nN`, N^2=0, for all integers n.
This n is a collar parameter, unrelated to the surgery parameter in section 1.

At q0, the constant-in-z coefficient of the trace difference after k=l+2 is

    6l^2+14l+12 = 6(l+7/6)^2 + 23/6 > 0.

Hence no integer winding pair on the required line passes even the trace gate.
More generally all six z-coefficients for arbitrary q_n generate the unit
ideal Q[n,l]. The saved certificate gives **explicit linear multipliers**
a_i(n,l) with `sum a_i c_i = 1`. A separate standard-library rational-polynomial
checker verifies this identity and rejects mutations to both an equation and
a multiplier. There is no simultaneous complex solution, hence no integer
solution, for this word family and these q_n maps.

**Scope is essential.** This is an exact incompatibility in the specified
algebraic model. None of the q_n maps has been geometrically identified with
the intended marked product-disk collar. General conjugating words, different
attachments, changed surfaces, and different collar identifications are
outside the conclusion. It is not a universal mixed-band obstruction, a
negative finite diagram search, or a nonconcordance proof for K0,K1.

The smallest natural repair has therefore failed its model-level check before
spending on diagrams. No finite box was launched or claimed exhausted, and
none of the earlier untested 449 paths was reclassified.

## 5. One correction in the constructive direction

The Norman-trick dismissal in research/34 section 6 cannot follow just from
homology. Conditional on the necessary framed dual spheres and realizable
tubes, signed tubing changes the class by `-(C.F)[G]`; here C.F=0. Opposite
signs can cancel. See the literature note for the sign calculation and source
scope. This removes the asserted blanket homological exclusion, but supplies
neither embedded tubes nor simultaneous disjointness from a hyperbolic sphere
pair. The fixed-annulus cyclic-complement obstruction in research/14 remains.

## Evidence, limitations, and next action

A subsequent audit of three concurrent upstream commits is in
[research/36](36_audit_of_framing_and_miyazaki_closures.md). In particular, the
already archived 0110 choice has zero response matrix and the target polynomial;
the nonzero response computed above is specific to 0000. It must not be
promoted to an all-band obstruction.

| Claim | Evidence | Confidence / limit |
|---|---|---|
| Fixed-link F=d^2+xyq^2 | All symbolic maximal minors; rational response matrix | Exact for archived PD and peripheral extraction |
| Mixed axes independent modulo d | Exact boundary-module reduction | Does not identify a disk-exterior map |
| Pure-meridian repair fails all saved q_n | Explicit Bezout identity, independent rational replay | Only the defined word/collar family |
| Norman homology dismissal overreaches | Signed tube formula | Geometric realizability remains open |

All work and failures are recorded in `results/night_2026_09_18/README.md`.
No claim of historical novelty outside this repository is made.

**Next action:** derive the marked product collar from geometry, and use it to
choose joint band connectors with the required dependent boundary classes.
The pure seam-meridian words above cannot serve under any saved q_n; a new
connector must change the nonabelian word as well as its winding (for example,
by a specified zero-abelianization factor), with a candidate compression disk
tracked from the beginning. Do not enumerate those factors without a local
cancellation design. The missing result remains an embedded modifying annulus,
standard-B4 modification, and boundary identification with D01.
