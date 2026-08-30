# Abe–Tagami route audit

## Exact objects and signs

Abe–Tagami [S06, §5] define

\[
K_n=A_n(6_3),
\]

using the (n)-fold annulus twist on their fixed annulus presentation of (6_3). To avoid suppressed mirror/reversal conventions, define

\[
D_{n,m}=K_n\#(-K_m),\qquad -K_m=r(\overline{K_m}).
\]

This is the oriented smooth-concordance difference. Therefore

\[
[K_n]=[K_m]\quad\Longleftrightarrow\quad D_{n,m}\text{ is smoothly slice}.
\]

The forward implication follows by gluing a concordance from (K_n) to (K_m) to the standard evaluation ribbon concordance for (K_m\#(-K_m)); equivalently, ([D_{n,m}]=[K_n]-[K_m]=0) in the smooth concordance group. This statement does **not** justify (K_n\#K_m), nor does common 0-surgery imply it.

## What Miyazaki actually gives

Miyazaki [S07, Thm. 5.5], restated as [S06, Thm. 4.1], concerns a connected sum of prime fibered knots that are minimal in the homotopy-ribbon partial order or satisfy the stated Alexander-polynomial condition (no nonunit factor that is a norm). If the sum is homotopy-ribbon, the summands must pair by the prescribed mirror/reversal relation.

Abe–Tagami verify the usable specialization in Corollary 4.3: for the relevant fibered knots with irreducible Alexander polynomials, ribbonness of the signed connected sum forces equality of the summands. Their (K_n) share the irreducible polynomial

\[
\Delta(t)=1-3t+5t^2-3t^3+t^4.
\]

They also establish that (K_n\cong K_m) exactly when (n=m) or (n+m=-1). Hence, when this exceptional isotopy relation is excluded,

\[
D_{n,m}\text{ is not ribbon}.
\]

This is a rigorous non-ribbon theorem. It says nothing by itself about smooth sliceness.

## Concordance status

- Lemma 5.6 gives orientation-preservingly homeomorphic/diffeomorphic 0-surgeries across the family under the paper’s convention. This is not a concordance.
- The contact (d_3) calculations used in [S06] distinguish knots/open books; they are not smooth-concordance invariants.
- No primary source through the cutoff was verified to prove ([K_n]=[K_m]) for any distinct pair.
- No primary source through the cutoff was verified to prove pairwise smooth-concordance independence for the entire family.
- Hom–Park’s γ₀-sharp theorem [S08] would be relevant only after its hypotheses are proved for these precise summands; that application was not found.

There is no structural reason in [S06] forcing a concordance collision. Common Alexander polynomial and common 0-surgery merely explain why elementary invariants are weak. Conversely, the family may be separated by a modern concordance invariant not yet computed.

## Adversarial lane analysis

**Strongest reason it might work.** Non-ribbonness is already complete. One explicit concordance between distinct (K_n,K_m) would produce a smooth slice disk for a knot already covered by Miyazaki’s theorem.

**Strongest reason it probably fails.** Annulus twisting preserves 0-surgery but has no known reason to preserve smooth concordance. Directional Floer and gauge invariants are designed to distinguish fibered knots after classical invariants collapse.

**Exact missing lemma.** For some (n,m) with (n\ne m) and (n+m\ne-1), prove

\[
[A_n(6_3)]=[A_m(6_3)]\in\mathcal C^{\mathrm{smooth}}.
\]

**Finite verification route if supplied.** Verify the concordance movie/handle diagram; form (D_{n,m}); extract its slice disk; mechanically check the hypotheses of [S06, Cor. 4.3] and the non-isotopy condition.

**Kill condition.** A smooth-concordance invariant that differs for the proposed pair kills that pair. A proof that the (K_n) are pairwise independent modulo (K_n\cong K_{-n-1}) closes the whole lane.

## Verdict

**WEAK/LIVE.** It is logically clean and auditable, but it is not a certified-slice lane. Until a concordance equality is proved, every (D_{n,m}) remains a **CANDIDATE**, never a CE.
