#!/usr/bin/env python3
from pathlib import Path
import sys,sqlite3,json,zlib,time,collections
from cyclic_cover_integer import calculate
import snappy
from spherogram import Link
B=Path(__file__).resolve().parent
p=B/'checkpoint';db=sqlite3.connect(f'file:{p}/evidence.sqlite?mode=ro',uri=True)
groups=[g for g in json.loads((B/'collisions/HOMFLY_AUDIT.json').read_text())['buckets'] if g['shared_homfly']]
start=time.monotonic();records={};checks=[]
for name in ['3_1','4_1','6_1','6_3']:
 L=Link(name)
 for degree in [2,3,4]:
  ours=calculate([list(r) for r in L.PD_code()],degree)['h1_elementary_divisors']
  covers=L.exterior().covers(degree,cover_type='cyclic')
  if len(covers)!=1:raise ValueError('Expected unique connected cyclic cover')
  actual=list(covers[0].homology().elementary_divisors())
  if ours!=actual:raise ValueError((name,degree,ours,actual))
  checks.append({'control':name,'degree':degree,'h1':ours,'cross_check':'SnapPea cyclic cover and triangulation homology'})
for n in sorted(set(n for g in groups for side in ['left_nodes','right_nodes'] for n in g[side])):
 pd=json.loads(zlib.decompress(db.execute('select payload from nodes where id=?',(n,)).fetchone()[0]))['state']['pd']
 fields={degree:calculate(pd,degree)['h1_elementary_divisors'] for degree in [2,3,4]}
 M=Link(pd).exterior();native=list(M.covers(4,cover_type='cyclic')[0].homology().elementary_divisors())
 if fields[4]!=native:raise ValueError((n,fields[4],native))
 records[n]={'node':n,'profiles':fields,'native_degree4':native,'matched':True}
 print(n,fields,flush=True)
result={'status':'ALL_REMAINING_OPPOSITE_SIDE_CHECKPOINT_ENDPOINTS_SEPARATED','counterexample_established':False,'seconds':time.monotonic()-start,'controls':checks,'nodes':list(records.values()),'buckets':[]}
for g in groups:
 sets=[{tuple(records[n]['profiles'][4]) for n in g[side]} for side in ['left_nodes','right_nodes']]
 if sets[0]&sets[1]:result['status']='SOME_ENDPOINT_PAIRS_REMAIN_UNRESOLVED'
 result['buckets'].append({'bucket':g['bucket'],'counts':[len(g[s]) for s in ['left_nodes','right_nodes']],'profiles_by_side':[[list(k) for k in sorted(s)] for s in sets],'shared_profiles':bool(sets[0]&sets[1]),'shared':[list(k) for k in sorted(sets[0]&sets[1])]})
(B/'collisions/CYCLIC_COVER_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['nodes','controls']},indent=2))
