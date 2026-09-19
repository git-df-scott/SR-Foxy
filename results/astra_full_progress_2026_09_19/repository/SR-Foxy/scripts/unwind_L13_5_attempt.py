#!/usr/bin/env python3
"""FAILED CONSTRUCTION, recorded with its exact failing gate.

Goal.  research/34 section 5 gives Sigma_2(K_1) as Dehn surgery on a 4-component
link in L(13,5).  The d-invariant formulas take surgery on a link in S^3, so the
plan was to "unwind" L(13,5) by drilling the core of its genus-1 Heegaard torus
and filling that core along the slope that restores S^3.  The cover already
carries the lifted branch knot K~_0 as its fifth cusp, so no new curve would
have been needed -- IF K~_0 were that core.

IT IS NOT, and the obstruction is homological and complete.  With the meridian
vector mu on the four lifted curves (so the ambient is L(13,5)), filling the
K~_0 cusp along (a,b) gives

    |H_1| = 13 * |a|,     independent of b.

That is exactly the signature of a NULL-HOMOLOGOUS knot in a rational homology
sphere: filling along a*meridian + b*longitude multiplies |H_1(Y)| by |a|.  So
[K~_0] = 0 in H_1(Sigma_2(K_0)) = Z/13, every filling has order divisible by 13,
and no filling is ever S^3.  The core of a Heegaard torus of L(13,5) generates
H_1, so K~_0 is not it.

WHAT THIS EXCLUDES, precisely: unwinding L(13,5) VIA THE LIFTED BRANCH KNOT.
WHAT IT DOES NOT EXCLUDE: unwinding via an actual Heegaard-torus core, which is
a different curve and is not present as a cusp of this cover; and it does not
touch the surgery description of research/34 section 5, which stands.

A first version of this search also reported zero, for a different and wrong
reason: it filtered on str(homology()) != '' when SnapPy prints trivial H_1 as
'0', so it discarded every candidate.  That zero was a bug.  This one is real,
and the H_1 grid below is the evidence rather than a failed search.

THE ROUTE THAT REPLACES IT, needing no unwinding: 13/5 = [3,3,2] as a continued
fraction, so -L(13,5) bounds the negative definite linear plumbing with weights
(-3,-3,-2).  Sigma_2(K_1) therefore bounds that plumbing with the four lifted
2-handles attached, b_2 = 3 + 4 = 7.  If that form is negative definite, then
D_{0,1} slice would make Sigma_2(D_{0,1}) = L(13,5) # -Sigma_2(K_1) bound a
rational homology ball, and Donaldson's theorem would force a lattice embedding
-- a finite exact integer test whose failure would kill the Abe-Tagami lane.
Computing that form needs the lifted curves' classes and pairwise linking in
L(13,5), which this script does not supply.

Usage: python3 scripts/unwind_L13_5_attempt.py <out.json>
"""
import json, math, os, sys, time
import snappy, regina

GRID = 4


def main(out_path):
    if os.path.exists(out_path):
        sys.exit('refusing to overwrite %s' % out_path)
    t0 = time.time()
    d = json.load(open('results/opus_2026_09_17/lifted_surgery_description.json'))
    C = snappy.Manifold(d['M_tilde_triangulation'])
    free, kl = d['free_cusps'], d['K_lift_cusp'][0]
    mu = [tuple(s) for s in d['fillings_giving_L13_5'][0]]

    def fill(slope):
        M = C.copy()
        M.dehn_fill(slope, kl)
        for c, s in zip(free, mu):
            M.dehn_fill(s, c)
        return M

    # control: the meridian filling must give L(13,5) by name
    M = fill((1, 0))
    T = regina.Triangulation3(M.filled_triangulation()._to_string())
    T.simplify()
    st = regina.StandardTriangulation.recognise(T)
    control = st.manifold().name() if (st and st.manifold()) else None

    grid, s3 = {}, []
    for a in range(-GRID, GRID + 1):
        for b in range(-GRID, GRID + 1):
            if math.gcd(abs(a), abs(b)) != 1:
                continue
            try:
                h = str(fill((a, b)).homology())
            except Exception as exc:
                h = 'error: %s' % exc
            grid['%d,%d' % (a, b)] = h
            if h == '0':
                s3.append([a, b])

    orders = {k: v for k, v in grid.items() if 'Z/' in v and '+' not in v}
    linear = all(v == 'Z/%d' % (13 * abs(int(k.split(',')[0])))
                 for k, v in orders.items() if int(k.split(',')[0]) != 0)
    out = {
        'snappy': snappy.version(), 'regina': regina.versionString(),
        'control_meridian_filling': control,
        'control_passes': control == 'L(13,5)',
        'meridian_vector_mu': [list(x) for x in mu],
        'H1_grid': grid, 'grid_box': GRID,
        'H1_order_is_13_times_a_independent_of_b': linear,
        'slopes_giving_S3': s3,
        'verdict': ('FAILED CONSTRUCTION. |H_1| = 13*|a| independent of b, the '
                    'signature of a null-homologous knot, so [K~_0] = 0 in '
                    'H_1(L(13,5)) = Z/13 and no filling of the lifted branch '
                    'knot is S^3. This excludes unwinding via K~_0 only; it '
                    'does not exclude unwinding via a Heegaard-torus core, and '
                    'it leaves the research/34 section 5 surgery description '
                    'untouched.'),
        'replacement_route': {
            'continued_fraction_13_over_5': [3, 3, 2],
            'check': '3 - 1/(3 - 1/2) = 3 - 2/5 = 13/5',
            'claim': ('-L(13,5) bounds the negative definite linear plumbing '
                      'with weights (-3,-3,-2); Sigma_2(K_1) then bounds that '
                      'plumbing plus the four lifted 2-handles, b_2 = 7'),
            'still_needed': ('the lifted curves classes and pairwise linking in '
                             'L(13,5); not supplied here'),
        },
        'seconds': round(time.time() - t0, 1),
    }
    with open(out_path, 'w') as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print('control:', control, '| S^3 slopes:', s3,
          '| |H1| = 13|a| independent of b:', linear)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1
         else 'results/opus_2026_09_17/unwind_L13_5_attempt.json')
