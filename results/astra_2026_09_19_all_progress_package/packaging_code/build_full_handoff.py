#!/usr/bin/env python3
"""Assemble the recovered handoff in this runtime; no remote writes or searches."""
from pathlib import Path
import argparse, ast, csv, hashlib, json, os, shutil, sqlite3, sys, zipfile
from datetime import datetime, timezone

ROOT=Path('/mnt/data/full_work_package')
SOURCE=ROOT/'SR-Foxy'
META=ROOT/'verification'
META.mkdir(exist_ok=True)

def write(path, text):
    p=ROOT/path; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding='utf-8')

# Preserve original research delivery archives as well as their expanded copies.
originals=ROOT/'original_archives'; originals.mkdir(exist_ok=True)
archives=[]
for p in sorted(Path('/mnt/data/recovered_sources').glob('*.zip')):
    shutil.copy2(p, originals/p.name)
    with zipfile.ZipFile(p) as z:
        bad=z.testzip()
        if bad: raise RuntimeError('Corrupt source archive: '+str(p)+': '+bad)
        archives.append({'file': 'original_archives/'+p.name, 'bytes':p.stat().st_size,
                         'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
                         'regular_members':sum(not i.is_dir() for i in z.infolist()),
                         'uncompressed_bytes':sum(i.file_size for i in z.infolist() if not i.is_dir()),
                         'crc_check':'PASS'})
write(Path('verification/ORIGINAL_ARCHIVES.json'),json.dumps(archives,indent=2)+'\n')

# Archive the previous delivery notes without pretending the old snapshot is current.
previous=ROOT/'previous_delivery'; previous.mkdir(exist_ok=True)
for name in ['SR_Foxy_START_HERE.md','SR_Foxy_verified_backup_53f800f.sha256']:
    shutil.copy2(Path('/mnt/data')/name,previous/name)
with zipfile.ZipFile('/mnt/data/SR_Foxy_verified_backup_53f800f.zip') as z:
    for i in z.infolist():
        if not i.is_dir() and 'VERIFY_BACKUP' in i.filename:
            (previous/Path(i.filename).name).write_bytes(z.read(i))
write(Path('previous_delivery/README.md'),'''# Superseded backup instructions

These are the notes/checksum/verifier delivered with the earlier `53f800f` backup.
They are preserved for accountability, not instructions for the new `8481d99` source.
The earlier backup ZIP is superseded here by the complete newer source and its
reachable Git history. Use the top-level START_HERE.md and VERIFY_PACKAGE.py.
''')

# Historical checkpoint: inspect read-only and avoid double-counting cumulative summaries.
cp=ROOT/'action_checkpoints/astra_seven_hour_10589240719'
conn=sqlite3.connect('file:'+str(cp/'evidence.sqlite')+'?mode=ro',uri=True)
conn.row_factory=sqlite3.Row
integrity=[r[0] for r in conn.execute('PRAGMA integrity_check')]
assert integrity==['ok']
rows=[dict(r) for r in conn.execute('SELECT * FROM runs ORDER BY id')]
for row in rows:
    if isinstance(row.get('summary'),str):
        try:row['summary']=json.loads(row['summary'])
        except json.JSONDecodeError:pass
checkpoint={
    'workflow_run_id':35455048082,'artifact_id':10589240719,
    'artifact_created_at_utc':'2026-09-19T17:29:39Z',
    'downloaded_artifact_sha256':'41b015d6114e936a4514573042377e01a3aefa74caa4a89b7479ffd7ed26d0cc',
    'source_commit':'042a7dfc6fe61967902e1c4f7174af5f6342862c',
    'sqlite_integrity_check':integrity,
    'table_rows':{table:conn.execute('SELECT COUNT(*) FROM '+table).fetchone()[0] for table in ['nodes','attempts','runs']},
    'completed_segments':len(rows), 'runs':rows,
    'measured_completed_search_seconds':sum(r['seconds'] or 0 for r in rows),
    'measured_completed_cpu_seconds':sum(r['cpu_seconds'] or 0 for r in rows),
    'counterexample_established':False,
    'scope':'Saved checkpoint only, not a claim of current live status, seven-hour completion, exhaustive coverage, or global nonribbonness. Smoke tests are separate. SQLite attempts rows are a retained subset, not the reported attempt counter.'}
checkpoint['reported_attempts']=sum(json.loads((cp/f'RUN-common_upper-{i}.json').read_text())['counts']['attempts'] for i in [1,2])
conn.close()
write(Path('verification/SEARCH_CHECKPOINT_SUMMARY.json'),json.dumps(checkpoint,indent=2)+'\n')
print('CHECKPOINT', checkpoint['reported_attempts'], checkpoint['measured_completed_search_seconds'],checkpoint['table_rows'])

provenance={
 'created_at_utc':datetime.now(timezone.utc).isoformat(),
 'repository':'git-df-scott/SR-Foxy',
 'source_commit':'8481d993ee7763c17a49637112a77673f91c5cb7',
 'source_tree':'188559fee43401a811824256433aec3a79109ea4',
 'source_file_count':2282,'reachable_commits':311,
 'source_export_workflow_commit':'def9f2192ce6e80393a45c289b77eceb1c3617a2',
 'source_export_run_id':35459378704,'source_export_artifact_id':10589831421,
 'source_export_download_sha256':'951a5c072a36f216138a2835bbfec14f80751c435eedd296d5722663b9625766',
 'checkpoint_artifact_id':10589240719,
 'scope':'One exact pinned source tree, all history reachable from that commit, recovered original research archives, saved Actions checkpoint, fresh isolated certificate replays, and a consolidated report. Not a promise to include future commits, unmerged branches, uncommitted work on other machines, or unsaved conversation/runtime state.',
 'remote_change_this_packaging_turn':'One read-only export workflow added directly to existing main; no remote branch created, no scientific source overwritten, no mathematical search launched.',
 'research_attribution':'Earlier failed attempt in this chat produced no new candidate or research code. Existing Astra/Opus and GST packages retain authorship. New work in this turn is preservation, source verification and four isolated replays of existing certificate checkers.'}
write(Path('PROVENANCE.json'),json.dumps(provenance,indent=2)+'\n')

# Readable navigation for every saved report, not a curated subset only.
reports=[]; code=[]; deps=[]
for p in sorted(SOURCE.rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(ROOT).as_posix()
    if p.suffix.lower() in {'.md','.rst'}: reports.append(rel)
    if p.suffix.lower() in {'.py','.mjs','.js','.sh','.sage','.ipynb','.cpp','.c','.h'}:code.append(rel)
    if ('requirements' in p.name.lower() or p.name in {'pyproject.toml','package.json','environment.yml','environment.yaml'}):deps.append(rel)
write(Path('REPORT_INDEX.md'),'# All saved text reports\n\nThis is a navigation index, not an endorsement of every historical claim.\nRead the correction registers and later handoffs alongside earlier reports.\n\n'+''.join(f'- [{p}]({p})\n' for p in reports))
write(Path('CODE_INDEX.md'),'# Source-code and dependency index\n\nThe complete pinned source tree is under `SR-Foxy/`.\nRun checkers in a fresh working copy; some write their result files.\n\n## Dependency manifests\n\n'+''.join(f'- [{p}]({p})\n' for p in deps)+'\n## Code\n\n'+''.join(f'- [{p}]({p})\n' for p in code))

write(Path('FULL_PROGRESS.md'),'''# SR-Foxy: full recovered progress and reproducible handoff

19 September 2026. Repository source pinned to
`8481d993ee7763c17a49637112a77673f91c5cb7`.

**No Slice–Ribbon counterexample is established by this package.**
This is the combined saved research record, not a claim that the interrupted
attempt in this chat performed all the work below. The original reports, code,
inputs, certificates, failed attempts and attribution are preserved.

## 1. What this delivery actually contains

`SR-Foxy/` is the complete, byte-verified working tree at the pinned commit:
**2,282 tracked files**, not the earlier 2,034-file `53f800f` snapshot and not a
selection of recent reports. This includes the newer Opus files as well as Astra
work, the merged GST package, campaign notes, correction registers, diagrams,
raw records, source code, tests and previously committed ZIPs.

`source_export/` preserves the exact source tarball, the export's per-file
manifest, a readable commit log and a Git bundle containing all **311 commits
reachable from the pinned revision**. That bundle is history, not a credentialed
`.git` directory. Other unmerged branches are outside this source snapshot.

`original_archives/` retains the separately recovered combined-work, GST,
17 September recovered-chat, and preflight ZIPs. The combined archive itself
preserves its three original research ZIPs. These duplicates are intentional:
original delivery bytes and internal relative paths remain available.

`action_checkpoints/` preserves the recovered search database, segment reports,
controls, frozen runner source, dependency versions and smoke-test records.
`verification/` records this turn's actual integrity checks and fresh isolated
certificate replays. `REPORT_INDEX.md` and `CODE_INDEX.md` locate all reports and
code, including older work not individually restated here.

The exact source tree is not silently patched with packaging files. New handoff
material lives outside `SR-Foxy/`. `PROVENANCE.json` records the revision, export
run, artifact IDs, timestamps and scope.

## 2. Accountability for this conversation

The first research attempt visible in this conversation failed during repository
inspection. It produced no new knot candidate, invariant calculation, slice-disk
movie, mathematical certificate or unpublished research code. The report at
`SR-Foxy/results/astra_2026_09_19_1608_session_accountability/README.md` records
that distinction and was previously committed directly to main as
`9d2e95b772dd54dc4fd13ff7a521649834e7e4eb`.

The earlier backup delivery was complete only for its older pinned revision; it
was not a full export of the later main. This delivery replaces that limitation
with the exact newer source and reachable history. No new mathematical discovery
is being claimed merely because the files have now been collected together.

During this packaging turn, one read-only archival workflow was added to the
existing main branch, commit `def9f2192ce6e80393a45c289b77eceb1c3617a2`.
Its completed run exported the pinned source and history. It did not start a new
knot search, overwrite scientific results, create a remote branch, or rewrite
history. The workflow source is included under `packaging_code/`.

## 3. The exact one-commutator result

Read the complete report and certificates in:
`SR-Foxy/results/sr_foxy_combined_saved_work_2026_09_19/02_one_commutator/`.

For the recorded eighteen-generator boundary presentation and original
104-letter correction delta, the saved result is

    delta = [A,B],  [A,B] = A B A^-1 B^-1,
    A = [4,-3,-3,1],
    B = [4,-9,-1,3,-1,8,-5,-8,1,1].

Both factors have meridional exponent zero. Seven Tietze eliminations and four
finite Schreier rules reduce the original correction and the displayed
commutator to the same 42-letter word. A representation of the full boundary
group into SL(2,F11) makes delta nonidentity. Together these certify the recorded
statement that its commutator length within G' is exactly one.

This replaced a thirteen-commutator recipe with a one-handle-pair recipe. It did
not turn a word identity into an annulus, identify a surgery knot, or prove
sliceness. The old stalled shortlex rewrite remains an inconclusive attempt,
not an obstruction. The package retains the full inputs, finite witnesses,
producer, independent JavaScript checker, compatibility identity and corrupt
certificate tests.

**Fresh replay in this delivery:** `check_independent.mjs` exited successfully.
Its exact identity, finite witnesses and eight deliberate corruptions were
checked again in a separate copy. The stdout/stderr and command record are in
`verification/replays/`; original saved outputs were not changed.

## 4. Explicit genus-one geometry and the actual surgery boundary

Read:
`SR-Foxy/results/sr_foxy_combined_saved_work_2026_09_19/03_explicit_genus_one/REPORT.md`.

This is a concrete construction, not just the previous algebraic recipe. The
saved integer-coordinate model realizes the two handle words, transports the
markings and constructs a genus-one surface from b-minus to b-prime. Its mesh
has V=499, E=1005, F=504, Euler characteristic -2 and two boundary components.
The record includes exact intersection checks, both boundary polygons, drawings,
an OBJ model and two failed or superseded construction attempts.

The final generic projection has 675 crossings. This is the size of an explicit
presentation, not a minimal crossing number or a count of different candidate
knots. The auxiliary sublink has a full peripheral certificate: 375 recorded
Tietze eliminations from 377 generators leave a free two-generator group and
both preferred longitudes become trivial. The report explains the theorem-based
unlink implication. It does not supply an explicit unlink isotopy.

The specified +1,-1 surgeries on that auxiliary unlink define an actual knot
K_new in S3. The exact Fox calculation replays 670 Laurent-unit pivots, retains
the preferred longitudes, obtains E(t)=0, and gives

    Delta(K_new) = d(t)^2,
    d(t) = t^4 - 3t^3 + 5t^2 - 3t + 1.

The expanded polynomial is
`[1,-6,19,-36,45,-36,19,-6,1]` and its determinant is 169.
The parameterized calculation proves the same order for the specified
(1,x),(1,y) family; it does not prove those knots isotopic, concordant or slice.

A separate subgroup certificate gives an injective map for this particular
surface under the recorded algebraic q0. Its no-compression interpretation is
conditional on identifying q0 with the geometric disk-exterior inclusion. Even
that interpretation does not exclude a different annulus between a and b-prime.
The correction surface has different boundary components and is not itself the
annulus required for annulus modification.

**What remains missing:** an ordinary diagram/identification or independent
nonribbon proof for this actual surgery boundary, plus the required modifying
annulus and standard-B4 conclusion. The ordinary two-handle trace has rank-two
H2 and is not B4. E=0 and the matching Alexander polynomial do not fill this gap.
The saved filled-group timeout is TIMEOUT_UNKNOWN, not a result.

**Fresh replays in this delivery:** all three documented independent checkers
passed in a separate copy: the integer projection/peripheral/Fox verifier, the
rational mesh-intersection verifier, and the subgroup verifier. The first
reconstructed all 675 crossings, all 670 pivots and all 375 auxiliary Tietze
moves, and rejected the recorded framing/longitude/polynomial/pivot corruptions.
These are bounded certificate replays, not a new global geometric theorem.

## 5. Infection audit and the nonfibered Whitehead stabilizer

Read:
`SR-Foxy/research/astra_2026_09_19_infection_gate_and_whitehead_target.md`
and `SR-Foxy/results/astra_2026_09_19_infection_gate/`.

The saved audit repairs the original infection argument with explicit satellite,
axis and essentiality hypotheses. It derives an all-winding obstruction for a
genuine fibered satellite with nontrivial slice companion and irreducible
Alexander polynomial. It also separates genus preservation from fiberedness,
gives the precise primality lemma, and corrects the claim that all campaign
routes share one unresolved standardization problem. Those source-based theorem
claims are preserved with their citations; they were not newly researched or
independently re-proved during packaging.

The regression example 12n382 is monic, irreducible-Delta, genus two and
full-degree, but nonfibered: its top HFK rank is three, not one. Its tau is one,
so it is a regression control, not a slice candidate.

The constructive auxiliary target is

    R = the square knot,
    J = the positive untwisted Whitehead double of R,
    T = stored D01 # J.

The saved diagrams have respectively 6, 26 and 51 crossings (D01 itself has 25).
The saved HFK data give J genus one and rank 33; T is nonfibered, genus five and
rank 5577. The report gives a ribbon construction for J. A ribbon certificate
for T would therefore imply D01 slice, but **no ribbon or slice disk for T was
obtained**. This is an auxiliary target, not an established counterexample.

The bounded first-band record has 544 distinct mixed bands in the smaller test,
all excluded by the stated necessary tests. The wider test has 8,106 distinct
mixed bands: 6,703 linking exclusions, 1,383 rank-zero exclusions, and 20
necessary-test passes. The saved prefix analysis excludes 19 of those 20;
`ca080502_0_-1` remains unexcluded by that analysis. It is a single bounded
prefix, not evidence that its continuation is slice or ribbon.

The full replay script, target PDs/HFK, regression control and summary are
included. The script can regenerate detailed band/prefix ledgers into a fresh
output directory. Those regenerated ledgers were not produced in this packaging
turn, and file names mentioned by the script are not asserted to be pre-existing
committed outputs. Use the supplied runbook and pinned package versions.

## 6. GST48: diagram, algebra, Floer data and finite-prefix work

Read `SR-Foxy/research/gst_2026_09_19_exact/REPORT.md` and `STATUS.json`.
This entire 65-file research directory and its original delivery ZIP are here.
Historical statements in the original report that it was not yet pushed are
preserved; its files are present in the pinned source used for this delivery.

The literal 48-crossing PD is supplied. Its identification as the published GST
example is source-attributed; the package does not independently replay a Kirby
bridge from that PD to the original paper's figure. This distinction remains
important when attaching a published sliceness theorem to the input.

The saved Floer computation gives genus 10, total rank 189 and top Alexander
rank two, so the direct fibered-knot obstruction is unavailable. It records F2/F3
and mirror/relabeling checks, the Euler-characteristic comparison and a complete
reduced 189-generator UV=0 complex. These check the stated calculation but do not
formally verify the Floer implementation.

The Alexander polynomial has breadth 16 and determinant one. Its distinct
reciprocal degree-eight factors give two rational primary summands and exactly
two rational Blanchfield metabolizers under the report's argument. This does
**not** mean that only two slice or ribbon disks are left to test. The recorded
resultant is 43^2, with the prime-43 interaction and an order-11 finite-field
calculation saved explicitly.

For the fixed diagram and stated band generators, all 164 single-face bands
are excluded by exact Alexander-rank certificates. The next setting has 1,698
bands, all excluded after separate-variable checks. In the larger 15,794-band
setting, the final disposition is 13,269 linking exclusions, 2,463
single-variable rank exclusions, 12 separate-variable rank exclusions and
50 replayable self-returns to the original knot plus a split unknot.

Those 50 movies are not new candidates and are not a ribbon disk. They also
cannot be discarded from every possible movie: later bands could use the added
unknot. The package supplies no theorem that all ribbon disks start within this
finite generator set. The global nonribbon question remains unresolved.

This packaging turn preserved these outputs and checked file integrity; it did
not rerun the GST search, its Floer calculation or all 15,794 replay records.

## 7. Existing marked-product, mixed-handle and Opus work

The source retains the marked-product/annulus directories, exact-identification
handoff, fixed-stabilizer and mixed-handle reports, and their recorded failures.
The mixed-handle work identifies a protected-axis linking issue for the specified
transfer and leaves the required geometric connector/Whitney-disk construction
open. Those are scoped exclusions, not a theorem excluding every possible
four-dimensional transfer. Start with the current Astra brief, correction
registers and later handoffs rather than taking an old status label literally.

All newer Opus infection, branched-cover surgery, HFK/Burau and Eisermann
calibration files present at the pinned revision are included, not merely cited
from a different checkout. The earlier status recovery read K0/K1 consistency
rows and the 599-control Eisermann calibration. Reading their saved outputs is
not an independent rerun; the full source and logs now allow another researcher
to audit them. Counts from different walker snapshots must not be added, and
historical RUNNING labels are not live-process evidence.

Older Astra recovery packages, supporting code, data and publication records
remain under the original `results/` paths and in the included history. The
complete report and code indexes are the inventory of those additional lanes.

## 8. What the recovered Actions checkpoint actually proves about work done

The preserved checkpoint is artifact 10589240719 from run 35455048082, created
at 17:29:39 UTC on 19 September 2026. It contains **two completed common-upper
segments**, not a completed seven-hour campaign:

- Segment 1: 88,855 reported attempts, 1,800.016701387 measured seconds.
- Segment 2: 78,308 reported attempts, 1,800.004341645 measured seconds.

That is **167,163 reported attempts and 3,600.021043032 measured seconds**.
Both completed segment statuses report no nomination. The database contains
21,067 node rows, 25,649 retained attempt rows and two run rows. The attempt
row count is not the aggregate attempt counter; do not conflate them. The
preflight's two five-second smoke runs are separate and are not added to the
completed research time.

The database passed SQLite's read-only integrity check in this delivery. The
frozen inputs, runner, requirement pins and environment listing are included.
No claim is made that later segments completed, that the whole seven hours ran,
or that a historical workflow is still running. Future output is outside this
fixed archive. A large negative search is not a global obstruction.

## 9. Verification completed while building this package

Every one of the 2,282 source files matched its exported byte count, SHA-256 and
Git blob SHA-1. The reconstructed Git tree equals
`188559fee43401a811824256433aec3a79109ea4`, the pinned source tree.
All **365 Python files passed syntax compilation** without imports or execution.
Of 838 JSON files, 835 parsed; the other three are existing zero-byte historical
outputs, preserved unchanged and listed in `verification/SOURCE_INTEGRITY.json`.
They are not successful computations or silently repaired data.

Four independent certificate checker entry points were actually rerun, all
successfully, in isolated working copies. Their logs and commands are saved.
Original archive CRC checks and the recovered database integrity check passed.
The export also includes a successful Git bundle verification record. This is
not a claim that every script, proof implication, citation or dependency in the
research repository has been audited.

## 10. Exact continuation and boundaries of this handoff

For the explicit surgery knot, the next concrete operation stated by the saved
geometry report is an explicit marked unlink isotopy or spanning-disk system,
followed by the two Rolfsen twists while transporting R. That yields an ordinary
diagram of the actual boundary and enables an identification/nonribbon audit on
the correct object. The required four-dimensional annulus remains a separate
construction. Do not replace these tasks with another word identity or a matching
Alexander polynomial.

The Whitehead-stabilized target and GST48 are independent saved objects with
separate logical gaps. A passing prefix, HFK consistency check, genus-one surface,
zero longitude response, common zero surgery or homotopy-ball disk must not be
promoted into a standard-B4 slice disk plus global nonribbon proof.

This archive contains the exact pinned committed work and the recovered saved
packages/checkpoint. It cannot represent unsaved output on other machines,
future commits, unmerged branches or a verbatim transcript of every conversation.
External dependency wheels are not bundled; package versions and installation
instructions are included. No counterexample claim is hidden behind those scope
limits: **the required paired sliceness and nonribbonness certificates have not
been established here.**
''')

write(Path('START_HERE.md'),'''# SR-Foxy — one complete recovered-work package

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
''')

write(Path('RUNBOOK.md'),'''# Reproduction and continuation

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
''')
write(Path('packaging_code/requirements-topology.txt'),'snappy==3.3.2\nspherogram==2.4.1\nregina==7.4.1\nknot_floer_homology==1.2.2\nsympy==1.14.0\n')

# Retain the actual helper scripts used for recovery and fresh replays.
for name in ['save_recovered_git_files.py','save_workflow_sources.py','run_handoff_checks.py','build_full_handoff.py']:
    p=Path('/mnt/data')/name
    if p.exists():shutil.copy2(p,ROOT/'packaging_code'/name)
for name in ['recovered_git_blobs.json','recovered_workflow_blobs.json']:
    shutil.copy2(Path('/mnt/data')/name,ROOT/'packaging_code'/name)
write(Path('packaging_code/README.md'),'''# Packaging and recovery helpers

`VERIFY_PACKAGE.py` at the delivery root is the portable, read-only integrity
checker. `requirements-topology.txt` is a convenience copy of the versions
recorded by the research; it is not represented as an earlier committed file.

Other scripts in this directory are the actual recovery/assembly helpers used
in the isolated `/mnt/data` runtime. They retain their original runtime paths
and are preserved as a record, not a one-command installer or a complete archive
fetcher. They do not contain credentials. Do not run them against a live checkout.
The source export workflow is the exact read-only workflow committed to existing
main for this delivery. Its execution completed before this package was issued.
No helper automatically resumes the mathematical search or pushes changes.
''')
print('REPORT WORDS',len((ROOT/'FULL_PROGRESS.md').read_text().split()))
print('INDICES',len(reports),'reports',len(code),'code',len(deps),'dependency manifests')
