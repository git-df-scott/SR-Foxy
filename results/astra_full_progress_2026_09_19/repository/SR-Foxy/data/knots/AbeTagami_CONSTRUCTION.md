# Abe–Tagami knots K_n = A^n(6_3) — construction and verification

Source: T. Abe, K. Tagami, *Fibered knots with the same 0-surgery and the slice-ribbon
conjecture*, arXiv:1502.01102.  Figures `annulus-pre`, `annulus-twist`, `fig`.

Everything below was produced by `build.py` (diagram → PD code), `assemble.py`
(verification + JSON output).  No PD code was guessed: the 3-component link `L` was
built from an explicit planar layout read off Figure `annulus-pre`, and every knot
`K_n` was **recovered from a Dehn filling of `L`'s exterior**, not transcribed.

## 1. Reading the annulus presentation

Figure `annulus-pre` (right) shows the knot `6_3` as `(A, b)`:

* `A` is an **unknotted annulus with one `+1` full twist**, drawn as a rounded
  rectangular band; `∂A = c_1 ∪ c_2` with `c_1` the inner and `c_2` the outer boundary.
* `b` is a band joining `c_1` and `c_2`; `6_3 = (∂A \ b(∂I×I)) ∪ b(I×∂I)`.
* Figure `annulus-twist` (left) shows the shrunken annulus `Ã ⊂ A`; `∂Ã = c'_1 ∪ c'_2`
  with `c'_1` parallel to `c_1` (inner) and `c'_2` parallel to `c_2` (outer).

So on the **left wall** of the rectangle four parallel strands run vertically; from
outside in they are

```
x = 0 : c_2      x = 10 : c'_2      x = 20 : c'_1      x = 30 : c_1
```

and on the **right wall** the four strands perform one full twist, i.e. the 4-braid
`Δ² = (σ1 σ2 σ3)^4`.  (This is the "one full twist" of `A`, applied to all four
parallel copies at once.)

### The band, read off the figure

Zooming on `annulus-pre` (600 dpi crops, see `hourglass.png`, `lp_vline.png`,
`ap_r_band.png`) the band's two edges `A` (outer) and `B` (inner) run as follows,
starting from the attaching arc on `c_2` near the top-left corner:

1. **attach 1** on `c_2` (left wall, just below the top-left corner);
2. leave the rectangle to the left, run **down** outside everything;
3. **one self-crossing of the band** (an "hourglass": the two band edges cross once —
   the half twist forced by the fact that `c_1` and `c_2` are anti-parallel as `∂A`).
   The strand running upper-left → lower-right passes **over**;
4. turn right and run **rightwards, over `c_2` and over `c'_2`**, stopping between
   `c'_2` and `c'_1`;
5. hairpin U-turn upwards, then run **leftwards, under `c'_2` and under `c_2`**
   (this is the ribbon intersection with `int A`, drawn dotted in the figure);
6. hairpin U-turn upwards, then run **rightwards, over `c_2`, over `c'_2`, over `c'_1`**,
   and **attach 2** on `c_1`.

The resulting diagram has `9` crossings for the knot alone — exactly the number of
crossings visible in the left-hand `6_3` picture of Figure `annulus-pre` (2 in the full
twist, 1 in the band's half twist, 6 where the three band strips meet the left edge of
`c_2`).  Adding `c'_1, c'_2` gives `12 + 1 + 14 = 27` crossings for `L`.

## 2. Sign convention

Two binary choices were left open by the drawing (handedness of the full twist, and
which band edge is over at the half twist).  All four combinations were built and the
knot component identified:

| full twist | band half twist | knot component |
|---|---|---|
| `+` | as drawn | `6_2` |
| `+` | flipped   | `9_42` |
| `−` | as drawn  | **`6_3`** ✓ |
| `−` | flipped   | `8_20` |

So the diagram as drawn in the paper, in my coordinate convention, needs
`sign = -1` (i.e. the braid generators of the full twist are negative in my
orientation of the right wall) together with the half twist as read.  With that choice

```
lk(c'_1, c'_2) = +1 ,  lk(K, c'_1) = lk(K, c'_2) = 0
```

so the annulus framing of `c'_i` is `+1` with respect to the Seifert framing, matching
the paper's "unknotted annulus with a `+1` full-twist".

## 3. Annulus twist as Dehn surgery

Abe–Tagami, §2: an `n`-fold annulus twist is `(+1/n)`-surgery on `c̃_1` and
`(−1/n)`-surgery on `c̃_2` **with respect to the framing induced by `A`**; and for an
unknotted annulus with `k` full twists this is `(k + 1/n)` and `(k − 1/n)` in Seifert
framing.  Here `k = +1`, so in SnapPy `(meridian, longitude)` coordinates:

```
c'_1  ↦  (n+1, n)        c'_2  ↦  (n-1, n)
```

with cusp 1 = `c'_1`, cusp 2 = `c'_2` of `L.exterior()`.  These slopes are confirmed by
the checks below; in particular `n = 0` (fillings `(1,0), (1,0)`) returns the `6_3`
exterior, and `n = -1` returns the `6_3` exterior, i.e. `K_{-1} = K_0`, and
`vol(K_{-n-1}) = vol(K_n)` throughout — exactly the paper's `K_n = K_m ⟺ n=m` or
`n+m=-1`.

## 4. Verification summary

See the `verification` dicts in the JSON files for the machine output.  All checks pass.

* **(a)** `c'_1 ∪ c'_2` simplifies to a 2-crossing diagram with `lk = +1`, `π_1` of its
  exterior is `⟨a,b | [a,b]⟩ = Z²`, and its exterior has the same Regina isoSig
  (`dLQacccbjkg`, after `simplifyExhaustive`) as `snappy.Manifold('L2a1')` — the Hopf
  link.  Linking matrix of `L` is `[[0,0,0],[0,0,1],[0,1,0]]`.
* **(b)** the knot component simplifies to a 6-crossing diagram whose exterior is
  isometric to `snappy.Manifold('6_3')`; `Δ(t) = t⁴−3t³+5t²−3t+1`; HFK: fibered,
  Seifert genus 2.
* **(c)** for `n = 1,2,3`, after filling `c'_1, c'_2` the remaining manifold, filled
  along the knot meridian `(1,0)`, is `S³` (Regina `isSphere()` = True).
* **(d)** filling the knot cusp along `(0,1)` gives a manifold isometric to the
  `0`-surgery on `6_3`, volume `4.059766425638614` for every `n`.
* **(e)** `n = 0` and `n = −1` both give the `6_3` exterior; `n = 1` and `n = −2` give
  isometric exteriors (vol `9.12000650079812`); `n = 2` and `n = −3` (vol
  `11.2414892516150`); `n = 3` and `n = −4` (vol `12.5204720623389`).
* **(f)** each recovered `K_n` has `Δ(t) = t⁴−3t³+5t²−3t+1` and is fibered of genus 2.
* **(g)** the three volumes above are distinct, so `K_1, K_2, K_3` have pairwise
  non-isometric (hence distinct) exteriors.

## 5. Recovered diagrams

`K_n` is recovered as `L.exterior()` with `c'_1, c'_2` filled, then
`filled_triangulation().exterior_to_link()` followed by randomized
`backtrack`/`simplify('global')`.  Each recovered knot's exterior was checked to be
isometric to the filled manifold it came from.

* `K_1` : 19 crossings   (vol 9.120006500798)
* `K_2` : 41 crossings   (vol 11.241489251615)
* `K_3` : 71 crossings   (vol 12.520472062339)

As an extra sanity check (the paper's own argument that `K_0 ≠ K_1`), the Jones
polynomials differ:

```
V(K_0) = -q^-6 + 2q^-4 - 2q^-2 + 3 - 2q^2 + 2q^4 - q^6
V(K_1) = -q^-18 + q^-16 - q^-14 + q^-12 + q^-8 - q^-6 + 2q^-4 - 2q^-2 + 2
         - 2q^2 + q^4 - q^8 + q^10
```

## 6. Connected sums

`D_{i,j} = K_i # (−K_j)` where `−K` = reverse of the mirror.  Mirroring uses
`spherogram.Link.mirror()`; orientation reversal is implemented in `tools.reverse_pd`
by reversing the edge labelling of the PD code (`e ↦ 2n−1−e`) and rotating each
`X[a,b,c,d]` to `X[c,d,a,b]`; connected sum uses
`spherogram.Link.connected_sum`.  Each `D` is checked to have
`Δ_D(t) = Δ(t)² = t⁸−6t⁷+19t⁶−36t⁵+45t⁴−36t³+19t²−6t+1`, and HFK gives
fibered with Seifert genus 4 for all three.  Sizes: `D_{0,1}` 25 crossings,
`D_{1,2}` 60, `D_{0,2}` 47.

## Files

* `build.py`   — the planar layout and the geometric PD-code builder
* `tools.py`   — orientation reversal of a knot PD code
* `assemble.py`— runs every check and writes the JSON files
* `L_63_c1_c2.json`, `K_1.json`, `K_2.json`, `K_3.json`,
  `D_0_1.json`, `D_1_2.json`, `D_0_2.json`

## 7. PD code of L (SnapPy / spherogram, 0-indexed)

```
[[3, 12, 4, 13], [15, 2, 16, 3], [33, 16, 0, 17], [0, 28, 1, 27], [28, 2, 29, 1], [4, 32, 5, 31], [5, 47, 6, 46], [6, 36, 7, 35], [7, 24, 8, 25], [49, 9, 50, 8], [38, 10, 39, 9], [21, 10, 22, 11], [32, 12, 33, 11], [44, 13, 45, 14], [14, 43, 15, 44], [41, 18, 34, 19], [52, 17, 53, 18], [19, 40, 20, 41], [20, 51, 21, 52], [37, 22, 38, 23], [48, 23, 49, 24], [34, 26, 35, 25], [53, 27, 42, 26], [29, 43, 30, 42], [45, 31, 46, 30], [47, 37, 48, 36], [39, 51, 40, 50]]
```

Component order in this PD labelling is `K`, `c'_1`, `c'_2`, matching cusps 0, 1, 2 of
`spherogram.Link(pd).exterior()`.  That the cusp order is *not* swapped is itself
verified: with the slopes above, `n = −1` gives the `6_3` exterior (so the filling
family really is `A^n`, not `A^{−n}`, since `A^{−1}(6_3) = K_{−1} = K_0`).
