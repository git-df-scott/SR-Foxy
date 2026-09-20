# RETRACTION: the link built here is `L_{0,1}`, not `L_{1,1}`

19 September 2026, Opus. **CE: NO.** `README.md` in this directory claims
`L_{1,1}` was built and that rung 1 of `research/53`'s ladder returned 9.
**The link is `L_{0,1}`.** The residue 9 is real but it is the wrong rung: it
tests a member GST list as ribbon for a different reason, and it is not the
calibration `research/53` asks for.

Found by the five-hour GST campaign's independent transcription of Figure
`example`, whose `n = 0` row matched this link. Confirmed here from my own side.

## The identification

The link built in `l11.py` / `pdbuild.py`, simplified:

| | |
|---|---|
| crossings | **10 = 6 self + 4 inter-component** |
| isometric to | **`L10n36`** (SnapPy `is_isometric_to`, True) |
| in certified `RibbonLinks` census | **yes**, `ribbon_2_10_7ecd0dc0` (index 4) |
| volume | 7.3277247534 |
| `det V` | `-23 = 9 (mod 32)` |

`6 self + 4 inter` is exactly the shape of GST Figure `squareknot`: the square
knot `Q` together with an unknotted component meeting it in four crossings, the
link on which a single handle slide gives the unlink. That is `L_{0,1}`.

Note `L10n32` and `L10n59` share the volume 7.3277247534 and are **not**
isometric to it, so the identification rests on the isometry test, not volume.

## Why the original verification could not catch it

Every check in `README.md` is satisfied by `L_{0,1}` just as well as by
`L_{1,1}`, because **`V_0` and `V_1` are both unknots**: `T_{0,1}` and `T_{1,2}`
are both trivial. So "one component is the square knot, the other is the
unknot, linking number 0, 0-surgery gives `#_2(S^1 x S^2)`" cannot distinguish
`n = 0` from `n = 1`. The 0-surgery check I leaned on hardest is exactly the
property GST impose on **every** `L_{n,k}`, so it tests membership in the
family, never the index within it.

**The lesson is not "verify more invariants". It is that a check shared by two
members of a family cannot select between them, and every check in that README
was of that kind.**

## The actual transcription error

Figure 1's bundle is an `n`-turn spiral. I collapsed it at `n = 1` to a single
rounded loop with the two arcs attached at its ends. That collapse loses one
turn of threading: the resulting component passes through `Q` as `V_0` does,
not as `V_1` does. The drawn end positions (arc A on the outermost strand, arc
B on the innermost) are artifacts of the multi-strand layout and must not be
read literally when the layout degenerates.

I also tested a symmetry-motivated repair — Figure 1 is invariant under
pi-rotation about a vertical axis in the plane of the paper, which swaps the
bundles, reverses over/under and exchanges the `-1` and `+1` twist boxes, and my
transcription broke it by giving `Q` six crossings with the left bundle and only
four with the right. Restoring the symmetry raises the raw count 20 -> 24 but
**the link is unchanged**: still 10 crossings, `det V = -23`, volume
7.3277247534. So the asymmetry was not the error; the lost spiral turn is.

## Independent support for the campaign's indexing

* **GHMR, arXiv:2304.09304**, full text verified in `research/03` line 48:
  "The first two links in the GST family (`L_{1,1}` with 18 crossings and
  `L_{2,1}` with 40 crossings)". The campaign's `n = 1` reconstruction has
  **18** crossings; this one has 10.
* The campaign's `n = -1` and `n = 0` rows agree with each other, which is
  what GST's symmetry `n <-> -n-1` requires (`0 <-> -1`). That is an internal
  consistency check the campaign's construction passes and mine never tested.
* Crossing arithmetic: `Q` contributes 6 self-crossings and the interleaving
  6 per bundle per turn, giving `6 + 12 = 18` at `n = 1` — the campaign's row.

**Residual discrepancy worth keeping open:** GHMR say `L_{2,1}` has 40
crossings; the campaign's `n = 2` reconstructs to 38. Probably diagram versus
simplified count, but it is unexplained and should not be waved through.

## What this does NOT establish

That `L10n36` **is** GST's `L_{0,1}`. What is established is that my Figure 1
transcription yields `L10n36`. The identification with `L_{0,1}` rests on the
campaign's independent Figure `example` construction matching it under a
meridian-preserving isometry, on the `6 + 4` structure matching Figure
`squareknot`, and on certified ribbon membership. That is convergent
invariant-and-structure evidence from two different source figures, **not** a
Kirby-move or isotopy certificate. Per the campaign's own rule, source identity
is not to be upgraded from matching invariants.

## Status of the ladder

Rung 1 (`L_{1,1}`, must give 9) is **not** done. Rung 2 (`L_{2,1}`, must give
17) is not done. What is done is `L_{0,1}`, returning 9, which is consistent
with its being ribbon and carries no calibration weight for `L_{3,1}`.
