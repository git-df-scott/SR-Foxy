#!/usr/bin/env python3
"""Checkpoint independent HKL jobs with a hard per-job timeout."""
import argparse,json,subprocess,sys,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('card');p.add_argument('directory');p.add_argument('--timeout',type=float,default=90)
p.add_argument('--cases',nargs='+',default=['4,3,advanced','4,13,advanced','8,3,advanced','8,13,advanced']);a=p.parse_args()
out=Path(a.directory)
if out.exists():raise FileExistsError(out)
out.mkdir(parents=True);rows=[]
for spec in a.cases:
 m,q,method=spec.split(',');result=out/f'{m}_{q}_{method}.json';log=out/f'{m}_{q}_{method}.log'
 cmd=[sys.executable,'scripts/hkl_targeted.py',a.card,str(result),'--p',m,'--q',q,'--method',method]
 start=time.monotonic();row={'p':int(m),'q':int(q),'method':method,'timeout':a.timeout,'command':cmd}
 with log.open('w') as f:
  try:
   r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=a.timeout)
   row['status']='finished' if r.returncode==0 else 'failed';row['returncode']=r.returncode
  except subprocess.TimeoutExpired:row['status']='timeout'
 row['seconds']=round(time.monotonic()-start,3)
 if result.exists():row['result']=json.loads(result.read_text())
 rows.append(row);(out/'manifest.json').write_text(json.dumps({'input':a.card,'jobs':rows,'complete':False},indent=2)+'\n');print(row,flush=True)
(out/'manifest.json').write_text(json.dumps({'input':a.card,'jobs':rows,'complete':True},indent=2)+'\n')
