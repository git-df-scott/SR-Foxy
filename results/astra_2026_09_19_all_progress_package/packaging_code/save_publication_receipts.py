from pathlib import Path
import hashlib,json,shutil
root=Path('/mnt/data/full_work_package')
workflow=r'''name: Astra complete handoff export 2026-09-19

# Archival export only. Does not launch a mathematical search or modify results.
on:
  push:
    branches: [main]
    paths: ['.github/workflows/astra-full-handoff-export-20260919.yml']
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: astra-full-handoff-export-20260919
  cancel-in-progress: false
jobs:
  export:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Read the pinned research revision with its reachable history
        uses: actions/checkout@v4
        with:
          ref: '8481d993ee7763c17a49637112a77673f91c5cb7'
          fetch-depth: 0
          persist-credentials: false
      - name: Export exact source, Git history, and byte manifest
        shell: bash
        run: |
          set -euo pipefail
          mkdir -p export
          git archive --format=tar.gz --prefix=SR-Foxy/ HEAD > export/SR-Foxy-source-8481d99.tar.gz
          git bundle create export/SR-Foxy-history-8481d99.bundle HEAD
          git bundle verify export/SR-Foxy-history-8481d99.bundle > export/BUNDLE_VERIFICATION.txt 2>&1
          git log --format='%H%x09%aI%x09%an%x09%s' HEAD > export/COMMIT_HISTORY.tsv
          python - <<'PY'
          import datetime, hashlib, json, pathlib, subprocess
          def git(*args):
              return subprocess.check_output(['git', *args])
          files = []
          for entry in git('ls-tree', '-rz', 'HEAD').split(b'\0'):
              if not entry:
                  continue
              header, raw_path = entry.split(b'\t', 1)
              mode, kind, oid = header.decode().split()
              path = raw_path.decode('utf-8')
              if kind != 'blob':
                  raise RuntimeError('Non-blob tracked entry requires separate export: ' + path)
              if pathlib.PurePosixPath(path).suffix.lower() in {'.ttf', '.otf', '.woff', '.woff2'}:
                  raise RuntimeError('Do not include font distributions in this handoff: ' + path)
              data = git('cat-file', 'blob', oid)
              files.append({'path':path, 'mode':mode, 'git_blob_sha1':oid, 'bytes':len(data), 'sha256':hashlib.sha256(data).hexdigest()})
          report = {'repository':'git-df-scott/SR-Foxy', 'source_commit':git('rev-parse','HEAD').decode().strip(), 'source_tree':git('rev-parse','HEAD^{tree}').decode().strip(), 'export_workflow_commit':__import__('os').environ['GITHUB_SHA'], 'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'scope':'Exact tracked source at the pinned commit plus all Git history reachable from it; no credentials, local untracked files, external dependency wheels, or future Actions output.', 'mathematical_tests_rerun':False, 'file_count':len(files), 'files':files}
          root = pathlib.Path('export')
          (root/'SOURCE_MANIFEST.json').write_text(json.dumps(report, indent=2)+'\n')
          sums = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.iterdir()) if p.is_file()}
          (root/'SHA256SUMS.json').write_text(json.dumps(sums, indent=2)+'\n')
          print(json.dumps({k:v for k,v in report.items() if k!='files'}, indent=2))
          PY
      - name: Save the complete archive without publishing research claims
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02
        with:
          name: sr-foxy-complete-handoff-8481d99
          path: export/
          retention-days: 7
          if-no-files-found: error
          compression-level: 0
'''
# The raw Python string above preserves the literal backslashes in the YAML heredoc.
readme='''# Complete recovered-work handoff — 19 September 2026

**Slice–Ribbon counterexample: not established.** This is a preservation and reproducibility report, not a claim that the earlier interrupted attempt produced new research.

## Exact source preservation

The consolidated delivery contains every one of the **2,282 tracked files** at commit `8481d993ee7763c17a49637112a77673f91c5cb7`, with source tree `188559fee43401a811824256433aec3a79109ea4`. Each file's byte count, SHA-256 and Git blob SHA-1 was checked locally against the exported manifest, and the source tree was reconstructed exactly. The export also contains a source tarball, a Git bundle with all **311 reachable commits**, and a readable commit log.

This replaces the earlier backup's old-snapshot limitation. It is not a claim to include future commits, unmerged branches, untracked work on other machines or unsaved runtime state.

A read-only export workflow was added directly to existing main in `def9f2192ce6e80393a45c289b77eceb1c3617a2`. Its run **35459378704** completed successfully and produced artifact **10589831421**, named `sr-foxy-complete-handoff-8481d99`. The downloaded archive's SHA-256 is `951a5c072a36f216138a2835bbfec14f80751c435eedd296d5722663b9625766`.

https://github.com/git-df-scott/SR-Foxy/actions/runs/35459378704

No new remote branch was created. No scientific source was overwritten and no mathematical search was launched by this archival export.

## Saved progress included

The source includes the older marked-product, exact-identification and mixed-handle work; the combined initial-audit/one-commutator/explicit-genus-one packages; the newer infection/Whitehead target; the complete GST48 package; the newer Opus infection, HFK/Burau, branched-cover surgery and Eisermann calibration work; and their code, inputs, reports, correction registers, raw outputs and recorded failures.

Important entry points:

- `results/sr_foxy_combined_saved_work_2026_09_19/02_one_commutator/REPORT.md`: the full correction delta=[A,B] and exact commutator-length-one certificate. It is not an annulus or slice disk.
- `results/sr_foxy_combined_saved_work_2026_09_19/03_explicit_genus_one/REPORT.md`: explicit marked genus-one surface, auxiliary unlink/peripheral certificate, actual framed surgery boundary and exact Alexander polynomial. The required sliceness/nonribbonness pair remains missing.
- `research/astra_2026_09_19_infection_gate_and_whitehead_target.md`: repaired infection hypotheses, nonfibered regression control and Whitehead-stabilized auxiliary target. The saved wider first-band test leaves one unexcluded prefix, not a disk.
- `research/gst_2026_09_19_exact/REPORT.md`: literal GST48 input, saved genus/nonfiberedness and Alexander data, exact finite-prefix exclusions and 50 self-return movies. It does not prove global nonribbonness.

Original reports retain historical status and publication statements. Presence in this pinned source is current archival evidence; reading an old RUNNING label is not a live-process check. Other sessions retain credit for their research.

## Four certificate entry points actually rerun

The following were executed successfully in fresh scratch copies, without modifying the archived evidence:

1. `02_one_commutator/check_independent.mjs`.
2. `03_explicit_genus_one/check_exact_independent.mjs`.
3. `03_explicit_genus_one/check_mesh_independent.py`.
4. `03_explicit_genus_one/check_subgroup_independent.py`.

The first checker rechecks the word certificate, full finite witnesses and eight corruptions. The exact genus-one checker reconstructs all 675 crossings, all 670 Fox pivots and all 375 auxiliary Tietze moves, including the framing and polynomial controls. The mesh and subgroup checks are separate algorithms. All four passed. This is replay of saved finite certificates, not a new geometric construction or a full audit of every theorem dependency.

All **365 Python files** in the pinned source passed syntax compilation without imports. Of 838 JSON files, 835 parsed and three existing zero-byte historical outputs did not; they are preserved and explicitly listed in the delivery's integrity report. No JSON results were fabricated to fill those files.

## Saved search checkpoint, not a seven-hour completion claim

The delivery also contains Actions artifact **10589240719** from run **35455048082**, created at **2026-09-19T17:29:39Z**. Its source commit is `042a7dfc6fe61967902e1c4f7174af5f6342862c`.

Two completed common-upper segments record **167,163 reported attempts** and **3,600.021043032 measured seconds**, with no nomination. The saved database has 21,067 node rows, 25,649 retained attempt rows and two run rows. The retained attempt rows are not the aggregate attempt counter. The smoke tests are separate and not counted as completed research segments. SQLite's read-only integrity check passed.

This report does not assert the current status of the live workflow, completion of later segments, seven hours of work, an exhaustive search or a global obstruction. No research was restarted for this handoff.

## Delivery and continuation

The consolidated ZIP contains the exact source tree and history, recovered original research archives, checkpoint/database, a full progress report, all-report and code indexes, pinned dependency instructions, a portable read-only package verifier, a scratch-copy certificate replay helper and the fresh verification logs.

External dependency wheels are not redistributed; environment pins and installation instructions are included. The independent commutator/mesh/subgroup/arithmetic replays do not need the native topology packages. Run scripts in a scratch copy because some write their output JSON files.

The geometric continuation remains: obtain a marked unlink isotopy or spanning-disk system for the explicit auxiliary pair, transport R through the two Rolfsen twists, identify or obstruct the actual surgery boundary, and separately construct the required four-dimensional annulus. Matching an Alexander polynomial, E=0 or a word identity does not discharge those tasks.

The earlier interrupted attempt in this conversation had no unpublished research code. The present additions are preservation, source-integrity checks, the consolidated handoff, and fresh replays of existing certificates. Read the original accountability record at `results/astra_2026_09_19_1608_session_accountability/README.md` alongside this report.
'''
entries=[('.github/workflows/astra-full-handoff-export-20260919.yml',workflow,'9cc44e1cfd986ca772829f9d2bb3c0d4b0ca9b68','def9f2192ce6e80393a45c289b77eceb1c3617a2'),('results/astra_2026_09_19_complete_handoff/README.md',readme,'47edc0b48af3ba894b18d75c950a3b4b839029ca','9e54e4f0c27118e346ff6d8188d71f0f077aee99')]
records=[]
for path,text,sha,commit in entries:
 b=text.encode(); got=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 assert got==sha,(path,got,sha)
 p=root/'publication_payload'/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 records.append({'path':path,'commit':commit,'git_blob_sha1':sha,'read_back_verified':True,'branch':'main'})
shutil.copy2(root/'publication_payload/.github/workflows/astra-full-handoff-export-20260919.yml',root/'packaging_code/astra-full-handoff-export-20260919.yml')
(root/'PUBLICATION.json').write_text(json.dumps(records,indent=2)+'\n')
p=root/'PROVENANCE.json';d=json.loads(p.read_text());d['remote_change_this_packaging_turn']='Read-only export workflow and handoff README added directly to existing main in two ordinary commits; no remote branch created, no scientific source overwritten, no mathematical search launched.';d['handoff_readme_commit']='9e54e4f0c27118e346ff6d8188d71f0f077aee99';p.write_text(json.dumps(d,indent=2)+'\n')
p=root/'FULL_PROGRESS.md';s=p.read_text();s=s.replace('history. The workflow source is included under `packaging_code/`.','history. The workflow source is included under `packaging_code/`.\nThe handoff README was then committed directly to main as\n`9e54e4f0c27118e346ff6d8188d71f0f077aee99` and read back successfully.\nBoth packaging-only additions are preserved under `publication_payload/` with\nexact blob hashes in `PUBLICATION.json`, outside the pinned research source.');p.write_text(s)
p=root/'START_HERE.md';s=p.read_text().replace('- `packaging_code/`: this delivery\'s assembly/recovery/export helpers.','- `packaging_code/`: this delivery\'s assembly/recovery/export helpers.\n- `publication_payload/` and `PUBLICATION.json`: exact copies and receipts for\n  the export workflow and handoff README added directly to existing main.');p.write_text(s)
shutil.copy2(Path(__file__),root/'packaging_code'/Path(__file__).name)
print('Publication files match GitHub blobs:',len(records))
