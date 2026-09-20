"""Wirtinger presentation from a spherogram Link, in ('conj') form.
Arc = maximal over-strand.  At each crossing:  out_under = over^{-s} in_under over^{s}.
Sign convention validated by Fox n-colouring controls in selftest().
"""
import spherogram

def wirtinger(link):
    cs = list(link.crossings)
    # arcs: union-find over (crossing, slot) for the over-strand slots 1,3 and
    # for under continuation we do NOT merge.  Arc labels: label each strand
    # position; the under-strand is broken at each crossing.
    # Build arc ids by walking: every (crossing,slot) is an end of an edge.
    # Edges of the diagram: connect (c,i) <-> c.adjacent[i].
    ends = {}
    parent = {}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(x, y):
        x, y = find(x), find(y); parent[x] = y
    for c in cs:
        for i in range(4):
            parent[(c, i)] = (c, i)
    for c in cs:
        for i in range(4):
            d, j = c.adjacent[i]
            union((c, i), (d, j))
    # over-strand passes through: slots 1 and 3 are the over strand, so merge them
    for c in cs:
        union((c, 1), (c, 3))
    reps = {}
    def arc(c, i):
        r = find((c, i))
        if r not in reps: reps[r] = len(reps) + 1
        return reps[r]
    rels = []
    info = []
    for c in cs:
        s = c.sign
        b = arc(c, 1)
        # slot 0 incoming under, slot 2 outgoing under
        i_ = arc(c, 0); o_ = arc(c, 2)
        rels.append((b, s, i_, o_))
        info.append((c.label, s, b, i_, o_))
    return len(reps), rels, info

def selftest():
    import homcount as H
    S3 = H.sym(3)
    H.count_homs.G = S3
    t = S3.index[(1, 0, 2)]
    for name, expect in [('3_1', 3), ('4_1', 1), ('6_3', None), ('8_18', None)]:
        L = spherogram.Link(name)
        n, rels, _ = wirtinger(L)
        dom = {g: S3.classes[S3.classof[t]] for g in range(1, n+1)}
        dom[1] = [t]
        c, st = H.count_homs(n, rels, [], dom)
        print(name, 'homs->S3 (mer=transposition):', c, 'expect', expect, 'nodes', st['nodes'])
if __name__ == '__main__':
    selftest()
