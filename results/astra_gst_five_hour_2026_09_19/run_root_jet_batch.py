import subprocess,sys,json,time
from pathlib import Path
p=Path(__file__).parent;rows=[]
for n,k in [(2,2),(3,2),(3,-2),(2,-2),(3,3)]:
 d=p/'family'/f'n{n}_k{k}'
 if not (d/'OUTPUT_PD.json').exists():rows.append({'n':n,'k':k,'status':'NO_PD'});continue
 try:
  with (d/'root_jet.log').open('w') as f:r=subprocess.run([sys.executable,str(p/'run_root_jet_case.py'),str(n),str(k)],stdout=f,stderr=subprocess.STDOUT,timeout=60)
  rows.append({'n':n,'k':k,'exit_code':r.returncode})
 except subprocess.TimeoutExpired:rows.append({'n':n,'k':k,'status':'TIMEOUT_60_SECONDS_INCONCLUSIVE'})
 (p/'family'/'ROOT_JET_BATCH_STATUS.json').write_text(json.dumps(rows,indent=2)+'\n');print(rows[-1],flush=True)
