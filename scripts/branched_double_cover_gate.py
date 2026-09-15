#!/usr/bin/env python3
"""Branched double covers of the Abe-Tagami family K_n = A_n(6_3).

The repository's earlier audits recorded branched-cover data as NOT covered
(RESUMED_2026-09-12.md: "Branched-cover and satellite data are not covered").
This script supplies the missing data for K_0, K_1, K_2.

Construction (no filling-slope ambiguity).  Dehn fill the knot exterior along
(2,0), giving the orbifold S^3 with cone angle pi along K, then take its
2-fold cyclic cover.  SnapPy carries the induced filling along, and the
induced slope comes back as (1,0) on the single cusp of the cover.  Composing
the two steps is exactly Sigma_2(K).  Taking the cyclic cover FIRST and then
guessing a filling slope does not work: every slope mu~ + k*lambda~ kills the
free summand of H_1 of the cover and returns Z/13, so homology cannot pick out
the correct one.

Separating invariant.  Low-index subgroup enumeration in pi_1 is exact and
combinatorial -- no numerical hyperbolic geometry is used or needed.  A lens
space L(p,q) has cyclic pi_1, hence no subgroup of index d unless d | p.

Controls: Sigma_2(3_1)=L(3,1), Sigma_2(4_1)=L(5,q), Sigma_2(6_3)=L(13,q)
(6_3 is the 2-bridge knot S(13,5)), and Sigma_2(3_1 # 3_1)=L(3,1)#L(3,1),
whose group Z/3 * Z/3 does have low-index subgroups.
"""
import json, os, sys
import snappy

MAX_INDEX = 5


def sigma_2(pd):
    """Branched double cover of S^3 over the knot with this PD code."""
    exterior = snappy.Link(pd).exterior()
    exterior.dehn_fill((2, 0))
    covers = exterior.covers(2, cover_type='cyclic')
    assert len(covers) == 1, 'expected a unique cyclic double cover'
    cover = covers[0]
    assert cover.num_cusps() == 1
    filling = cover.cusp_info('filling')[0]
    assert (round(filling[0]), round(filling[1])) == (1, 0), filling
    return cover


def profile(pd):
    """Homeomorphism invariants of Sigma_2 that separate the K_n."""
    cover = sigma_2(pd)
    out = {
        'H1': str(cover.homology()),
        'tetrahedra': cover.num_tetrahedra(),
        'low_index_subgroup_homology': {},
    }
    for degree in range(2, MAX_INDEX + 1):
        out['low_index_subgroup_homology'][str(degree)] = sorted(
            str(c.homology()) for c in cover.covers(degree))
    return out


def knot_record(name, pd):
    link = snappy.Link(pd)
    rec = {
        'name': name,
        'crossings': len(pd),
        'determinant': int(link.determinant()),
        'alexander_polynomial': str(link.alexander_polynomial()),
        'sigma_2': profile(pd),
    }
    # The profile must not depend on the diagram used to present the knot.
    simplified = snappy.Link(pd)
    simplified.simplify('global')
    rec['sigma_2_from_simplified_diagram'] = profile(simplified.PD_code())
    rec['diagram_independent'] = (
        rec['sigma_2'] == rec['sigma_2_from_simplified_diagram'])
    return rec


def main(out_path):
    if os.path.exists(out_path):
        sys.exit('refusing to overwrite %s' % out_path)

    controls = []
    for name in ('3_1', '4_1', '6_3'):
        controls.append(knot_record('control %s' % name,
                                    snappy.Link(name).PD_code()))
    granny = snappy.Link('3_1').copy()
    granny = snappy.Link(snappy.Link('3_1').PD_code())
    controls.append(knot_record(
        'control 3_1 # 3_1 (non-cyclic pi_1 positive control)',
        (granny.connected_sum(snappy.Link('3_1'))).PD_code()))

    targets = []
    for fname, label in (('AbeTagami_K_0_K_-1__6_3', 'K_0'),
                         ('AbeTagami_K_1', 'K_1'),
                         ('AbeTagami_K_2', 'K_2')):
        data = json.load(open('data/knots/%s.json' % fname))
        targets.append(knot_record(label, data['pd_code_snappy_0indexed']))

    by_label = {t['name']: t['sigma_2'] for t in targets}
    result = {
        'construction': 'orbifold (2,0) filling, then 2-fold cyclic cover',
        'max_subgroup_index': MAX_INDEX,
        'snappy_version': snappy.version(),
        'controls': controls,
        'targets': targets,
        'separations': {
            'Sigma_2(K_0) != Sigma_2(K_1)': by_label['K_0'] != by_label['K_1'],
            'Sigma_2(K_0) != Sigma_2(K_2)': by_label['K_0'] != by_label['K_2'],
            'Sigma_2(K_1) != Sigma_2(K_2)': by_label['K_1'] != by_label['K_2'],
        },
        'scope': (
            'Distinct branched double covers. This is NOT a concordance '
            'obstruction: nothing here bears on whether [K_0] = [K_1].'),
    }
    with open(out_path, 'w') as fh:
        json.dump(result, fh, indent=1, sort_keys=True)
    print(json.dumps(result['separations'], indent=1))
    for rec in controls + targets:
        print(rec['name'], rec['sigma_2']['H1'],
              rec['sigma_2']['low_index_subgroup_homology'],
              'diagram_independent=%s' % rec['diagram_independent'])


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1
         else 'results/branched_double_cover_gate.json')
