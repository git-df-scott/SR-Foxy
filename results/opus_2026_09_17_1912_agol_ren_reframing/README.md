# The KDG lane is exactly an open question of Agol–Ren, and the Abe–Tagami certificate can be replaced

17 September 2026, ~19:12 UTC. **CE: NO.** No counterexample, no disk, no
concordance. This pass is a literature search that changed the strategic picture,
plus one airtight reframing and one cleaner certificate.

Primary sources fetched and read this pass (LaTeX source, not summaries):

* **Trevor Oliveira-Smith**, *A Dunfield–Gong 4-Sphere is Standard*,
  [arXiv:2603.23717](https://arxiv.org/abs/2603.23717), submitted 24 March 2026.
  Abstract, verbatim: *"we standardize a homotopy 4-sphere constructed by
  Dunfield and Gong. As a corollary, we show that the 18-crossing knot
  18_nh00000601, which is not known to be ribbon, is slice in the standard
  4-ball. … In addition, we show that the same knot bounds a fibered
  handle-ribbon disk in B⁴."* This confirms the campaign's `[S01]` dependency is
  a real, current preprint.
* **Ian Agol, Qiuyu Ren**, *Ribbon concordance of fibered knots and compressions
  of surface homeomorphisms*, [arXiv:2603.10884](https://arxiv.org/abs/2603.10884),
  source dated 12 March 2026. Read: abstract, §1.1, §1.2, §2 definitions, §7.

---

## 1. The finding: `KDG` is a counterexample **iff** `≤_h` is strictly finer than `≤`

Agol–Ren §2, verbatim definition:

> *"A concordance from `J` to `K` in a homotopy `I×S³` is **strongly
> homotopy-ribbon** if its complement admits a relative handle decomposition
> with only 1- and 2-handles. If such a concordance exists, we write `J ≤_h K`."*

**That is exactly the handle-ribbon condition** — a complement with no 3-handles.
So Oliveira-Smith's theorem that `KDG` bounds a *fibered handle-ribbon disk in
`B⁴`* says precisely `U ≤_h KDG`, and in the **standard** `I×S³`, which is
stronger than the "some homotopy `I×S³`" that `≤_h` allows.

Meanwhile `KDG` is ribbon iff `U ≤ KDG` (a ribbon disk, punctured at its
minimum, is a ribbon concordance from the unknot). Therefore:

> **Proposition.** `KDG` is a counterexample to the Slice–Ribbon Conjecture
> **if and only if** `U ≤_h KDG` and `U ≰ KDG`. Since `U ≤_h KDG` is a theorem
> (Oliveira-Smith), `KDG` is a counterexample **iff** `≤_h ≠ ≤`, witnessed at
> the pair `(U, KDG)`.
>
> *Proof.* `KDG` is slice in standard `B⁴` (Oliveira-Smith, Cor. 1.1.1), so it is
> a counterexample iff it is not ribbon, iff `U ≰ KDG`. The handle-ribbon disk
> gives `U ≤_h KDG` by the definition above. A pair with `U ≤_h KDG` and
> `U ≰ KDG` is exactly a witness that `≤_h` is strictly finer than `≤`. ∎

And Agol–Ren state, §1.2, verbatim:

> *"To our knowledge, it is open whether `≤_h` is a strictly finer relation
> than `≤`."*

**Consequences, and they are strategic rather than mathematical.**

1. Proving `KDG` non-ribbon would *simultaneously* resolve an open question
   posed by Agol and Ren in March 2026. The lane cannot be cheaper than that.
2. Conversely, if `≤_h = ≤`, then `U ≤_h KDG` gives `U ≤ KDG` and **`KDG` is
   ribbon** — the flagship candidate dies outright.
3. This explains, structurally, why every entry in `OBSTRUCTION_MATRIX.md`
   reads `APPLIES BUT VANISHES` for `KDG`: each of those obstructions
   (π₁-epimorphism, Casson–Gordon extension, metabelian restrictions, R-link
   derivatives) factors through `≤_h`, and `U ≤_h KDG` holds. Nothing that
   factors through `≤_h` can ever separate. The matrix was recording a single
   underlying fact.

This is a **hardness calibration, not an obstruction**. It does not show `KDG`
is ribbon and does not show it is not.

## 2. A cleaner certificate for the Abe–Tagami lane

Agol–Ren Corollary 1.10(1), verbatim:

> *"If the slice-ribbon conjecture is true, then every concordance class of
> knots contains at most one fibered knot that is minimal with respect to
> `≤_h`."*

Applied to the lane: `K_0 = 6_3` and `K_1 = A_1(6_3)` are fibered, **distinct**
(distinct exterior volumes `5.693…` vs `9.120…`; `Σ₂(K_0) = L(13,5)` is a lens
space while `Σ₂(K_1)` is not, `research/21` §2), and conjecturally concordant.
So:

> **If `K_0` and `K_1` are concordant and both `≤_h`-minimal, the Slice–Ribbon
> Conjecture is false.**

This is the same conclusion as the repository's Abe–Tagami/Miyazaki route, but
the hypotheses are *fewer and cleaner*: fibered, distinct, `≤_h`-minimal. It
needs **no** irreducible-Alexander-polynomial condition and **no** prime-summand
audit — the audit that `ERRATA_2026-09-16.md` (E16-1) already had to correct
once, after five planning sites restated Miyazaki 5.5 without a quantifier.

### 2a. Minimality is now reducible to one lemma

Agol–Ren's Theorem 1.4 (Casson–Gordon 1983): for fibered `J, K`, `J ≤_h K` iff
`φ_K` **compresses** to `φ_J`. In their §2, a compression body is built from
`I × ∂_iC` by 0- and 1-handles, equivalently from `∂_eC` by 2- and 3-handles —
so `fiber(J)` is obtained from `fiber(K)` by genuine compressions. A nontrivial
compression strictly reduces `−χ`. Hence:

> **Lemma (immediate from their definitions).** If `J <_h K` are fibered knots
> with `J ≠ K`, then `g(J) < g(K)`.

`6_3` has genus 2, so proper `≤_h`-predecessors have genus `≤ 1`:

| candidate | status |
|---|---|
| genus 0, i.e. `U` | **excluded, airtight.** `U ≤_h 6_3` would make `6_3` handle-ribbon hence slice; `det(6_3) = 13` is not a perfect square, verified, so Fox–Milnor forbids it |
| genus 1 fibered, i.e. `3_1`, `m3_1`, `4_1` | excluded **modulo** Alexander divisibility under `≤_h` (§2b) |

Verified this pass: `Δ_{6_3} = t⁴−3t³+5t²−3t+1` is **irreducible over `Q`**;
`det = 13`, not a perfect square; `Δ_{3_1} = t²−t+1` and `Δ_{4_1} = t²−3t+1`
**neither divides** `Δ_{6_3}`. `K_1` has the same `Δ` and the same genus 2, so
the identical argument applies to it.

### 2b. The single remaining dependency, stated exactly

What is needed is: **`J ≤_h K` implies `Δ_J | Δ_K`.** Gilmer (1984) proves this
for ribbon concordance `≤`. Agol–Ren state that their Theorems 1.1, 1.2, 1.3
strengthen from `≤` to `≤_h`, but I did **not** find a statement of Alexander
divisibility at the `≤_h` level in the parts I read, and I did **not**
reconstruct its proof. It is plausible from the compression-body structure
(`H₁(fiber K) ↠ H₁(C) ↩ H₁(fiber J)`, equivariantly for the monodromy, which is
the circle of ideas in Miyazaki's Lemma 1.3 that Agol–Ren cite at §2), but it is
recorded here as **UNVERIFIED DEPENDENCY**, not as established.

With that one lemma, `K_0` and `K_1` are `≤_h`-minimal and the lane's non-ribbon
certificate is Agol–Ren Cor. 1.10(1).

### 2c. Why the dilatation route does not close it instead

Agol–Ren Theorem 1.2 gives `J ≤_h K ⟹ λ(J) ≤ λ(K)`. That would exclude `4_1`
(`λ = (3+√5)/2 ≈ 2.618034`) if `λ(6_3) < 2.618034`. All I can compute here is
the **homological lower bound** `λ(6_3) ≥ 1.722084`, the spectral radius of the
monodromy action on `H₁(fiber)`, i.e. the largest `|root|` of `Δ_{6_3}`. That
bound is attained by a **complex-conjugate pair** of roots, not a real root, so
the invariant foliations are not orientable and `λ(6_3)` is strictly larger than
the bound by an unknown amount. A lower bound cannot exclude anything here.
Computing `λ(6_3)` needs train-track software (`flipper`/`Twister`), which is not
installed. Recorded **UNKNOWN**, not as a failed exclusion.

## 3. What this does not do

It produces no disk, no concordance, and no counterexample. §1 makes the `KDG`
lane *harder to justify*, not easier. §2 improves the *certificate* on the
Abe–Tagami lane while leaving its missing ingredient — a smooth concordance
`K_0 ≃ K_1` — exactly where it was.

## 4. Reproduction

```sh
python3 results/opus_2026_09_17_1912_agol_ren_reframing/check_agol_ren_arithmetic.py   # exit 0
```

Standard library plus `sympy` only. No SnapPy, Regina or Sage. Nothing was
rerun: not the 65,536 fillings, `s`, HKL, Floer, the `D01` parallels, or the KDG
four-parallel.
