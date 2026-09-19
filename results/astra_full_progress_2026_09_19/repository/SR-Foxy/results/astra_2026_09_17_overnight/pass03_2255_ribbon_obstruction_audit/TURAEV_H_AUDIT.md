# Turaev Theorem H(ii): primary-source audit

**Verdict:** useful historical obstruction, but **not ribbon-only against a knot already known homotopy-ribbon/handle-ribbon**. No KDG computation is warranted.

## What the theorem states

Turaev's Theorem H(ii), in the English translation on journal p. 341, asserts that if an oriented knot `K ⊂ S^3` is ribbon, then the nil-form

`F_2(l_1(K), l_2(K))`

is metabolic. The abstract advertises this as an obstruction to ribbonness, so without the proof it was reasonable to flag it as a possible forgotten ribbon-specific condition.

## What the proof actually uses

The decisive passage is §7.4, journal p. 356. Turaev says that part (ii) follows from Lemmas 7.2 and 7.3 and the fact that a ribbon knot bounds a smooth disk `D ⊂ B^4` for which the inclusion-induced map

`pi_1(S^3 - K) -> pi_1(B^4 - D)`

is onto.

Lemma 7.2 is already formulated for a smooth disk in `B^4` with the relevant induced epimorphism. Lemma 7.3 is the algebraic metabolic conclusion. Thus, once a smooth disk satisfying the epimorphism hypothesis is provided, the proof of H(ii) does not subsequently use ribbon singularities, bands, minima/maxima of the radial function, or an unlink derivative.

In current terminology, the displayed surjectivity is the group condition attached to a homotopy-ribbon disk. A handle-ribbon disk is in particular homotopy-ribbon. Therefore the implication proved in H(ii) extends at least to every knot equipped with such a disk.

## Application to KDG

The campaign's KDG candidate `18nh00000601` is already certified handle-ribbon in standard `B^4` in the Oliveira-Smith lane. Consequently Turaev's metabolic condition is forced by the known stronger-than-slice disk data and cannot separate KDG from ribbon knots.

This is a logical no-go, not a numerical pass. There is no reason to implement Turaev's nil-form for KDG unless it is wanted for independent mathematical interest or as a control.

## Scope

This does **not** say Theorem H is a sliceness obstruction or that every slice disk satisfies the needed epimorphism. It does not eliminate Theorem H from a candidate that is only known slice with no homotopy-ribbon disk. The conclusion here is candidate-specific: it cannot obstruct a knot already known handle-ribbon/homotopy-ribbon.

It also does not change Turaev's Theorem I, which constructs explicit knots whose nil-forms fail metabolic/hyperbolic/invertible conditions; the point is only the logical level of Theorem H(ii)'s necessary condition.

## Repository correction

`research/02_ribbon_only_obstructions.md` currently lists Turaev Theorem H among under-examined leads and says the primary text was not obtained. That historical status is now obsolete. This pass does not overwrite that file; this note is the additive correction to be folded into a future handoff/errata pass.

## Primary source

V. G. Turaev, *Multiplace generalizations of the Seifert form of a classical knot*, Math. USSR-Sb. 44(3) (1983), 335–361.

- Theorem H: journal p. 341.
- Lemmas 7.2–7.3 and proof of H(ii): §7, especially journal pp. 355–356.
- Math-Net English article/PDF entry: https://www.mathnet.ru/eng/sm2474
- DOI: https://doi.org/10.1070/SM1983v044n03ABEH000971

The proof was read in the English translation. The conclusion above is a direct logical strengthening of the stated ribbon implication using the hypothesis actually invoked in Turaev's proof; it is not claimed as a separately published theorem.
