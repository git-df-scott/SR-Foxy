# Large checkpoint databases — stored as a release, not a git blob

`checkpoint-1.zip`, `checkpoint-2.zip`, and `terminal-checkpoint.zip` are the
original downloaded GitHub artifact bytes for run 35455048082 (SQLite
databases plus RUN summaries and deployed code), ~57MB combined. Per this
bundle's own `README.md` ("The two large checkpoint databases ... are
supplied in this bundle rather than committed to the repository"), they are
attached to this repo as release assets instead of being committed as git
blobs, so nothing from the original evidence zip is missing from the repo's
reach while git history stays free of large binaries.

Release: https://github.com/git-df-scott/SR-Foxy/releases/tag/checkpoint-evidence-2026-09-19

| file | sha256 | bytes |
|---|---|---|
| checkpoint-1.zip | `ed95f67285a105410eaefd8e0354b1343af90831969a69e802efa5b50dab334c` | 10181039 |
| checkpoint-2.zip | `41b015d6114e936a4514573042377e01a3aefa74caa4a89b7479ffd7ed26d0cc` | 20919987 |
| terminal-checkpoint.zip | `cf4f075c1a66df3e1d1ae33b6dd717a70e49a735026bee943eb0cdb7b9d570ea` | 25617704 |

These match the SHA-256 values recorded in `MANIFEST.json` for the ZIP
member checksums shipped with the original evidence archive
`SR_Foxy_search_evidence_and_audit_2026-09-19.zip`, verified locally before
upload. Everything else in that archive (audit/, publication/, terminal/,
README.md, MANIFEST.json) is committed in full alongside this file.
