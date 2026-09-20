"""Inspect the one unexcluded pinned Whitehead first band; preserve raw input."""
import json
import random
import time
from pathlib import Path
import whitehead_replay as r

HERE = Path(__file__).resolve().parent
random.seed(20260919)
start = time.monotonic()
targets = json.loads((HERE / 'whitehead_TARGETS.json').read_text())
target = r.Link(targets['T']['pd'])
r.normalize_crossing_labels(target)
bands = r.simple_bands(target, max_twists=3, max_band_len=4)
matches = [b for b in bands if b.compressed_spec() == 'ca080502_0_-1']
assert matches
out = r.add_one_band(target, matches[0])
raw = out.PD_code()
assert len(out.link_components) == 2
assert r.linking_number(out) == 0
out.simplify('basic')
report = {'source': 'origin/main Whitehead-stabilizer experiment',
          'band': 'ca080502_0_-1', 'raw_pd': raw, 'pd': out.PD_code(),
          'unlinked_unknot_components': out.unlinked_unknot_components,
          'rank_upper_bound': r.alexander_rank_upper_bound(out), 'components': []}
for index in range(len(out.link_components)):
    k = out.sublink(index)
    k.simplify('basic')
    row = {'index': index, 'pd': k.PD_code(), 'crossings': len(k.crossings)}
    if k.crossings:
        row['jones'] = str(r.as_regina(k).jones())
        row['hfk'] = r.checked_hfk(k)
        row['factors'] = []
        for f in k.deconnect_sum():
            f.simplify('basic')
            if f.crossings:
                row['factors'].append({'pd': f.PD_code(), 'crossings': len(f.crossings),
                                      'hfk': r.checked_hfk(f),
                                      'jones': str(r.as_regina(f).jones())})
    report['components'].append(row)
    print(json.dumps({key: val for key, val in row.items() if key not in ['pd', 'factors']}), flush=True)
report['seconds'] = time.monotonic() - start
report['scope'] = 'One fixed first-band output. Invariants are not a disk certificate.'
dest = HERE / 'WHITEHEAD_SURVIVOR.json'
with dest.open('x') as f:
    json.dump(report, f, indent=2)
print('Saved', dest, flush=True)
