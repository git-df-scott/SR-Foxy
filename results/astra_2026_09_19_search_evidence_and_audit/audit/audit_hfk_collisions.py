#!/usr/bin/env python3
"""Exact graded HFK comparison on remaining checkpoint collision groups.
Runs each compiled-library computation in a process with a real wall timeout.
"""
from pathlib import Path
import json,sqlite3,zlib,multiprocessing as mp,time
BASE=Path(__file__).resolve().parent

def work(pd,send):
 try:
  from spherogram import Link
  h=Link(pd).knot_floer_homology()
  h['ranks']=[list(k)+[v] for k,v in sorted(h['ranks'].items())]
  send.send({'status':'EXACT_COMPUTATION','hfk':h})
 except BaseException as e:send.send({'status':'UNKNOWN','error':repr(e)})
 finally:send.close()

def main():
 inp=json.loads((BASE/'collisions/HOMFLY_AUDIT.json').read_text());groups=[b for b in inp['buckets'] if b['shared_homfly']]
 db=sqlite3.connect(f'file:{BASE}/checkpoint/evidence.sqlite?mode=ro',uri=True)
 results={};start=time.monotonic()
 with (BASE/'collisions/hfk.jsonl').open('x') as out:
  for n in sorted(set(n for b in groups for side in ['left_nodes','right_nodes'] for n in b[side])):
   pd=json.loads(zlib.decompress(db.execute('select payload from nodes where id=?',(n,)).fetchone()[0]))['state']['pd']
   a,b=mp.Pipe(duplex=False);proc=mp.Process(target=work,args=(pd,b));t=time.monotonic();proc.start();b.close()
   row={'node':n,'crossings':len(pd)}
   if a.poll(8):
    try:row.update(a.recv())
    except EOFError:row.update(status='UNKNOWN',error='child closed without result')
   else:row.update(status='UNKNOWN_TIMEOUT',seconds_limit=8)
   proc.join(0.2)
   if proc.is_alive():proc.kill();proc.join()
   a.close();row['seconds']=time.monotonic()-t;results[n]=row;out.write(json.dumps(row)+'\n');out.flush()
 print('nodes',len(results),'seconds',time.monotonic()-start)
 result={'counterexample_established':False,'seconds':time.monotonic()-start,'groups':[]}
 for group in groups:
  ds=[]
  for side in ['left_nodes','right_nodes']:
   dic={}
   for n in group[side]:
    h=results[n].get('hfk')
    if h:dic.setdefault(json.dumps(h['ranks']),[]).append(n)
   ds.append(dic)
  shared=ds[0].keys()&ds[1].keys()
  result['groups'].append({'bucket':group['bucket'],'hfk_classes_by_side':[{k:v for k,v in d.items()} for d in ds],'shared_full_hfk_classes':len(shared),'unresolved_pairs':[{'ranks':json.loads(k),'left_nodes':ds[0][k],'right_nodes':ds[1][k]} for k in shared],'unknown':[n for side in ['left_nodes','right_nodes'] for n in group[side] if 'hfk' not in results[n]]})
 (BASE/'collisions/HFK_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
