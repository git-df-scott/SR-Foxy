# One geometric winding recovers the second handle match

18 September 2026; start HEAD `3e4461e23fce6687293f6abef963011b37677c55`.
No counterexample, compression disk, or complete pair of transfer movies.

The new construction is on the **actual original product-band surface F**.
Its previously unspecified second handle z0 follows B1, a vertical across
the c1 product annulus, B2, then a vertical and the recorded native c2 arc.
The exact port routes determine its image in the actual product-disk exterior
W. It cannot be transferred to the correction handle B: an SL(2,F17)
representation distinguishes their traces, 1 versus 2. This also excludes an
unbased transfer and either orientation of B.

**One geometric modification works at this gate.** Wind the first annulus
spanning arc once in the positive native c1 direction, keeping its endpoints
fixed. The resulting embedded surface curve z1 equals B in pi1(W), proved
by six recorded relator applications. The first handle v is A^-1, proved by
one. This is not an arbitrary word change: the new annulus path, including
its specific traversed c1 cycle, is recorded. It changes the curve and its
punctured-torus neighborhood, not the underlying surface or its boundary.

The inverse correction has the required handle orientations (-A,B).
Four explicitly ordered parallel connector tracks through the b-root
corridor give a **relative geometric prescription** for a disjoint mixed
cut system. Its abstract compressions would produce an annulus. The
common connector has trivial image in W with the specified root corridor;
its class in the protected-sheet complement remains uncomputed. These
statements use Research42's existence realization of the correction with
that fixed root. They are not a new embedded diagram for its 14 disk pushes.

## Why the winding is genuinely geometric

Parameterize each native product annulus by (theta,s), where s=0 is the
upper end and s=1 the lower end. The annulus-1 attachment points project to
the SAME source edge, so normalize their theta coordinate to zero. Initially
rho1(t)=(0,1-t). Replace it by

    rho1_new(t)=(t mod 1,1-t),       0<=t<=1.

Smooth its endpoint tangent in fixed attaching collars. Distinct t values
have distinct s values, so the new arc is embedded. It has the same endpoints
and makes exactly one positive turn. In the universal covering strip it is
homotopic rel endpoints to a vertical followed by one positive upper c1
cycle. That is the inserted factor in GEOMETRY.json; this homotopy is only
used for computing the groupoid path. We do not replace the embedded helix
by a self-overlapping upper-boundary picture.

The surface curve framing is always the normal-to-curve direction within F,
transported along the actual helix. For annulus orientation e*dtheta ds and
curve tangent (theta',s'), take its transverse vector e*(-s',theta'); this
gives the positive tangent pair. No numerical framing of a nonexistent
compression disk is inferred. F, the correction surface, the original disk,
and the exterior boundary knot are not moved by this change of cut system.

This particular choice was motivated by the failed vertical representative
and the two-annulus geometry, not by a partner or knot census search.
An exploratory finite-matrix check of twists in v alone did not construct
any additional curve: its fixed punctured-torus boundary trace already
distinguishes that handle piece from the correction. The realized change
uses the OTHER annulus, hence changes the punctured-torus neighborhood.

## Files and replay

- `GEOMETRY.json`, `build_geometry.py`: endpoint matches, all new original
  surface paths, Dehn verticals, both words, six-step repair proof, hashes.
- `check_geometry.py`, `REPLAY.json`: independent finite replay, including
  wrong-winding, wrong-orientation, and wrong-vertical negative controls.
- `CONNECTOR_AUDIT.md`: all four tracks, root corridor, orientation and
  cut-system topology. This is a relative prescription on the existing
  correction realization, not its missing coordinate construction.
- `LOCAL_MOVIE.md`, `check_local_movie.py`, `LOCAL_REPLAY.json`: two explicit
  smooth crossing patches at the native c2/a underpass. Their signed points
  have equal local ambient labels but DIFFERENT transfer sheets. They cannot
  be called a Whitney pair. These local patches have not been attached to
  the actual correction endpoints or given the global whiskers.
- `LIMITATIONS.md`: exact remaining missing geometry and source dependence.

Run from the repository root:

    python3 results/astra_2026_09_18_mixed_transfer/check_geometry.py
    python3 results/astra_2026_09_18_mixed_transfer/check_local_movie.py

Both use the standard library. The builder refuses to overwrite its saved
output. Old source rewrite rules are previously proved input lemmas; the
new independent checker replays the new consequences and checks all original
source relations in the rejecting representation. It does not claim formal
verification of smooth embeddings.

## Next executable action

Realize the FOUR A-band disk pushes, with their entire ribbon widths, on the
fixed correction collar at b-root (7,1). Attach their endpoint to the saved
crossing-26 local model and replay the single crossing-11 relation geometrically,
retaining a. Record every resulting crossing and its global whisker before
attempting the B transfer. The corrected second handle z1 is now fixed and
ready; its six algebraic relator moves are not yet a geometric movie.
