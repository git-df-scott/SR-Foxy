"""L_{n,1} of GST for general n, from Figure 1 of arXiv:1103.1601.

Geometry:
  * each bundle is an n-turn planar SPIRAL (radial positions 1=outer..n=inner).
    A planar n-turn spiral is the (n,1) curve, so its closure is the unknot;
    the +-1 twist box adds a full twist, sending it to T_{n,n+1}.  The box
    therefore carries Delta^{+-2} = (s_1...s_{n-1})^{+-n}.
  * the spiral step from turn i to turn i+1 sits in the window between the two
    arc attachments, where Q never goes.
  * Q's polyline is independent of n: it stays inside the innermost turn on
    both sides and its gaps span every turn's edge.
Green over/under with a bundle is uniform across the n strands, as drawn.
"""
DELTA = 5.0

# ----------------------------------------------------------------- Q (green)
Q = [
    (131.1, 5.1), (194.9, 5.0), (236.2, 50.7),
    (256.1, 51.2), (307.1, 51.2), (320.7, 51.4), (377.3, 51.9),
    (375.7, 152.9), (304.0, 152.3), (228.1, 152.4), (178.5, 152.4),
    (146.5, 152.7), (73.7, 153.2), (72.1, 52.6), (122.3, 52.0),
    (198.8, 52.0), (213.2, 39.4), (227.3, 27.3), (250.7, 1.9), (311.9, 1.8),
    (311.5, 10.2), (312.7, 35.3), (314.3, 107.8), (237.6, 107.0),
    (224.9, 94.3), (217.2, 86.5), (205.0, 75.1), (128.6, 75.1),
    (102.8, 75.5), (103.6, 134.1), (141.4, 133.8), (177.4, 131.7),
    (303.1, 131.7), (354.8, 132.0), (355.9, 76.3), (320.4, 76.0),
    (288.8, 76.0), (236.0, 75.8), (205.5, 105.4), (129.6, 105.4),
    (129.9, 85.1), (128.2, 47.7), (128.3, 38.9), (131.4, 13.7),
]


def braid_polyline(x0, y0, x1, y1, n, word, sign):
    """n strands running vertically from y0 to y1 across x0..x1, carrying `word`
    (a list of 1-based generator indices).  Returns (paths, overs) where paths[i]
    is the polyline of the strand starting at position i, and overs is a list of
    (approx point, 'which position is over')."""
    xs = [x0 + (x1 - x0) * (i / max(n - 1, 1)) for i in range(n)]
    if n == 1:
        xs = [x0]
    m = len(word)
    paths = [[(xs[i], y0)] for i in range(n)]
    where = list(range(n))          # where[i] = current lane of strand i
    overs = []
    for k, g in enumerate(word):
        ya = y0 + (y1 - y0) * (k / max(m, 1))
        yb = y0 + (y1 - y0) * ((k + 1) / max(m, 1))
        a, b = g - 1, g
        ia = where.index(a); ib = where.index(b)
        for i in range(n):
            if i == ia:
                paths[i].append((xs[b], yb)); where[i] = b
            elif i == ib:
                paths[i].append((xs[a], yb)); where[i] = a
            else:
                paths[i].append((xs[where[i]], yb))
        pt = ((xs[a] + xs[b]) / 2.0, (ya + yb) / 2.0)
        # sign>0: the strand moving to the RIGHT passes over
        overs.append((pt, ia if sign > 0 else ib))
    for i in range(n):
        paths[i].append((xs[where[i]], y1))
    return paths, overs, where


def full_twist_word(n):
    """Delta^2 = (s_1 s_2 ... s_{n-1})^n, plus the spiral shift s_1..s_{n-1}."""
    delta = list(range(1, n))
    return delta * (n + 1)
