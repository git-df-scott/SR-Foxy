#!/usr/bin/env python3
"""Replay saved operations and check the new homology rejection ledger.

This checks computations and provenance, not a formalized topology proof.
It deliberately preserves incomplete searches and the failed pilot.
"""
import hashlib
import json
from pathlib import Path
import snappy
from spherogram.links.bands.core import add_one_band, normalize_crossing_labels
from fusion_successors import replay
from khovanov_upper_filter import parse_poincare, euler_check, deficits
from two_fission_target import alex_rank


def read(path): return json.loads(Path(path).read_text())
def ranks(row): return {(i, j): n for i, j, n in row['ranks']}


def run():
    result = {'status': 'COMPUTATIONAL_CHECKS_PASSED_NOT_A_COUNTEREXAMPLE',
              'kh_logs_checked': 0, 'reverse_band_replays': 0, 'forward_movie_replays': 0,
              'searches': [], 'limitations': 'Jones checks do not independently determine all Khovanov gradings. Raw band replay does not certify simplification movies.'}
    # A total-rank-only implementation would falsely pass this fixture.
    assert deficits({(0, 0): 1}, {(1, 0): 100}) == [[0, 0, 1, 0]]
    try:
        parse_poincare('calculation aborted')
    except ValueError:
        pass
    else:
        raise AssertionError('Missing output was accepted')
    for folder, field in [('nonfibered_khovanov_filter', 2), ('nonfibered_khovanov_Q', 1), ('nonfibered_khovanov_F3', 3)]:
        base = Path('results') / folder
        d = read(base / 'manifest.json'); assert d['complete']
        controls = {r['name']: ranks(r) for r in d['runs'] if r['source_index'] is None}
        for row in d['runs']:
            assert row['status'] == 'computed_and_euler_checked'
            assert parse_poincare((base / (row['name'] + '.log')).read_text(), field) == ranks(row)
            assert euler_check(row['pd'], ranks(row)) == row['euler_validation']
            assert row['euler_validation']['passed']
            if row['source_index'] is not None:
                assert deficits(controls['K0'], ranks(row)) == row['K0_deficits'] == []
                assert deficits(controls['K1'], ranks(row)) == row['K1_deficits']
                assert bool(row['K1_deficits']) == row['K1_ribbon_predecessor_obstructed']
            result['kh_logs_checked'] += 1
        if field == 2:
            candidates = [r for r in d['runs'] if r['source_index'] is not None]
            assert len(candidates) == 48
            assert sum(r['K1_ribbon_predecessor_obstructed'] for r in candidates) == 46
            assert [r['source_index'] for r in candidates if not r['K1_deficits']] == [25533, 25541]
            assert deficits(controls['K0'], controls['K1']) == []
    for name in ['fusion_AT0_wider_targets', 'K1_nonfibered_shortlist']:
        for r in read('results/' + name + '.json')['candidates']:
            assert replay(r)
            result['forward_movie_replays'] += 1
    for name in ['nonfibered_reverse_batch1', 'nonfibered_reverse_batch2', 'nonfibered_reverse_batch3',
                 'nonfibered_reverse_focused_v2', 'K1_nonfibered_reverse']:
        d = read('results/' + name + '.json')
        for row in d['runs']:
            J = snappy.Link(row['start_pd']); normalize_crossing_labels(J)
            for endpoint in row['endpoints']:
                assert add_one_band(J, endpoint['band']).PD_code() == [tuple(c) for c in endpoint['raw_split_pd']]
                assert endpoint['raw_replay'] and not endpoint['certified']
                result['reverse_band_replays'] += 1
        result['searches'].append({'name': name, 'complete': d['complete'], 'checkpointed_targets': len(d['runs']),
                                  'checkpointed_bands': sum(r['counts'].get('shortest_bands', 0) + r['counts'].get('edge_sample_bands', 0) for r in d['runs']),
                                  'nominations': sum(len(r.get('K0_nominations', r.get('K1_nominations', []))) for r in d['runs'])})
    reg = read('results/alexander_overpassing_control.json')
    for row in reg['controls'] + [reg['regression']]:
        L = snappy.Link(row['pd']); L.unlinked_unknot_components = row.get('unlinked_unknots', 0)
        assert alex_rank(L) == (row['rank'], row['columns'])
    L = snappy.Link(reg['regression']['pd'])
    old_arcs = {tuple(cs) for part in L._pieces() for cs in part}
    assert any((c, 1) not in old_arcs for c in L.crossings)
    result['missing_generator_regression_reproduced'] = True
    two = read('results/two_fission_nonfibered_25533.json')
    assert two['complete'] and not any('K1' in r.get('matching_source_HFK', []) for r in two['endpoint_checks'])
    intermediates = {r['first_band']: r for r in two['intermediates']}
    for endpoint in two['endpoint_checks']:
        I = snappy.Link(intermediates[endpoint['first_band']]['intermediate_pd'])
        normalize_crossing_labels(I)
        assert add_one_band(I, endpoint['second_band']).PD_code() == [tuple(c) for c in endpoint['raw_second_pd']]
    processed_second = sum(min(r['second_attempts'], two['second_limit_per_intermediate']) for r in two['intermediates'])
    result['two_fission'] = {'retained_intermediates': len(two['intermediates']),
                            'processed_second_bands': processed_second, 'K1_matches': 0}
    assert processed_second == 30173
    sl3 = read('results/nonfibered_sl3_pilot/checked.json')
    assert sl3['status'] == 'TARGET_SL3_CALCULATIONS_INCONCLUSIVE' and not sl3['obstructions']
    result['kh_rejections'] = 46; result['kh_survivors'] = [25533, 25541]
    result['sha256'] = {}
    for p in sorted(Path('results').glob('nonfibered*')):
        for f in sorted(p.rglob('*')) if p.is_dir() else [p]:
            if f.is_file() and f.name != 'nonfibered_session_validation.json':
                result['sha256'][str(f)] = hashlib.sha256(f.read_bytes()).hexdigest()
    for name in ['README.md', 'HANDOFF.md', 'research/16_nonfibered_khovanov_gate.md',
                 'scripts/nonfibered_reverse_audit.py', 'scripts/khovanov_upper_filter.py',
                 'scripts/check_nonfibered_session.py', 'scripts/check_sl3_pilot.py',
                 'scripts/two_fission_target.py', 'scripts/plot_khovanov_gate.py',
                 'results/K1_nonfibered_reverse.json', 'results/K1_nonfibered_shortlist.json',
                 'results/alexander_overpassing_control.json', 'results/two_fission_nonfibered_25533.json',
                 'results/fusion_AT0_wider_targets.json', 'results/fusion_HFK_filter_all.json',
                 'data/knots/AbeTagami_K_0_K_-1__6_3.json', 'data/knots/AbeTagami_K_1.json']:
        p = Path(name)
        if p.suffix == '.py': compile(p.read_text(), name, 'exec')
        result['sha256'][name] = hashlib.sha256(p.read_bytes()).hexdigest()
    Path('results/nonfibered_session_validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print({k: v for k, v in result.items() if k != 'sha256'})


if __name__ == '__main__': run()
