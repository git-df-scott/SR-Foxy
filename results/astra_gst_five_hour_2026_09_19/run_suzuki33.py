from pathlib import Path
import subprocess,sys,json
p=Path(__file__).parent;name=sys.argv[1];rows=[];out=p/'suzuki33'/name;out.mkdir(parents=True,exist_ok=True)
for total in range(2,7):
 for a in range(4):
  b=total-a
  if not 0<=b<=3:continue
  d=out/f'{a}{b}';d.mkdir(exist_ok=True)
  with (d/'run.log').open('w') as f:
   try:r=subprocess.run([sys.executable,str(p/'suzuki33_term.py'),name,str(a),str(b)],stdout=f,stderr=subprocess.STDOUT,timeout=20);s={'exit_code':r.returncode}
   except subprocess.TimeoutExpired:s={'status':'TIMEOUT_20_SECONDS_INCONCLUSIVE'}
  rows.append(dict(a=a,b=b,**s));(out/'STATUS.json').write_text(json.dumps(rows,indent=2)+'\n');print(rows[-1],flush=True)
