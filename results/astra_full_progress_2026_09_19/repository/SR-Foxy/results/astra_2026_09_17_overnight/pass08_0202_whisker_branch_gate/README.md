# SL(2,F5) whisker-branch gate for the explicit crossed axes

17 September 2026 UTC. **NO COUNTEREXAMPLE.**

Input main commit: `0439e8fa002f2c107fa699df6e57e5a313ffd23a`.
Explicit bands from pass06/pass07:

```
a40a423e_0_0
d0826c36_0_0
```

This pass addresses the exact next gate left by pass07: do the two new axes
`eta1,eta2` pass the known finite-quotient conjugacy test in the product-disk
exterior? The answer is **not yet uniquely determined by the stored scaffold**, but the ambiguity is now finite and sharply classified.

## Result

Using the 54-crossing marked product scaffold directly, kill the four auxiliary
meridians and build the Wirtinger presentation of the boundary knot `R`. Fix the
known meridian image

```
[[4,1],[2,2]] in SL(2,F5).
```

There are exactly **49** `SL(2,F5)` colourings of the doubled boundary knot with
that fixed meridian. This is the expected `7 x 7` end-factor count from the
source quotient. Their original marked-circle trace data split as

```
(tr c1_upper, tr c2_upper, tr c1_lower, tr c2_lower)
(1,4,1,4): 36
(1,4,2,2):  6
(2,2,1,4):  6
(2,2,2,2):  1
```

The 36 `(1,4,1,4)` colourings are exactly the branches on which both ends carry
the previously certified nonabelian witness-type free-homotopy data. For every
one of these 36 branches, each corresponding original upper/lower axis pair is
conjugate up to inversion in `SL(2,F5)`, a positive control required by the
product construction at the free-homotopy level.

Evaluate the **actual two band-summed curves** on those same 36 colourings. The
outcomes form six equally sized branch types:

| tr eta1 | tr eta2 | ord eta1 | ord eta2 | conjugate up to inversion? | count |
|---:|---:|---:|---:|:---:|---:|
| 0 | 2 | 4 | 5 | no | 6 |
| 0 | 3 | 4 | 2 | no | 6 |
| 2 | 0 | 5 | 4 | no | 6 |
| 4 | 0 | 3 | 4 | no | 6 |
| 2 | 2 | 5 | 5 | yes | 6 |
| 4 | 4 | 3 | 3 | yes | 6 |

Therefore **24 of the 36 witness/witness branches are killed immediately by
this finite quotient, while 12 survive it**. Equivalently, after fixing one
upper witness realization there are six possible relative lower witness
placements visible to this quotient: four separate the new axes, two do not.

## What this proves — and what it does not

This is a useful negative/positive split, not a choice of the physical branch.
The stored scaffold records the doubled diagram and the band paths, but it does
not record a **based lower-to-upper whisker map in the product-disk group**.
Free-homotopy data for the four original circles are insufficient to recover
that based relative placement: all 36 branches pass the corresponding-circle
positive controls, yet they disagree on the new band-summed axes.

Consequently it would be invalid to pick one of the 24 separating colourings
and declare the explicit candidate dead. It would be equally invalid to pick
one of the 12 surviving colourings and declare the group gate passed. The
actual product construction selects one based branch; that branch must be
computed geometrically/algebraically from the cut-and-glue whisker data.

This sharpens the missing step:

> **Whisker-selection lemma / missing certificate.** Lift the corresponding-
> endpoint gluing used by `build_marked_product_scaffold.py` to a based
> fundamental-group identification between the lower and upper end copies.
> Once this single based map is known, the existing `SL(2,F5)` quotient decides
> this explicit band pair immediately: four of the six quotient-level relative
> branch types fail conjugacy, while two survive.

No annulus, compression disk, Park 0-standardness certificate, surgery framing,
or resulting boundary-knot identification is produced here. The pass07 relative
RIII+RII move and the pass05 genus-one calculation remain unchanged.

## Reproduction

Standard Python only; no SnapPy, Spherogram, floating point, network, or random
search is used:

```
python3 check_whisker_branch_gate.py
```

On the run saved with this checkpoint it completed in about 0.7 seconds and
used under 100 MB. The checker reconstructs both explicit bands, constructs the
boundary-knot Wirtinger quotient, enumerates `SL(2,F5)` exactly, evaluates the
four original marked loops and the two new axes, directly enumerates finite-
group conjugacy up to inversion, and runs the corresponding-axis positive
controls.

## Single next action

**Compute the based lower-to-upper whisker identification induced by the exact
corresponding-endpoint gluing in `build_marked_product_scaffold.py`.** Do not
search for another band pair yet. Selecting the actual one of the six relative
quotient branches either kills this explicit candidate cheaply or clears its
last known group-theoretic gate and justifies returning to the compression /
embedded-annulus geometry.
