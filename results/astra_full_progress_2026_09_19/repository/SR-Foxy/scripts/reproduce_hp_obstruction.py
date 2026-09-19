#!/usr/bin/env python3
"""Rebuild the explicit Hom--Park member and retain exact norm-test inputs.

Run inside Sage/passagemath with SnapPy 3.3.2. Uses no legacy cable builder.
The four braids are 2-parallels of sigma_1^n with longitude correction q-2n.
Output is computational evidence using SnapPy's published HKL implementation.
"""
import argparse
import json
from pathlib import Path
import time
from sage.all import PolynomialRing, QQ
import snappy
from snappy.snap.slice_obs_HKL import rep_theory


def normalized(f):
    return f / f.parent().gen()**f.valuation() / f.leading_coefficient()


def run(output):
    out = Path(output)
    if out.exists():
        raise FileExistsError(out)
    R = PolynomialRing(QQ, 't'); t = R.gen()
    pieces, knots = [], []
    for n, q, expected_tau in [(3,1,2), (3,3,3), (5,3,5), (5,1,4)]:
        word = [2,1,3,2]*n + [-1]*(2*n-q)
        K = snappy.Link(braid_closure=word)
        actual = R(K.alexander_polynomial())
        expected = R((t**(2*n)+1)/(t**2+1) * (t**q+1)/(t+1))
        assert normalized(actual) == normalized(expected)
        tau = K.knot_floer_homology()['tau']
        assert tau == expected_tau
        pieces.append({'n':n, 'q':q, 'word':word, 'pd':K.PD_code(),
                       'alexander':str(actual), 'Alexander_identity_passed':True,
                       'tau':tau, 'expected_tau':expected_tau})
        knots.append(K)
    P = knots[0].connected_sum(knots[1].mirror()).connected_sum(knots[2]).connected_sum(knots[3].mirror())
    M = P.exterior()
    norm_tests = []
    original = rep_theory.poly_is_a_norm
    def recording_norm(poly):
        result = original(poly)
        norm_tests.append({'polynomial': str(poly), 'coefficient_field':str(poly.base_ring()),
                           'coefficients_low_to_high': list(map(str, poly.list())),
                           'factorization':str(poly.factor()), 'is_norm':bool(result)})
        return result
    rep_theory.poly_is_a_norm = recording_norm
    t0 = time.monotonic()
    try:
        advanced = M.slice_obstruction_HKL((2,3), method='advanced', ribbon_mode=False, verbose=2)
    finally:
        rep_theory.poly_is_a_norm = original
    direct = M.slice_obstruction_HKL((2,3), method='direct', ribbon_mode=False, verbose=2)
    control = snappy.Manifold('K12n813').slice_obstruction_HKL((2,3), method='advanced')
    assert advanced == direct == control == (2,3)
    assert len(norm_tests) == 4 and not any(r['is_norm'] for r in norm_tests)
    result = {'construction':'T23_21 # -T23_23 # T25_23 # -T25_21',
              'pieces':pieces, 'pd_code_snappy_0indexed':P.PD_code(),
              'advanced':advanced, 'direct':direct, 'control_K12n813':control,
              'p':2, 'q':3, 'ribbon_mode':False, 'norm_tests':norm_tests,
              'seconds':round(time.monotonic()-t0,3), 'snappy':snappy.__version__,
              'conclusion':'This explicit member is obstructed from topological sliceness. No conclusion about the whole Hom-Park family; no claim of literature priority.'}
    out.write_text(json.dumps(result, indent=2, default=int)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['pieces','pd_code_snappy_0indexed','norm_tests']}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('output'); a = p.parse_args(); run(a.output)
