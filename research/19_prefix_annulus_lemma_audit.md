# Audit of the connected genus-zero prefix lemma

14 September 2026. Requested by Astra, authorized by Scott. **No counterexample
found.** This note audits a proposed lemma, states where it is correct, where it
is stronger than claimed, and identifies the one load-bearing step that is
asserted rather than cited.

## The statement audited

> A connected genus-zero movie prefix from one knot to a two-component link L
> extends to an annulus only if L is link-concordant to a split knot/unknot
> pair. The complement of the prefix pair of pants in the annulus is an annulus
> plus a disk. Puncture that disk and extend its puncture along a tube about an
> arc to the final boundary, disjoint from the annulus, giving a split unknot.
> Thus the generic Alexander-module rank of L must be one.

Setting: `A` is a smooth concordance in `S^3 x I` from `K` at level 0 to `K'`
at level 1, so `A` is an annulus. At a regular level `t` the slice is a
two-component link `L = L_1 ∪ L_2`. `P = A ∩ (S^3 x [0,t])` is the prefix,
`Q = A ∩ (S^3 x [t,1])`.

## 1. The Euler-characteristic bookkeeping is correct

`∂P = K ∪ L_1 ∪ L_2` (three circles) and `∂Q = L_1 ∪ L_2 ∪ K'` (three circles).
Gluing along the two circles `L_1, L_2` contributes nothing to Euler
characteristic, so `χ(P) + χ(Q) = χ(A) = 0`.

With `P` connected of genus `g`, `χ(P) = 2 - 2g - 3 = -1 - 2g`, hence
`χ(Q) = 1 + 2g`. A surface with exactly three boundary circles has `χ = 3` if
it is three disks, `χ = 1` if it is a disk plus an annulus, and `χ = -1` if it
is connected. So `g = 0` gives `χ(Q) = 1` and `Q` is a disk plus an annulus,
exactly as claimed.

## 2. The genus-zero hypothesis is redundant, not an extra assumption

This is a strengthening, and it is worth recording as such.

Suppose `g = 1`. Then `χ(Q) = 3`, forcing `Q` to be three disks. Two of them cap
`L_1` and `L_2`; the third has boundary `K'` and is glued to nothing. Then `A`
has that disk as a whole connected component, so `A` is disconnected. An
annulus is connected, contradiction. Larger `g` needs `χ(Q) ≥ 5` with three
boundary circles, which is impossible.

**So for a connected prefix whose top slice has two components, genus zero is
forced.** The lemma may be stated with "connected" alone.

## 3. A case the statement does not exclude, and must

`Q` being "an annulus plus a disk" leaves two configurations, and only one of
them gives the conclusion:

* **(a)** the annulus joins some `L_i` to `K'`, and the disk caps the other `L_j`;
* **(b)** the annulus joins `L_1` to `L_2`, and the disk has boundary `K'`.

In case (b) the argument collapses. Gluing that annulus to the pair of pants
`P` yields a genus-one surface with the single boundary circle `K`
(`χ = -1 + 0 = -1`, one boundary, so `2 - 2g - 1 = -1`, `g = 1`), and the
`K'`-disk is a separate component, so `A` is disconnected. So (b) is excluded
— **but only by connectedness of `A`, not by the Euler characteristic count.**

This matters beyond pedantry: it is the step where "`A` is a concordance"
is used, as opposed to merely "`χ(A) = 0`". Applied to a genus-`g` cobordism
with `χ = 0` in place of an annulus, the lemma is false, because (b) survives.
Any restatement should carry the connectedness hypothesis explicitly.

## 4. The tubing step is sound

Given case (a): `L_1` cobounds an annulus with `K'` in `S^3 x [t,1]`, and `L_2`
bounds a disk `D` there, disjoint from that annulus. Remove an open disk from
`int D` to get an annulus from `L_2` to a small circle `c_0`, then tube `c_0`
out to `S^3 x {1}` along an arc `α`.

Two things need checking and both hold. First, `α` can be chosen disjoint from
the `L_1`-to-`K'` annulus: in a 4-manifold a generic arc misses a surface, since
`1 + 2 < 4`. Second, the resulting circle `c ⊂ S^3 x {1}` is a small unknot that
can be placed in a ball disjoint from `K'`, by choosing the endpoint of `α`
there, so `K' ∪ c` is genuinely split and not merely "unknotted component plus
knot".

So `L` is link-concordant to `K' ⊔ (split unknot)`. **The geometric content of
the lemma is correct.**

## 5. The load-bearing step that is asserted rather than cited

The jump from "L is link-concordant to a split pair" to "the generic
Alexander-module rank of L must be one" requires:

> the rank of `H_1(X_L; Λ) ⊗ Q(t_1,t_2)` is an invariant of link concordance.

This is **not** a formal consequence of anything in sections 1-4, and it is not
the multivariable Fox-Milnor theorem. Fox-Milnor constrains the polynomial of a
slice link; it does not by itself say that two concordant links have Alexander
modules of equal rank. The usual route is that the exterior `W` of a
concordance satisfies `H_*(W, X_L; Q(t)) = 0`, so that `W` is a homology
cobordism after localizing at the multivariable field of fractions, whence
`dim_{Q(t)} H_1(X_L;Q(t)) = dim_{Q(t)} H_1(X_{L'};Q(t))`. That statement is
standard in the Cochran-Orr-Teichner style literature, but it is a theorem with
hypotheses, not an observation, and this repository's standing rule is that
non-elementary inputs carry a primary source.

**Requested of Astra: a primary-source citation for exactly this claim, added
to a source ledger in the style of research/17.** Until then the rank-zero
exclusions should be labelled conditional on it. Nothing else in the lemma
needs a citation.

The target value is right once the invariance is granted: for the two-component
unlink the Alexander module is free of rank `μ - 1 = 1`, and a split pair has
the same rank, so rank one is the correct necessary value and rank zero excludes.

## 6. The consequence that is more useful than the exclusion

For a two-component link the module rank is at most one, and positive rank is
equivalent to vanishing of the multivariable Alexander polynomial. So the lemma's
real content is:

> a link `L` that occurs as the two-component slice of a connected prefix of a
> concordance must have `Δ_L(t_1,t_2) = 0`.

That is a **cheap, permissive, positively-usable screen**, and it is a better
search target than the split-product Jones test currently used. Splitness is
sufficient but far from necessary; `Δ_L = 0` is necessary and admits nonsplit
links. The 1,092 normalized matches in `results/normalized_component_neighborhoods.json`
were all shown nonsplit by the Jones split-product test, and a nonsplit link
generically has `Δ_L ≠ 0`, so rank zero on all 1,092 is the expected outcome and
is consistent rather than surprising.

**Recommendation:** stop requiring splitness at the endpoint and start
enumerating for `Δ_L = 0`. A nonsplit `L` with vanishing multivariable Alexander
polynomial is exactly the kind of object the current pipeline discards and the
lemma says is required.

## 7. Scope limits

* The lemma assumes the prefix is **connected**. A movie with a birth below
  level `t` has a disconnected prefix and escapes the lemma entirely. This is a
  larger escape than "fixed prefixes only": it is the whole birth-carrying class
  that the campaign's own common-upper-knot construction lives in.
* It assumes the slice at level `t` has exactly **two** components.
* It excludes specified prefixes. It is not an obstruction to `K_0` and `K_1`
  being concordant, and no statement in this note bears on that question.

## Verdict

Sections 1-4 are correct, and section 2 makes the lemma slightly stronger than
stated. Section 3 records a case that must be excluded by hand and is excluded
only by connectedness of the annulus. Section 5 is the one genuine gap: the
concordance invariance of the generic Alexander rank is doing real work and is
currently uncited. Section 6 proposes turning the lemma from an exclusion into a
search target.
