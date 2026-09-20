# Where `L_{2,1}` stops, stated precisely

`L_{1,1}` is built and verified (`README.md`). This records exactly what
defeats `n >= 2`, so the next attempt does not re-derive it.

## What IS settled

**The bundle's knot type is forced and checked.** A planar `n`-turn spiral is
the `(n,1)` curve on a torus, so its closure is the unknot; a full twist sends
`(n,1)` to `(n,n+1)`. So the `+-1` twist box carries `Delta^{+-2}` and the
bundle is the closure of

    delta^(n+1),   delta = s_1 s_2 ... s_{n-1}   on n strands.

Verified in spherogram: `n=1` empty braid -> unknot; `n=2` -> `s_1^3`, one
component, det 3 = `T_{2,3}`; `n=3` -> `(s_1 s_2)^4`, one component, det 3 =
`T_{3,4} = 8_19`. So `det(V_n) = 3 * 3 = 9` for `n = 2, 3`, which is exactly
`research/53`'s table. `full_twist_word(n)` in `gen.py` emits these.

**Q is `n`-independent.** With radial step 5pt its inner chains stay inside the
innermost turn on both sides and its gaps span every turn's edge, for `n <= 3`.
Its 6 self-crossings and its over/under pattern against a bundle (left: over at
`y = 52, 75, 105`, under at the top and `y = 132, 152`; right: mirrored) do not
change with `n`.

## What is NOT settled

**Where the spiral is cut for the connected sum.** `V_n = T_{n,n+1} #
mirror(T_{n,n+1})` needs one cut per summand. Figure 1 attaches the two
connecting arcs at *different radial positions*: arc A leaves the left bundle at
`(152.6, 154.0)`, the INNERMOST lane, and arc B at `(174.1, 179.7)`, the
OUTERMOST. At `n = 1` those lanes coincide, which is why `n = 1` is clean and
says nothing about this.

For `n >= 2` three readings are all consistent with the drawing and give
*different links*:

1. the bundle is a closed braid, cut at one point, with a connector running
   between lanes — the connector's over/under against the intermediate lanes is
   undetermined, and it first bites at `n = 3`;
2. the bundle is an open spiral arc whose two ends are the arc attachments — then
   whichever lane is traversed first loses its green crossings, and green no
   longer meets all `n` strands, contradicting the drawn erasers;
3. the sub-arc between the two cut points is removed — at `n = 1` this is the
   short right-edge piece `y in (154, 180)` and reproduces the verified link,
   but for `n >= 2` the two cut points are on different lanes and the arc
   between them is most of the curve.

Reading 2 is contradicted by the figure. Readings 1 and 3 are not
distinguishable by staring at Figure 1, because the ellipsis dashes are drawn
exactly over the region that would settle it.

## What would settle it

Not more of Figure 1. Either

* **Figure `Gompffig3b`** (`Text.tex` line 651), where `L_{n,k}` appears BEFORE
  blow-down as black curves against a red `[+-1]`-framed unlink, with every
  `n`- and `k`-dependence confined to labelled twist boxes — then blow down the
  two red unknots; or
* **Figure `example`** (line 948), the same thing simplified: four twist boxes
  `k, -k, n, -n`, red `[1]` and `[-1]` to blow down, black `0`-framed pair; or
* **Diao-Pan-Yan** (arXiv:2604.17737), who implement an explicit algorithm but
  publish no PD codes, braid words or data, deferring details to a later paper.

The blow-down route needs a spanning disk for each red unknot, which is the
work: blowing down is combinatorial only once the `+-1`-framed component is
isotoped to a round circle.

## The rule that still stands

**Do not trust an `L_{3,1}` residue until `L_{2,1}` returns 17.** Every reading
above can be built and tested; the one that returns 17 on `L_{2,1}` -- with
components `3_1 # -3_1` and `Q`, linking number 0, and 0-surgery giving `pi_1`
free of rank 2 -- is the one to trust. Fitting a reading until it clears the
rung and then believing `L_{3,1}` is exactly the false-counterexample mode this
campaign exists to avoid.
