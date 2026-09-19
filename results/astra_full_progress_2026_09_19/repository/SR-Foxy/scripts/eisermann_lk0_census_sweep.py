#!/usr/bin/env python3
"""Sweep the tabulated 2-component links for a TESTABLE lk = 0 example.

Why.  research/22 §3.3 stakes the whole L_{3,1} test on Eisermann's Theorem 2,
and argues from §3.2 that Theorem 2 "has teeth" because L9n18 and L9n19 violate
it.  Both of those have LINKING NUMBER 4.  GST's L_{3,1} is algebraically
unlinked, lk = 0.  `scripts/eisermann_lk0_vacuity.py` found that in the small
census NO lk = 0 link is even testable -- every one has null V = 0, so it fails
Theorem 1 and det V is undefined.

So the teeth of the L_{3,1} test are UNESTABLISHED in the regime L_{3,1} lives
in.  This sweep looks for the missing object:

    a 2-component link with lk = 0 AND null V = 1.

Those are exactly the links on which Theorem 2 is a real test rather than a
vacuous statement.  If one is found and VIOLATES det V = det(K_1)det(K_2) mod 32,
the L_{3,1} test has teeth and the reconstruction is worth doing.  If many are
found and none violates, that is evidence the test cannot fire on L_{3,1} and the
reconstruction buys nothing.

Writes incrementally so a container reclamation loses nothing.
"""
import sys, os, json, time, warnings, datetime
warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import snappy
import sagefree_jones as SJ
import spherogram.links.links_base as lb

def _jp(self, new_convention=True, **kw):
    return SJ.jones_polynomial(self)
snappy.Link.jones_polynomial = lb.Link.jones_polynomial = _jp
import eisermann_ribbon_link_gate as G
from eisermann_lk0_vacuity import linking_number, component_dets

OUT = sys.argv[1] if len(sys.argv) > 1 else 'results/eisermann_lk0_census_sweep.json'
MAXCR = int(sys.argv[2]) if len(sys.argv) > 2 else 12

rec = {'date': datetime.datetime.utcnow().isoformat() + 'Z',
       'question': 'is there a 2-component link with lk = 0 and null V = 1?',
       'why': ('Theorem 2 is a real test only when null V = n-1 makes det V finite. '
               'research/22 §3.2 establishes teeth only at lk = 4; L_{3,1} has lk = 0.'),
       'max_crossings': MAXCR, 'scanned': 0, 'two_component': 0,
       'lk0': 0, 'testable_lk0': [], 'violations': [], 'rows': []}

def flush():
    tmp = OUT + '.tmp'
    json.dump(rec, open(tmp, 'w'), indent=1, default=str)
    os.replace(tmp, OUT)

t0 = time.time()
for cr in range(2, MAXCR + 1):
    for kind in ('a', 'n'):
        idx = 1
        misses = 0
        while misses < 3:
            name = 'L%d%s%d' % (cr, kind, idx)
            try:
                L = snappy.Link(name)
                misses = 0
            except Exception:
                misses += 1; idx += 1; continue
            idx += 1
            rec['scanned'] += 1
            try:
                if len(L.link_components) != 2:
                    continue
                rec['two_component'] += 1
                lk = linking_number(L)
                if lk != 0:
                    continue
                rec['lk0'] += 1
                nv = G.nullity(L)
                row = {'name': name, 'crossings': cr, 'lk': 0, 'null_V': nv}
                if nv == 1:
                    dv = G.det_V(L, 2)
                    cds = component_dets(L)
                    prod = None
                    if all(c is not None for c in cds):
                        prod = cds[0] * cds[1]
                    row.update(det_V=dv, comp_dets=cds, product=prod,
                               congruence_holds=None if prod is None
                               else (dv % 32 == prod % 32))
                    rec['testable_lk0'].append(row)
                    if row['congruence_holds'] is False:
                        rec['violations'].append(row)
                    print('TESTABLE  %-8s lk=0 nullV=1 detV=%s prod=%s holds=%s'
                          % (name, dv, prod, row['congruence_holds']), flush=True)
                rec['rows'].append(row)
            except Exception as e:
                rec['rows'].append({'name': name, 'error': str(e)[:80]})
            if rec['scanned'] % 25 == 0:
                rec['elapsed'] = round(time.time() - t0, 1)
                flush()
                print('[%7.1fs] scanned %d, 2-comp %d, lk0 %d, testable %d'
                      % (time.time() - t0, rec['scanned'], rec['two_component'],
                         rec['lk0'], len(rec['testable_lk0'])), flush=True)
rec['elapsed'] = round(time.time() - t0, 1)
flush()
print('DONE scanned=%d two_component=%d lk0=%d testable_lk0=%d violations=%d'
      % (rec['scanned'], rec['two_component'], rec['lk0'],
         len(rec['testable_lk0']), len(rec['violations'])), flush=True)
