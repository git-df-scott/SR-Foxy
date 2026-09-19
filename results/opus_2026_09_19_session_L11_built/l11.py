"""L_{1,1} from GST Figure 1 (arXiv:1103.1601, Ln1.eps), n = 1.

Coordinates are taken from the vector path data of Ln1.pdf.  At n = 1 each
"n-stranded spiral" is a single loop, so the two bundles become one rounded
rectangle each, joined by the two connecting arcs into a single curve V_1.
Green is the square knot Q.  Gaps in the drawn paths are undercrossings.
"""
import math

# ---------------------------------------------------------------- curve Q
# Traversed in the order the drawn segments actually connect up; the path
# closes, which is the first consistency check on the reading of the figure.
Q = [
    (131.1, 5.1), (194.9, 5.0),          # top horizontal
    (236.2, 50.7),                        # diagonal down-right  (over at upper X)
    (256.1, 51.2), (307.1, 51.2),         # y=51 run, under right loop
    (320.7, 51.4), (377.3, 51.9),         # into right chain 1
    (375.7, 152.9), (304.0, 152.3),
    (228.1, 152.4), (178.5, 152.4),       # y=152 run, over right loop, under left loop
    (146.5, 152.7), (73.7, 153.2),        # left chain 1
    (72.1, 52.6), (122.3, 52.0),
    (198.8, 52.0),                        # y=52 run, over left loop
    (213.2, 39.4), (227.3, 27.3),         # up-right, under at upper X
    (250.7, 1.9), (311.9, 1.8),           # top horizontal right
    (311.5, 10.2), (312.7, 35.3),         # down, under right loop top
    (314.3, 107.8),                       # long vertical, over y=51 and y=76
    (237.6, 107.0),                       # y=107 run, over right loop
    (224.9, 94.3), (217.2, 86.5),         # up-left, under at middle X
    (205.0, 75.1), (128.6, 75.1),         # y=75 run, over left loop
    (102.8, 75.5), (103.6, 134.1),        # left chain 2
    (141.4, 133.8), (177.4, 131.7),       # under left loop
    (303.1, 131.7),                       # y=131.7 run, over right loop
    (354.8, 132.0), (355.9, 76.3),        # right chain 2
    (320.4, 76.0), (288.8, 76.0),         # y=76 run, under vertical then right loop
    (236.0, 75.8),
    (205.5, 105.4),                       # diagonal down-left (over at middle X)
    (129.6, 105.4), (129.9, 85.1),        # y=105.4 run then vertical up
    (128.2, 47.7), (128.3, 38.9),
    (131.4, 13.7),                        # under left loop top, closes
]

# ---------------------------------------------------------------- curve V_1
# left loop: outer end (174,180) -> all the way round -> inner end (174,154)
V = [
    (174.0, 180.0), (174.0, 206.0), (155.0, 223.0), (36.0, 223.0),
    (17.0, 206.0), (17.0, 34.0), (36.0, 18.0), (155.0, 18.0),
    (174.0, 34.0), (174.0, 154.0),
    # arc A: out of the inner end, under the left loop, across to the right loop
    (150.0, 117.0), (246.0, 117.0), (262.0, 128.0),
    # right loop: up the left edge, round, back down to its other end
    (262.0, 30.0), (281.0, 14.0), (400.0, 14.0), (419.0, 30.0),
    (419.0, 202.0), (400.0, 218.0), (281.0, 218.0), (262.0, 202.0),
    (262.0, 156.0),
    # arc B: inside to x=287, down to y=194, back left over the right loop edge
    (287.0, 156.0), (287.0, 194.0), (190.0, 194.0),
]


def segs(poly):
    return [(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))]


def inter(p1, p2, p3, p4):
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    d = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)
    if abs(d) < 1e-12:
        return None
    t = ((x3 - x1) * (y4 - y3) - (y3 - y1) * (x4 - x3)) / d
    u = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / d
    e = 1e-9
    if e < t < 1 - e and e < u < 1 - e:
        return t, u, (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    return None


if __name__ == '__main__':
    SQ, SV = segs(Q), segs(V)
    found = []
    for i, a in enumerate(SQ):
        for j, b in enumerate(SQ):
            if j <= i:
                continue
            r = inter(a[0], a[1], b[0], b[1])
            if r:
                found.append(('QQ', i, j, r[2]))
    for i, a in enumerate(SQ):
        for j, b in enumerate(SV):
            r = inter(a[0], a[1], b[0], b[1])
            if r:
                found.append(('QV', i, j, r[2]))
    for i, a in enumerate(SV):
        for j, b in enumerate(SV):
            if j <= i:
                continue
            r = inter(a[0], a[1], b[0], b[1])
            if r:
                found.append(('VV', i, j, r[2]))
    import collections
    print('Q points', len(Q), ' V points', len(V))
    print('total crossings found:', len(found))
    print(collections.Counter(f[0] for f in found))
    for f in sorted(found, key=lambda z: (z[0], z[3][1])):
        print('  %s  segQ/V %3d %3d  at (%6.1f,%6.1f)' % (f[0], f[1], f[2], f[3][0], f[3][1]))
