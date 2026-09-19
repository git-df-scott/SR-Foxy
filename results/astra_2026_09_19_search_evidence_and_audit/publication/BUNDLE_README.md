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
