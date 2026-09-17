# Pass 01 — adversarial audit of the low-wrapping transfer lemma

17 September 2026 UTC. **NO COUNTEREXAMPLE.** This is an independent proof audit of `results/astra_2026_09_17_satellite_plan/LOW_WRAPPING_LEMMA.md`; it does not regenerate the stored KDG cable diagrams or their Jones jets.

## Verdict

The low-wrapping transfer lemma **survives this audit**, conditional on the previously recorded KDG cable identifications and values. I found one terminology point that should be kept explicit but does not change the proof: in the two-parallel argument, the quantity that vanishes before dividing by the unlink factor is the **ordinary link determinant** `V(L)(i)=Delta(L)(i)`, not Eisermann's reduced **Jones determinant** `det V(L)`. The latter is the quotient after removing the Jones-nullity factor and need not vanish.

This audit checked the five load-bearing points requested in the overnight plan.

## 1. Common writhe normalization

Let an oriented pattern meet a fixed meridional disk in signed points `s_1,...,s_N`, `s_j in {+1,-1}`, and let `W=sum s_j` be the algebraic winding of the whole oriented pattern. At a companion crossing of sign `epsilon`, the satellite diagram contains one crossing for each ordered pair of local pattern strands. Its total signed contribution is

`epsilon * sum_{j,k} s_j s_k = epsilon * W^2`.

Therefore

`w(P(K)) = w(P in the standard solid torus) + W^2 w(K_diagram)`.

Choosing the companion diagram with blackboard writhe zero makes the writhe-normalizing monomial identical for `P(K)`, `P(U)`, and the ribbon reference `P(R0)`. This works for multicomponent patterns as well: only the total signed meridional intersection enters the sum. It justifies comparing the unnormalized annular brackets first and applying one common unit at the end.

No claim is made that an arbitrary pre-existing diagram already has writhe zero; Reidemeister-I curls may be added before taking its zero-framed satellite. The satellite framing must remain the zero framing throughout.

## 2. Integral annular skein support

The proof uses the ordinary Kauffman bracket skein module of the solid torus over `Z[A,A^-1]`, not Jones-Wenzl projectors or a localized coefficient ring. Resolving crossings away from a meridional disk preserves the `N` intersection points with that disk. Each essential state circle has odd mod-2 intersection with the disk and each contractible state circle has even intersection. Hence the number `j` of essential circles obeys

`0 <= j <= N`,  `j == N (mod 2)`.

For geometric wrapping `N<=3`, the annular bracket therefore has support contained in `{1,z^2}` (even) or `{z,z^3}` (odd), with Laurent-polynomial coefficients in `Z[A,A^-1]`. Under a zero-framed companion embedding, `z^j` evaluates to the bracket `B_j(K)` of the `j` zero-framed parallels. This is the precise support statement needed by the transfer proof.

## 3. Exact two-parallel divisibility

Let `L=K^2` be the zero-framed two-parallel. Give its two components opposite orientations. They cobound the obvious annulus on the boundary of a tubular neighborhood of `K`. The annulus has a one-generator Seifert matrix `[0]`, so its ordinary signed link determinant vanishes:

`Delta(L)(i)=0`.

Eisermann states that the ordinary Jones and Alexander specializations agree at `q=i`, so `V(L)(i)=0`. His general upper bound gives `null V(L)<=1` for a two-component link. Consequently

`null V(K^2)=1`

**exactly**, for every knot `K` and its zero-framed two-parallel. Since the unnormalized bracket differs from the normalized Jones polynomial by one factor `delta=q+q^-1` and a writhe unit, `B_2(K)` is divisible by `delta^2` exactly in characteristic zero. Thus the saved modular KDG two-parallel jet may legitimately be divided by `delta^2`; no modular-zero-implies-exact-zero inference is required.

Reversing one component changes the oriented Jones normalization only by the usual linking-number monomial; the zero-framed parallel has mutual linking number zero, so the coherent and annulus orientations give the same value relevant here.

Terminology correction: the reduced quotient after this factor is Eisermann's `det V(K^2)` and can be nonzero (for `6_1` it is 49). Do not call that reduced determinant zero.

## 4. Coefficient-divisibility argument

For even support `P=a z^2+b`, ribbonness of `P(U)` gives

`a delta^2+b = delta^m C`,

where `m` is the number of components. For the ribbon control `S=6_1`, Example 6.16 gives reduced two-parallel Jones determinant 49, hence

`B_2(S)-delta^2 = delta^2(E_2(S)-1)`

has **exact** `delta`-valuation 2 because `(E_2(S)-1)(alpha)=48 != 0`. Since `P(S)` is ribbon by Eisermann Proposition 6.13, its bracket has valuation at least `m`. If `v_delta(a)+2<m`, the `a` term has strictly smaller valuation than the `delta^m C` term and cannot cancel. Hence `v_delta(a)>=max(0,m-2)`.

The odd-support proof is identical with

`B_3(S)-delta^2 B_1(S)=delta^3(E_3(S)-E_1(S))`

and Example 6.16 values `1785-9=1776 != 0`, yielding `v_delta(a)>=max(0,m-3)`. This step is over the integral Laurent ring; 48 and 1776 are never inverted modulo 32.

## 5. Signed component determinants

Use the symmetric, normalized knot Alexander polynomial with `Delta(1)=1`. The satellite formula is

`Delta_{P_i(K)}(t)=Delta_{P_i(U)}(t) Delta_K(t^{w_i})`,

where `w_i` is the algebraic winding of component `P_i`. At `t=-1`, even `w_i` contributes `Delta_K(1)=1`, while odd `w_i` contributes the signed knot determinant `Delta_K(-1)`. Thus for two companions whose signed determinants agree modulo 32, every component determinant, and therefore the whole product required by Eisermann Theorem 2, agrees modulo 32. Negative winding has the same parity and causes no extra companion-dependent factor.

For the bracket leading coefficient, the common writhe monomial from section 1 is a unit independent of the companion. Matching the `d,e2,e3` residues with a ribbon reference therefore matches the normalized Jones quotient modulo 32. Since the ribbon reference quotient is odd, the target leading coefficient is nonzero; the Jones nullity is exactly `m-1`, not merely at least that value.

## Primary-source checks

Michael Eisermann, *The Jones polynomial of ribbon links*, Geometry & Topology 13 (2009), 623–660:

- Theorem 1: every `n`-component ribbon link has Jones nullity exactly `n-1`.
- Theorem 2: the reduced Jones determinant is congruent mod 32 to the product of signed component determinants.
- Definition 6.12 / Proposition 6.13: `P(U)` ribbon is exactly the ribbon-pattern condition used to infer `P(S)` ribbon for a ribbon companion.
- Corollary 6.15 / Example 6.16: zero-framed cables of a ribbon knot are ribbon; for `6_1`, `det=9`, `det V(K^2)=49`, `det V(K^3)=1785`.

Primary text checked 17 September 2026 at:
`https://pnp.mathematik.uni-stuttgart.de/igt/eiserm/publications/ribbonlinks.pdf`
and `https://arxiv.org/abs/0802.2287`.

The Alexander satellite formula was cross-checked in standard normalized form; it is also quoted in the SR-Foxy source `LOW_WRAPPING_LEMMA.md` via A. Jimenez Pascual, arXiv:1501.01734.

## Consequence

Do not enumerate wrapping-at-most-three ribbon patterns for these two Eisermann tests. The first clean pattern outside the theorem is already available without introducing a Bing diagram: the **four-parallel pattern `P=z^4`**. Its unknot satellite is the four-component unlink, so it is a ribbon pattern, and its annular leading coefficient is exactly `a=1`. The next checkpoint develops this direct four-parallel gate.
