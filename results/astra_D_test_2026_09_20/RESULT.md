# D = K9n4 # (-K14n282): marked test excludes sliceness

20 September 2026. This supersedes the surviving-lead status in `../astra_additional_3pct_2026_09_20/HANDOFF.md`.

**Result:** the computation supplies a twisted-Alexander/Casson–Gordon obstruction to locally flat sliceness of this D, hence to smooth sliceness. It is not a Slice–Ribbon counterexample. This is our reproducible computational deduction using published theorems, not an independently reviewed result.

## Exact question and definitions

Minus denotes the concordance inverse (mirror with reversed orientation). Knot names use the SnapPy/Spherogram census; the precise input PD codes are saved in `EXACT_MARKED.json`. Success would require a smooth disk in standard B4 and global nonribbonness for this same knot. Here the test instead rules out such a disk.

## The coordinate issue is resolved

The earlier calculation found three matching polynomial pairs but did not identify their linking-form coordinates. To avoid guessing an isomorphism between independently simplified presentations, this test reconstructs a Wirtinger presentation directly from each PD diagram. The same mod-7 cocycle is used both for the Fox twisted-torsion calculation and for Fox-to-Dehn region coloring. The region coloring supplies the character in a reduced Goeritz presentation.

For a Goeritz matrix G and an integer lift v of the character vector, Gv is divisible by 7. The dual linking pairing numerator is

    d = (v^T G v)/7 mod 7.

Indeed x=Gv/7 is integral and x^T G^-1 x = v^T Gv/49; pairing x with a presented generator evaluates the character divided by 7. A common overall orientation sign does not affect the isotropy condition for a difference of two knots.

The recorded characters give d0=6 for K9n4 and d1=3 for K14n282. Thus an annihilating character for a metabolizer of the difference must satisfy

    6 a^2 - 3 b^2 = 0 mod 7,

or b=±3a. There are exactly two isotropic lines; no coordinate axis is isotropic. In a nonsingular two-dimensional metabolic linking form the annihilator of a metabolizer is an isotropic line in the dual pairing, so this enumerates all possibilities.

## A single explicit obstruction covers both lines

Let z be a primitive seventh root of unity. In these marked coordinates, characteristic-zero reduced twisted polynomials are

    F0(t) = t^2 + (z^5+2z^4+2z^3+z^2+1)t + 1,
    F1(t) = t^2 + (z^5-z^4-z^3+z^2)t + 1.

Character scale c replaces z by z^c. These coefficients are fixed by z -> z^-1, verified exactly modulo Phi_7. Choose (a,b)=(1,3) or (1,-3), one nonzero character on each isotropic line. At the saved prime above 13, their polynomials reduce respectively to

    t^2 + 11t + 1 = (t-1)^2,
    t^2 + 3t + 1.

The second quadratic has discriminant 5, a nonsquare modulo 13. Its two roots in F_(13^2) are distinct and satisfy r^13=r^-1. Thus its two linear factors are each fixed by conjugate reciprocity and appear with odd multiplicity. Neither is a root of the first polynomial. The product is not a conjugate-reciprocal norm.

For completeness, the conjugate-reciprocal norm condition is unchanged by the connected-sum normalization factor (t-1)^2, which is a norm up to Laurent unit. Taking a concordance inverse inverts the discriminant class; modulo norms this yields the same parity obstruction. Both summand characters here are nontrivial.

The characteristic-zero polynomials are monic with algebraic-integer coefficients and constant term one. Any monic factor has algebraic-integer coefficients, and its constant coefficient is a unit. Therefore a norm factorization would survive reduction at a conjugation-stable prime above 13 (13=-1 modulo 7). The finite-field non-norm is consequently an obstruction in characteristic zero, not merely a failed numerical search. The odd-character norm sliceness theorem then excludes both possible metabolizers.

The earlier polynomial matches occurred at b=±2a instead. They do not annihilate a metabolizer: 6-3(2^2)=1 mod 7. This explains exactly why the earlier unmarked test failed to exclude D.

## Verification and limits

- Exact cyclotomic arithmetic from the new Wirtinger presentations reproduces both earlier polynomials. No unknown generator identification is used for the marked computation.
- Representation relators, the Fox chain identity, exact Bareiss divisions, and reduced-polynomial normalization are checked by the reused implementation.
- Every possible base face and both checkerboard choices give the same marked pairing: all 11 face choices for K9n4 give 6; all 16 for K14n282 give 3.
- Reordered crossing lists preserve the paired invariant. Mirror controls reverse the linking sign after explicitly matching character scale through the polynomial; K14n282's mirror requires scale 2. All four controls passed.
- All nine nonzero character pairs modulo independent signs were enumerated. The isotropic pairs are (1,3),(2,1),(3,2); none is among the three exact polynomial matches.
- Reductions at both 13 and 41 were computed. The prime-13 witness at (1,±3) alone suffices for the exclusion.
- Preliminary Levine–Tristram signatures agreed at fractions .05,.1,.2,.3,.4,.5 of a full turn (0,0,0,-2,-2,-2). This finite numerical check was not used in the proof. An initial attempt to use NumPy failed because it was unavailable; the check was rerun with mpmath.

The remaining general limitation is independent review of the implementation and conventions. No slice-disk search should be pursued for this D unless a concrete flaw in the obstruction is identified.

## Primary sources checked

1. Lorenzo Traldi, *Link colorings and the Goeritz matrix*, arXiv:1701.04308v4 (8 June 2017), https://arxiv.org/pdf/1701.04308. Definitions 2–3 and Theorem 4 give the Fox/Dehn coloring correspondence; the paper relates the region colors to the Goeritz kernel.
2. R. A. Litherland and S. D. Wallace, *Surgery description of colored knots*, Algebraic & Geometric Topology 8 (2008), 1295–1332, https://msp.org/agt/2008/8-3/agt-v8-n3-p04-s.pdf. Proposition 3.4 and its proof, sections 3.2.2–3.2.3, identify v^T Gv/p with the dual linking/Bockstein value for a marked character.
3. Nathan Dunfield and Sherry Gong, *Ribbon concordances and slice obstructions: experiments and examples*, arXiv:2512.21825 (2025), https://arxiv.org/pdf/2512.21825. Theorem 3.3 supplies the odd-prime character norm obstruction. Section 3.23 explicitly discusses using a marked linking form to reduce the two-dimensional case to two possible metabolizers. The exclusion of this D is our deduction, not a claim from that paper.
4. Tetsuya Abe and Keiji Tagami, *Fibered knots with the same 0-surgery and the slice-ribbon conjecture*, Math. Res. Lett. 23 (2016), 303–323, DOI 10.4310/MRL.2016.v23.n2.a1, https://arxiv.org/pdf/1502.01102. Corollary 4.3 was verified directly: distinct fibered knots with irreducible Alexander polynomials give the relevant nonribbon difference. That half does not rescue a candidate now obstructed from being slice.

All accessed 20 September 2026. The published Abe–Tagami PDF initially loaded but a subsequent request returned HTTP403; its arXiv version supplied the exact corollary.

## Reproduction and status

Runtime: `/tmp/sr-foxy-20260919-leads-venv/bin/python`.

Run `marked_test.py`, then `exact_marked.py`, then `certify.py` from the repository root. `certify.py` also consumes the saved `MARKED_SCALES.json` (all three character scales at primes 13 and 41). That file records exact inputs and outputs of `probe(name, M(G(Link(name))), 2, 7, 6, ell, scale)` from `marked_test.py`. The scripts reuse the preceding session's Fox implementation; they do not run remote searches.

Displayed weekly usage was 26% at the beginning and at the last check. No recurring automation or paused remote search was resumed. This requested candidate test is complete.
