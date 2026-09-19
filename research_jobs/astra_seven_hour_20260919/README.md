# Astra seven-hour movie search — 19 September 2026

This is an executable, bounded search, not a claimed counterexample and not an exhaustive treatment of Slice–Ribbon. Scott explicitly authorized its initial seven-hour run and downloadable evidence. The workflow has read-only repository permissions and never changes scientific reports or restarts a search automatically.

## Execution

The workflow is `.github/workflows/astra-seven-hour-movie-search-20260919.yml`, named **Astra seven-hour movie search 2026-09-19**. A separate commit creating `START.json` launches its first execution. Ordinary repository edits do not trigger it. Manual dispatch remains available for a separately authorized future run.

Preflight checks the frozen diagram fields against the checked-out repository, installs pinned packages, recalculates the input fiberedness/Alexander/Jones checks, reproduces ribbon movies for the stevedore and its mirror, rejects corrupted death ledgers, tests local births and sampled bands, and runs both modes briefly. Preflight and installation are NOT included in the requested seven-hour search budget.

The two sequential computation jobs each contain seven 1,800-second search segments. The total requested search wall time is 25,200 seconds. Each job stays below GitHub's six-hour job limit. Actual wall and CPU times, interruptions, parameter bounds, and counters are written by the running processes. Do not infer completion from the workflow title.

1. **Common-upper movies:** the stored Abe–Tagami pair and K7a2/K10n4. Each endpoint is reached using at most two explicit split-unknot births and fusion bands, interspersed with recorded elementary Reidemeister moves. Opposite sides are compared with a mirror-sensitive combinatorial diagram signature.
2. **Stabilized disk movies:** D01 and the K7a2/K10n4 difference, each connected-summed with the stevedore or its mirror. Search at most five fission bands, with explicitly counted deaths of split trivial circles. Nonzero pairwise linking and nonsquare component determinants reject individual branches, not the original target.

The segment bounds on crossed diagram edges are 2,3,4,5,6,2,3; the corresponding absolute half-twist bounds are 4,6,8,6,8,10,10. The crossing cap is 72. Parent selection is randomized with a bias toward the 384 smallest eligible stored diagrams. Each attempted band samples an edge-labelled simple augmented dual-face path, retaining the actual parallel edge choice. This is not uniform sampling and not exhaustive enumeration. Diagram reversal is allowed in signature comparison; mirror reflection is not. Final orientation and same-knot identification still require audit.

## Evidence

The cumulative `astra-seven-hour-checkpoint` artifact is replaced after each successful or failed computation segment. Each replacement includes all earlier database evidence, so superseded uploads need not consume cumulative storage. Phase 2 downloads the final Phase 1 checkpoint before continuing. The smaller `astra-seven-hour-preflight` artifact is retained separately. Artifacts are retained for seven days.

- `CONTROLS.json`: control results, input hypotheses, version and source hashes, and the two positive-control ribbon movies.
- `RUN.json`, `RUN-<phase>-<segment>.json`: exact counters and measured computation times. `FINAL.json` is written only after both phases complete.
- `evidence.sqlite`: retained endpoints, compressed move histories, parent chains, run ledgers, and selected attempt records. Every new endpoint, timeout, error and nomination has an attempt row. Other outcomes are sampled at one row per 32 attempts; their exact TOTAL counters remain in the run summaries. Do not equate the attempts-table row count with the total number of attempts.
- `source/`: the actual checked-out job source, input diagrams, requirements, and launch marker.
- `smoke/`: short preflight runs, explicitly excluded from the seven-hour runtime total.
- `POTENTIAL_COUNTEREXAMPLE.json`, if produced: a nomination requiring independent audit, with saved movie chains. Exit code 42 stops further computation. This is NOT an established counterexample.
- `FAILURE.json`, if produced: an interruption or mathematical/software control failure. These are not negative mathematical results.

To inspect a node, use `runner.path_to(sqlite_connection, node_id)`. It expands its complete parent chain and replays it through the pinned native implementation. This native replay is not an independent implementation or a formal proof. A proposed hit additionally requires independent elementary-movie verification, exact endpoint identification excluding mirror-only matches, and the nonribbon hypotheses for the same actual knot. A stabilized-disk hit also requires the partner's ribbon certificate. The input check does not establish the historical paper-figure correspondence of an archived diagram.

The local pre-deployment tests passed the mathematical controls and both bounded search modes. Twenty saved complete parent chains were replayed and the SQLite integrity check passed. These tests are calibration, not a Slice–Ribbon result.

## Local commands

```sh
python -m pip install -r research_jobs/astra_seven_hour_20260919/requirements.txt
python research_jobs/astra_seven_hour_20260919/runner.py --out evidence --controls
python research_jobs/astra_seven_hour_20260919/runner.py --out evidence --phase common_upper --segment 1 --seconds 1800
```

Do not automatically rerun a failed expensive job. Inspect the actual log and checkpoint first. A final report must distinguish a nomination, a verified result, a bounded negative search, and UNKNOWN computations, and must report measured rather than requested runtime.
