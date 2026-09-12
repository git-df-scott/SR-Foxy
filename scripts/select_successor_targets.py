#!/usr/bin/env python3
"""Preserve full moves for Floer-compatible targets, ordered by diagram size."""
import argparse
import json
from pathlib import Path
import snappy
from filter_common_successors import read_unique


def select(movies, filtered, output):
    if Path(output).exists():raise FileExistsError(output)
    checks=json.loads(Path(filtered).read_text())['sides'][0]['checks']
    selected={r['index']:r for r in checks if r.get('common_successor_not_excluded')}
    rows=[]
    for r in read_unique(movies):
        if r['index'] not in selected:continue
        h=selected[r['index']];r['hfk_check']=h
        try:r['numerical_isometry_signature']=snappy.Link(r['endpoint_pd']).exterior().isometry_signature(of_link=True,ignore_orientation=False)
        except Exception:r['numerical_isometry_signature']=None
        rows.append(r)
    rows.sort(key=lambda r:(r['hfk_check']['fibered'],r['crossings'],r['index']))
    result={'status':'NECESSARY_TEST_PASSES_ONLY_NOT_CONCORDANCE_CERTIFICATES',
            'movies':movies,'hfk_results':filtered,'candidates':rows,
            'count':len(rows),'nonfibered_count':sum(not r['hfk_check']['fibered'] for r in rows)}
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='candidates'}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('movies');p.add_argument('filtered');p.add_argument('output')
    a=p.parse_args();select(a.movies,a.filtered,a.output)
