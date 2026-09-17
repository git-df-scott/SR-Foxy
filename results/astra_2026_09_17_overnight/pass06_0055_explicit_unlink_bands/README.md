# Explicit crossed-axis unlink gate

**Status: NO COUNTEREXAMPLE.**

Input repository state: `70c6e7edfae59ecd042ae2d72dea851a0142f23d`.
Source scaffold: `data/knots/AbeTagami_marked_product_scaffold.json`.

This pass turns the changed-axis proposal into one replayable diagram-level object.

## Explicit bands

Starting from the stored 54-crossing marked product scaffold, use these two
zero-twist Spherogram band specifications, in this order:

```
a40a423e_0_0
d0826c36_0_0
```

Decoded paths are

```
B1: [(15,2),(16,2),(2,2),(41,0)], under-bits [0,0], twist 0
    c1_upper -> c2_lower

B2: [(13,2),(27,0),(32,2),(52,0)], under-bits [0,0], twist 0
    c2_upper -> c1_lower
```

The second specification is interpreted on the once-banded 58-crossing
diagram. Its listed crossings happen all to be inherited source crossings.

The resulting full marked diagram has 62 crossings and three components:
the original boundary knot `R` and the two new axes `eta1,eta2`.

## New verified gate: the two new axes are exactly the unlink in S3

Delete `R` and smooth every mixed `R`--`eta` crossing. The resulting
two-component sublink has the six-crossing PD code

```
[[0, 1, 2, 3], [4, 0, 3, 5], [2, 6, 7, 8], [9, 7, 6, 10], [1, 11, 9, 10], [4, 5, 8, 11]]
```

A deterministic Reidemeister-II simplifier, implementing the same local
criterion as Spherogram's `reidemeister_I_and_II`, removes all six crossings:

```
R2 (1,5), ports (3,1)
R2 (0,2), ports (2,0)
R2 (3,4), ports (0,2)
```

No Reidemeister I, III, randomization, knot table, floating point, or topology
database is used. Since the starting sublink has two components and RII moves
preserve component number, the final zero-crossing diagram is the
two-component unlink `L_0`.

This is stronger than the previous linking-number-zero scaffold gate: one
explicit crossed pair now passes Park's **boundary-link-type** requirement for
the `l=0` setup. Park's Definition 2.1 requires the boundary pair to be
isotopic to `L_l`; his Remark 2.2 says the extra fundamental-group condition is
automatic for `L_0`. This still does **not** make the pair `0`-nice or
`0`-standard, because the required annulus must be embedded in the slice-disk
exterior, and standardness is an additional proper-isotopy condition.

Primary source: JungHwan Park, *A Construction of Slice Knots via Annulus
Modifications*, arXiv:1512.00401, Definition 2.1, Remark 2.2, Definition 3.1,
Theorem 3.3.

## Why the unlink certificate is not yet the missing annulus

The simplest unlinking isotopy is already blocked *relative to R*. The first
RII move above is between full crossings 26 and 56. After deleting `R`, its two
bigon sides are

```
26 --(through mixed crossing 17)-- 56
26 --(through mixed crossing 18)-- 56.
```

In the full marked diagram the `R` strand connects `(17,0)` directly to
`(18,2)`, so that R strand pierces the would-be RII bigon. Therefore this
specific RII cancellation is not an isotopy in `S^3 \ R`, and the unlink
certificate must not be promoted to a modifying annulus in the product-disk
exterior.

This localizes the next geometric question much more sharply: compute the two
new axes in the product-disk group (cheap necessary conjugacy gate), and if
they pass, search for a nonseparating compression disk for the canonical
genus-one twice-banded surface or a separately embedded annulus. The pass05
Euler-characteristic argument remains in force: the two product annuli plus
these two bands alone form a genus-one surface, not an annulus.

## Reproduction

Standard Python only:

```
python3 check_explicit_unlink_bands.py
```

The checker reconstructs both bands from the stored scaffold PD, extracts the
new-axis sublink, verifies the exact three RII moves, and verifies the explicit
R-strand piercing of the first RII bigon.

## Scope / unresolved obligations

This pass does **not** prove sliceness of D01 and does not identify a new
counterexample. It has not yet verified:

1. the based words of `eta1,eta2` in the product-disk group or their conjugacy;
2. an embedded annulus disjoint from the product disk;
3. `0`-standardness in Park's sense;
4. the surgery coefficients and exact resulting boundary knot;
5. that the resulting boundary is the certified Abe--Tagami nonribbon target.

The single next action is the group-word/conjugacy calculation for these exact
two band specs. A failure kills this candidate cheaply; a pass justifies
spending effort on the compression/annulus geometry.
