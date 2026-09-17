# Proposition C as a searchlight, the general annulus-twist stabilization, and the lifted surgery description

17 September 2026 (Opus, second pass, integrating Astra's `results/astra_2026_09_17_annulus_gate/`).
**No counterexample to the Slice–Ribbon Conjecture was found.** Nothing here is a
slice disk for `D_{0,1}` and nothing here obstructs one.

This pass did four things, in order of how much they change the board. It did
**not** re-audit Astra's algebra, and it did not repeat any completed search.

---

## 1. The Σ_p linking-form ladder is dead for this family, at every odd prime below 60

Last pass's Proposition C (`research/33` §4b) says: for `p` an odd prime, if
`H_1(Σ_p(K))` is elementary abelian of exponent `q` with `q ≡ 1 (mod p)`, the
linking form is *hyperbolic*, so the metabolizer gate is vacuous. The
complementary regime `q ≡ −1 (mod p)` is where it has teeth.

That is a **searchlight**: it says exactly where to look. So look.
`|H_1(Σ_p(K_n))| = |Res(Δ, 1 + t + … + t^{p−1})|` with
`Δ = t⁴ − 3t³ + 5t² − 3t + 1`:

| p | `|H_1(Σ_p)|` | structure | `q mod p` | regime |
|---:|---:|---|---:|---|
| 3 | 49 | `7²` | 1 | vacuous |
| 5 | 256 | `2⁸` | 2 | not elementary abelian; settled separately in `research/33` §4c |
| 7 | 1849 | `43²` | 1 | vacuous |
| 11 | 157609 | `397²` | 1 | vacuous |
| 13 | 1371241 | `1171²` | 1 | vacuous |
| 17 | `10303²` | | 1 | vacuous |
| 19 | `30553²` | | 1 | vacuous |
| 23 | `139² · 1933²` | | 1, 1 | vacuous |
| 29 | `523² · 13399²` | | 1, 1 | vacuous |
| 31, 37, 41, 43, 47, 53, 59 | — | | all 1 | vacuous |

**Every odd prime `p < 60` lands in the `q ≡ 1` regime.** By Proposition C the
linking form of `Σ_p(K_n)` is hyperbolic in each case, so the metabolizer gate
cannot fire for *any* difference `D_{n,m}` at any of those primes.

Why `±1` and nothing else, in general: the deck transformation acts on
`H_1(Σ_p) ⊗ F_q` with order `p` and no nonzero fixed vector, so `p | q² − 1`,
i.e. `q ≡ ±1 (mod p)`. Concretely `H_1(Σ_p; F_q) = F_q[t]/gcd(Δ, t^p − 1)`, and
the regime is `+1` exactly when that gcd splits into linear factors over `F_q`.
For this `Δ` it splits every time in the scanned range.

**What this excludes, precisely.** The branched-cyclic-cover linking-form
metabolizer obstruction, for `D_{n,m}` in the Abe–Tagami family, at every odd
prime `p < 60`; together with `research/33` §4 and §4c it also covers `p = 2`
and `p = 5`. It excludes nothing finer on the same covers — `d`-invariants,
Casson–Gordon and metabelian twisted Alexander all remain live, and Proposition
C says nothing about them.

Reproduced by the inline scan recorded in
`results/opus_2026_09_17/sigma_p_ladder_scan.json`.

---

## 2. Theorem A′: the stabilization is a feature of annulus twists, not of 6₃

`research/33`'s Theorem A was stated for `K_0 = 6_3`. It is a special case.

> **Theorem A′.** Let `K ⊂ S³` have an annulus presentation `(A, b)` in which `A`
> is an unknotted annulus with `k` full twists, so `∂A` is the `(2, 2k)` torus
> link and `lk(c'_1, c'_2) = k`, with `lk(K, c'_i) = 0`. Let `W_k` be the trace
> of the **1-fold** annulus twist: `S³ × I` with 2-handles on `c'_1, c'_2` with
> the integral framings `k + 1` and `k − 1`. Then
>
> * `K × I ⊂ W_k` is a smooth annulus from `K` to `A¹(K)`, disjoint from the
>   handles;
> * the intersection form is `Q_k = [[k+1, k],[k, k−1]]`, with
>   `det Q_k = −1` and `sign Q_k = 0` **for every `k`**;
> * `Q_k` is **even iff `k` is odd**.
>
> Hence for `k` odd, `W_k` is simply connected with the even hyperbolic form `H`,
> so `K` and `A¹(K)` cobound an annulus in a 4-manifold homeomorphic rel
> boundary to `(S³ × I) # (S²×S²)`; for `k` even the form is `⟨1⟩ ⊕ ⟨−1⟩` and the
> ambient is `(S³ × I) # CP² # \overline{CP²}`.

The determinant is `(k+1)(k−1) − k² = −1` identically — that is the whole
computation, and it is why the 1-fold annulus twist always has an `S³` boundary
and always costs exactly rank two. Checked for `−3 ≤ k ≤ 5` in
`results/opus_2026_09_17/theorem_A_prime.json`.

**What is new.** `research/33` proved the `k = 1` case smoothly and remarked that
`n = ±1` are the only integral slopes. Theorem A′ says the phenomenon is uniform
over annulus presentations: *every* annulus-twist pair is one stabilization
apart, with the parity of the twist number deciding which stabilization. The
Abe–Tagami lane is therefore not a special coincidence to be exploited; it is the
generic behaviour of the construction, and the counterexample question is
uniformly "can this one stabilization be removed?"

**What it is not.** It is not a smooth statement for `|k| ≠ 1`: reducing `Q_k` to
`H` over `Z` is immediate, but realizing that reduction by handle slides on the
`(2,2k)` torus link was not done here. For `k = 1` the smooth statement stands,
now with the citation removed — see §3.

---

## 3. The one cited step in Theorem A is now proved here

`research/33` §1.4 flagged `W ≅ (S³×I) # (S²×S²)` as resting on Gompf–Stipsicz,
`SECONDARY, NOT VERIFIED FROM ORIGINAL`. That dependency is removable. Elementary
proof, for `k = 1`, framings `(2, 0)` on the Hopf link `c'_1 ∪ c'_2`:

1. `B⁴ ∪ h(c'_2, framing 0)` is the `D²`-bundle over `S²` with Euler number 0,
   i.e. `S² × D²`, with boundary `S² × S¹`.
2. Write `S³ = (S¹ × D²) ∪ (D² × S¹)` with `c'_2 = S¹ × 0` and `c'_1 = 0 × S¹`
   — the Hopf link. Zero-surgery on `c'_2` reglues so that the result is
   `(D² × S¹) ∪_id (D² × S¹) = (D² ∪ D²) × S¹ = S² × S¹`, and `c'_1 = 0 × S¹`
   becomes `pt × S¹`.
3. Under that identification the Seifert framing 0 of `c'_1` in `S³` **is** the
   product framing of `pt × S¹`, because two parallel cores of the unknotted
   solid torus `D² × S¹ ⊂ S³` have linking number 0.
4. So `X̂_m := B⁴ ∪ h(c'_2, 0) ∪ h(c'_1, m) ∪ B⁴` is `S² × D²` glued to `D² × S²`
   along `S² × S¹` by a map `(x, θ) ↦ (ρ(θ)·x, θ)`, where the framing shift `m`
   corresponds to the `m`-fold rotation loop `ρ ∈ π₁(SO(3))`.
5. `π₁(SO(3)) = Z/2`, so the gluing for `m = 2` is isotopic to the gluing for
   `m = 0`, which is the identity: `X̂_2 ≅ S² × D² ∪_id D² × S² = S² × S²`. ∎

Since the handles are attached inside a ball in `S³ × {1}`, `W = (S³×I) ♮ X`
with `∂X = S³`, hence `W ≅ (S³×I) # X̂_2 ≅ (S³×I) # (S²×S²)`.

This uses only `π₁(SO(3)) = Z/2` and the two standard bundle identifications. The
Gompf–Stipsicz citation is retained as corroboration, not as a dependency.

**On Astra's framing trap.** The `FRAMING_ADDENDUM` rejects the shortcut that
inherits the mirrored `n = 1` framings on the two cross-paired classes and
discards the rest: that gives `diag(2, −2)`, `H_1 = Z/2 ⊕ Z/2`, not `S³`.
Theorem A is a different object and does not use that shortcut: its matrix is the
actual `n = 1` trace matrix `[[2,1],[1,0]]`, and its boundary was certified `S³`
by **Regina's 3-sphere recognition**, not by reading off `det = ±1`. Astra's
instruction "never promote `det = ±1` to `S³` or to standardness" is respected;
the determinant is reported as a property of the form only.

---

## 4. Astra's flagged upstream dependency is discharged

`REPORT.md` §2 states: *"No independent SnapPy extraction from the PD was
possible in this environment"*, and `inputs.json` labels the upstream PD hash
*reported, not recomputed*.

`scripts/regenerate_marked_axes_from_pd.py` supplies the extraction. From the
stored 27-crossing PD of `L = K ∪ c'_1 ∪ c'_2` it fills both surgery cusps along
`(1,0)`, restoring the `K_0` exterior, reads the old longitudes of `c'_1, c'_2`
as the marked axes `u, v`, and then **rebuilds the nonconjugacy certificate from
scratch**: it brute-force enumerates every homomorphism of the freshly generated
presentation into `SL(2, F_5)` and exhibits one whose image conjugacy classes of
`u` and of `v^{±1}` differ. No word, matrix or presentation from `research/14` is
used as input.

Six independent triangulation seeds, presentations with 2 or 3 generators and
axis words of lengths 4–17, **all six agree**: `u` is conjugate to neither `v`
nor `v^{-1}`. Result in
`results/opus_2026_09_17/regenerate_marked_axes_from_pd.json`.

**Limits.** This discharges the PD → marked-group → nonconjugacy chain. It does
**not** independently re-verify that the stored PD is the Abe–Tagami figure —
that still rests on `data/knots/AbeTagami_CONSTRUCTION.md`, where the two binary
drawing choices were resolved by which knot the construction produced. The
Alexander cross-check inside the script returned `None` (the generated
presentations were not of deficiency one in the form the Fox routine expects);
that check is **not obtained**, not failed.

Astra's two verifiers were rerun here with fresh output paths and reproduce
exactly: 44 named checks and 4681 arithmetic controls pass, and the framing gate
returns `all_plus_matrix = [[2,0],[0,-2]]` as published.

---

## 5. The annulus twist hands over a surgery description of Σ₂(K₁)

`research/33` §3 left the `research/21` §3 `d`-invariant gate "out of
computational reach", because `Σ₂(K_1)` is hyperbolic and therefore bounds no
plumbing. The missing alternative was *a surgery description on which existing
formulas apply*. The annulus twist supplies one, because `lk(K, c'_i) = 0` means
each surgery curve lifts to **two** curves in the double branched cover.

Concretely: fill the knot cusp of `L`'s exterior along `(2,0)` and take the
2-fold cyclic cover. Among the seven index-2 covers exactly one has five cusps —
the `K`-lift, carrying the induced filling `(1,0)`, plus two lifts each of
`c'_1` and `c'_2`. Call the resulting 4-cusped manifold `M̃` (34 tetrahedra,
`H_1 = Z⁴`). Then

* filling all four cusps trivially gives `Σ₂(K_0)`, recognized by Regina as
  **`L(13,5)` exactly** (3 tetrahedra);
* filling with the lifted twist slopes gives a `Z/13` manifold that agrees with
  the directly built `Σ₂(K_1)` (20 tetrahedra, same isoSig).

So **`Σ₂(K_1)` is Dehn surgery on an explicit 4-component link in `L(13,5)`**,
namely the preimage of `c'_1 ∪ c'_2`. That is the object the `d`-invariant gate
needs. Cross-validation of both endpoints is in
`results/opus_2026_09_17/lifted_surgery_description.json`.

**Limits, and one retracted method.** SnapPy renormalizes cusp bases per cover,
so the lifted slopes are not `(1,0)` and `(2,1)/(0,1)` in the cover's own basis;
they have to be found by search and then pinned by saving the triangulation,
because `covers()` need not return the same representative on a rerun (34, 36
and 38 tetrahedra were all observed).

**Retraction.** A first version of that search identified the filled manifold by
comparing Regina `isoSig`s after a randomised `simplify()`. That is unsound:
`isoSig` is a canonical invariant of a *triangulation*, not of a manifold, and
two simplifications of the same manifold routinely differ — the target here
simplified to 19 tetrahedra on one run and 20 on the next. That method reported
two fillings on one run and zero on the next; **both are artifacts and neither
is an identification**, and any slopes read off it are withdrawn. The script's
own `controls_pass` flag caught this, by finding `L(13,5)` fillings but no
`Σ₂(K_1)` filling, which the construction forbids.

Survivors are now identified by hyperbolic volume and confirmed with
`is_isometric_to`, legitimate for closed hyperbolic manifolds by Mostow
rigidity, with failures to find a positively oriented solution recorded
`UNKNOWN` rather than as non-matches. **On that method the controls pass**, and
the slopes exist:

| | count | identified by |
|---|---:|---|
| fillings searched | 65,536 | slope box `|p|,|q| ≤ 2`, coprime |
| give `Σ₂(K_0) = L(13,5)` | **320** | Regina recognition *by name* |
| give `Σ₂(K_1)` | **59** | volume `7.28132635174862` + `is_isometric_to` |
| no geometric solution found | 986 | recorded `UNKNOWN`, not as non-matches |

`M̃` is the unique 5-cusped index-2 cover, **34 tetrahedra**, `H_1 = Z⁴`, and its
triangulation string is saved in the artifact — without it the slopes are
meaningless, since `covers()` returned 34-, 36- and 38-tetrahedron
representatives on different runs.

**The slopes have exactly the structure the construction predicts.** Every one
of the 59 hits assigns `±(2,−1)` to two of the four cusps and `±(1,1)` to the
other two — that is, the two lifts of `c'_1` share a slope up to sign and the
two lifts of `c'_2` share the other. Downstairs the twist is `(2,1)` on `c'_1`
and `(0,1)` on `c'_2`; SnapPy's per-cover basis differs, but the pairing is the
signature of the doubled lift and it is reproduced by the search rather than
assumed. Of the `C(4,2) · 2⁴ = 96` slope assignments with that shape, 59 are
confirmed and the remainder fall in the `UNKNOWN` bucket; **no claim is made
about those 37.**

So: **`Σ₂(K_1)` is Dehn surgery on an explicit 4-component link in `L(13,5)`,
with an explicit slope vector on a saved triangulation.** That is the object the
`research/21` §3 `d`-invariant gate was missing.

### 5a. The unwinding to `S³` fails, and the gate is homological

The `d`-invariant formulas consume surgery on a link in `S³`, so the obvious
follow-through was to unwind `L(13,5)`: drill the core of its genus-1 Heegaard
torus and fill that core along the slope restoring `S³`. The cover already
carries the **lifted branch knot** `K̃_0` as its fifth cusp, so no new curve
would have been needed — *if* `K̃_0` were that core.

**It is not.** With the meridian vector `μ` on the four lifted curves, so that
the ambient is `L(13,5)`, filling the `K̃_0` cusp along `(a,b)` gives

```
|H_1| = 13 · |a|,   independent of b
```

over the whole box `|a|,|b| ≤ 4`. That is exactly the signature of a
**null-homologous** knot in a rational homology sphere, where filling along
`a·μ + b·λ` multiplies `|H_1(Y)|` by `|a|`. So `[K̃_0] = 0` in
`H_1(Σ₂(K_0)) = Z/13`, every filling has order divisible by 13, and **no filling
is ever `S³`**. A Heegaard-torus core generates `H_1`, so `K̃_0` is not one.

*Excluded, precisely:* unwinding `L(13,5)` **via the lifted branch knot**.
*Not excluded:* unwinding via an actual Heegaard-torus core, which is a
different curve and is not a cusp of this cover. The §5 surgery description is
untouched.

A first version of this search also returned zero, for a different and wrong
reason — it filtered on `str(homology()) != ''` when SnapPy prints trivial `H_1`
as `'0'`, discarding every candidate. That zero was a bug; this one is a
computation, and the `H_1` grid is the evidence rather than a failed search.
Artifact: `results/opus_2026_09_17/unwind_L13_5_attempt.json`.

**The route that replaces it, needing no unwinding.** `13/5 = [3,3,2]`
(`3 − 1/(3 − 1/2) = 13/5`), so `−L(13,5)` bounds the negative definite linear
plumbing with weights `(−3,−3,−2)`. `Σ₂(K_1)` therefore bounds that plumbing
with the four lifted 2-handles attached, `b₂ = 3 + 4 = 7`. **If that form is
negative definite**, then `D_{0,1}` slice would make
`Σ₂(D_{0,1}) = L(13,5) # −Σ₂(K_1)` bound a rational homology ball, and
Donaldson's theorem would force the form to embed in the diagonal lattice — a
finite, exact, integer test whose *failure* would kill the Abe–Tagami lane
outright. What it still needs is the lifted curves' classes and pairwise
linking in `L(13,5)`, which is not yet computed.

---

## 6. Two moves that fail, delimited exactly

* **Norman-trick destabilization of the Theorem A annulus.** `C` is disjoint from
  neither sphere `F` (from the 0-framed handle) nor `G` (from the 2-framed one)
  in general, but `[F]·[C] = lk(K_0, c'_2) = 0` and `F·G = 1`, so Norman's trick
  can tube `C` into parallel copies of `G` to remove `C ∩ F`. **It fails**,
  because tubing into `G` changes `[C] ∈ H_2(W, ∂)` by `[G] ≠ 0`, and a
  concordance needs `[C] = 0`. The failure is homological and complete: no
  choice of tubes avoids it. This does not exclude other destabilizations.
* **Pushing `C` off the summand.** If `C` could be isotoped into the `S³ × I`
  part, then `π₁((S³×I) ∖ C) = π₁(W ∖ C) = Z` (connected sum with simply
  connected `S²×S²` does not change `π₁`), and `research/14` §3's lemma would
  force `Δ_{K_0} = 1`. It does not. So `C` is **stably essential**: it can never
  be pushed off the stabilization. Theorem A and that lemma are two halves of one
  statement, and neither says anything about a *different* annulus.

---

## 7. Ten leads, each with its first computation

Ordered by expected value per unit of work. None is a claim; each is a next step.

1. ~~Pin the lifted slopes on `M̃`.~~ **Done, see §5**: 59 confirmed slope
   vectors on a saved 34-tetrahedron triangulation. The lead becomes: convert
   that surgery description into one on a link in `S³` by unwinding
   `L(13,5) = -13/5` surgery on an unknot, which is what the `d`-invariant
   formulas actually take as input.
2. **Intersection form of the branched double cover of the trace.** `W₂ → W`
   branched over `C` has `∂W₂ = (−L(13,5)) ⊔ Σ₂(K_1)` and `b₂ = 4`. First
   computation: the `4 × 4` form from the lifted curves. *If it is definite*,
   Donaldson gives a lattice obstruction to `sn(D_{0,1}) = 0` — i.e. to the
   counterexample — and if it is not, it still bounds the `d`-invariant shift.
3. **Casson–Gordon / HKL at `(p, q) = (3, 7)`,** implemented without Sage by Fox
   calculus over `Q(ζ_7)`. This is the cheapest obstruction that neither
   Lemma B nor Proposition C touches. First computation: the metabelian
   representation on the `(Z/7)²` characters, whose Gram matrices are already in
   `results/opus_2026_09_17/cyclic_cover_linking_form_gate.json`.
4. **Find an annulus presentation with `k` odd on another negative amphichiral
   fibered knot** — `8_12`, `8_17`, `10_17` are the natural targets. Theorem A′
   then gives the stabilized annulus for free, and a *different* `Δ` means the
   Σ_p ladder of §1 must be recomputed and may land in the live `q ≡ −1` regime.
   This is the one lead that could make Proposition C's teeth bite.
5. **Test the `q ≡ −1 (mod p)` regime directly** by searching the knot tables for
   any knot whose `Σ_p` homology is `(Z/q)²` with `q ≡ −1 (mod p)` *and* which
   carries a nonribbon certificate. `scripts/prop_c_census.py` already found 271
   such knot/prime pairs; none has been cross-referenced against the candidate
   ledger. First computation: that cross-reference.
6. **The Abe–Tagami monodromy, used computationally for the first time.**
   `t_{c'_1}^{-n} t_{c'_2}^{n} t_d^{-1} t_b t_c^{-1} t_a` on a genus-2
   once-punctured fiber is recorded in `data/knots/AbeTagami_K_n_NOTES.json` and
   has never been run. First computation: its action on `H_1` of the fiber and on
   the set of cut systems, to test the Agol–Ren fibered-compression criterion.
7. **`sn` for the other differences.** Theorem A′ plus the composition
   `A^n = (A^1)^n` stacks traces: `sn(D_{0,n}) ≤ n`. First computation: check
   whether the annulus framing is preserved by one twist (so the stacking is
   legitimate), which decides whether `D_{0,2}` is two stabilizations or more.
8. **Donaldson on the `n = 2` trace.** For `|n| ≥ 2` the slopes are rational and
   the trace has `b₂ = 4`; the continued-fraction expansion is a choice. First
   computation: enumerate expansions of `3/2` and `1/2` and record which give
   definite or spin traces — a definite one would be an obstruction, not a
   construction.
9. **Cross-apply the §1 ladder to the Hom–Park and Miyazaki Tier-B knots.** Those
   have free nonribbon certificates and unknown sliceness. Caveat worth stating
   up front: the Miyazaki cables are strongly rationally slice (Kawauchi), so
   their `Σ_p` linking forms are metabolic *a priori* and this screen is vacuous
   there — the Hom–Park knots are the non-vacuous half.
10. **Recover the `r = 0` RBG generator.** `UNFINISHED` §4 is blocked only on two
    lost files (`../mma.py`, `../mp_auto.py`). First computation: regenerate the
    generator from the GHMR paper rather than hunting for the files. It is the
    only lane whose success needs no concordance coincidence at all.

---

## 8. Reproduction

```sh
python3 scripts/regenerate_marked_axes_from_pd.py results/opus_2026_09_17/regenerate_marked_axes_from_pd.json
# Astra's verifiers, fresh outputs, from a checkout of origin/main's directory:
python3 verify_annulus_gate.py --output opus_annulus_recheck.json
python3 verify_framing_gate.py --output opus_framing_recheck.json
```

Environment: Python 3.11, `snappy` 3.3.2, `regina` 7.4, `sympy` 1.14.0, no Sage.
Astra's verifiers are standard-library only and were run unmodified from
`origin/main` without altering the working tree.
