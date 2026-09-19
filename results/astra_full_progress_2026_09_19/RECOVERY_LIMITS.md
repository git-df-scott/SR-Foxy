# Interrupted checkpoint: what is and is not recovered

The run was cancelled at Scott's explicit request. This is an operational interruption, not a mathematical control failure or a counterexample nomination.

## Preserved originals

- Artifact **10589240719**: checkpoint after two completed segments, SHA-256 `41b015d6114e936a4514573042377e01a3aefa74caa4a89b7479ffd7ed26d0cc`. Its SQLite database passes integrity checking.
- Artifact **10589621369**: cancellation-time checkpoint, SHA-256 `cf4f075c1a66df3e1d1ae33b6dd717a70e49a735026bee943eb0cdb7b9d570ea`. The ZIP CRC passes, but the SQLite database produces `database disk image is malformed`.

Both ZIPs are copied unchanged under `search_run/original_artifacts/`. The recovered database is a third, new file, never a replacement for these originals.

## Conservative salvage

`search_run/recovered_partial/recover_readable_prefix.py` reads the damaged database and copies the readable table prefixes to a new database. Node payloads are decompressed and parsed as JSON. The script checks the recovered data against the intact completed checkpoint. It neither fabricates missing records nor claims that unreadable tails are empty.

The resulting `readable_partial.sqlite` has 25,669 readable node records, 31,235 stored attempt records, and three run records. All 21,067 stable node records, all 25,649 stable stored attempt records, and both stable run records are present unchanged. There are no missing parents among recovered nodes and no detected node-depth inconsistencies. The node and attempt reads both terminated on malformed data, so neither is known complete.

Attempt row 31234 has a child reference outside the recovered node set. It remains preserved and flagged. The recovered database is structurally valid SQLite; this does not erase that semantic gap. It must not silently be treated as a pristine resume checkpoint.

The original database's index suggested additional rows, but corrupt indices/tables do not establish an exact number of lost records. The missing tail and the exact final attempt counter remain UNKNOWN.

No full mathematical movie replay was run during packaging. The recovery verifies storage structure, payload readability, and preservation of stable rows, not independent topology. A mathematical use of a recovered movie still needs its full parent-chain replay and any required independent verification.

## Why the cancellation-time upload is suspect

The downloaded job log places cancellation of the shell step at 17:43:10 UTC, the always-upload action immediately afterward, and termination of the orphan Python process only during job cleanup at 17:43:13 UTC. That ordering is consistent with copying a database while its writer was still alive. It is a plausible cause of the malformed snapshot, not a proved diagnosis of the exact damaged page or transaction.

A future implementation should stop and join the producer before exporting a consistent SQLite backup, retain the last known-good checkpoint until validation succeeds, and test actual cancellation behavior. Those are recorded repair requirements, not changes applied to the scientific runner in this pause task.

## Stale run labels

The interrupted `RUN.json` still says `RUNNING` because its last heartbeat predates the cancellation. GitHub's actual run metadata is terminal `completed / cancelled`. No `FINAL.json` or `POTENTIAL_COUNTEREXAMPLE.json` was present in the captured search evidence. No seven-hour result is claimed.

## Earlier session source coverage

The 15 earlier conversation artifacts are preserved in `previous_session/sr_foxy_session/`. Several producer scripts named by their report were not found among those files, the inspected source snapshot, or the exact-name Library results. The missing originals have not been guessed or regenerated. Existing historical packages are included as recovered, not represented as covering every unsaved file from every prior runtime.
