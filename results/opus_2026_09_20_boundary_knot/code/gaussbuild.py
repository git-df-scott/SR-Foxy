"""Build a spherogram Link from per-component signed Gauss words, and the
inverse extraction, with a round-trip validation harness.

Gauss word for a component: ordered list [crossing_id, 'O'|'U', sign] in the
direction of travel.  Conventions used for construction (from spherogram
links_base.Crossing.orient): slots 0/2 are the under-strand oriented 0 -> 2;
the over-strand is 3 -> 1 when sign = +1 and 1 -> 3 when sign = -1.
"""
import snappy, spherogram
from spherogram.links.links_base import Crossing
from spherogram import Link

def extract_gauss(L):
    words = []
    for comp in L.link_components:
        w = []
        for ep in comp:
            c = ep.crossing; slot = ep.strand_index
            w.append([c.label, 'U' if slot == 0 else 'O', c.sign])
        words.append(w)
    return words

def build_link(words):
    ids = sorted({v[0] for w in words for v in w})
    sign = {}
    for w in words:
        for cid, typ, s in w:
            if cid in sign and sign[cid] != s: raise ValueError('sign clash')
            sign[cid] = s
    cr = {cid: Crossing(cid) for cid in ids}
    # visit -> (entry slot, exit slot)
    def slots(cid, typ):
        s = sign[cid]
        if typ == 'U': return 0, 2
        return (3, 1) if s == 1 else (1, 3)
    seq = []
    for w in words:
        vis = [(cid, typ) + slots(cid, typ) for cid, typ, s in w]
        seq.append(vis)
    # check each crossing visited exactly once as O and once as U
    from collections import Counter
    cnt = Counter((cid, typ) for vis in seq for cid, typ, _, _ in vis)
    for cid in ids:
        if cnt[(cid, 'O')] != 1 or cnt[(cid, 'U')] != 1:
            raise ValueError('bad Gauss code at %s' % cid)
    for vis in seq:
        n = len(vis)
        for k in range(n):
            cid, typ, ein, eout = vis[k]
            nid, ntyp, nein, neout = vis[(k+1) % n]
            cr[cid][eout] = cr[nid][nein]
    # Pre-set orientations and signs so spherogram does not re-derive them
    # (Crossing.orient would be free to traverse a component backwards, which
    # flips the signs of all crossings between that component and the others).
    for cid in ids:
        s = sign[cid]
        cr[cid].directions = {(0, 2), (3, 1) if s == 1 else (1, 3)}
        cr[cid].sign = s
    L = Link([cr[cid] for cid in ids], check_planarity=False, build=True)
    for cid in ids:
        if cr[cid].sign != sign[cid]:
            raise ValueError('sign mismatch after orient at %s: %s vs %s' % (cid, cr[cid].sign, sign[cid]))
    return L

def roundtrip_test(names):
    ok = True
    for nm in names:
        L = spherogram.Link(nm)
        w = extract_gauss(L)
        try:
            M = build_link(w)
        except Exception as e:
            print(nm, 'BUILD FAIL', e); ok = False; continue
        same = (len(M.link_components) == len(L.link_components)
                and sorted(c.sign for c in M.crossings) == sorted(c.sign for c in L.crossings)
                and M.exterior().identify() == L.exterior().identify())
        try:
            aL = L.alexander_polynomial(); aM = M.alexander_polynomial()
        except Exception:
            aL = aM = None
        print(nm, 'roundtrip', same, 'alex-equal', aL == aM,
              'writhe', L.writhe(), M.writhe(), 'lk', L.linking_matrix(), M.linking_matrix())
        ok = ok and same
    return ok

if __name__ == '__main__':
    print(roundtrip_test(['3_1','4_1','6_3','8_18','9_46','L2a1','L6a5','L7n1','12n242']))
