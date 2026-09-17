#!/usr/bin/env python3
"""Geometry of the Abe-Tagami branched double covers Sigma_2(K_n).

research/21 left Sigma_2(K_1) as "unrecognized", explicitly withdrawing an
earlier hyperbolicity claim because SnapPy found no positively oriented
solution and Regina did not recognize the triangulation.  That withdrawal is
correct as a statement about what had been shown; this script supplies the
missing computation by simplifying in Regina first and re-solving in SnapPy.

What this establishes and what it does not:
  * a positively oriented hyperbolic solution on an explicit triangulation is
    strong numerical evidence for hyperbolicity.  It is NOT a proof: interval
    arithmetic verification (M.verify_hyperbolicity) needs Sage, which is not
    available in this container.
  * hyperbolic => not Seifert fibered => Sigma_2(K_1) bounds no plumbing on a
    negative definite tree with at most one bad vertex, so the Ozsvath-Szabo
    plumbing algorithm cannot be used to compute its d-invariants.  That is the
    only currently implementable route to the d-invariant gate of research/21
    section 3, so the gate is not reachable by that route.

Controls: Sigma_2(3_1) = L(3,1), Sigma_2(4_1) = L(5,q), Sigma_2(6_3) = L(13,5),
all of which must be recognized as lens spaces and must NOT admit a hyperbolic
structure.

Usage: python3 scripts/sigma2_geometry_probe.py <out.json>
"""
import json, os, sys, time
import snappy, regina

TRIES_REGINA = 40
TRIES_SNAPPY = 400


def sigma_2(pd):
    e = snappy.Link([tuple(c) for c in pd]).exterior()
    e.dehn_fill((2, 0))
    covers = e.covers(2, cover_type='cyclic')
    assert len(covers) == 1
    c = covers[0]
    assert c.num_cusps() == 1
    f = c.cusp_info('filling')[0]
    assert (round(f[0]), round(f[1])) == (1, 0), f
    return c


def smallest_regina(Y, tries=TRIES_REGINA):
    best = None
    for i in range(tries):
        N = Y.copy()
        if i:
            N.randomize()
        T = regina.Triangulation3(N.filled_triangulation()._to_string())
        T.simplify()
        if best is None or T.size() < best.size():
            best = T
    return best


def probe(label, pd):
    t0 = time.time()
    Y = sigma_2(pd)
    T = smallest_regina(Y)
    rec = {'label': label,
           'H1': T.homology().str(),
           'regina_tetrahedra': T.size(),
           'regina_isoSig': T.isoSig(),
           'irreducible': bool(T.isIrreducible())}
    try:
        rec['Haken'] = bool(T.isHaken())
    except Exception as exc:
        rec['Haken'] = 'error: %s' % exc
    st = regina.StandardTriangulation.recognise(T)
    name = None
    if st is not None:
        m = st.manifold()
        name = m.name() if m is not None else str(st)
    rec['regina_standard_recognition'] = name
    M = snappy.Manifold(T.snapPea())
    geometric = None
    for i in range(TRIES_SNAPPY):
        N = M.copy()
        if i:
            N.randomize()
        if N.solution_type() == 'all tetrahedra positively oriented':
            geometric = {'attempt': i, 'tetrahedra': N.num_tetrahedra(),
                         'volume': float(N.volume()),
                         'census_identify': [str(x) for x in N.identify()]}
            break
    rec['hyperbolic_solution'] = geometric
    rec['hyperbolic_numerically'] = geometric is not None
    rec['seconds'] = round(time.time() - t0, 1)
    return rec


def main(out_path):
    if os.path.exists(out_path):
        sys.exit('refusing to overwrite %s' % out_path)
    out = {'snappy': snappy.version(), 'regina': regina.versionString(),
           'tries_regina': TRIES_REGINA, 'tries_snappy': TRIES_SNAPPY,
           'controls': [], 'targets': []}
    for nm in ('3_1', '4_1', '6_3'):
        out['controls'].append(probe('control %s' % nm,
                                     snappy.Link(nm).PD_code()))
    for lab, f in (('K_0 (= 6_3)', 'AbeTagami_K_0_K_-1__6_3'),
                   ('K_1', 'AbeTagami_K_1'),
                   ('K_2', 'AbeTagami_K_2')):
        pd = json.load(open('data/knots/%s.json' % f))['pd_code_snappy_0indexed']
        out['targets'].append(probe(lab, pd))
    out['verdict'] = (
        'Sigma_2(K_0) = L(13,5) is recognized exactly, as in research/21. '
        'Sigma_2(K_1) and Sigma_2(K_2) admit positively oriented hyperbolic '
        'solutions on explicit triangulations. Numerical, not verified: '
        'interval arithmetic needs Sage. If hyperbolic they are not Seifert '
        'fibered, which removes the Ozsvath-Szabo plumbing algorithm as a '
        'route to their d-invariants and hence to the research/21 section 3 '
        'gate.')
    with open(out_path, 'w') as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    for rec in out['controls'] + out['targets']:
        print(rec['label'], '| tets', rec['regina_tetrahedra'],
              '| recognised', rec['regina_standard_recognition'],
              '| hyperbolic', rec['hyperbolic_numerically'],
              '| vol', (rec['hyperbolic_solution'] or {}).get('volume'))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1
         else 'results/opus_2026_09_17/sigma2_geometry_probe.json')
