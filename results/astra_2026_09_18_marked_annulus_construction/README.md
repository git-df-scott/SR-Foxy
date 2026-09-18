# Marked product inclusion, a failed compression, and one fixed stabilizer

**CE status: not established.** No immersed-annulus movie, embedded modifying
annulus, or new nonribbon slice boundary was produced.

The strongest new geometric result is the explicit whole-sphere collar in
`GEOMETRY.md`. Its boundary charts agree on both balls and both seam edges;
the actual above-plane whisker pulls back through the saved region-0 bridge.
For this now-specified product model the inclusion is q0. The construction
transports both actual 0110 bands, including their ribbon normal fields.
It does not infer a unique historical disk from endpoint-only data.

The next attempted surface compression failed precisely: both designated
factor-10 handle loops have nonidentity images in SL(2,F_17), with all source
relators checked. Thus those particular compression disks do not exist.
This does not exclude another annulus construction. The genus-13 correction
is still an existence surface, not a newly recorded PD.

**Late update:** the one-commutator publication in `ceb83c2` now gives an
alternative genus-TWO surface. `ONE_HANDLE_UPDATE.md` connects its exact inputs
to this checkout and evaluates both new handle loops in the actual marked
exterior. Both designated caps fail; the second matrix has trace 2 but is
nonidentity. This smaller recipe may have a different embedded endpoint;
its actual PD and surgery boundary remain unknown.

The single pivot is fully specified in `STABILIZER.md`: J=C_(2,1)(K0#-K0),
with a geometric ribbon-disk construction, a 49-crossing PD, and a fixed
74-crossing D01#J diagram. The exact first split saddle was performed. It
produces component types R and D01#R. The latter is nonribbon under the
already checked pairing hypotheses, so that ribbon prefix cannot complete.
The ribbon status of D01#J remains unknown.

## Artifacts and reproduction

- `transport.json`: source hashes, 108 port correspondences, both seam-face
  circuits, both actual band routes and axis traversals, the transported
  correction word, and the two finite-quotient compression tests.
- `stabilizer.json`: the fixed braid and PD inputs, parallel-crossing blocks,
  component projections, the connected-sum diagram, the exact saddle
  attachments, and its complete output PD.
- `surface_attempt.json`: the native orientation checks and genus-14 surface
  ledger. Its annulus movie, double-point labels, and Whitney disks are null.
- `one_handle_connection.json`: the later genus-two alternative, checked
  source correspondence, and both nontrivial q0 handle images.
- `factor_identification/`: the actual stored D01 cut, factor PDs, four
  intermediate triangulations, and a positive mirrored-K1 identification.
- `GEOMETRY.md`: the continuous collar map, framing transport, surface attempt,
  and scope of the compression failure.
- `STABILIZER.md`: ribbon certificate for J and the failed-prefix argument.
- `check_saved.py`: independent standard-library replay of the finite data;
  the continuous geometric proofs and existing nonribbon hypotheses remain
  mathematical inputs, not computer-verified theorems.

From repository root:

```
python3 results/astra_2026_09_18_marked_annulus_construction/check_saved.py
python3 results/astra_2026_09_18_marked_annulus_construction/check_factor_identification.py
```

The producers are `build_transport.py` and `build_surface_attempt.py`
(standard library and archived diagram code), `build_stabilizer.py`
(Spherogram 2.4.1), and `build_factor_identification.py` (SnapPy 3.3.2).
They refuse to overwrite their saved JSON files/directories. For a fresh
production run, copy the scripts to a new results
subdirectory at the same depth. The stabilizer producer has a 30-second CPU
cap; the recorded run completed in under one second. There was one substantive
calculation at a time, no invariant rerun, and no partner or census sweep.
The factor comparison also completed in under one second with a 30-second
CPU cap; its checker passes 48 face checks and rejects a false even map.
The full-surface relative normal framing remains uncomputed.

**Exact missing step:** an actual immersed-annulus movie with measured
double-point labels and subsequent embedded Whitney disks was not obtained;
in the fixed stabilizer pivot, the second ribbon certificate for D01#J is
missing. Research/46--47 does not fill either gap.

**Next action:** on the saved D01#J diagram, construct one mixed first splitting
band using the shorter A whisker from the new one-handle correction. First
supply its marked transfer onto the cable diagram, then identify the output
components before attempting further bands. Do not change partners.
