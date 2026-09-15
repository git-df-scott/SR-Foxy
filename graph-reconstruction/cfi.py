"""Cai-Furer-Immerman pairs, as adversarial candidates for deck collisions.

CFI graphs are the standard construction of non-isomorphic graph pairs that
agree on every statistic visible to bounded-dimension Weisfeiler-Leman, i.e.
on all sufficiently local structure.  That is exactly the property a
reconstruction counterexample needs, so they are the principled place to look
once enumeration is out of reach: they scale to any size, where brute force
stops dead at 13 vertices.

Gadget for a vertex v of degree d, over its incident edge slots E(v):
  - edge vertices  e_v^0, e_v^1  for each e in E(v);
  - middle vertices m_v^S for each S subset of E(v) with |S| even;
  - m_v^S ~ e_v^1 if e in S, else m_v^S ~ e_v^0.
For each edge e={u,v} of the base graph, join e_u^i to e_v^i (untwisted) or
e_u^i to e_v^(1-i) (twisted).  Twisting an odd number of edges gives the
partner graph, which is non-isomorphic to the untwisted one for connected base
graphs.
"""
from itertools import combinations
import deck


def cfi(base_n, base_edges, twisted_edge=None):
    """Build the CFI graph over a base graph; twist one edge if given.

    Returns (n, edges) with vertices numbered 0..n-1.
    """
    inc = {v: [] for v in range(base_n)}
    for i, (u, v) in enumerate(base_edges):
        inc[u].append(i)
        inc[v].append(i)

    idx, edges = {}, []
    def node(key):
        if key not in idx:
            idx[key] = len(idx)
        return idx[key]

    for v in range(base_n):
        slots = inc[v]
        d = len(slots)
        for e in slots:                       # edge vertices, created up front
            node(('e', v, e, 0)); node(('e', v, e, 1))
        for size in range(0, d + 1, 2):       # middle vertices, even subsets
            for S in combinations(slots, size):
                m = node(('m', v, S))
                Sset = set(S)
                for e in slots:
                    edges.append((m, node(('e', v, e, 1 if e in Sset else 0))))

    for i, (u, v) in enumerate(base_edges):
        tw = (i == twisted_edge)
        for b in (0, 1):
            edges.append((node(('e', u, i, b)), node(('e', v, i, (1 - b) if tw else b))))

    n = len(idx)
    clean = sorted({(min(a, b), max(a, b)) for a, b in edges})
    return n, clean


def pair(base_n, base_edges):
    """The untwisted/twisted CFI pair as graph6 strings."""
    n0, e0 = cfi(base_n, base_edges, None)
    n1, e1 = cfi(base_n, base_edges, 0)
    return deck.g6_encode(n0, e0), deck.g6_encode(n1, e1)


BASES = {
    'K4':        (4, [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]),
    'C4':        (4, [(0,1),(1,2),(2,3),(3,0)]),
    'C5':        (5, [(0,1),(1,2),(2,3),(3,4),(4,0)]),
    'K33':       (6, [(0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5)]),
    'prism':     (6, [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)]),
    'theta':     (4, [(0,1),(0,2),(0,3),(1,2),(1,3)]),
    'path3':     (3, [(0,1),(1,2)]),
    'triangle':  (3, [(0,1),(1,2),(2,0)]),
}
