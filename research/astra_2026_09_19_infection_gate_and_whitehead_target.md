# All-winding infection gate, two different gaps, and a nonfibered stabilizer

19 September 2026, Astra. **Counterexample: NOT established. D01 sliceness: UNKNOWN.**

This is an additive response to research/51, cross-checked with research/48--50 and the actual marked-product files. It does not replace their geometric certificates. A new auxiliary target is constructed below; it is not advertised as a newly proved slice/nonribbon knot.

## 1. The satellite statement is verified, with its hypotheses

Hirasawa--Silver--Williams, *When does a satellite knot fiber?*, arXiv:0705.0012, Theorem 2.1 and its proof, give the needed result for a genuine satellite: if P(J) fibers, its winding is nonzero and its companion J fibers. Their definition excludes a pattern contained in a ball, a core pattern, and a trivial companion. Equivalently, the companion torus used in the argument must be essential.

The proof of the winding assertion is particularly clean. At winding zero, the injected Z^2 of the companion torus lies in the kernel of the knot abelianization. For a fibered knot that kernel is a free surface group, which cannot contain Z^2. This replaces the incorrect genus-growth argument and the unverified intersection-count explanation in research/51.

An arbitrary infection curve is not automatically a satellite axis in S^3. In the usual single-axis construction, the axis must be an unknot and the peripheral gluing must be specified; otherwise the resulting ambient manifold need not be S^3. Essentiality alone does not certify distinctness of the resulting knot.

## 2. A stronger derived gate: ALL windings with a slice companion

**Proposition.** Let L=P(J) be a genuine satellite with J a nontrivial smoothly slice knot. If L is fibered, its Alexander polynomial has a nontrivial norm divisor. In particular, Delta_L cannot be irreducible.

**Proof.** The satellite theorem gives w != 0 and J fibered. Since J is nontrivial and fibered, Delta_J is nonconstant. Fox--Milnor gives, in Q[t,t^-1],

    Delta_J(t) = unit * f(t) f(t^-1)

with f a nonunit. The satellite Alexander formula therefore gives

    Delta_L(t) = unit * Delta_P(U)(t) * f(t^w) * f(t^-w).

Both substituted f factors are nonunits because w != 0. This proves the claim. If a nontrivial slice companion has Delta_J=1, it cannot be fibered and is excluded at the earlier step. QED.

This is a corollary derived here from established results, not a claimed new published theorem. It closes the direct slice-companion machine for the campaign's irreducible-Delta pair at every winding, not only winding zero. It does not exclude multi-axis constructions without an essential companion torus, or constructions whose final companion structure disappears.

## 3. Genus and primality: the precise repair

If an UNKNOTTED infection axis is disjoint from an actual minimal-genus Seifert surface F, that surface survives in the infected exterior. At winding zero Delta is unchanged. When the original knot satisfies span(Delta)=2g, these facts sandwich the new genus between g and g, so genus really is preserved. A literal curve on F must first be given an appropriate disjoint push-off and its axis/gluing hypotheses checked.

Primality is not automatic from winding zero. The following lemma supplies the missing argument when the stronger hypotheses hold.

**Lemma.** If Delta_L is a nonunit irreducible polynomial over Q and span(Delta_L)=2g(L), then L is prime, without assuming L fibered.

**Proof.** For L=A#B, Alexander polynomials multiply and genera add. Irreducibility makes one factor polynomial a unit. The inequalities span(Delta_A)<=2g(A) and span(Delta_B)<=2g(B), together with equality for L, force equality in both. The unit-polynomial factor then has genus zero and is an unknot. QED.

An explicit independent regression example is **12n382**:

    monic Delta = t^4 - 5t^3 + 7t^2 - 5t + 1;
    Seifert genus = 2;
    dim HFKhat at top Alexander grading = 3, not 1;
    total HFKhat rank = 35; tau = 1.

The polynomial was checked both as the HFK Euler characteristic and as det(V-t V^T) of an independently computed 20-by-20 Seifert matrix. It is irreducible over Q. HFK computations over F2 and F3 agree on genus, nonfiberedness and total rank. Thus this knot is prime, monic, irreducible-Delta and full-degree, yet nonfibered. It is a regression control, NOT a slice candidate: tau=1 already obstructs sliceness. This check does not purport to reproduce Opus's 59-row DG count.

## 4. Standardization is NOT one universal remaining wall

Abe--Tange, *A construction of slice knots via annulus twists*, arXiv:1305.7492, Theorem 3.1, proves that their associated W(K_n) is standard B4 for every integer n when the seed is a RIBBON knot admitting their annulus presentation. This resolves the standardization question in that stated setting. It does not prove concordance between the nonslice 6_3 seed and A_1(6_3). Their Theorem 5.4 also proves ribbonness for the specified 8_20 family with n>=0, so those are not new candidates.

Oliveira-Smith, *A Dunfield--Gong 4-Sphere is Standard*, arXiv:2603.23717, Theorem 1.1 and Corollary 1.1.1, already proves **18nh00000601 smoothly slice in standard B4**. Theorem 1.2 supplies a fibered handle-ribbon disk. The paper does not prove the knot ribbon. The remaining KDG problem is a ribbon-only obstruction, not the standardization gap asserted in research/51's last section. This agrees with research/50's last section and the older campaign baseline. It is a correction, not a new discovery of the KDG candidate.

Do not infer that an arbitrary punctured homotopy ball is standard merely from standardness of a glued sphere. The cited KDG sliceness corollary uses the trace-embedding setup.

## 5. A disk-exterior transplant gate

**Lemma.** Suppose E is the exterior of a homotopy-ribbon disk and phi:M0(K') -> boundary(E) is a diffeomorphism. Attach a two-handle along the image of the surgery-dual meridian, so that its cocore D' has boundary K' and exterior E up to a collar. If the resulting ambient manifold is standard B4, then D' is homotopy-ribbon.

**Proof.** The map pi1(S3 minus K') -> pi1(M0(K')) is onto. Composing with phi_* and the surjective boundary(E) -> E map remains onto. This is exactly the boundary-knot-exterior map for D'. QED.

Consequently, a literal transplant of a ribbon-disk exterior, even after successful standardization, cannot produce a knot already certified NOT homotopy-ribbon by the campaign's Miyazaki obstruction. This does NOT prove the transplanted knot ribbon. It applies only when the identified cocore exterior really is the original E; a common zero surgery or an abstract group homomorphism alone is not enough.

## 6. An actual auxiliary construction, not another fibered cable

The fixed fibered cable stabilizer in research/49 is excluded. I instead constructed

    R = closure(sigma_1^3 sigma_2^-3), the square knot;
    J = positive untwisted Whitehead double of R;
    T = stored D01 # J.

Regina's whiteheadDouble uses Seifert framing; its definition constructs two opposite-oriented parallel copies and reconnects them by the specified positive clasp. The saved diagrams have 6, 26, 25 and 51 crossings for R, J, D01 and T respectively; these are diagram sizes, not asserted minimal crossing numbers.

J is ribbon: take two disjoint normal parallel copies of a product ribbon disk for R, and attach the Whitehead clasp band in the boundary collar. The resulting connected surface has Euler characteristic 2-1=1 and admits a no-maxima movie. J has Delta=1 and genus one, and is nonfibered. Direct HFK gives genus 1, rank 33, tau=nu=epsilon=0. Direct HFK for T gives genus 5 and rank 5577=169*33, with tau=0 and nonfiberedness; Delta_T=Delta_D01=d(t)^2.

This construction does not satisfy the fibered-upper-knot hypotheses of the specific Agol--Ren argument used in research/49. That is NOT a claim that no other theorem excludes T. It also does not identify J with that note's marked geometric stabilizer.

The useful conditional is exact: **a ribbon certificate for T would prove D01 slice**, since J is ribbon and hence smoothly concordant to the unknot. Combined with the existing D01 nonribbon certificate this would produce a counterexample. Neither a ribbon nor a slice disk for T was obtained here.

A bounded mixed-first-band experiment and its replay code are saved in results/astra_2026_09_19_infection_gate/. Bounds apply to one pinned diagram and one generated set only. Passing an Alexander-rank test is not a slice or ribbon certificate.

## Sources read

- Hirasawa--Silver--Williams, Theorem 2.1 and proof: https://arxiv.org/abs/0705.0012
- Abe--Tange, Theorem 3.1, Lemma 2.5, Theorem 5.4: https://arxiv.org/abs/1305.7492
- Oliveira-Smith, Theorems 1.1, 1.2 and Corollary 1.1.1: https://arxiv.org/abs/2603.23717
- Agol--Ren, Theorems 1.7 and 1.13, specifically their fibered hypotheses: https://arxiv.org/abs/2603.10884

Repository inputs actually read include research/48--51; results/astra_2026_09_18_marked_annulus_construction/GEOMETRY.md and ONE_HANDLE_UPDATE.md; results/astra_2026_09_18_mixed_handle_gate/MIXED_HANDLE.md; and data/knots/AbeTagami_D_0_1.json at e5491286f233d4edcf6603ecba44cf24fbab2341 (blob a7f0d719e295bf50598886392233128749fa6904).
