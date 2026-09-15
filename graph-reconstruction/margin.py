"""How close does the reconstruction conjecture come to failing?

Two non-isomorphic n-vertex graphs sharing all n cards ARE a counterexample.
So the honest quantity to measure is the margin: the largest number of common
cards attained by a non-isomorphic pair.  Margin n-1 would mean the conjecture
survives by a single card; margin n is a disproof.

Finding pairs that share at least n-k cards does not need all pairs.  Two
graphs share >= n-k cards exactly when their decks have a common
sub-multiset of size n-k, so bucketing every graph by every way of dropping k
of its cards turns the pair search into hashing: O(C(n,k)) keys per graph
rather than O(N^2) comparisons.
"""
import deck
from collections import Counter
from itertools import combinations


def drop_keys(d, k):
    """Every sub-multiset of the deck d obtained by dropping k cards."""
    return {tuple(sorted(d[:i] + d[i+1:])) for i in range(len(d))} if k == 1 else \
           {tuple(sorted(x)) for x in combinations(d, len(d) - k)}


def max_common_cards(g6_list, kmax=3, report=None):
    """Largest common-card count achieved by a non-isomorphic pair.

    Scans k = 0, 1, 2, ... : k=0 asks for identical decks (a counterexample).
    Returns (best_common, witnesses) where witnesses are canonical pairs.
    """
    ds = deck.decks(g6_list)
    cs = deck.canon_many(g6_list)
    n = len(ds[0]) if ds else 0
    for k in range(0, kmax + 1):
        buckets = {}
        for d, c in zip(ds, cs):
            for key in drop_keys(d, k):
                buckets.setdefault(key, set()).add(c)
        hits = {key: v for key, v in buckets.items() if len(v) > 1}
        if report:
            report(k, n - k, len(hits))
        if hits:
            wit = set()
            for v in hits.values():
                sv = sorted(v)
                for i in range(len(sv)):
                    for j in range(i + 1, len(sv)):
                        wit.add((sv[i], sv[j]))
            return n - k, wit
    return None, set()


def verify_pair(a, b):
    """Independently re-check a reported pair: non-isomorphic, common-card count."""
    ca, cb = deck.canon_many([a, b])
    da, db = deck.decks([a, b])
    common = sum((Counter(da) & Counter(db)).values())
    return {'non_isomorphic': ca != cb, 'n': len(da),
            'common_cards': common, 'identical_decks': da == db}
