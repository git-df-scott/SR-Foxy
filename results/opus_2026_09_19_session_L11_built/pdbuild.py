"""Turn the transcribed L_{1,1} polylines into a PD code.

y is negated first: PDF y grows downward, and the counterclockwise convention
in a PD code is for the standard orientation of the plane.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from l11 import Q, V, segs, inter

CURVES = {'Q': [(x, -y) for x, y in Q], 'V': [(x, -y) for x, y in V]}

# crossing location (x, y as printed, y still positive-down) -> over strand
OVER = {
    (220.4,  33.2): ('Q', 1),    # upper X:  long diagonal over
    (313.1,  51.3): ('Q', 21),   # right vertical over y=51
    (128.4,  52.0): ('Q', 14),   # y=52 horizontal over left vertical
    (129.4,  75.1): ('Q', 26),   # y=75 horizontal over left vertical
    (313.6,  76.0): ('Q', 21),   # right vertical over y=76
    (221.0,  90.4): ('Q', 37),   # middle X
    (311.7,  14.0): ('V', 14),   # Q under right loop top
    (130.9,  18.0): ('V', 6),    # Q under left loop top
    (262.0,  51.2): ('V', 12),   # Q under right loop
    (174.0,  52.0): ('Q', 14),   # Q over left loop
    (174.0,  75.1): ('Q', 26),
    (262.0,  75.9): ('V', 12),   # Q under right loop
    (174.0, 105.4): ('Q', 38),   # Q over left loop
    (262.0, 107.3): ('Q', 22),   # Q over right loop
    (174.0, 131.9): ('V', 8),    # Q under left loop
    (160.2, 132.7): ('V', 9),    # Q under arc A
    (174.0, 152.4): ('V', 8),    # Q under left loop
    (173.0, 152.5): ('V', 9),    # Q under arc A
    (174.0, 117.0): ('V', 8),    # arc A under the left loop
    (262.0, 194.0): ('V', 23),   # arc B over the right loop
}


def find_crossings():
    S = {k: segs(v) for k, v in CURVES.items()}
    out = []
    keys = ['Q', 'V']
    for a in range(len(keys)):
        for b in range(a, len(keys)):
            ka, kb = keys[a], keys[b]
            for i, s1 in enumerate(S[ka]):
                for j, s2 in enumerate(S[kb]):
                    if ka == kb and j <= i:
                        continue
                    r = inter(s1[0], s1[1], s2[0], s2[1])
                    if r:
                        t, u, pt = r
                        out.append({'a': (ka, i, t), 'b': (kb, j, u),
                                    'pt': (pt[0], -pt[1])})
    return out


def lookup_over(c):
    x, y = c['pt']
    best, bd = None, 1e9
    for (kx, ky), who in OVER.items():
        d = (kx - x) ** 2 + (ky - y) ** 2
        if d < bd:
            bd, best = d, who
    assert bd < 4.0, 'no over/under rule near %.1f,%.1f (nearest %.2f)' % (x, y, bd)
    return best


def build():
    cr = find_crossings()
    assert len(cr) == 20, len(cr)
    # order crossings along each curve
    along = {'Q': [], 'V': []}
    for n, c in enumerate(cr):
        for side in ('a', 'b'):
            k, i, t = c[side]
            along[k].append((i + t, n, side))
    for k in along:
        along[k].sort()
    # edge numbering: edge e follows the e-th crossing along the walk
    edge_after = {}
    e = 0
    for k in ('Q', 'V'):
        base = e
        m = len(along[k])
        for idx, (_, n, side) in enumerate(along[k]):
            edge_after[(k, idx)] = base + idx
        e = base + m
    def edge_in(k, idx):
        m = len(along[k]);  return edge_after[(k, (idx - 1) % m)]
    def edge_out(k, idx):
        return edge_after[(k, idx)]

    pos = {}
    for k in ('Q', 'V'):
        for idx, (_, n, side) in enumerate(along[k]):
            pos[(n, side)] = (k, idx)

    def direction(k, i):
        P = CURVES[k];  p, q = P[i], P[(i + 1) % len(P)]
        return (q[0] - p[0], q[1] - p[1])

    PD = []
    signs = []
    for n, c in enumerate(cr):
        ov = lookup_over(c)
        sides = {}
        for side in ('a', 'b'):
            k, i, t = c[side]
            sides[side] = (k, i)
        over_side = 'a' if sides['a'] == ov else 'b'
        under_side = 'b' if over_side == 'a' else 'a'
        assert sides[over_side] == ov, (sides, ov)
        ku, iu = sides[under_side];  ko, io = sides[over_side]
        u = direction(ku, iu);  v = direction(ko, io)
        cross = u[0] * v[1] - u[1] * v[0]
        ku_k, ku_idx = pos[(n, under_side)]
        ko_k, ko_idx = pos[(n, over_side)]
        ui, uo = edge_in(ku_k, ku_idx), edge_out(ku_k, ku_idx)
        oi, oo = edge_in(ko_k, ko_idx), edge_out(ko_k, ko_idx)
        PD.append((ui, oi, uo, oo) if cross > 0 else (ui, oo, uo, oi))
        signs.append(1 if cross > 0 else -1)
    return PD, cr, along


if __name__ == '__main__':
    PD, cr, along = build()
    print('crossings along Q:', len(along['Q']), ' along V:', len(along['V']))
    print('PD code (%d crossings):' % len(PD))
    print(PD)
