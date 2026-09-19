# Reproduction and continuation

## 1. Verify preserved bytes

In the root of the extracted delivery:

```sh
python3 VERIFY_PACKAGE.py
```

Python 3.10+ is sufficient for this packaging verifier. It needs no external
packages, network, credentials or GitHub account. A PASS means the recorded
package/source bytes match, not that all mathematical assertions are proved.

## 2. Replay the four independent certificate checkers

Use Node.js with BigInt support and ordinary Python 3. Do not use `python -O`
for the subgroup checker; it deliberately relies on enabled assertions.
Copy the research subdirectories into a scratch directory first. For example,
from the extracted delivery on macOS/Linux:

```sh
scratch=$(mktemp -d)
cp -R SR-Foxy/results/sr_foxy_combined_saved_work_2026_09_19/02_one_commutator "$scratch/one_commutator"
cp -R SR-Foxy/results/sr_foxy_combined_saved_work_2026_09_19/03_explicit_genus_one "$scratch/genus_one"
(cd "$scratch/one_commutator" && node check_independent.mjs)
(cd "$scratch/genus_one" && node check_exact_independent.mjs)
(cd "$scratch/genus_one" && python3 check_mesh_independent.py)
(cd "$scratch/genus_one" && python3 check_subgroup_independent.py)
```

These four commands were actually run during this delivery and passed.
Fresh logs are in `verification/replays/`. The standard-library mesh and subgroup
checks do not need SnapPy, Sage, Regina or a network connection.

## 3. Whitehead-stabilizer replay

The recorded environment pins SnapPy 3.3.2, Spherogram 2.4.1, Regina 7.4.1,
knot_floer_homology 1.2.2 and SymPy 1.14.0. Native wheels may be platform-specific.
The environment used for the recorded topology computations was Python 3.13.
These installation commands use the network; no dependency wheelhouse is included.

```sh
python3.13 -m venv /tmp/sr-foxy-replay-env
. /tmp/sr-foxy-replay-env/bin/activate
python -m pip install -r packaging_code/requirements-topology.txt
python SR-Foxy/results/astra_2026_09_19_infection_gate/replay.py --out /tmp/sr-foxy-whitehead-replay
```

The output directory must be absent or empty. This regenerates detailed band and
prefix ledgers; those files are not invented or inferred from summary counts.
The `--skip-hfk` option deliberately skips the full HFK/factor-certificate work;
do not report a skip-mode run as the full replay. This topology replay was not
executed during packaging.

## 4. GST48 replay

Make a scratch copy of `SR-Foxy/research/gst_2026_09_19_exact/` and follow its
`README.md`. Its `requirements.txt` pins the packages. Start with
`verify_algebra.py` and `verify_topology.py`; `replay_saved.py --level 4` supports
four shards for the 15,794 recorded bands. The source includes all 50 self-return
movies. These computations were not rerun in this packaging turn.

## 5. Inspect the saved search without restarting anything

`action_checkpoints/astra_seven_hour_10589240719/evidence.sqlite` is a static
checkpoint, not a running process. Its source and requirements are in `source/`.
Use a read-only SQLite URI when inspecting it. The two completed run rows sum to
3,600.021043032 seconds and 167,163 reported attempts, with no nomination.
The preflight smoke database is separate. Do not run the source's START workflow
merely to read or copy the results. No search is automatically resumed by this ZIP.

## 6. Continue in your existing main checkout

The source is already committed at the pinned revision. You do not need to push
it again. Preserve local work before updating your own checkout:

```sh
git status --short
git branch --show-current
```

Stop if you have unrelated changes or are not on the intended existing `main`.
A clean existing main can be updated without creating a new branch:

```sh
git fetch origin main
git merge --ff-only origin/main
```

If fast-forwarding fails, inspect the divergence; do not force-reset or force-push.
The handoff is an archive for reference, not permission to overwrite newer files.
To publish fresh evidence later, copy only reviewed new result paths, inspect
`git diff --cached`, and make an ordinary commit/push to existing main. Never
blanket-copy `.github/`, historical START markers, or the whole old source tree.

## 7. Recover source history offline

The source is readable without Git. The bundle retains all history reachable
from the pinned commit and contains no stored checkout credentials. From an
existing Git repository, this reads its recorded head without changing a branch:

```sh
git bundle list-heads /path/to/source_export/SR-Foxy-history-8481d99.bundle
git bundle verify /path/to/source_export/SR-Foxy-history-8481d99.bundle
```

Its advertised head is the pinned research revision. The export's own successful
bundle verification and readable 311-commit log are included. Unmerged branches,
untracked files and future commits are not represented by this bundle.
