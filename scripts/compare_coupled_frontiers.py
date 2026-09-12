#!/usr/bin/env python3
"""Compare cached old/new endpoints; retain undecided HFK cases."""
from collections import defaultdict
import hashlib
import json
from pathlib import Path


def run(output,include_returns=False):
    if Path(output).exists():raise FileExistsError(output)
    inputs={};sides=[[],[]]
    def read(path):
        inputs[path]=hashlib.sha256(Path(path).read_bytes()).hexdigest()
        return json.loads(Path(path).read_text())
    for c in read('results/fusion_AT0_wider_targets.json')['candidates']:
        sides[0].append({'origin':'K0_wider','index':c['index'],'diagram_signature':c['diagram_signature'],'numerical_signature':c['numerical_isometry_signature']})
    old=read('results/two_birth_comparison.json')
    manifest=read(old['manifest'])
    old_sigs={(p['parent_index'],r['index']):r['diagram_signature'] for p in manifest['parents'] for r in p['survivors']}
    for c in old['checks']:
        sides[0].append(dict(c,origin='K0_sequential',diagram_signature=old_sigs[c['parent_index'],c['index']]))
    for c in read('results/AT1_successor_index.json')['entries']:sides[1].append(dict(c,origin='K1_previous'))
    structural=read('results/resumed_failed_identifications.json')
    for side,key in enumerate(['left','right']):
        lookup={(r.get('parent_index'),r['index']):r['factor_key'] for r in structural[key]}
        for c in sides[side]:
            if (c.get('parent_index'),c['index']) in lookup:c['factor_key']=lookup[c.get('parent_index'),c['index']]
    for side in [0,1]:
        d=read(f'results/coupled_K{side}_batch1_audit.json');assert d['complete']
        for c in d['checks']:
            if c.get('common_successor_not_excluded',True):sides[side].append(dict(c,origin=f'K{side}_coupled'))
    if include_returns:
        for side in [0,1]:
            d=read(f'results/coupled_K{side}_double_return_audit.json');assert d['complete']
            for c in d['checks']:
                if c.get('common_successor_not_excluded',True):sides[side].append(dict(c,origin=f'K{side}_returns'))
    result={'status':'MATCH_NOMINATIONS_ONLY','inputs_sha256':inputs,'counts':[len(s) for s in sides],
            'matches':[],'sides':sides,'limitations':'Finite sampled frontiers; canonical diagram, numerical peripheral, and factor matches all need oriented geometric verification. HFK timeouts remain unknown.'}
    for kind in ['diagram_signature','numerical_signature','factor_key']:
        lookup=defaultdict(list)
        for c in sides[1]:
            key=c.get(kind)
            if key:lookup[tuple(key) if isinstance(key,list) else key].append({'origin':c['origin'],'index':c['index']})
        for c in sides[0]:
            key=c.get(kind);key=tuple(key) if isinstance(key,list) else key
            if key and key in lookup:result['matches'].append({'kind':kind,'left':{'origin':c['origin'],'index':c['index'],'parent_index':c.get('parent_index')},'right':lookup[key]})
    Path(output).write_text(json.dumps(result,separators=(',',':'))+'\n')
    print(json.dumps({'counts':result['counts'],'matches':result['matches']}))


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('output');p.add_argument('--include-returns',action='store_true');a=p.parse_args();run(a.output,a.include_returns)
