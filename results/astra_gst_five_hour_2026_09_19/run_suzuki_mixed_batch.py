import subprocess,sys,json,time
from pathlib import Path
p=Path(__file__).parent;rows=[]
for name,ci in [('unlink',0),('split_trefoil',0),('split_trefoil',1),('L10n36',1),('L5a1',0),('L5a1',1),('GST1',0),('GST1',1),('GST2',0),('GST2',1),('GST3',0),('GST3',1)]:
 out=p/'suzuki_mixed'/f'{name}_c{ci}';out.mkdir(parents=True,exist_ok=True);start=time.monotonic()
 with (out/'run.log').open('w') as f:
  try:r=subprocess.run([sys.executable,str(p/'suzuki_mixed_colour.py'),name,str(ci)],stdout=f,stderr=subprocess.STDOUT,timeout=45);status={'exit_code':r.returncode}
  except subprocess.TimeoutExpired:status={'status':'TIMEOUT_45_SECONDS_INCONCLUSIVE'}
 rows.append(dict(label=name,cycle=ci,seconds=time.monotonic()-start,**status));(p/'SUZUKI_MIXED_BATCH_STATUS.json').write_text(json.dumps(rows,indent=2)+'\n');print(rows[-1],flush=True)
