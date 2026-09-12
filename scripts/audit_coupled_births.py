#!/usr/bin/env python3
"""Replay a coupled-birth archive; falsify movies using HFK; index a sample.

No match or passing check certifies a concordance. Numerical identifications
and same-library replay require independent verification for every positive hit.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import time
import snappy
from spherogram.links.bands.core import add_one_band
from coupled_births import replay_placement,diagram_signature
from filter_common_successors import dominates
from index_successors import signature
from audit_failed_identifications import factors


def run(archive,output,sample=128,timeout=3,seed=20260919):
    if Path(output).exists():raise FileExistsError(output)
    records=[json.loads(x) for x in gzip.open(archive,'rt')]
    header=records[0];assert header['type']=='header' and records[-1]['type']=='summary'
    placements={};first={};unique=[];replayed=0;relabeled=0
    for r in records[1:-1]:
        if r['type']=='placement':
            replay_placement(r)
            # Exact initial source diagram plus the two specified split circles.
            n=len(header['source_pd']);extra=[]
            for o in [2*n,2*n+4]:extra.extend([(o,o+1,o+1,o+2),(o+2,o+3,o+3,o)])
            split=snappy.Link([tuple(x) for x in header['source_pd']]+extra)
            assert split.PD_code()==[tuple(x) for x in r['split_pd']]
            placements[r['placement']]=r
        elif r['type']=='first':
            L=snappy.Link(placements[r['placement']]['birth_pd'])
            I=add_one_band(L,r['band'])
            assert len(L.link_components)==3 and len(I.link_components)==2
            assert I.PD_code()==[tuple(x) for x in r['raw_output_pd']]
            # Fusion from an algebraically split link preserves zero linking.
            assert I.linking_number()==0
            first[r['first_id']]=r
        elif r['type']=='move':
            I=snappy.Link(first[r['first_id']]['raw_output_pd']);J=add_one_band(I,r['band'])
            assert len(J.link_components)==1
            assert J.PD_code()==[tuple(x) for x in r['raw_output_pd']]
            J.simplify('basic')
            # RI/II simplification visits a set of crossing objects. Another
            # process can visit them in another order and relabel the diagram.
            if J.PD_code()!=[tuple(x) for x in r['endpoint_pd']]:
                relabeled+=1
                assert diagram_signature(J.PD_code())==r['diagram_signature'], ('simplification diagram differs',r['index'])
            replayed+=1
            if r['new_signature']:unique.append(r)
        else:raise ValueError(r['type'])
    # Include every distinct endpoint retained through an intermediate without
    # an immediately detected split unknot, plus two complementary samples.
    priority=[r for r in unique if not first[r['first_id']]['detected_split_unknot']]
    small=sorted(unique,key=lambda r:(r['crossings'],r['index']))[:sample]
    uniform=random.Random(seed).sample(unique,min(sample,len(unique)))
    chosen={r['index']:r for r in priority+small+uniform}
    names=['AbeTagami_K_0_K_-1__6_3','AbeTagami_K_1']
    source=[snappy.Link(json.loads(Path('data/knots/'+n+'.json').read_text())['pd_code_snappy_0indexed']).knot_floer_homology()['ranks'] for n in names]
    own=0 if 'K_0_' in header['card'] else 1
    required={g:max(h.get(g,0) for h in source) for g in set().union(*source)}
    result={'status':'COMPUTATIONAL_REPLAY_AND_NECESSARY_FILTER_NOT_A_CERTIFICATE',
            'archive':archive,'sha256':hashlib.sha256(Path(archive).read_bytes()).hexdigest(),
            'source_side':own,'replayed_moves':replayed,'simplified_pd_relabelings':relabeled,'unique_diagrams':len(unique),
            'first_bands':len(first),'first_without_detected_split_unknot':sum(not r['detected_split_unknot'] for r in first.values()),
            'priority_unique':len(priority),'selection':'all retained nontrivial-intermediate endpoints, smallest crossing sample, uniform sample',
            'sample':sample,'seed':seed,'hard_hfk_timeout':timeout,'checks':[],
            'limitations':'A retained representative may have a trivial intermediate even if another movie for that diagram does not. Samples are incomplete. HFK and replay share unverified software dependencies. Numerical and factor signatures only nominate matches.'}
    def save():Path(output).write_text(json.dumps(result,separators=(',',':'))+'\n')
    t0=time.monotonic()
    for r in sorted(chosen.values(),key=lambda r:(r['crossings'],r['index'])):
        c={k:r[k] for k in ['index','diagram_signature','first_id','crossings']}
        try:
            p=subprocess.run([sys.executable,str(Path(__file__).with_name('hfk_worker.py'))],input=json.dumps(r['endpoint_pd']),capture_output=True,text=True,timeout=timeout,check=True)
            h=json.loads(p.stdout);ranks={(a,m):n for a,m,n in h['ranks']}
            c.update(status='computed',hfk=h,own_source_injection_passed=dominates(ranks,source[own]),common_successor_not_excluded=dominates(ranks,required))
        except Exception as e:c.update(status='inconclusive',error=type(e).__name__+': '+str(e))
        # Do not throw away a timeout; it may still identify with another endpoint.
        if c.get('common_successor_not_excluded',True):
            c.update(signature(r['endpoint_pd']))
            if c['numerical_signature'] is None:
                c.update(factors(r['endpoint_pd'],seed+r['index']))
        result['checks'].append(c)
        if c.get('own_source_injection_passed') is False:
            result['invalid_movie_detected']=True;save();raise AssertionError('Source injection failed; stop search')
        if len(result['checks'])%64==0:
            save();print('checked',len(result['checks']),'of',len(chosen),'seconds',round(time.monotonic()-t0,1),flush=True)
    result['complete']=True
    result['summary']={'checked':len(chosen),'computed':sum(c['status']=='computed' for c in result['checks']),
        'common_passes':sum(c.get('common_successor_not_excluded',False) for c in result['checks']),
        'inconclusive':sum(c['status']=='inconclusive' for c in result['checks']),
        'source_failures':sum(c.get('own_source_injection_passed') is False for c in result['checks'])}
    save();print(json.dumps(result['summary']),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('archive');p.add_argument('output');p.add_argument('--sample',type=int,default=128)
    p.add_argument('--timeout',type=float,default=3);p.add_argument('--seed',type=int,default=20260919);a=p.parse_args()
    run(a.archive,a.output,a.sample,a.timeout,a.seed)
