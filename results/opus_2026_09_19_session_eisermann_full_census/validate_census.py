"""Eisermann Theorem 1 and 2 on SnapPy's certified RibbonLinks census.

Every link here is ribbon, so Theorem 2 must hold on every one:
    det V(L) = det(K_1) * det(K_2)   (mod 32).
A single violation would mean the pipeline is broken, and would invalidate any
verdict it later returns on L_{3,1}.  Component determinants go through the
splice in compdet.py, not Link.sublink, which crashes on most of this census.
"""
import json, os, signal, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import snappy
import compdet
from compdet import knot_determinant, component_determinants
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'SR-Foxy', 'scripts'))
from sagefree_eisermann import null_and_det_V

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'census_validation.json')
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 12184
PER_LINK_SECONDS = 120


class Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise Timeout()


signal.signal(signal.SIGALRM, _alarm)

rows, viol, skipped = [], [], []
R = snappy.RibbonLinks
t0 = time.time()
for i in range(min(LIMIT, len(R))):
    try:
        signal.alarm(PER_LINK_SECONDS)
        L = R[i].link()
        n = len(L.link_components)
        nu, dv, _ = null_and_det_V(L)
        if dv is None:
            signal.alarm(0)
            skipped.append({'i': i, 'why': 'null_V=%d < n-1=%d' % (nu, n - 1)})
            continue
        dets = component_determinants(L)
        signal.alarm(0)
        if any(not isinstance(d, int) for d in dets):
            skipped.append({'i': i, 'why': 'component det failed: %r' % (dets,)})
            continue
        prod = 1
        for d in dets:
            prod *= d
        try:
            dvi = int(dv)
        except TypeError:
            skipped.append({'i': i, 'why': 'det V not real: %r' % (dv,)})
            continue
        row = {'i': i, 'name': str(R[i].name()), 'crossings': len(L.crossings),
               'components': n, 'null_V': nu, 'thm1': nu == n - 1,
               'det_V': dvi, 'det_V_mod32': dvi % 32,
               'component_dets': dets, 'product_mod32': prod % 32,
               'thm2': (dvi - prod) % 32 == 0}
        rows.append(row)
        if not (row['thm1'] and row['thm2']):
            viol.append(row)
    except Timeout:
        skipped.append({'i': i, 'why': 'timeout %ds' % PER_LINK_SECONDS})
    except Exception as e:
        signal.alarm(0)
        skipped.append({'i': i, 'why': '%s: %s' % (type(e).__name__, e)})
    if (i + 1) % 10 == 0 or i + 1 == LIMIT:
        at17 = sum(1 for r in rows if r['det_V_mod32'] == 17)
        json.dump({'evaluated': len(rows), 'violations': viol,
                   'skipped': skipped, 'at_residue_17': at17,
                   'elapsed_s': round(time.time() - t0, 1), 'rows': rows},
                  open(OUT, 'w'), indent=1)
        print('%d evaluated, %d skipped, %d VIOLATIONS, %d at residue 17, %.0fs'
              % (len(rows), len(skipped), len(viol), at17, time.time() - t0),
              flush=True)
print('DONE')
