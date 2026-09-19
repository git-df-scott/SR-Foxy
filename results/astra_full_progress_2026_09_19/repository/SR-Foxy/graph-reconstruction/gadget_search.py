"""Search for a selector gadget that would give a reconstruction counterexample.

Reduction (from the exact-deficit computation in results_selector_scan.json):
in Ivanov's framework the deficit never reaches 0 because the selector's own
vertex-deleted cards never match.  Write a gadget as a graph S together with
sigma: V(S) -> nonempty subsets of the r ports; port class i is a false-twin
class joined to {v : i in sigma(v)}.  A port permutation tau extends to the
whole graph exactly when some phi in Aut(S) satisfies sigma(phi(v)) = tau(sigma(v)).

    Ext(S, sigma) = { tau : exists phi in Aut(S), sigma . phi = tau . sigma }

For the pair G = S(a), H = S(tau0 . a) with tau0 an odd permutation:
  (a)  tau0 NOT in Ext(S, sigma)              -- else G = H, no pair at all
  (b)  tau0 in Ext(S - v, sigma) for EVERY v  -- else that selector card is unmatched

A gadget meeting (a) and (b) kills the selector part of the deficit outright.
It is necessary, not sufficient: the class cards must also all match.  But
without it no construction of this shape can ever reach deficit 0.
"""
import itertools, subprocess, deck


def auts(n, edges):
    """All automorphisms of a small graph, as tuples (brute force, n <= 7)."""
    adj = [[False]*n for _ in range(n)]
    for u, v in edges:
        adj[u][v] = adj[v][u] = True
    out = []
    for p in itertools.permutations(range(n)):
        if all(adj[u][v] == adj[p[u]][p[v]] for u in range(n) for v in range(u+1, n)):
            out.append(p)
    return out


def ext(n, edges, sigma, r):
    """Port permutations induced by automorphisms of the gadget."""
    found = set()
    for p in auts(n, edges):
        tau = {}
        ok = True
        for v in range(n):
            src, dst = sorted(sigma[v]), sorted(sigma[p[v]])
            if len(src) != len(dst):
                ok = False; break
            # tau must map sigma(v) onto sigma(phi(v)); try every bijection
        if not ok:
            continue
        # build tau candidates consistently across all vertices
        for cand in itertools.permutations(range(1, r+1)):
            t = {i+1: cand[i] for i in range(r)}
            if all({t[i] for i in sigma[v]} == set(sigma[p[v]]) for v in range(n)):
                found.add(cand)
    return found


def delete(n, edges, v):
    m = {u: (u if u < v else u-1) for u in range(n) if u != v}
    return n-1, [(m[a], m[b]) for a, b in edges if a != v and b != v], m


def search(r=4, mmax=5, tau0=None, verbose=True):
    """Enumerate gadgets on <= mmax vertices; report any meeting (a) and (b)."""
    if tau0 is None:
        tau0 = tuple([2, 1] + list(range(3, r+1)))      # the transposition (1 2)
    subsets = [s for k in range(1, r+1) for s in itertools.combinations(range(1, r+1), k)]
    hits, tested = [], 0
    for m in range(2, mmax+1):
        for g6 in deck.geng(m):
            n, es = deck.g6_decode(g6)
            edges = sorted(es)
            for sigma in itertools.product(subsets, repeat=m):
                tested += 1
                if tau0 in ext(n, edges, sigma, r):
                    continue                              # fails (a)
                ok = True
                for v in range(n):
                    nn, ee, mp = delete(n, edges, v)
                    sig2 = [sigma[u] for u in range(n) if u != v]
                    if nn == 0 or tau0 not in ext(nn, ee, sig2, r):
                        ok = False; break                 # fails (b)
                if ok:
                    hits.append((g6, sigma))
                    if verbose:
                        print('   HIT  m=%d  %s  sigma=%s' % (m, g6, sigma), flush=True)
        if verbose:
            print('  m=%d done, gadgets tested so far %d, hits %d' % (m, tested, len(hits)), flush=True)
    return tested, hits
