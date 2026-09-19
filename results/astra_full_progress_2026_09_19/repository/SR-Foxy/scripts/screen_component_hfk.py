#!/usr/bin/env python3
"""Bounded HFK/component obstructions; inconsistent calculations remain unknown."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import snappy
import sympy
from bounded_ribbon_search import save
from component_guided_bands import parts, jones
from fission_ancestry_audit import determinant
from fusion_successors import diagram_signature
from nonfibered_reverse_audit import hfk
from teichner_component_slice_gate import norm_test


def run(source, output):
    source, output = Path(source), Path(output)
    if output.exists():
        raise FileExistsError(output)
    gate = json.loads(source.read_text())
    assert gate['complete']
    rec = {'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
           'rows': [], 'components': {}, 'complete': False,
           'scope': 'Component obstructions to pure-fission ribbon completion. '
                    'HFK calculation timeout is 5 seconds each; determinant/Euler checks precede any exclusion.'}
    t = sympy.Symbol('t')
    def component(link):
        if not link.crossings:
            return 'U'
        key = diagram_signature(link.PD_code())
        if key not in rec['components']:
            data = {'pd': link.PD_code(), 'rejections': [], 'status': 'UNKNOWN'}
            try:
                H = hfk(link.PD_code())
                coeff = Counter()
                for a, m, n in H['ranks']:
                    coeff[a] += n * (-1 if m % 2 else 1)
                coeff = {a: n for a, n in coeff.items() if n}
                low = min(coeff)
                P = sympy.Poly(sum(n*t**(a-low) for a, n in coeff.items()), t)
                if P.eval(1) == -1:
                    P = -P
                det = determinant(jones(link))
                # Retain evidence even when a consistency check fails.
                data.update(HFK=H, determinant=det,
                            alexander=[int(P.nth(i)) for i in range(P.degree()+1)])
                assert P.eval(1) == 1, 'HFK Euler polynomial is not normalized at 1'
                assert abs(int(P.eval(-1))) == det, 'HFK and Jones determinants disagree'
                assert sorted(H['ranks']) == sorted([[-a, m-2*a, n] for a, m, n in H['ranks']]), 'HFK grading symmetry failed'
                reasons = []
                if H['tau'] != 0:
                    reasons.append('tau_nonzero')
                if not any(a == m == 0 and n for a, m, n in H['ranks']):
                    reasons.append('ribbon_unknot_HFK_injection_fails')
                witnesses = norm_test(P)
                if witnesses:
                    reasons.append('Fox_Milnor_norm_fails')
                data.update(status='CHECKED', HFK=H, determinant=det, rejections=reasons,
                            norm_witnesses=witnesses, alexander=[int(P.nth(i)) for i in range(P.degree()+1)])
            except Exception as e:
                data['error'] = repr(e)
            rec['components'][key] = data
        return key
    rec['components']['U'] = {'status': 'KNOWN_UNKNOT', 'rejections': [], 'pd': []}
    control_slice = component(snappy.Link('6_1'))
    control_nonslice = component(snappy.Link('3_1'))
    assert rec['components'][control_slice]['status'] == 'CHECKED'
    assert not rec['components'][control_slice]['rejections']
    assert 'tau_nonzero' in rec['components'][control_nonslice]['rejections']
    rec['controls'] = {'ribbon_6_1': control_slice, 'trefoil': control_nonslice}
    loaded = {}
    for row in gate['rows']:
        if row['ribbon_completion_obstructed']:
            continue
        origin = row['origin']
        path = Path(origin['source'])
        if str(path) not in loaded:
            assert hashlib.sha256(path.read_bytes()).hexdigest() == gate['input_hashes'][str(path)]
            loaded[str(path)] = json.loads(path.read_text())
        endpoint = loaded[str(path)]['frontier'][origin['index']]['endpoint_pd']
        keys = [component(link) for link in parts(snappy.Link(endpoint))]
        rejected = any(rec['components'][k]['rejections'] for k in keys)
        rec['rows'].append({'origin': origin, 'components': keys,
                            'ribbon_completion_obstructed': rejected})
        save(output, rec)
    rec.update(complete=True, additional_excluded=sum(r['ribbon_completion_obstructed'] for r in rec['rows']),
               retained_unknown=sum(not r['ribbon_completion_obstructed'] for r in rec['rows']),
               unknown_components=sum(c['status'] == 'UNKNOWN' for c in rec['components'].values()))
    save(output, rec)
    print(json.dumps({k: rec[k] for k in ['additional_excluded', 'retained_unknown', 'unknown_components']}), flush=True)


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2])
