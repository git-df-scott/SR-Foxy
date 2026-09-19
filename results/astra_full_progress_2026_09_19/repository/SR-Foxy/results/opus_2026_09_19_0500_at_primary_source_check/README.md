# The stored Abe-Tagami family, checked against the primary source

19 September 2026, Opus. **CE: NO.**
**Smooth concordance `K_0 ~ K_1`: UNKNOWN. Slice-Ribbon CE: NO.**

`check_at_primary_source.py` -> `RESULTS.json`, **17/17**, SnapPy 3.3.2,
sympy 1.14.0, no Sage, no network at run time.

---

## 1. The gap this narrows

`results/opus_2026_09_19_0300_k1_identification/` §4 recorded the upstream
dependency in plain terms:

> the PD code of `L` itself is taken as committed, and nothing here re-derives
> it from Abe-Tagami's figures.

That cannot be fully closed here — the figures are pictures, and no amount of
computation reads a picture. But the paper also states numerical facts **in
words**, and those are checkable against the stored PD codes without ever
looking at a figure. Nobody in this campaign had done that.

## 2. The source

**Abe, T. and Tagami, K., _Fibered knots with the same 0-surgery and the
slice-ribbon conjecture_, arXiv:1502.01102, Math. Res. Lett. 23 (2016) 303-323.**
Fetched and text-extracted here. From the proof of Theorem 1.6, verbatim:

> "First, note that `K_0` is the fibered knot `6_3` in Rolfsen's knot table, see
> KnotInfo [12]. By Gabai's theorem in [20], `K_1` is also fibered since
> 0-surgeries on `K_1` and `K_2` give the same 3-manifold ... Here we can see
> that `K_0` and `K_1` are different knots (for example, by calculating the
> Jones polynomials of `K_0` and `K_1`). Also, we see that `K_0` and `K_1` have
> the same irreducible Alexander polynomial
> `Delta_{K_0}(t) = Delta_{K_1}(t) = 1 - 3t + 5t^2 - 3t^3 + t^4`."

And Example 5.4 / 5.5: `6_3` admits the annulus presentation `(A, b)` of Figure
4; `A(6_3)` is the right picture of Figure 5.

## 3. Result

`Delta` is computed **Sage-free** as the HFK Euler characteristic
(Ozsvath-Szabo), so this shares no code path with any Seifert-matrix routine.

| knot | crossings | `Delta` | fibered | genus |
|---|---|---|---|---|
| `K_0 = 6_3` | 6 | `t^4 - 3t^3 + 5t^2 - 3t + 1` | yes | 2 |
| `K_1` | 19 | same | yes | 2 |
| `K_2` | 41 | same | yes | 2 |
| `K_3` | 71 | same | yes | 2 |

All four match **the polynomial the paper states**, all four are irreducible
over `Z`, all four are fibered of genus 2 — consistent with `deg Delta = 2g` and
with an annulus twist being supported off a fiber surface, hence genus- and
fiberedness-preserving.

The stored family therefore reproduces every numerical assertion Abe-Tagami make
in words about it, including for `K_2` and `K_3`, which the paper does not
tabulate.

## 4. What this does NOT show

**Matching `Delta` does not identify `K_1` with `A_1(6_3)`.** Alexander
polynomials are very far from complete; this is a necessary condition that
passes, and calling it more would be exactly the failure mode
`ERRATA_2026-09-18_OPUS.md` records three times. The identification still rests
on the oriented isometry signature of
`results/opus_2026_09_19_0300_k1_identification/`, whose own residual gap
(`verified=True` needs Sage) is unchanged.

**The Jones polynomial check could not be run.** `spherogram`'s
`jones_polynomial` raises `SageNotAvailable` here, and a Kauffman state sum at
19 and 41 crossings is not worth the cores. The paper's own distinctness
argument is therefore not reproduced by its own method — but distinctness of
`K_0` and `K_1` is already established here more strongly, by oriented
isometry signature, which sees more than Jones does.

**Nothing here bears on the missing half of the lane.** `D_{0,1}` slice is still
MISSING, with no construction.

## Reproduce

```
python3 check_at_primary_source.py     # exit 0, 17/17
```
