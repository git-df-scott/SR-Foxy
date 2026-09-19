# A positive combinatorial identification of the stored K1 exterior

18 September 2026. Audit of Opus's `8574c44`, continued from research/38.

## Question and result

Does filling the stored three-component L at slopes (2,1), (0,1) give the
exterior of the stored K1? **Yes, as a positive combinatorial computation
trusting SnapPy's topological construction and retriangulation routines.**
An independent standard-library checker verifies the final oriented
tetrahedron-gluing isomorphism. Numerical hyperbolic canonicity is unnecessary
for this positive result.

This does not certify the preceding transcription of the paper's annulus
diagram into the stored L. It also does not supply a standalone Pachner-move
trace from each original PD to the final triangulation.

## Why this is stronger than a signature match

The computation constructs actual filled triangulations and applies `canonize`
to each side. Numerical choices guide that routine, but its operations preserve
the underlying manifold. Once the returned triangulations are explicitly
isomorphic, their homeomorphism does not depend on their being canonical.
We therefore use neither volume equality nor a numerical inequality to identify
the manifolds.

The software boundary was checked against SnapPy 3.3.2's release source, tag
`3.3.2_as_released`, commit `42217b3867ce3a00d1125a1b6860db335684c333`:

- [`canonize_part_1.c`, lines 53--60](https://github.com/3-manifolds/SnapPy/blob/3.3.2_as_released/kernel/kernel_code/canonize_part_1.c#L53-L60)
  explicitly distinguishes geometric accuracy from topology preservation.
- [`filling.c`, lines 98--146](https://github.com/3-manifolds/SnapPy/blob/3.3.2_as_released/kernel/kernel_code/filling.c#L98-L146)
  checks the filling specifications, subdivides, fills, and removes finite vertices.
- [`close_cusps.c`](https://github.com/3-manifolds/SnapPy/blob/3.3.2_as_released/kernel/kernel_code/close_cusps.c#L8-L36)
  describes the slope-specific combinatorial filling construction.
- [`triangulation.pyx`](https://github.com/3-manifolds/SnapPy/blob/3.3.2_as_released/cython/core/triangulation.pyx#L995-L1037)
  provides combinatorial isomorphisms and their peripheral matrices.

Source checked 18 September 2026, including an independent code/source audit.
This is a code-level trust argument, not a formal verification of the kernel.

## Saved certificates

| Case | Stored knot | L filling slopes | Final tetrahedra on each side | Directed face checks |
|---|---|---|---:|---:|
| n=0 control | K0 | (1,0), (-1,0) | 6 | 24 |
| n=1 target | K1 | (2,1), (0,1) | 12 | 48 |

For every source tetrahedron i the certificate specifies a target tetrahedron
j and an even permutation p_i of its four vertices. If its face f is glued
to tetrahedron i' by a permutation a, then the checker verifies

    target(i') = neighbor(target(i), p_i(f)),
    p_(i') a = b p_i,

where b is the corresponding target face permutation. It also checks bijectivity,
reciprocal face gluings, connectedness, orientation, and the single cusp.
The checker reads the saved SnapPea files directly and ignores all shape
coordinates. It checks the input/stage hashes and rejects both an incorrect
even permutation and an orientation reversal, in each case.

SnapPy additionally reports a peripheral map equal to I for each case. That
calculation and the earlier peripheral transport remain kernel-trusted; the
independent checker does not recompute homology on the cusp triangulation.
The positive complement identification can alternatively use knot-complement
uniqueness, with the assumption that both sides are the knot exteriors given
by the construction card.

Every stage is saved: the PD exterior, the link with filling instructions,
the filled exterior, and both final retriangulations. The bounded producer
has a 45-second CPU limit and completed in under one second. Its only finite
map search tests at most 24 times the tetrahedron count seed maps, then
propagates across faces. There was no manifold census search.

## Limits and an important correction to search interpretation

Equal explicitly checked triangulations give positive homeomorphism evidence.
**Unequal unverified canonical signatures do not give certified exclusions.**
The Opus shard language “decided NOT isometric” should therefore be read as
a numerical result unless the canonical computations were verified. This
does not stop the shards from serving as a useful filter; it changes the
strength of the conclusion one may draw from them.

The paper-to-L diagram correspondence still needs its own geometric audit.
The present result cannot establish that correspondence by matching several
invariants or by selecting the desired sign convention. No sliceness,
concordance, or Slice--Ribbon counterexample follows.

Artifacts: `results/night_2026_09_18_positive_identification/`.
