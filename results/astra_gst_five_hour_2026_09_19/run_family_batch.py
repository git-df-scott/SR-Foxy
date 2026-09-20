import subprocess,sys,time,json
from pathlib import Path
p=Path(__file__).parent;start=time.monotonic();cases=[(3,-1),(3,0),(2,2),(3,2),(4,1),(3,-2),(2,-2),(3,3)];rows=[]
for n,k in cases:
 if time.monotonic()-start>900:break
 out=p/'family'/f'n{n}_k{k}';out.mkdir(parents=True,exist_ok=True)
 if (out/'RESULT.json').exists():continue
 try:
  with (out/'run.log').open('w') as log:
   r=subprocess.run([sys.executable,str(p/'family_case.py'),str(n),str(k)],stdout=log,stderr=subprocess.STDOUT,timeout=120)
  row={'n':n,'k':k,'exit_code':r.returncode}
 except subprocess.TimeoutExpired:row={'n':n,'k':k,'status':'TIMEOUT_120_SECONDS_NOT_A_NEGATIVE_RESULT'}
 rows.append(row);(p/'family'/'BATCH_STATUS.json').write_text(json.dumps({'cases':rows,'seconds':time.monotonic()-start},indent=2)+'\n');print(row,flush=True)
