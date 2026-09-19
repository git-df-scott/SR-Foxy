#!/usr/bin/env python3
"""One explicitly scoped HKL calculation, with method and mode preserved."""
import argparse
import json
from pathlib import Path
import time
import sage.all
import snappy

ap = argparse.ArgumentParser()
ap.add_argument('card')
ap.add_argument('output')
ap.add_argument('--p', type=int, required=True)
ap.add_argument('--q', type=int, required=True)
ap.add_argument('--method', choices=['basic', 'advanced', 'direct'], default='advanced')
args = ap.parse_args()
d = json.loads(Path(args.card).read_text())
pd = d.get('pd_code_snappy_0indexed') or d['pd_code']
out = Path(args.output)
if out.exists():
    raise FileExistsError(out)
M = snappy.Link([tuple(c) for c in pd]).exterior()
start = time.monotonic()
result = M.slice_obstruction_HKL((args.p, args.q), method=args.method, ribbon_mode=False, verbose=2)
record = {'knot': d['name'], 'p': args.p, 'q': args.q, 'method': args.method,
          'ribbon_mode': False, 'result': None if result is None else list(map(int, result)),
          'seconds': round(time.monotonic()-start, 3), 'snappy': snappy.__version__,
          'meaning': 'A returned pair is a computational nonsliceness obstruction; null means only no obstruction in this calculation.'}
out.write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps(record), flush=True)
