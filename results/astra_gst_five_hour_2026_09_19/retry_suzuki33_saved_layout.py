"""Bounded retry of missing GST1 root jets; reuse and verify saved Morse data."""
from pathlib import Path
import json, sys, time, signal, hashlib
import snappy, regina

p = Path(__file__).resolve().parent
sys.path.insert(0, str(p.parents[1] / 'scripts'))
from sagefree_jones import PerfectMatching, install
from suzuki_root_minus_one import Jet, Ring
from spherogram.links import jones, exhaust

term = sys.argv[1]
assert term in ('23', '33')
out = p / 'suzuki33' / 'GST1' / term
assert not (out / 'RESULT.json').exists(), 'Preserve completed traces'
layout = next(r for r in json.loads((p / 'SUZUKI33_GST1_LAYOUT_LIMITS.json').read_text()) if r['term'] == term)
inp = json.loads((out / 'INPUT.json').read_text())
encoded = exhaust.MorseEncoding(layout['morse_events'])
link = snappy.Link(inp['simplified_pd'])
def signature(L):
    return regina.Link.fromPD([[a + 1 for a in row] for row in L.PD_code()]).sig(False, True, True)
sig = signature(link)
assert sig == signature(encoded.link()), 'Saved Morse encoding differs from input diagram'
assert encoded.width == layout['max_frontier_strands']
# All pairwise linking numbers are zero, so orientation reversals allowed by
# the signature comparison do not change the normalized Jones polynomial.
assert all(x == 0 for row in link.linking_matrix() for x in row)
cap = 60000 if term == '23' else 210000
seconds = int(sys.argv[2]) if len(sys.argv) > 2 else 90
assert 1 <= seconds <= 240
audit_path = out / ('RETRY_CHECKPOINT09.json' if seconds == 90 else f'RETRY_CHECKPOINT09_{seconds}S.json')
assert not audit_path.exists(), 'Preserve previous attempt'
def timeout(*_):
    raise TimeoutError(f'{seconds}_SECOND_LIMIT_INCONCLUSIVE')
signal.signal(signal.SIGALRM, timeout)
signal.alarm(seconds)
start = time.monotonic()
install()
precision = sum(map(int, term)) - 1
Jet.order = precision
jones.R = Ring(); jones.q = Jet([10, 1]); jones.PerfectMatching = PerfectMatching
value = jones.VElement()
peak = 1
audit = dict(term=term, state_cap=cap, time_limit_seconds=seconds,
             saved_layout_verified=True, reflection_allowed=False,
             input_sha256=hashlib.sha256((out / 'INPUT.json').read_bytes()).hexdigest(),
             morse_width=encoded.width, diagram_signature=sig, precision=precision)
try:
    for i, event in enumerate(encoded):
        if event.kind == 'cup': value = value.insert_cup(event.min)
        elif event.kind == 'cap': value = value.cap_off(event.min)
        elif event.a < event.b: value = value.add_positive_crossing(event.min)
        else: value = value.add_negative_crossing(event.min)
        value.dict = {key: c for key, c in value.dict.items() if c}
        peak = max(peak, len(value.dict))
        if peak > cap: raise RuntimeError('STATE_CAP_INCONCLUSIVE')
    empty = PerfectMatching([])
    assert not (set(value.dict) - {empty})
    signs = [c.sign for c in link.crossings]
    minus, plus = signs.count(-1), signs.count(1)
    v = jones.q
    result = (-1)**minus * v**(plus - 2*minus) * value.dict.get(empty, Jet(0))
    result *= (v + v**-1)**inp['unlinked_components']
    audit.update(status='complete', coefficients_mod101=list(result.d),
                 label='GST1', a=int(term[0]), b=int(term[1]),
                 crossings=len(link.crossings), morse_events=layout['morse_events'],
                 scope='Unreduced Jones in F101[x]/x^precision at v=10+x; zero is inconclusive.')
except Exception as exc:
    audit.update(status='inconclusive', error=repr(exc))
finally:
    signal.alarm(0)
    audit.update(seconds=time.monotonic()-start, max_retained_states=peak, last_event=i)
    audit_path.write_text(json.dumps(audit, indent=2)+'\n')
if audit['status'] == 'complete':
    (out / 'RESULT.json').write_text(json.dumps(audit, indent=2)+'\n')
print({k: v for k, v in audit.items() if k not in ('morse_events', 'diagram_signature')}, flush=True)
