#!/usr/bin/env python3
"""Seeded diagram diversification with stored intermediates and numerical control."""
import argparse
import json
from pathlib import Path
import random
import time
import snappy
from fusion_successors import diagram_signature


def run(card,output,iterations=150,seconds=90,seed=20260915):
    if Path(output).exists():raise FileExistsError(output)
    data=json.loads(Path(card).read_text());pd=data['pd_code_snappy_0indexed'];K=snappy.Link(pd)
    original_sig=K.exterior().isometry_signature(of_link=True,ignore_orientation=False)
    best=K.copy();current=K.copy();seen=set();records=[];t0=time.monotonic()
    for i in range(iterations):
        random.seed(seed+i);start=best.copy() if i%3 else current.copy();start_pd=start.PD_code()
        steps=5+5*(i%6);start.backtrack(steps,prob_type_1=.1,prob_type_2=.7)
        shaken=start.PD_code();start.simplify('global',type_III_limit=300);current=start
        sig=diagram_signature(current.PD_code())
        if len(current.crossings)<=len(best.crossings) and sig not in seen:
            seen.add(sig)
            control=current.exterior().isometry_signature(of_link=True,ignore_orientation=False)
            assert control==original_sig
            records.append({'iteration':i,'seed':seed+i,'steps':steps,'start_pd':start_pd,'shaken_pd':shaken,
                            'endpoint_pd':current.PD_code(),'crossings':len(current.crossings),'diagram_signature':sig,
                            'numerical_source_match':True})
            if len(current.crossings)<len(best.crossings):
                best=current.copy();print('improved',i,len(best.crossings),flush=True)
        if time.monotonic()-t0>=seconds:break
    result={'status':'ISOTOPY_SEARCH_WITH_NUMERICAL_CONTROL_NOT_CERTIFIED_IDENTIFICATION','card':card,
            'iterations_done':i+1,'seed':seed,'time_cap':seconds,'best_crossings':len(best.crossings),
            'best_pd':best.PD_code(),'original_numerical_signature':original_sig,'records':records,
            'seconds':round(time.monotonic()-t0,3)}
    Path(output).write_text(json.dumps(result,separators=(',',':'))+'\n');print('best',len(best.crossings),'diagrams',len(records),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('card');p.add_argument('output');p.add_argument('--iterations',type=int,default=150)
    p.add_argument('--seconds',type=float,default=90);p.add_argument('--seed',type=int,default=20260915)
    a=p.parse_args();run(a.card,a.output,a.iterations,a.seconds,a.seed)
