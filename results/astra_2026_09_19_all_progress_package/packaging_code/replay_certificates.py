#!/usr/bin/env python3
"""Replay four existing certificates in scratch copies; never mutate source inputs."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--package-root',type=Path,default=Path(__file__).resolve().parents[1])
    p.add_argument('--output',type=Path,required=True,help='New or empty directory for logs.')
    p.add_argument('--timeout',type=float,default=60.0,help='Timeout per checker in seconds.')
    args=p.parse_args()
    if args.timeout<=0:p.error('--timeout must be positive')
    if args.output.exists() and any(args.output.iterdir()):p.error('--output must be empty')
    args.output.mkdir(parents=True,exist_ok=True)
    source=args.package_root/'SR-Foxy/results/sr_foxy_combined_saved_work_2026_09_19'
    if not source.is_dir():p.error('Research source directory not found')
    node=shutil.which('node')
    if not node:p.error('Node.js with BigInt support is required')
    jobs=[('one_commutator','02_one_commutator',[node,'check_independent.mjs']),
          ('genus_one_exact','03_explicit_genus_one',[node,'check_exact_independent.mjs']),
          ('genus_one_mesh','03_explicit_genus_one',[sys.executable,'check_mesh_independent.py']),
          ('genus_one_subgroup','03_explicit_genus_one',[sys.executable,'check_subgroup_independent.py'])]
    results=[]
    with tempfile.TemporaryDirectory(prefix='sr-foxy-certificate-replay-') as temp:
        scratch=Path(temp)
        for _,directory,_ in jobs:
            if not (scratch/directory).exists():shutil.copytree(source/directory,scratch/directory)
        for label,directory,command in jobs:
            start=time.monotonic()
            try:
                r=subprocess.run(command,cwd=scratch/directory,capture_output=True,timeout=args.timeout)
                status='PASS' if r.returncode==0 else 'FAIL'; stdout,stderr=r.stdout,r.stderr; code=r.returncode
            except subprocess.TimeoutExpired as e:
                status='TIMEOUT_UNKNOWN'; stdout,stderr=e.stdout or b'',e.stderr or b''; code=None
            except OSError as e:
                status='EXECUTION_ERROR'; stdout,stderr=b'',str(e).encode(); code=None
            (args.output/(label+'.stdout.log')).write_bytes(stdout)
            (args.output/(label+'.stderr.log')).write_bytes(stderr)
            row={'check':label,'command':command,'status':status,'exit_code':code,'seconds':time.monotonic()-start}
            results.append(row); print(json.dumps(row),flush=True)
    (args.output/'RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    return 0 if all(r['status']=='PASS' for r in results) else 1

if __name__=='__main__':
    raise SystemExit(main())
