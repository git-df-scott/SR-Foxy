# Terminal status — read before the first-hour audit

**The GitHub run was cancelled, not completed for seven hours. No counterexample was established.**

Run 35455048082 stopped during common-upper segment 3. The first two segments completed. Phase two did not execute. The job was marked cancelled at 17:43:15 UTC on 19 September 2026 (11:43:15 a.m. Edmonton). The available records do not identify who cancelled it or why. No restart was performed.

Both original first-hour checkpoints are intact and preserved as checkpoint-1.zip and checkpoint-2.zip. Their exact finite audit is the subject of the report below: 21,067 stored states, 167,163 attempts, and 3600.021043032 seconds of completed search wall time.

terminal-checkpoint.zip is the exact cancellation artifact, including its DAMAGED SQLite file. Its ZIP hash and CRCs pass, but its database fails PRAGMA integrity_check. It is retained as evidence, not presented as a valid completed checkpoint. No repair was performed. The raw RUN heartbeat still says RUNNING and has no finalizer result; GitHub's cancelled state supersedes that stale status.

The last heartbeat records at least 4381.7414871949995 search-wall seconds (1 h 13 min 1.741 s) cumulatively, with 4356.703731456 CPU seconds. This is not the exact final duration of the cancelled segment. Its aggregate 201,277 attempts are heartbeat counters, not a validated final database total. The extra third-segment endpoints have not been covered by the first-hour all-endpoints exclusion.

See terminal/TERMINAL_STATUS.json, terminal/TERMINAL_INTEGRITY.json, and terminal/SELECTED_JOB_LOG.txt. The four initial audit files and a terminal addendum were pushed to main, ending with publication commit 9bc873b6921b42c3f79e73046a3a4f617b66d001. The result-watch automation was disabled after the terminal report, as requested. No chat access token was used.

Published terminal addendum:
https://github.com/git-df-scott/SR-Foxy/blob/9bc873b6921b42c3f79e73046a3a4f617b66d001/results/astra_2026_09_19_live_checkpoint_audit/TERMINATION.md

---

# SR-Foxy live-checkpoint audit — 19 September 2026

No Slice–Ribbon counterexample was established. This bundle preserves the
first two checkpoints of run 35455048082 and the computations performed in
this continuation. The audited checkpoint closes at 17:29:36 UTC and records
3600.021043032 search-wall seconds, not seven hours.

For each target family, no left endpoint in that checkpoint is the same knot
as a right endpoint there. Full Jones polynomials, then HOMFLY-PT, then cyclic
and all degree-four cover homology spectra separate the saved endpoints.
This is a finite negative result, not an exhaustion of the search bounds and
not a nonconcordance theorem for the original input knots.

## Contents

- checkpoint-1.zip and checkpoint-2.zip are the ORIGINAL downloaded GitHub
  artifact bytes, including SQLite databases, RUN summaries and deployed code.
- audit/ contains the first-checkpoint analysis scripts and their outputs.
- audit/snapshot2/ contains the cumulative second-checkpoint analyses.
- publication/ contains the compact independent mod-5 witnesses/checker,
  the structured summary, and the exact publication commit list.
- MANIFEST.json lists SHA-256 hashes of all other ZIP members.

The detailed report is committed to main at:
https://github.com/git-df-scott/SR-Foxy/blob/0e358a27e2de1e5d6dcca58f8a8ffaff8fdd1785/results/astra_2026_09_19_live_checkpoint_audit/README.md

The four public repository files are an additive report and compact witnesses.
The two large checkpoint databases and the full postprocessing are supplied
in this bundle rather than committed to the repository.

## Independent fixed-witness replay (standard library only)

    python publication/verify_cyclic4.py

This independently computes Betti numbers 3,5,5,3 and rejects eight corrupted
witnesses. It verifies the four named diagrams, not every computation in this
bundle. For the integral Smith certificates and 20 corruption controls:

    python audit/check_cyclic_certificate.py audit/collisions/cyclic4_certificate_*.json

## Reproduce the exact full-checkpoint filters in a fresh directory

Use the pinned requirements in each original archive's source/requirements.txt.
The machine running this audit used the existing authorized wheelhouse when
network package installation was unavailable; wheels are not redistributed here.

For checkpoint 2, from the unzipped bundle root:

    mkdir replay2
    unzip checkpoint-2.zip -d replay2/checkpoint
    cp audit/snapshot2/*.py replay2/
    python replay2/jones_checkpoint_audit.py replay2/checkpoint --out replay2/jones
    python replay2/audit_jones_collisions.py
    python replay2/run_cyclic_audit.py
    python replay2/audit_full_covers.py

The HFK collision computation is additional evidence about the first checkpoint;
it is not required by the final second-checkpoint finite exclusion.

    mkdir replay1
    unzip checkpoint-1.zip -d replay1/checkpoint
    cp audit/*.py replay1/
    python replay1/jones_checkpoint_audit.py replay1/checkpoint --out replay1/jones
    python replay1/audit_jones_collisions.py
    python replay1/audit_hfk_collisions.py
    python replay1/run_cyclic_audit.py

These tools compute from the saved diagrams and do not restart a search.
JSONL producers normally refuse existing outputs; use fresh replay directories.
The full-cover postprocessor intentionally resumes its own completed node records.

## Verification boundaries

The hash, SQLite, parent/depth/death ledger checks pass. Two hundred complete
chains per checkpoint passed native replay. That replay shares Spherogram
with the producer and is not an independent proof of every saddle.

Both low-index cover enumerators agree on all 141 final-stage nodes, but share
SnapPy's triangulation and H1 implementation. The independent PD/integer checks
are explicitly scoped to their recorded diagrams. Numerical volumes are saved
only as exploratory observations and are not used in the exclusion pipeline.

Two local 60-second wrapper limits interrupted full-cover postprocessing.
Completed records were resumed; all 141 nodes eventually completed. The field
last_invocation_seconds is NOT total audit runtime. No GitHub search was
restarted. All requested seven-hour completion claims must come from later
actual RUN/FINAL records, not this snapshot.
