# Crossed-band genus gate for the changed-axis proposal

17 September 2026 UTC. Input repository commit:
`2a03c21bdfe8c024f0eddb9b19b4e23b20414b6b`.

**Status: NO COUNTEREXAMPLE.** This pass does not construct a new annulus, disk,
or concordance. It falsifies the most literal geometric realization of the
`uv`/`vu` changed-axis suggestion and replaces a vague missing-embedding gate by
a precise compression problem.

## New geometric lemma

Let `A1` and `A2` be the two disjoint product annuli joining the upper and lower
copies of the original marked circles. Their four boundary components are

`c1_upper, c1_lower, c2_upper, c2_lower`.

Suppose we realize the repository's crossed pairing by two disjoint,
orientation-compatible boundary bands:

1. band-sum `c1_upper` to `c2_lower`, producing `eta1`;
2. band-sum `c2_upper` to `c1_lower`, producing `eta2`.

If we build the spanning surface only from `A1 union A2` and these two bands,
the resulting surface is **not an annulus**.

Proof: initially `chi=0`, there are two connected components and four boundary
components. The first boundary 1-handle joins the two annuli, so the surface is
connected with `chi=-1` and three boundary components: a pair of pants. The
second boundary 1-handle joins the two remaining distinct boundary components
of this connected orientable surface. Thus `chi=-2` and the boundary has two
components. For a connected orientable surface,

`chi = 2 - 2g - b`,

so `g=1`. Therefore the canonical twice-banded surface is a genus-one
cobordism from `eta1` to `eta2`, not an annulus.

If either band is orientation-incompatible, the resulting surface is
nonorientable and therefore is also not the required oriented annulus.

This is pure surface topology and does not depend on the group calculation,
Jones data, framings, or a bounded search.

### What this does and does not rule out

This **does rule out** the shortcut "choose crossed bands whose boundary words
are `uv` and `vu`; the two old product annuli plus those same two bands are the
desired annulus." Even perfect algebraic conjugacy of the new boundary words
does not change the Euler characteristic.

It **does not rule out** the changed-axis program. The two new boundary curves
may still cobound some other embedded annulus. In particular, the canonical
genus-one surface can be converted to an annulus if one finds a
**nonseparating compressing disk** in the disk exterior, disjoint from the
surface away from its boundary. Compression raises `chi` by two and turns
`(g,b)=(1,2)` into `(0,2)`. A different annulus not obtained by compressing
this particular surface is also possible.

Thus the constructive target is now sharper:

> A proposed crossed-band construction must provide either (a) an explicit
> nonseparating compression disk for the canonical genus-one surface, with its
> interior disjoint from the product disk and the surface, or (b) a separately
> specified embedded annulus with the same two new boundary curves.

A word identity alone is not a substitute for either object.

## Conditional framing calculation: what is and is not blocked

For comparison with the prior framing addendum only, assume the mirrored
`n=1` four-handle trace has auxiliary linking/intersection matrix

```
Q = [[ 2, 1, 0, 0],
     [ 1, 0, 0, 0],
     [ 0, 0,-2,-1],
     [ 0, 0,-1, 0]]
```

in the order `(c1_upper,c2_upper,c1_lower,c2_lower)`. This diagonal/framing
data are **not** part of the unframed scaffold; this section is conditional on
that previously stated hypothesis.

The naive two retained cross classes

`e1+e4, e2+e3`

have Gram matrix `diag(2,-2)`, determinant `-4`; this reproduces the earlier
homology failure.

A useful counterpoint is that the **full** lattice has no integral
"mixedness" obstruction. The four columns of

```
M = [[ 0, 2, 0,-1],
     [ 1,-2, 1, 1],
     [ 0, 1, 0,-1],
     [ 1,-1, 2, 1]]
```

all have support in both the upper and lower halves, `det(M)=-1`, and exact
integer multiplication gives

`M^T Q M = H + H`

with

```
H + H = [[0,1,0,0],
         [1,0,0,0],
         [0,0,0,1],
         [0,0,1,0]].
```

So the previous two-handle failure must not be promoted to "all mixed handle
slides fail." They do not fail at the ordinary integral-form level. This is
consistent with `research/14_marked_annulus_audit.md`, which already warns that
the ordinary intersection form is too coarse and records an equivariant
obstruction for the fixed trace.

Conversely, keeping all four 2-handles is not by itself a standard-ball
certificate. A pure `0+four 2-handle` handlebody with no 1- or 3-handles has
handle chain group `C2=Z^4`, `C1=0`, hence `H2=Z^4`. Even though `det(Q)=1`
makes its surgery boundary an integral homology sphere, the 4-manifold itself
cannot be `B4` or a product cobordism without additional handle
cancellations/attachments or a separate standardness theorem.

## Campaign consequence

The changed-axis proposal has two independent geometric obligations that
should not be conflated:

1. **surface obligation:** eliminate the genus-one handle (or construct a
   different annulus);
2. **ambient obligation:** certify that the corresponding surgery/annulus
   modification occurs in the standard ambient `B4`/`S3 x I` with the intended
   boundary knot.

The next useful object is therefore not another pair of conjugate words. It is
one explicit replayable crossed band pair **plus a candidate compression
disk**, with band whiskers/orientations and the compression boundary recorded.
That object can then be checked against the marked group and surgery framing
before any large search.

## Reproduction

`check_cross_band_gate.py` is standard-library-only and checks the
Euler-characteristic calculation and the exact conditional integer matrices.
Run it in a fresh directory if a saved JSON result is desired:

```
python3 check_cross_band_gate.py
```

The checker is arithmetic support for the written topology argument; it is not
a topology engine and does not certify an embedding.

## Reading scope

This pass read the current pass04 checkpoint and the construction notes
`research/12_coupled_movie_audit.md`,
`research/14_marked_annulus_audit.md`,
`research/15_infection_target_compatibility.md`,
`research/20_next_construction_plan.md`,
`research/opus_mixed_lift_review.md`,
`scripts/build_marked_product_scaffold.py`, and
`scripts/mixed_stabilization_bands.py`.

No new Opus annulus/disk/handle construction was present on `main` when this
checkpoint began. Existing long band searches and settled Jones/Floer/HKL/s
computations were not rerun.
