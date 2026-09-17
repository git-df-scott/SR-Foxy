# Trace-cap gate: the branched annulus-twist trace can never be capped to a negative definite filling

17 September 2026, 18:36 UTC. **CE: NO.** No counterexample, no disk, no
concordance, no definite filling.

This pass tested one proposed obstruction before spending anything on the
rank-seven matrix it was meant to guard, and the obstruction is **SOUND**. The
plan it kills is my own, from `research/34` §5a.

Read this pass: `research/33` §3, `research/34` §5/§5a,
`scripts/lifted_surgery_description.py`,
`results/opus_2026_09_17/lifted_surgery_description.json`,
`scripts/build_marked_product_scaffold.py` (lines 15–50),
and on `origin/main` at `f7ba2516304c0553a3180570abb6e257f4a68094`:
`results/astra_2026_09_17_overnight/pass08_0202_whisker_branch_gate/RESULTS.json`.
Nothing else was re-audited.

One-command check of every arithmetic fact below:

```sh
python3 results/opus_2026_09_17_1836_trace_cap_gate/check_trace_cap_gate.py   # exit 0
```

---

## 1. The lemma

Let `W` be the `n = 1` annulus-twist trace from `K_0` to `K_1`: `S³ × I` with
2-handles on `c'_1, c'_2` with framings 2 and 0, so `Q_W = [[2,1],[1,0]] ≅ H`
(verified `det = −1`). Let `C = K_0 × I ⊂ W` be the trace annulus and
`p : W_2 → W` its oriented double branched cover, with
`∂W_2 = (−Y_0) ⊔ Y_1`, `Y_i = Σ₂(K_i)`, both rational homology spheres
(`|H_1| = 13`).

> **Lemma.** `b₂⁺(W_2) ≥ 1` and `b₂⁻(W_2) ≥ 1`. Consequently, for any compact
> oriented `P` glued to either boundary component of `W_2` along a rational
> homology sphere, `Q_{P ∪ W_2} ≅ Q_P ⊕ Q_{W_2}` over `Q`, so `P ∪ W_2` is
> **indefinite in either orientation** and in particular is never negative
> definite.

**Proof.**

*(i) The cobordism really is `W_2`, and `p` extends across those exact handles.*
`C` is disjoint from `c'_1, c'_2` and `lk(K_0, c'_i) = 0`
(`results/opus_2026_09_17/annulus_trace_stabilization.json`), so each `c'_i`
lifts to two disjoint curves and each 2-handle lifts to two 2-handles. Hence
`W_2 = (Y_0 × I) ∪ (four 2-handles on the lifted curves)` and the branched
covering is defined on all of it. This is exactly the four-handle cobordism of
`research/34` §5, not a different filling with the same boundary.

*(ii) Both rational forms exist and are nondegenerate.* `∂W = S³ ⊔ S³` and
`∂W_2` is a disjoint union of rational homology spheres, so with `Q`
coefficients `H¹(∂;Q) = H²(∂;Q) = 0`. The pair sequence
`H¹(∂;Q) → H²(·,∂;Q) → H²(·;Q) → H²(∂;Q)` therefore gives isomorphisms
`H²(W,∂W;Q) ≅ H²(W;Q)` and `H²(W_2,∂W_2;Q) ≅ H²(W_2;Q)`. Define
`Q(a,b) = ⟨ã ∪ b̃, [·,∂·]⟩` using the **unique** relative lift. Poincaré–Lefschetz
makes both forms nondegenerate. Note both boundary components are used, and
both are rational homology spheres, so no component is exempt.

*(iii) Degree.* `p` is proper of degree 2 with `p(∂W_2) ⊆ ∂W`, so
`p_*[W_2, ∂W_2] = 2 [W, ∂W]`. Cup products are natural for **any** continuous
map, and the branch locus has codimension 2, so by the projection formula
`Q_{W_2}(p^*a, p^*b) = ⟨p^*(ã ∪ b̃), [W_2,∂W_2]⟩ = ⟨ã ∪ b̃, p_*[W_2,∂W_2]⟩
= 2 Q_W(a,b)`. Branching does not enter: nothing here needs `p` to be a covering
map away from a set of measure zero beyond what degree already encodes.

*(iv) Injectivity.* If `p^*a = 0` then `2 Q_W(a,b) = 0` for all `b`, and `Q_W`
is nondegenerate, so `a = 0`. Hence `V := p^*H²(W;Q)` has dimension 2.

*(v) Indefiniteness.* `Q_{W_2}|_V ≅ 2 Q_W = [[4,2],[2,0]]`, `det = −4 < 0`
(verified), so `Q_{W_2}|_V` is nondegenerate of signature `(1,1)`. A
nondegenerate subspace splits off orthogonally, so `b₂⁺(W_2) ≥ 1` and
`b₂⁻(W_2) ≥ 1`.

*(vi) Gluing.* If `Y` is the rational homology sphere along which `P` is glued,
`H₂(Y;Q) = H₁(Y;Q) = 0`, so Mayer–Vietoris gives
`0 → H₂(P;Q) ⊕ H₂(W_2;Q) → H₂(P ∪ W_2;Q) → 0`, and classes supported in the two
pieces are orthogonal. Hence `Q_{P ∪ W_2} ≅ Q_P ⊕ Q_{W_2}` over `Q` and
`b₂⁺ ≥ 1`.

*(vii) Orientation.* `−W_2` carries `−Q_{W_2}`, which still has `b₂⁺ ≥ 1` and
`b₂⁻ ≥ 1`. So neither orientation of the capped trace is definite. ∎

**Independent cross-check.** For a double cover branched over a properly
embedded surface `F`, `σ(W_2) = 2σ(W) − ½[F]²`. Here `σ(W) = 0` (rank 2,
`det < 0`) and `[C]² = 0` (`C = K_0 × I` carries a product normal framing and is
pushed off itself), so `σ(W_2) = 0`. With `b₂(W_2) ≥ 2` from (iv) that forces
indefiniteness independently of the pullback argument. Two proofs agree.

## 2. Application, stated as narrowly as it deserves

**Excluded:** the specific plan of `research/34` §5a — cap the branched trace
`W_2` with the negative definite plumbing `P(−3,−3,−2)` bounding `L(13,5)` and
hope for a rank-seven negative definite filling of `Σ₂(K_1)`. Handle slides
preserve the form up to isometry and negative blow-ups only add `⟨−1⟩`
summands, so neither can remove a positive direction that lives in a
nondegenerate rational subspace.

**Not excluded:** (a) other, non-trace negative definite fillings of `Y_1`;
(b) Donaldson-type arguments in general; (c) any `d`-invariant or Floer
argument; (d) sliceness of `D_{0,1}`. **This lemma says nothing whatever about
whether `D_{0,1}` is slice.**

## 3. Orientations, and the correct Donaldson statement

**The orientation gate dissolves, by a fact rather than a convention.**
`5² ≡ −1 (mod 13)` and `5·8 ≡ 1 (mod 13)` (verified), so
`L(13,5) ≅ L(13,5^{-1}) = L(13,8) = L(13,−5) = −L(13,5)`. `Y_0` is
**amphichiral**, so the question "does `P(−3,−3,−2)` bound `Y_0` or `−Y_0`" has
the same answer either way and no convention needs to be fixed. (`P` verified
negative definite with `det = −13 = −|H_1(Y_0)|`.) This reproduces
`research/21` §3 independently.

**The obstruction, stated completely.** `D_{0,1}` slice means `K_0` and `K_1`
are smoothly concordant. It does **not** mean `K_1` is slice, and it does
**not** mean `Y_1` bounds a rational homology ball. What it gives is: the double
branched cover of the concordance is a **rational homology cobordism** `V` from
`Y_0` to `Y_1` (`b₂(V;Q) = 0`), equivalently `Σ₂(D_{0,1}) = Y_0 # (−Y_1)` bounds
a rational homology ball `Z`.

So a Donaldson argument needs an explicit negative definite filling `X_1` of
`−Y_1`, which nobody has. Given one, `P ♮ X_1` has boundary `Y_0 # (−Y_1)` and
`(P ♮ X_1) ∪_∂ (−Z)` is a **closed** smooth oriented negative definite
4-manifold with `b₂ = 3 + b₂(X_1)`. Donaldson's diagonalizability theorem then
forces `Q_P ⊕ Q_{X_1}` to embed as a finite-index sublattice of
`⟨−1⟩^{3 + b₂(X_1)}`.

**The correct target lattice is `⟨−1⟩^{3 + b₂(X_1)}`, not `⟨−1⟩⁷`.** The
rank-seven figure came from using the trace as the filling, which §1 now
excludes. Demanding a rank-seven embedding would also have silently treated
`Y_1` as rationally null-cobordant, which it is not known to be.

A definite form alone is not a contradiction; an indefinite form alone gives no
`d`-invariant shift. The additional data the theorem needs — an explicit `X_1`,
its form, and the oriented gluing — is not in hand.

## 4. Constructive pivot: what the based product-disk map still needs

Pass08 found 49 fixed-meridian `SL(2,F_5)` boundary colourings, 36 with witness
data on both factors, 24 separating the crossed axes and 12 not. Its own
interpretation is the right one: *"Unbased end-circle data do not select the
actual product-disk based-whisker branch."* Those counts are not success
probabilities and do not identify the physical map.

One small thing is now settled. `scripts/build_marked_product_scaffold.py`
builds the double from `upper, lower = original.copy(), original.mirror()`, and
`spherogram`'s `.mirror()` **preserves crossing labels exactly** (checked: label
multisets equal on all 27 crossings, component lengths `[34, 8, 12]` on both
sides, signs flipped). So the lower→upper correspondence needed for the based
map is canonically available from stored data: it is the identity on crossing
labels, made explicit by the scaffold's own `(label, side)` relabelling. The cut
is recorded exactly, at `upper` crossing 0 index 0 and `lower` crossing 0 index
`sign % 4 = 3`, with `pairing: corresponding endpoints, not crossed endpoints`.

**What is still missing is only the whisker**, and the scaffold admits it in its
own `orientation_limit` field: *"Explicit product boundary orientations and band
whiskers must be tracked before any surgery/concordance certificate."* The based
map `φ` is: Wirtinger generators of the lower half `↦` their label-matched upper
counterparts, conjugated by the transport word along a path from the basepoint
through the glued arcs `f1[i1] = g1[j1]`, `f2[i2] = g2[j2]`. Producing that
transport word is the next concrete step; it was **not completed in this pass**
and no claim is made about which of the 12 surviving branches is physical.

## 5. Honest scope

* The lemma is pure algebraic topology and needs no new computation; the
  checker only confirms the arithmetic it quotes.
* Nothing here was rerun: not the 65,536 fillings, not `s`, HKL, Floer, the
  `D01` parallels, or the KDG four-parallel.
* `research/34` §5's surgery description is untouched and remains correct; what
  is excluded is one 4-dimensional use of it.
* Whether the fillings found by that bounded slope search are the
  covering-induced ones was **not** established, and the lemma does not need it:
  it is proved about `W_2` itself, defined by the branched cover, not about any
  filling matched only on the boundary.
