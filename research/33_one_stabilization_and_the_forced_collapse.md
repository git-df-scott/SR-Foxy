# One stabilization, a forced algebraic collapse, and why the d-invariant gate is out of reach

17 September 2026. **No counterexample to the Slice–Ribbon Conjecture was found.**
Nothing here is a slice disk for `D_{0,1}` and nothing here obstructs one.

This note answers the question the campaign has been circling — *can the actual
annulus-twist geometry produce a smooth concordance between `K_0` and `K_1`?* —
with a precise, verified partial answer, and then closes several of the routes
that were still open on paper.

Six results, in decreasing order of how much they change the board:

1. **Theorem A.** `K_0` and `K_1` cobound an explicit smooth annulus in a
   4-manifold `W` with `∂W = (−S³) ⊔ S³` whose intersection form is the even
   hyperbolic form `H`. So the annulus twist does deliver a concordance —
   *after a single `S²×S²` stabilization* (one is an upper bound; it is zero
   precisely in the counterexample case), and `n = ±1` is the only annulus
   twist for which the stabilization is this cheap. §1.
2. **Lemma B.** Every knot invariant that factors through the S-equivalence
   class of the Seifert matrix is *forced* to agree on `K_n` and `K_m`. The long
   list of vanishing classical computations in this repository was never
   evidence; it was a theorem. §2.
3. **Σ₂(K₁) is hyperbolic** (numerically; see the honesty note in §3). This removes the Ozsváth–Szabó plumbing algorithm, the only
   implementable route we have, from the d-invariant gate of `research/21` §3.
   §3.
4. **The linking-form metabolizer gate is passed at `p = 2, 3, 5`**, exactly and
   with certificates. `λ(Σ₂(K_n))(g,g) = 5/13, 6/13, 7/13` for `n = 0,1,2`, all
   in one square class; `H_1(Σ_3) = (Z/7)²` with equal discriminants;
   `H_1(Σ_5) = (Z/4)⁴` with an explicit verified metabolizer. §4, §4b, §4c.
5. **Proposition C.** For `p` an odd prime and `H_1(Σ_p(K))` elementary abelian
   of exponent `q ≡ 1 (mod p)`, the linking form is *always* hyperbolic. So the
   `p = 3` gate above was vacuous before it was run — an obstruction that
   vanishes on everything of the relevant shape. §4b.
6. **A ribbon control refutes a tempting shortcut.** The Gauss-sum criterion
   `GS(λ) = +|H_1|^{1/2}` for metabolic linking forms is false over even-order
   groups: `8_20` is ribbon and gives `−8`, not `+4`. §4b. It is recorded with
   that restriction rather than used where it would mislead.

---

## 1. Theorem A: the annulus twist is one stabilization away from a concordance

### 1.1 Statement

> **Theorem A.** Let `K_0 = 6_3` and `K_1 = A_1(6_3)` be the Abe–Tagami knots as
> built in `data/knots/AbeTagami_CONSTRUCTION.md`. Let `W` be the trace of the
> `n = 1` annulus twist: `S³ × I` with two 2-handles attached along
> `c'_1, c'_2 ⊂ S³ × {1}` with integral framings `2` and `0`. Then
>
> * `C = K_0 × I ⊂ S³ × I ⊂ W` is a smoothly embedded annulus with
>   `∂C = K_0 ⊂ ∂_− W` and `K_1 ⊂ ∂_+ W`;
> * `∂_± W = S³`, `W` is simply connected, and its intersection form is the even,
>   unimodular, indefinite rank-2 form `H`;
> * consequently `W ≅ (S³ × I) # (S²×S²)`, and `D_{0,1} = K_0 # (−K_1)` bounds a
>   smooth disk in `B⁴ # (S²×S²)`.

Equivalently, writing `sn(K)` for the least `n` with `K` bounding a smooth
null-homologous disk in `(#ⁿ(S²×S²)) ∖ B⁴` (so `sn(K) = 0` means slice):
`sn(D_{0,1}) ≤ 1`, and
`sn(D_{0,1}) = 0` is exactly the counterexample this campaign is looking for.

### 1.2 What is machine-checked

`scripts/annulus_trace_stabilization.py` →
`results/opus_2026_09_17/annulus_trace_stabilization.json`, `ALL_CHECKS_PASS = true`,
from the committed 27-crossing link `L = K ∪ c'_1 ∪ c'_2`:

| check | value |
|---|---|
| linking matrix of `L` | `[[0,0,0],[0,0,1],[0,1,0]]` |
| `lk(K, c'_1) = lk(K, c'_2)` | `0` — so `K × I` misses the handles |
| `lk(c'_1, c'_2)` | `+1` |
| `c'_1 ∪ c'_2` | simplifies to a 2-crossing 2-component diagram; its exterior has Regina isoSig `dLQacccbjkg`, equal to that of `snappy.Manifold('L2a1')`: the **Hopf link** |
| knot component | exterior isometric to `6_3` |
| `n = 1` slopes | `(2,1)` and `(0,1)`: **integral**, framings `2` and `0` |
| handle form | `[[2,1],[1,0]]`, determinant `−1`, even, indefinite ⇒ `≅ H` over `Z` |
| `∂_+ W` | Regina `isSphere() = True` |
| outgoing knot | exterior isometric to the stored `K_1` (vol 9.120006500798…) and **not** to `6_3` |

The Hopf-link identification is also complete as a diagram argument on its own:
a 2-crossing diagram of a 2-component link with `lk = ±1` is the Hopf link.

### 1.3 Movie bookkeeping

`C` is a product annulus: it has **no** births, saddles or deaths at all, so the
required count is trivially satisfied — connected, `χ(C) = 0`, two boundary
components, relative Euler characteristic `0`. The four-manifold, not the
surface, is where the whole difficulty sits. This is the honest answer to
"turn the annulus presentation into an explicit surface movie": the movie is
the constant movie, and the price is paid entirely by the ambient manifold.

### 1.4 The one step that is not machine-checked

`W` is `(S³ × I)` boundary-connect-summed with `X = B⁴ ∪ (2-handles on the Hopf
link, framings 2 and 0)`, because the handles are attached inside a ball in
`S³ × {1}`; and `∂X = S³`, so `W ≅ (S³ × I) # X̂` with `X̂ = X ∪ B⁴` closed.
`X̂` is the `S²`-bundle over `S²` whose Kirby diagram is a Hopf link with one
`0`-framed component and one component framed `2`; since `π₁(SO(3)) = Z/2`
there are exactly two such bundles and the even framing gives the trivial one,
`S²×S²`. This is standard Kirby calculus (Gompf–Stipsicz, *4-Manifolds and
Kirby Calculus*, GSM 20, ch. 4). **The original was not consulted in this
container and this step is marked `SECONDARY, NOT VERIFIED FROM ORIGINAL`.**
It is not load-bearing for the topological statement: `W ∪ (two B⁴)` is closed,
simply connected with even form `H`, so it is *homeomorphic* to `S²×S²` by
Freedman with no citation beyond that.

### 1.5 Why `n = ±1` and nothing else

The `n`-fold annulus twist is `(n+1)/n` and `(n−1)/n` surgery on `c'_1, c'_2`
in the Seifert framing. These are integral **only** for `n = ±1`
(`n = −1` gives framings `0, 2`, and `K_{−1} = K_0`). For `|n| ≥ 2` the slopes
are genuinely rational — `n = 2` gives `3/2` and `1/2` — so each surgery curve
needs a chain of at least two integer-framed 2-handles and the trace has
`b_2 ≥ 4`, not `2`. (Which 4-manifold you get depends on the continued-fraction
expansion chosen, e.g. `1/2 = 1 − 1/2 = 0 − 1/(−2)`, so no parity claim is made
here; only the rank.) So `D_{0,1}` is not merely the smallest member of the
Abe–Tagami lane, it is the only one whose annulus-twist trace is a **single**
stabilization. That is a structural reason to prefer it, which this repository
did not previously have.

### 1.6 What Theorem A is not

Two warnings, both sharp.

* **The trace annulus cannot be destabilized.** `research/14` §3 proves
  `π₁(W ∖ C) = Z`, and its lemma then forces `Δ_{K_0} = Δ_{K_1} = 1` if `W`
  could be replaced by a standard `S³ × I` keeping this annulus. Since
  `Δ = t⁴ − 3t³ + 5t² − 3t + 1 ≠ 1`, it cannot. Theorem A and that obstruction
  are two halves of one statement: the annulus exists, at stabilization one,
  and *this* annulus never descends.
* **Existence of the stabilized annulus carries no concordance information.**
  Run the same construction at `n = −1`: identical Hopf link, framings `0` and
  `2`, identical form `H` — and the endpoints are `K_0` and `K_{−1} = K_0`,
  which are of course concordant. So Theorem A must not be read as evidence
  for `[K_0] = [K_1]`. It is a statement about *where the difficulty lives*,
  and a quantitative one: one stabilization, not two, not none.

---

## 2. Lemma B: the classical collapse is forced, not observed

> **Lemma B.** Let `K, K'` be knots and suppose there is an orientation-preserving
> homeomorphism `M(K) → M(K')` of the zero-framed surgeries carrying meridian to
> meridian. Then the Seifert matrices of `K` and `K'` are S-equivalent; hence
> `[K] = [K']` in the algebraic concordance group and `K # (−K')` is
> algebraically slice.

*Proof.* (i) The Blanchfield pairing is defined intrinsically on `M(K)`:
Borodzik–Friedl, *The unknotting number and classical invariants I*,
[arXiv:1203.3225](https://arxiv.org/abs/1203.3225), §"The Blanchfield pairing and
intersection pairings on 4-manifolds" (there `M := M(K)`, the zero-framed
surgery), verbatim: *"It is well-known that the natural map `H_1(X(K);Λ) →
H_1(M;Λ)` is an isomorphism, and it follows immediately that the Blanchfield
pairing on `X(K)` is isometric to the pairing … on `M`."* The
meridian-preserving hypothesis is what matches the two `Λ = Z[t,t^{-1}]`
structures. (ii) Trotter, *On S-equivalence of Seifert matrices*,
Invent. Math. **20** (1973), 173–207: the isometry type of the Blanchfield
pairing determines the S-equivalence class of the Seifert matrix; quoted in the
same section of Borodzik–Friedl as *"Note that the isometry type of the
Blanchfield pairing in fact determines the S-equivalence class of the Seifert
matrix, see [Tro73] and [Ran03]. In that sense the Blanchfield pairing is a
'complete' classical invariant, i.e. it determines all other classical
invariants."* (iii) S-equivalence preserves the Witt class. ∎

**It applies to this family with no hypothesis to check.** The annulus twist is
supported in a neighbourhood of the annulus, which is disjoint from `K`, so the
Abe–Jong–Omae–Takeuchi homeomorphism `M(K_n) → M(K_m)` is the identity near `K`
and therefore preserves the meridian by construction. No numerical
identification of 0-surgeries is needed or used.

**The exclusion, stated precisely.** *No invariant that factors through the
S-equivalence class of the Seifert matrix can obstruct sliceness of any
`D_{n,m}`.* That covers the Alexander polynomial and Fox–Milnor, the Alexander
module and Blanchfield pairing, **all** Levine–Tristram signatures and
nullities, Milnor signatures, the Arf invariant, and the Levine algebraic
concordance class. Every such computation on this family is an audit, not a
test, and a null answer from one is not information.

It covers **nothing else**. Casson–Gordon and metabelian twisted-Alexander
obstructions, `d`-invariants of branched covers, and all gauge-theoretic and
Floer invariants do *not* factor through S-equivalence and remain live.

`scripts/zero_surgery_algebraic_concordance.py` records the predicted equalities
(Levine–Tristram signatures of `K_0`, `K_1`, `K_2` at 24 sample points, with a
trefoil positive control that fires). Agreement is a consistency check on the
stored diagrams, not new evidence — the lemma already forces it.

---

## 3. `Σ₂(K_1)` is hyperbolic, and that closes the d-invariant gate's only route

`research/21` §3 states the sharpest falsifiable gate on the board:

> `D_{0,1}` smoothly slice ⟹ the thirteen `d`-invariants of `Σ₂(K_1)` are, as a
> multiset, exactly those of `L(13,5)`.

and §4 leaves `Σ₂(K_1)` unidentified, explicitly withdrawing an earlier
hyperbolicity claim because SnapPy found no positively oriented solution and
Regina did not recognize the triangulation. **That withdrawal was correct about
what had been shown, and the manifold really is (numerically) hyperbolic.** The
fix is to simplify in Regina first and re-solve in SnapPy:

| manifold | Regina tets | recognition | hyperbolic solution | volume |
|---|---:|---|---|---:|
| `Σ₂(K_0)` | 3 | `L(13,5)` | none (correct: lens space) | — |
| `Σ₂(K_1)` | 19 | none | yes, 9 tetrahedra | `7.2813263517` |

`Σ₂(K_1)` is irreducible and **non-Haken**. The `Σ₂(K_1)` row above was read
off a direct run; the packaged `scripts/sigma2_geometry_probe.py`, which adds
the lens-space controls and a `Σ₂(K_2)` row, was **still running when this note
was committed** and its
`results/opus_2026_09_17/sigma2_geometry_probe.json` lands in a follow-up
commit. Nothing in §3 or §5 depends on the `K_2` row. See that file for the
triangulation isoSigs and the controls (`3_1 → L(3,1)`, `4_1 → L(5,q)`, `6_3 → L(13,5)`, all
recognized, none hyperbolic).

**Honesty note.** A positively oriented solution is strong numerical evidence,
not a proof. Interval-arithmetic verification (`M.verify_hyperbolicity`) needs
Sage, which is not available in this container. This is recorded as
`hyperbolic_numerically`, never as `hyperbolic`.

**Why it matters, negatively** (conditional on the hyperbolic structure being
genuine, which is exactly what the honesty note above withholds). The boundary
of a plumbing on a tree of
`S²`-bundles is a graph manifold, and a hyperbolic 3-manifold is not a graph
manifold. So `Σ₂(K_1)` bounds no plumbing at all, negative definite or
otherwise, and the Ozsváth–Szabó plumbing algorithm — which needs a negative
definite plumbing with at most one bad vertex — cannot compute its
`d`-invariants. That
was the only route to the §3 gate implementable at this scale; `research/21` §4
had already found 40 randomized Goeritz forms indefinite, killing the sharp
`d`-invariant bound from a definite filling. **The gate is not refuted and not
closed — it is out of computational reach here, and the reason is now known.**
Reaching it needs either bordered Floer machinery for a genuinely hyperbolic
rational homology sphere, or a surgery description of `Σ₂(K_1)` on which
existing formulas apply.

---

## 4. The order-13 linking form gate, passed exactly

If `D_{i,j}` is slice then `Σ₂(D_{i,j}) = Σ₂(K_i) # (−Σ₂(K_j))` bounds a
rational homology 4-ball, so `λ_i ⊕ (−λ_j)` on `Z/13 ⊕ Z/13` must be metabolic.
On a cyclic group of prime order that happens **iff** `a_i · a_j` is a quadratic
residue, where `λ(g,g) = a/13`.

`scripts/sigma2_linking_form_gate.py`, exact integer arithmetic (Smith normal
form over `Z`, rational inverse of `V + Vᵀ`, no floating point):

| knot | `λ(g,g)` |
|---|---|
| `K_0 = 6_3` | `5/13` — matching `L(13,5)`, the control |
| `K_1` | `6/13` |
| `K_2` | `7/13` |

`5`, `6`, `7` are all non-residues mod 13, so every product `a_i a_j` is a
residue (`3`, `9`, `3` respectively) and **all three gates are passed**.
Controls: `3_1 → 1/3`, `4_1 → 3/5`, `5_1 → 1/5`, `6_1 → 5/9`, `6_3 → 5/13`.

*This excludes exactly one thing*: the order-13 linking form of the double
branched cover cannot obstruct sliceness of `D_{0,1}`, `D_{0,2}` or `D_{1,2}`.
It says nothing about the `d`-invariants of the same covers, which is a strictly
finer obstruction on the same metabolizers.

---

## 4b. The 3-fold cover too — and there it is vacuous *by theorem*

The natural next test is the same gate one cover up. `Δ = t⁴−3t³+5t²−3t+1` gives
`|H_1(Σ_3(K_n))| = |Δ(ω)Δ(ω̄)| = 49`, and the computation returns
`H_1(Σ_3) = (Z/7)²` for both `K_0` and `K_1`, with Gram matrices (times 7)

```
K_0 : [[1,3],[3,1]]   det = -8 ≡ 6 (mod 7)
K_1 : [[5,1],[1,0]]   det = -1 ≡ 6 (mod 7)
```

Same discriminant class, so the forms are isometric over `F_7` and a metabolizer
exists: **gate passed again.** The linking form is read off the Kauffman–Taylor
intersection form of the `p`-fold cyclic branched cover of `B⁴` over a pushed-in
Seifert surface (block tridiagonal in `V+Vᵀ`, `Vᵀ`, `V`), and every group order
produced is checked against an independently computed resultant
`|∏_j Δ(ζ_p^j)|`; all controls agree, including `Σ_3(3_1) = (Z/2)²`, the
quaternionic space.

That is not luck. Here is why it could never have fired:

> **Proposition C.** Let `p` be an odd prime, `K` a knot, and suppose
> `H_1(Σ_p(K))` is an elementary abelian `q`-group with `q` a prime satisfying
> `q ≡ 1 (mod p)`. Then the linking form of `Σ_p(K)` is hyperbolic. Consequently
> the `Σ_p` linking-form metabolizer obstruction vanishes identically on every
> difference of two such knots.

*Proof.* Write `H = H_1(Σ_p(K))`, an `F_q`-vector space, and let `τ` be the deck
transformation, of order `p`; it is an orientation-preserving diffeomorphism of
`Σ_p(K)`, hence preserves the linking form `λ`. Since
`H ≅ H_1(X_∞)/(t^p−1)` and `t−1` acts invertibly on the Alexander module
(`Δ_K(1) = ±1`), `τ − 1` is invertible on `H`; in particular `1` is not an
eigenvalue of `τ`. As `gcd(p,q) = 1`, `τ` is diagonalizable, and `q ≡ 1 (mod p)`
puts the primitive `p`-th roots of unity in `F_q`, so `H = ⊕_α E_α` over
eigenvalues `α ≠ 1` of order dividing `p`. For `x ∈ E_α`, `y ∈ E_β`,
`λ(x,y) = λ(τx,τy) = αβ·λ(x,y)`, so `E_α ⊥ E_β` unless `αβ = 1`. Nondegeneracy
of `λ` therefore makes the pairing `E_α × E_{α^{-1}} → F_q` perfect, so in
particular `dim E_α = dim E_{α^{-1}}`; and `α = α^{-1}` is impossible because
it forces `α² = 1` with `α ≠ 1`, i.e. `α` of order 2, while `α` has odd order
dividing `p`. So `H` is an orthogonal sum of hyperbolic planes
`E_α ⊕ E_{α^{-1}}`, each summand having both lines isotropic. ∎

For us `p = 3`, `q = 7`, and `7 ≡ 1 (mod 3)`. **The `p = 3` gate was vacuous
before it was run**, for `K_0`, `K_1`, `K_2` and indeed for any knot whose
3-fold branched cover has elementary abelian homology of exponent `7`, `13`,
`19`, … This is exactly the kind of check the campaign is supposed to make
before investing: an obstruction that provably vanishes on everything of the
relevant shape cannot separate anything.

The proposition also says where the gate *is* live: when `q ≡ −1 (mod p)`, the
eigenvalue argument does not apply, `τ` generates an `F_{q²}`-structure, and the
invariant form is the anisotropic norm form, whose discriminant is a non-square.
The Abe–Tagami family is simply not in that regime at `p = 3`.

`scripts/prop_c_census.py` tests both halves over the SnapPy knot table at
`p = 3, 5, 7` (Seifert matrices of size `≤ 12`), and the dichotomy is exact:

| case | hyperbolic | anisotropic |
|---|---:|---:|
| `q ≡ 1 (mod p)` | **372** | 0 |
| `q ≡ −1 (mod p)` | 0 | **271** |

Zero violations of Proposition C, and no case outside the dichotomy — as there
cannot be, since a fixed-point-free `Z/p` action on `(Z/q)²` forces the order of
`q` mod `p` to be 1 or 2. A census is corroboration, not proof; the proof is the
five lines above.

At `p = 5` the family leaves the reach of both tests: `|H_1(Σ_5(K_n))| = 256`
with `H_1 = (Z/4)^4`, not elementary abelian and of even order, so neither the
discriminant criterion nor the Gauss-sum criterion applies. A **ribbon-knot
control caught exactly this**: `8_20` is ribbon, so its `Σ_3` linking form on
`(Z/4)²` must be metabolic, yet its Gauss sum is `−8`, not `+√16 = 4`. The
Gauss-sum criterion `GS(λ) = +|H_1|^{1/2}` is therefore valid only for
odd-order `H_1`, and is recorded with that restriction rather than applied
where it would have given a false positive.

---

## 4c. The 5-fold cover, where the group is a 2-group — passed, with a certificate

`|H_1(Σ_5(K_n))| = 256` and the group is `(Z/4)^4` for both `n = 0, 1`. Even
order and not elementary abelian, so neither §4's discriminant criterion nor any
Gauss-sum criterion applies. The gate was therefore settled *constructively*: an
explicit isometry

```
φ : (H_1(Σ_5(K_0)), λ_0) → (H_1(Σ_5(K_1)), λ_1)
e_1 ↦ (1,0,0,0)   e_2 ↦ (1,1,1,0)   e_3 ↦ (2,0,3,0)   e_4 ↦ (0,1,2,1)
```

whose graph `{(x, φx)}` is a subgroup of order `256 = |G|^{1/2}` of
`H_1(Σ_5(K_0)) ⊕ H_1(Σ_5(K_1))` on which `λ_0 ⊕ (−λ_1)` vanishes. The script
does not report the search; it rebuilds the subgroup and checks **all 65,536
pairings and all 65,536 sums** exhaustively. So the `p = 5` gate is passed, with
a certificate any reader can re-verify from the two `4×4` Gram matrices
recorded in `results/opus_2026_09_17/sigma5_metabolizer_gate.json`.

Ribbon knots (`6_1`, `9_46`) are put through an independent direct metabolizer
search at `p = 5` as positive controls and both come back metabolic; `10_3`
gives `(Z/211)²`, too large for that search here, and is recorded as *not
attempted* rather than as a negative.

The certificate is then re-checked by `scripts/check_sigma5_certificate.py`,
which shares **no code** with the generator: it reads only the two stored `4×4`
Gram matrices and the stored generators, rebuilds the subgroup of `(Z/4)^8` from
scratch, and reports

```
group_order 65536 | required 256 | found 256 | closed_under_addition true
isotropic true | pairs_checked 65536 | CERTIFICATE_VERIFIES true
```

---

## 5. Negative results, stated as exclusions

* Seifert-form invariants are excluded **by theorem** (Lemma B), for the whole
  Abe–Tagami family and every difference `D_{n,m}`.
* The linking-form metabolizer obstruction of the branched cyclic cover is
  excluded, **by exact computation with verified certificates**, at `p = 2`
  (`Z/13`, for `D_{0,1}`, `D_{0,2}`, `D_{1,2}`), at `p = 3` (`(Z/7)²`) and at
  `p = 5` (`(Z/4)⁴`). At `p = 3` it is excluded *a priori* by Proposition C,
  for every knot of that shape.
* The Seifert-fibered/plumbing route to `d(Σ₂(K_1))` is excluded **conditionally
  on the numerical hyperbolicity** of `Σ₂(K_1)`.
* Destabilizing the specific trace annulus `C` is excluded by `research/14` §3.
  Theorem A does not weaken that; it sharpens it to "one stabilization".

None of these excludes a concordance `[K_0] = [K_1]`, and none of them is
evidence for one.

## 5b. The `K_DG` side: why the Abe–Tagami lane got this session

`K_DG = 18nh00000601` is certified smoothly slice in the standard `B⁴`
(Oliveira–Smith), so the first filter to apply to any proposed obstruction is:
*does it vanish on every smoothly slice knot?* If yes it cannot separate `K_DG`
from a ribbon knot, no matter how expensive it is. That filter is what the
"APPLIES BUT VANISHES" column of `OBSTRUCTION_MATRIX.md` already records, and it
kills every sliceness invariant outright — `τ`, `s`, `ν⁺`, `Υ`, `d`-invariants,
Casson–Gordon, twisted Alexander, Donaldson-type lattice embeddings.

Exactly two approaches survive the filter, and they fail for different reasons.

1. **Unlink-derivative necessity** (Meier–Zupan, as used in `research/02`,
   `research/06`): `K` is ribbon iff some derivative link on some — possibly
   heavily stabilized — Seifert surface is an unlink, while handle-ribbonness
   only gives an R-link. This is genuinely ribbon-specific, it is exactly the
   gap `OBSTRUCTION_MATRIX.md` identifies, and `K_DG` has a known non-unlink
   R-link derivative. It is blocked by two things at once: Generalized Property
   R, and the stabilization barrier (`research/06` §O4) — no known invariant is
   invariant under `L ↦ L ⊔ U`. Nothing in this session moves either.
2. **Eisermann-type Jones identities on satellites** (`research/28`,
   `research/31`, and the 16 September exact `q = i` computation). Ribbon-link
   identities are not slice-invariant, so they pass the filter, and the
   machinery is computable. But `K_DG`'s zero-framed 3-parallel passes
   (`determinant 6601`, nullity 2), Eisermann's own Question 7.8 leaves
   boundary-link automaticity open, and finitely many passing patterns prove
   nothing either way.

Given that, the Abe–Tagami lane is the better use of a bounded session: its
missing ingredient is a *concordance*, which is attackable by computable
obstructions that are not required to vanish on slice knots — because
`D_{0,1}`'s sliceness is precisely what is unknown. That is why this session
spent itself there. No new `K_DG` computation was run today, and none of the
above is a new result; it is the reasoned choice, recorded so the next session
does not re-derive it.

## 6. Reproduction

```sh
python3 scripts/annulus_trace_stabilization.py        results/opus_2026_09_17/annulus_trace_stabilization.json
python3 scripts/sigma2_linking_form_gate.py           results/opus_2026_09_17/sigma2_linking_form_gate.json
python3 scripts/sigma2_geometry_probe.py              results/opus_2026_09_17/sigma2_geometry_probe.json
python3 scripts/zero_surgery_algebraic_concordance.py results/opus_2026_09_17/zero_surgery_algebraic_concordance.json
python3 scripts/cyclic_cover_linking_form_gate.py     results/opus_2026_09_17/cyclic_cover_linking_form_gate.json
python3 scripts/cyclic_cover_gauss_sum_gate.py        results/opus_2026_09_17/cyclic_cover_gauss_sum_gate.json
python3 scripts/sigma5_metabolizer_gate.py            results/opus_2026_09_17/sigma5_metabolizer_gate.json
python3 scripts/prop_c_census.py                      results/opus_2026_09_17/prop_c_census.json
python3 scripts/check_sigma5_certificate.py   # independent re-check, exit 0 iff valid
```

The eight generating scripts refuse to overwrite an existing output. Environment: Python 3.11,
`snappy` 3.3.2, `regina` 7.4, `sympy` 1.14.0, no Sage. Seeds: SnapPy's
`randomize()` is used only to search for smaller triangulations and better
solutions; every reported conclusion is read off an isoSig or an exact integer
computation, never off a random search that failed.

## 7. Sources used, with the precise claim taken from each

* **Tetsuya Abe, Keiji Tagami**, *Fibered knots with the same 0-surgery and the
  slice-ribbon conjecture*, [arXiv:1502.01102](https://arxiv.org/abs/1502.01102).
  §2 and Appendix B: the definition of the `n`-fold annulus twist as
  `(+1/n)`/`(−1/n)` surgery on `c'_1, c'_2` in the annulus framing, and
  `K_n = A^n(6_3)`. Used for the slopes in §1.
* **Tetsuya Abe, In Dae Jong, Yuka Omae, Masanori Takeuchi**,
  [arXiv:1209.0361](https://arxiv.org/abs/1209.0361). Annulus twists preserve the
  zero surgery. Used for the hypothesis of Lemma B. *Restated from this
  repository's own reading, recorded in
  `data/knots/AbeTagami_K_n_NOTES.json`; not re-fetched today.*
* **Maciej Borodzik, Stefan Friedl**, *The unknotting number and classical
  invariants I*, [arXiv:1203.3225](https://arxiv.org/abs/1203.3225). LaTeX source
  fetched 2026-09-17. Two verbatim statements quoted in §2: the Blanchfield
  pairing lives on `M(K)`, and Trotter's completeness.
* **Hale F. Trotter**, *On S-equivalence of Seifert matrices*,
  Invent. Math. **20** (1973), 173–207. Blanchfield ⟹ S-equivalence.
  `SECONDARY RESTATEMENT` (via Borodzik–Friedl); the original was not obtained.
* **Robert E. Gompf, András I. Stipsicz**, *4-Manifolds and Kirby Calculus*,
  GSM 20, AMS 1999, ch. 4. `S²`-bundles over `S²` as Hopf links with framings
  `n` and `0`. `SECONDARY, NOT VERIFIED FROM ORIGINAL` — see §1.4, where the
  weaker Freedman statement is given as a citation-free fallback.
* **Louis H. Kauffman, Laurence R. Taylor**, *Signature of links*,
  Trans. Amer. Math. Soc. **216** (1976), 351–365. The `p`-fold cyclic branched
  cover of `B⁴` over a pushed-in Seifert surface and its block-tridiagonal
  intersection form, used in §4b and §4c. `STANDARD FORMULA, NOT VERIFIED FROM
  ORIGINAL HERE.` It is instead validated computationally: for every knot and
  every `p` tested, `|coker(A_p)|` equals the independently computed resultant
  `|Res(Δ_K, 1 + t + … + t^{p−1})|`, and at `p = 2` the construction reduces to
  `V + Vᵀ` and reproduces `λ(Σ_2(6_3)) = 5/13` for `L(13,5)`.
* `research/14` §3 (this repository): `π₁(W ∖ C) = Z` and the cyclic-group
  concordance-exterior lemma. Used in §1.6.
* `research/21` §3–4 (this repository): the `d`-invariant gate and the
  indefinite-Goeritz search. Used in §3.
