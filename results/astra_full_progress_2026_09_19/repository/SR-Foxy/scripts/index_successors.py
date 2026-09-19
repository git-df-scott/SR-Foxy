#!/usr/bin/env python3
"""Cache a numerical peripheral index, or compare a two-birth manifest to it."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import snappy
from filter_common_successors import read_unique


def signature(pd):
    try:
        sig=snappy.Link(pd).exterior().isometry_signature(of_link=True,ignore_orientation=False)
        if sig is None:raise ValueError('No numerical signature')
        return {'numerical_signature':sig}
    except Exception as e:return {'numerical_signature':None,'error':type(e).__name__+': '+str(e)}


def index(archive,filtered,output):
    if Path(output).exists():raise FileExistsError(output)
    checks=json.loads(Path(filtered).read_text())['sides'][1]['checks']
    wanted={r['index'] for r in checks if r.get('common_successor_not_excluded')}
    result={'status':'NUMERICAL_INDEX_NOT_CERTIFIED_IDENTIFICATION','archive':archive,
            'archive_sha256':hashlib.sha256(Path(archive).read_bytes()).hexdigest(),
            'filter':filtered,'filter_side':1,'snappy':snappy.__version__,'entries':[]}
    for r in read_unique(archive):
        if r['index'] not in wanted:continue
        result['entries'].append(dict(index=r['index'],diagram_signature=r['diagram_signature'],**signature(r['endpoint_pd'])))
        if len(result['entries'])%128==0:
            Path(output).write_text(json.dumps(result,indent=2)+'\n')
            print('indexed',len(result['entries']),flush=True)
    result['complete']=True;result['failed']=sum(r['numerical_signature'] is None for r in result['entries'])
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print('complete',len(result['entries']),'failed',result['failed'],flush=True)


def compare(manifest,index_path,output):
    if Path(output).exists():raise FileExistsError(output)
    idx=json.loads(Path(index_path).read_text());assert idx.get('complete')
    exact=defaultdict(list);numerical=defaultdict(list)
    for r in idx['entries']:
        exact[r['diagram_signature']].append(r['index'])
        if r['numerical_signature']:numerical[r['numerical_signature']].append(r['index'])
    result={'status':'NUMERICAL_SCREEN_NOT_A_CONCORDANCE_CERTIFICATE','manifest':manifest,'index':index_path,
            'checks':[],'diagram_matches':[],'numerical_matches':[],
            'limitations':'Each hit still needs certified peripheral identification and both oriented movie audits. Failed or unsampled cases remain unresolved.'}
    for parent in json.loads(Path(manifest).read_text())['parents']:
        for r in parent['survivors']:
            row=dict(parent_index=parent['parent_index'],index=r['index'],**signature(r['endpoint_pd']))
            result['checks'].append(row)
            if r['diagram_signature'] in exact:result['diagram_matches'].append(dict(row,right=exact[r['diagram_signature']]))
            if row['numerical_signature'] in numerical:result['numerical_matches'].append(dict(row,right=numerical[row['numerical_signature']]))
    result['failed']=sum(r['numerical_signature'] is None for r in result['checks'])
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:len(result[k]) for k in ['checks','diagram_matches','numerical_matches']}),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='mode',required=True)
    a=s.add_parser('index');a.add_argument('archive');a.add_argument('filtered');a.add_argument('output')
    a=s.add_parser('compare');a.add_argument('manifest');a.add_argument('index');a.add_argument('output')
    a=p.parse_args()
    if a.mode=='index':index(a.archive,a.filtered,a.output)
    else:compare(a.manifest,a.index,a.output)
