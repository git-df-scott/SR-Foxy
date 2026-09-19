# Fixed-stabilizer exclusion and a mixed-handle marking test

**CE status: not established.** This is a continuation of research/48, with
one targeted literature check and small exact diagram/group calculations.
No knot, band, or partner sweep ran.

The fixed stabilizer is now excluded as a way to obtain TWO ribbon
certificates: D01#C_(2,1)(R) is nonribbon by the argument in
`FIBERED_STABILIZER_OBSTRUCTION.md`, using Agol–Ren's March 2026 preprint.
That result is stronger than the old specified-prefix failure. All
C_(p,1)(R), p>=2, fail the same necessary condition. It says nothing new
about smooth sliceness.

The geometric continuation changes compression curves. The correction
handle A equals reversed native c2 in the actual boundary group; the new
identity reduces to one crossing-11 Wirtinger relation. Yet the prescribed
A-core and reversed c2 have different linking with protected axis a. The
exact missing meridian is the over-strand at crossing 26, passed underneath
by native c2 at port (26,2). A collar-only transfer cannot avoid that sheet.
See `MIXED_HANDLE.md`. An arbitrary four-dimensional transfer remains open.

## Reproduce

From repository root, with standard-library Python:

```
python3 results/astra_2026_09_18_mixed_handle_gate/check_saved.py
```

`build_checks.py` generates CHECKS.json in a fresh same-depth results directory
and refuses to overwrite it. It reuses the archived finite diagram routines
and a prior certified word-rewrite lemma. `check_saved.py` independently checks
the integer Bezout identity, mod-2 irreducibility, the actual signed linking
and protected underpass, the planar rotation system, and the simpler direct
Wirtinger proof. Two deliberately corrupted inputs are rejected. No SnapPy,
Sage, or new knot invariant is used by either main calculation.

CHECKS.json preserves the actual banded PD and every native traversal step.
REPLAY.json contains the independent results, including the full local
meridian sequence in the doubly marked exterior. MANIFEST.json pins files
and reused dependencies. Earlier results remain unchanged.

## An unfinished diagram probe, preserved separately

Before the stronger stabilizer obstruction was checked, a short source-diagram
probe removed the auxiliary components and simplified the upper nine-crossing
knot with six type-III moves and three type-I removals. Its six-crossing PD did
not directly match the stored K0 port graph under the tested even rotations.
That comparison was inconclusive about knot type. The probe did not transport
the A-whisker and is NOT an identification of marked cable diagrams. Its
reproducible local move record is `diagram_probe.json`; the Spherogram-based
producer is `diagram_probe.py`. It was not expanded into a search after the
global obstruction made the proposed ribbon construction impossible.

## Exact remaining step and one next action

No actual genus-two mixed compression curve with all four surface connectors,
embedded cap, framed Whitney disk, or modifying annulus was constructed.
The signed collar intersection is a necessary total, not a complete movie.

Next: draw the SECOND mixed transfer with its four connector paths and measure
its intersections with the same a-collar. Test whether it supplies an opposite
contribution at all; then track full-group labels before any Whitney pairing.
No replacement stabilizer or undirected partner search is scheduled.
