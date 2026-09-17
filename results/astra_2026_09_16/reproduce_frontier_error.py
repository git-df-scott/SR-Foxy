"""Reproduce error-as-negative bookkeeping in pinned SR-Foxy runner.

The topology library is deliberately mocked to raise. This tests only the
runner's handling of failure; it makes no claim about any knot or old run.
Usage: python3 reproduce_frontier_error.py /path/to/reviewed/repository
"""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import runpy
import sys
import tempfile
import types

root = Path(sys.argv[1]).resolve()
source = root / 'scripts/teichner_frontier_resumable.py'
class FakeLink:
    crossings = [None]
    def __init__(self, *args): pass
    def connected_sum(self, other): return self
    def simplify(self, *args): pass

def fail(*args, **kwargs):
    raise RuntimeError('INJECTED_SEARCH_FAILURE')

mods = {name: types.ModuleType(name) for name in (
    'snappy', 'spherogram', 'spherogram.links',
    'spherogram.links.bands', 'spherogram.links.bands.search')}
mods['snappy'].Link = FakeLink
mods['spherogram'].links = mods['spherogram.links']
mods['spherogram.links'].bands = mods['spherogram.links.bands']
mods['spherogram.links.bands'].search = mods['spherogram.links.bands.search']
mods['spherogram.links.bands.search'].ribbon_concordant_links = fail
mods['spherogram.links.bands.search'].verify_ribbon_to_unknot = lambda *a: False
sys.modules.update(mods)
with tempfile.TemporaryDirectory() as tmp:
    p = Path(tmp)
    inp = p / 'input.json'
    inp.write_text(json.dumps({'name':'MOCK_TARGET','pd_code':[[0,1,2,3]]}))
    out = p / 'checkpoint.json'
    transcript = []
    for _ in range(2):
        sys.argv = [str(source), str(out), str(inp), '6_1', '1', '4']
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            runpy.run_path(str(source), run_name='__main__')
        transcript.append(buf.getvalue())
    rec = json.loads(out.read_text())
    row = next(iter(rec['completed'].values()))
    assert row['error'] == 'RuntimeError: INJECTED_SEARCH_FAILURE'
    assert rec['coverage']['6_1']['complete'] is True
    assert rec['coverage']['6_1']['zero_survivor_diagrams'] == [0]
    assert 'skip (done)' in transcript[1]
    result = {
        'status': 'REPRODUCED_ERROR_AS_COMPLETED_NEGATIVE',
        'scope': 'Mocked search failure; not a topology calculation or claim that old results contain this failure.',
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'checkpoint': rec, 'transcript': transcript,
    }
    destination = Path(__file__).with_name('frontier-error-reproduction.json')
    if destination.exists(): raise FileExistsError(destination)
    destination.write_text(json.dumps(result, indent=2) + '\n')
    print(result['status'])
