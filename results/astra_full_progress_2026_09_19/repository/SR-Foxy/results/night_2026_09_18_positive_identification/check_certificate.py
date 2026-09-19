"""Standard-library, integer-only verification of final gluing maps.

Does NOT validate the topology of upstream kernel transformations or rederive
peripheral curve transport. Those trust boundaries are explicit in the report.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def sign(p):
    inversions = sum(a > b for i,a in enumerate(p) for b in p[i+1:])
    return 1 if inversions % 2 == 0 else -1

def read_saved_gluings(path):
    """Parse the saved one-cusp SnapPea format without a geometry library."""
    lines = [s.strip() for s in path.read_text().splitlines() if s.strip()]
    assert lines[0] == '% Triangulation' and lines[3] == 'oriented_manifold'
    assert lines[5] == '1 0' and lines[6].split()[0] == 'torus'
    assert lines[6].split()[1:] == ['0.000000000000', '0.000000000000']
    n = int(lines[7])
    assert len(lines) == 8 + 8*n
    gluings, cusps = [], []
    for i in range(n):
        block = lines[8+8*i:16+8*i]
        adjacent = list(map(int, block[0].split()))
        permutations = [list(map(int, word)) for word in block[1].split()]
        assert len(adjacent) == len(permutations) == 4
        gluings.append([adjacent, permutations])
        cusps.append(list(map(int, block[2].split())))
        for curve_row in block[3:7]:
            assert len(list(map(int, curve_row.split()))) == 16
        # Shape coordinates in block[7] are deliberately unused.
    return gluings, cusps

def validate_triangulation(T):
    n = len(T)
    reached = {0}
    pending = [0]
    while pending:
        i = pending.pop()
        for f in range(4):
            j = T[i][0][f]
            p = T[i][1][f]
            assert 0 <= j < n and sorted(p) == [0,1,2,3]
            assert sign(p) == -1, 'oriented tetrahedron convention failed'
            g = p[f]
            assert T[j][0][g] == i
            q = T[j][1][g]
            assert all(q[p[v]] == v for v in range(4))
            if j not in reached:
                reached.add(j)
                pending.append(j)
    assert len(reached) == n

def check_case(c):
    A, B = c['source_gluings'], c['target_gluings']
    validate_triangulation(A)
    validate_triangulation(B)
    maps = c['orientation_preserving_simplex_map']
    n = len(A)
    assert len(B) == len(maps) == n
    assert sorted(m['target'] for m in maps) == list(range(n))
    count = 0
    for i, m in enumerate(maps):
        j, p = m['target'], m['vertices']
        assert sorted(p) == [0,1,2,3] and sign(p) == 1
        for v in range(4):
            assert c['source_cusps'][i][v] == c['target_cusps'][j][p[v]] == 0
        for f in range(4):
            ai, ag = A[i][0][f], A[i][1][f]
            bj, bg = B[j][0][p[f]], B[j][1][p[f]]
            assert maps[ai]['target'] == bj
            assert all(maps[ai]['vertices'][ag[v]] == bg[p[v]] for v in range(4))
            count += 1
    return count

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path, nargs='?', default=Path(__file__).with_name('saved'))
    args = parser.parse_args()
    d = json.loads((args.directory/'certificate.json').read_text())
    for item in d['inputs']:
        assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest() == item['sha256']
    counts = []
    for c in d['cases']:
        for stage in c['stages']:
            assert hashlib.sha256((args.directory/stage['file']).read_bytes()).hexdigest() == stage['sha256']
        for label, suffix in [('source', 'stored'), ('target', 'filled')]:
            gluings, cusps = read_saved_gluings(args.directory/f"n{c['n']}_{suffix}_retriangulated.tri")
            assert gluings == c[label+'_gluings'] and cusps == c[label+'_cusps']
        counts.append(check_case(c))
        bad = copy.deepcopy(c)
        p = bad['orientation_preserving_simplex_map'][0]['vertices']
        p[0],p[1],p[2] = p[1],p[2],p[0]  # even but incorrect permutation
        try:
            check_case(bad)
        except AssertionError:
            pass
        else:
            raise AssertionError('incorrect even simplex map was accepted')
        bad = copy.deepcopy(c)
        bad['orientation_preserving_simplex_map'][0]['vertices'][0:2] = list(reversed(
            bad['orientation_preserving_simplex_map'][0]['vertices'][0:2]))
        try:
            check_case(bad)
        except AssertionError:
            pass
        else:
            raise AssertionError('orientation mutation was accepted')
    print(json.dumps({'case_indices': [c['n'] for c in d['cases']],
                      'directed_face_checks': counts, 'simplex_maps': 'PASS',
                      'orientation_preserving': True, 'input_and_stage_hashes': 'PASS',
                      'mutations_rejected': 2*len(counts),
                      'scope': 'Final face-gluing isomorphisms only; preceding moves and cusp matrices remain kernel-trusted'}, indent=2))

if __name__ == '__main__':
    main()
