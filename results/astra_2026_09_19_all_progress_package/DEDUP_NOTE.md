# What was left out of this package, and why

The source delivery was `SR.zip` (148MB, 2358 files, `SR_Foxy_All_Progress_2026-09-19/`).
Everything not committed here was checked byte-for-byte against content
already reachable from this repository's git history or from the
`checkpoint-evidence-2026-09-19` release, and found identical — committing
it again would duplicate, not add, evidence. Nothing was dropped because it
seemed unimportant; each exclusion below is verified, not assumed.

## `SR-Foxy/` (2,282 files, ~170MB)

A full working-tree mirror of this repository. Its git tree hash is
`188559fee43401a811824256433aec3a79109ea4`, which is exactly the tree of
commit `8481d993ee7763c17a49637112a77673f91c5cb7` — already an ancestor of
`main` (verified with `git merge-base --is-ancestor`). Anyone can recover it
with `git checkout 8481d993ee7763c17a49637112a77673f91c5cb7`.

## `source_export/SR-Foxy-source-8481d99.tar.gz` and `SR-Foxy-history-8481d99.bundle` (~79.5MB)

A tarball and bundle export of the same commit `8481d99`, i.e. the same
content as above, already in `main`'s history. Redundant with the repository
itself. `source_export/BUNDLE_VERIFICATION.txt`, `COMMIT_HISTORY.tsv`,
`SHA256SUMS.json`, and `SOURCE_MANIFEST.json` — the small metadata *about*
that export — are kept here.

## `action_checkpoints/astra_seven_hour_10589240719/` (~31MB)

Byte-identical to `checkpoint-2.zip` already uploaded to the
`checkpoint-evidence-2026-09-19` release
(https://github.com/git-df-scott/SR-Foxy/releases/tag/checkpoint-evidence-2026-09-19).
Confirmed: `evidence.sqlite` in both has sha256
`8003e6108f89b30028735c47381f3dce69b80ed478934327b071e1b13e6c8888`, and the
file list (`CONTROLS.json`, `RUN.json`, `RUN-common_upper-*.json`,
`environment.txt`, `smoke/`, `source/`) matches exactly.

## `publication_payload/`

- `results/astra_2026_09_19_complete_handoff/README.md` — byte-identical
  (`diff` clean) to the file already committed at that same path in `main`.
- `.github/workflows/astra-full-handoff-export-20260919.yml` — a workflow
  file with the same name already present in `main`'s `.github/workflows/`.

## Kept in full

Everything else from the zip: `original_archives/` (the four raw input
zips), `packaging_code/` (12 scripts), `previous_delivery/` (4 files),
`verification/` (21 replay logs/results), and the top-level package
metadata (`CODE_INDEX.md`, `FULL_PROGRESS.md`, `PACKAGE_CONTENTS.tsv`,
`PACKAGE_MANIFEST.json`, `PROVENANCE.json`, `PUBLICATION.json`,
`REPORT_INDEX.md`, `RUNBOOK.md`, `START_HERE.md`, `VERIFY_PACKAGE.py`).
