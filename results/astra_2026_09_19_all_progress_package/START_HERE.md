# SR-Foxy — one complete recovered-work package

**Start with [FULL_PROGRESS.md](FULL_PROGRESS.md).** It gives the actual results,
what was checked again, what remains open, source attribution and exact limits.
No Slice–Ribbon counterexample is established.

## Contents

- `SR-Foxy/`: all 2,282 tracked files at commit
  `8481d993ee7763c17a49637112a77673f91c5cb7`, verified byte-for-byte.
- `source_export/`: original source tarball, 311-commit reachable Git history
  bundle, source manifest, export checksums and commit log.
- `original_archives/`: recovered original research delivery ZIPs, intact.
- `action_checkpoints/`: two completed common-upper search segments, database,
  controls, runner source, preflight and exact recorded environment.
- `verification/`: integrity reports and four freshly executed certificate replays.
- `RUNBOOK.md`: reproducible checks and safe continuation without a new branch.
- `REPORT_INDEX.md` and `CODE_INDEX.md`: navigation for all reports/code.
- `packaging_code/`: this delivery's assembly/recovery/export helpers.
- `publication_payload/` and `PUBLICATION.json`: exact copies and receipts for
  the export workflow and handoff README added directly to existing main.
- `PROVENANCE.json` and `PACKAGE_MANIFEST.json`: scope and file integrity.

## Verify first

From this extracted directory:

```sh
python3 VERIFY_PACKAGE.py
```

This is read-only. It checks every manifest byte count and SHA-256, exact source
blob hashes, and the source Git tree. It does not claim to prove the mathematics.
Run experiments in fresh copies, because some checkers overwrite their own
result JSON files. The included `RUNBOOK.md` gives commands.

## Branch and publication safety

No new remote branch was created. The source snapshot is read-only archival
material, not an instruction to replace your working checkout. Do not copy its
`.github/` or historical `START.json` wholesale into live main: existing path-based
workflows can run when those files change. Do not run an old `publish_main.py`
without reviewing it. Do not use force-push or an automatic blanket `git add .`.

The new export workflow was committed directly to existing main and completed;
it exported data only, without running a new mathematical search. The research
snapshot intentionally remains pinned to the revision before that packaging-only
commit. A ZIP cannot include future search output or uncommitted files on another
machine. The previous `53f800f` backup is superseded by this exact newer source
and history, rather than presented again as current.
