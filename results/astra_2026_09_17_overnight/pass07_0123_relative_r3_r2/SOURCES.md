# Source and scope record

- SR-Foxy main input: `9d4634224db3c32dce419e67510c994111bd7502`, especially pass06 and `data/knots/AbeTagami_marked_product_scaffold.json`.
- Spherogram source commit `ea6da8a70a581a37f15fa4837a79fa7d63fad91e`:
  - `spherogram_src/links/simplify.py`: `possible_type_III_moves`, `reidemeister_III`, and the RII criterion in `reidemeister_I_and_II`.
  - `spherogram_src/links/links_base.py`: `CrossingStrand.next_corner` / face traversal.
  The checker ports these small combinatorial rules; it does not import Spherogram.
- JungHwan Park, *A Construction of Slice Knots via Annulus Modifications*, arXiv:1512.00401. This pass does not claim Park's 0-standardness hypothesis; it only improves the explicit boundary geometry.

Reading scope was targeted to pass06, the marked scaffold construction, research/14's changed-axis proposal, and the cited Reidemeister implementation. No exhaustive repository or literature audit is claimed.
