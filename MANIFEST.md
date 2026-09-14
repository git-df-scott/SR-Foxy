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

## Added 2026-09-14 (fold of PRs #2, #3, #4 into `main`)

| artifact | what it claims | evidence level | how to verify | unresolved assumptions |
|---|---|---|---|---|
| `research/18_r0_rbg_pair_first_search.md` | first ribbon search on the unmined r=0 super-special pair K(0,0,0,-1,2,1); frontier grows 13 → 60 from one band to two | executed search with a replayed calibration | rerun `scripts/rbg_r0_search.py` against the stored PD sha256 | coverage of the stated boxes only; neither knot is known slice, so a negative carries no information |
| `research/21_branched_double_covers.md` | Σ₂(K_0)=L(13,5), Σ₂(K_1) has non-cyclic π₁, so the Abe-Tagami members are separated; d(L(13,5)) computed | exact low-index subgroup enumeration with four controls | rerun `scripts/branched_double_cover_gate.py` and `scripts/lens_d_invariants.py` | §3's d-invariant claim is **offered for a second reader, not asserted**; separation is not a concordance obstruction |
| `research/22_where_a_counterexample_can_come_from.md` | route B can only succeed by refuting "every slice knot is homotopy-ribbon"; CAMPAIGN_PLAN WS5 is vacuous as written | citation chain plus one elementary implication | check Miyazaki Thm 5.5 hypotheses and Eisermann Lemma 1 / Remark 3.6 | §3.1 is a three-line argument that should be checked before WS5 is struck; not struck here |
| `research/23_prefix_annulus_lemma_audit.md` | audit of the connected planar prefix lemma, plus a retracted claim about the J25533 survivors | proof reading plus a corrected computation with a positive control | rerun `scripts/alexander_rank_screen.py`, which refuses to report if its controls fail | **§5 is stale**: the rank-invariance citation it calls missing is in `research/19`. See HANDOFF §3 |
| `research/24_why_route_b_is_circular.md` | every satellite route to a counterexample is circular; Teichner is the unique non-circular constructive lane; one untried r=0 crossing | strategy synthesis over the ledger and executed runs | check each ledger row cited and the cost table against `results/teichner_*` | §4 is a proposal with an unquantified prior; not a theorem that the lane is non-empty |
| `results/teichner_D01_8_8_summary.json`, `..._frontier.json.gz` | D_{0,1} # 8_8 complete at 7.96 h, no certificate, 10,023-link frontier preserved | executed search, partner ribbonness verified | replay any frontier triple `[starting PD, band descriptor, endpoint]` | coverage of that box only; says nothing about whether D_{0,1} is slice |
| `results/teichner_lane_size_floor.json` | D_{0,1} does not simplify below 25 crossings over 120 seeds, K_1 below 19 over 400 | negative search | rerun with more seeds | a negative search result, **not** a proof of crossing number |
| `results/teichner_mirror_*.json` | both chiralities of seven Teichner partners swept at band lengths 4, 6, 8; `certified_slice` false | executed bounded search | rerun `scripts/teichner_mirror_partners.py` | a timed-out case is UNKNOWN, never a negative; the `cap420` file is an interrupted attempt, not coverage |
| `results/eisermann_ribbon_link_gate.json` | Eisermann's ribbon-link tests reproduce on three unlinks and fail maximally on six non-ribbon controls | executed, primary source re-read 14 Sep 2026 | rerun `scripts/eisermann_ribbon_link_gate.py`; `controls_pass` must be true | **controls only**; no slice link is tested, because GST L_{3,1} is not in this repository |
| `results/two_fission_J149_sharded/` | four terminated shards of the J149 reverse search; every endpoint is the K0 positive control | executed, hand-stopped before its cap | read the per-shard counts in `README.md` | every shard has `complete: false`; partial coverage, and the filters are blind to the K0/K1 distinction by `research/11` |
| `graph-reconstruction/` | exact deck engine; deficit measured through n=9 and growing; Ivanov's family improves fraction while deficit diverges | exhaustive computation with nauty canonical forms | `python3 -c "import deck; print(deck.find_collisions(list(deck.geng(9))))"` → `{}` | unrelated to slice-ribbon; Ivanov's b is a *lower* bound, so quoted deficits are upper bounds on the true deficit |

### Note on numbering

`research/23` and `research/24` were published as `research/19` and
`research/20` on `claude/counterexample-search-ungpe2` and renumbered on fold,
because `main` had independently used those numbers. `research/09` is duplicated
for unrelated historical reasons. The next free number is 25.

## Global unresolved assumptions

1. “Current status” is frozen at the cutoff and can change after 2026-08-30.
2. No silence-of-literature inference is upgraded to a proof that a problem is open.
3. A preprint theorem is cited as a theorem in that version, not as peer-reviewed fact.
4. `DG` nomenclature follows SnapPy/Hoste–Thistlethwaite style exactly as printed in [S01,S03]: `18nh00000601`.
5. Any future use of Turaev’s Theorem H must begin by replacing the present abstract-level evidence with the complete primary theorem and hypotheses.
6. As of the 2026-09-14 fold, every branch is merged into `main` and there are no unmerged branches. Session records written on a branch (`SESSION_2026-09-14.md`, and the per-session sections of `HANDOFF.md`) are true about their own session only; `HANDOFF.md`'s top section is the only one written with sight of the whole board.
