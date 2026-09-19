#!/usr/bin/env python3
"""Exact finite-cover homology refinement of surviving checkpoint pairs.

Enumeration methods low_index and snappea are compared independently.
Homology still uses SnapPy's integer triangulation routines; this is a
computer-assisted finite exclusion, not a formal proof of its implementation.
"""
from pathlib import Path
import json,sqlite3,zlib,time,collections,multiprocessing as mp
import snappy  # Imported once before fork; child computations remain bounded.
B=Path(__file__).resolve().parent

def work(pd,degree,send):
 try:
  import snappy
  from spherogram import Link
  M=Link(pd).exterior();out={}
  for method in ['low_index','snappea']:
   covers=M.covers(degree,method=method)
   out[method]=sorted([list(N.homology().elementary_divisors()) for N in covers])
  if out['low_index']!=out['snappea']:raise ValueError('Enumeration disagreement')
  send.send({'status':'EXACT_ENUMERATORS_AGREE','profile':out['low_index']})
 except BaseException as e:send.send({'status':'UNKNOWN','error':repr(e)})
 finally:send.close()

def main():
 db=sqlite3.connect(f'file:{B}/checkpoint/evidence.sqlite?mode=ro',uri=True)
 homfly=json.loads((B/'collisions/HOMFLY_AUDIT.json').read_text())['buckets']
 cyclic=json.loads((B/'collisions/CYCLIC_COVER_AUDIT.json').read_text())
 profiles={r['node']:r['profiles']['4'] for r in cyclic['nodes']}
 groups=[]
 for bucket in homfly:
  if not bucket['shared_homfly']:continue
  sides=[]
  for side in ['left_nodes','right_nodes']:
   d=collections.defaultdict(list)
   for n in bucket[side]:d[tuple(profiles[n])].append(n)
   sides.append(d)
  for profile in sides[0].keys()&sides[1].keys():
   groups.append({'bucket':bucket['bucket'],'representatives':[{'nodes_in_same_homology_class':d[profile]} for d in sides]})
 ids=sorted(set(n for g in groups for s in g['representatives'] for n in s['nodes_in_same_homology_class']))
 start=time.monotonic();result={};path=B/'collisions/cover4_profiles.jsonl'
 
 if path.exists():
  for line in path.read_text().splitlines():
   r=json.loads(line);result[r['node']]=r
 with path.open('a') as out:
  for n in ids:
   if n in result:continue
   pd=json.loads(zlib.decompress(db.execute('select payload from nodes where id=?',(n,)).fetchone()[0]))['state']['pd']
   a,b=mp.Pipe(duplex=False);p=mp.Process(target=work,args=(pd,4,b));t=time.monotonic();p.start();b.close()
   row={'node':n,'degree':4}
   if a.poll(8):
    try:row.update(a.recv())
    except EOFError:row.update(status='UNKNOWN',error='child process failed')
   else:row.update(status='UNKNOWN_TIMEOUT',limit_seconds=8)
   p.join(.2)
   if p.is_alive():p.kill();p.join()
   a.close();row['seconds']=time.monotonic()-t;result[n]=row;out.write(json.dumps(row)+'\n');out.flush()
 outcome={'counterexample_established':False,'last_invocation_seconds':time.monotonic()-start,'sum_recorded_per_node_wall_seconds':sum(r['seconds'] for r in result.values()),'runtime_note':'Resumable postprocessing. Per-node records include completed child computations; last_invocation_seconds is not total elapsed time if resumed.','checked_nodes':len(result),'groups':[]}
 for g in groups:
  ds=[];unknown=[]
  for side in g['representatives']:
   d=collections.defaultdict(list)
   for n in side['nodes_in_same_homology_class']:
    if 'profile' not in result[n]:unknown.append(n)
    else:d[json.dumps(result[n]['profile'])].append(n)
   ds.append(d)
  shared=ds[0].keys()&ds[1].keys()
  outcome['groups'].append({'bucket':g['bucket'],'classes_by_side':[{k:v for k,v in d.items()} for d in ds],'shared_classes':len(shared),'unresolved_pairs':[{'profile':json.loads(k),'left_nodes':ds[0][k],'right_nodes':ds[1][k]} for k in shared],'unknown':unknown})
 outcome['all_resolved']=all(not g['shared_classes'] and not g['unknown'] for g in outcome['groups'])
 (B/'collisions/FULL_COVER_AUDIT.json').write_text(json.dumps(outcome,indent=2)+'\n')
 print(json.dumps({**outcome,'groups':[{k:v for k,v in g.items() if k!='classes_by_side'} for g in outcome['groups']]},indent=2))
if __name__=='__main__':main()
