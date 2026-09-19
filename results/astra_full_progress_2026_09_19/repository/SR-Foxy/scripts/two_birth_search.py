#!/usr/bin/env python3
"""Bounded second birth+fusion, preserving both parent and child witnesses.

Deliberately include a first-stage target failing common HFK domination:
only final targets, not intermediate vertices, must pass that test.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import snappy
from fusion_successors import search,replay,pd_hash,diagram_signature
from filter_common_successors import read_unique,dominates,rows


def run(output_dir,moves=2000,sample=64,seed=20260914):
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    selected=[];seen=set()
    for r in json.loads(Path('results/fusion_AT0_wider_targets.json').read_text())['candidates']:
        key=r.get('numerical_isometry_signature') or r['diagram_signature']
        if not r['hfk_check']['fibered'] and key not in seen:
            selected.append(r);seen.add(key)
        if len(selected)==3:break
    selected.append(next(r for r in read_unique('results/fusion_AT0_wider.jsonl.gz') if r['index']==21))
    sources=[snappy.Link(json.loads(Path('data/knots/'+name+'.json').read_text())['pd_code_snappy_0indexed']).knot_floer_homology()
             for name in ['AbeTagami_K_0_K_-1__6_3','AbeTagami_K_1']]
    required={}
    for h in sources:
        for grade,n in h['ranks'].items():required[grade]=max(n,required.get(grade,0))
    result={'status':'BOUNDED_TWO_BIRTH_EXPERIMENT_NOT_A_SLICE_CERTIFICATE','seed':seed,
            'moves_per_parent':moves,'hfk_sample_per_parent':sample,'parents':[],
            'hfk_backend':'knot_floer_homology.pd_to_hfk, direct PD input',
            'hard_timeout_seconds':5,
            'limitations':'Parents selected using numerical coalescing only for prioritization. Each movie uses two births and two fusions. Simplification and endpoint identification still need independent audits for any hit.'}
    for pno,parent in enumerate(selected):
        assert replay(parent)
        pd=parent['endpoint_pd'];parent_hfk=snappy.Link(pd).knot_floer_homology()
        raw=out/f'parent_{parent["index"]}.jsonl'
        summary=search(pd,raw,max_length=9,max_twists=3,max_moves=moves,seconds=90,
                       detours=16,seed=seed+pno,per_face_moves=100)
        candidates=read_unique(raw)
        if sample and len(candidates)>sample:candidates=random.Random(seed+pno).sample(candidates,sample)
        checks=[];survivors=[]
        for r in candidates:
            c={'index':r['index'],'diagram_signature':r['diagram_signature'],'crossings':r['crossings']}
            try:
                # SIGALRM cannot reliably interrupt the calculator's C code.
                # Use an isolated process so a timeout really ends this case.
                worker=subprocess.run([sys.executable,str(Path(__file__).with_name('hfk_worker.py'))],
                                      input=json.dumps(r['endpoint_pd']),capture_output=True,text=True,timeout=5,check=True)
                h=json.loads(worker.stdout);h['ranks']={(a,m):n for a,m,n in h['ranks']}
                c.update({'status':'computed','ranks':rows(h['ranks']),'total_rank':h['total_rank'],
                          'fibered':h['fibered'],'genus':h['seifert_genus'],
                          'parent_injection_passed':dominates(h['ranks'],parent_hfk['ranks']),
                          'K0_injection_passed':dominates(h['ranks'],sources[0]['ranks']),
                          'common_successor_not_excluded':dominates(h['ranks'],required)})
                if c['common_successor_not_excluded']:
                    survivors.append(dict(r,hfk_check=c,parent_index=parent['index']))
            except Exception as e:
                c.update(status='inconclusive',error=type(e).__name__+': '+str(e))
            checks.append(c)
            if c.get('status')=='computed':assert c['parent_injection_passed'] and c['K0_injection_passed']
        data=raw.read_bytes();compressed=gzip.compress(data,mtime=0)
        archive=Path(str(raw)+'.gz');archive.write_bytes(compressed)
        # Remove only this run's intermediate after checking lossless compression.
        assert gzip.decompress(archive.read_bytes())==data
        raw.unlink()
        entry={'parent_index':parent['index'],'parent_witness':parent,'parent_hfk_ranks':rows(parent_hfk['ranks']),
               'parent_common_pass':dominates(parent_hfk['ranks'],required),
               'source_pd_sha256':pd_hash(pd),'archive':str(archive),
               'sha256':hashlib.sha256(compressed).hexdigest(),'uncompressed_sha256':hashlib.sha256(data).hexdigest(),
               'generation':summary,'hfk_checks':checks,'survivors':survivors}
        result['parents'].append(entry)
        (out/'manifest.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({'parent':parent['index'],'moves':summary['moves'],'unique':summary['unique_diagrams'],
                          'checked':len(checks),'inconclusive':sum(c['status']!='computed' for c in checks),'survivors':len(survivors)}),flush=True)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output_dir');p.add_argument('--moves',type=int,default=2000)
    p.add_argument('--sample',type=int,default=64);p.add_argument('--seed',type=int,default=20260914)
    a=p.parse_args();run(a.output_dir,a.moves,a.sample,a.seed)
