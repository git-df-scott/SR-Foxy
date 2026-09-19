#!/usr/bin/env python3
"""Full pipeline sweep: find a lk=0 link that is Eisermann-non-ribbon AND may be slice.

For each tabulated 2-component link in the given crossing range:
  1. linking number 0?                     (else skip -- wrong regime)
  2. null V = 1?                           (else it fails Theorem 1 and det V is
                                            infinite; not ribbon, but Theorem 2 is
                                            silent and the beta screen still applies)
  3. det V vs det(K_1)det(K_2) mod 32      (Eisermann Theorem 2)
  4. if it VIOLATES, it is PROVED NOT RIBBON.  Then screen for sliceness:
       - both component determinants perfect squares and Fox-Milnor (else not slice)
       - Sato-Levine beta = mu-bar(1122) = [z^3] nabla_L must vanish for a slice link
  5. a link surviving 4 is a CANDIDATE: proved non-ribbon, sliceness not excluded.

A survivor is NOT a counterexample.  research/22's standing rule applies: it would
still need a slice disk exhibited, and being unobstructed is not being slice.

Controls run first and the sweep refuses to start if they miss.
Writes incrementally; a container reclamation loses at most one link.
"""
import sys, os, json, time, math, warnings, datetime
warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import snappy
import sagefree_jones as SJ
import spherogram.links.links_base as lb
def _jp(self, new_convention=True, **kw): return SJ.jones_polynomial(self)
snappy.Link.jones_polynomial = lb.Link.jones_polynomial = _jp
import eisermann_ribbon_link_gate as G
from fox_milnor_sagefree import delta_from_hfk, fox_milnor
from triple_linking import conway_coefficients
from eisermann_lk0_vacuity import linking_number

def comp_det(L, i):
    S = L.sublink([i])
    if len(S.crossings) == 0 or len(S.link_components) == 0:
        return 1, True                      # crossingless component = unknot
    S.simplify('global')                    # single component, so safe
    if len(S.crossings) == 0:
        return 1, True
    p = delta_from_hfk(S.knot_floer_homology())
    ok, _, _, _ = fox_milnor(p)
    return abs(int(p.eval(-1))), ok

def beta(L):
    nab = conway_coefficients(L)
    return (nab[3] if len(nab) > 3 else 0), nab

OUT = sys.argv[1]; LO = int(sys.argv[2]); HI = int(sys.argv[3])

# ---- controls --------------------------------------------------------------
c = {}
for n in (2, 3):
    U = G.unlink(n); c['O%d' % n] = (G.nullity(U), int(G.det_V(U, n)))
wh = beta(snappy.Link('L5a1'))[0]
l9 = int(G.det_V(snappy.Link('L9n18'), 2))
assert c['O2'] == (1, 1) and c['O3'] == (2, 1), 'unlink control failed: %s' % c
assert wh != 0, 'Whitehead Sato-Levine control failed: beta = %s' % wh
assert l9 % 32 == 9, 'L9n18 det V control failed: %s' % l9
print('controls PASS: unlinks %s | Whitehead beta = %s | L9n18 det V = %s' % (c, wh, l9), flush=True)

rec = {'date': datetime.datetime.utcnow().isoformat() + 'Z',
       'range': [LO, HI], 'controls': {'unlinks': c, 'whitehead_beta': wh, 'L9n18_detV': l9},
       'scanned': 0, 'lk0': 0, 'testable': 0, 'violations': [], 'candidates': [], 'rows': []}
def flush():
    tmp = OUT + '.tmp'; json.dump(rec, open(tmp, 'w'), indent=1, default=str); os.replace(tmp, OUT)

t0 = time.time()
for cr in range(LO, HI + 1):
    for kind in ('a', 'n'):
        idx, misses = 1, 0
        while misses < 3:
            name = 'L%d%s%d' % (cr, kind, idx)
            try:
                L = snappy.Link(name); misses = 0
            except Exception:
                misses += 1; idx += 1; continue
            idx += 1; rec['scanned'] += 1
            try:
                if len(L.link_components) != 2 or linking_number(L) != 0:
                    continue
                rec['lk0'] += 1
                nv = G.nullity(L)
                if nv != 1:
                    continue
                rec['testable'] += 1
                dv = int(G.det_V(L, 2))
                d0, fm0 = comp_det(L, 0); d1, fm1 = comp_det(L, 1)
                prod = d0 * d1
                if dv % 32 == prod % 32:
                    continue                                  # satisfies Theorem 2
                row = {'name': name, 'crossings': cr, 'det_V': dv,
                       'comp_dets': [d0, d1], 'product': prod}
                rec['violations'].append(row)
                sq = (math.isqrt(d0) ** 2 == d0) and (math.isqrt(d1) ** 2 == d1)
                if not (sq and fm0 and fm1):
                    row['verdict'] = 'not slice: a component is not slice'
                else:
                    b, nab = beta(L); row['beta'] = b; row['conway'] = nab
                    if b != 0:
                        row['verdict'] = 'not slice: Sato-Levine beta = %s' % b
                    else:
                        row['verdict'] = 'CANDIDATE: non-ribbon, sliceness not excluded'
                        rec['candidates'].append(row)
                        print('*** CANDIDATE %s  detV=%d prod=%d beta=0 ***' % (name, dv, prod), flush=True)
                print('VIOLATION %-10s detV=%-6d prod=%-5d %s' % (name, dv, prod, row['verdict']), flush=True)
            except Exception as e:
                rec['rows'].append({'name': name, 'error': str(e)[:90]})
            if rec['scanned'] % 50 == 0:
                rec['elapsed'] = round(time.time() - t0, 1); flush()
                print('[%7.1fs] scanned %d lk0 %d testable %d violations %d candidates %d'
                      % (time.time() - t0, rec['scanned'], rec['lk0'], rec['testable'],
                         len(rec['violations']), len(rec['candidates'])), flush=True)
rec['elapsed'] = round(time.time() - t0, 1); flush()
print('DONE scanned=%d lk0=%d testable=%d violations=%d candidates=%d'
      % (rec['scanned'], rec['lk0'], rec['testable'], len(rec['violations']),
         len(rec['candidates'])), flush=True)
