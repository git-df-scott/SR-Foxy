# Manifest

Cutoff: 2026-08-30. Repository history was preserved; this session only adds the files listed here.

| artifact | what it claims | evidence level | how to verify | unresolved assumptions |
|---|---|---|---|---|
| `SESSION0_BATTLEFIELD.md` | NO CE; identifies the certified frontier and ranks five attack doors | synthesis of primary papers, including 2026 preprints | follow each `[Sxx]` theorem pointer in `SOURCES.md`; check implication chains against `OBSTRUCTION_MATRIX.md` | current-status claims are bounded by the documented search; several 2026 results are unrefereed |
| `CANDIDATE_LEDGER.md` | separates certified smooth-slice/ribbon-unknown objects from non-ribbon/slice-unknown objects | theorem-level primary citations | verify slice ambient manifold, disk construction, signed concordance convention and exact ribbon status row-by-row | openness is reported as `UNKNOWN` when not affirmatively verified |
| `OBSTRUCTION_MATRIX.md` | records which obstruction families can logically touch each serious object | theorem hypotheses plus candidate status | start with [S01,S02,S04,S06,S08]; confirm each cell uses one allowed label | unperformed candidate calculations stay `NOT YET COMPUTED`/`UNKNOWN` |
| `ABANDONED_WEAPONS_2010_2026.md` | distinguishes structurally exhausted homotopy-ribbon tools from unexecuted ribbon-specific tools | primary sources; blog only for discovery | inspect [S13,S17–S20] and compare conclusions to handle-ribbon status | exact text of Turaev Theorem H remains unrecovered/unverified |
| `NEW_WEAPONS_2023_2026.md` | audits genuinely new structures without mislabeling sliceness tools | theorem-level audit of primary papers/preprints | inspect theorem numbers and candidate applications in [S01–S03,S08–S15] | no-application findings are search results, not universal negatives |
| `ABE_TAGAMI_AUDIT.md` | fixes the signed connected sum and states the exact concordance gap | Miyazaki + Abe–Tagami primary theorem chain | verify [S06, Thm. 4.1, Cor. 4.3, §5] and [S07, Thm. 5.5] | no concordance equality or pairwise distinction theorem was verified |
| `GST_AUDIT.md` | proves the exact smooth-slice status, separates stable/ordinary handleslides, states the missing converse | peer-reviewed GST plus later primary work | reproduce [S04, §8] disk/band argument; inspect [S05,S14,S16] | handle-ribbon terminology for every arbitrary band should be checked from its exact handle diagram; fiberedness of (B_{3,1}) is not assumed |
| `SOURCES.md` | bibliographic and theorem-level verification register | mixed peer-reviewed primary and clearly labeled preprints | open linked source and compare theorem number/hypotheses | author metadata for a few very recent multi-author preprints should be read from the linked version; Turaev theorem text incomplete |
| `candidate_ledger.csv` | machine-readable summary of the candidate tiers | derived from `CANDIDATE_LEDGER.md` | diff each row against the Markdown ledger | abbreviated fields omit proof detail |
| `obstruction_matrix.csv` | machine-readable matrix using only allowed cell labels | derived from `OBSTRUCTION_MATRIX.md` | validate labels and compare row/column coordinates | explanatory reasons remain in Markdown |

## Added 2026-09-11

| artifact | what it claims | evidence level | how to verify | unresolved assumptions |
|---|---|---|---|---|
| `CAMPAIGN_PLAN.md` | binding plan: no CE exists, no known invariant can prove one, a new theorem is required; six workstreams, gates, kill conditions | synthesis of the five `research/` audits plus corrected sources | follow `[Sxx]` pointers; check each workstream's kill condition against `ERRATA_2026-09-11.md` | schedule assumes one small team; Oliveira-Smith [S01] unrefereed |
| `ERRATA_2026-09-11.md` | corrections to Session 0, including closure of the Turaev door and two missed candidate lanes | theorem-level re-fetch of every load-bearing source | open `research/01_source_verification.md` and the mathnet.ru Turaev text | none beyond those listed in the file |
| `TOOLING.md` | software stack, install spec, first scripts | repo/docs inspection by the tooling audit | run the install spec on a clean machine | API names must be re-checked against pinned versions |
| `research/01_source_verification.md` | per-source verification table and post-cutoff sweep | primary texts fetched | re-fetch listed URLs | — |
| `research/02_ribbon_only_obstructions.md` | catalog of ribbon necessities and the level at which each dies | primary texts for key items | check each "dies at" label against the cited theorem | Turaev row superseded by `ERRATA` E1 |
| `research/03_candidate_families.md` | all candidate families with ambient tags, ranked table, generators | mixed primary/abstract | check ambient tag row by row | some rows abstract-only, marked |
| `research/04_computational_tooling.md` | tool survey | repo/docs inspection | see `TOOLING.md` | — |
| `research/05_adversarial_memo.md` | history of dead candidates, trap list, probability estimates | primary quotes where marked | check quoted text against sources | probabilities are judgement |

## Global unresolved assumptions

1. “Current status” is frozen at the cutoff and can change after 2026-08-30.
2. No silence-of-literature inference is upgraded to a proof that a problem is open.
3. A preprint theorem is cited as a theorem in that version, not as peer-reviewed fact.
4. `DG` nomenclature follows SnapPy/Hoste–Thistlethwaite style exactly as printed in [S01,S03]: `18nh00000601`.
5. Any future use of Turaev’s Theorem H must begin by replacing the present abstract-level evidence with the complete primary theorem and hypotheses.
