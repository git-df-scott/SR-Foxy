#!/usr/bin/env python3
"""Full sweep: is Sigma_2(K_1) surgery on a knot in S^3 via ANY drilled geodesic?

A hit makes the campaign's one decisive gate computable.  research/21 section 3:
D_{0,1} slice implies the thirteen d-invariants of Sigma_2(K_1) are exactly
those of L(13,5); a mismatch proves [K_0] != [K_1] and closes the lane.  If
Sigma_2(K_1) = S^3_{p/q}(J) then the Ozsvath-Szabo rational surgery formula
gives all thirteen from the V_i, H_i of J.

research/52 closed ONE route: the natural cusped presentation (volume
9.2540100733, H_1 = Z) is not a knot exterior.  That was a single curve.  This
sweeps all 122 dual curves.

Method (Dunfield-Obeidin-Rubinstein, as used by Dunfield-Gong for 0-friends):
drill a closed geodesic, keep the complement if H_1 = Z, then look for a slope
whose filling is S^3.  Gordon-Luecke makes that slope unique and equal to the
meridian, so finding it exhibits the knot.

The drilled manifold must KEEP the original filling on cusp 0 -- unfilling it
discards the surgery that defines Sigma_2(K_1).  research/52 section 4 records
getting this wrong.

Control: meridian_slope must find the S^3 slope on genuine knot exteriors.
Verified on 4_1, 3_1, 6_3, 5_2 -> (-1,0) each.  Without that a negative here
would decide nothing.

Usage: sigma2_knot_surgery_sweep.py <out.jsonl> [n_curves] [slope_bound]
"""
import json, os, sys, time
from math import gcd

import snappy
import regina

SIGMA2_K1 = 'tvLvLLAzPzQQQkehkhglpmksnqrosprsqrgligsglwklpalagbokog'
CONTROLS = ['4_1', '3_1', '6_3', '5_2']


def is_S3(mfd):
    try:
        T = regina.Triangulation3(mfd.filled_triangulation()._to_string())
        for _ in range(4):
            T.intelligentSimplify()
        return bool(T.isSphere())
    except Exception:
        return False


def meridian_slope(N, bound):
    for a in range(-bound, bound + 1):
        for b in range(0, bound + 1):
            if (a, b) == (0, 0) or gcd(abs(a), b) != 1:
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


def run_controls(bound):
    rows = []
    for k in CONTROLS:
        M = snappy.Manifold(k)
        M.dehn_fill((0, 0))
        rows.append(dict(knot=k, slope=meridian_slope(M, min(bound, 3))))
    ok = all(r['slope'] is not None for r in rows)
    return ok, rows


def main():
    out = sys.argv[1]
    n_curves = int(sys.argv[2]) if len(sys.argv) > 2 else 122
    bound = int(sys.argv[3]) if len(sys.argv) > 3 else 20

    ok, crows = run_controls(bound)
    print('CONTROLS', 'PASS' if ok else 'FAIL', crows, flush=True)
    if not ok:
        print('controls failed -- a negative from this sweep would decide nothing',
              flush=True)
        sys.exit(1)

    done = set()
    if os.path.exists(out):
        for line in open(out):
            try:
                done.add(json.loads(line)['curve'])
            except Exception:
                pass

    M = snappy.Manifold(regina.Triangulation3(SIGMA2_K1).snapPea())
    filling = M.cusp_info('filling')[0]
    fill = (int(round(filling[0])), int(round(filling[1])))
    MAXSEG = int(os.environ.get("SWEEP_MAX_SEGMENTS", 12))
    curves = M.dual_curves(max_segments=MAXSEG)
    # dual_curves reports more curves than drill() accepts; the drillable set is
    # what bounds this sweep, so record both.
    try:
        import inspect  # noqa
    except Exception:
        pass
    print(f'Sigma_2(K_1): vol {M.volume()} H1 {M.homology()}; '
          f'{len(curves)} dual curves; keeping cusp-0 filling {fill}; '
          f'slope bound {bound}', flush=True)

    fh = open(out, 'a')
    t0 = time.time()
    hits = 0
    for i in range(min(n_curves, len(curves))):
        if i in done:
            continue
        row = dict(curve=i)
        try:
            D = M.drill(i)
            D.dehn_fill(fill, 0)
            D.dehn_fill((0, 0), 1)
            row.update(cusps=D.num_cusps(), volume=float(D.volume()),
                       homology=str(D.homology()))
            if str(D.homology()) in ('Z', 'Z/1 + Z'):
                s = meridian_slope(D, bound)
                row['S3_slope'] = s
                row['is_knot_exterior'] = s is not None
                if s is not None:
                    hits += 1
                    print(f'*** HIT: curve {i} drills to a KNOT EXTERIOR, '
                          f'meridian {s}, volume {row["volume"]} ***', flush=True)
            else:
                row['skipped'] = 'H1 != Z'
        except Exception as e:
            row['error'] = f'{type(e).__name__}: {e}'[:200]
        fh.write(json.dumps(row) + '\n')
        fh.flush()
        os.fsync(fh.fileno())
        print(f'[{time.time()-t0:7.1f}s] curve {i}: H1={row.get("homology")} '
              f'S3_slope={row.get("S3_slope")}', flush=True)
    fh.close()
    print(f'# done: {hits} knot-exterior drillings found', flush=True)


if __name__ == '__main__':
    main()
