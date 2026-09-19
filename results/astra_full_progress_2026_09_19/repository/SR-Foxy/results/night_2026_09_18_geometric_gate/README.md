# Peripheral tests and surface realization

18 September 2026. Read research/41--43 for the mathematical statements and
their limits. All computations below are finite, deterministic, and small.

- `peripheral_certificate.json`: oriented boundary transport and two exact
  source-group identities prove the preferred longitude is killed by every
  saved q_n. This is necessary compatibility, not a marked disk identification.
- `point_push_certificate.json`: six local strand orders realize the small
  commutator but have nonzero longitude row `+/- (2-t-t^-1)`, despite an
  identity specialized meridian Fox matrix. No full-scaffold splice is claimed.
- `surface_recipe.json`: the 26 handle targets of the genus-13 construction
  in research/42, with at most 614 disk-push instructions. The independent
  checker replays the word inputs and insertion order; geometry is established
  by the written argument, not by this JSON. No marked PD has been generated.
- `independent_review.md`: distinct audits of the capped-clasper criterion,
  disk-push argument, fixed-collar framing, and exact linking calculation.

Reproduce from repository root with Python 3 (standard library only):

```sh
python3 results/night_2026_09_18_geometric_gate/peripheral_gate.py > /tmp/sr-peripheral.json
python3 results/night_2026_09_18_geometric_gate/point_push.py > /tmp/sr-point-push.json
python3 results/night_2026_09_18_geometric_gate/surface_recipe.py > /tmp/sr-surface-recipe.json
python3 results/night_2026_09_18_geometric_gate/check_peripheral.py
python3 results/night_2026_09_18_geometric_gate/check_point_push.py
python3 results/night_2026_09_18_geometric_gate/check_surface_recipe.py
```

The first two producers have 30-second CPU limits; the point-push producer
also bounds intermediate word lengths. The surface recipe has exactly 26
finite words. Our complete reproduction/check run took under one second.
The peripheral checker uses an archived independent Tietze/relator replay;
the point-push checker uses Laurent first jets instead of the producer's
free-word substitution. Deliberately corrupted crossing sign, zeroed longitude
response, and wrong insertion order are rejected. The upstream surface
checker additionally rejects two corrupted commutator/relator certificates.

No broad census search, HFK job, or random search was run for this package.
The remaining 4D annulus and actual nonribbon boundary are unestablished.
