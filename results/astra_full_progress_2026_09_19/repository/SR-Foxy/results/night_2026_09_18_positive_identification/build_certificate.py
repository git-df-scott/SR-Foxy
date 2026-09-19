"""Positive combinatorial comparison, not a numerical non-isometry test.

Requires SnapPy 3.3.2. Saves all intermediate triangulations in a NEW directory.
Numerical choices guide canonize; the proof uses its topology-preserving moves
and a final exact face-gluing isomorphism. No hyperbolic canonicity is asserted.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import resource

import snappy
import spherogram

ROOT = Path(__file__).resolve().parents[2]

def compose(p, q):
    return [p[q[i]] for i in range(4)]

def inverse(p):
    return [p.index(i) for i in range(4)]

def parity(p):
    return (-1) ** sum(p[i] > p[j] for i in range(4) for j in range(i+1, 4))

def find_map(A, B):
    """At most 24*n seeds; propagation determines every other simplex map."""
    n = len(A)
    assert len(B) == n
    for target in range(n):
        for perm in itertools.permutations(range(4)):
            if parity(perm) != 1:
                continue
            mapping = {0: (target, list(perm))}
            pending = [0]
            valid = True
            while pending and valid:
                i = pending.pop()
                j, p = mapping[i]
                for f in range(4):
                    ai, ag = A[i][0][f], A[i][1][f]
                    bj, bg = B[j][0][p[f]], B[j][1][p[f]]
                    required = (bj, compose(compose(bg, p), inverse(ag)))
                    if ai in mapping:
                        if mapping[ai] != required:
                            valid = False
                            break
                    else:
                        mapping[ai] = required
                        pending.append(ai)
            if valid and len(mapping) == n and len({v[0] for v in mapping.values()}) == n:
                return [{'target': mapping[i][0], 'vertices': mapping[i][1]} for i in range(n)]
    raise ValueError('No positive combinatorial map found; this is not a non-homeomorphism certificate')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(exist_ok=False)
    resource.setrlimit(resource.RLIMIT_CPU, (45, 50))
    snappy.set_rand_seed(18092026)
    assert snappy.__version__ == '3.3.2'
    paths = {'L': ROOT/'data/knots/AbeTagami_L_63_c1_c2.json',
             'K0': ROOT/'data/knots/AbeTagami_K_0_K_-1__6_3.json',
             'K1': ROOT/'data/knots/AbeTagami_K_1.json'}
    cards = {k: json.loads(p.read_text()) for k,p in paths.items()}
    assert len(cards['L']['component_order']) == 3
    cases = []
    for n in (0, 1):
        stages = []
        def save(M, name):
            filename = f'n{n}_{name}.tri'
            M.save(str(args.output/filename))
            stages.append({'file': filename, 'tetrahedra': M.num_tetrahedra(),
                           'sha256': hashlib.sha256((args.output/filename).read_bytes()).hexdigest()})
        K = spherogram.Link(cards[f'K{n}']['pd_code']).exterior()
        L = spherogram.Link(cards['L']['pd_code']).exterior()
        assert L.num_cusps() == 3
        slopes = [[n+1, n], [n-1, n]]
        L.dehn_fill(slopes[0], 1)
        L.dehn_fill(slopes[1], 2)
        save(K, 'stored_pd_exterior')
        save(L, 'link_with_filling_instructions')
        F = L.filled_triangulation()
        save(F, 'filled_exterior')
        K.canonize()
        F.canonize()
        save(K, 'stored_retriangulated')
        save(F, 'filled_retriangulated')
        A, B = K._get_tetrahedra_gluing_data(), F._get_tetrahedra_gluing_data()
        assert not K.has_finite_vertices() and not F.has_finite_vertices()
        assert K.num_cusps() == F.num_cusps() == 1
        mapping = find_map(A, B)
        peripheral = []
        for iso in K.isomorphisms_to(F):
            m = iso.cusp_maps()[0]
            peripheral.append([[int(m[i,j]) for j in range(2)] for i in range(2)])
        assert [[1,0],[0,1]] in peripheral
        cases.append({'n': n, 'slopes': slopes, 'stages': stages,
                      'source_gluings': A, 'target_gluings': B,
                      'orientation_preserving_simplex_map': mapping,
                      'kernel_computed_peripheral_maps': peripheral,
                      'source_cusps': K._get_cusp_indices_and_peripheral_curve_data()[0],
                      'target_cusps': F._get_cusp_indices_and_peripheral_curve_data()[0]})
    out = {'scope': 'Positive combinatorial identification, trusting kernel filling/retriangulation; no move log',
           'snappy_version': snappy.__version__, 'seed': 18092026,
           'inputs': [{'path': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                      for p in paths.values()], 'cases': cases,
           'unverified': ['Paper figure to stored L PD', 'Standalone input-to-output move sequence',
                          'Independent peripheral homology transport', 'Sliceness or concordance']}
    (args.output/'certificate.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({'cases': len(cases), 'tetrahedra': [len(c['source_gluings']) for c in cases],
                      'positive_combinatorial_maps': True, 'scope': out['scope']}))

if __name__ == '__main__':
    main()
