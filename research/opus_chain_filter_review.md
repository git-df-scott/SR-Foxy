# External model critique: chain filter

This is advisory model output, not a source or a proof. Its suggestions require independent checking.

## Prompt

Give a skeptical mathematical audit, at most 900 words, of this proposed necessary condition for ribbon concordance K -> J. No tools; identify hidden hypotheses or counterexamples. Zemke 2019 Theorems 1.1 and 1.7 say the hat HFK map is injective and there is a bifiltered Maslov-degree-zero chain map on CFK-infinity with a filtered homotopy left inverse. SnapPy/Szabo HFK Calculator complex=True returns the simplified knot complex over R=F2[U,V]/(UV); generators have (Alexander A, Maslov M) and all horizontal/vertical differential arrows, with mixed UV terms omitted. I propose to test existence of a homogeneous degree-(A=0,M=0) R-linear chain map F from this R-complex of K to that of J, whose reduction mod(U,V) is injective in every (A,M) grade. A possible term x_i -> U^a V^b y_j has a=(M_j-M_i)/2, b=A_i-A_j+a, so require a,b nonnegative integers and ab=0. Differential exponents use a=(M_j-M_i+1)/2 with the same b. The equation d_J F + F d_K=0 is linear over F2 in the finitely many allowed coefficients. Hat-injectivity is finitely many nonzero-vector constraints per grade, solvable by SAT. A SAT solution is merely a necessary-test pass, never a concordance certificate. UNSAT would exclude K -> J if the model is justified. Is the passage from bifiltered CFK-infinity to this UV=0 Rees complex correct? Are absolute grading shifts and HFK map reductions as assumed? Could the two asserted maps fail to be compatible? Are there representation issues from HFK Calculator simplified complexes? We will control with every explicitly generated birth+fusion K0->J movie: own-source maps must exist. Advise whether to label UNSAT a rigorous necessary obstruction or an exploratory check pending a more precise functorial reference. Do not assume your answer solves Slice-Ribbon.


## Response

## Verdict

The logical skeleton is sound; the implementation assumptions are where the risk lives. **Label UNSAT an exploratory obstruction, not a theorem** — with one exception noted at the end. Below, what survives scrutiny and what does not.

## What is actually correct

**The quotient step is fine.** Zemke's $F_C$ is $\mathbb{F}[U,V]$-equivariant on the free complex $\mathit{CFK}_{\mathbb{F}[U,V]}$. Tensoring with $R=\mathbb{F}[U,V]/(UV)$ is functorial, so a ribbon concordance yields an $R$-linear chain map $\bar F = F_C\otimes R$, and the homotopy left inverse of Thm 1.7 descends too. Nonexistence over $R$ therefore does imply nonexistence over $\mathbb{F}[U,V]$. Discarding mixed terms loses information (that is exactly the gap between $\mathit{CFK}$ and its immersed-curve shadow) but only *weakens* the test — it cannot manufacture a false UNSAT.

**The grading arithmetic is self-consistent** *in the convention $M=\mathrm{gr}_w$*, i.e. $\deg U=(-2;A{-}1)$, $\deg V=(0;A{+}1)$, $\deg\partial=(-1;0)$. Then $a=(M_j-M_i)/2$, $b=A_i-A_j+a$ for $F$, and $a=(M_j-M_i+1)/2$ for $\partial$ — both as you state. Note the consequence: each ordered pair $(i,j)$ admits **at most one** monomial, so your SAT instance is one bit per pair. Good.

**Your injectivity test is homotopy-invariant**, which is the non-obvious point in your favor. If both complexes are *reduced*, every differential arrow carries a positive power of $U$ or $V$, so $C/(U,V)$ has zero differential and equals $\widehat{\mathit{HFK}}$ on the nose; and any homotopy $dh+hd$ lands in $(U,V)$. So "$\bar F \bmod (U,V)$ injective" is well defined on homotopy classes and is literally Thm 1.1. That is a genuine win.

## Hidden hypotheses (each a potential false UNSAT)

1. **Reducedness.** Everything above collapses if the calculator returns any coefficient-1 arrow. Then $C/(U,V)\neq\widehat{\mathit{HFK}}$, chain-level injectivity is the wrong condition, and it is *stronger* than Zemke's — a manufactured obstruction. Verify no unit arrows before trusting any UNSAT.
2. **Grading convention.** If the tool reports $\mathrm{gr}_z$, $\delta=M-A$, or a symmetrized Maslov instead of $\mathrm{gr}_w$, your $a$ formula silently permutes the allowed monomials and UNSAT becomes meaningless. Also check the Alexander sign convention and whether the tool returns $K$ or its mirror ($U\leftrightarrow V$).
3. **Absolute normalization must agree across the two knots.** $F_C$ preserves both absolute gradings only because the concordance has $\chi=0$ *and* carries Zemke's standard two-arc decoration. A different decoration shifts by powers of $U,V$. Confirm the tool normalizes both complexes identically (unknot $\mapsto \mathbb{F}$ in $(A,M)=(0,0)$).
4. **Direction.** Ribbon concordance from $K_0$ (births + fusions upward) to $K_1$ gives $\widehat{\mathit{HFK}}(K_0)\hookrightarrow\widehat{\mathit{HFK}}(K_1)$; the source is the *smaller* knot. Conventions in the literature are not uniform. A flipped direction gives systematic spurious UNSAT precisely on the interesting pairs.
5. **Freeness of the returned basis** over $R$, and $\bar\partial^2=0$ on the returned data. Both are cheap integrity checks; run them.
6. **Finiteness** is fine ($A,M$ ranges bounded), but confirm you are not silently dropping $(a,b)=(0,0)$ or pairs where $M_j-M_i$ is odd.

## Compatibility of Thms 1.1 and 1.7

No conflict — 1.1 is the mod-$(U,V)$ shadow of 1.7's map, and you are requiring both of a *single* $F$, which is what the theorem gives. But you have discarded the strongest content. Two strictly stronger and still-decidable tests:

- **Left inverse:** ask for $G$ and $h$ with $GF + \mathrm{id} = dh+hd$ over $R$. Bilinear in the unknowns, hence still SAT-encodable, and it implies your injectivity condition.
- **Direct summand:** Zemke gives $\mathit{CFK}(J)\simeq \mathit{CFK}(K)\oplus A$. Over $R$ this is summand-containment of reduced complexes, i.e. (via Hanselman–Rasmussen–Watson) *containment of multicurve components as a multiset* — a near-trivial computation, far stronger than a generic chain map, and no SAT needed. Caveat: uniqueness of the indecomposable decomposition over the graded-local ring $R$ is the Krull–Schmidt statement you would need to cite properly. I would run this as the primary test and keep SAT as a fallback.

## Controls

Your birth+fusion movies only exercise the SAT direction and cannot validate absence. Add: identity $K\to K$; $U\to R$ for known ribbon $R$; $K\to K\# R$ (always ribbon-concordant); composition/transitivity; and **negative** controls where nonexistence is known independently — $g(K)>g(J)$, and Gordon's $\Delta_K \mid \Delta_J$. Any UNSAT should be accompanied by a report of which of these classical obstructions already fires; an UNSAT that is the *first* obstruction on a pair is the one deserving hand-verification of the two complexes.

## Recommendation

Call it an exploratory necessary check pending (i) a written grading/decoration dictionary between Zemke's conventions and the calculator's, verified on $\ge 3$ knots by hand, and (ii) the reducedness and $\bar\partial^2=0$ audits. Promote a *specific* UNSAT to "rigorous obstruction" only after the complexes involved are independently reproduced.

Finally: an UNSAT for $K\to J$ with both nontrivial says nothing about sliceness. Only $U\to K$ with $K$ slice would bear on slice-ribbon, and that conclusion's weight vastly exceeds what a convention-sensitive pipeline can currently carry.
