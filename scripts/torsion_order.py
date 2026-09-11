#!/usr/bin/env python3
"""U-torsion order of HFK^- from SnapPy's UV=0 complex.

Juhasz-Miller-Zemke: for a ribbon knot J, fusion number F(J) >= Ord_U(J).
So a large torsion order is a LOWER BOUND on the number of bands in any
ribbon disk, and tells us how deep a band search must go.

Grading conventions (Zemke): gr_U(x) = M(x), gr_V(x) = M(x) - 2A(x);
U has (gr_U,gr_V) = (-2,0), V has (0,-2); the differential drops both by 1.
For an arrow a -> b carrying U^i V^j:   i = (M_b - M_a + 1)/2,
                                        j = i + (A_a - A_b),
and UV = 0 forces i = 0 or j = 0.
Setting V = 0 leaves the F[U]-complex whose homology is HFK^-.
"""
import json, sys
from fractions import Fraction

def arrows(h):
    gens = h['generators']; out = []
    for (a, b), c in h['differentials'].items():
        Ma, Aa = gens[a][1], gens[a][0]
        Mb, Ab = gens[b][1], gens[b][0]
        i2 = Mb - Ma + 1
        assert i2 % 2 == 0, (a, b, Ma, Mb)
        i = i2 // 2
        j = i + (Aa - Ab)
        assert i == 0 or j == 0, f'UV!=0 arrow {a}->{b}: U^{i}V^{j}'
        out.append((a, b, i, j))
    return out

def torsion_order(h):
    """All U-arrow exponents; SNF over F2[U] of a matrix whose nonzero entries
    are U^{i} has elementary divisors U^{i}, so the max exponent bounds Ord_U,
    and equals it when the U-part of the differential is nonzero."""
    ar = arrows(h)
    u = [x for x in ar if x[3] == 0 and x[2] > 0]
    v = [x for x in ar if x[2] == 0 and x[3] > 0]
    return {'n_gens': len(h['generators']), 'n_arrows': len(ar),
            'U_arrows': len(u), 'V_arrows': len(v),
            'U_exponents': sorted({x[2] for x in u}),
            'V_exponents': sorted({x[3] for x in v}),
            'max_U_exponent': max([x[2] for x in u], default=0)}

if __name__ == '__main__':
    import snappy
    for f in sys.argv[1:]:
        d = json.load(open(f))
        pd = d.get('pd_code_snappy_0indexed') or d['pd_code']
        K = snappy.Link([tuple(c) for c in pd])
        h = K.knot_floer_homology(complex=True)
        t = torsion_order(h)
        t['knot'] = d['name']; t['genus'] = h['seifert_genus']; t['fibered'] = h['fibered']
        t['thin_delta0'] = all(g[0] == g[1] for g in h['generators'].values())
        t['JMZ_fusion_lower_bound'] = t['max_U_exponent']
        print(json.dumps(t))
