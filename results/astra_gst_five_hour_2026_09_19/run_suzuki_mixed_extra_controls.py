import subprocess,sys,json
from pathlib import Path
p=Path(__file__).parent;rows=[]
for name,ci in [('L10n57',0),('L10n57',1),('L14n38935',0),('L14n38935',1)]:
 out=p/'suzuki_mixed'/f'{name}_c{ci}';out.mkdir(parents=True,exist_ok=True)
 with (out/'run.log').open('w') as f:
  try:r=subprocess.run([sys.executable,str(p/'suzuki_mixed_colour.py'),name,str(ci)],stdout=f,stderr=subprocess.STDOUT,timeout=30);status={'exit_code':r.returncode}
  except subprocess.TimeoutExpired:status={'status':'TIMEOUT_30_SECONDS_INCONCLUSIVE'}
 rows.append(dict(label=name,cycle=ci,**status));(p/'SUZUKI_MIXED_EXTRA_CONTROL_STATUS.json').write_text(json.dumps(rows,indent=2)+'\n');print(rows[-1],flush=True)
