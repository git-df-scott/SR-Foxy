> **RETRACTED 19 September 2026.** The link built here is **`L_{0,1}`**, not
> `L_{1,1}`. It is `L10n36`, 10 crossings (6 self + 4 inter), in the certified
> `RibbonLinks` census. `V_0` and `V_1` are both unknots, so every check below
> is satisfied by either member and none of them selects the index. See
> `RETRACTION_IT_IS_L01.md`. Rung 1 of the ladder is NOT done.

# `L_{1,1}` is built, and rung 1 of the GST ladder returns 9

**19 September 2026. CE: NO.** `research/53` §3's calibration ladder has a first
rung for the first time. `det V(L_{1,1}) = 9 (mod 32)`, as pre-registered.

## The blocker was a false premise

`research/22` §3.3 and `research/53` §2 gate this lane on "`L_{3,1}` is a
picture, not a combinatorial description", with tracing judged too risky
because the figure is a **raster**. It is not. `arXiv:1103.1601` ships its
LaTeX source, and `Ln1.eps` / `Ln1.pdf` (Figure 1) are **vector**. The path
data gives exact coordinates, the width-8 white strokes in the content stream
are erasers marking the undercrossing gaps, and the long-dashed black curves
are the "n strands" ellipsis.

At `n = 1` each n-stranded spiral degenerates to a single loop, so Figure 1
becomes an honest finite diagram with no schematic content at all. That is what
was transcribed here.

## The link

20 crossings as transcribed (6 green self-crossings, 2 black, 12 between),
simplifying to 10.

| check | required | got |
|---|---|---|
| components | 2 | **2** |
| linking number | 0 (GST Prop. 2.2, algebraically unlinked) | **0** |
| component 1 | square knot `Q` | **Jones polynomial identical to `3_1 # -3_1`** |
| component 2 | `V_1 = T_{1,2} # mirror = unknot` | **simplifies to 0 crossings** |
| 0-surgery on both | `#_2(S^1 x S^2)` | **`pi_1` free of rank 2, `H_1 = Z + Z`** |
| split? | no | **hyperbolic, volume 7.3277** |

The 0-surgery result is GST's *defining* property of `L_{n,k}`, and it is the
check that the transcription is the right link rather than merely a link with
the right components.

## The test

```
null V         = 1          (Theorem 1 needs n-1 = 1; automatic here, research/22 3.1)
det V          = -23
det V mod 32   = 9
component dets = [9, 1] -> product 9 -> 9 mod 32
predicted      = 9
```

**MATCH.**

## Why this is not vacuous

A split `Q u O` also gives residue 9 — but it gives `det V = 9` *exactly*,
where `L_{1,1}` gives `-23`. Same residue, different link, and the exterior is
hyperbolic with volume 7.3277, so nothing here is the trivial answer. The rung
tests the normalisation of `V` at `q = i`, the component-determinant path, and
the transcription simultaneously.

## What rung 2 needs

`L_{2,1}` requires `n = 2`, where the spirals stop being degenerate: two turns,
the `+-1` twist boxes become `Delta^{+-2} = sigma_1^{+-2}`, and
`V_2 = T_{2,3} # mirror(T_{2,3})` is the square knot. The structure that is
**not** yet pinned down from Figure 1 is where the spiral step (the shift from
turn `i` to turn `i+1`) sits relative to the two arc attachments — at `n = 1`
that question is invisible, and the ellipsis dashes hide it. Resolving it wants
Figure `Lnk`, Figure `Gompffig3b` (where `L_{n,k}` appears before blow-down with
all `n`,`k` dependence in labelled twist boxes), or Diao-Pan-Yan's algorithm.

**Do not trust an `L_{3,1}` residue until `L_{2,1}` returns 17.** That is the
pre-registered rule and it is the only thing standing between this lane and a
false counterexample.

## Reproduce

```
python pdbuild.py     # prints the 20-crossing PD code
```
`l11.py` holds the transcribed polylines with the figure's own coordinates.
Needs snappy + spherogram; no Sage.
