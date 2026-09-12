#!/usr/bin/env python3
"""Compare saved fusion endpoints; numerical matches require certification."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import time
import snappy
from filter_common_successors import read_unique


def compare(paths, output, left_filter=None):
    if Path(output).exists():
        raise FileExistsError(output)
    selected = None
    if left_filter:
        d = json.loads(Path(left_filter).read_text())
        selected = {c['index'] for c in d['sides'][0]['checks']
                    if c.get('common_successor_not_excluded')}
    maps, summaries, exact_maps = [], [], []
    for side, path in enumerate(paths):
        t0 = time.monotonic(); rows = read_unique(path)
        if side == 0 and selected is not None:
            rows = [r for r in rows if r['index'] in selected]
        mapping, exact, failed = defaultdict(list), defaultdict(list), []
        for r in rows:
            exact[r['diagram_signature']].append(r['index'])
            try:
                M = snappy.Link(r['endpoint_pd']).exterior()
                sig = M.isometry_signature(of_link=True, ignore_orientation=False)
                if sig is None:
                    raise ValueError('No numerical isometry signature')
                mapping[sig].append(r['index'])
            except Exception as e:
                failed.append({'index':r['index'], 'error':type(e).__name__+': '+str(e)})
        maps.append(mapping); exact_maps.append(exact)
        summaries.append({'path':str(path), 'attempted':len(rows),
                          'successful':sum(map(len, mapping.values())),
                          'failed':failed, 'seconds':round(time.monotonic()-t0,3)})
    result = {'status':'NUMERICAL_SCREEN_NOT_A_CERTIFICATE', 'left_filter':left_filter,
              'of_link':True, 'ignore_orientation':False, 'sides':summaries,
              'numerical_matches':[{'signature':k,'left':maps[0][k],'right':maps[1][k]}
                                   for k in sorted(maps[0].keys() & maps[1].keys())],
              'diagram_matches':[{'signature':k,'left':exact_maps[0][k],'right':exact_maps[1][k]}
                                 for k in sorted(exact_maps[0].keys() & exact_maps[1].keys())],
              'limitations':'Failed/nonhyperbolic cases remain unresolved. Hits require verified peripheral identification and an oriented movie audit. No hit does not imply nonconcordance.'}
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'sides'}))
    return result


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('left'); p.add_argument('right'); p.add_argument('output')
    p.add_argument('--left-filter'); a=p.parse_args()
    compare([a.left,a.right],a.output,a.left_filter)
