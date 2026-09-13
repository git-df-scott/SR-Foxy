#!/usr/bin/env python3
"""Preserve the five-component diagram for a future mixed-circle construction.

This is a marked input scaffold, not a new candidate or a slice certificate.
"""
import hashlib
import json
from pathlib import Path
import snappy
from spherogram import Link

ROOT = Path(__file__).resolve().parents[1]


def main():
    path = ROOT/'data/knots/AbeTagami_L_63_c1_c2.json'
    source = json.loads(path.read_text())
    original = Link(source['pd_code'])
    original_lengths = [len(c) for c in original.link_components]
    assert len(set(original_lengths)) == 3
    # Cut at corresponding points of the marked arc. The generic connected_sum
    # helper cuts index 0 on both copies, which need not correspond under mirror.
    upper, lower = original.copy(), original.mirror()
    f1, i1 = upper.crossings[0], 0
    f2, i2 = f1.adjacent[i1]
    g1, j1 = lower.crossings[0], original.crossings[0].sign % 4
    g2, j2 = g1.adjacent[j1]
    source_cut = {'upper_endpoints': [[f1.label, i1], [f2.label, i2]],
                  'lower_endpoints': [[g1.label, j1], [g2.label, j2]],
                  'pairing': 'corresponding endpoints, not crossed endpoints'}
    starts = [upper.link_components[0][0], upper.link_components[1][0],
              upper.link_components[2][0], lower.link_components[1][0],
              lower.link_components[2][0]]
    f1[i1] = g1[j1]
    f2[i2] = g2[j2]
    for side, link in ((1, upper), (2, lower)):
        for c in link.crossings:
            c.label = (c.label, side)
            c._clear()
    doubled = Link(upper.crossings+lower.crossings, build=False)
    doubled._build(start_orientations=starts, component_starts=starts)
    assert len(doubled.link_components) == 5 and doubled.is_planar()
    markings = {}
    for i, component in enumerate(doubled.link_components):
        sides = {cs.crossing.label[1] for cs in component}
        if sides == {1, 2}:
            name = 'R'
            assert len(component) == 2*original_lengths[0]
        else:
            source_component = original_lengths.index(len(component))
            assert source_component in (1, 2)
            name = f'c{source_component}_' + ('upper' if sides == {1} else 'lower')
        markings[name] = i
    pd = doubled.PD_code()
    reconstructed = Link(pd)
    assert [len(c) for c in reconstructed.link_components] == [len(c) for c in doubled.link_components]
    assert reconstructed.linking_matrix() == doubled.linking_matrix()
    for side, sign in [('upper', 1), ('lower', -1)]:
        a, b = markings['c1_'+side], markings['c2_'+side]
        assert doubled.linking_matrix()[a][b] == sign
    assert all(x == 0 for x in doubled.linking_matrix()[markings['R']])
    result = {
        'name': 'Marked double of the Abe–Tagami surgery-link input',
        'status': 'INPUT_SCAFFOLD_NOT_A_NEW_CANDIDATE',
        'source_path': str(path.relative_to(ROOT)),
        'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'snappy_version': snappy.__version__,
        'construction': 'Double the punctured marked link: glue each cut endpoint to its corresponding mirrored endpoint; retain all four surgery circles.',
        'source_cut': source_cut,
        'pd_code': pd, 'component_markings': markings,
        'component_lengths': [len(c) for c in doubled.link_components],
        'linking_matrix': doubled.linking_matrix(),
        'crossings': len(pd), 'planarity_and_pd_roundtrip': True,
        'orientation_limit': 'Underlying marked diagram only. Explicit product boundary orientations and band whiskers must be tracked before any surgery/concordance certificate.',
        'proposed_mixed_pairs': [['c1_upper', 'c2_lower'], ['c2_upper', 'c1_lower']],
        'proposal': 'Band-sum each listed pair into a new circle; these are new circles, not annuli joining the listed pair. Seek based words uv and vu, with explicit band paths.',
        'unproved_gates': ['actual words after choosing bands', 'standard two-component annulus boundary link',
                          'asymmetric boundary surgery giving a certified nonribbon target',
                          'embedded standard modifying annulus disjoint from the disk'],
    }
    output = ROOT/'data/knots/AbeTagami_marked_product_scaffold.json'
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('status', 'crossings', 'component_markings', 'linking_matrix')}))


if __name__ == '__main__':
    main()
