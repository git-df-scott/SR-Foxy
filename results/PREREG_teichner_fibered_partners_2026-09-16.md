# Pre-registration: Teichner search on `D_{0,1} # J` for the three fibered ribbon partners

Written **before** the run was launched, 16 September 2026. Decision rules below
are fixed and are not to be retuned after seeing results.

## Why this run is legitimate at all

`UNFINISHED.md` §2, `HANDOFF.md`, `SESSION_2026-09-15.md`, `research/24` §3 and
the docstring of `scripts/teichner_mirror_partners.py` all excluded `8_9`,
`8_20`, `9_27` a priori, on the ground that Miyazaki's pairing theorem still
returns non-ribbon for `D_{0,1} # J` when `J` is fibered. That exclusion is
**withdrawn** — see `ERRATA_2026-09-16.md`. Miyazaki [S07, Thm 5.5] requires
*every* prime fibered summand to satisfy one of two alternatives, and a
nontrivial ribbon `J` satisfies neither. So the theorem does not apply to the
sum and cannot obstruct a certificate.

## Target and box

* Target: `D_{0,1} = K_0 # (-K_1)`, from `data/knots/AbeTagami_D_0_1.json`.
  Already certified **non-ribbon** by the Miyazaki/Abe-Tagami audit, so a
  *verified* certificate here is a counterexample to Slice-Ribbon outright.
* Partners `J`: `8_9`, `8_20`, `9_27`, in that order.
* Box, chosen to match the **completed** `8_8` run exactly so the outcome is
  comparable rather than novel: `max_bands = 2`, `max_band_len = 5`,
  `max_twists = 2`, `paths = 'shortest'`, canonical diagram (`TEICHNER_SEED`
  unset). The `8_8` run in this box took 7.96 h at 33 crossings and found no
  certificate.
* Runner: `scripts/teichner_certify_nosage.py`. Its slice filter is
  `sagefree_slice_filter`, strictly weaker than spherogram's Sage filter, so it
  keeps more links in the search and cannot lose a disk. Coverage claims remain
  valid; SageMath is not installed in this container.
* Command, verbatim:
  `TEICHNER_J=8_9,8_20,9_27 python3 scripts/teichner_certify_nosage.py results/teichner_D01_fibered_partners.json 2 5 data/knots/AbeTagami_D_0_1.json`

## Controls, not optional

The script computes and verifies a ribbon certificate for each `J` **on its own**
before touching the sum. Each of `8_9`, `8_20`, `9_27` is a ribbon knot, so
`partner_certificate_verified` must come back `true` for all three. **If any
partner's own certificate fails to verify, that partner's row is void** and is
reported as void, not as a negative.

## Decision rules, fixed in advance

1. `certificate_verified == true` is **not** a counterexample by itself. It is a
   candidate requiring, before any claim is made: an orientation-compatible
   peripheral identification of every intermediate link (`are_same_link` allows
   mirror equivalence, which is not enough), and a replayable movie.
2. `unknot_endpoint_found == true` with `certificate_verified == false` is a
   **failed verification**, reported as such, never as a hit.
3. No certificate within the box is **coverage of that box only**. It is not a
   non-existence proof and not evidence that `D_{0,1}` is non-slice.
4. A run killed by the wall clock or container reclamation is **UNKNOWN** for
   that partner, never a negative. An unfinished search supports no conclusion.
5. Negatives and voids are reported with the same prominence as a hit.

## Prior, stated in advance

Low. Two comparable completed runs (`6_1` at 31 crossings, `8_8` at 33) returned
no certificate in this box. What this run buys is that three partners wrongly
ruled out on a theorem error are returned to the board in the cheapest crossing
band; it is not a reason to expect a hit.
