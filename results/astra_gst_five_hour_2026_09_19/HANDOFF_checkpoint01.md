# Five-hour GST campaign — checkpoint 1

**Active campaign, not finished. No counterexample.** Started 2026-09-19 23:41:43 UTC (5:41:43 PM MDT). Hard end 2026-09-20 04:41:43 UTC (10:41:43 PM MDT). Shared weekly baseline 7%, reset 1790432261, total allowance 7 additional percentage points. Latest displayed use 8% at 23:56 UTC. Stop with buffer at displayed 13%; allowance does not restart at checkpoints. Automation `slice-ribbon-next-5-session-at-4-pm` now continues this campaign every 30 minutes and replaces the earlier 9 PM reminder. Pause it at campaign end. Do not restart remote run 35455048082.

## Concrete new lead: bypass manual framed blow-downs

The installed SnapPy 3.3.2 implements Dunfield–Obeidin–Rudd peripheral-marked `exterior_to_link`. Thus a correctly transcribed four-component pre-blow-down diagram can be filled along the two red +/-1 surgery components, permanently filling only those cusps. Reconstruction with the surviving meridians then produces an explicit two-component link diagram in S3. Source transcription and framing still need independent verification; the reconstruction algorithm does not fix a wrongly transcribed input. All runs enabled check_input, check_answer and careful_perturbation, seed 20260919.

`build_preblow.py` transcribes primary Figure `example` using exact rational polygon intersections, eight explicitly specified outside crossings, full twist braids in four boxes, and tracked component edge labels. For k=1 its crossing count is 20+4|n|. A=outer red (+1), I=inner red (-1), B=large black, M=small black. The red sublink simplifies to two crossing-free unknots. Their surgery leaves meridian filling S3; the filled group simplifies to the trivial presentation. `reconstruct.py` saves triangulations, PD codes and exact Jones calculations.

These are EXPERIMENTAL source transcriptions. They are precisely identified combinatorial links, but are NOT yet certified GST links. Do not silently upgrade source identity from matching invariants.

| drawing n | k | reconstructed crossings | component dets | det V | mod32 | product mod32 |
|---|---|---|---|---|---|---|
| -1 | 1 | 10 | 1,9 | -23 | 9 | 9 |
| 0 | 1 | 10 | 1,9 | -23 | 9 | 9 |
| 1 | 1 | 18 | 1,9 | 73 | 9 | 9 |
| 2 | 1 | 38 | 9,9 | -143 | 17 | 17 |
| 3 | 1 | 62 | 9,9 | 241 | 17 | 17 |

Every row has two components, linking number zero and Jones nullity one. Its zero surgery group computationally simplifies to two generators with no relators. Component Jones polynomials for n=1,2,3 match Q and T(n,n+1)#mirror exactly (`COMPONENT_JONES_CHECK.json`); this is an invariant check, not a knot-identification proof. All rows pass the ribbon congruence. The alternate global twist convention n=-1,k=-1 was also tested: dets 1,25 and det V=-71; it fails the intended square-knot component check. File tag 101 denotes drawing n=-1,k=1, while file tag -1 denotes n=-1,k=-1; actual n,k are stored in both inputs and results.

## Crucial control inconsistency

The repo's stored L11 at commit 17b6785 has det V=-23 and approximate volume 7.3277247534. The new drawing n=0 (and n=-1,k=1) matches it: SnapPy reports meridian-preserving isometries extending to link equivalences. The new n=1 instead has det V=73, volume approximately 12.1390113315, and cannot be the same link because its exact Jones invariant differs. See `L11_CONTROL_COMPARISON.json` for peripheral maps. The numerical isometry report is supporting evidence; no separate interval-certified isometry or standalone move certificate was produced.

Do NOT tune the new construction to the stored control and call that source certification. At least one parameter/transcription interpretation is wrong or incomplete. A plausible explanation is that collapsing the Figure 1 spiral to one rounded loop in the published L11 loses its connector placement even at n=1. This is only a hypothesis. An error in this new Figure example trace or its box convention remains possible. Resolve against the primary vector paths and intermediate figures Gompffig3b, gompf6, Gompffig4/5. Their original PDFs/EPS are saved under sources/. The newly reconstructed n=2 and n=3 cannot be called certified L21/L31 until this is resolved.

## Next checkpoint: exact order of work

1. Independently review all eight outside crossings and all four full-twist conventions against source example.pdf/EPS; verify source labels against Text.tex. Compare with gompf6/Gompffig3b rather than inventing additional parameter readings. The source text asserts Figure example is obtained by isotopy; exploit that independent diagram.
2. Audit the old Figure 1 n=1 connector interpretation. Record whether it actually represents n=0. Seek a literal diagram/isotopy certificate; matching component polynomials and surgery groups are insufficient to select the correct link. The current mismatch is a reproducible finding, not a conclusion that the old author is wrong.
3. If the source family is certified, repeat the exact Jones test through an independent normalized implementation or compact recurrence. The n=3 result 241=17 mod32 would close only this obstruction on this member, not GST or ribbonness.
4. Explore generalized n,k only after source identity checks. Also retain the ribbon-preserving satellite avenue (Eisermann Prop.6.13); research/28's blanket closure was retracted. Any link nonribbon result must be connected to the same slice knot by a valid universal implication.
5. Falsify rather than assume research/54's empirical mod16 rule. It is based on 189 square-determinant examples, not a theorem. An unexpected residue is a discrepancy to investigate, not automatically a bug. Also square determinant is only one necessary Fox–Milnor consequence, not satisfaction of the polynomial factorization condition.

## Reproduction and preservation

Environment: /tmp/sr-foxy-20260919-leads-venv/bin/python. Scripts import the existing repository scripts/sagefree_jones.py and sagefree_eisermann.py, with the corrected component extractor copied from origin/main into sources/compdet.py. All inputs, outputs, source excerpts and logs are local in this directory. PREBLOW_n1.svg is an annotated view of the experimental transcription. Outputs from completed experiments should not be overwritten when testing variants; use a distinct run directory/tag. No long computation is currently required or authorized remotely.

The checkout stayed at 3e4461e; origin/main fetched to bd80f8e. Concurrent untracked work was preserved. Future checkpoints should inspect only changed repository state, not reread the entire archive. Relevant GPT task Find GST Knot Counterexample was inspected: its saved package preserves exact PD/Floer results with source-identification caveats; it does not contain a nonribbon proof.

## Sources and limits

GST: R. Gompf, M. Scharlemann, A. Thompson, Fibered knots and potential counterexamples to the Property 2R and Slice-Ribbon Conjectures, Geometry & Topology 14 (2010), 2305–2347, arXiv:1103.1601v1 (2011-03-08), https://arxiv.org/html/1103.1601v1. Figure example and its preceding paragraph supply the surgery construction and claimed isotopy. Source archive was previously downloaded and hashed.

N. Dunfield, M. Obeidin, C. Rudd, Computing a Link Diagram from its Exterior, arXiv:2112.03251, https://arxiv.org/abs/2112.03251; implementation contract: https://snappy.computop.org/triangulation.html#snappy.Triangulation.exterior_to_link. Checked 2026-09-19. The method uses specified meridians, rather than recognizing unmarked exteriors as link identities.

M. Eisermann, The Jones polynomial of ribbon links, Geometry & Topology 13 (2009), 623–660, https://pnp.mathematik.uni-stuttgart.de/igt/eiserm/publications/ribbonlinks.pdf. Cor.6.9 supplies the mod32 test; Prop.6.13 supplies ribbon-preserving satellite transfer. Neither identifies our source transcription nor proves nonribbonness here.
