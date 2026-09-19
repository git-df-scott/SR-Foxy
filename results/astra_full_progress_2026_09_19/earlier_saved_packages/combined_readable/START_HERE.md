# SR-Foxy — combined saved research packages

Prepared 19 September 2026. This is an archival consolidation, not new research or a new counterexample claim.

## Start with the reports

- [Explicit genus-one construction: full report](03_explicit_genus_one/REPORT.md)
- [One-commutator result: full report](02_one_commutator/REPORT.md)
- [Initial sweep and construction audit](01_initial_audit/AUDIT.md)
- [Original research handoff](01_initial_audit/TONIGHT_HANDOFF.md)

## What is preserved

`01_initial_audit/` contains all 9 files from the initial audit/handoff ZIP.
`02_one_commutator/` contains all 27 files from the one-commutator ZIP, including its original manifest.
`03_explicit_genus_one/` contains all 92 files from the explicit genus-one ZIP, including its nested prior work, reports, source code, raw data, mesh, drawings, verification records, and recorded failures.

The three original ZIP files are also preserved byte-for-byte in `original_archives/`. All extracted member bytes are unchanged. There is intentional duplication so that every original package and its internal paths remain recoverable.

The genus-one ZIP alone contains the main genus-one report and the prior one-commutator report, but not the separate initial audit/handoff package. Its prior directory contains all 26 files listed in the old one-commutator manifest, but omits that old manifest itself. This combined archive restores the standalone original package as well.

`ARCHIVE_VERIFICATION.json` records the actual CRC, size and SHA-256 checks performed. `MANIFEST.json` records the byte count and SHA-256 of every other file in this combined archive.

## Scope — do not mistake this for a complete repository export

This archive consolidates the three saved research packages available as attachments in this conversation. It does not include the full GitHub repository or its history, later GitHub Actions outputs/checkpoints, a verbatim conversation transcript, or transient/unsaved runtime files. It is not a guarantee that every action mentioned anywhere in the conversation produced a saved artifact.

The reports retain their original dates and historical publication statements. Those statements are not current GitHub-status assertions. This packaging operation did not push or modify GitHub, change a branch, or rerun the mathematical experiments.

For the explicit surgery knot, the recorded work does not yet establish both a smooth slice disk in standard B4 and a global nonribbon proof. Read the qualifications in the original reports before extending any result.
