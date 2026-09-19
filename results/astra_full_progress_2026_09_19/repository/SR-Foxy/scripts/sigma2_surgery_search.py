#!/usr/bin/env python3
"""Is Sigma_2(K_1) Dehn surgery on a knot in S^3?

WHY.  research/21 section 3 states the campaign's one named DECISIVE gate:

    D_{0,1} smoothly slice  ==>  the thirteen d-invariants of Sigma_2(K_1)
    are, as a multiset, exactly those of L(13,5).

A mismatch proves [K_0] != [K_1] and closes the primary lane outright.  It has
never been evaluated because nothing here computes Heegaard Floer d-invariants
of a closed hyperbolic QHS^3, and results/opus_2026_09_17/sigma2_geometry_probe
confirms Sigma_2(K_1) IS hyperbolic -- so it is not Seifert fibered and the
Ozsvath-Szabo plumbing algorithm does not apply.

But if Sigma_2(K_1) = S^3_{p/q}(J) for a knot J, the Ozsvath-Szabo RATIONAL
SURGERY FORMULA gives all thirteen d-invariants from the V_i, H_i of J.  That
converts the blocked gate into a computation.  This script looks for such a
description by Dunfield-Obeidin-Rubinstein's method, the same one Dunfield-Gong
use to manufacture 0-friends: drill a closed geodesic and test whether the
result is a knot exterior in S^3.

METHOD.  For each drilled curve: keep it if H_1 = Z (necessary for a knot
exterior), then search short slopes for one whose filling is S^3.  By
Gordon-Luecke that slope is unique and is the meridian, so finding it exhibits
the knot; the original filling slope then gives the surgery coefficient.

CONTROL, and it is the point of the run: the identical procedure is applied to
Sigma_2(K_0) = L(13,5), which IS surgery on the unknot.  If the control does not
recover a knot-exterior drilling, a negative on K_1 means nothing -- exactly the
failure mode HANDOFF section 6 records ("always run a control that asks whether
the tool works at all before believing an all-negative sweep").

Already established before this script, by direct test: the cusped manifold that
Sigma_2(K_1) is presented as a (1,0) filling of (volume 9.2540100733, H_1 = Z)
is NOT a knot exterior in S^3 -- its only two trivial-homology fillings, at
slopes (-5,11) and (-1,2), are hyperbolic with volumes 9.0048 and 1.9122.

Usage: sigma2_surgery_search.py <out.json> [n_curves]
"""
import json, sys, time
from math import gcd

import snappy
import regina

SIG = {
    'Sigma_2(K_1)': 'tvLvLLAzPzQQQkehkhglpmksnqrosprsqrgligsglwklpalagbokog',
}

# CONTROL.  The first version of this script used Sigma_2(K_0) = L(13,5), which
# was a BAD control and failed: a lens space is not hyperbolic, SnapPy returned
# 0 dual curves, and the sweep therefore decided nothing.  A usable control must
# be (a) hyperbolic, so that geodesic drilling applies at all, and (b) known in
# advance to be surgery on a knot in S^3.  S^3_{13}(4_1) is both, and it has
# H_1 = Z/13 like the target.
CONTROL_SURGERY = ('4_1', (13, 1))


def is_S3(mfd):
    """Regina S^3 recognition on the filled triangulation."""
    try:
        T = regina.Triangulation3(mfd.filled_triangulation()._to_string())
        for _ in range(4):
            T.intelligentSimplify()
        return bool(T.isSphere())
    except Exception:
        return False


def meridian_slope(N, bound=14):
    """A slope whose filling is S^3, if one exists among short slopes."""
    for a in range(-bound, bound + 1):
        for b in range(0, bound + 1):
            if (a, b) == (0, 0):
                continue
            if gcd(abs(a), b) != 1:
                continue
            X = N.copy()
            try:
                X.dehn_fill((a, b))
                if X.homology().order() != 1:
                    continue
            except Exception:
                continue
            if is_S3(X):
                return (a, b)
    return None


def scan(label, sig, n_curves, t0):
    return scan_manifold(label, snappy.Manifold(regina.Triangulation3(sig).snapPea()),
                         n_curves, t0)


def scan_manifold(label, M, n_curves, t0):
    sig = label
    rec = dict(label=label, isosig=sig, volume=float(M.volume()),
               homology=str(M.homology()), drillings=[], knot_exterior_found=None)
    try:
        curves = M.dual_curves(max_segments=12)
    except Exception as e:
        rec['error'] = f'dual_curves: {type(e).__name__}'
        return rec
    rec['n_dual_curves'] = len(curves)
    for i in range(min(n_curves, len(curves))):
        try:
            D = M.drill(i)
            # drill() on a FILLED manifold returns 2 cusps: cusp 0 is the
            # original (carrying M's filling) and cusp 1 is the drilled
            # geodesic.  Unfilling both gives the wrong manifold entirely --
            # it drops the surgery that defines Sigma_2(K_n).  Keep cusp 0
            # filled and leave only the drilled cusp open, so D is
            # Sigma_2(K_n) minus that geodesic.
            filling = M.cusp_info('filling')[0]
            D.dehn_fill((int(round(filling[0])), int(round(filling[1]))), 0)
            D.dehn_fill((0, 0), 1)
        except Exception as e:
            rec['drillings'].append(dict(curve=i, error=type(e).__name__))
            continue
        row = dict(curve=i, cusps=D.num_cusps(), volume=float(D.volume()),
                   homology=str(D.homology()))
        if D.homology().order() == 0 and str(D.homology()) in ('Z', 'Z/1 + Z'):
            m = meridian_slope(D)
            row['S3_slope'] = m
            if m is not None:
                row['IS_KNOT_EXTERIOR'] = True
                rec['knot_exterior_found'] = dict(curve=i, meridian=m,
                                                  volume=float(D.volume()))
        rec['drillings'].append(row)
        print(f'  [{time.time()-t0:6.1f}s] {label} curve {i}: cusps={row["cusps"]} '
              f'H1={row["homology"]} S3_slope={row.get("S3_slope")}', flush=True)
        if rec['knot_exterior_found']:
            break
    return rec


def main():
    out = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    t0 = time.time()
    res = {}
    for label, sig in SIG.items():
        print(f'=== {label} ===', flush=True)
        res[label] = scan(label, sig, n, t0)

    kname, slope = CONTROL_SURGERY
    C = snappy.Manifold(kname); C.dehn_fill(slope)
    label = f'CONTROL S^3_{slope[0]}/{slope[1]}({kname})'
    print(f'=== {label} ===', flush=True)
    res[label] = scan_manifold(label, C, n, t0)
    res['control_found_knot_exterior'] = res[label]['knot_exterior_found'] is not None
    res['meaning'] = (
        'If control_found_knot_exterior is False the sweep has decided NOTHING: '
        'the method failed on a manifold that is known to be surgery on the '
        'unknot. Only with the control passing does a negative on Sigma_2(K_1) '
        'mean that no drilled curve among those tried exhibits it as surgery on '
        'a knot in S^3 -- and even then that is a bounded search, not a theorem.')
    res['counterexample'] = False
    json.dump(res, open(out, 'w'), indent=1)
    print(json.dumps({k: (v if not isinstance(v, dict) else
                          {kk: vv for kk, vv in v.items() if kk != 'drillings'})
                      for k, v in res.items()}, indent=1)[:1800])


if __name__ == '__main__':
    main()
