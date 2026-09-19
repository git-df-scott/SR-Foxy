# Full saved progress — published and verified

The complete preserved contents of `SR_Foxy_Full_Progress_2026-09-19.zip` are now tracked in this directory on **main**, not merely in temporary Actions artifacts or unfinished transfer fragments.

Publication commit: **6e6153c55cb7d1581535f37f0fc3d6730f82c85b**.

Publication workflow **35471117227** completed successfully. It restored all **2,555 payload files / 388,797,483 bytes**, matched the exact original manifest digest, committed them, then read every payload back from the committed Git objects and verified that the publication commit was on the remote main branch. The two original metadata files were also preserved; the publication verification files and this entry point were added afterward.

Read [START_HERE.md](START_HERE.md) for the directory map and [HANDOFF.md](HANDOFF.md) for the saved research state. [PUBLICATION_RECEIPT.json](PUBLICATION_RECEIPT.json) records the successful push and verification. [MANIFEST.json](MANIFEST.json) preserves the original per-file SHA-256 manifest.

The package includes the pinned repository and Git history, earlier reports and source code, saved construction and GST packages, the intact completed checkpoint, the original damaged cancellation artifact, conservative partial recovery, logs and controls. In particular the usable first-hour database is `search_run/completed_checkpoint/evidence.sqlite`; the separately salvaged database is `search_run/recovered_partial/readable_partial.sqlite`.

## Limits retained, not erased

The research remains paused. No search was restarted for this publication, no new branch was created, and no chat access token was used. Existing mathematical reports outside this new preservation directory were not overwritten. No counterexample or seven-hour completion is claimed.

The raw cancellation-time SQLite file is still damaged; its exact original archive is preserved alongside the intact checkpoint and explicitly limited recovery. Read [RECOVERY_LIMITS.md](RECOVERY_LIMITS.md). Historical statements in the preserved handoff that the ZIP had not yet been committed describe its original delivery time; this publication receipt supersedes that publication status without rewriting the old reports. The archive's explicit limits on unrecovered, never-persisted producer scripts remain unchanged.

Run `python3 VERIFY_ARCHIVE.py` from this directory for a read-only hash check. Git preserves file bytes and executable bits, not every historical Unix permission bit; original permission metadata remains in the manifest and original nested archives.
