# Checkpoint 9 — GST1 root test completed

2026-09-20 03:32 UTC. No counterexample. Weekly usage 17% at start, 18% at finish; original baseline 7%, total allowance 14 additional points, buffered stop 20%, deadline 04:41:43 UTC. Reset remains 1790432260/61 (one-second reporting variation). No local jobs remain. Paused remote searches were not restarted. Local status and remote main are unchanged from checkpoint 8; remote main is 2a071282514b448da4b5f0ab44afcc3308fee562. Preserve concurrent untracked research files.

## Exact question and scope

For the provisional source-derived GST1 link, does the Suzuki (3,3) necessary ribbon-link condition fail at q=-1, detected modulo 101? Use v=10+x, q=v^2, over F101. The combined numerator must vanish modulo x^5; a nonzero degree-four term after the four Habiro baseline zeros would obstruct ribbonness. This is a link test. A knot counterexample still requires a precisely identified knot, a smooth disk in standard B4, and an independent global nonribbon proof.

## Completed calculation

Only the two missing cable traces were retried; the eleven completed traces were preserved. Saved Morse layouts were reconstructed and compared with input PDs using Regina signatures with reflection disallowed. Component reversals and diagram rotation were allowed; zero pairwise linking numbers were separately checked, so component orientation changes do not alter the normalized Jones polynomial. The comparison certifies the saved diagram representation, not the original GST source identification.

| Trace | Crossings | Precision | Peak retained states | Runtime | Required coefficients mod 101 |
|---|---:|---:|---:|---:|---|
| (2,3) |126|4|58,543|24.214 s|[0,0,0,0]|
| (3,3) |162|5|208,009|170.187 s|[0,0,0,0,0]|

The first (3,3) retry hit its 90-second limit at event index 107, with peak 207,945 states. That failure is retained. A second explicitly bounded attempt used 240 seconds and the same 210,000-state cap and completed at event index 193. No full-polynomial independent calculation was attempted for these two large traces; the previously independent small controls and Whitehead full-polynomial cross-check remain the implementation controls.

`COMBINED.json` now contains all thirteen terms, with numerator [0,0,0,0,0]. The earlier incomplete file is preserved as `COMBINED_CHECKPOINT08.json`. This is a complete modular test with no detected obstruction, not an exact divisibility proof, not a proof of ribbonness, and not grounds to close higher colours, other roots/primes, or other GST parameters.

Reproducible artifacts: `retry_suzuki33_saved_layout.py`, `suzuki33/GST1/{23,33}/RESULT.json`, both 90-second audit records and the 240-second audit record, input SHA256 hashes, original PDs and saved Morse events. The stale root-probe docstring was corrected to the actual F101 / v=10+x computation; arithmetic was unchanged.

## Next-test prerequisite discovered

The earlier handoff listed GST3 (2,2) as uncomputed. A schema audit now shows that the existing driver cannot simply run it: both GST3 `POLYNOMIALS.json` files omit the full AAB traces, while saved exact mixed traces have only six coefficients. The (2,2) numerator needs eight. Its multiplier a=v+v^-1+v^3+v^-3 has a(1)=4, so the missing degree-six and degree-seven trace coefficients directly affect the obstruction. Passing the lower mixed test does not supply them.

`GST3_DOUBLE_PRECISION_AUDIT.json` saves the formula, missing data and correction steps. Before the GST3 (2,2) test: recompute both mixed traces to order eight (reuse c0's saved verified layout; c1 needs a saved seeded layout), then audit the four-parallel state cost before bounded contraction. Do not run `suzuki_double_colour.py GST3` unchanged or pad the unknown coefficients with zeros.

## Evidence and remaining obligations

Established theorem source: Sakie Suzuki, *On the colored Jones polynomials of ribbon links, boundary links and Brunnian links*, Banach Center Publications 100 (2014), 213–222, DOI 10.4064/bc100-0-12; https://arxiv.org/abs/1111.6408, Theorems 2.2/3.1. The modular criterion and calculations are our derived test; source PDFs and the derivation were saved in preceding checkpoints.

The remaining campaign has two displayed percentage points before its operational stop. Prioritize a bounded GST3 precision upgrade/layout audit, or source-certified literal dotted-band transport, rather than blindly expanding GST3 six-parallels. GST1's zero does not justify an all-slice extension of Suzuki's theorem. Source identity qualifications and the missing universal link-to-knot nonribbon implication remain. Final campaign checkpoint must finish before 04:41:43 UTC and pause the automation, or earlier if displayed usage reaches 20%.
