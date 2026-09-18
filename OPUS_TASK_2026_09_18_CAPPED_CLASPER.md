# Concrete geometry task for Opus

Prepared 18 September 2026 at the user's request to coordinate if useful.
This file is a handoff; it does not mean an external Claude session has been
started or notified. Keep all progress on existing main; preserve concurrent
work. Read research/41--43 before starting.

Update: research/42 now gives a separate disk-push surface argument realizing
the whole correction while preserving the unlink and exact E. The task below
is still a valuable independent *diagrammatic audit*, but is no longer our
only boundary-existence route. The higher-priority 4D task is to identify the
marked product disk exterior and construct an immersed annulus movie for the
repaired pair. Record its signed double-point group labels and framing, as
specified in research/43. Do not infer embeddedness from the word conjugacy.

## Target

Construct and audit one marked Y-clasper for the 0110 auxiliary link which
inserts the tenth factor of the saved correction:

    [x3^-1 x4, x1^-1 x3].

The x_i are the one-based boundary Wirtinger generators, not the source knot
generators. Inputs:

- `results/astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json`
- `results/night_2026_09_18/word_correction.json`
- `results/night_2026_09_18_surface/surface_certificate.json`, factor 10
- archived `pass09_product_collar/diagram_core.py`, full path in the manifests

## What a useful answer must certify

1. An actual annular-leaf Y-graph disjoint from R and the auxiliaries, including
   leaf framings, stems, basepoints, and labels. The proposed leaf words are
   u=x3^-1 x4 and v=x1^-1 x3; the third leaf is a meridian of eta2.
2. A correctly framed cap for the third leaf, disjoint from R and eta1,
   intersecting eta2 once. This identifies the tame move with R fixed.
3. A cap for another leaf, disjoint from both auxiliaries and the rest of the
   clasper, but allowed to pierce R. This gives the separate unlink certificate.
4. Verify that puncturing/completing each cap describes the SAME surgery;
   compute the actual transported based word of eta2. Do not replace this
   computation by the slogan that claspers are commutators.

Research/41 proves a conditional implication: these cap and null-LP hypotheses
preserve the auxiliary unlink and E=0 simultaneously, with transported lifts
and push-offs. A cap intersecting eta2 is compatible with the all-annular
surgery handlebody being disjoint from eta2. Keep those neighborhoods separate.

## Known trap and limits

The obvious calibrated point-push braid has the correct deleted-axis word
and identity meridian Fox matrix, but a nonzero longitude row
`+/- (2-t-t^-1)` in all six local strand orders. See
`results/night_2026_09_18_geometric_gate/point_push_certificate.json`.
Do not silently identify that braid with the proposed capped-null-clasper.

Do not run broad knot searches or long HFK jobs. A small diagram, exact local
Kirby move, or a specific obstruction to one cap would be a valuable result.
This task constructs only one factor. It does not establish an embedded
modifying annulus, a standard-B4 slice disk, or a nonribbon resulting boundary.
