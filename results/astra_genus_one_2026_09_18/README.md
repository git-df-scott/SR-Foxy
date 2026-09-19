# Astra: explicit genus-one realization and framed boundary

**CE: NO.** Start with `REPORT.md` and `VERIFICATION.json`.

The frozen geometric object is an embedded genus-one surface with two boundary
components, not a modifying annulus or a slice disk. The actual surgery link is
R,a,b', with preferred coefficients +1,-1. Its auxiliary sublink is an unlink;
its exact longitude response is zero and its filled Alexander polynomial is d².
No identification with D01 or new global nonribbon proof is asserted.

## Essential files

- `correction_cobordism_mesh.json`: integer PL surface, incidence, both boundaries.
- `marked_genus_one.obj`: surface plus R,a, for spatial inspection.
- `marked_genus_one_spatial.png` / `.svg`: marked centerline view of the model.
- `surgery_diagram.json`: integer polygons, generic projection, all 675 crossings,
  signed Gauss words and intended axis words.
- `surgery_link.json`: construction-level polygons, joining band and surgery slopes.
- `framed_fox_boundary.json`: full peripheral presentation, 670 Laurent-unit pivots,
  reduced matrix, longitude response and Smith calculation.
- `filled_maximal_minors.json` and `two_parameter_minors.json`: exact determinant
  certificates for the specified and parameterized fillings.
- `auxiliary_group_certificate.json`: full link-group proof of null longitudes.
- `surface_boundary_framing.json`: explicit mutual-linking calculation for the
  surface's two boundary components; induced normal framings are zero.
- `stallings_probe.json`: conditional no-compression result under q0.
- `independent_*_check.json`: separate arithmetic/geometry/group replays.
- `prior/`: the unchanged prior one-commutator package and frozen inputs.
- `attempt01/`, `attempt02/`: failed or superseded geometry/diagnostics, not results.

Producer snapshots retain their original pending-validation status strings.
`VERIFICATION.json` records the subsequent completed checks. A pending producer
label is not a claim that the final geometric checks were skipped.

## Recheck the frozen certificates

Use a fresh copy of this directory. The checkers may rewrite their own output
JSON files in that copy. Do not run construction scripts over an active research
checkout's uncommitted results.

```
node check_exact_independent.mjs
python3 check_mesh_independent.py
python3 check_subgroup_independent.py
```

The independent verifiers use Node.js BigInt and the Python standard library.
The subgroup checker requires assertions enabled. They do not require SnapPy,
Sage, Regina, a network connection, or access to the Mac checkout.

The first checker independently reconstructs the polygon projection, full
peripheral data, auxiliary sublink presentation, every recorded pivot and Tietze
move, the exact determinant and the all-parameter extension. The second uses
rational segment clipping rather than the producer's triangle-intersection
algorithm. The third uses a separate graph-quotient implementation.

To regenerate calculations from frozen geometry in a fresh copy:

```
python3 mesh_check.py
python3 check_spatial_marking.py
python3 splice_axis.py
python3 build_correction_cobordism.py
python3 framed_fox_boundary.py
python3 check_auxiliary_group.py
```

Construction planning in `build_spatial_model.py` uses NumPy, NetworkX and Shapely;
see `environment.json`. Do not assume a route regenerated with different
versions has the same geometry. Recheck its integer mesh and markings.
`planar_base.json` is retained as an explicit input embedding.

The failed full filled-group simplification is documented by
`filled_group_certificate.json` as TIMEOUT_UNKNOWN. Its original complete input
presentation is available from the framed Fox file plus the two stated surgery
relations. Do not report the timeout as nonidentity or nonsliceness.

## Immediate handoff

The entire old 104-letter repair now has an explicit one-handle geometric
realization. Do not rediscover A,B, repeat the knot census, or merely raise band
length. Convert this certified auxiliary unlink to an explicit marked unlink
isotopy/spanning-disk system and transport R through the +1,-1 Rolfsen twists.
The new knot must be identified or given its own nonribbon proof. An immersed
annulus between a and b' would then be a separate four-dimensional object; the
existing correction surface b^- to b' is not that annulus and cannot be assumed
compressible under the saved q0.

No changes were pushed in this session. No branch was created; the Mac checkout
was not accessed. The read snapshot was main at ceb83c2c86c4b538599f95b62812587d2fa3c6fe.
