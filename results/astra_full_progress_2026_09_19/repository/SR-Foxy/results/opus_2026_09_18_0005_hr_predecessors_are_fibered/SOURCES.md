# Sources, quoted verbatim

## Primary new input

**Brian Sun, *Twisted Alexander Polynomials and Fibered Classes in Ribbon
Homology Cobordisms*, arXiv:2604.20785.** v1 22 Apr 2026, **v2 6 May 2026**
(this is the version read). Fetched live from `https://arxiv.org/html/2604.20785v2`
on 18 September 2026 and text-extracted. Unrefereed preprint.

**Abstract (verbatim).**

> Let `Y_-` and `Y_+` be two compact 3-manifolds with empty or toroidal boundary.
> A 4-dimensional ribbon homology cobordism is a homologically trivial cobordism
> built with 1-handles and 2-handles. In this note, following the work of Friedl
> and collaborators, we apply twisted Alexander polynomials to show that the
> fibered classes of `Y_+` map to those of `Y_-`.

**Theorem 1.1 (verbatim).**

> Let `Y_-` and `Y_+` be 3-manifolds with a ribbon homology cobordism `W` from
> `Y_-` to `Y_+`. If `phi_+ in H^1(Y_+;Q)` is a fibered class, then the
> associated class `phi_- in H^1(Y_-;Q)` is also fibered.

**Corollary 1.2 (verbatim), with the author's own attribution.**

> Let `L_0` and `L_1` be links with `L_1 >= L_0` with `L_1` nontrivial. If `L_1`
> is fibered, then so is `L_0`.

Introduced by Sun as "Specializing to ribbon concordances, we have the following
result, **first shown in the case of knots [Sil92, Koc06]**." So the *ribbon
concordance* knot case is Silver 1992 / Kochloukova 2006, not new; the content
we need is the extension of Theorem 1.1 beyond ribbon concordances to arbitrary
ribbon homology cobordisms.

**Lemma 3.1 (verbatim) - the step that makes it work for `<=_h`.**

> Let `beta: pi_1(Y_-) -> G` be a representation to a compact connected Lie
> group `G`. Then `beta` can be extended to a representation
> `alpha: pi_1(W) -> G` that restricts to `beta`.
>
> *Proof.* In a ribbon homology cobordism we have
> `W = Y_- x I u 1-handles u 2-handles`. This means we can write
> `pi_1(W) = (pi_1(Y_-) * F) / <<r_1,...,r_n>>`. Since
> `H_*(Y_-;Q) -> H_*(W;Q)` is an isomorphism, there are the same number of
> 1-handles (generators of `F`) and 2-handles (relations), with the 2-handles
> cancelling out the 1-handles homologically. This implies that the `r_i`
> satisfy the conditions of [GR62, Theorem 1(ii)], from which we immediately
> obtain `alpha`. []

`[GR62]` is Gerstenhaber-Rothaus - the same tool Gordon used in [Gor81]. Note
what Lemma 3.1 does **not** assume: no ribbon concordance, no band presentation,
no standard ambient. Only the handle structure and the homology isomorphism.

**Direction conventions, checked rather than assumed.** Sun sets `L_1 >= L_0`
with `W` the concordance exterior, and Corollary 1.2 concludes "`L_1` fibered =>
`L_0` fibered". Matching that against Theorem 1.1's "`phi_+` fibered => `phi_-`
fibered" pins `Y_+ = X_1` (exterior of the larger knot) and `Y_- = X_0`
(exterior of the smaller). So `W` runs from the **smaller** knot's exterior and
is built from it with 1- and 2-handles. This agrees with the standard
homotopy-ribbon convention - `pi_1(X_1) ->> pi_1(W)` surjective and
`pi_1(X_0) >-> pi_1(W)` injective, which Sun also states explicitly, citing
[Gor81] and [DLVVW22, Proposition 2.1].

## Matching definition on the Agol-Ren side

Ian Agol, Qiuyu Ren, arXiv:2603.10884v1, definition quoted verbatim:

> A concordance from `J` to `K` in a homotopy `I x S^3` is strongly
> homotopy-ribbon if its complement admits a relative handle decomposition with
> only 1- and 2-handles.

This is literally Sun's "ribbon" condition on the complement. The relative
decomposition of a cobordism from `E_J` to `E_K` is relative to `E_J`, which is
the smaller end, matching the direction fixed above.

## Other inputs (already recorded in this repository)

- Agol-Ren Theorem 1.7, printed by them as "([CG83])", i.e. **Casson-Gordon**:
  for fibered `J, K`, `J <=_h K` in some homotopy `I x S^3` iff the monodromy of
  `K` compresses to that of `J`.
- Friedl-Powell arXiv:1907.09031 Theorem 1.1, settled for `<=_h` in
  `results/opus_2026_09_17_2230_alexander_divisibility_settled/`.
- The compression genus lemma, proved in the same directory.
- `data/knots/AbeTagami_L_63_c1_c2.json` for every stored geometric fact.
- Classification of genus-one fibered knots (fiber a once-punctured torus):
  the two trefoils and the figure-eight. Classical.
