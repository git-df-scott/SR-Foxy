# Direct diagram verification of the fixed-axis annulus obstruction

**No counterexample. The obstruction is old; its direct PD-level certificate
and replay below are new computations in this pass.**

The earlier product-disk obstruction depended on a saved SnapPy presentation
and peripheral-word extraction. Here those intermediate group words are not
inputs to the check. Starting with the marked 27-crossing diagram itself, we
construct a finite Wirtinger representation, kill the auxiliary meridians, and
read the two axis images by following their diagram paths.

## What was actually supplied and verified

The input is the PD field of `data/knots/AbeTagami_L_63_c1_c2.json` at
`7a74678daccd9f3148b25a22a3f84a82eb1d374b`, source blob
`6791fef9dc837ab0bb697ff27f1fd1925fdbb03e`. The stored markings are recovered as
three directed edge cycles: K uses labels 0..33, c1 uses 34..41, c2 uses 42..53.
All traversals and consecutive-label orientations are checked, not assumed
from an unexplained component index. The linking matrix is exactly

```
[[0,0,0],[0,0,1],[0,1,0]].
```

We assign SL(2,F5) matrices to Wirtinger arcs, joining the two segments of each
overpass. At a crossing let i and o be incoming and outgoing under-meridians,
b the over-meridian, and epsilon the sign. Our relation is

```
o = b^(-epsilon) i b^(epsilon).
```

This agrees with Spherogram's published `knot_group` relation convention,
checked at the source level; we did not execute or import that method.
Underpass transport accumulates b^epsilon in traversal order. Its product
is the blackboard longitude. The preferred-longitude correction is a power
of that component's meridian; for the two auxiliary components it evaluates
to the identity after the specified meridian filling.

All auxiliary meridians are assigned the identity. Therefore the resulting
representation factors through meridional filling of the auxiliary circles,
which is the exterior of the remaining knot component. The auxiliary
longitudes then represent the two marked circle cores in that exterior.

## Explicit output

The two filled-axis images are

```
c1 -> [[3,4],[2,3]],     trace 1 mod 5, order 6,
c2 -> [[2,3],[1,2]],     trace 4 mod 5, order 3.
```

Every matrix has determinant one, and all 27 original crossing relations are
satisfied. Trace is invariant under conjugacy and under inversion in SL(2).
Thus these marked axes are not conjugate in either orientation in the group
of the knot exterior. A continuous annulus between them would give just such
a conjugacy. None exists in this specified exterior.

The finder used the old witness's meridian conjugacy class as a SEARCH HINT.
It did not import the old group presentation or axis words, or prescribe the
answer for the two longitudes. The certificate is self-contained: a verifier
needs only the marked PD and the matrix assignment, not the search hint or
any previous SnapPy result.

## Independent replay within this package

`marked_pd_certificate.py` finds the coloring by exact constraint propagation.
`check_marked_pd_certificate.py` does NOT import the finder. It expands the
arc assignment to per-edge matrices and independently checks original
crossings, filled meridians, component traversals, longitude products and
peripheral commutation. It also enumerates all 120 group elements to check
conjugacy to c2 and its inverse directly, rather than relying only on traces.

Controls include a conjugated-same-axis positive test, the abelian coloring
where both axes are trivial (which must NOT give an obstruction), all cyclic
longitude-basepoint shifts, and rejected mutations of a matrix, the PD and
a reported longitude. The replay records 322 elementary checks, including
27 original crossing relations and 240 finite conjugacy comparisons. These
are validation counts, not distinct knot searches or independent proofs.

The finder completed in about 0.025 seconds after three search nodes and one
full coloring. No large enumeration, topology library, numerical recognition,
or floating-point holonomy was used. The numerical speed is not a theorem.

## Exact scope and remaining dependencies

This removes the reliance on SnapPy's GROUP AND PERIPHERAL EXTRACTION for
this particular diagram-level nonconjugacy certificate. It does not by itself
verify that the stored marked diagram is the one drawn in the source paper.
That diagram-to-paper correspondence remains a separate dependency.

For application in four dimensions, the standard product-disk construction
identifies its exterior group with the knot exterior group, with the axes in
the specified end. That geometric interpretation is still to be matched to
any proposed modification. Arbitrary new axes or genuinely nonlocal disk
changes are not excluded. The existing local-knotting retraction lemma applies
only when its marked-image hypotheses hold.

No smooth disk for D01, no global nonribbon proof for KDG, and no obstruction
to concordance of K0 and K1 follows from this fixed-axis result.

## Reproduce

```
python3 marked_pd_certificate.py --output NEW_CERTIFICATE.json
python3 check_marked_pd_certificate.py --certificate NEW_CERTIFICATE.json --output NEW_REPLAY.json
```

Both scripts use only Python's standard library and refuse overwrites. The
finder has a time/solution cap and reports a cap as UNKNOWN rather than
nonexistence. The checker is a positive-certificate verifier, not an exhaustive
search or proof assistant.
