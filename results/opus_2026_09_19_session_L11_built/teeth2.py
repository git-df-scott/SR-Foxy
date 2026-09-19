"""Is Theorem 2's bite at lk=0 entirely explained by non-ribbon COMPONENTS?

Fox-Milnor: a ribbon knot has det = f(-1)^2, a perfect square.  So if
prod det(K_i) is not a square, some component is already not a ribbon knot and
the link cannot be ribbon for a reason that has nothing to do with how the
components are linked.  L_{3,1} has components Q and V_3 with det 9 and 9, both
squares.  If every violation in this population has a non-square product, then
Theorem 2 has no demonstrated bite in the regime L_{3,1} actually lives in.
"""
import sys, os, math, collections, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SR-Foxy', 'scripts'))
import snappy, compdet
from sagefree_eisermann import null_and_det_V

def sq(v):
    return int(math.isqrt(v)) ** 2 == v

rows = []
for L in snappy.HTLinkExteriors(cusps=2):
    try:
        K = L.link()
    except Exception:
        continue
    if len(K.link_components) != 2 or abs(K.linking_number()) > 1e-9:
        continue
    try:
        nu, dv, _ = null_and_det_V(K)
        dvi = int(dv)
    except Exception:
        continue
    dets = compdet.component_determinants(K)
    if any(not isinstance(d, int) for d in dets):
        continue
    prod = dets[0] * dets[1]
    rows.append({'name': str(L), 'det_V': dvi, 'dets': dets, 'prod': prod,
                 'prod_square': sq(prod), 'all_comp_square': all(sq(d) for d in dets),
                 'ok': (dvi - prod) % 32 == 0})

tab = collections.Counter((r['prod_square'], r['ok']) for r in rows)
print('testable lk=0, 2-component links:', len(rows))
print()
print('                       satisfies Thm 2   violates Thm 2')
print('  product a square  :  %6d            %6d' % (tab[(True, True)], tab[(True, False)]))
print('  product NOT square:  %6d            %6d' % (tab[(False, True)], tab[(False, False)]))
print()
viol_sq = [r for r in rows if r['ok'] is False and r['prod_square']]
print('VIOLATIONS with a perfect-square product (the regime L_{3,1} lives in):', len(viol_sq))
for r in viol_sq[:20]:
    print('   %-16s dets=%s prod=%d detV=%d  detV mod32=%d pred=%d'
          % (r['name'], r['dets'], r['prod'], r['det_V'], r['det_V'] % 32, r['prod'] % 32))
print()
allsq = [r for r in rows if r['all_comp_square']]
print('links where EVERY component determinant is a square (components can be ribbon):', len(allsq))
print('   of those, violating Theorem 2:', sum(1 for r in allsq if not r['ok']))
json.dump(rows, open('teeth_rows.json', 'w'), indent=1)
