#!/usr/bin/env python3
"""Refine the exact Jones collision classes without changing the search.
Full HOMFLY-PT is compared exactly. Equality is never used as identification.
"""
from pathlib import Path
import sqlite3,json,zlib,sys,time,collections,regina,signal
BASE=Path(__file__).resolve().parent
p=BASE/'checkpoint';db=sqlite3.connect(f'file:{p}/evidence.sqlite?mode=ro',uri=True)
buckets=json.loads((BASE/'jones/JONES_AUDIT.json').read_text())['targets']['wild17']['shared']
out=BASE/'collisions';out.mkdir(exist_ok=True)
res={};start=time.monotonic()
def timeout(*args): raise TimeoutError('per-polynomial bound 5 seconds')
signal.signal(signal.SIGALRM,timeout)
with (out/'homfly.jsonl').open('x') as f:
 for n in sorted(set(n for s in buckets for side in ['left_nodes','right_nodes'] for n in s[side])):
  pd=json.loads(zlib.decompress(db.execute('select payload from nodes where id=?',(n,)).fetchone()[0]))['state']['pd']
  row={'node':n,'crossings':len(pd)};a=time.monotonic()
  try:
   signal.setitimer(signal.ITIMER_REAL,5)
   R=regina.Link.fromPD([[v+1 for v in r] for r in pd]);row['homfly_az']=str(R.homflyAZ());row['status']='EXACT'
  except Exception as e:row['status']='UNKNOWN';row['error']=repr(e)
  finally:signal.setitimer(signal.ITIMER_REAL,0)
  row['seconds']=time.monotonic()-a;res[n]=row;f.write(json.dumps(row)+'\n');f.flush()
result={'counterexample_established':False,'seconds':time.monotonic()-start,'buckets':[]}
for i,b in enumerate(buckets):
 sets=[{res[n].get('homfly_az') for n in b[side]} for side in ['left_nodes','right_nodes']]
 shared=sets[0]&sets[1]-{None}
 result['buckets'].append({'bucket':i,'left_nodes':b['left_nodes'],'right_nodes':b['right_nodes'],'distinct_homfly_counts':[len(x-{None}) for x in sets],'shared_homfly':sorted(shared),'unknown':[n for side in ['left_nodes','right_nodes'] for n in b[side] if res[n]['status']=='UNKNOWN'],'claim':'No opposite-side identification is possible if shared_homfly and unknown are both empty.'})
(out/'HOMFLY_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
