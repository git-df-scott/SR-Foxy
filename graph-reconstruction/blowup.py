"""Deck-collision search over false-twin blowups of small cores.

Every graph in Ivanov's family is a blowup: a small core graph C, with vertex
i replaced by an independent set of size s_i, all of whose members inherit i's
neighbourhood (false twins).  Blowups reach n = 20 and beyond while the search
space stays enumerable -- which is the point, since exhaustive enumeration of
all graphs dies at n = 13.

A deck collision between two non-isomorphic blowups is a counterexample to the
reconstruction conjecture.  Collisions are checked with nauty canonical forms,
so a reported hit is real.
"""
import deck
from itertools import combinations


def blow(core_g6, sizes):
    """Blow up each core vertex into an independent set of the given size."""
    m, edges = deck.g6_decode(core_g6)
    assert len(sizes) == m
    start, off = [], 0
    for s in sizes:
        start.append(off); off += s
    out = []
    for u, v in edges:
        for a in range(sizes[u]):
            for b in range(sizes[v]):
                out.append((start[u]+a, start[v]+b))
    return deck.g6_encode(off, out)


def compositions(n, k, lo=1):
    """All ordered k-tuples of integers >= lo summing to n."""
    if k == 1:
        if n >= lo: yield (n,)
        return
    for first in range(lo, n - lo*(k-1) + 1):
        for rest in compositions(n - first, k - 1, lo):
            yield (first,) + rest


def family(n, mmax, cores=None):
    """Every blowup of a core with <= mmax vertices totalling n vertices."""
    out = []
    for m in range(2, mmax+1):
        for c in (cores or deck.geng(m)):
            if len(deck.g6_decode(c)[0] if False else deck.g6_decode(c)) and deck.g6_decode(c)[0] != m:
                continue
            for s in compositions(n, m):
                out.append((c, s, blow(c, s)))
    return out


def scan(n, mmax):
    """Look for two non-isomorphic blowups on n vertices with identical decks."""
    fam = family(n, mmax)
    g6s = [f[2] for f in fam]
    canon = deck.canon_many(g6s)
    # de-duplicate isomorphic blowups before computing decks
    uniq, seen = [], set()
    for f, c in zip(fam, canon):
        if c not in seen:
            seen.add(c); uniq.append((f, c))
    ds = deck.decks([u[0][2] for u in uniq])
    buckets = {}
    for (f, c), d in zip(uniq, ds):
        buckets.setdefault(d, []).append((f[0], f[1], c))
    hits = {d: v for d, v in buckets.items() if len({x[2] for x in v}) > 1}
    return len(fam), len(uniq), hits
