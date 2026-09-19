from pathlib import Path
import hashlib, json
root=Path('/mnt/data/full_work_package/SR-Foxy')
records=[]
def save(name,s,sha):
    b=s.encode();actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    if actual != sha: raise ValueError((name,actual,sha))
    p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    records.append({'path':name,'git_blob_sha1':sha,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)})
save('.github/workflows/astra-boundary-tools-20260919.yml',r'''name: Astra boundary recovery tools 2026-09-19
on:
  push:
    branches: [main]
    paths: ['.github/workflows/astra-boundary-tools-20260919.yml']
  workflow_dispatch:
permissions:
  contents: read
jobs:
  tools:
    runs-on: ubuntu-latest
    timeout-minutes: 8
    steps:
      - uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065
        with:
          python-version: '3.13'
      - name: Retrieve pinned GMP rational arithmetic distribution
        shell: bash
        run: |
          set -euo pipefail
          mkdir -p arithmetic-wheel
          python -m pip download --only-binary=:all: --no-deps --dest arithmetic-wheel 'gmpy2==2.2.1'
          (cd arithmetic-wheel && sha256sum *.whl > SHA256SUMS)
          printf '%s\n' 'Public pinned gmpy2 distribution for exact rational geometry.' 'No repository checkout, secret access, or result mutation.' > arithmetic-wheel/PROVENANCE.txt
      - name: Export distribution bytes
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02
        with:
          name: astra-boundary-gmpy2-cp313
          path: arithmetic-wheel/
          retention-days: 7
          if-no-files-found: error
''','526557f1d8e03838f103f042f50bfc0d63bdb243')
save('.github/workflows/astra-gst-primary-source-20260919.yml',r'''name: Astra GST primary vector source 2026-09-19
on:
  push:
    branches: [main]
    paths: ['.github/workflows/astra-gst-primary-source-20260919.yml']
  workflow_dispatch:
permissions:
  contents: read
jobs:
  primary-source:
    runs-on: ubuntu-latest
    timeout-minutes: 8
    steps:
      - name: Fetch the pinned public primary paper and figure source
        shell: bash
        run: |
          set -euo pipefail
          mkdir -p primary
          curl --fail --location --retry 2 --max-time 90 'https://arxiv.org/e-print/1103.1601v1' -o primary/1103.1601v1-source.tar
          curl --fail --location --retry 2 --max-time 90 'https://arxiv.org/pdf/1103.1601v1' -o primary/1103.1601v1.pdf
          printf '%s\n' 'Public primary source only. No repository checkout or mutation.' 'https://arxiv.org/e-print/1103.1601v1' 'https://arxiv.org/pdf/1103.1601v1' > primary/PROVENANCE.txt
          (cd primary && sha256sum 1103.1601v1* > SHA256SUMS)
      - name: Export original bytes for diagram verification
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02
        with:
          name: astra-gst-primary-1103-1601v1
          path: primary/
          retention-days: 7
          if-no-files-found: error
''','2bb67a3f1bf1373b714327e8fcbe51a3561c392b')
save('.github/workflows/astra-snapshot-20260919.yml',r'''name: Astra research snapshot 2026-09-19

# Read-only environment setup; reruns only when this file changes or by dispatch.
on:
  push:
    branches: [main]
    paths: ['.github/workflows/astra-snapshot-20260919.yml']
  workflow_dispatch:
permissions:
  contents: read
jobs:
  dependencies:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - name: Fetch missing offline CPython 3.13 topology dependencies
        shell: bash
        run: |
          set -euo pipefail
          mkdir -p export/wheels
          for package in 'cypari>=2.3' 'low_index>=1.2.1' 'tkinter-gl>=1.0' 'pypng' 'pickleshare'; do
            python -m pip download --dest export/wheels --no-deps --only-binary=:all: --platform manylinux_2_17_x86_64 --platform manylinux2014_x86_64 --platform manylinux_2_24_x86_64 --platform manylinux_2_28_x86_64 --platform manylinux_2_34_x86_64 --python-version 313 --implementation cp --abi cp313 "$package" || printf 'UNAVAILABLE: %s\n' "$package" >> export/wheels/UNAVAILABLE.txt
          done
          python -m pip wheel --wheel-dir export/wheels --no-deps PyX
          (cd export/wheels && sha256sum *.whl > SHA256SUMS)
      - name: Publish dependency wheels
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02
        with:
          name: sr-foxy-extra-wheels-cp313
          path: export/wheels/
          retention-days: 3
          if-no-files-found: error
          compression-level: 0
''','3c5a7cb742ba7f64c2295ae9dec5ec7728cc5e9f')
save('.github/workflows/astra-surgery-environment-20260919.yml',r'''name: Astra surgery environment 2026-09-19
on:
  push:
    paths:
      - '.github/workflows/astra-surgery-environment-20260919.yml'
  workflow_dispatch:
permissions:
  contents: write
jobs:
  wheelhouse:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - name: Record run identifier
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          cat > /tmp/record_run.py <<'PY'
          import os,json,urllib.request,urllib.error,base64
          path='results/astra_surgery_bootstrap_2026_09_19/RUN.json'
          url='https://api.github.com/repos/'+os.environ['GITHUB_REPOSITORY']+'/contents/'+path
          headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json'}
          record={'run_id':int(os.environ['GITHUB_RUN_ID']),'source_commit':os.environ['GITHUB_SHA'],'status':os.environ.get('RESULT_STATUS','STARTED'),'artifact_id':os.environ.get('ARTIFACT_ID',''),'scope':'Topology environment bootstrap only; no mathematical result.'}
          payload={'message':'Record Astra topology bootstrap '+record['status'],'branch':'main','content':base64.b64encode((json.dumps(record,indent=2)+'\n').encode()).decode()}
          try:
              with urllib.request.urlopen(urllib.request.Request(url,headers=headers)) as r: payload['sha']=json.load(r)['sha']
          except urllib.error.HTTPError as e:
              if e.code!=404: raise
          with urllib.request.urlopen(urllib.request.Request(url,data=json.dumps(payload).encode(),headers=headers,method='PUT')) as r: print('Run record published:',json.load(r)['commit']['sha'])
          PY
          python /tmp/record_run.py
      - name: Build topology wheelhouse
        run: |
          mkdir -p wheelhouse
          python -m pip wheel --wheel-dir wheelhouse snappy==3.3.2 regina==7.4.1 gmpy2
          python -m pip install --no-index --find-links wheelhouse snappy==3.3.2 regina==7.4.1 gmpy2
          python - <<'PY'
          import json,pathlib,hashlib,sys,snappy,regina,gmpy2
          p=pathlib.Path('wheelhouse')
          r={'python':sys.version,'snappy':snappy.__version__,'regina':regina.versionString(),'gmpy2':gmpy2.version(),'files':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in p.iterdir() if f.is_file()}}
          (p/'MANIFEST.json').write_text(json.dumps(r,indent=2))
          PY
      - uses: actions/upload-artifact@v4
        id: archive
        with:
          name: astra-topology-wheelhouse-20260919
          path: wheelhouse/
          retention-days: 7
          if-no-files-found: error
      - name: Record completion
        if: always()
        env:
          GH_TOKEN: ${{ github.token }}
          RESULT_STATUS: ${{ job.status }}
          ARTIFACT_ID: ${{ steps.archive.outputs.artifact-id }}
        run: python /tmp/record_run.py
''','98848cf38803cd68ea18aa8cde6fef594e7b36af')
save('results/astra_surgery_bootstrap_2026_09_19/RUN.json','''{
  "run_id": 35417723921,
  "source_commit": "b87baaf335eced0b5967e247c771a84d73d75853",
  "status": "success",
  "artifact_id": "10576048198",
  "scope": "Topology environment bootstrap only; no mathematical result."
}
''','07b6a1ddc7bb5783a9c64f414a1190aeee04b112')
head=r'''name: Astra seven-hour movie search 2026-09-19

# A deliberate, separate START.json commit launches the first run.
# Ordinary scientific edits and workflow edits do not launch another search.
on:
  push:
    branches: [main]
    paths: ['research_jobs/astra_seven_hour_20260919/START.json']
  workflow_dispatch:

permissions:
  contents: read
concurrency:
  group: astra-seven-hour-movie-search-20260919
  cancel-in-progress: false

env:
  PYTHONUNBUFFERED: '1'
  PYTHONHASHSEED: '0'

jobs:
  validate:
    name: Mathematical controls and short end-to-end tests
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.sha }}
          persist-credentials: false
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - name: Install pinned topology environment
        run: |
          python -m pip install -r research_jobs/astra_seven_hour_20260919/requirements.txt
          mkdir -p evidence/source evidence/smoke
          cp research_jobs/astra_seven_hour_20260919/* evidence/source/
          python -m pip freeze > evidence/environment.txt
      - name: Verify frozen diagram fields against this checkout
        run: |
          python - <<'PY'
          import json,pathlib
          p=pathlib.Path('research_jobs/astra_seven_hour_20260919')
          x=json.loads((p/'INPUTS.json').read_text())
          for field,name in [('D01','AbeTagami_D_0_1.json'),('K1','AbeTagami_K_1.json')]:
              source=json.loads((pathlib.Path('data/knots')/name).read_text())
              if x[field] != source['pd_code']:
                  raise RuntimeError('CONTROL FAILURE: frozen diagram differs from checkout: '+name)
          PY
      - name: Run mathematical controls
        run: python research_jobs/astra_seven_hour_20260919/runner.py --out evidence --controls
      - name: Smoke test both computation phases without counting them toward seven hours
        run: |
          cp evidence/CONTROLS.json evidence/smoke/CONTROLS.json
          python research_jobs/astra_seven_hour_20260919/runner.py --out evidence/smoke --phase common_upper --segment 1 --seconds 5
          python research_jobs/astra_seven_hour_20260919/runner.py --out evidence/smoke --phase stabilized_disks --segment 1 --seconds 5
      - name: Publish preflight evidence even on failure
        if: always()
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02
        with:
          name: astra-seven-hour-preflight
          path: evidence/
          retention-days: 7
          if-no-files-found: warn

  phase_one:
    name: Phase 1 - 3.5 hours of common-upper movie search
    needs: validate
    runs-on: ubuntu-latest
    timeout-minutes: 260
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.sha }}
          persist-credentials: false
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - name: Install pinned topology environment
        run: python -m pip install -r research_jobs/astra_seven_hour_20260919/requirements.txt
      - uses: actions/download-artifact@v4
        with:
          name: astra-seven-hour-preflight
          path: evidence
'''
for i in range(1,8):
    head += f'''      - name: Common-upper segment {i} of 7
        uses: ./research_jobs/astra_seven_hour_20260919
        with:
          phase: common_upper
          segment: '{i}'
'''
head+=r'''
  phase_two:
    name: Phase 2 - 3.5 hours of stabilized disk-movie search
    needs: phase_one
    runs-on: ubuntu-latest
    timeout-minutes: 260
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.sha }}
          persist-credentials: false
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - name: Install pinned topology environment
        run: python -m pip install -r research_jobs/astra_seven_hour_20260919/requirements.txt
      - uses: actions/download-artifact@v4
        with:
          name: astra-seven-hour-checkpoint
          path: evidence
'''
for i in range(1,8):
    head+=f'''      - name: Stabilized-disk segment {i} of 7
        uses: ./research_jobs/astra_seven_hour_20260919
        with:
          phase: stabilized_disks
          segment: '{i}'
'''
head+=r'''      - name: Report measured computation time, never assumed completion
        run: |
          python - <<'PY'
          import json,pathlib,sqlite3
          p=pathlib.Path('evidence')
          c=sqlite3.connect(p/'evidence.sqlite')
          rows=c.execute('SELECT phase,segment,status,seconds,cpu_seconds FROM runs ORDER BY id').fetchall()
          expected={(phase,i) for phase in ['common_upper','stabilized_disks'] for i in range(1,8)}
          finished={(r[0],r[1]) for r in rows if r[2]=='BOUNDED_SEGMENT_COMPLETE_NO_NOMINATION'}
          measured=sum(r[3] or 0 for r in rows)
          answer={'counterexample_established':False,'requested_search_seconds':25200,'measured_search_seconds':measured,'measured_cpu_seconds':sum(r[4] or 0 for r in rows),'both_phases_complete':finished==expected,'seven_hours_recorded':finished==expected and measured>=25200,'scope':'Bounded randomized searches only. A negative search is not a nonconcordance or nonribbonness theorem. UNKNOWN computations remain UNKNOWN.'}
          (p/'FINAL.json').write_text(json.dumps(answer,indent=2)+'\n')
          print(json.dumps(answer,indent=2))
          with open(__import__('os').environ['GITHUB_STEP_SUMMARY'],'a') as s:
              s.write('## Measured search result\n\n```json\n'+json.dumps(answer,indent=2)+'\n```\n')
          PY
      - name: Publish final cumulative evidence
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02
        with:
          name: astra-seven-hour-checkpoint
          path: evidence/
          overwrite: true
          retention-days: 7
          if-no-files-found: error
          compression-level: 6
'''
save('.github/workflows/astra-seven-hour-movie-search-20260919.yml',head,'7d907776e9ed7803f389d858bcae363cdc371800')
Path('/mnt/data/recovered_workflow_blobs.json').write_text(json.dumps(records,indent=2)+'\n')
print('All',len(records),'workflow/environment source files match pinned GitHub blob hashes.')
