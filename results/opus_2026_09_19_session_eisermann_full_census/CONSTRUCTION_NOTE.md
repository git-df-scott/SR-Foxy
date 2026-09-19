# The `L_{n,k}` blocker is weaker than the campaign recorded

`research/22` §3.3 and `research/53` §2 both gate the whole GST link lane on
"`L_{3,1}` is a picture, not a combinatorial description", with tracing from a
**raster** figure judged too risky. That premise is wrong in two ways, both
checked here against the primary source.

## 1. The figures are vector, and the source is public

`arXiv:1103.1601` ships its full LaTeX source, including **`Ln1.eps` /
`Ln1.pdf`** (Figure 1, `L_{n,1}`) and `Lnk.eps` (Figure `L_{n,k}`) as vector
EPS/PDF, not raster. Path geometry is exact and machine-readable.

Caveat that survives: Figure 1 is **schematic in `n`** — the bundles are drawn
with ellipsis dashes meaning "`n` strands", so the vector data cannot simply be
crossing-detected. It still has to be understood and regenerated per `n`.

## 2. There is a much smaller parameterized diagram

`Text.tex` line 948 points at **Figure `example`** as "a somewhat simpler
picture of `L_{n,k}`". It is a 4-component framed diagram with every `n`- and
`k`-dependence confined to four twist boxes. From the figure's own pinlabels:

| curve | framing | role |
|---|---|---|
| outer red | `[1]` | blow down |
| middle red circle | `[-1]` | blow down |
| small black circle (top) | `0` | becomes a component of `L_{n,k}` |
| large black curve | `0` | becomes the other component |

twist boxes: `k` (left), `-k` (right), `n` (middle), `-n` (bottom).

Blowing down a `±1`-framed unknot is a purely combinatorial operation on a
diagram. So `L_{n,k}` is reachable as: *write down this small diagram with twist
regions, then blow down two unknots* — no spiral bundle tracing.

## 3. Primary-source confirmation of the calibration rungs

`Text.tex` line 776, verbatim:

> "The authors do not know whether `L_{n,k}` is ribbon except in the special
> cases `n=0,1` or `k=0` or `(n,k)=(2,1)`."

So `L_{1,1}` and `L_{2,1}` are known ribbon, exactly as `research/53` §3 claims.
The ladder is sound at its source.

## Status

**Not built.** This note records that the gate is combinatorial work on a small
labelled diagram rather than an unreadable bitmap. Nothing here is a link, a
residue, or a counterexample.
