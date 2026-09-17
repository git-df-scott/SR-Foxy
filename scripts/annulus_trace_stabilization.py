#!/usr/bin/env python3
"""Verify the annulus-twist trace W for n = 1 on the Abe-Tagami family, and the
data needed for the statement

    K_0 = 6_3 and K_1 = A_1(6_3) cobound a smooth annulus in a 4-manifold W
    with boundary (-S^3) u S^3, simply connected, intersection form the even
    hyperbolic form H.

W = (S^3 x I) with two 2-handles attached along c'_1, c'_2 in S^3 x {1} with
integral framings 2 and 0.  The annulus is C = K_0 x I, which is disjoint from
the attaching circles because lk(K_0, c'_i) = 0.

Everything checked here is input verification for that statement; the handle
calculus step (H is realised by a Hopf link with framings 2 and 0, whose
closed-up 4-manifold is the S^2-bundle over S^2 of even Euler number) is
recorded but NOT machine-checked.

Usage: python3 scripts/annulus_trace_stabilization.py <out.json>
Refuses to overwrite an existing output file.
"""
import json, os, sys, time
import snappy
import regina

DATA = 'data/knots'
N = 1
SLOPES = {1: ((N + 1, N), (N - 1, N))}


def linking_matrix(pd):
    L = snappy.Link([tuple(c) for c in pd])
    return [[int(x) for x in row] for row in L.linking_matrix()]


def sublink(pd, keep):
    """PD code of the sublink on the given component indices."""
    L = snappy.Link([tuple(c) for c in pd])
    drop = [i for i in range(len(L.link_components)) if i not in keep]
    L2 = L.sublink(keep) if hasattr(L, 'sublink') else None
    if L2 is None:
        raise RuntimeError('spherogram build without Link.sublink')
    return L2


def regina_isosig(manifold, exhaustive=0):
    T = regina.Triangulation3(manifold.filled_triangulation()._to_string())
    T.simplify()
    if exhaustive:
        T.simplifyExhaustive(exhaustive)
    return T.isoSig(), T.size()


def main(out_path):
    if os.path.exists(out_path):
        sys.exit('refusing to overwrite %s' % out_path)
    t0 = time.time()
    card = json.load(open(os.path.join(DATA, 'AbeTagami_L_63_c1_c2.json')))
    pd = card['pd_code_snappy_0indexed']
    L = snappy.Link([tuple(c) for c in pd])
    out = {
        'input': 'data/knots/AbeTagami_L_63_c1_c2.json',
        'component_order': card['component_order'],
        'crossings': len(pd),
        'snappy': snappy.version(),
        'regina': regina.versionString(),
    }

    # (a) linking matrix
    lm = linking_matrix(pd)
    out['linking_matrix'] = lm
    out['lk_K_c1'] = lm[0][1]
    out['lk_K_c2'] = lm[0][2]
    out['lk_c1_c2'] = lm[1][2]
    out['annulus_disjoint_from_K'] = (lm[0][1] == 0 and lm[0][2] == 0)

    # (b) the surgery sublink c'_1 u c'_2 is the Hopf link
    H = L.sublink([1, 2])
    H.simplify('global')
    hopf_sig, hopf_tets = regina_isosig(H.exterior(), exhaustive=1)
    ref_sig, ref_tets = regina_isosig(snappy.Manifold('L2a1'), exhaustive=1)
    hpd = H.PD_code()
    out['surgery_sublink'] = {
        'crossings_after_simplify': len(hpd),
        'components': len(H.link_components),
        'isoSig': hopf_sig,
        'isoSig_tets': hopf_tets,
        'L2a1_isoSig': ref_sig,
        'L2a1_tets': ref_tets,
        'exterior_isosig_match': hopf_sig == ref_sig,
        'note': 'the Hopf link exterior is T^2 x I, not hyperbolic, so no '
                'isometry test is used or available',
        'diagram_argument': (
            'the sublink simplifies to a 2-crossing 2-component diagram with '
            'lk = +1; the only such link is the Hopf link'),
        'is_hopf_link': (len(hpd) == 2 and len(H.link_components) == 2
                         and abs(lm[1][2]) == 1),
    }

    # (c) the knot component is 6_3
    K = L.sublink([0])
    K.simplify('global')
    out['knot_component'] = {
        'crossings_after_simplify': len(K.PD_code()),
        'isometric_to_6_3': bool(K.exterior().is_isometric_to(snappy.Manifold('6_3'))),
    }

    # (d) the n = 1 trace: framings, S^3 boundary, and the outgoing knot
    s1, s2 = SLOPES[1]
    out['n'] = 1
    out['slopes'] = {"c'_1": list(s1), "c'_2": list(s2)}
    out['framings_are_integral'] = (s1[1] == 1 and s2[1] == 1)
    f1, f2 = s1[0] // s1[1], s2[0] // s2[1]
    out['framings'] = [f1, f2]
    Q = [[f1, lm[1][2]], [lm[1][2], f2]]
    det = Q[0][0] * Q[1][1] - Q[0][1] * Q[1][0]
    out['handle_intersection_form'] = {
        'matrix': Q,
        'determinant': det,
        'unimodular': abs(det) == 1,
        'even': (Q[0][0] % 2 == 0 and Q[1][1] % 2 == 0),
        'signature': 0 if det < 0 else None,
        'isomorphic_over_Z_to_hyperbolic_H': (abs(det) == 1
                                              and Q[0][0] % 2 == 0
                                              and Q[1][1] % 2 == 0
                                              and det < 0),
    }

    E = L.exterior()
    E.dehn_fill(s1, 1)
    E.dehn_fill(s2, 2)
    # boundary of the trace: fill the knot cusp along its meridian
    F = E.copy()
    F.dehn_fill((1, 0), 0)
    T = regina.Triangulation3(F.filled_triangulation()._to_string())
    T.simplify()
    out['outgoing_boundary_is_S3'] = bool(T.isSphere())

    K1 = json.load(open(os.path.join(DATA, 'AbeTagami_K_1.json')))
    stored = snappy.Link([tuple(c) for c in K1['pd_code_snappy_0indexed']]).exterior()
    out['outgoing_knot_is_stored_K_1'] = bool(E.is_isometric_to(stored))
    out['outgoing_knot_volume'] = float(E.volume())
    out['stored_K_1_volume'] = float(stored.volume())
    out['K_0_is_not_K_1'] = not bool(E.is_isometric_to(snappy.Manifold('6_3')))

    out['conclusion'] = {
        'annulus': 'C = K_0 x I in W, chi(C) = 0, connected, two boundary '
                   'components K_0 in -S^3 and K_1 in S^3',
        'W': '(S^3 x I) with 2-handles on the Hopf link c1 u c2, framings 2 and 0',
        'W_intersection_form': 'even, unimodular, indefinite, rank 2 = H',
        'handle_calculus_step_NOT_machine_checked':
            'H realised by a Hopf link with one 0-framed component and one '
            'even framing is the S^2-bundle over S^2 with even Euler number, '
            'i.e. S^2 x S^2; hence W is diffeomorphic to (S^3 x I) # (S^2 x S^2). '
            'Cited to standard Kirby calculus (Gompf-Stipsicz, GSM 20, ch. 4); '
            'NOT verified from the original in this container. The weaker '
            'statement (W simply connected with form H, hence homeomorphic to '
            '(S^3 x I) # (S^2 x S^2) by Freedman) needs no such citation.',
        'this_is_not_a_concordance':
            'W is not S^3 x I. research/14 section 3 proves pi_1(W - C) = Z, '
            'which with Delta_{K_0} != 1 forbids replacing W by a standard '
            'S^3 x I keeping this annulus.',
    }
    out['seconds'] = round(time.time() - t0, 1)
    all_checks = [out['annulus_disjoint_from_K'],
                  out['surgery_sublink']['is_hopf_link'],
                  out['knot_component']['isometric_to_6_3'],
                  out['framings_are_integral'],
                  out['handle_intersection_form']['isomorphic_over_Z_to_hyperbolic_H'],
                  out['outgoing_boundary_is_S3'],
                  out['outgoing_knot_is_stored_K_1'],
                  out['K_0_is_not_K_1']]
    out['ALL_CHECKS_PASS'] = all(all_checks)
    with open(out_path, 'w') as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in out.items() if k != 'conclusion'}, indent=1))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1
         else 'results/opus_2026_09_17/annulus_trace_stabilization.json')
