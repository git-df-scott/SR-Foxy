#!/usr/bin/env python3
"""Alexander polynomial by Fox calculus on the Wirtinger presentation.

Independent of BOTH the HFK calculator and spherogram's Seifert algorithm:
it reads the PD code, builds the Wirtinger presentation of the knot group,
abelianises the Fox derivatives (every meridian -> t), deletes one column and
takes the determinant.  Nothing here touches a Seifert surface or a Floer
complex, which is the point -- the audit needs a route that shares no
conventions with the thing being audited.

Self-validating: run this file directly to check it against knots whose
Alexander polynomial is in the tables.
"""
import sympy
from sympy import symbols, Matrix, expand, Poly

t = symbols('t')


def normalise(coeffs):
    c = [int(x) for x in coeffs]
    while c and c[-1] == 0:
        c.pop()
    while c and c[0] == 0:
        c.pop(0)
    if c and c[0] < 0:
        c = [-x for x in c]
    if c and c[0] > c[-1]:
        pass
    return c


def alexander_from_pd(pd):
    """PD code (4-tuples, SnapPy/KnotTheory convention) -> normalised Delta coeffs.

    Each crossing X[a,b,c,d] has arcs labelled by their endpoints.  The arcs of
    the diagram are the edges between consecutive undercrossings; we take the
    arc labels directly from the PD entries and identify them into arcs by
    walking the overstrands.  For a crossing with under-in u, over o and
    under-out v, the Wirtinger relation is v = o^{+-1} u o^{-+1}, whose
    abelianised Fox derivatives give the row
        d/du = t,   d/do = 1 - t,   d/dv = -1
    (signs of the o-entry flip with the crossing sign; the determinant is
    unchanged up to a unit, which `normalise` removes).
    """
    pd = [tuple(int(x) for x in c) for c in pd]
    n = len(pd)
    labels = sorted({x for c in pd for x in c})
    m = len(labels)
    idx = {l: i for i, l in enumerate(labels)}

    # Union-find over arc labels: at a crossing the OVER strand keeps its label
    # through the crossing, so its two labels are identified.
    parent = list(range(m))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[ra] = rb

    for a, b, c, d in pd:
        # PD convention X[a,b,c,d]: a is under-in, c is under-out;
        # b,d are the over strand's two labels (which one is in/out depends on sign)
        union(idx[b], idx[d])

    arcs = {}
    for l in labels:
        r = find(idx[l])
        arcs.setdefault(r, len(arcs))
    def arc(l):
        return arcs[find(idx[l])]
    na = len(arcs)

    rows = []
    for a, b, c, d in pd:
        u, v, o = arc(a), arc(c), arc(b)
        row = [0] * na
        row[u] += t
        row[o] += (1 - t)
        row[v] += -1
        rows.append(row)
    M = Matrix(rows)
    # delete one column; any column gives the same answer up to a unit
    M = M[:, 1:]
    # square it up: n relations, na-1 columns; for a knot diagram n == na
    k = min(M.rows, M.cols)
    det = expand(M[:k, :k].det())
    if det == 0:
        return None
    p = Poly(det, t)
    return normalise(p.all_coeffs())


CONTROLS = {
    '3_1': [1, -1, 1],
    '4_1': [1, -3, 1],
    '5_2': [2, -3, 2],
    '6_1': [2, -5, 2],
    '6_2': [1, -3, 3, -3, 1],
    '6_3': [1, -3, 5, -3, 1],
    '7_4': [4, -7, 4],
    '8_8': [2, -6, 9, -6, 2],
}

if __name__ == '__main__':
    import snappy, json, sys
    ok = True
    for name, want in CONTROLS.items():
        got = alexander_from_pd(snappy.Link(name).PD_code())
        good = got == want or (got == want[::-1])
        ok = ok and good
        print(('PASS ' if good else 'FAIL ') + f'{name}: got {got} want {want}')
    print('\ncontrols_pass =', ok)
    sys.exit(0 if ok else 1)
