# A proposed all-degree transfer theorem for two Eisermann tests

17 September 2026 UTC. **NO COUNTEREXAMPLE.**

**Status: complete proposed proof supplied; independently unreviewed.** This is an original derivation in this research pass, not a cited published theorem and not a claim of publication novelty. The finite calculations and direct controls below test the argument; they do not replace its all-degree proof. A second mathematical reader should attack the proof before the campaign treats the entire test family as closed. No previous result or research file is overwritten.

Input repository commit: `0eb81a1a15147b2059b9028d0bbc0f4173f0ad33`.

## 1. Statement and exact scope

**Proposed theorem.** Let K be smoothly slice in standard B4. Let P be an oriented, m-component link pattern in the zero-framed solid torus, m>=1, such that P(U) is a ribbon link. Then P(K) has normalized Jones nullity exactly m-1, and its reduced Jones determinant satisfies

    det_V(P(K)) = product_i det(P_i(K))  (mod 32).

The determinants of the components are signed Jones/Alexander determinants in Eisermann's convention. There is no geometric-wrapping bound. All computations are at the primitive eighth root in the Kauffman variable, corresponding to q=i.

If correct, these TWO necessities cannot prove nonribbonness of an already smoothly slice companion by applying a ribbon pattern. This includes all zero-framed parallels. It does not prove any satellite ribbon, does not decide Slice–Ribbon, and does not settle the corresponding conditions for arbitrary slice links. It also does not address all colored-Jones ideals, higher coefficients, Khovanov invariants, other roots, arbitrary surgery constructions, or other satellite obstructions.

The proof has three parts: transfer full parallel divisibility through a ribbon stabilization; transfer the leading parallel congruences; then control every coefficient of a ribbon pattern using a family of ribbon companions.

## 2. Conventions and imported facts

Let R=Z[A,A^-1], h=A^4+1 and t=delta=-A^2-A^-2. The elements t and h differ by a Laurent unit. Since h is irreducible, use its valuation v, normalized by v(t)=1. Work first in the discrete valuation ring obtained by localizing Q[A,A^-1] at (h). This allows rational constants, but **not** inversion of h. Divisibility of an integral Laurent polynomial by h^r over Q implies the same integral divisibility by Gauss's lemma. Only after this step do we reduce leading values modulo 32 in Z[alpha], alpha^4=-1. Constants with odd denominator may be reduced modulo 32; constants with even denominator may not.

Use empty-link bracket 1 and unknot bracket t. Take each companion diagram to have blackboard writhe zero. B_j(K) denotes the unnormalized bracket of its zero-framed j-parallel; B_0=1. In the convention q=-A^-2, t=q+q^-1. Writhe normalization is trivial on the coherently oriented zero-framed parallel. If t^j divides B_j, write

    E_j(K)=B_j(K)/t^j,     e_j(K)=E_j(K)(alpha),     e_0=1.

Thus e_1=d(K), the signed knot determinant. When full nullity holds, e_j is the reduced Jones determinant of the j-parallel. Inversion of the Jones variable does not change this reduced value: both the numerator parity and the corresponding unlink factor change by the same sign.

We use the following external results, separately from our deductions.

**[E] Eisermann.** Theorems 1 and 2 give full Jones nullity and the mod-32 product congruence for ribbon links. Definition 6.12 and Proposition 6.13 say that P(U) ribbon and J ribbon imply P(J) ribbon. Corollary 6.15 applies this to parallels. Example 6.16 supplies, for S=6_1,

    e_1(S)=9, e_2(S)=49, e_3(S)=1785.

The universal upper bound for Jones nullity of an m-component link is m-1 (Lemma 1).

**[L] Stable ribbon fact.** For every smoothly slice knot K there exists a ribbon knot J such that X=K#J is ribbon. Livingston's survey, section 2.1 after Definition 2.3, records this observation of Casson; Eisermann section 7.1 also states it. This is a knot statement. We do not assume a corresponding assertion for arbitrary slice links.

**[MS] Colored connected-sum and cabling identities.** Put S_0(z)=1, S_1(z)=z and S_{r+1}(z)=zS_r(z)-S_{r-1}(z). These Chebyshev skein elements are the irreducible colors. Set

    c_rj = [z^j] S_r(z),
    C_r(K) = sum_j c_rj B_j(K),
    D_r = S_r(t).

The zero-framed identities are

    C_r(K#J) = C_r(K) C_r(J) / D_r,
    B_n(K) = sum_{r=n mod 2} mu_nr C_r(K),
    mu_nr = binom(n,(n-r)/2) - binom(n,(n-r)/2-1).

The second sum is over 0<=r<=n; out-of-range binomials vanish. The normalized colored scalar multiplies under composition of (1,1)-tangles, and its closure multiplies by D_r. Morton–Strickland Theorem 1.1 and Corollary 1.2, printed p.87, give this principle. Their Theorem 2.1 and Corollaries 2.2–2.3, pp.92–93, give cabling as tensor product. The fundamental SU(2) decomposition, or the Chebyshev recurrence directly, gives the stated multiplicities. The rational formulas are used generically, before taking the root limit; division by D_r at its zero is not an evaluation rule.

**[A] Integral skein and determinant formulas.** The annular bracket is in R[z], with finite support of one parity. This follows by resolving crossings into essential and contractible circles; no Jones–Wenzl denominators are introduced into the PATTERN coefficients. For each pattern component of winding w,

    d(P_i(K)) = d(P_i(U)) d(K)  if w is odd,
    d(P_i(K)) = d(P_i(U))       if w is even.

This is the normalized Alexander satellite formula evaluated at -1. Use Delta(1)=1 and its symmetric normalization; negative winding has the same parity. Smooth sliceness implies the signed determinant is an odd square, so d(K)=1 mod 8.

For any fixed oriented pattern, the writhe-normalizing monomial is the same for P(K), P(U), and P(J) when companions have writhe zero. Companion crossings contribute the square of the total algebraic winding times the companion writhe. Consequently all bracket comparisons below may be normalized using one common Laurent unit. The number of components, not the wrapping number, determines the required power of t.

## 3. The filtered connected-sum kernel

Define the universal rational coefficients

    T_nj(J) = sum_r mu_nr c_rj C_r(J)/D_r,

so that B_n(K#J)=sum_j T_nj(J) B_j(K), with j of the same parity as n.

**Kernel lemma.** If v(B_k(J))>=k for all k<=n, then

    v(T_nj(J)) >= n-j.

The diagonal has leading value T_nn(J)(alpha)=1 for even n and d(J) for odd n. These are valuation units over Q because a knot determinant is nonzero.

Here is a coefficientwise, all-n proof. Substituting B_k(J)=t^k E_k(J), it suffices to show

    v(Q_njk(t)) >= n,
    Q_njk(t)=t^(j+k) sum_r mu_nr c_rj c_rk/S_r(t),                 (1)

for every eligible j,k. This is a statement of rational functions of t; the E_k are independent coefficients in the valuation ring.

Define a polynomial in r by

    P_s(r)=binom((r+s)/2,s).

It has degree s and leading coefficient 1/(2^s s!). For nonnegative r,s of the same parity,

    c_rs=(-1)^((r-s)/2) P_s(r),
    P_s(-r-2)=(-1)^s P_s(r).

If s>r in the relevant ranges then P_s(r)=0. The P_s of a fixed parity form a basis for polynomials of that degree bound with the corresponding parity under reflection r -> -r-2. This is the usual even/odd polynomial decomposition after translating r to r+1.

The Chebyshev decomposition z^n=sum_r mu_nr S_r(z) implies that the functional

    L_n(f)=sum_r mu_nr (-1)^((r-epsilon)/2) f(r), epsilon=n mod 2,

annihilates every reflection-parity polynomial of degree <n and parity epsilon. Indeed it annihilates P_s for s<n by comparing the coefficient of z^s. Its top-degree value is

    L_n(r^n)=(-1)^((n-epsilon)/2) 2^n n!.                       (2)

For even r,

    S_r(t)=(-1)^(r/2) sum_l (-1)^l P_(2l)(r)t^(2l).

The constant term after removing the sign is 1. Recursively inverting this series, its coefficient of t^(2l) is a reflection-even polynomial in r of degree at most 2l. Therefore the coefficient of t^(j+k+2l) in (1) is, up to a constant sign, L_n applied to a reflection-even polynomial of degree at most j+k+2l. It vanishes if that exponent is <n.

For odd r,

    S_r(t)=(-1)^((r-1)/2) t P_1(r)
           [sum_l (-1)^l (P_(2l+1)(r)/P_1(r))t^(2l)],
    P_1(r)=(r+1)/2.

Each ratio P_(2l+1)/P_1 is a reflection-even polynomial of degree 2l, and its l=0 term is 1. Reciprocal coefficients retain degree at most 2l. Since P_j and P_k are both odd under the reflection, P_j P_k/P_1 is a reflection-odd polynomial of degree j+k-1. Thus the coefficient of t^(j+k-1+2l) in (1) is L_n applied, up to a sign, to a reflection-odd polynomial of degree at most that exponent. It also vanishes below n. This proves (1) in both parities, and hence the kernel lemma.

For the diagonal, T_nn=C_n(J)/S_n(t). For even n, the numerator and denominator have the same nonzero constant term. For odd n, their leading t terms differ by the factor E_1(J)(alpha)=d(J). This proves the stated units.

**Important:** polynomial cancellations take place in characteristic zero. The factors (r+1)/2 in the odd case may be even. They are not inverted modulo 32. Section 5 separately proves that the FINAL leading law has odd denominators only.

## 4. Consequence for all parallels of a smooth slice knot

Choose ribbon J with X=K#J ribbon by [L]. Eisermann gives v(B_k(J))>=k and v(B_k(X))>=k for every k. Induct on n, starting with B_0=1 and B_1=t times the normalized knot Jones polynomial.

In

    B_n(X)=T_nn(J) B_n(K) + sum_(j<n) T_nj(J) B_j(K),

every lower summand has valuation at least n by the kernel lemma and the induction hypothesis. The left side also has valuation at least n, and T_nn is a unit. Therefore v(B_n(K))>=n. Gauss's lemma makes this an integral divisibility statement in R. The universal upper bound gives exact normalized nullity n-1.

This proves the proposed all-parallel nullity statement for SMOOTH SLICE knots, not for all knots. In particular, it does not use a broader claim whose proof is unfinished in the 2025 report mentioned in section 9.

## 5. The leading connected-sum laws and 2-integrality

Suppose both factors have the full divisibilities. Define formal series

    F_K(x)=sum_(a>=0) (-1)^a e_(2a)(K) x^(2a)/(2a)!,
    G_K(x)=sum_(a>=0) (-1)^a e_(2a+1)(K) x^(2a)/(2a+1)!.

These are formal exponential series encoding coefficients, not analytic claims. The leading laws are

    F_(K#J)=F_K F_J / cos(x),
    G_(K#J)=G_K G_J / (sin(x)/x).                             (3)

For completeness, the coefficient extraction from section 3 is as follows. In the even case the top-degree part of the reciprocal series is the reciprocal of cos(rt/2). In the odd case, after the t P_1 factor is removed, it is the reciprocal of sin(rt/2)/(rt/2). Using (2), all terms of degree below n disappear. The coefficient multiplying e_j(K)e_k(J) in e_n(K#J) is

    (-1)^l n!/(j! k!) * [x^(2l)] sec(x),      n=j+k+2l, j,k even;
    (-1)^l n!/(j! k!) * [x^(2l)] x/sin(x),   n=j+k-1+2l, j,k odd. (4)

Equation (4) is exactly (3). It provides explicit formulas without an unjustified limiting interchange. Higher t coefficients of E_j(K), E_k(J) cannot contribute, because their kernel already vanishes to order n.

Examples, with a_j=e_j(K) and b_j=e_j(J), are

    e_2(K#J)=a_2+b_2-1,
    e_3(K#J)=a_3 b_1+a_1 b_3-a_1 b_1,
    e_4(K#J)=a_4+b_4+6(a_2-1)(b_2-1)-1.

We next prove that each polynomial (4) has coefficients in Z_(2), the rationals with odd denominator.

For the even law, (2l)![x^(2l)]sec(x) is an Euler integer. The remaining coefficient is the multinomial n!/(j!k!(2l)!), hence integral.

For the odd law, put u_l=(2l)![x^(2l)]x/sin(x). The reciprocal identity gives, for n>0,

    sum_(j=0)^n (-1)^(n-j) binom(2n+1,2j) u_j = 0.

The coefficient of u_n is 2n+1, odd. Starting with u_0=1, this proves u_n is 2-integral. The other factor in (4) is

    n!/(j! k! (2l)!),  n=2a+1, j=2b+1, k=2c+1, a=b+c+l.

By the factorial 2-adic valuation formula, its valuation is

    s_2(b)+s_2(c)+s_2(l)-s_2(a) >= 0,

where s_2 counts binary ones; the inequality follows from binary addition. Therefore (4) is 2-integral, even though it need not be an ordinary integer coefficient. For instance, the fifth law has denominator 3, not a power of 2. Only these final 2-integral polynomials are reduced modulo 32.

## 6. All-parallel congruences for smooth slice knots

Write H_n(a,b) for the polynomial (4). Its coefficient on the top variable a_n is 1 for even n and b_1 for odd n. All other terms use lower a_j. The unknot has e_j(U)=1, so H_n(a,1)=a_n.

Set a_j=d^j and b_j=e^j and denote the resulting scalar polynomial by h_n(d,e). Since h_n(d,1)=d^n and h_n(1,e)=e^n,

    h_n(d,e)-(de)^n is divisible by (d-1)(e-1)

in Z_(2)[d,e]. In particular it vanishes modulo 32 whenever d and e are 1 modulo 8. In fact the displayed factor gives divisibility by 64, but no stronger general ribbon congruence is inferred.

Again choose ribbon J and X=K#J. The determinants d(K) and d(J) are odd squares, hence 1 modulo 8. Eisermann gives

    e_n(J)=d(J)^n (mod 32),
    e_n(X)=(d(K)d(J))^n (mod 32).

Inductively suppose e_j(K)=d(K)^j modulo 32 for j<n. Compare H_n(e(K),e(J)) with h_n(d(K),d(J)). Their difference is

    e_n(K)-d(K)^n                    for even n,
    d(J) [e_n(K)-d(K)^n]             for odd n.

The left side is zero modulo 32, and d(J) is an odd unit. Thus

    e_n(K)=d(K)^n (mod 32) for every n.                        (5)

This is a proof using stabilization, the exact filtered kernel, and 2-integrality. It is not a statistical generalization from the KDG values through n=4.

## 7. Coefficient restrictions on every ribbon pattern

Let P=sum_j a_j z^j in R[z] be a ribbon pattern with m components. Its finite support has one parity epsilon. Extend missing coefficients by zero and let j range over epsilon,epsilon+2,...,epsilon+2N. Put S_p=#^p S, S=6_1, with S_0=U. Each S_p is ribbon, so P(S_p) is ribbon by [E]. Consequently

    sum_j E_j(S_p) [a_j t^j] = B(P(S_p)) lies in t^m R.        (6)

Use p=0,...,N. The coefficient matrix in (6) is invertible at alpha. Here is a proof that does not require computing arbitrarily many Jones polynomials.

For even j=2a, (3) gives

    F_(S_p)=cos(x) [F_S(x)/cos(x)]^p.

The number e_(2a)(S_p) is a polynomial in p of exact degree a with leading coefficient

    (2a)! (e_2(S)-1)^a / (2^a a!).                            (7)

For odd j=2a+1,

    G_(S_p)=(sin(x)/x) [G_S(x)/(sin(x)/x)]^p.

The number e_(2a+1)(S_p)/d(S)^p is a polynomial in p of exact degree a, with leading coefficient

    (2a+1)! (e_3(S)/d(S)-1)^a / (6^a a!).                    (8)

These formulas follow by taking the degree-a term in p when expanding a power of a series with nonzero x^2 coefficient. The required coefficients are nonzero because e_2(S)-1=48, e_3(S)-d(S)=1776, and d(S)=9.

The evaluation matrix of polynomials of degrees 0,...,N at distinct integers p=0,...,N has determinant equal to the product of leading coefficients times the Vandermonde. In the odd case there is the additional nonzero factor d(S)^(N(N+1)/2). Therefore the matrix of e_j(S_p) is nonsingular over Q, and the matrix of E_j(S_p) is invertible in the characteristic-zero valuation ring.

Solving (6) in that ring yields

    v(a_j t^j)>=m, hence v(a_j)>=max(0,m-j).                  (9)

This argument does NOT invert the Vandermonde determinant modulo 32. Its factors 48 and 1776 need not be units there. It establishes integral coefficient divisibility first, by Gauss's lemma. That distinction is essential.

## 8. Finish the satellite transfer

Let K be smooth slice. Sections 4 and 6 supply B_j(K)=t^j E_j(K) and (5) for all j. Equation (9) implies every term in P(K)=sum_j a_j B_j(K) has valuation at least m.

At order exactly m, only j<=m contribute. For those indices set a_j=t^(m-j) H_j with H_j in R. Thus

    [B(P(K))/t^m](alpha)=sum_(j<=m) H_j(alpha) e_j(K).         (10)

Select a ribbon R0=#^r S with d(R0)=d(K) modulo 32: r in {0,1,2,3} suffices because 9^r has residues 1,9,17,25. By (5), every e_j(K) equals e_j(R0) modulo 32. Equation (10), with the common writhe-normalizing unit included, shows the reduced Jones quotients of P(K) and P(R0) agree modulo 32.

The signed determinant product of the components also agrees, by [A]'s winding-parity formula. P(R0) is ribbon, so its congruence transfers to P(K). The required product is odd, hence nonzero; the quotient cannot vanish. This proves exact valuation m, or normalized Jones nullity m-1, and the proposed theorem.

The argument has not assumed an embedding of a disk for P(K) with no maxima. It establishes two numerical necessities only.

## 9. Actual computations, source checks, and limitations

`check_general_transfer.py` independently expands the rational Chebyshev kernel by exact series division and compares its leading terms with (4). It checks all relevant indices through n=20, including lower-term cancellation, leading laws, odd-denominator legality, scalar congruences, unit/diagonal terms, and synthetic Vandermonde controls. The saved run has 4,832 passing checks in approximately 0.10 seconds. The 20 Vandermonde fixtures use synthetic uncomputed higher seed values and are explicitly not knot calculations. Twenty-two negative checks reject a perturbation of the top invariant, division by 2 modulo 32, or an ineligible determinant fixture.

A DIFFERENT route checks two connected-sum predictions geometrically: the pass02 standalone planar-diagram cabler and exact C++ frontier evaluator were applied to S#S. The new 80-crossing two-parallel gives e_2=97, and the new 180-crossing three-parallel gives e_3=32049. Both exactly match (4), with exact divisibility checked. This is independent of the colored connected-sum algebra, but shares the previously audited cabler/frontier engine. It is not an independent topology library or proof assistant.

An optional 320-crossing four-parallel control failed with `std::bad_alloc` inside the 2 GiB address-space cap. No value was produced. The algebraic prediction 53185 for that control is **NOT** reported as a computed knot invariant. The failure and partial log are preserved, and it was not rerun. No fifth-parallel target was attempted. No KDG target, settled s/HKL/Floer calculation, or broad band sweep was repeated.

The 2025 Texas A&M report *Connections between common slice obstructions and the Eisermann ribbon obstruction* by Megan du Preez, Bryan Silva, Eric Yu and Sherry Gong prints a stronger all-knot parallel assertion as Theorem 5.10, but its proof on printed p.18 is marked WIP. That page was inspected directly. We do not cite that assertion as an established theorem. Our proof is restricted to smooth slice companions and does not depend on it.

The important independent-review targets are: (i) zero-framed irreducible-color normalization; (ii) coefficientwise filtered-kernel proof for odd colors; (iii) all-degree 2-integrality rather than cancellation after an illegal modular division; (iv) matrix invertibility used over Q at the root before returning to integral pattern coefficients; and (v) the common writhe and signed component determinant conventions. A gap in one of these must be fixed or the global claim downgraded. Passing finite checks does not license ignoring a gap.

## 10. Campaign consequence, if the proof survives review

Do not allocate a fifth-parallel or high-wrapping ribbon-pattern Jones search for KDG on the expectation that these two necessities can fail. Return effort to constructing the missing smooth concordance for D01, or to a genuinely different ribbon-specific obstruction for a certified-slice target. This is not a global exclusion of all satellite approaches.

The next action is ONE adversarial mathematical audit of this proof, not another cabling computation. Opus should continue any actual nonlocal disk construction already in progress; a finite audit of this separate lane should not replace geometry with an endless review loop.

## Sources (precise use; accessed 17 September 2026 UTC)

1. Michael Eisermann, *The Jones polynomial of ribbon links*, Geometry & Topology 13 (2009), 623–660. Theorems 1–2; Lemma 1; Definition 6.12; Proposition 6.13; Corollary 6.15; Example 6.16; section 7.1. Author PDF printed pp.30–31 inspected, including the example and stable-ribbon observation. https://pnp.mathematik.uni-stuttgart.de/igt/eiserm/publications/ribbonlinks.pdf ; arXiv:0802.2287.
2. H. R. Morton and P. Strickland, *Jones polynomial invariants for knots and satellites*, Mathematical Proceedings of the Cambridge Philosophical Society 109 (1991), 83–103. Theorem 1.1, Corollary 1.2 (p.87), Theorem 2.1 and Corollaries 2.2–2.3 (pp.92–93). Actual paper pages 87 and 92 inspected as images; not inferred from an abstract. Author-uploaded PDF: https://www.researchgate.net/profile/Hugh-Morton/publication/232015440_Jones_polynomial_invariants_for_knots_and_satellites/links/5ba287fd92851ca9ed15cead/Jones-polynomial-invariants-for-knots-and-satellites.pdf . Liverpool preprint mirror returned 406; this did not prevent reading the paper from the author upload.
3. Charles Livingston, *A survey of classical knot concordance*, Handbook of Knot Theory (2005), 319–347; arXiv:math/0307077v4. Section 2.1 immediately after Definition 2.3 gives the stable-ribbon observation in the smooth category. Theorem 2.6 and section 3.3 support the metabolic/Fox–Milnor determinant fact. https://arxiv.org/pdf/math/0307077 . The fetched file's arXiv banner says 26 Nov 2004, while a body date is rendered as 2024; neither date is used as a new-result claim.
4. Adrian Jimenez Pascual, *On lassos and the Jones polynomial of satellite knots*, arXiv:1501.01734v2 (2015). Introduction for the normalized Alexander satellite formula; section 2 for the solid-torus skein/cabling conventions. The proof here uses its own integral empty=1 state-sum basis, rather than substituting between incompatible normalized bases. https://arxiv.org/pdf/1501.01734 . The HTML fetch failed in this pass; the PDF introduction was then read directly. The conventions were also checked in the previous low-wrapping audit.
5. Megan du Preez, Bryan Silva, Eric Yu and Sherry Gong, *Connections between common slice obstructions and the Eisermann ribbon obstruction*, Texas A&M REU report, July 2025. Theorem 5.10, printed p.18, has proof WIP; NOT used as an established input. https://artsci.tamu.edu/mathematics/_files/_docs/reu/results/2025/dupreez-silva-yu-report.pdf .
6. SR-Foxy at the input commit: `results/astra_2026_09_17_satellite_plan/LOW_WRAPPING_LEMMA.md`, `FOUR_STRAND_GATE.md`, and `results/astra_2026_09_17_overnight/pass02_0410_four_parallel/`. These supplied the prior test definitions, numerical controls and portable engine. No exhaustive repository audit was performed.
