import subprocess,sys,json,time
from pathlib import Path
p=Path(__file__).parent;rows=[]
for name in ['split_trefoil','L10n57','L14n38935','GST1','GST2']:
 out=p/'suzuki_double'/name;out.mkdir(parents=True,exist_ok=True);start=time.monotonic()
 with (out/'run.log').open('w') as f:
  try:r=subprocess.run([sys.executable,str(p/'suzuki_double_colour.py'),name],stdout=f,stderr=subprocess.STDOUT,timeout=45);s={'exit_code':r.returncode}
  except subprocess.TimeoutExpired:s={'status':'TIMEOUT_45_SECONDS_INCONCLUSIVE'}
 rows.append(dict(label=name,seconds=time.monotonic()-start,**s));(p/'SUZUKI_DOUBLE_BATCH_STATUS.json').write_text(json.dumps(rows,indent=2)+'\n');print(rows[-1],flush=True)
