# Sources, quoted verbatim

Fetched live on 17 September 2026 from `https://arxiv.org/html/2603.10884v1`
(Ian Agol, Qiuyu Ren, *Ribbon concordance of fibered knots and compressions of
surface homeomorphisms*, arXiv:2603.10884, **v1 only**, submitted 11 March 2026).
Text extracted by stripping HTML tags; LaTeX-ese from the HTML renderer removed
by hand where it duplicated a symbol. Nothing below is paraphrase.

## Theorem 1.13

> Let `J_1,...,J_m, K_1,...,K_n` be prime fibered knots, `m,n >= 0`. Then
> `J_1 # ... # J_m <=_h K_1 # ... # K_n` if and only if there exist knots
> `K_{i,j}`, `1 <= j <= l_i`, `1 <= i <= n`, for some `l_i >= 0`, such that
>
> * `K_{i,1} # ... # K_{i,l_i} <=_h K_i` for all `i`;
> * the collection of knots `K_{i,j}` consists of exactly the knots
>   `J_1,...,J_m` and some other `2k` knots
>   `J_{m+1}, -J_{m+1}, ..., J_{m+k}, -J_{m+k}` that come in (reversed)
>   mirrored pairs, `k >= 0`.

## Corollary 1.14

> (1) If the slice-ribbon conjecture is true, then every concordance class of
> knots contains at most one fibered knot that is minimal with respect to `<=_h`.
>
> (2) If the slice-ribbon conjecture and the smooth 4-dimensional Poincare
> conjecture are both true, then no torsion element in the knot concordance
> group of order greater than 2 can be represented by a fibered knot.

**Provenance, stated by the authors immediately after:**

> Theorem 1.13 implies parts of Theorems 5.3 and 5.5 in [Miy94], and conversely,
> Miyazaki's proof of these results may also apply to show Theorem 1.13.
> Corollary 1.14(1) is an immediate consequence of Miyazaki (see [Bak16,
> Remark 6]), and Corollary 1.14(2) follows from Theorem 5.8 in [Miy94].

So **Corollary 1.14(1) is Miyazaki's, not Agol-Ren's**. Cite Miyazaki (Trans.
AMS 341 (1994)) / Baker [Bak16, Remark 6] as the source, with Agol-Ren 1.14(1)
as the convenient modern statement.

## Question 1.15

> If `K_1` and `K_2` are concordant fibered knots, must there be a fibered knot
> `K` with `K_1 <= K`, `K_2 <= K`? (Or with `<=` replaced by `<=_h`?)

> One may replace the existence of `K` in Question 1.15 by the equivalent
> condition that `K_1, K_2` are related by a zigzag of (strongly
> homotopy-)ribbon concordances between fibered knots. Note that Question 1.15
> is implied by the slice-ribbon conjecture, since one could take
> `K = K_1 # K_2 # (-K_1)`.

## The unnumbered genus-<=3 remark (immediately after Question 1.15)

> Using the characteristic submanifold theory in the spirit of the arguments in
> [Bon83], one can show that if `K_1, K_2` are hyperbolic knots with genus at
> most 3, and are each minimal with respect to `<=_h`, then the existence of a
> fibered knot `K` with `K_1 <=_h K`, `K_2 <=_h K` implies that `K_1 = K_2`.

**Status caveat.** This is an unnumbered remark. The paper gives no proof, no
lemma reference beyond "[Bon83]" and the phrase "one can show". It is NOT a
theorem of the paper and must not be cited as one.

## Theorem 1.7 (quoted for the genus lemma's hypothesis)

> **Theorem 1.7 ([CG83]).** If `J, K` are fibered, then `J` admits a strongly
> homotopy-ribbon concordance to `K` in some homotopy `I x S^3` if and only if
> the monodromy of `K` compresses to that of `J`.

Not Agol-Ren's result: printed by them as Casson-Gordon [CG83].

## Definition used

> A concordance from `J` to `K` in a homotopy `I x S^3` is strongly
> homotopy-ribbon if its complement admits a relative handle decomposition with
> only 1- and 2-handles.

## Repository inputs (not re-derived here)

- `data/knots/AbeTagami_L_63_c1_c2.json` - the 27-crossing link `6_3 u c'_1 u c'_2`,
  its linking matrix, the `n = 1` slopes `(2,1),(0,1)`, the Regina `isSphere`
  check, the SnapPy isometry tests and volumes. All gates G1-G8 read this file.
- `data/knots/AbeTagami_K_n_NOTES.json` - Abe-Tagami Appendix B: `K_n` is fibered
  with monodromy `t_{c'_1}^{-n} t_{c'_2}^{n} t_d^{-1} t_b t_c^{-1} t_a` on the
  genus-2 fiber of `6_3`; Remark B (Oba): `d_3(xi_n) = -n^2-n+3/2`, so
  `K_n = K_m` iff `n = m` or `n + m = -1`.
- `research/33_one_stabilization_and_the_forced_collapse.md` - Theorem A.
- `research/14_marked_annulus_audit.md` Section 3 - `pi_1(W - C) = Z` and the
  cyclic-exterior lemma.
- `results/opus_2026_09_17_2230_alexander_divisibility_settled/` - Friedl-Powell
  arXiv:1907.09031 Theorem 1.1 giving `J <=_h K ==> Delta_J | Delta_K`, and the
  genus lemma.
