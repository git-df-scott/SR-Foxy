# Where a counterexample can actually come from

14 September 2026. **No counterexample found.** This note is strategy, not a
new object. It argues that the campaign's two routes are not merely hard in
different ways: one of them is provably harder than the problem being attacked,
and the one cheap lane that was supposed to escape both is vacuous as written.

## 1. The dichotomy, stated once

`{ribbon} ⊆ {handle-ribbon} ⊆ {homotopy-ribbon} ⊆ {slice}`, and Miller–Zupan
record that **none of these inclusions is known to be strict**.

- **Route A** (K_G, GST band sums, r=0 RBG pairs, Abe–Tange outputs): sliceness
  certified, ribbonness open. Every one of these is *handle-ribbon by
  construction*. research/02 audited the entire obstruction catalog and found
  no computable invariant whose vanishing theorem holds at the ribbon level but
  not at the handle-ribbon level. Route A is therefore blocked by a survey
  result, not by a shortage of compute.
- **Route B** (Miyazaki cables, Abe–Tagami `D_{n,m}`, Gompf–Miyazaki,
  Hom–Park): non-ribbonness certified, sliceness open.

## 2. Route B is strictly harder than the problem

Every non-ribbonness certificate in Tier B of `CANDIDATE_LEDGER.md` is in fact
a **non-homotopy-ribbon** certificate. Miyazaki's Theorem 5.5, which carries
the whole Abe–Tagami lane through Abe–Tagami Cor. 4.3, takes *homotopy-ribbon*
as its hypothesis; `ABE_TAGAMI_AUDIT.md` states this explicitly, and the ledger
writes the Miyazaki cables as "not (homotopy) ribbon". Hom–Park is recorded in
research/02 as "likely homotopy-ribbon, not verified to be ribbon-only".

So if `D01 = K_0 # (-K_1)` is smoothly slice, it is a slice knot that is **not
homotopy-ribbon**. That refutes

> (HR) every slice knot is homotopy-ribbon,

and HR false implies slice-ribbon false, because ribbon ⟹ homotopy-ribbon.
The converse fails: slice-ribbon could be false via a knot that is
homotopy-ribbon, even handle-ribbon, but not ribbon.

**Therefore the campaign's primary lane can only succeed by refuting a strictly
stronger conjecture than the one it is trying to refute.** That is worth
knowing when allocating effort. It does not make the lane wrong — it may still
be the only constructive path, since Teichner's lemma is the sole known
generator of a slice disk that is not automatically handle-ribbon — but the
price is explicit now.

The logically cheapest counterexample is the opposite shape: a knot that **is**
handle-ribbon and **is not** ribbon. By Miller–Zupan that is exactly a knot
with an R-link derivative and no unlink derivative, i.e. a Generalized
Property R failure realized as a derivative. research/02 already identifies the
missing ingredient: no theorem bounds or classifies the derivatives of a fixed
knot, so "no unlink derivative" is an infinite search. research/06–07 began
that theory for K_G (surface slides preserve derivatives; the two-lattice
lemma pins the homology span to one of two rank-5 lattices) and stalled for
want of an explicit fiber and monodromy.

## 3. The one computable ribbon-only tool, and where it can fire

research/02's catalog leaves exactly one computable, genuinely ribbon-only
family: **Eisermann's theorems for links**, dead for knots only because n = 1
makes them vacuous. Primary source re-read 14 September 2026
([arXiv:0802.2287](https://arxiv.org/abs/0802.2287), Geom. Topol. 13 (2009)):

- **Lemma 1.** Every n-component link satisfies `0 ≤ null V(L) ≤ n−1`.
- **Theorem 1.** Every n-component **ribbon** link satisfies `null V(L) = n−1`.
- **Theorem 2.** `det V(L) ≡ det(K_1)···det(K_n) (mod 32)`, so `≡ 1 (mod 8)`.

`null V(L)` is the multiplicity of the zero of `V(L)` at `q = i`;
`det V(L) = [V(L)/V(O^n)]` at `q = i`. Eisermann proves neither statement for
slice links: his Remark 3.6 gives only the classical nullity and signature, and
`Δ(L) = 0` for `n ≥ 2`. The slice case is untouched.

The test discriminates sharply. `scripts/eisermann_ribbon_link_gate.py`
reproduces `null V = n−1` on the unlinks `O²`, `O³`, `O⁴` with `det V = 1`,
and every non-ribbon link tried — Hopf, Whitehead, L6a1, Borromean, L7a1,
L8a21 — returns `null V = 0`, a maximal violation.

### 3.1 But Theorem 1 is vacuous on 2-component slice links

`CAMPAIGN_PLAN.md` WS5 proposes computing `null V(L_{3,1})` for GST's slice
link `L_{3,1}`, calling it "one afternoon of computation; expected to vanish".
It is worse than expected to vanish: it **cannot** fire.

A slice link with `n ≥ 2` has `Δ(L) = 0` (Eisermann, Remark 3.6), hence
`det(L) = 0`, hence `V(L)(q=i) = 0`, hence `null V(L) ≥ 1`. Lemma 1 caps
`null V(L) ≤ n−1`. For `n = 2` those two bounds meet, so `null V(L) = 1 = n−1`
holds automatically for *every* 2-component slice link. `L_{3,1}` has two
components. WS5 as written is therefore vacuous, and that half of the lane
should be closed by this argument rather than by running it.

### 3.2 Theorem 2 has teeth

Worth checking before recommending a construction. Of **75 tabulated
2-component links scanned, only two have `null V = 1` at all** — `L9n18` and
`L9n19`. Every other one has `null V = 0` and fails Theorem 1 outright. So
Theorem 2 is rarely even testable; and on both links where it is, it **fails**:
`det V = 9` and `25` against a component-determinant product of `1` (both
components of each are unknots). Neither link is slice — linking number 4,
signature −6 and −4 — so these are calibration, not candidates. But they show
Theorem 2 is a sharp constraint rather than a formality, and that a link can
satisfy Theorem 1 and be caught only by Theorem 2, which is exactly the shape
of the `L_{3,1}` test.

### 3.3 The `L_{3,1}` test, pre-registered

GST Figure 1 and Section 7: `L_{n,1}` is the **square knot `Q` interleaved with
`V_n = T_{n,n+1} # mirror(T_{n,n+1})`**; the components are algebraically
unlinked and 0-framed (Prop. 2.2); Section 8 proves the link slice. Both
components are of the form `K # −K`, hence ribbon, with
`det(Q) = det(V_3) = 9`. Theorem 1 holds automatically by §3.1, so the entire
test is the single congruence

> **if `L_{3,1}` is ribbon then `det V(L_{3,1}) ≡ 81 ≡ 17 (mod 32)`.**

A different residue makes `L_{3,1}` slice and not ribbon.

**Blocker.** The construction cannot be reconstructed from prose. GST describe
each summand as "an n-stranded spiral, with a full ±1 twist added relative to
the plane of the paper", interleaved — that is a figure, not a combinatorial
description, and guessing it would risk a *false* counterexample, which is the
worst available outcome. Diao–Pan–Yan (arXiv:2604.17737) implement an algorithm
to build these links explicitly but defer its details to a later paper and
publish no PD codes, braid words or data repository. So the gating task is
reading GST Figure 1 itself.

### 3.4 What is still live

1. **Theorem 2 on `L_{3,1}`.** `det V(L) ≡ det(K_1)det(K_2) (mod 32)` is not
   implied by `Δ(L) = 0`, and is defined precisely because Theorem 1 holds
   automatically. A violation would make `L_{3,1}` slice and not ribbon.
2. **Theorem 1 on a slice link with `n ≥ 3`.** There slice gives only
   `null V ≥ 1` while ribbon demands `n−1 ≥ 2`, so the bounds no longer meet
   and the test has room to fail.

Both need an object this repository does not have: `L_{3,1}` is not in
`data/knots/`. Regina's `ExampleLink.gst()` supplies the 48-crossing band-sum
**knot** `B_{3,1}`, not the link, and a band sum cannot be reversed without its
band. Building `L_{n,k}` from GST Figure 1 is the gating task for the whole
link lane, and it is the highest-value construction on the board that is not
another band search: it is the only place in the catalog where a computable
ribbon-only obstruction meets an open question.

## 4. Honest limits

A link-level counterexample would not settle Fox's Problem 25, which is about
knots. It would be the first slice-not-ribbon object of any kind, which is why
it is worth the construction, but the knot conjecture would remain open.

Nothing here is a new theorem. §2 is a chain of citations plus one elementary
implication; §3.1 is a three-line argument from Lemma 1 and Remark 3.6 that
should be checked by a second reader before WS5 is struck from the plan.

## 5. Reproduction

```sh
../knot-venv/bin/python scripts/eisermann_ribbon_link_gate.py \
    results/eisermann_ribbon_link_gate.json
```

Refuses to overwrite its output. `controls_pass` must be true: it asserts
`null V = n−1` with `det V = 1` on the three unlinks and `null V < n−1` on all
six non-ribbon controls.
