from pathlib import Path
import subprocess, shutil, json, time, sys
base=Path('/mnt/data/full_work_package')
source=base/'SR-Foxy/results/sr_foxy_combined_saved_work_2026_09_19'
work=Path('/mnt/data/handoff_check_workspace')
work.mkdir(exist_ok=True)
out=base/'verification/replays'; out.mkdir(parents=True,exist_ok=True)
results=[]
for label, dirname, command, timeout in [
 ('one_commutator','02_one_commutator',['node','check_independent.mjs'],15),
 ('genus_one_mesh','03_explicit_genus_one',[sys.executable,'check_mesh_independent.py'],15),
 ('genus_one_subgroup','03_explicit_genus_one',[sys.executable,'check_subgroup_independent.py'],15),
]:
 target=work/dirname
 if not target.exists(): shutil.copytree(source/dirname,target)
 started=time.monotonic()
 try:
  r=subprocess.run(command,cwd=target,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
  (out/(label+'.stdout.log')).write_bytes(r.stdout); (out/(label+'.stderr.log')).write_bytes(r.stderr)
  row={'check':label,'command':command,'exit_code':r.returncode,'status':'PASS' if r.returncode==0 else 'FAIL','seconds':time.monotonic()-started}
 except subprocess.TimeoutExpired as e:
  (out/(label+'.stdout.log')).write_bytes(e.stdout or b'');(out/(label+'.stderr.log')).write_bytes(e.stderr or b'')
  row={'check':label,'command':command,'status':'TIMEOUT_UNKNOWN','timeout_seconds':timeout,'seconds':time.monotonic()-started}
 results.append(row); print(json.dumps(row),flush=True)
(out/'EXECUTED_CHECKS.json').write_text(json.dumps(results,indent=2)+'\n')
