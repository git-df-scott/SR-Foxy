# The GST figures are readable, and the stored `B_{3,1}` survives every slice test I can run

16 September 2026. **No counterexample to the Slice-Ribbon Conjecture was found.**
Two results, one negative-but-useful and one that removes a blocker this repository
has carried since `research/22`.

---

## 1. The stated blocker on the Eisermann lane was "read GST Figure 1". That is now done.

`research/22` §3.3 and `CAMPAIGN_PLAN.md` both stop at the same place:

> GST describe each summand as "an n-stranded spiral, with a full ±1 twist added
> relative to the plane of the paper", interleaved — that is a figure, not a
> combinatorial description ... **So the gating task is reading GST Figure 1
> itself.**

The figures ship in the arXiv source of [S04] (`arxiv.org/e-print/1103.1601`) as
individual PDFs, and render cleanly with `pymupdf` at 6× (no poppler, no
ImageMagick, no LaTeX needed). They are archived at `figures/gst_source/`:

| file | is | shows |
|---|---|---|
| `Ln1_z6.png` | **Figure 1** | `L_{n,1}`, the 2-component slice link |
| `sliceknot_z6.png` | **Figure 2** | `B_{3,1}`, "A slice knot that might not be ribbon" |
| `Lnk_z6.png` | Figure 8 | the general `L_{n,k}` |
| `Gompffig1b_z6.png`, `Gompffig3b_z6.png`, `Gompffig5_z6.png` | Kirby diagrams | the handle picture `L_{n,k}` is blown down from |
| `squareknot_z6.png` | | the square knot `Q` |

### What Figure 1 actually shows

Read off the rendering, and consistent with the surrounding prose (`Text.tex`
lines 110–116, 713):

* **Black component** = `V_n = T_{n,n+1} # mirror(T_{n,n+1})`. It is drawn as **two
  spirals**, left and right, each an `n`-stranded spiral closed off, joined across
  the middle of the figure by two long black arcs. Each spiral carries one **twist
  box**, drawn as a rectangle at the far left and far right of the figure. The
  `\pinlabel` directives in `Text.tex` (lines 106–107) label them **`-1`** (left)
  and **`+1`** (right) — that is the `±1` full twist of the prose, one per
  summand, and it is what makes the right spiral the *mirror* of the left.
* **Green component** = the square knot `Q = 3_1 # (-3_1)`, drawn interleaved
  through both spirals. Its two visible clasp regions are the two crossings-pairs
  in the upper middle and centre of the figure.
* **Red dashed arc** = the band. It sits on the right, connecting the green
  component to the black one, and the band move along it produces Figure 2.

So the only non-literal content in Figure 1 is the two twist boxes, and a **full
`±1` twist on `n` strands is the braid `(σ_1 σ_2 ⋯ σ_{n-1})^{±n}`** — at `n = 3`
that is `(σ_1σ_2)^{±3}`, six crossings each. Figure 2 is a literal knot diagram
apart from the same two boxes.

### What this does and does not unblock

It converts the blocker from **"read a figure"** to **"trace ~36 crossings from a
raster image without a single error, then verify"**. That is a real reduction, and
it is still not free: `research/22` §3.3's warning stands, and a mis-traced strand
yields a *false* counterexample, the worst available outcome. **I did not trace it,
and no PD code for `L_{3,1}` is claimed here.** The verification protocol that a
future attempt must pass is unchanged and is stated in
`research/22` §3.3: two components, identified as `Q` and `V_3` on their own;
linking number 0; and the band sum along GST's band reproducing `B_{3,1}`.

Diao–Pan–Yan (arXiv:2604.17737) was re-checked in full LaTeX source today and
still contains **no** PD code, braid word, DT code or data repository — 635 lines,
entirely figure-driven. Nothing there shortcuts the tracing.

---

## 2. `TOOLING.md` fact 7's "discrepancy" on the stored GST knot is resolved: it is not a discrepancy

`TOOLING.md` fact 7 has stood unresolved:

> Regina's built-in `ExampleLink.gst()` (48 crossings, docstring: GST Figure 2)
> computes as genus 10, **non-fibered**, Δ of degree 16 ... **the object must be
> reconciled with GST Figure 2 by hand before use.**

GST prove `B_{3,1}` is **smoothly slice** (Section 8, via the 4-manifold being
`B^4` [Go1]). So every slice obstruction must vanish on it. That is a sharp,
cheap test of the stored object, and it had never been run because `Δ` needed
Sage, which this container does not have.

`scripts/fox_milnor_sagefree.py` gets `Δ` from the **HFK Euler characteristic**,
`Δ_K(t) = Σ (-1)^M rk HFK(K;A,M) t^A`, so no Seifert matrix and no Sage; then
factors over `Z` with sympy and decides Fox–Milnor exactly — every irreducible
factor not associate to its own reverse must pair with that reverse at equal
multiplicity, and every self-reciprocal irreducible must occur to even
multiplicity.

**Controls, all eleven correct** (`controls_pass = True`): the ribbon knots `6_1`,
`8_8`, `8_20`, `9_41`, `9_46`, `10_3` all read `norm = True`; the non-slice knots
`3_1`, `4_1`, `5_2`, `6_2`, `7_4` all read `norm = False`.

**Result on `data/knots/GST_B31_regina.json`:**

| test | required if slice | computed | |
|---|---|---|---|
| `τ` | 0 | **0** | ok |
| `ν` | 0 | **0** | ok |
| `ε` | 0 | **0** | ok |
| `det` a perfect square | yes | **1** = 1² | ok |
| `deg Δ ≤ 2·genus` | yes | 16 ≤ 20 | ok |
| **Fox–Milnor** `Δ ≐ f(t)f(1/t)` | yes | **yes**, with an explicit witness | ok |

The witness, which is the whole point:

```
Δ = t^16 - 2t^15 + t^14 + 2t^12 - 5t^11 + 2t^10 + 7t^9 - 13t^8
       + 7t^7 + 2t^6 - 5t^5 + 2t^4 + t^2 - 2t + 1
  = f_1 · f_2,   f_1 = t^8 - 2t^7 + t^6 + t^5 - 2t^4 + t^3 - 1
                 f_2 = t^8 - t^5 + 2t^4 - t^3 - t^2 + 2t - 1
```

both irreducible over `Z`, and `reverse(f_1) = -f_2` exactly. So `Δ ≐ f_1 f_1*`.

**Verdict: the stored object passes every slice necessary condition computable
here.** `TOOLING.md` fact 7's flagged discrepancy — non-fibered, genus 10 — is
*not* a discrepancy: the ledger already records fiberedness of `B_{3,1}` as
UNKNOWN, `deg Δ = 16 < 20 = 2g` is exactly what a **non-fibered** knot looks like,
and nothing about GST's construction forces `B_{3,1}` to be fibered.

**What this is not.** Passing every slice obstruction is *consistency*, not
identification. It does **not** prove Regina's `gst()` is `B_{3,1}`; it proves the
object is not disqualified from being it, which is what fact 7 asked and what had
never been checked. A genuine identification still needs the trace of Figure 2.
Had any row above failed, the stored object would have been provably *not* GST's
knot, and every `GST` column in `OBSTRUCTION_MATRIX.md` would have needed
retracting. It did not fail.

### One methodological note, recorded because a control caught it

The first version of the Fox–Milnor routine normalised `Δ` by shifting the lowest
*Alexander grading* to degree 0 rather than the lowest *nonzero coefficient*. For a
non-fibered knot the extreme Alexander grading can carry Euler characteristic
zero, which leaves a spurious factor of `t` in the factorisation — and `t` has no
reverse, so **every non-fibered knot would have read "not a norm"**, including the
GST object. The bug is fixed in `scripts/fox_milnor_sagefree.py` and is called out
in its docstring. It would have produced a spectacular and entirely false erratum.

---

## 2b. Audit sweep: every stored object behaves as it should

`results/fox_milnor_audit_2026-09-16.json`, produced with the same tool. The point
of the sweep is integrity: any object the ledger treats as slice that *failed*
Fox–Milnor would be a serious bug, since `Δ` had never been checked without Sage.

| object | cr | g | fibered | `det` | square | Fox–Milnor |
|---|---|---|---|---|---|---|
| `10_17_2_1-cable` | 41 | 8 | yes | 1 | yes | **norm** |
| `18nh00000601` (`K_G`) | 18 | 5 | yes | 25 | yes | **norm** |
| `AbeTagami_D_0_1` | 25 | 4 | yes | 169 | yes | **norm** |
| `AbeTagami_D_0_2` | 47 | 4 | yes | 169 | yes | **norm** |
| `GST_B31_regina`, `GST_knot` | 48 | 10 | no | 1 | yes | **norm** |
| `HomPark_P` | 104 | 14 | yes | 9 | yes | **norm** |
| `K_0 = 6_3`, `K_1`, `K_2`, `K_3` | 6–71 | 2 | yes | 13 | **no** | **not a norm** |
| `CONTROL_3_1` | 3 | 1 | yes | 3 | **no** | **not a norm** |

**No integrity problem found.** Every certified-slice or candidate object passes;
every object that is *known not to be slice* fails, correctly — the `K_n` are
concordant to `6_3` and `det 13` is not a square, and the repository's own
`CONTROL_3_1` fires. That the non-slice rows fail is what makes the passing rows
mean anything.

Two incidental notes. `HomPark_P` at 104 crossings passing is the first
confirmation in this repository that the stored Hom–Park knot is algebraically
slice as [S08] constructs it. And `AbeTagami_D_0_2` passing — `det 169 = 13²`,
`Δ` a norm — says the classical obstructions all vanish on it, which is exactly
why the `s`-invariant was the right next tool there and why the three failed
attempts in `UNFINISHED.md` §3 were worth making.

## 3. What this does not do

It does not produce a counterexample, and it does not bring one closer by any
amount that should be called progress. The Eisermann lane still needs `L_{3,1}`
traced and verified; the Teichner lane still needs a machine that stays up longer
than this container (see `UNFINISHED.md` §3); `s(D_{0,2})` still needs more memory
than this container has. What changed today is that the Eisermann blocker is now a
tracing job rather than an access problem, and that one long-standing
reconciliation item is closed in the direction that keeps the GST lane alive.
