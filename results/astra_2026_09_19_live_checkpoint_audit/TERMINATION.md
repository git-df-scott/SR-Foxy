# Terminal update: cancellation and a malformed cancellation checkpoint

19 September 2026. **No counterexample established; seven hours did not complete.** This operational addendum does not change the finite endpoint exclusions proved for the first two intact checkpoints in README.md.

## Actual run status

GitHub run `35455048082`, attempt 1, is `completed/cancelled`. Phase-one job `105928864600` completed as cancelled at **17:43:15 UTC (11:43:15 a.m. America/Edmonton)**. Common-upper segments 1 and 2 succeeded. Segment 3 was cancelled, segments 4-7 were skipped, and phase two never executed a computation step.

Primary records read through the authorized GitHub connector:

- https://api.github.com/repos/git-df-scott/SR-Foxy/actions/runs/35455048082
- https://api.github.com/repos/git-df-scott/SR-Foxy/actions/runs/35455048082/jobs?per_page=10
- Decoded logs of job `105928864600`.
- Run-artifact listing and downloaded artifact `10589621369`.

The log contains normal search heartbeats through **17:42:41.8436883 UTC**, then `The operation was canceled.` at **17:43:10.8906495 UTC**. It does not identify the cancellation's initiator or reason. The run's actor/triggering_actor identifies the launch context, not who cancelled it. There is no mathematical-control failure or potential-counterexample announcement in the retrieved log.

## Evidence preserved, and the failure found

The cancellation uploader successfully replaced the previous GitHub artifact with `10589621369`, size **25,617,704 bytes**, SHA256:

`cf4f075c1a66df3e1d1ae33b6dd717a70e49a735026bee943eb0cdb7b9d570ea`

The downloaded ZIP matches that hash and passes ZIP CRC checks. Its `evidence.sqlite`, however, fails a read-only `PRAGMA integrity_check` with **`database disk image is malformed`**. Reading the attempts-table count also fails. Some other reads, including the runs table and a nodes count, succeed; this does NOT make the database an accepted complete checkpoint.

The database SHA256 is `2be2074398922ba1e3599e5bf9368409d8224e6b550289ae86137dbe6c4db032`. It was not repaired or rewritten. The raw damaged artifact and read-only diagnostics are preserved in the downloadable evidence.

The log shows the cancellation upload beginning before the orphan Python process was terminated during cleanup. A non-atomic copy during cancellation is a possible explanation for the malformed database, not a uniquely established cause. The final snapshot cannot be called failure-safe merely because its upload succeeded.

Crucially, both earlier ZIPs were already downloaded before they were replaced remotely. Their SQLite files still pass integrity checks. The complete **21,067-node, 167,163-attempt** first-hour snapshot and its exact endpoint audit are therefore preserved and remain usable.

## Measured runtime, without inflating completion

The two completed segments record **3600.021043032 search-wall seconds** and **3579.326956595 CPU seconds**.

The third segment's last heartbeat records another **781.7204441629997 search-wall seconds**, with **777.376774861 CPU seconds** in its run row. The cumulative last-heartbeat totals are therefore **4381.7414871949995 wall seconds (1 h 13 min 1.741 s)** and **4356.703731456 CPU seconds**. These are recorded progress through the last heartbeat, not an exact final runtime for the interrupted segment.

That heartbeat reports cumulative **201,277 attempts**, including **25,528 NEW_ENDPOINT**, **175,572 DUPLICATE_ENDPOINT**, and **177 NO_SAMPLED_BAND** outcomes. These are heartbeat counters, not a verified final reconstruction from the damaged attempts table. More computation occurred before cancellation, but its exact final counts and complete move evidence have not been validated. The first-hour complete audit must not be extended to those additional endpoints.

`RUN.json` still says `RUNNING` because the graceful finalizer did not publish a terminal result. Its `measured_completed_segment_seconds` field includes the unfinished third row; the field name must not be interpreted as completed-segment runtime. Neither `FINAL.json`, `FAILURE.json`, nor `POTENTIAL_COUNTEREXAMPLE.json` is present in the terminal archive. The authoritative terminal state is GitHub's cancelled run, not the stale heartbeat status.

The third segment had bounds of four crossed edges and eight absolute half twists, but it is incomplete. Phase two's absence is uncomputed, not a negative result. Seven-hour completion is false.

## Actions taken

No cancellation, restart, new workflow execution, or scientific-input modification was performed in this audit session. The terminal result-watch was disabled as previously requested after reporting the cancellation, to avoid repeated terminal notifications. No access token from chat was used. This addendum and the earlier compact verifier are additive files on `main`; large checkpoint archives remain in the downloadable evidence rather than being represented as pushed repository data.
