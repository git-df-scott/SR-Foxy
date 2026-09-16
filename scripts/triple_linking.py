#!/usr/bin/env python3
"""Milnor's triple linking number for a 3-component link, from the Conway
polynomial, plus a report on the Eisermann census shortlist.

For a 3-component link with all pairwise linking numbers zero, the Conway
polynomial begins in degree 4 and

    [z^4] nabla_L(z) = mu-bar(123)^2

(Cochran, *Concordance invariance of coefficients of Conway's link
polynomial*, Invent. Math. 82 (1985); the degree-(n-1) coefficient is the
reduced linking-matrix determinant, which vanishes here).  Milnor's invariants
vanish for slice links, so a nonzero value rules a shortlist entry out of
being slice, and only entries with 0 stay live.

The Conway polynomial is obtained from a Seifert matrix: `det(V - tV^T)` is the
one-variable Alexander polynomial up to a unit `+- t^k`, and substituting
`t = s^2`, `z = s - 1/s` after symmetrising converts it.  The unit does not
affect whether a coefficient vanishes.

This is reported, not used to delete entries: the value is printed for every
shortlist member so the cut can be checked rather than trusted.

Usage: triple_linking.py <census.json> <out.json>
"""
import json, os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import snappy
from fractions import Fraction
from sagefree_slice_filter import _det_int


def alexander_coeffs(link):
    """det(V - t V^T) over Z, low degree first, by exact interpolation.

    sympy's symbolic determinant is far too slow on the larger Seifert
    matrices in a link census; the determinant is a polynomial of degree at
    most n in t, so evaluating it at n+1 integer points with an exact integer
    determinant and interpolating is both faster and exact.
    """
    V = link.seifert_matrix()
    n = len(V)
    if n == 0:
        return [1]
    xs = list(range(-(n // 2), -(n // 2) + n + 1))
    ys = []
    for x in xs:
        M = [[V[i][j] - x * V[j][i] for j in range(n)] for i in range(n)]
        ys.append(_det_int(M))
    # Lagrange interpolation over Q, exactly
    coeffs = [Fraction(0)] * (n + 1)
    for i, xi in enumerate(xs):
        denom = 1
        for j, xj in enumerate(xs):
            if i != j:
                denom *= (xi - xj)
        # basis polynomial prod_{j != i} (t - xj)
        basis = [Fraction(1)]
        for j, xj in enumerate(xs):
            if i == j:
                continue
            new = [Fraction(0)] * (len(basis) + 1)
            for k, c in enumerate(basis):
                new[k + 1] += c
                new[k] -= c * xj
            basis = new
        scale = Fraction(ys[i], denom)
        for k, c in enumerate(basis):
            coeffs[k] += c * scale
    out = []
    for c in coeffs:
        assert c.denominator == 1, 'interpolation did not land in Z'
        out.append(int(c))
    return out


def conway_coefficients(link):
    """Coefficients of nabla_L(z), lowest degree first, up to sign."""
    c = alexander_coeffs(link)                  # det(V - t V^T), low to high
    while c and c[0] == 0:
        c = c[1:]
    while c and c[-1] == 0:
        c = c[:-1]
    if not c:
        return [0]
    d = len(c) - 1
    # f(t) = sum c_k t^k.  Put s^2 = t and divide by s^d so the Laurent
    # polynomial in s is symmetric; then rewrite in z = s - 1/s.
    lau = {}
    for k, coeff in enumerate(c):
        lau[2 * k - d] = lau.get(2 * k - d, 0) + coeff
    out = []
    # repeatedly strip the top power of s using z^m = (s - 1/s)^m
    from math import comb
    while any(v != 0 for v in lau.values()):
        m = max(e for e, v in lau.items() if v != 0)
        if m < 0:
            break
        a = lau[m]
        while len(out) <= m:
            out.append(0)
        out[m] = a
        for j in range(m + 1):
            e = m - 2 * j
            lau[e] = lau.get(e, 0) - a * ((-1) ** j) * comb(m, j)
    return out


def main():
    census_path, out = sys.argv[1], sys.argv[2]
    d = json.load(open(census_path))
    rec = {'date': datetime.datetime.utcnow().isoformat() + 'Z',
           'source': census_path,
           'test': ('[z^4] nabla_L = mu-bar(123)^2 for a 3-component link with '
                    'vanishing linking numbers; Milnor invariants vanish for '
                    'slice links, so nonzero rules out slice'),
           'rows': [], 'still_live': []}
    for row in d.get('shortlist', []):
        L = snappy.Link([tuple(c) for c in row['pd_code']])
        try:
            nab = conway_coefficients(L)
        except Exception as e:
            rec['rows'].append({'name': row['name'],
                                'error': f'{type(e).__name__}: {e}'})
            continue
        z2 = nab[2] if len(nab) > 2 else 0
        z4 = nab[4] if len(nab) > 4 else 0
        entry = {'name': row['name'], 'crossings': row['crossings'],
                 'null_V': row['null_V'], 'conway': nab[:8],
                 'z2_coefficient': z2, 'mu_bar_123_squared': z4,
                 'slice_ruled_out_by_mu_bar': z4 != 0}
        rec['rows'].append(entry)
        if z4 == 0:
            rec['still_live'].append(row['name'])
        print(f"{row['name']:12s} {row['crossings']:3d} cr  nabla = {nab[:7]}  "
              f"mu123^2 = {z4}  " +
              ('RULED OUT of slice' if z4 else '*** STILL LIVE ***'), flush=True)
    rec['summary'] = {'examined': len(rec['rows']),
                      'still_live': len(rec['still_live'])}
    json.dump(rec, open(out, 'w'), indent=1)
    print('still live:', rec['still_live'], flush=True)
    print('wrote', out)


if __name__ == '__main__':
    main()
