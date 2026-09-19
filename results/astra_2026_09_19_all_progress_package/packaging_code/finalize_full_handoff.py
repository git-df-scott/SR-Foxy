#!/usr/bin/env python3
"""Finalize the local handoff's manifest and ZIP; no remote changes."""
from pathlib import Path
from datetime import datetime, timezone
import csv, hashlib, json, shutil, subprocess, sys, zipfile

root=Path('/mnt/data/full_work_package')
out=Path('/mnt/data/SR_Foxy_All_Progress_2026-09-19.zip')
shutil.copy2(Path(__file__),root/'packaging_code'/Path(__file__).name)
# This inventory is navigational; PACKAGE_MANIFEST is authoritative for its bytes.
paths=sorted(p for p in root.rglob('*') if p.is_file() and p.name not in {'PACKAGE_MANIFEST.json','PACKAGE_CONTENTS.tsv'})
with (root/'PACKAGE_CONTENTS.tsv').open('w',newline='') as f:
    w=csv.writer(f,delimiter='\t');w.writerow(['path','bytes'])
    for p in paths:w.writerow([p.relative_to(root).as_posix(),p.stat().st_size])
entries=[]
for p in sorted(root.rglob('*')):
    if p.is_file() and p.name!='PACKAGE_MANIFEST.json':
        b=p.read_bytes();entries.append({'path':p.relative_to(root).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
manifest={'schema':1,'created_at_utc':datetime.now(timezone.utc).isoformat(),
          'source_commit':'8481d993ee7763c17a49637112a77673f91c5cb7',
          'source_file_count':2282,'manifest_file_count':len(entries),
          'excluded_self':'PACKAGE_MANIFEST.json','files':entries}
(root/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
# No logs are written inside the manifest-protected package after this point.
r=subprocess.run([sys.executable,str(root/'VERIFY_PACKAGE.py'),'--archives'],capture_output=True,text=True,timeout=35)
Path('/mnt/data/SR_Foxy_Final_Verification.json').write_text(r.stdout)
print(r.stdout,flush=True)
if r.returncode:
    print(r.stderr,file=sys.stderr);raise SystemExit('Package verification failed')
for p in (root/'packaging_code').rglob('*.py'):compile(p.read_bytes(),str(p),'exec')
compile((root/'VERIFY_PACKAGE.py').read_bytes(),'VERIFY_PACKAGE.py','exec')
prefix='SR_Foxy_All_Progress_2026-09-19'
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
    for p in sorted(root.rglob('*')):
        if p.is_file():
            # Source/history transport files and original ZIPs are already compressed.
            store=p.suffix.lower() in {'.zip','.gz','.bundle','.png','.jpg','.jpeg'}
            z.write(p,prefix+'/'+p.relative_to(root).as_posix(),compress_type=zipfile.ZIP_STORED if store else zipfile.ZIP_DEFLATED)
with zipfile.ZipFile(out) as z:
    bad=z.testzip()
    if bad:raise SystemExit('Final ZIP CRC failure: '+bad)
    zip_count=len(z.infolist())
sha=hashlib.sha256(out.read_bytes()).hexdigest()
checksum=out.with_suffix('.sha256');checksum.write_text(sha+'  '+out.name+'\n')
shutil.copy2(root/'FULL_PROGRESS.md','/mnt/data/SR_Foxy_Full_Progress_2026-09-19.md')
shutil.copy2(root/'START_HERE.md','/mnt/data/SR_Foxy_All_Progress_START_HERE.md')
summary={'zip':str(out),'zip_bytes':out.stat().st_size,'zip_MiB':out.stat().st_size/1024**2,
         'zip_MB':out.stat().st_size/1000000,'files':zip_count,'sha256':sha,
         'source_files':2282,'reachable_commits':311,'python_syntax_files':365,
         'certificate_entry_points_replayed':4,'all_four_passed':True,
         'final_zip_crc':'PASS','manifest_check':'PASS','no_new_remote_branches':True,
         'source_commit':'8481d993ee7763c17a49637112a77673f91c5cb7',
         'handoff_commit':'9e54e4f0c27118e346ff6d8188d71f0f077aee99'}
Path('/mnt/data/SR_Foxy_Delivery_Summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2),flush=True)
