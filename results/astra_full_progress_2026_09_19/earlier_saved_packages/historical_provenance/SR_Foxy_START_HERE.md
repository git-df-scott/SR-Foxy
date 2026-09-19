# SR-Foxy — verified historical source backup

## Use the current version for continued research

The `SR-Foxy/` directory in this package is a complete, unmodified source snapshot
of commit **53f800feb98faf177b4cb89c5204bb0fcbb4fa3b**, committed at **2026-09-19 02:32:23 UTC**.
It is **not the latest main**.

At the final repository inspection used for this package, `main` was
**b370fc0064bf2731a55443f3c4636a7316e311bf** (2026-09-19 17:25:24 UTC).
It advanced during packaging. The earlier main `042a7df` was already 54 commits
ahead of the backup, with 50 changed paths. For all committed code, data, reports,
and workflows at the final observed main, use GitHub's full pinned source ZIP:

https://github.com/git-df-scott/SR-Foxy/archive/b370fc0064bf2731a55443f3c4636a7316e311bf.zip

This ZIP link is a GitHub-generated export, not an archive that was downloaded
and verified in the local runtime. Direct GitHub archive retrieval was unavailable
here. The local backup was recovered through the existing authorized GitHub
Actions artifact download instead. No new workflow was started for this delivery.

## What is preserved locally

Every one of the **2,034 tracked files** at the backup commit is included under
`SR-Foxy/`, including source code, tests, input data, reports, saved results,
figures, and previously committed archives. Contents have not been rewritten.
The original Git file modes are recorded in `SOURCE_MANIFEST.json` and are also
stored in the ZIP metadata. There are no symlinks in this source snapshot.

The reconstructed Git root tree is:

`9b221b37ceba2963c6579ee9f53282b3999be35b`

It exactly matches the tree named by GitHub for the backup commit. This is a
whole-tree integrity check, not just a filename count. `SOURCE_MANIFEST.json`
also gives SHA-256, Git blob SHA-1, size, and recorded mode for each source file.
The package-level verification files sit outside `SR-Foxy/`, so the source tree
itself remains byte-for-byte unchanged.

## Verify and read the backup

After extracting the ZIP, run:

```sh
python3 VERIFY_BACKUP.py
```

This verifier is read-only. It checks every source file, missing and extra paths,
and the manifest's reconstructed Git tree. It uses only Python's standard library.
Filesystem executable bits may differ after extraction on some platforms; the
manifest retains the canonical Git modes.

For orientation, start with `SR-Foxy/README.md` and `SR-Foxy/TOOLING.md`, then use
the per-result `README.md` and replay scripts in the relevant `results/` directory.
Historical handoffs and statuses are snapshots: prefer a later explicit correction
when one exists. Dependencies and runtime needs vary by workstream; this package
is source and saved research data, not a universal preinstalled environment.

## Checks performed for this delivery

- The downloaded Actions ZIP matched its published SHA-256 and passed its ZIP
  integrity check.
- The enclosed source tarball matched its supplied SHA-256.
- All 2,034 source files reproduce the backup commit's exact Git root tree.
- All **306 Python source files** passed Python syntax parsing.
- **729 of 732 JSON files** parsed. The remaining three are empty historical
  output files, listed in `BASELINE_VERIFICATION.json`. They were preserved rather
  than filled with invented results.

These are preservation and static-readability checks. They do not establish
runtime correctness of every script, correctness of the mathematics, or a
Slice–Ribbon counterexample. No complete research test suite or search was run
for this packaging task.

## Continue safely on main

To work with the current repository, use your existing clone rather than copying
this historical source tree over a newer checkout:

```sh
git status --short
git branch --show-current
```

When the working tree is clean and the branch is already `main`, update it with:

```sh
git pull --ff-only origin main
```

Do not discard local changes to make that command run. Resolve an unclean tree
or divergent history deliberately. Do not replace newer files with this backup.

There is no need to push the historical source again: it is already committed.
For genuinely new edits, review `git diff`, stage only the intended files, commit,
and use `git push origin main`. No force-push or new branch is needed.

## This chat's scope

The interrupted research attempt generated no new source code. Its subsequent
accountability/handoff report was checked at the newer pinned main under:

`results/astra_2026_09_19_1608_session_accountability/README.md`

The report was read at the earlier observed main `042a7df`; the final main
commit has that commit as a parent. The report is newer than this historical
snapshot and therefore is not inside
its unmodified source tree. It is available in the current-main ZIP linked above.

No unpublished research code was present in this runtime. The only new code in
this packaging task is `VERIFY_BACKUP.py`, supplied with this delivery. No
repository write, new branch, reset, force-push, or search launch was performed.

## Archive provenance

GitHub workflow run: `35416348435`
Artifact: `10576590507` (`sr-foxy-source-53f800f`)
Outer artifact SHA-256:
`d12881f06d6d21f586775aa5805fdec4cdfb32926ffff972448c489a26aa7828`
Source tarball SHA-256:
`f496b01315a0753bc105466666098951f8d193eb66965723ede792f57cf33be7`

The external GitHub links may require normal GitHub access. The preserved local
source and the standard-library integrity verifier work without network access.
