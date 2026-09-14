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

## 5a. Terminology correction

An earlier draft of this note, and the first commit of
`scripts/alexander_rank_screen.py`, described the computed quantity as "the
multivariable Alexander polynomial `Δ_L(t_1,t_2)`". That is not what
`snappy`'s `Manifold.alexander_polynomial()` returns on a link exterior. It
returns the **order of the Alexander module of the exterior**. The two differ:
on the Whitehead link `snappy` gives `a^2 b^3 - a b^2 - a b + 1`, whose `b = 1`
specialisation is `(a-1)^2`, while the classical `Δ_L` of a linking-number-zero
link must satisfy the Torres condition `Δ_L(t,1) = 0`.

The conclusions are unaffected, because the order vanishes exactly when the
module has positive rank, and positive rank is the condition the lemma needs.
The naming is corrected because the distinction matters to anyone re-deriving
these numbers.

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

## 8. A retracted claim, and what the screen actually says

**Retraction.** An earlier version of this section reported that the two
first-stage links research/17 retained on target J25533, `6267660c_0_0` and
`2b2a271f_1_0`, both FAIL the rank condition, that the two necessary conditions
therefore had empty intersection, and that either 25533 was dead or one of the
arguments was wrong. **That was wrong, and the cause was a defect in my own
screen, not anything in either argument.**

The screen called `Link.simplify('global')` before building the exterior.
That method **deletes split unknot components**. A trefoil with a split unknot,
which has order 0 and passes, becomes the bare trefoil, which has order
`a^2 - a + 1` and fails. The defect inverted the verdict on precisely the links
the screen is meant to accept, since a split knot-plus-unknot pair is the
intended pass.

The original calibration could not catch this. `3_1 ⊔ 4_1` has no unknotted
component, so simplification had nothing to delete and the control passed while
the screen was broken. The calibration set now includes a knot with a **split
unknot** component, which is the case that fails loudly.

**Corrected result**, with no simplification, in
`results/alexander_rank_screen_25533.json`:

| | of 61 stored first-stage links |
|---|---:|
| positive Alexander module rank | **29** |
| known-good control `1918_0_-1` passes | **yes** |
| research/17 survivors `6267660c_0_0`, `2b2a271f_1_0` pass | **both** |
| intersection of the two necessary conditions | **both survivors** |

The control is the decisive check and it is what exposed the defect. The band
`1918_0_-1` is the first band of the stored two-fission movie that recovers
K0 from J25533; its endpoint is verified here to be a six-crossing knot whose
exterior is isometric to the `6_3` exterior, with HFK rank 13, fibered, genus 2,
tau 0. That movie exists, so its first-stage link **must** satisfy every
necessary condition. It does: two components, order 0, positive rank. A screen
that failed the control was refuted by the control.

**So there is no tension.** Both research/17 survivors satisfy the rank
condition, nothing on 25533 is eliminated that research/17 had kept, and the
lemma of this note removes 32 of the 61 first-stage links, which research/17's
component tests had already removed. On this target the screen is consistent
with, and weaker than, the component filter.

The lesson is the calibration, not the target: a screen whose intended pass is
"split knot plus unknot" must be calibrated on a link with a split unknot
component, and must include a positive control drawn from a movie known to
exist. Both are now enforced in `scripts/alexander_rank_screen.py`, which
refuses to report if either fails.

The 1,092 normalized matches are unaffected. Re-run with the corrected screen:
**1,092 examined, 0 with positive rank, 0 errors.** Those links were certified
nonsplit, so they carry no split unknot component for `simplify` to delete, and
the independent confirmation of Astra's rank-zero result stands as reported.

## Verdict

Sections 1-4 are correct, and section 2 makes the lemma slightly stronger than
stated. Section 3 records a case that must be excluded by hand and is excluded
only by connectedness of the annulus. Section 5 is the one genuine gap: the
concordance invariance of the generic Alexander rank is doing real work and is
currently uncited. Section 6 proposes turning the lemma from an exclusion into a
search target.
