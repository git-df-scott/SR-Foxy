# SR-Foxy — full recovered progress archive

**Paused at Scott's request on 19 September 2026. No Slice–Ribbon counterexample has been established.**

This is a preservation package, not a new research result. It contains a verified complete repository snapshot, captured Git history, both saved search checkpoints, conservatively salvaged partial records, the earlier files delivered in this conversation, and recovered related research packages. Original scientific files are not rewritten.

## 1. What is stopped

GitHub Actions search run **35455048082**, launched from **042a7dfc6fe61967902e1c4f7174af5f6342862c**, is **completed / cancelled**. GitHub recorded the terminal update at **2026-09-19 17:43:16 UTC**. The first two common-upper segments completed; segment 3 was interrupted. The main stabilized-disk phase did not run. The two short preflight smoke tests are separate.

The result-watch automation **6aae1d60002c81918a2f4657a1c867c6** was disabled. No search was restarted to prepare this archive. A small GitHub workflow performed the requested cancellation and then a source/history/log export; neither operation is a mathematical search.

## 2. Readable directory map

| Location | Contents |
|---|---|
| `repository/SR-Foxy/` | All **2,287 tracked files**, unchanged, from pinned commit **43b71f03a9332af96d96ed1d53370233a1567768**: code, reports, input diagrams, results, tests, figures, previous committed archives, and workflows. |
| `repository/SR-Foxy-history.bundle` | Exported Git objects and ancestry, including the launch commit, the pinned snapshot, and later captured commit **9bc873b6921b42c3f79e73046a3a4f617b66d001**. |
| `repository/provenance/` | Per-file snapshot hashes, Git refs/log, source verification, local Git-object verification, and original export checksums. |
| `repository/later_captured_commit/` | The single termination memo from the later captured commit, kept outside the unchanged snapshot. |
| `search_run/original_artifacts/` | Byte-for-byte preflight ZIP, intact two-segment checkpoint ZIP, and raw interrupted-checkpoint ZIP. |
| `search_run/completed_checkpoint/` | Expanded, intact checkpoint with source, controls, smoke evidence, run summaries, and usable `evidence.sqlite`. |
| `search_run/interrupted_checkpoint_metadata/` | Unmodified heartbeat and control JSONs from the interrupted checkpoint. The `RUNNING` label is stale, not current run status. |
| `search_run/recovered_partial/` | New `readable_partial.sqlite`, conservative salvage report, and the recovery script. This is not a complete recovery. |
| `search_run/logs_and_metadata/` | Downloaded GitHub run logs and actual run/job/artifact metadata. |
| `previous_session/sr_foxy_session/` | All **15 earlier files actually preserved in this conversation**, including the multiedge-band code, recorded searches, calibration evidence, GST identification, Jones-pattern results, Floer results, and report. |
| `earlier_saved_packages/` | Original combined construction package, GST research package, historical verified repository backup, historical sidecars, and readable expansions of the two smaller research packages. |
| `PAUSE_STATUS.json`, `RECOVERY_LIMITS.md`, `HANDOFF.md` | Current state, measured totals, limitations, and continuation cautions. |
| `MANIFEST.json`, `VERIFY_ARCHIVE.py` | Whole-package file hashes and a read-only standard-library verifier. |

The source snapshot is deliberately pinned. It is not a claim that `main` cannot have advanced during export. The bundle also captured the later termination memo; it is separately identified rather than silently mixed into the frozen tree.

## 3. Actual computation preserved — not seven hours

| Recorded computation | Search wall time | Process CPU time | Attempt counter | Status |
|---|---:|---:|---:|---|
| Common-upper segment 1 | 1,800.016701387 s | 1,789.511606257 s | 88,855 | Completed, no nomination |
| Common-upper segment 2 | 1,800.004341645 s | 1,789.815350338 s | 78,308 | Completed, no nomination |
| Common-upper segment 3, last saved heartbeat only | 781.720444163 s | 777.376774861 s | 34,114 | Interrupted; final accounting unavailable |

**Completed search budget: 3,600.021043032 seconds, about one hour.** Those two segments account for **167,163 attempts**. Including the last recorded partial heartbeat gives **4,381.741487195 seconds**, or **1 hour 13 minutes 1.74 seconds**, and **201,277 attempts**. These latter numbers are the documented accounting through that heartbeat, not exact cancellation-time totals. Additional readable node rows postdate the heartbeat.

Queueing, dependency installation, preflight, smoke tests, archive export, and verification are excluded. The requested seven hours were not completed. The original field named `measured_completed_segment_seconds` in the interrupted JSON includes the running segment: its name must not be used as proof of completed time.

The executed common-upper bounds were at most two birth/fusion steps, crossing cap 72, and 48 post-band Reidemeister-III trials. Segments 1, 2, and the partial segment 3 used crossed-edge bounds 2, 3, 4 and absolute half-twist bounds 4, 6, 8 respectively. The randomized parent selection used roots or a pool of up to 384 small eligible recorded diagrams. This was not exhaustive enumeration. The source and per-attempt parameters contain the exact implementation.

The reported attempt counters include duplicate endpoints and unsuccessful band sampling; they are not counts of distinct knots or independent isotopy classes. The `attempts` table samples many duplicate/rejection rows, so its row count is not the aggregate attempt count.

## 4. Important checkpoint integrity issue

The latest uploaded ZIP is byte-for-byte intact, but its **SQLite database is malformed**. The preceding completed checkpoint was downloaded before cancellation and passes `PRAGMA integrity_check`.

The read-only recovery recovered **25,669 node records**, including every one of the **21,067 nodes** in the intact checkpoint unchanged and **4,602 additional readable nodes**. It also recovered **31,235 stored attempt rows** and three run rows. The new recovery database passes SQLite integrity checking and retains all node parents. Attempt row **31234** refers to a child node that could not be recovered; this is explicitly recorded.

Original checkpoints have not been patched or replaced. The damaged raw bytes remain available for better recovery. Read `RECOVERY_LIMITS.md` before using the partial database. Recovery and hash checks do not independently prove the mathematical correctness of any saved movie.

## 5. Historical claims and unrecovered material

The old reports remain historical reports. Their preservation does not upgrade a bounded negative search into a theorem or revalidate every claim. Later errata in the repository can supersede older handoffs.

The earlier session report names additional producer scripts, including `bing_tree_probe.py`, `check_bing_symbolic.py`, and `ribbon_pattern_probe.py`. These exact files were **not recovered** among the current mounted session files or the inspected repository snapshot; exact-name Library searches also returned no matching files. They have not been recreated and presented as originals. The saved report and output JSONs are included. There is no guarantee about unpersisted files in a reclaimed runtime or content never supplied as an artifact.

This package is not a verbatim chat transcript. It is a complete copy of the specified repository snapshot plus all research artifacts recovered for this delivery, with the interrupted-data and earlier-source limitations stated here.

## 6. Verify without starting any computation

From this directory run:

```sh
python3 VERIFY_ARCHIVE.py
```

The verifier reads file bytes and checks their sizes and SHA-256 values. It does not import the knot software, connect to GitHub, launch a search, alter the database, or write to the repository. The exact Git blob identities for the source snapshot are also recorded in `repository/provenance/SNAPSHOT.json`.

This is not a universal preinstalled topology environment. The search's pinned requirements and actual environment listing are preserved. Historical scripts may require different dependencies. Do not overwrite a newer existing clone with this snapshot.

## 7. GitHub changes and provenance

This archive task committed only the narrow pause/export workflow, first at **8a618293173dbeefcfc110c9c980f459a31d71ef**, then at **43b71f03a9332af96d96ed1d53370233a1567768**. Existing scientific reports were not edited by those two changes. A later termination memo was captured separately in the bundle.

The repository source and workflow code are already committed. Search evidence normally lives in Actions artifacts, not in the tracked source; this ZIP preserves those evidence bytes locally. The completed-checkpoint artifact was later overwritten on GitHub, so retaining this downloaded copy matters. The final combined ZIP itself was created for download, not automatically committed to `main`.

No access token from chat was used. See `ARTIFACT_PROVENANCE.json` for artifact IDs, sizes, and SHA-256 checks.
