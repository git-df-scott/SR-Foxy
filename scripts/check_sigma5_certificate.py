#!/usr/bin/env python3
"""Independent checker for the Sigma_5 metabolizer certificate.

Reads results/opus_2026_09_17/sigma5_metabolizer_gate.json and re-verifies the
claim from the stored data alone, with no shared code: it takes the two 4x4
Gram matrices and the stored metabolizer generators, rebuilds the subgroup of
(Z/4)^8 they generate, and checks

  * the subgroup has order 256 = |G|^{1/2},
  * it is closed under addition and contains 0,
  * lambda_0 (+) (-lambda_1) vanishes on all 256^2 ordered pairs.

It deliberately does NOT import the generating script, does not recompute
Seifert matrices, and does not use the branched-cover machinery.  Its purpose
is to catch an error in that machinery's bookkeeping, not to re-derive the
Gram matrices; those are checked separately by the order/resultant agreement
recorded in cyclic_cover_linking_form_gate.json.

Usage: python3 scripts/check_sigma5_certificate.py [in.json]
Exit status 0 iff the certificate verifies.
"""
import json, sys
from fractions import Fraction

PATH = (sys.argv[1] if len(sys.argv) > 1
        else 'results/opus_2026_09_17/sigma5_metabolizer_gate.json')


def main():
    d = json.load(open(PATH))
    t = d['target']
    g0 = [[Fraction(x) for x in row] for row in t['gram_K_0']]
    g1 = [[Fraction(x) for x in row] for row in t['gram_K_1']]
    orders = list(t['H1_K_0']) + list(t['H1_K_1'])
    k = len(orders)
    assert k == 8 and orders == [4] * 8, orders
    n0 = len(g0)
    gram = [[Fraction(0)] * k for _ in range(k)]
    for i in range(n0):
        for j in range(n0):
            gram[i][j] = g0[i][j]
            gram[n0 + i][n0 + j] = -g1[i][j]      # the minus sign is the point

    def add(x, y):
        return tuple((x[a] + y[a]) % orders[a] for a in range(k))

    def pair(x, y):
        s = Fraction(0)
        for a in range(k):
            if x[a]:
                for b in range(k):
                    if y[b]:
                        s += x[a] * y[b] * gram[a][b]
        return s - int(s // 1)

    zero = tuple([0] * k)
    gens = [tuple(v) for v in t['metabolizer_generators']]
    M = {zero}
    for g in gens:
        mult, cur = [], zero
        while True:
            mult.append(cur)
            cur = add(cur, g)
            if cur == zero:
                break
        M = {add(s, m) for s in M for m in mult}
    M = sorted(M)

    total = 1
    for o in orders:
        total *= o
    want = int(round(total ** 0.5))
    checks = {
        'group_order': total,
        'required_metabolizer_order': want,
        'metabolizer_order': len(M),
        'order_ok': len(M) == want,
        'contains_zero': zero in set(M),
    }
    S = set(M)
    checks['closed_under_addition'] = all(add(x, y) in S for x in M for y in M)
    bad = [(x, y) for x in M for y in M if pair(x, y) != 0]
    checks['isotropic'] = not bad
    checks['pairs_checked'] = len(M) ** 2
    checks['first_failure'] = bad[0] if bad else None
    ok = (checks['order_ok'] and checks['contains_zero']
          and checks['closed_under_addition'] and checks['isotropic'])
    checks['CERTIFICATE_VERIFIES'] = ok
    print(json.dumps(checks, indent=1))
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
