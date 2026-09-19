#!/usr/bin/env python3
"""Exact, mirror-sensitive Jones comparison of EVERY stored endpoint.

Read-only GitHub checkpoint input. Creates separate audit evidence; never
changes the search or its endpoint records. Jones equality is necessary,
not sufficient, for identification. An empty cross-side intersection is a
finite exclusion for this downloaded checkpoint, not for its search box.
"""
from pathlib import Path
import argparse,collections,hashlib,json,sqlite3,time,zlib,sys
import regina

def jones_key(pd):
    R=regina.Link.fromPD([[int(v)+1 for v in row] for row in pd])
    if R.countComponents()!=1: raise ValueError('Expected a knot')
    p=R.jones()
    return [int(p.minExp()),[int(str(p[i])) for i in range(p.minExp(),p.maxExp()+1)]]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('checkpoint',type=Path);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    a.out.mkdir(parents=True,exist_ok=True)
    db=sqlite3.connect(f'file:{a.checkpoint}/evidence.sqlite?mode=ro',uri=True)
    if db.execute('PRAGMA integrity_check').fetchone()[0]!='ok': raise ValueError('Corrupt SQLite')
    start=time.monotonic();group=collections.defaultdict(lambda:collections.defaultdict(list));counts=collections.Counter();signatures=collections.defaultdict(lambda:collections.defaultdict(list))
    checkpoint_hash=hashlib.sha256((a.checkpoint/'evidence.sqlite').read_bytes()).hexdigest()
    with (a.out/'endpoint_jones.jsonl').open('x') as out:
        for ident,phase,target,side,depth,crossings,sig,payload in db.execute('SELECT id,phase,target,side,depth,crossings,sig,payload FROM nodes ORDER BY id'):
            obj=json.loads(zlib.decompress(payload));key=jones_key(obj['state']['pd']);s=json.dumps(key,separators=(',',':'))
            group[target][side,s].append(ident);signatures[target][side,sig].append(ident);counts[target,side]+=1
            out.write(json.dumps({'node':ident,'target':target,'side':side,'depth':depth,'crossings':crossings,'jones_min_and_coefficients':key},separators=(',',':'))+'\n')
            if ident%2000==0:print('processed',ident,'elapsed',time.monotonic()-start,flush=True)
    result={'status':'EXACT_FINITE_CHECKPOINT_AUDIT','counterexample_established':False,'input_database_sha256':checkpoint_hash,'regina_version':regina.versionString(),'targets':{},'seconds':time.monotonic()-start}
    for target,data in group.items():
        sets=[{k for s,k in data if s==side} for side in [0,1]];shared=sets[0]&sets[1]
        sigs=[{k for s,k in signatures[target] if s==side} for side in [0,1]]
        result['targets'][target]={'node_counts':[counts[target,s] for s in [0,1]],'distinct_jones_counts':[len(s) for s in sets],'shared_jones_classes':len(shared),'shared_saved_diagram_signatures':len(sigs[0]&sigs[1]),'shared':[{'jones':json.loads(k),'left_nodes':data[0,k],'right_nodes':data[1,k]} for k in sorted(shared)],'claim':'Empty shared Jones set certifies no two opposite-side STORED endpoints are isotopic. Nonempty sets require further exact tests. No statement about unstored or unsearched endpoints.'}
    (a.out/'JONES_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({**result,'targets':{k:{x:v for x,v in d.items() if x!='shared'} for k,d in result['targets'].items()}},indent=2))
if __name__=='__main__':main()
