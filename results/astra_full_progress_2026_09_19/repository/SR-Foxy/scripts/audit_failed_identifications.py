#!/usr/bin/env python3
"""Try diagram-visible connected-sum factors in failed numerical identifications.

Canonical factor signatures nominate matches; they do not certify orientation,
prime decomposition or a slice movie. All unrecognised factors remain open.
"""
from collections import defaultdict
import json
from pathlib import Path
import random
import snappy
from fusion_successors import diagram_signature
from filter_common_successors import read_unique


def factors(pd,seed):
    random.seed(seed);L=snappy.Link(pd);L.simplify('global')
    result=[]
    for P in L.deconnect_sum():
        P.simplify('global');pd=P.PD_code()
        ds=diagram_signature(pd);row={'pd':pd,'diagram_signature':ds,'crossings':len(pd)}
        try:
            sig=P.exterior().isometry_signature(of_link=True,ignore_orientation=False)
            if not sig:raise ValueError('no signature')
            row['numerical_signature']=sig;row['key']='HYP:'+sig
        except Exception as e:
            row['numerical_signature']=None;row['error']=str(e);row['key']='PD:'+ds
        result.append(row)
    return {'factors':result,'factor_key':sorted(r['key'] for r in result)}


def run(output):
    if Path(output).exists():raise FileExistsError(output)
    index=json.loads(Path('results/AT1_successor_index.json').read_text())
    right_ids={r['index'] for r in index['entries'] if r['numerical_signature'] is None}
    right=[r for r in read_unique(index['archive']) if r['index'] in right_ids]
    comp=json.loads(Path('results/two_birth_comparison.json').read_text())
    left_ids={(r['parent_index'],r['index']) for r in comp['checks'] if r['numerical_signature'] is None}
    left=[dict(r,parent_index=p['parent_index']) for p in json.loads(Path(comp['manifest']).read_text())['parents']
          for r in p['survivors'] if (p['parent_index'],r['index']) in left_ids]
    out={'status':'STRUCTURAL_MATCH_NOMINATION_ONLY','seed':20260915,'left':[],'right':[],'matches':[],
         'limitations':'Only decomposition visible after bounded diagram simplification. Failed recognition is unresolved; no nonconcordance conclusion.'}
    for side,records in [('left',left),('right',right)]:
        for j,r in enumerate(records):
            row={'index':r['index'],'parent_index':r.get('parent_index'),'endpoint_pd':r['endpoint_pd'],**factors(r['endpoint_pd'],20260915+j)}
            out[side].append(row)
        print(side,len(records),'split',sum(len(r['factors'])>1 for r in out[side]),flush=True)
    lookup=defaultdict(list)
    for r in out['right']:lookup[tuple(r['factor_key'])].append(r['index'])
    for r in out['left']:
        if tuple(r['factor_key']) in lookup:out['matches'].append({'left_parent':r['parent_index'],'left_index':r['index'],'right_indices':lookup[tuple(r['factor_key'])]})
    Path(output).write_text(json.dumps(out,separators=(',',':'))+'\n')
    print('matches',out['matches'],flush=True)


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('output');run(p.parse_args().output)
