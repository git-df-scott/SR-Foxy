# Two ways to make Eisermann non-vacuous for knots, and why both fail

> Follow-up correction, 16 September: the seven cable computations below do
> **not** prove that the cable congruence is an identity, or close all
> ribbon-preserving satellite constructions. Eisermann's Proposition 6.13
> explicitly preserves ribbonness under ribbon patterns; Corollary 6.15 treats
> every parallel multiplicity. The discussion after Example 6.16 describes
> boundary-link automaticity as a possible explanation, referring to open
> Question 7.8. The blanket conclusions below are withdrawn. Primary source:
> https://pnp.mathematik.uni-stuttgart.de/igt/eiserm/publications/ribbonlinks.pdf
> A truncated exact Jones calculation and bounded KDG cable tests are recorded
> in `results/astra_2026_09_16_followup/`. Passing a modular test is inconclusive.

16 September 2026. **No counterexample to the Slice-Ribbon Conjecture was found.**
This note is a **negative result**, recorded at the same prominence a hit would
get, because both ideas are attractive enough that someone will have them again.

## The setting

`research/02` §0 and `research/22` §3 establish that Eisermann's theorems
([S-Eisermann], Geom. Topol. 13 (2009) 623–660) are the **only** computable,
genuinely ribbon-only obstruction in the whole catalogue — and that they are
useless on knots, because `n = 1` makes both statements vacuous:

* **Lemma 1.** `0 ≤ null V(L) ≤ n-1`.
* **Theorem 1.** `L` an `n`-component **ribbon** link ⟹ `null V(L) = n-1`.
* **Theorem 2.** `L` ribbon ⟹ `det V(L) ≡ det(K_1)⋯det(K_n) (mod 32)`.

So the obvious move is to manufacture a link out of a knot in a way that
**preserves ribbonness**, pushing `n` up to 2 or more. Two such constructions
were tried today. Both are vacuous, and the reason is the same both times.

---

## Attempt 1 — add a split unknot. Vacuous, provably.

Take `L ⊔ O`. Ribbonness is unaffected, and `n` goes up by one.

In Eisermann's convention the split-union factor is `δ = -q - q^{-1}`, and
`δ(i) = -i - i^{-1} = 0`. So **each split component contributes exactly 1 to
`null V`**. A 2-component slice link already has `null V = 1` automatically
(`research/22` §3.1), so `L ⊔ O` has `n = 3` and `null V = 2 = n-1` — automatic
again. The gap between what slice forces and what ribbon demands does not open.

Control run today, `controls_pass = True`: `null V(O^n) = n-1` for `n = 2, 3, 4`
with `det V = 1` throughout, which is exactly what pins the convention and
confirms `δ(i) = 0`. **Proved, modulo the standard split-union multiplicativity
of `V`.**

---

## Attempt 2 — the 0-framed 2-cable. Vacuous, empirically, and decisively so.

This one looked much better, and it is worth writing down why it looked good.

> If `K` bounds a ribbon disk `D ⊂ B^4`, the 0-framed pushoff `D'` is a **disjoint
> ribbon disk** (an isotopic copy of `D` has no local maxima either), and the
> pushoff framing is the Seifert framing because `H_2(B^4) = 0`. So the 0-framed
> 2-cable `K^{(2)} = K ∪ K'` is a **ribbon 2-component link**.
> Contrapositive: **`K^{(2)}` not a ribbon link ⟹ `K` not a ribbon knot.**

That implication is correct. And on `K^{(2)}`, Theorem 1 is still automatic
whenever `K` is slice (slice `K` ⟹ `K^{(2)}` slice ⟹ `Δ = 0` ⟹ `null V ≥ 1`,
capped at `n-1 = 1`) — but **Theorem 2 is not obviously automatic**:

> `K` ribbon ⟹ `det V(K^{(2)}) ≡ det(K)² (mod 32)`.

If that congruence ever failed on a slice knot, the knot would be slice and not
ribbon. Applied to `18nh00000601` it would settle the flagship lane.

**It never fails.** Built with the repository's own Seifert-framed cabling
(`scripts/cable.py`, `p = 2, q = 0`), Jones via `scripts/sagefree_jones.py`,
`null V`/`det V` via `scripts/eisermann_ribbon_link_gate.py`. Gate controls
first: `null V(O^n) = n-1`, `det V = 1`, for `n = 2, 3`.

| knot | slice? | cable cr | lk | `det K` | `null V` | `det V` | `det K²` | `det V − det K²` |
|---|---|---|---|---|---|---|---|---|
| `3_1` | **no** | 18 | 0 | 3 | 1 | −23 | 9 | −32 = −1·32 |
| `4_1` | **no** | 16 | 0 | 5 | 1 | 25 | 25 | 0 |
| `5_1` | **no** | 30 | 0 | 5 | 1 | −71 | 25 | −96 = −3·32 |
| `5_2` | **no** | 46 | 0 | 7 | 1 | −47 | 49 | −96 |
| `6_1` | ribbon | 52 | 0 | 9 | 1 | 49 | 81 | −32 |
| `6_2` | **no** | 28 | 0 | 11 | 1 | 25 | 121 | −96 |
| `6_3` | **no** | 24 | 0 | 13 | 1 | −23 | 169 | −192 = −6·32 |

Every row satisfies both theorems. **Six of the seven knots are not even slice**,
so their 2-cables are certainly not ribbon links — and the obstructions pass
anyway. `null V = 1 = n-1` in every row, `det V ≡ det(K)² (mod 32)` in every row,
with the difference an *exact* multiple of 32 each time.

**Conjecture (numerically supported, 7 knots, exact integer arithmetic, no
floating point):** `det V(K^{(2)}) ≡ det(K)² (mod 32)` for **every** knot `K`,
ribbon or not. If so, Theorem 2 on the 0-framed 2-cable is an identity, not a
test. Not proved here, and not needed: seven counterexample-free rows including
six non-slice knots already show the construction has no teeth.

---

## The lesson, which is the point of the note

Both attempts build the link **functorially from the knot**. When they do, `null V`
and `det V` end up determined by the knot's own classical data, and Eisermann's
conclusions become identities rather than constraints. That is not bad luck; it is
what "the statements are vacuous for `n = 1`" looks like after you push `n` up by a
construction that adds no independent information.

**So a future attempt should not try to manufacture a link from a knot at all.**
Eisermann bites only on a link whose components are genuinely independent data —
which is precisely why `research/22` §3.3 points at GST's `L_{3,1}`, a slice link
that is *not* built from any single knot, and why the gating task there remains
what it was: build `L_{3,1}` and verify it. See `research/27` for the state of
that blocker after the GST figures were rendered.

A corollary worth stating plainly: **Eisermann on knots is now closed by two
independent failures, not one.** Anyone proposing a third functorial construction
should expect the same outcome and should test it against the non-slice controls
above *before* spending compute on a candidate.

## Reproduction

`scripts/eisermann_two_cable_gate.py` (added today) builds the 0-framed 2-cable and
reports `null V`, `det V`, `det K` and the linking number, with `det K` taken from
the HFK Euler characteristic and the linking number counted from crossing signs,
both Sage-free. The `7_4`, `7_7` and `8_20` rows were launched and had not returned
when the session ended; their cables are 46+ crossings and the Kauffman-bracket
cost is exponential in girth. **Those three are UNKNOWN, not negative** — though
with seven rows already in hand the verdict does not depend on them.
