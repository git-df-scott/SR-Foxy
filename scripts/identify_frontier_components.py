#!/usr/bin/env python3
"""Bounded census nominations for saved components, not topology certificates.

Numerical isometry lookup only nominates a knot. It never excludes a path or
establishes sliceness/non-sliceness. Each component has an isolated time limit.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from bounded_ribbon_search import save


def run(source, output):
    source, output = Path(source), Path(output)
    if output.exists():
        raise FileExistsError(output)
    data = json.loads(source.read_text())
    assert data['complete']
    record = {'source': str(source), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'scope': 'Unverified numerical census nominations only; no exclusion or certificate.',
              'timeout_seconds': 8, 'rows': [], 'complete': False}
    code = '''import json, sys, snappy
pd = json.load(sys.stdin)
E = snappy.Link(pd).exterior()
match = snappy.HTLinkExteriors.identify(E, extends_to_link=True)
print(json.dumps({'match': match.name() if match else None, 'verified': False}))
'''
    used = {key for row in data['rows'] for key in row['components']}
    for key in sorted(used):
        component = data['components'][key]
        if not component['pd']:
            continue
        row = {'component': key, 'crossings': len(component['pd'])}
        try:
            result = subprocess.run([sys.executable, '-c', code], input=json.dumps(component['pd']),
                                    text=True, capture_output=True, timeout=8)
            if result.returncode:
                row['error_unknown'] = result.stderr[-2000:]
            else:
                row.update(json.loads(result.stdout.strip().splitlines()[-1]))
        except Exception as e:
            row['error_unknown'] = repr(e)
        record['rows'].append(row)
        save(output, record)
        print(json.dumps(row), flush=True)
    record['complete'] = True
    save(output, record)


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2])
