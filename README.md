# Slice–Ribbon counterexample research

**No counterexample found.** Start with the [19 September night handoff](HANDOFF_2026_09_19_OPUS_NIGHT.md), the current state of the whole board. It supersedes the 14 September [`HANDOFF.md`](HANDOFF.md), which is kept for history. Read the retractions in its §4 before relying on anything from earlier sessions.

## Where things stand

Three lanes closed on 19 September, all for a related reason — the certificates this repository can apply only reach **fibered** knots:

- **DG 0-friend mining** is closed by a theorem: Fox–Milnor makes the wild-pair population disjoint from every plausibly-slice census, at any crossing number (0 of 158,174 rows have irreducible `Delta`). See [`research/50`](research/50_the_dg_dataset_is_here_and_the_0_friend_lane_is_closed.md).
- **Infection as a construction** is closed: it fails whenever the infection curve lies on the fiber, which is the real obstruction (not "genus grows," which was wrong and is retracted). See [`research/51`](research/51_why_infection_cannot_make_a_wild_pair.md).
- **Surgery to `d(Sigma_2(K_1))`** is closed over all 28 drillable geodesics. See [`research/52`](research/52_sigma2_K1_is_not_surgery_on_a_knot_via_its_natural_presentation.md).

## GST knots — current status

`B_{3,1}` (GST's slice-but-maybe-not-ribbon knot) is now the **third** independent shortlist killed by the same fibered-only wall: genus 10, **not fibered**, `deg Delta = 16 < 2g`, `det = 1`. Neither Miyazaki Thm 5.5 nor Hom–Park Thm 1.1 reaches it, and Eisermann's Theorem 2 degenerates to `det = 1 (mod 8)`, which it trivially satisfies. See [`research/53`](research/53_the_gst_lane_has_a_known_answer_calibration.md).

That leaves the **link** `L_{3,1}` as the only live GST route, pre-registered as a single congruence: if `L_{3,1}` is ribbon, `det V(L_{3,1}) = 17 (mod 32)`; a different residue would make it slice and not ribbon — the first such object of any kind. Progress on that route:

- The Eisermann pipeline itself is now validated against ground truth: **599/599** SnapPy `RibbonLinks` pass both theorems with 0 tool failures, 134 of them at exactly the residue 17 mod 32 that `L_{3,1}` is tested against. See [`results/opus_2026_09_19_1100_eisermann_validation`](results/opus_2026_09_19_1100_eisermann_validation/README.md).
- The **in-family calibration** `research/53` actually asks for — build `L_{1,1}` (must give 9), then `L_{2,1}` (must give 17, the disputed residue, on a known-ribbon object) — is still **unattempted**. Only after both pass is tracing `L_{3,1}` itself (currently blocked on recovering it from a raster figure rather than a combinatorial description) worth the risk of a false positive.
- A large-scale exact search over the GST 48-crossing diagram itself (band-prefix exclusion to length 4, 15,794 band specs, all replayed) found no ribbon movie to an unknot; see [`research/gst_2026_09_19_exact/REPORT.md`](research/gst_2026_09_19_exact/REPORT.md).
- A separate seven-hour bounded movie search (common-upper and stabilized-disk searches over Abe–Tagami/K7a2-K10n4 targets) was launched via [`.github/workflows/astra-seven-hour-movie-search-20260919.yml`](.github/workflows/astra-seven-hour-movie-search-20260919.yml); see [`research_jobs/astra_seven_hour_20260919`](research_jobs/astra_seven_hour_20260919/README.md) for scope. Its evidence is a GitHub Actions artifact, not yet reflected in this repository — check the workflow run for outcome before assuming it finished or found anything.

## The one real advance today

Risk 1/2 of the mixed-lift review is now closed independently for `K_0`, `K_1`: the graded Euler characteristic of the stored HFK bigradings equals `Delta` computed with no Floer code and no Seifert surface (reduced Burau, 9/9 controls), at `[1,-3,5,-3,1]` for both. Not closed: the lift to a homogeneous minimal complex, and `K_2`/`K_3`.

## Older but still-standing results

- The **Abe–Tagami** difference has a nonribbonness argument; smooth sliceness is unknown. See the [marked-annulus audit](research/14_marked_annulus_audit.md) and [infection compatibility audit](research/15_infection_target_compatibility.md).
- Branched double covers separate `K_0`, `K_1` (`Sigma_2(K_0) = L(13,5)`, `Sigma_2(K_1)` non-cyclic `pi_1`) — not a concordance obstruction, but opens a [d-invariant gate](research/21_branched_double_covers.md).
- The **Teichner lane** (`D_{0,1} # J`) has run out of tractable partners; cost roughly doubles per two crossings of the sum, and `max_band_len` saturates at 6. See [the saturation measurement](results/band_generator_saturation.json) and [what's still open](UNFINISHED.md). A broader Miyazaki-pair search over 35,612 wild pairs (`results/ce_hunt_2026_09_19`) is running with 0 hits so far — weak evidence at best, since GHMR's own walker also fails on known-ribbon `L_{1,1}`/`L_{2,1}`.
- Rasmussen's `s` is zero on all four knots of both `r = 0` RBG pairs — survival, not evidence.
- The **link census lane is closed**: of 34,590+7,463+1,101 tabulated hyperbolic links to 14 crossings, 115 are certified non-ribbon by Eisermann Theorem 1, and all 115 are provably not slice ([session record](SESSION_2026-09-15b.md) §14-17).

## Saved/archived work

`results/astra_genus_one_2026_09_18/`, `results/astra_one_commutator_2026_09_18/`, and `results/sr_foxy_combined_saved_work_2026_09_19/` are an explicit-construction side investigation (spatial models, mesh/group verification, a marked genus-one surface) preserved from earlier sessions, including original zips for recoverability. They record no counterexample and are not part of the GST/Teichner/RBG lanes above.

`graph-reconstruction/` is a self-contained side project on the Kelly–Ulam conjecture, unrelated to slice–ribbon. No counterexample there either.

See [reproduction instructions](REPRODUCE_2026-09-12.md), [exact Floer-filter diagram](figures/common-successor-filter.png), and [an actual search move](figures/fusion-example.png). All development stays on `main`.
