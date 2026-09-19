# The d-invariant gate: one concrete route to it is now closed, with a control

19 September 2026, Opus. **CE: NO.** A bounded negative, and a record of two
failed controls that voided earlier versions of it.

---

## 1. The gate, and why it is the campaign's only live decisive test

`research/21` §3:

> `D_{0,1}` smoothly slice **⟹** the thirteen d-invariants of `Σ₂(K₁)` are, as a
> multiset, exactly those of `L(13,5)` = `{0, ±2/13, ±2/13, ±6/13, ±6/13, ±8/13, ±8/13}`.

A mismatch **proves `[K₀] ≠ [K₁]`** and closes the primary lane outright. It is
finite, falsifiable and small. It has never been evaluated, for one reason:
nothing here computes Heegaard Floer d-invariants of a closed hyperbolic QHS³.

The cheaper gates in the same family are already spent, and both **passed**:

* **Linking form** (`sigma2_linking_form_gate.py`, `research/33` §4):
  `λ(K₀) = 5/13`, `λ(K₁) = 6/13`, and `5·6 = 30 ≡ 4 (mod 13)` is a quadratic
  residue, so `λ₀ ⊕ (−λ₁)` is metabolic. No obstruction.
* **HKL / Casson–Gordon metabelian**: run on `D_{0,1}` — `None` in 0.8 s, it
  survives.

`results/opus_2026_09_17/sigma2_geometry_probe.json` establishes `Σ₂(K₁)` is
hyperbolic (19 tetrahedra, `H₁ = Z/13`, volume 7.2813263517), hence **not**
Seifert fibered, which removes the Ozsváth–Szabó plumbing algorithm.

## 2. The route tried here

If `Σ₂(K₁) = S³_{p/q}(J)` for some knot `J`, the Ozsváth–Szabó **rational
surgery formula** gives all thirteen d-invariants from the `V_i`, `H_i` of `J`,
turning the blocked gate into a computation. So: is it surgery on a knot?

`Σ₂(K₁)` is presented by SnapPy as the `(1,0)` filling of a **one-cusped**
manifold of volume **9.2540100733** with **`H₁ = Z`** — which is exactly the
homology of a knot exterior, so the question is live rather than idle.

## 3. Result: that cusped manifold is not a knot exterior in S³

By Gordon–Luecke a knot exterior in `S³` has exactly one slope whose filling is
`S³`, namely the meridian. Over all slopes `(a,b)` with `|a|,|b| ≤ 14`:

* only **two** fillings have trivial `H₁`: `(-5,11)` and `(-1,2)`;
* both are **hyperbolic**, of volume `9.0048191754` and `1.9122102501` — so
  neither is `S³`;
* no other slope can be `S³`, since `S³` has trivial `H₁`.

**Control (passes):** the same slope search finds the `S³` slope `(-1,0)` on the
exteriors of `4_1`, `3_1`, `6_3` and `5_2`. So the detector fires on genuine knot
exteriors, and the negative above is not a tool failure.

**Conclusion.** `Σ₂(K₁)`'s natural cusped presentation does **not** exhibit it as
surgery on a knot in `S³`, so the rational surgery formula cannot be reached that
way. Bounded: it says nothing about other drillings, and nothing about whether
`Σ₂(K₁)` is surgery on a knot via some other curve.

## 4. Two controls that failed first, and what they voided

Recorded because each one voided a negative I would otherwise have reported.

1. **Control was a lens space.** The first sweep used `Σ₂(K₀) = L(13,5)` as the
   control for a geodesic-drilling search. `L(13,5)` is **not hyperbolic**, so
   SnapPy returned **0 dual curves** and the control could not fire at all. The
   script's own `control_found_knot_exterior: false` voided the run. A drilling
   control has to be hyperbolic *and* known to be surgery on a knot.
2. **Drilling a filled manifold.** `M.drill(i)` on `Σ₂(K₁)` returns **two**
   cusps — the original (carrying the `(1,0)` filling) and the drilled geodesic.
   The first version unfilled **both**, which throws away the surgery that
   defines `Σ₂(K₁)` and tests an entirely different manifold. Visible in the log
   as `H1=Z + Z` on every row; after the fix, `H1=Z`.
3. The replacement control `S³_{13}(4_1)` also did not fire, and that is
   **correct behaviour**: its drilled geodesics give `H₁ = Z/13 + Z`, showing a
   random geodesic is not the surgery core. This is why the final control is on
   `meridian_slope` itself, the actually load-bearing sub-tool.

## 5. What is still open

The gate. `Σ₂(K₁)` is a 19-tetrahedron closed hyperbolic QHS³ with `H₁ = Z/13`
and no plumbing, no lens-space structure, and — via this presentation — no
knot-surgery description. Computing its d-invariants needs either a different
drilling that *is* a knot exterior, a negative-definite filling (40 randomized
Goeritz forms were indefinite, `research/21` §4), or bordered Floer.

That remains the single highest-value computation on this board: it is decisive
in one direction and would be the campaign's first positive evidence in the
other.

---

## 6. The full drilling sweep: still no knot-surgery description

`scripts/sigma2_knot_surgery_sweep.py` -> `results/opus_2026_09_19_1000_sigma2_surgery/sweep*.jsonl`.

§3 closed one curve. This sweeps every drillable geodesic of `Σ₂(K₁)`.

| | |
|---|---|
| dual curves reported by SnapPy | 122 |
| **actually drillable** (`drill()` accepts `range(28)`) | **28** |
| drilled complements with `H₁ = Z` | **26** (20 distinct by volume, 8.505 to 11.709) |
| slopes tested per complement | all `(a,b)`, `|a|,|b| <= 20` |
| **knot-exterior drillings found** | **0** |

Raising `max_segments` to 20, 30 and 40 does not enlarge the drillable set: it
stays at 28, so 28 is a SnapPy cap here, not a search parameter I can turn up.
**The 122 figure is the wrong denominator** — the first run of this sweep
recorded 94 `IndexError`s, and reading "0 of 122" off it would have overstated
the coverage more than four-fold.

**Control passes** on every run: `meridian_slope` recovers `(-1,0)` on the
exteriors of `4_1`, `3_1`, `6_3`, `5_2`.

### Statement of the negative, with its bounds

> No drillable geodesic of `Σ₂(K₁)` exhibits it as Dehn surgery on a knot in
> `S³`, over 28 drilled curves and slopes to `|a|,|b| <= 20`.

Bounded, not a theorem: SnapPy's drillable set is not every simple closed curve,
and a knot-surgery description could use a curve outside it or a slope outside
the box. But it does mean **the rational-surgery route to the d-invariants of
`Σ₂(K₁)` has been tried properly and does not open**, and the next person should
spend their time on a negative-definite filling or on bordered Floer rather than
re-running this.
