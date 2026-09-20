# The trefoil cable candidate (-9,-3) fails the sliceness test

20 September 2026. This is our explicit deduction from the source results below, with finite algebra checks. It is not a new Slice–Ribbon counterexample or a claim of independent peer review.

Write T for the right-handed trefoil, C_{2,q}(T) for its cable, and U_{2,q} for the torus knot. The exact proposed knot was

    C = C_{2,-9}(T) # -C_{2,-3}(T) # U_{2,-3} # -U_{2,-9}.

Claim: C is not smoothly slice. With the genus-one upper bound below, g4(C)=1. Thus withdraw this particular candidate from a slice-disk construction search. Do not infer a closure of the full Hom–Park family or of GST.

## Source inputs

Matthew Hedden, Paul Kirk, Charles Livingston, *Non-slice linear combinations of algebraic knots*, JEMS 14 (2012), 1181–1208, DOI 10.4171/JEMS/330. https://arxiv.org/html/0909.1247 ; checked 2026-09-20.

We use Lemma 2.2 (cable cover and linking form), Proposition 3.1 (satellite formula), Lemma 3.2 (orientation), the slice-metabolizer condition at the start of Section 4, Theorem 5.1 and Corollary A.2 (discriminants), and the Fox-matrix method in the proof of Lemma 5.2. Section 8 supplies g4<=1 for this cable-difference family. We do NOT apply their coprimality-dependent Theorem 6.5 or Proposition 4.2 to our noncoprime parameters.

Jennifer Hom, JungHwan Park, *Ribbon knots and iterated cables of fibered knots*, Mathematische Zeitschrift 313, article 53 (2026), DOI 10.1007/s00209-026-04050-3. https://link.springer.com/article/10.1007/s00209-026-04050-3 ; checked 2026-09-20. Proposition 1.4 gives nonribbonness and ordinary knot-Floer local equivalence to the unknot here. Neither assertion supplies sliceness.

## 1. Orientation and linking form

Put Q=-T and J=-C. Cabling commutes with mirror/orientation reversal by reversing the second cable parameter, so

    J = C_{2,9}(Q) # -C_{2,3}(Q) # U_{2,3} # -U_{2,9}.

In this order, the first homology of its double branched cover is

    H = Z/9(A) + Z/3(B) + Z/3(E) + Z/9(D),
    lambda = diag(1,-3,3,-1)/9.

The group has order 729 and a metabolizer has order 27. Use E for the third coordinate to avoid confusing it with the knot C. Characters to F3 are written (a,b,c,d); their value is a*A+b*B+c*E+d*D mod3.

## 2. A witness for every metabolizer

Let V be any metabolizer, Vbar its image in H/3H=F3^4, and W=ann(Vbar) the characters vanishing on V. We claim W contains a character with a=1,b=0.

Otherwise the functional a on W vanishes on ker(b), so a=k*b on W for some k in F3 (this also covers b identically zero). Ordinary finite-dimensional duality then implies (1,-k,0,0) is in Vbar. Lift it to v=(A,B,E,D) in V. Isotropy requires

    A^2 - 3 B^2 + 3 E^2 - D^2 = 0 mod9.

Reduction modulo3 gives A^2-D^2=0. But the specified residue vector has A=1,D=0 modulo3, a contradiction. Therefore a character with b=0 and a nonzero exists; scale to a=1.

This argument quantifies over EVERY metabolizer and does not classify or select only diagonal ones.

## 3. Satellite contribution

Let z be a primitive cube root and omega=-z^2 a primitive sixth root; z*omega=-1 and z^-1*omega=omega^-1. Apply the general satellite formula separately to all four summands, allowing both cable characters to be nontrivial. For the character from Section 2, a=1,b=0, the companion part of tau(J,chi) is

    alpha_Q(z*t) + alpha_Q(z^-1*t) - 2 alpha_Q(t).

The remaining terms are torus-knot Casson–Gordon classes for U_{2,9} and U_{2,3}, with arbitrary order-three characters and signs.

The Alexander polynomial of Q is t^2-t+1, up to a unit. Its valuations at t=omega after the three substitutions are respectively 0,1,1. Thus the companion discriminant has valuation 0+1-2=-1, which is ODD modulo norms. Units and inversion change no parity. This is equivalently a nonzero discriminant parity in F2.

## 4. Composite parameter 9 checked separately

The published Lemma 5.2 is stated for prime parameters. We instead reproduce the portion of its Fox calculation needed here, for each q in {3,9} and each phase d in {0,1,2}.

Use the presentation <alpha,beta | alpha^2 beta^q>, with

    A0 = [[0,1],[t,0]],
    rho(alpha) = t^((q-1)/2) A0,
    rho(beta) = t^-1 diag(z^d,z^-d).

The relator maps to the identity since q is divisible by3. The Fox formula has numerator det(I+rho(alpha))=1-t^q and denominator, up to a monomial unit,

    (t-z^d)(t-z^-d).

At omega, both are nonzero: omega^3=omega^9=-1 and omega is not a cube root. Any H0 correction and the (1-t)^e factor are also units there (rho(beta)-I is already invertible locally at omega). Consequently every torus term has discriminant valuation zero at omega. This checks the trivial character as well as the two nontrivial phases; phase choices from changing lift generators are included.

Therefore the TOTAL Casson–Gordon discriminant has odd omega valuation. A norm has even valuation at a unit-circle root, so tau(J,chi) is nonzero.

## 5. Contradiction and independent checks

If J were slice, a metabolizer would exist for which every prime-order character annihilating it had vanishing Casson–Gordon class. Sections 2–4 produce a violating character for each metabolizer. Hence J, and therefore C, is not slice.

`audit_metabolizers.py` exhaustively enumerated all isotropic subgroups: 1 of order1, 22 of order3, 43 of order9, and 14 of order27. All 14 metabolizers have the required witness. `METABOLIZERS.json` records every subgroup and its witnesses; runtime about0.053 seconds.

`audit_discriminants.py` works exactly in Q(z), verifies all six representation relators, and checks all root valuations without floating-point approximation. `DISCRIMINANTS.json` records the results. The direct valuation argument is independent of a signature sign convention.

Limits: these computations verify the finite algebra, not the cited topology theorems. The proof is a local research deduction awaiting outside mathematical review. It rules out this precise proposed knot; it does not prove that every negative cable difference is nonslice. A future broader statement needs its own quantifier and character audit.
