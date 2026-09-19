# A low-wrapping transfer lemma for the Eisermann tests

17 September 2026 UTC. **NO COUNTEREXAMPLE.** This is a new deduction in this
session, not a claimed publication novelty. A complete proof is supplied below;
independent mathematical review is the first overnight gate. The application
to KDG is conditional on the previously recorded cable identifications and
computations. No new satellite diagram, slice disk, or Jones evaluation was
computed in this pass.

## Claim and scope

Let K be a knot with signed Jones determinant d congruent to 1 modulo 8.
Suppose its zero-framed two- and three-parallels have normalized Jones nullity
at least 1 and 2, respectively, and their Jones determinants satisfy

    e2(K) = d^2 (mod 32),    e3(K) = d^3 (mod 32).

Then every ribbon pattern P in a solid torus with geometric wrapping number
at most three produces a satellite P(K) that passes BOTH of the following
Eisermann necessary conditions for ribbonness:

* its normalized Jones nullity is exactly c(P)-1;
* its Jones determinant equals the product of its signed component
  determinants modulo 32.

Here “ribbon pattern” means that P(U), with the standard zero-framed embedding
of the solid torus, is a ribbon link. This is Definition 6.12 of Eisermann,
and Proposition 6.13 gives preservation of ribbonness for a ribbon companion.
The number c(P) of pattern components is unrestricted. Wrapping number is
geometric intersection count with a meridional disk, NOT algebraic winding.

More precisely, the proof works whenever the integral annular bracket has
support contained in {1,z^2} or {z,z^3}. The geometric wrapping bound is a
sufficient condition for this support statement. A pattern of larger wrapping
can still have small skein support and therefore yield no new test.

This does not prove P(K) ribbon, K ribbon, or the slice-ribbon conjecture.
It does not concern Khovanov homology or every satellite obstruction. It makes
no assertion about arbitrary wrapping-four patterns or higher Jones jets.

## 1. Integral conventions, not a division in characteristic 32

Work in R = Z[A,A^{-1}], with

    delta = -A^2-A^{-2} = -A^{-2}(A^4+1).

Use the unnormalized Kauffman bracket: empty diagram evaluates to 1 and an
unknot to delta. Put a companion diagram in blackboard framing zero (its
writhe is zero). Let B_j(K) be the bracket of its j zero-framed parallels,
so B_0(K)=1 and B_1(K)=delta E_1(K).

The usual writhe normalization converts the bracket to delta times the
normalized Jones polynomial, in the convention q=-A^2 (the inverse Jones
variable convention gives the same signed values needed here). For coherently
oriented zero-framed parallels their total writhe is zero. Hence when B_j is
divisible by delta^j, E_j=B_j/delta^j evaluates at a primitive eighth root
alpha to the signed Jones determinant e_j. In particular E_1(alpha)=d.

For a fixed oriented pattern diagram the writhe-normalizing monomial is the
SAME for P(K), P(U), and P(R0), when all companions are inserted with zero
blackboard writhe. Indeed the contribution from companion crossings is the
square of the total algebraic winding times the companion writhe, hence zero.
The pattern crossings retain their writhe. We may therefore compare the
unnormalized brackets first and multiply by this common unit at the end.

The polynomial A^4+1 is irreducible over Z, and delta differs from it by a
Laurent unit. Define v_delta by its multiplicity. Divisibility and valuations
below are taken over R, in characteristic ZERO. We only reduce the final
leading coefficients modulo 32 in O = Z[A]/(A^4+1). We never invert 48 or 1776
modulo 32; both are nonunits there.

## 2. Why a small-wrapping pattern has only two skein terms

Choose a meridional disk meeting the pattern in N<=3 points. Resolve crossings
of an annular projection away from the disk. Every state consists of essential
circles (parallel cores z) and contractible circles (factors delta). Resolving
crossings preserves mod-two meridional intersection and cannot create more
than N essential circles: an essential circle needs at least one of the N
intersection points. Contractible circles can use an even number of these
points; essential circles use an odd number. Thus every exponent of z is at
most N and has parity N.

All smoothing coefficients are integral Laurent polynomials: no projectors,
denominators, or change of coefficient field is used. Therefore

    P = a z^2 + b              (even parity),
    P = a z^3 + b z            (odd parity),

with a,b in R. Lower-degree cases are included by a=0. The same expansion
under satellite evaluation sends z^j to B_j(K). This is the elementary
skein-resolution argument, consistent with the usual solid-torus skein module
and satellite substitution formula; it does not rely on equality of skein
degree and geometric wrapping number.

## 3. Two exact ribbon controls force coefficient divisibility

Let S=6_1. Eisermann Example 6.16 gives

    d(S)=9,   e2(S)=49,   e3(S)=1785.

Since S is ribbon, B_2(S)=delta^2 E_2(S) and
B_3(S)=delta^3 E_3(S). Consequently

    v_delta(B_2(S)-delta^2) = 2,       since 49-1=48 != 0;
    v_delta(B_3(S)-delta^2 B_1(S))=3, since 1785-9=1776 != 0.

These exact nonzero numbers, not finite statistical agreement of examples,
are the reason the following universal coefficient restrictions hold.
Write m=c(P)>=1. Because P(U) and P(S) are ribbon, their unnormalized brackets
are divisible by delta^m.

### Even support

From P(U)=a delta^2+b=delta^m C we obtain

    P(K)=a(B_2(K)-delta^2)+delta^m C.

Apply this equality first to S. Its first parenthesis has EXACT valuation two,
while the second term already has valuation at least m. Therefore

    v_delta(a) >= max(0,m-2).

No possible cancellation by the second term evades this inequality. Writing
a=delta^{max(0,m-2)} H proves divisibility of P(K) by delta^m whenever
B_2(K)=delta^2 E_2(K). For m>=2 the leading coefficient is

    H(alpha)(e2(K)-1)+C(alpha).

For m=1 the first term has higher order and the leading coefficient is simply
C(alpha). The formulas hold for Laurent-polynomial coefficient values in O.

### Odd support

P(U)=a delta^3+b delta=delta^m C gives

    b=-a delta^2+delta^{m-1} C,
    P(K)=a(B_3(K)-delta^2 B_1(K))+delta^{m-1} C B_1(K).

Applying this to S, whose first parenthesis has EXACT valuation three, forces

    v_delta(a) >= max(0,m-3).

It follows that P(K) is divisible by delta^m. For m>=3, with
H=a/delta^{m-3}, its leading coefficient is

    H(alpha)(e3(K)-d(K))+C(alpha)d(K).

For m=1 or m=2 the first summand has strictly higher order and the leading
coefficient is C(alpha)d(K).

This is a proof for ALL m and ALL eligible patterns, not a bounded search of
coefficients or links.

## 4. Transfer from a ribbon knot with the same determinant residue

The residues 9^n mod 32, for n=0,1,2,3, are 1,9,17,25. Thus for any
 d(K)=1 (mod 8) there is a ribbon knot R0, a connected sum of n copies of 6_1
(with n=0 meaning the unknot), with d(R0)=d(K) modulo 32. Ribbonness of these
connected sums follows by boundary connecting their ribbon disks.

Eisermann Corollary 6.15 gives

    e2(R0)=d(R0)^2 (mod 32),   e3(R0)=d(R0)^3 (mod 32).

By the hypotheses, the three residues d,e2,e3 of R0 and K agree. The formulas
in section 3 therefore show that the normalized leading Jones quotients for
P(K) and P(R0) agree modulo 32. The common writhe-normalization unit does not
change that equality.

It remains to compare the REQUIRED product of component determinants, rather
than only Jones quotients. For each component P_i of winding w_i the normalized
Alexander satellite formula gives

    d(P_i(K)) = d(P_i(U)) * d(K)  if w_i is odd,
    d(P_i(K)) = d(P_i(U))         if w_i is even.

Negative winding has the same parity, and the normalized knot Alexander
polynomial has value 1 at 1. Hence these component determinants, and their
products, agree modulo 32 for K and R0. Because P(R0) is ribbon, Eisermann's
congruence holds there, and transfers to P(K).

Every knot determinant is odd. Thus the obtained quotient for P(K) is odd
modulo 32, in particular nonzero. Its bracket has EXACT valuation m, and its
normalized Jones nullity is exactly m-1. This proves both conclusions. QED.

## 5. Application to the stored KDG computation

At base commit 6722dc9686d419bb63edefd3cb6024973f4165f6, the saved data give

    d(KDG)=25,
    e2(KDG)=17 (mod 32)=25^2 (mod 32),
    e3(KDG)=6601=9 (mod 32)=25^3 (mod 32).

The three-parallel divisibility was computed exactly. The two-parallel
calculation was modular, so its exact divisibility must NOT be inferred just
from a zero modular remainder. It follows separately for any zero-framed
two-parallel: with opposite component orientations it bounds its zero-framed
annulus, whose Seifert matrix is [0]. Its signed determinant is zero; the
Jones and Alexander determinants agree. Thus its normalized Jones polynomial
vanishes at q=i, and the integral bracket is divisible by delta^2. Reversing
one component does not change that vanishing (indeed the mutual linking is
zero). The saved modular jet then determines its quotient residue 17.

For this KDG application take R0=6_1#6_1#6_1, with determinant 729 congruent to
25 modulo 32. It is not asserted that KDG is concordant or isotopic to R0, or
that their full Jones polynomials coincide. Only the three leading residues
are used.

Subject to the recorded cable identifications, the theorem excludes a hit
from every ribbon pattern of wrapping at most three using THESE Eisermann
tests. It does NOT justify the old blanket claim that all satellite tests
are powerless. An attempted new test needs higher annular skein support or a
different invariant. The first not-excluded support is {1,z^2,z^4}.

## 6. Reproduction and adversarial review

    python3 check_transfer.py --output fresh_results.json

This standard-library checker verifies the saved q-jet divisions, determinant
residues, exact coefficient identities on synthetic polynomial fixtures,
modulo-32 transfer, and four deliberately failing counterfixtures. These are
proof-arithmetic controls, not new knot computations. It refuses overwrites.

Priority review points: the COMMON writhe-normalization unit; integral rather
than complex skein coefficients; the distinction between geometric wrapping
and winding; the exact two-parallel divisibility argument; and the signed
component determinant formula. A failure in any of those requires revising the
claim, not just retaining passing arithmetic tests.

## Sources checked in this pass

1. Michael Eisermann, *The Jones polynomial of ribbon links*, Geometry &
   Topology 13 (2009), 623-660. Definitions and determinant equality in section 2;
   Theorems 1-2; Definition 6.12, Proposition 6.13, Corollary 6.15, Example 6.16.
   The 6_1 values were also inspected in the PDF page image (printed p.31).
   https://pnp.mathematik.uni-stuttgart.de/igt/eiserm/publications/ribbonlinks.pdf
   https://arxiv.org/html/0802.2287
2. Adrian Jimenez Pascual, *On lassos and the Jones polynomial of satellite
   knots*, arXiv:1501.01734v2, 2 February 2015. Introduction, normalized
   Alexander satellite formula; section 2.1, solid-torus skein module;
   section 2.3, skein evaluation and framing correction. The source uses a
   different normalized empty/unknot basis in part of the discussion. Our
   proof explicitly uses the unnormalized empty=1 basis and integral state
   resolution instead; no incompatible basis substitution is imported.
   https://arxiv.org/html/1501.01734
3. SR-Foxy files in inputs.json, pinned at the base commit. Read as existing
   computational evidence; the knot diagrams and original Jones calculations
   were not regenerated here.
