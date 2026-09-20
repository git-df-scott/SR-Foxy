# Checkpoint8 — first non-q=1 coloured test implemented

2026-09-20 02:57UTC. No counterexample. Shared weekly usage16% at start,17% at finish; baseline7%, total14extra points, buffered stop20%, deadline04:41:43UTC. Repository local3e4461e and remote2a07128 unchanged; prior bibliography correction remains ours. All bounded local jobs complete. No paused remote run restarted.

## New test and controls

`variable_parallel.py` now supports component multiplicities0..3 with independent Seifert-framing corrections. Six knot-only controls (two- and three-parallels of3_1,4_1,6_1) agree with the earlier braid-cabling implementation and have all mutual linking numberszero. Deleting a component is represented by widthzero in the tracked braid. Crossing-free braid components are counted explicitly.

`suzuki_root_minus_one.py` contracts ordinary cable Jones traces in F101[x]/x^r atv=10+x; since10^2=-1mod101 this probesSuzukiq=-1. `suzuki33_term.py` uses the varying precisionr=a+b-1 required by the coefficients, then `combine_suzuki33.py` combines the13 contributing traces. All16 terms were considered in the symbolic design; three vanish at the required precision before computing any trace. The baseline requires numerator coefficients0..3 to vanish; a nonzero coefficient4 obstructs the additionalPhi2 factor. Zero modulo101 is only inconclusive, not full ideal membership.

| input | traces complete | numerator coefficients0..4 mod101 | result |
|---|---|---|---|
| ribbonL10n36 |13/13|[0,0,0,0,0]|no obstruction|
| WhiteheadL5a1 |13/13|[0,0,0,0,66]|**nonribbon obstruction detected**|
| L10n57 |13/13|[0,0,0,0,0]|no obstruction at this prime/root|
| provisionalGSTn1 |11/13|partial sumzero|**incomplete; no conclusion**|

Whitehead is a known nonslice control, not a counterexample. Its largest(3,3)cable trace was independently compared with the full Regina polynomial; allfive coefficients agree (`INDEPENDENT_FULL_REGINA.json`). Other traces with<=40crossings also receive independent full-polynomial checks. The ribbon control and baseline checks pass. These controls show the implementation can detect an actual failure at the intended root.

Each term has saved input/output braids, PDs, component multiplicities, framing self-writhes, Taylor coefficients, layout seeds and full Morse events under `suzuki33/<name>/<ab>/`. The complete combination is `COMBINED.json`. Each term was bounded at20seconds and20000states. Do not conflate separate partial-sumzeros with complete tests.

## Failures and corrections retained

The first L10n36 run had a fixed five-term precision reset inside the probe even when the caller requested fewer terms. Independent controls caught incompatible inverses/Jones checks. The entire initial run is archived as `L10n36_INITIAL_PRECISION_FAILURE`; no outputs from it are used. The corrected probe uses its precision argument.

The(0,3)control traces forWhitehead andL10n57 exposed a crossing-free braid-component count error: Spherogram stores those separately. The assertion now checks visible plus unlinked components. Initial logs are retained as `initial_component_count_failure.log`; only those two failed terms were rerun. Original STATUS.json files describe the first batch; final COMBINED.json and REPAIRS.json record the corrected complete control runs.

GSTn1 terms(2,3) and(3,3) hit20000-state caps; these are resource failures. No target obstruction was found. A layout-only audit, without repeating contraction, preserved the best seeded layouts:

| term | crossings | maximum frontier strands | Catalan upper bound |
|---|---:|---:|---:|
| (2,3) |126|22|58786|
| (3,3) |162|24|208012|

`SUZUKI33_GST1_LAYOUT_LIMITS.json` saves the events, seeds and exact scores. These bounds describe potential state counts, not measured memory and not proofs that every state occurs.

## Next bounded options

Use the saved layouts to attempt only the two missing GSTn1 traces with explicit larger state budgets and timeouts, if useful for calibration. The profile supplies a concrete cost estimate; avoid recomputing the11successful traces. A modest state-limit increase may still fail on(3,3); label that inconclusive. Do not extrapolate to a blind six-parallel GSTn3 computation. A tangle/representation-based contraction that avoids expanding all parallels would be the more substantial algorithmic step.

The separate GSTn3(2,2)exact Taylor test remains uncomputed; allGSTn1–3mixed(2,1)choices pass exactly. A partial or complete link-obstruction failure would still need a source-certified standardB4 disk construction and a valid universal transfer to the same knot before claiming a knot counterexample. Literal GST dotted-band transport is still an independent geometric lead.

Underlying theorem/formula source remains Suzuki, *On the colored Jones polynomials of ribbon links, boundary links and Brunnian links*, Banach Center Publications100(2014),213–222, DOI10.4064/bc100-0-12, https://arxiv.org/abs/1111.6408, Theorems2.2/3.1; source PDF and verified metadata saved atcheckpoint6. The modular criterion and computations above are our explicit derivation and implementation. No extension from boundary/ribbon links to all slice links is assumed.
