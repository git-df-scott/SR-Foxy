"""Count homomorphisms from a Wirtinger-style group presentation into a finite
permutation group, with a distinguished meridian generator pinned to one element.

Generators are 1..n. Two kinds of relations:
  ('conj', b, s, i, o)   meaning  gen[o] = gen[b]^(-s) * gen[i] * gen[b]^(s)
  ('word', [signed ints]) meaning  the reduced word evaluates to identity.
No topology is assumed; this is pure combinatorial group theory on the input.
"""
import itertools, sys
from functools import lru_cache

class PermGroup:
    def __init__(self, perms):
        perms = sorted(set(perms))
        self.elts = perms
        self.index = {p: i for i, p in enumerate(perms)}
        n = len(perms)
        self.n = n
        deg = len(perms[0])
        self.mul = [[0]*n for _ in range(n)]
        for i, p in enumerate(perms):
            for j, q in enumerate(perms):
                # (p*q)(x) = p(q(x))
                self.mul[i][j] = self.index[tuple(p[q[x]] for x in range(deg))]
        self.inv = [0]*n
        for i, p in enumerate(perms):
            ip = [0]*deg
            for x in range(deg):
                ip[p[x]] = x
            self.inv[i] = self.index[tuple(ip)]
        self.e = self.index[tuple(range(deg))]
        # conjugacy classes
        seen = set(); self.classes = []
        for i in range(n):
            if i in seen: continue
            cl = sorted({self.mul[self.mul[j][i]][self.inv[j]] for j in range(n)})
            for c in cl: seen.add(c)
            self.classes.append(cl)
        self.classof = {}
        for ci, cl in enumerate(self.classes):
            for c in cl: self.classof[c] = ci

    @staticmethod
    def generated(gens):
        deg = len(gens[0])
        idp = tuple(range(deg))
        seen = {idp}; frontier = [idp]
        while frontier:
            nxt = []
            for p in frontier:
                for g in gens:
                    q = tuple(g[p[x]] for x in range(deg))
                    if q not in seen:
                        seen.add(q); nxt.append(q)
            frontier = nxt
        return PermGroup(sorted(seen))

def sym(k):
    return PermGroup([tuple(p) for p in itertools.permutations(range(k))])

def alt(k):
    def parity(p):
        p = list(p); s = 0
        for i in range(len(p)):
            while p[i] != i:
                j = p[i]; p[i], p[j] = p[j], p[i]; s += 1
        return s % 2
    return PermGroup([tuple(p) for p in itertools.permutations(range(k)) if parity(p) == 0])

def count_homs(ngens, conj_rels, word_rels, domains, verbose=False):
    """domains: dict gen -> list of allowed element indices (required for all gens)."""
    G = count_homs.G
    mul, inv = G.mul, G.inv
    val = [None]*(ngens+1)
    # relation occurrence index
    occ = [[] for _ in range(ngens+1)]
    for ri, (b, s, i, o) in enumerate(conj_rels):
        for g in (b, i, o): occ[g].append(ri)
    wocc = [[] for _ in range(ngens+1)]
    for ri, w in enumerate(word_rels):
        for x in set(abs(y) for y in w): wocc[x].append(ri)
    stats = {'nodes': 0, 'sols': 0}

    def evalword(w):
        r = G.e
        for x in w:
            v = val[abs(x)]
            if v is None: return None
            r = mul[r][v if x > 0 else inv[v]]
        return r

    def propagate(pending, newly):
        """Assign forced generators. Returns True on success, False on contradiction.
        Every generator it assigns is appended to `newly` (even on failure) so the
        caller can always undo."""
        queue = list(pending)
        while queue:
            ri = queue.pop()
            b, s, i, o = conj_rels[ri]
            vb, vi, vo = val[b], val[i], val[o]
            if vb is None: continue
            cb = vb if s > 0 else inv[vb]
            if vi is not None:
                u = mul[mul[inv[cb]][vi]][cb]
                if vo is None:
                    if u not in domset[o]: return False
                    val[o] = u; newly.append(o); queue.extend(occ[o])
                elif vo != u: return False
            elif vo is not None:
                u = mul[mul[cb][vo]][inv[cb]]
                if u not in domset[i]: return False
                val[i] = u; newly.append(i); queue.extend(occ[i])
        return True

    def check_words(touched):
        cand = set()
        for g in touched: cand.update(wocc[g])
        for ri in cand:
            r = evalword(word_rels[ri])
            if r is not None and r != G.e: return False
        return True

    domset = {g: set(v) for g, v in domains.items()}
    order = sorted(range(1, ngens+1), key=lambda g: -len(occ[g]))

    def search():
        stats['nodes'] += 1
        pick = None
        for g in order:
            if val[g] is None: pick = g; break
        if pick is None:
            for w in word_rels:
                if evalword(w) != G.e: return
            stats['sols'] += 1
            return
        for v in domains[pick]:
            val[pick] = v
            newly = []
            ok = propagate(occ[pick], newly)
            if ok and check_words([pick]+newly):
                search()
            for g in newly: val[g] = None
            val[pick] = None

    pre = [g for g in range(1, ngens+1) if len(domains[g]) == 1]
    for g in pre: val[g] = domains[g][0]
    newly = []
    if not propagate(range(len(conj_rels)), newly): return 0, stats
    if not check_words(pre+newly): return 0, stats
    search()
    return stats['sols'], stats
