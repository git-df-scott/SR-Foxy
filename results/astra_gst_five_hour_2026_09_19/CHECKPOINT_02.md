# Checkpoint 2 — September 19, 2026, 6:13 PM MDT continuation

**No counterexample. New source agreement and independent exact polynomial verification.** Shared weekly usage displayed 8% at entry and at the milestone; baseline remains 7%, hard buffer stop 13%, deadline remains 04:41:43 UTC. Origin/main remains bd80f8e. No remote search restarted.

## Second source diagram agrees through n=3

`build_gompf6.py` separately transcribes the primary diagram gompf6.pdf: four components, 22 outside crossings, and four full-twist boxes. This uses different outside geometry and different crossing assignments from `build_preblow.py`'s Figure example trace (eight outside crossings). The two implementations share the braid-generation helper and the PD convention, so this is not independence of every assumption.

For n=1,2,3 at k=1, SnapPy reports an isometry between the four-cusped exteriors with cusp permutation [0,1,2,3] and peripheral matrices -I,+I,-I,-I. These preserve every labelled meridian and the red +1/-1 surgery slopes. Thus the numerical comparison respects the full surgery data, not only volumes or unmarked exteriors. The other isometry exchanges red cusps and reflects slopes; it is not needed. Both red sublinks simplify to two crossing-free unknots.

After filling the two red cusps, the two implementations also give matching peripheral-marked two-cusped exteriors. The approximate volumes are 12.1390113315, 15.6792526732 and 18.3972750565 for n=1,2,3 respectively. Full maps are in SOURCE_COMPARISON_n1.json through n3.json. These are numerical isometry reports, not independently certified interval geometry or exported Pachner certificates. No source-identification claim was silently upgraded.

This agreement makes the old Figure 1 n=1 spiral-collapse interpretation a more focused suspect. It does not prove which source interpretation is correct: common twist/framing assumptions remain to be checked. In particular, do not replace the source problem with fitting a trace to the expected residue.

## Independent Jones arithmetic passes

Regina 7.4's treewidth algorithm independently computed the entire Jones polynomial for eight diagrams: trefoil, figure-eight, Hopf link, L10n36, and reconstructed n=0,1,2,3. After the documented x=-q convention change, every coefficient equals the existing repository engine's output. All arithmetic in the comparison is integer arithmetic. REGINA_JONES_CHECK.json preserves both coefficient lists and timings; check_regina_jones.py reproduces them.

Consequently the provisional n=3 value det V=241=17 mod32 is supported by two different Jones implementations. It does not obstruct ribbonness. The n=1 invariant discrepancy (-23 for stored L11 versus 73 for the new trace) survives this independent check.

## Failed limited simplification and next work

A deterministic Regina type-I/type-II reduction was attempted for both pre-blow-down diagrams at n=1,2,3. No crossings were removed: Figure example stayed 24,28,32 and gompf6 stayed 38,42,46. Their diagram signatures differ. This only says those immediate simplifying moves do not supply an equivalence certificate; it is not evidence against the isotopy.

Next: resolve the shared twist convention against Gompffig3b and the explicit k=1 intermediate pictures, and audit the Figure 1 connector at n=1. Seek a reproducible Reidemeister/Pachner move certificate between the separately transcribed surgery diagrams, if feasible within budget. Do not repeat the eight successful Jones checks without a changed input. Then consider generalized n,k or the still-open ribbon-preserving satellite transfer; do not infer knot nonribbonness from a GST-link test alone.

Sources already retrieved: GST primary arXiv:1103.1601v1 (Text.tex describes gompf6-to-example as an isotopy), original PDFs under sources/; installed Regina 7.4 Link.jones documentation specifies x=-q conversion. The new work here is computation on saved inputs, not a new external theorem claim.
