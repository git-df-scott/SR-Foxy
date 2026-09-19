#!/usr/bin/env python3
"""Read-only ledger and deterministic native movie replay audit.
Native replay is explicitly NOT an independent implementation.
"""
from pathlib import Path
import sqlite3,importlib.util,json,zlib,hashlib,random,time,collections
B=Path(__file__).resolve().parent
out={'status':'PASS','counterexample_established':False,'snapshots':[]}
for base in [B,B/'snapshot2']:
 p=base/'checkpoint';db=sqlite3.connect(f'file:{p}/evidence.sqlite?mode=ro',uri=True)
 if db.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise ValueError('SQLite integrity')
 control=json.loads((p/'CONTROLS.json').read_text())
 for name,h in control['source_sha256'].items():
  if hashlib.sha256((p/'source'/name).read_bytes()).hexdigest()!=h:raise ValueError('Source hash mismatch')
 rows={row[0]:row for row in db.execute('SELECT id,phase,target,side,depth,deaths,parent,payload FROM nodes')}
 for ident,phase,target,side,depth,deaths,parent,payload in rows.values():
  if parent is None:
   if depth!=0 or deaths!=0:raise ValueError('Root topology ledger')
  else:
   old=rows[parent];step=json.loads(zlib.decompress(payload))['step']
   if parent>=ident or (phase,target,side)!=old[1:4] or depth!=old[4]+1 or deaths!=old[5]+step['deaths']:raise ValueError('Parent-chain ledger')
   if phase=='common_upper' and (step['kind']!='birth_fusion' or step['deaths']!=0):raise ValueError('Common upper topology ledger')
 spec=importlib.util.spec_from_file_location('checkpoint_native_runner',p/'source/runner.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
 ids=sorted(i for i,row in rows.items() if row[6] is not None);selected=random.Random(19519).sample(ids,200);start=time.monotonic()
 for ident in selected:r.path_to(db,ident)
 agg=collections.Counter();run_rows=[]
 for phase,segment,status,seconds,cpu,summary in db.execute('select phase,segment,status,seconds,cpu_seconds,summary from runs order by id'):
  counts=json.loads(summary);agg.update(counts);run_rows.append(dict(phase=phase,segment=segment,status=status,seconds=seconds,cpu_seconds=cpu,counts=counts))
 if agg['NEW_ENDPOINT']!=len(ids):raise ValueError('Endpoint counts inconsistent with ledger')
 if agg['attempts']!=sum(v for k,v in agg.items() if k!='attempts'):raise ValueError('Attempt outcomes do not partition attempts')
 out['snapshots'].append({'directory':str(base.relative_to(B)),'database_sha256':hashlib.sha256((p/'evidence.sqlite').read_bytes()).hexdigest(),'source_hashes_match':True,'sqlite_integrity':'ok','all_parent_ledgers_valid':True,'stored_nodes':len(rows),'new_endpoint_nodes':len(ids),'run_rows':run_rows,'aggregate_counts':dict(agg),'sampled_complete_chains':selected,'native_replay_count':len(selected),'native_replay_seconds':time.monotonic()-start,'native_replay_is_independent':False})
(B/'LEDGER_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({**out,'snapshots':[{k:v for k,v in a.items() if k!='sampled_complete_chains'} for a in out['snapshots']]},indent=2))
