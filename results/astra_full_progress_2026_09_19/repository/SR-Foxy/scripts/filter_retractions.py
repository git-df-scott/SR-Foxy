#!/usr/bin/env python3
"""Reproducible homotopy-retraction search using stored quotient complexes."""
import argparse
import json
from pathlib import Path
from chain_map_filter import check_retraction


def restore(c):
    return dict(c,generators={int(k):tuple(v) for k,v in c['generators'].items()})


def run(input_path,output,count=0,timeout_ms=20000):
    if Path(output).exists():raise FileExistsError(output)
    data=json.loads(Path(input_path).read_text())
    sources=list(map(restore,data['source_complexes']))
    result={'status':'EXPLORATORY_NECESSARY_CONDITION_ONLY','input':input_path,
            'ring':'F2[U,V]/(UV)','solver_timeout_ms':timeout_ms,'runs':[],
            'meaning':'SAT is an algebraic retraction, not a geometric concordance. UNKNOWN is inconclusive.'}
    for r in (data['runs'][:count] if count else data['runs']):
        target=restore(r['target_complex'])
        own=check_retraction(sources[0],target,timeout_ms)
        other=check_retraction(sources[1],target,timeout_ms)
        result['runs'].append({'source_index':r['source_index'],'K0_to_J':own,'K1_to_J':other})
        Path(output).write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({'index':r['source_index'],'K0':own['status'],'K1':other['status']}),flush=True)
        assert own['status']!='UNSAT','Own-source contradiction: suspend mathematical use of this filter'
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('output')
    p.add_argument('--count',type=int,default=0);p.add_argument('--timeout-ms',type=int,default=20000)
    a=p.parse_args();run(a.input,a.output,a.count,a.timeout_ms)
