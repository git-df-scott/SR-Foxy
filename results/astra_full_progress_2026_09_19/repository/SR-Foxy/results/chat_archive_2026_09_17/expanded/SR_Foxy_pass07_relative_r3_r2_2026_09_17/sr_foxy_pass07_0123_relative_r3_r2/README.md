# Relative Reidemeister correction for the explicit crossed axes

17 September 2026 UTC. **NO COUNTEREXAMPLE.**

Input main commit: `9d4634224db3c32dce419e67510c994111bd7502`.
Input construction: `results/astra_2026_09_17_overnight/pass06_0055_explicit_unlink_bands/`.

This pass audits the first alleged relative obstruction in pass06. The conclusion changes in the constructive direction: the first Reidemeister-II cancellation of the new axes is **not blocked by the boundary knot R**. There is an explicit Reidemeister-III move in the full marked diagram, followed by the desired Reidemeister-II move. The first eta cancellation can therefore be carried out by an isotopy in `S^3 \ R`.

This is one certified local step, not an annulus, concordance or slice disk.

## Input bands

The explicit zero-twist crossed bands remain

```
a40a423e_0_0
d0826c36_0_0
```

from pass06. They turn the 54-crossing marked product scaffold into a 62-crossing three-component diagram `R union eta1 union eta2`. Deleting R gives a six-crossing eta sublink which is the two-component unlink.

## Correction to pass06

Pass06 observed that the first eta-only RII bigon has sides passing through mixed crossings 17 and 18 and that the R strand directly joins those crossings. It concluded that this specific cancellation was unavailable relative to R. That conclusion omitted the crossing-height data.

In the full 62-crossing diagram, crossings 17, 18 and 26 form an exact Reidemeister-III triangle under Spherogram's published face criterion:

```
[(17,3),(18,2),(26,3)]
```

At both mixed crossings 17 and 18, R occupies ports 0 and 2, which are the under-strand in the PD convention; eta occupies ports 1 and 3. Thus R is the common bottom strand. The standard RIII can be supported in a local ball by moving the two eta strands in the upper half-ball while keeping R fixed pointwise.

After that RIII, crossings 26 and 56 satisfy the exact RII criterion:

```
(26,56,3,1)
```

Both are eta-eta crossings, so this RII is also supported away from R. This supplies an explicit relative-to-R realization of the first cancellation.

The checker ports the exact RIII face criterion/rewiring and RII criterion from Spherogram rather than inferring a move from a picture.

## What remains after the certified move

After RIII then RII, the full marked diagram has 60 crossings. Deleting R leaves the four-crossing eta diagram

```
[[0,1,2,3],
 [2,4,5,3],
 [6,5,4,7],
 [1,0,6,7]]
```

If R is deleted, those four crossings disappear by two RII moves and the eta pair is again the two-component unlink. In the full diagram, however, no RII is immediately available.

As a bounded control, `check_relative_r3_r2.py` exhausts every diagram reachable from this 60-crossing state by at most four RIII moves, with crossing labels retained. It visits 6,478 distinct states (6,477 noninitial expansions). **No eta-eta RII move appears anywhere in that radius.** In particular the next eta-only pair does not become cancellable in that search.

That is only a finite diagram search. It is not a proof that the remaining four crossings cannot be removed relative to R: longer RIII sequences, pickup/isotopy moves, or a different annulus/compression can still work.

## Relation to the genus-one gate

Pass05's Euler-characteristic calculation is unchanged. The two original product annuli plus the two crossed bands form a connected genus-one surface with two boundary components, not an annulus. The relative RIII+RII above is an ambient isotopy of its boundary data; it does not compress that genus.

Thus the candidate is now in a stronger state than pass06 recorded:

- the two new boundary curves are exactly `L_0` in S3;
- the first apparent obstruction to simplifying them relative to R was spurious and is explicitly removed;
- the remaining four-crossing relative configuration is unresolved;
- no nonseparating compression disk, separately embedded annulus, Park 0-standardness certificate, surgery framing, or target-boundary identification has been produced.

## Reproduction

Standard Python only; no SnapPy/Spherogram import, floating point, knot table, network, or randomization:

```
python3 check_relative_r3_r2.py
```

The run reconstructs both pass06 bands from the stored scaffold PD, verifies the full RIII and RII combinatorially, checks which components occupy each port, extracts the residual eta sublink, and performs the exhaustive depth-four RIII search.

## Single next action

Compute the based classes of these **exact** `eta1,eta2` in the product-disk group, with the band whiskers included, and test conjugacy up to inversion. A nonconjugacy witness kills this explicit candidate cheaply. A conjugacy pass would justify spending the next construction effort on a nonseparating compression disk for the genus-one surface or a separately embedded annulus.
