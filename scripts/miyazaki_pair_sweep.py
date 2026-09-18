#!/usr/bin/env python3
"""Search for ANY concordant pair of distinct prime fibered knots with irreducible
Alexander polynomial - each such pair is a slice-ribbon counterexample generator.

THE CRITERION.  Miyazaki Theorem 5.5, quoted verbatim in ERRATA_2026-09-16.md
from Abe-Tagami Appendix A: if K_1, ..., K_n are prime fibered knots in homotopy
3-spheres, each satisfying one of

  * K_i is minimal with respect to >= among all fibered knots in homology
    spheres, or
  * there is no f(t) in Z[t] \\ {+-t^k} with f(t) f(t^{-1}) | Delta_{K_i}(t),

and K_1 # ... # K_n is HOMOTOPICALLY RIBBON, then the indices pair up with
K_{i_s} = conj(K_{j_s}).

An IRREDUCIBLE Delta satisfies the second alternative.  Proof: f of degree 1
gives a degree-2 factor of Delta, and f of degree d >= 2 with f f* | Delta of
degree 2d forces Delta = f f* up to units - both contradict irreducibility; a
constant f needs f^2 | content(Delta) = 1.

CONSEQUENCE.  For DISTINCT prime fibered J, J' with irreducible Alexander
polynomials, J # (-J') is never homotopy-ribbon, hence never ribbon.  So if any
such pair is smoothly concordant, J # (-J') is slice and not ribbon, and the
slice-ribbon conjecture is FALSE.

This is much wider than the Abe-Tagami family, which is one guess at such a pair.

FOX-MILNOR PINS THE SEARCH.  A concordance forces Delta_J * Delta_{J'} =
f(t) f(1/t).  With both factors irreducible, f must be Delta_J up to units and
then Delta_{J'} = Delta_J^* = Delta_J.  So a concordant pair necessarily SHARES
one irreducible Alexander polynomial.  That turns the search into a grouping
problem.

METHOD.  One HFK call per census knot gives fiberedness, genus, tau, nu, epsilon
and (via the graded Euler characteristic) Delta.  Keep the fibered knots with
irreducible Delta, group them by Delta, and inside each group report the pairs
that agree on every cheap concordance invariant.  Hyperbolic knots are prime, so
primality is automatic.

SCOPE.  All hyperbolic knots of at most 14 crossings.  Surviving pairs are
CANDIDATES needing much stronger tests (signatures, Casson-Gordon, Floer local
equivalence); a null result is a bounded negative, not a theorem.
"""
import json
import sys
import time
from collections import defaultdict

import snappy
import sympy as sp

t = sp.Symbol("t")
OUT = "/tmp/claude-0/miyazaki_pair_sweep.json"


def alex_from_ranks(ranks):
    """Alexander polynomial as the graded Euler characteristic of HFK-hat."""
    poly = defaultdict(int)
    for (A, M), r in ranks.items():
        poly[A] += ((-1) ** M) * r
    lo = min(poly)
    c = sp.Poly(sum(v * t ** (A - lo) for A, v in poly.items()), t).all_coeffs()[::-1]
    while c and c[0] == 0:
        c = c[1:]
    if sum(c) < 0:
        c = [-x for x in c]
    return tuple(int(x) for x in c)


def main():
    census = snappy.HTLinkExteriors(cusps=1)
    n = len(census)
    print("census size:", n)
    sys.stdout.flush()

    rows = []
    t0 = time.time()
    for i in range(n):
        if i and i % 10000 == 0:
            print(f"  {i}/{n}  {time.time()-t0:.0f}s  kept={len(rows)}")
            sys.stdout.flush()
        try:
            h = census[i].link().knot_floer_homology()
        except Exception:
            continue
        if not h.get("fibered"):
            continue
        ranks = dict(h["ranks"])
        d = alex_from_ranks(ranks)
        if len(d) < 3:
            continue                       # Delta = 1, outside the criterion
        if not sp.Poly(sum(v * t**k for k, v in enumerate(d)), t).is_irreducible:
            continue
        rows.append({"i": i, "name": census[i].name(), "delta": d,
                     "genus": h.get("seifert_genus"), "tau": h.get("tau"),
                     "nu": h.get("nu"), "eps": h.get("epsilon"),
                     "rank": sum(ranks.values()),
                     "ranks": {f"{A},{M}": r for (A, M), r in sorted(ranks.items())}})

    print(f"fibered knots with irreducible Delta: {len(rows)}  ({time.time()-t0:.0f}s)")
    groups = defaultdict(list)
    for r in rows:
        groups[r["delta"]].append(r)
    multi = {k: v for k, v in groups.items() if len(v) > 1}
    print("Alexander polynomials shared by more than one such knot:", len(multi))

    pairs = []
    for d, v in sorted(multi.items(), key=lambda kv: -len(kv[1])):
        for a in range(len(v)):
            for b in range(a + 1, len(v)):
                A, B = v[a], v[b]
                if (A["tau"], A["nu"], A["eps"]) == (B["tau"], B["nu"], B["eps"]):
                    pairs.append({"delta": list(d), "genus": A["genus"],
                                  "tau": A["tau"], "nu": A["nu"], "eps": A["eps"],
                                  "a": A["name"], "b": B["name"],
                                  "rank_a": A["rank"], "rank_b": B["rank"],
                                  "same_hfk": A["ranks"] == B["ranks"]})
    print("CANDIDATE PAIRS (shared irreducible Delta, matching tau/nu/epsilon):",
          len(pairs))
    with open(OUT, "w") as fh:
        json.dump({"searched": n, "n_fibered_irreducible": len(rows),
                   "n_shared_delta": len(multi), "n_pairs": len(pairs),
                   "pairs": pairs[:2000], "rows": rows,
                   "scope_caveat": "hyperbolic knots of at most 14 crossings;"
                                   " a null result is a bounded negative"}, fh)
    for p in pairs[:30]:
        print("   ", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
