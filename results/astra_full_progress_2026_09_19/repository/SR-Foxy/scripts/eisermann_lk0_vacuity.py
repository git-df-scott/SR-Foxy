#!/usr/bin/env python3
"""Does Eisermann's Theorem 2 have teeth on ALGEBRAICALLY SPLIT 2-component links?

This decides whether the pre-registered L_{3,1} test in research/22 §3.3 is worth
building the link for.

  Theorem 2 (Eisermann).  L an n-component RIBBON link  =>
        det V(L) = det(K_1)...det(K_n)   (mod 32).

research/22 §3.1 already shows Theorem 1 is vacuous on 2-component slice links.
§3.3 therefore stakes the whole L_{3,1} test on Theorem 2, whose teeth are argued
from §3.2: of 75 tabulated 2-component links, only L9n18 and L9n19 have
null V = 1, and BOTH violate the congruence (det V = 9 and 25 against a component
product of 1).

But those two links have LINKING NUMBER 4.  Every 2-cable tested in research/28
had linking number 0 and satisfied the congruence, non-slice ones included.  And
GST's L_{3,1} is algebraically unlinked, i.e. lk = 0.

So the question this script asks is precise:

    does  det V(L) = det(K_1) det(K_2)  (mod 32)  hold AUTOMATICALLY
    for every 2-component link with lk = 0?

If yes, Theorem 2 is vacuous on algebraically split 2-component links, the
L_{3,1} test cannot fire whatever the link turns out to be, and reconstructing it
buys nothing.  If no -- if some lk = 0 link violates the congruence -- the test
has teeth and the reconstruction is worth doing.

Everything is exact integer arithmetic on Jones polynomials; no floating point.
"""
import sys, os, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import snappy, spherogram
import sagefree_jones as SJ
import spherogram.links.links_base as lb

def _jp(self, new_convention=True, **kw):
    return SJ.jones_polynomial(self)
snappy.Link.jones_polynomial = lb.Link.jones_polynomial = _jp
import eisermann_ribbon_link_gate as G
from fox_milnor_sagefree import delta_from_hfk


def linking_number(L):
    """lk of a 2-component link from crossing signs; Sage-free."""
    which = {}
    for i, comp in enumerate(L.link_components):
        for ce in comp:
            which[(ce[0], ce[1])] = i
    tot = 0
    for c in L.crossings:
        idx = [which.get((c, k)) for k in range(4)]
        idx = [x for x in idx if x is not None]
        if len(set(idx)) == 2:
            tot += c.sign
    return tot // 2


def component_dets(L):
    """|Delta(-1)| of each component, via HFK on the sublink."""
    out = []
    for i in range(len(L.link_components)):
        M = snappy.Link(L.PD_code())
        # delete the other components by taking the sublink
        keep = [j for j in range(len(M.link_components)) if j == i]
        try:
            S = M.sublink(keep)
            if len(S.crossings) == 0:
                out.append(1)                     # unknot component
            else:
                out.append(abs(delta_from_hfk(S.knot_floer_homology()).eval(-1)))
        except Exception:
            try:
                comp = L.link_components[i]
                sub = snappy.Link([c for c in L.PD_code()])
                out.append(None)
            except Exception:
                out.append(None)
    return out


def row(name, L):
    n = len(L.link_components)
    lk = linking_number(L) if n == 2 else None
    nv = G.nullity(L)
    # det V = [V(L)/V(O^n)](q=i) is FINITE exactly when null V = n-1, i.e. exactly
    # when Theorem 1 already holds.  Otherwise the ratio blows up (ComplexInfinity)
    # and Theorem 2 is moot: the link has already failed Theorem 1 and is not ribbon.
    dv = G.det_V(L, n) if nv == n - 1 else None
    cds = component_dets(L)
    prod = None
    if all(c is not None for c in cds):
        prod = 1
        for c in cds:
            prod *= c
    holds = None if (prod is None or dv is None) else (dv % 32 == prod % 32)
    return dict(name=name, comps=n, lk=lk, null_V=nv, det_V=dv,
                comp_dets=cds, prod=prod, congruence_holds=holds)


if __name__ == '__main__':
    print('control: unlinks must give null V = n-1 and det V = 1')
    for n in (2, 3):
        L = G.unlink(n)
        print('   O^%d  null V = %d  det V = %d' % (n, G.nullity(L), G.det_V(L, n)))
    print()
    names = sys.argv[1:] or ['L2a1', 'L5a1', 'L6a1', 'L6a2', 'L6a3', 'L6a5',
                             'L7a1', 'L7a2', 'L7a3', 'L7a4', 'L7a5', 'L7a6',
                             'L7n1', 'L7n2', 'L8a1', 'L8a2', 'L8n1', 'L8n2',
                             'L9n18', 'L9n19']
    print('null V = n-1 is Theorem 1; det V is defined only then, so a "n/a" row is')
    print('a link that already fails Theorem 1 and cannot be ribbon.')
    print()
    print('%-8s %5s %4s %7s %9s %14s %9s %s'
          % ('link', 'comps', 'lk', 'null V', 'det V', 'comp dets', 'product', 'Thm2 holds'))
    viol_lk0 = []; rows = []
    for nm in names:
        try:
            L = snappy.Link(nm)
        except Exception as e:
            print('%-8s  could not load: %s' % (nm, str(e)[:40]))
            continue
        try:
            r = row(nm, L)
        except Exception as e:
            print('%-8s  ERROR %s' % (nm, str(e)[:60]))
            continue
        print('%-8s %5d %4s %7d %9s %14s %9s %s'
              % (r['name'], r['comps'], r['lk'], r['null_V'],
                 'n/a' if r['det_V'] is None else r['det_V'],
                 r['comp_dets'], r['prod'], r['congruence_holds']))
        rows.append(r)
        if r['comps'] == 2 and r['lk'] == 0 and r['congruence_holds'] is False:
            viol_lk0.append(r['name'])
    print()
    tested = [r for r in rows if r['comps'] == 2 and r['lk'] == 0
              and r['congruence_holds'] is not None]
    untestable = [r for r in rows if r['comps'] == 2 and r['lk'] == 0
                  and r['congruence_holds'] is None]
    print('lk = 0 rows that were ACTUALLY TESTABLE (null V = 1, det V defined):',
          len(tested), [r['name'] for r in tested])
    print('lk = 0 rows that were NOT testable (null V = 0, already fail Theorem 1):',
          len(untestable))
    print()
    if viol_lk0:
        print('VIOLATIONS AMONG TESTABLE lk = 0 LINKS:', viol_lk0)
        print('=> Theorem 2 HAS TEETH on algebraically split 2-component links, so the')
        print('   L_{3,1} test can fire and reconstructing the link is worth it.')
    elif tested:
        print('All %d testable lk = 0 rows satisfied the congruence.' % len(tested))
        print('=> Evidence, of that sample size, that Theorem 2 is vacuous on')
        print('   algebraically split 2-component links.')
    else:
        print('*** NO lk = 0 LINK IN THIS CENSUS WAS TESTABLE AT ALL. ***')
        print('Every one has null V = 0, so it fails Theorem 1 and det V is undefined.')
        print('This run therefore provides NO evidence either way about the lk = 0')
        print('regime -- and that is the point worth recording, because research/22')
        print('§3.2 argues Theorem 2 "has teeth" from L9n18 and L9n19, which have')
        print('lk = 4.  GST\'s L_{3,1} has lk = 0.  So the teeth of the pre-registered')
        print('L_{3,1} test are UNESTABLISHED, not disproved.  The only testable lk = 0')
        print('examples anyone has are the 0-framed 2-cables of research/28, where the')
        print('congruence held 7 times out of 7, non-slice knots included.')
