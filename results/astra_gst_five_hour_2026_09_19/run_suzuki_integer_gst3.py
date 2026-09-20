from pathlib import Path
import sys,subprocess,json
p=Path(__file__).parent;rows=[]
for ci in [0,1]:
 out=p/'suzuki_mixed'/f'GST3_c{ci}'
 with (out/'integer_taylor.log').open('w') as f:
  try:r=subprocess.run([sys.executable,str(p/'check_suzuki_taylor_integer.py'),'GST3',str(ci)],stdout=f,stderr=subprocess.STDOUT,timeout=60);s={'exit_code':r.returncode}
  except subprocess.TimeoutExpired:s={'status':'TIMEOUT_60_SECONDS_INCONCLUSIVE'}
 rows.append(dict(cycle=ci,**s));(p/'SUZUKI_INTEGER_GST3_STATUS.json').write_text(json.dumps(rows,indent=2)+'\n');print(rows[-1],flush=True)
