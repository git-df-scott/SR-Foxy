"""Do the lk=0 links where Theorem 2 is testable resemble L_{3,1}?

research/31 shows 22 of 41 testable lk=0 links violate Theorem 2, concluding the
test "can fire".  L_{3,1} has components Q and V_3 with det 9 each.  If every
testable link in that population has UNKNOTTED components, the teeth have again
been demonstrated in a different regime from the one the test is run in --
exactly the gap research/31 itself found for the linking number.
"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SR-Foxy', 'scripts'))
import snappy, compdet
from sagefree_eisermann import null_and_det_V

rows, testable = [], []
for L in snappy.HTLinkExteriors(cusps=2):
    try:
        K = L.link()
    except Exception:
        continue
    if len(K.link_components) != 2:
        continue
    if abs(K.linking_number()) > 1e-9:
        continue
    try:
        nu, dv, _ = null_and_det_V(K)
    except Exception:
        continue
    if dv is None:
        continue
    try:
        dvi = int(dv)
    except TypeError:
        continue
    dets = compdet.component_determinants(K)
    if any(not isinstance(d, int) for d in dets):
        continue
    prod = 1
    for d in dets:
        prod *= d
    testable.append({'name': str(L), 'crossings': len(K.crossings),
                     'det_V': dvi, 'mod32': dvi % 32, 'dets': dets,
                     'prod_mod32': prod % 32,
                     'ok': (dvi - prod) % 32 == 0})

print('testable lk=0 links (2 components, null V = 1):', len(testable))
sat = sum(1 for t in testable if t['ok'])
print('  satisfy Theorem 2 :', sat)
print('  VIOLATE Theorem 2 :', len(testable) - sat)
print()
nontriv = [t for t in testable if any(d != 1 for d in t['dets'])]
print('with a KNOTTED component :', len(nontriv))
for t in nontriv[:15]:
    print('   %-14s cr=%2d dets=%s detV=%d mod32=%d pred=%d %s'
          % (t['name'], t['crossings'], t['dets'], t['det_V'], t['mod32'],
             t['prod_mod32'], 'ok' if t['ok'] else 'VIOLATES'))
print()
print('component determinants over the testable population:',
      collections.Counter(d for t in testable for d in t['dets']).most_common())
