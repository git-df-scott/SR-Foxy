# SETTLED: `J ≤_h K ⟹ Δ_J | Δ_K` is TRUE, and Gilmer's hypothesis was never needed

17 September 2026. **CE: NO.** This pass settles the dependency flagged
`UNVERIFIED` in `results/opus_2026_09_17_1912_agol_ren_reframing/`. No new
object was constructed.

## Verdict

**The implication holds.** Moreover the answer to "does Gilmer's argument
genuinely need `J ≤ K`?" is a clean *both*:

* **Gilmer's proof does need more.** Friedl–Powell say so explicitly:
  *"For knots and for `≥_sm` instead of `≥_top`, Theorem 1.1 is a consequence of
  a more general theorem of Gilmer. However **Gilmer's proof does not extend to
  the topological category**."*
* **But the theorem is true under strictly weaker hypotheses anyway**, by a
  different proof.

> **Theorem (Friedl–Powell, [arXiv:1907.09031](https://arxiv.org/abs/1907.09031),
> Thm 1.1).** If `J ≥_top L` then `Δ_L | Δ_J`.

with (their §1, verbatim) `J ≥_top L` meaning a locally flat concordance `C` in
`S³ × I` from `J` to `−L` such that `π₁(X_J) ↠ π₁(X_C)` is **surjective** and
`π₁(X_L) ↪ π₁(X_C)` is **injective**.

### The decisive remark

Friedl–Powell, §1, verbatim:

> *"Perhaps somewhat surprisingly, the condition that `π₁(X_L) → π₁(X_C)` is
> injective is **not needed anywhere in our proof** of Theorem 1.1."*

So the divisibility needs **only π₁-surjectivity from the larger end**. That is
strictly less than homotopy-ribbon, and far less than ribbon.

## Why this applies to Agol–Ren's `≤_h`

Orientation conventions differ between the two papers and getting them backwards
would invert the conclusion, so explicitly: Friedl–Powell's `J` (surjective end)
is Agol–Ren's `K`; Friedl–Powell's `L` (injective end) is Agol–Ren's `J`. Hence
`Δ_L | Δ_J` reads **`Δ_J | Δ_K`** in Agol–Ren's `J ≤ K` notation — the direction
needed.

The chain, hypothesis by hypothesis:

1. **`≤_h` gives the surjectivity.** Agol–Ren §2: `J ≤_h K` iff the concordance
   complement admits a relative handle decomposition with only 1- and 2-handles.
   Relative to the *smaller* end `X_J` — this is fixed by the ribbon-disk case,
   where `X_U` is a solid torus and the disk exterior is a 0-handle plus 1- and
   2-handles. Dually the decomposition is relative to `X_K` with handles of index
   `4−1 = 3` and `4−2 = 2`, i.e. **index ≥ 2 only**, which changes `π₁` by adding
   relations at most. Hence `π₁(X_K) ↠ π₁(X_C)`. Friedl–Powell make exactly this
   step for `≥_sm` in their §1 ("*admits a handle decomposition relative to `X_J`
   with only 2- and 3-handles, from which it is easy to see that the induced map
   … is surjective*").
2. **The ambient.** Friedl–Powell state Theorem 1.1 for `S³ × I`; Agol–Ren's
   `≤_h` allows *some homotopy* `I × S³`. A homotopy `I × S³` is a simply
   connected h-cobordism from `S³` to `S³`, hence **homeomorphic to `S³ × I`** by
   Freedman's topological h-cobordism theorem, and a smooth concordance in it
   becomes a locally flat concordance in `S³ × I` — which is precisely the
   category Friedl–Powell work in. Independently, they note their proof
   "*can also be generalised to concordances between links in homology spheres*",
   though they did not carry that out. **The Freedman route is the one used
   here**; the authors' own generalisation remark is not relied on.
3. **Injectivity is not required**, by their remark above. So no appeal to
   Gordon's Lemma 3.1 or to residual finiteness of knot groups is needed at all.

**Conclusion: `J ≤_h K ⟹ Δ_J | Δ_K`.** The `UNVERIFIED DEPENDENCY` recorded in
the previous checkpoint is discharged.

### A sharper fact worth keeping

Friedl–Powell's source carries an author comment isolating what Gordon's
argument actually proves:

> *"[SF] … he proves a stronger statement, if `Y = X` with `n` 1-handles and `n`
> 2-handles attached and if `H_*(Y,X) = 0`, then `π₁(X) → π₁(Y)` is a
> monomorphism. This works for any `X` as long as `π₁(X)` is residually finite."*

Under `≤_h` the handle counts are automatically **balanced**: `χ(X_C) = χ(X_J)`
because both are homology circles, and each 1-handle contributes `−1` and each
2-handle `+1`, so `#1 = #2`. With `H_*(X_C, X_J) = 0` and knot groups residually
finite, Gordon's argument therefore *also* delivers injectivity under `≤_h`.
So `≤_h` implies the **full** `≥_top` condition, not merely the half that
Theorem 1.1 uses. Recorded as a strengthening; the main conclusion does not
depend on it.

## Consequence for the campaign

`research/34` and `results/opus_2026_09_17_1912_agol_ren_reframing/` reduced
`≤_h`-minimality of `K_0 = 6_3` and `K_1 = A_1(6_3)` to exactly this lemma. It
is now available, so:

* A nontrivial compression strictly reduces `−χ`, so a proper `≤_h`-predecessor
  of a fibered knot has **strictly smaller genus** (Agol–Ren Thm 1.4 plus their
  §2 compression-body definition).
* `6_3` has genus 2, so proper predecessors have genus `≤ 1`.
* **Genus 0** (the unknot): `U ≤_h 6_3` would make `6_3` handle-ribbon hence
  slice, but `det(6_3) = 13` is not a perfect square. Excluded.
* **Genus 1** (`3_1`, `m3_1`, `4_1`): now excluded, because `Δ_{3_1} = t²−t+1`
  and `Δ_{4_1} = t²−3t+1` neither divides the **irreducible**
  `Δ_{6_3} = t⁴−3t³+5t²−3t+1`. All three facts verified exactly.

Hence **`K_0` and `K_1` are both `≤_h`-minimal**, and they are distinct
(exterior volumes `5.693…` vs `9.120…`; `Σ₂(K_0) = L(13,5)` is a lens space,
`Σ₂(K_1)` is not). By Agol–Ren Corollary 1.10(1):

> **If `K_0` and `K_1` are smoothly concordant, the Slice–Ribbon Conjecture is
> false.**

This is the same conclusion the repository already had from Abe–Tagami/Miyazaki,
but the certificate now needs only *fibered + distinct + `≤_h`-minimal* — no
irreducible-Alexander hypothesis on the pair, and no prime-summand audit. That
audit is the one `ERRATA_2026-09-16.md` (E16-1) already had to correct after
five planning sites restated Miyazaki 5.5 without its quantifier. **The lane's
most error-prone dependency is retired.**

The missing ingredient is unchanged and untouched: a smooth concordance
`K_0 ≃ K_1`.

## Positive control

Friedl–Powell's own example, verified here: `3_1 # −3_1` and `4_1 # −4_1` are
both slice, hence concordant, yet their Alexander polynomials
`t⁴−2t³+3t²−2t+1` and `t⁴−6t³+11t²−6t+1` are **coprime**, so neither is
homotopy ribbon concordant to the other. The divisibility test has teeth; it is
not vacuous on concordant pairs.

## Why a counterexample was never worth hunting

Gilmer proves divisibility under `≤`. So any pair with `J ≤_h K` and
`Δ_J ∤ Δ_K` would satisfy `J ≤_h K` but `J ≰ K`, i.e. **would by itself prove
`≤_h ≠ ≤`** — the question Agol–Ren record as open. Searching for a
counterexample was therefore at least as hard as an open problem, and the
proof direction was the only tractable one. This is recorded because it is the
reasoning that chose the direction of attack, not a result.

## Reproduction

```sh
python3 results/opus_2026_09_17_2230_alexander_divisibility_settled/check_divisibility_settled.py   # exit 0
```

`sympy` only. Sources read this pass as LaTeX source, not summaries:
[arXiv:1907.09031](https://arxiv.org/abs/1907.09031) (Friedl–Powell) and
[arXiv:2603.10884](https://arxiv.org/abs/2603.10884) (Agol–Ren).
