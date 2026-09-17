#!/usr/bin/env python3
"""An explicit surgery description of Sigma_2(K_1) inside Sigma_2(K_0) = L(13,5).

research/33 section 3 left the d-invariant gate of research/21 section 3 out of
reach: Sigma_2(K_1) is hyperbolic, so it bounds no plumbing, and the only
remaining route named there was "a surgery description on which existing
formulas apply".  The annulus twist supplies one for free.

Because lk(K, c'_i) = 0, each surgery curve of the twist lifts to TWO curves in
the double branched cover.  So: fill the knot cusp of the exterior of
L = K u c'_1 u c'_2 along (2,0) -- the orbifold with cone angle pi along K --
and take the 2-fold cyclic cover.  Exactly one of the index-2 covers has five
cusps: the K-lift (carrying the induced filling (1,0)) plus two lifts each of
c'_1 and c'_2.  Discarding the filled K-cusp leaves a 4-cusped manifold M~,
the exterior in L(13,5) of the preimage of c'_1 u c'_2.

SnapPy chooses a cusp basis per cover, so the lifted slopes are NOT (1,0) and
(2,1)/(0,1) in that basis; they are found by a bounded search and then pinned by
saving the triangulation itself.  The saved triangulation string is what makes
this reproducible: rerunning covers() can return a different representative.

Controls, both required:
  * some filling of M~ must give Sigma_2(K_0), recognised by Regina as exactly
    L(13,5);
  * some filling must give a manifold with the same Regina isoSig as Sigma_2(K_1)
    built independently from the stored K_1 diagram.

Usage: python3 scripts/lifted_surgery_description.py <out.json>
"""
import itertools, json, math, os, sys, time
import snappy, regina

SLOPE_RANGE = 2


def closed(M, rounds=4):
    T = regina.Triangulation3(M.filled_triangulation()._to_string())
    T.simplify()
    for _ in range(rounds):
        T.simplify()
    return T


def recognise(T):
    st = regina.StandardTriangulation.recognise(T)
    if st is None:
        return None
    m = st.manifold()
    return m.name() if m is not None else str(st)


def main(out_path):
    if os.path.exists(out_path):
        sys.exit('refusing to overwrite %s' % out_path)
    t0 = time.time()
    pd = json.load(open('data/knots/AbeTagami_L_63_c1_c2.json'))['pd_code_snappy_0indexed']
    E = snappy.Link([tuple(c) for c in pd]).exterior()
    E.dehn_fill((2, 0), 0)
    covers = E.covers(2)
    five = [C for C in covers if C.num_cusps() == 5]
    assert len(five) == 1, [C.num_cusps() for C in covers]
    Mt = five[0]
    tri = Mt._to_string()
    info = Mt.cusp_info('filling')
    free = [i for i, f in enumerate(info) if (f[0], f[1]) == (0.0, 0.0)]
    klift = [i for i in range(5) if i not in free]
    assert len(free) == 4 and len(klift) == 1

    # independent target: Sigma_2(K_1) built from the stored K_1 diagram
    k1 = json.load(open('data/knots/AbeTagami_K_1.json'))['pd_code_snappy_0indexed']
    e = snappy.Link([tuple(c) for c in k1]).exterior()
    e.dehn_fill((2, 0))
    T_target = closed(e.covers(2, cover_type='cyclic')[0])
    target = T_target.isoSig()

    slopes = [(p, q) for p in range(-SLOPE_RANGE, SLOPE_RANGE + 1)
              for q in range(-SLOPE_RANGE, SLOPE_RANGE + 1)
              if math.gcd(abs(p), abs(q)) == 1]
    lens, hits, checked = [], [], 0
    for combo in itertools.product(slopes, repeat=4):
        checked += 1
        M = Mt.copy()
        for c, s in zip(free, combo):
            M.dehn_fill(s, c)
        try:
            if str(M.homology()) != 'Z/13':
                continue
        except Exception:
            continue
        T = closed(M)
        if recognise(T) == 'L(13,5)':
            lens.append([list(s) for s in combo])
        if T.isoSig() == target:
            hits.append([list(s) for s in combo])

    out = {
        'snappy': snappy.version(), 'regina': regina.versionString(),
        'construction': ('fill knot cusp of L with (2,0), take the unique '
                         '5-cusped index-2 cover; the K-lift carries the induced '
                         'filling and the other four cusps are the lifts of '
                         "c'_1, c'_2"),
        'M_tilde_tetrahedra': Mt.num_tetrahedra(),
        'M_tilde_H1': str(Mt.homology()),
        'M_tilde_triangulation': tri,
        'K_lift_cusp': klift, 'free_cusps': free,
        'K_lift_induced_filling': [list(map(float, info[klift[0]]))],
        'slope_box': SLOPE_RANGE, 'slopes_per_cusp': len(slopes),
        'fillings_checked': checked,
        'target_isoSig_Sigma2_K1': target,
        'target_tetrahedra': T_target.size(),
        'fillings_giving_L13_5': lens,
        'fillings_giving_Sigma2_K1': hits,
        'n_L13_5': len(lens), 'n_Sigma2_K1': len(hits),
        'controls_pass': bool(lens) and bool(hits),
        'seconds': round(time.time() - t0, 1),
        'limits': ('A bounded slope search, not a classification of fillings. '
                   'The triangulation string is saved because covers() need not '
                   'return the same representative on a rerun; the slopes are '
                   'meaningless without it. This is a surgery description, not a '
                   'd-invariant computation.'),
    }
    with open(out_path, 'w') as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print('M~ tets', Mt.num_tetrahedra(), '| checked', checked,
          '| L(13,5):', len(lens), '| Sigma_2(K_1):', len(hits),
          '| %.0fs' % (time.time() - t0))
    print('Sigma_2(K_1) fillings:', hits)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1
         else 'results/opus_2026_09_17/lifted_surgery_description.json')
