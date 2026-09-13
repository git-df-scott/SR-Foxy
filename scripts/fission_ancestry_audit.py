#!/usr/bin/env python3
"""Necessary component tests for completing a pure-fission reverse ribbon movie.

After the first fission, one component must be ribbon-concordant above the
desired knot and the other must be ribbon. This follows by tracing descendants
in the fission tree and forgetting the other surface. These are necessary
conditions only, and do not apply to arbitrary movies with later fusion saddles.
"""
import argparse
from collections import Counter
import hashlib
import json
from math import isqrt
from pathlib import Path
import snappy
from component_guided_bands import parts, jones, encoded
from fusion_successors import diagram_signature
from nonfibered_reverse_audit import hfk


def determinant(p):
    assert all(i % 2 == 0 for i in p)
    return abs(sum(v * (-1 if (i//2) % 2 else 1) for i,v in p.items()))


def square(n): return n >= 0 and isqrt(n)**2 == n


def deficits(low, high):
    H = {(a,m):v for a,m,v in high}
    return [[a,m,v,H.get((a,m),0)] for a,m,v in low if v > H.get((a,m),0)]


def run(a):
    out = Path(a.output)
    if out.exists(): raise FileExistsError(out)
    raw = Path(a.input).read_bytes(); d = json.loads(raw)
    cache = {}; sources = {}
    for side,card in [('K0','AbeTagami_K_0_K_-1__6_3'), ('K1','AbeTagami_K_1')]:
        pd = json.loads(Path('data/knots/'+card+'.json').read_text())['pd_code_snappy_0indexed']
        P = jones(snappy.Link(pd)); sources[side] = {'Jones': encoded(P), 'det': determinant(P), 'HFK': hfk(pd)}
    def component(K):
        key = diagram_signature(K.PD_code())
        if key not in cache:
            P = jones(K); c = {'pd':K.PD_code(), 'Jones':encoded(P), 'det':determinant(P)}
            if not K.crossings:
                c['HFK'] = {'ranks':[[0,0,1]], 'tau':0, 'seifert_genus':0, 'fibered':True, 'total_rank':1}
            else:
                try: c['HFK'] = hfk(K.PD_code())
                except Exception as e: c['HFK_unknown'] = type(e).__name__ + ': ' + str(e)
            cache[key] = c
        return key
    rec = {'status':'NECESSARY_FISSION_ANCESTRY_AUDIT', 'parameters':vars(a),
           'input_sha256':hashlib.sha256(raw).hexdigest(), 'sources':sources,
           'components':cache, 'rows':[], 'summary':{}, 'complete':False,
           'scope':'No later fusion saddles or new births; only oriented fissions, isotopies, and split unknot deaths.'}
    def save(): out.write_text(json.dumps(rec,indent=2)+'\n')
    for r in d['intermediates']:
        L = snappy.Link(r['intermediate_pd']); P = parts(L); assert len(P)==2
        keys = [component(K) for K in P]; C = [cache[k] for k in keys]
        row = {'first_band':r['first_band'], 'component_keys':keys, 'sources':{}}
        for side,S in sources.items():
            assignments=[]
            for i in range(2):
                target, disk = C[i], C[1-i]; reasons=[]
                if not square(S['det'] * target['det']): reasons.append('target_determinant_product_not_square')
                if not square(disk['det']): reasons.append('disk_determinant_not_square')
                if 'HFK' in target:
                    if deficits(S['HFK']['ranks'],target['HFK']['ranks']): reasons.append('target_HFK_injection_fails')
                    if target['HFK']['tau'] != S['HFK']['tau']: reasons.append('target_tau_differs')
                if 'HFK' in disk:
                    if deficits([[0,0,1]],disk['HFK']['ranks']): reasons.append('unknot_HFK_injection_fails')
                    if disk['HFK']['tau'] != 0: reasons.append('disk_tau_nonzero')
                # With only one saddle remaining, one component is untouched:
                # either the target component already is K, or the disk component
                # already is an unknot. Jones matches here remain only necessary.
                two_possible = target['Jones']==S['Jones'] or disk['Jones']==[[0,1]]
                assignments.append({'target_component':i,'rejections':reasons,
                                    'passes_necessary_any_number_of_fissions':not reasons,
                                    'passes_necessary_one_remaining_fission':not reasons and two_possible,
                                    'HFK_unknown':any('HFK_unknown' in c for c in (target,disk))})
            row['sources'][side] = assignments
        rec['rows'].append(row); save()
    for side in sources:
        rec['summary'][side] = {'intermediates':len(rec['rows']),
            'retained_any_number_of_fissions':sum(any(a['passes_necessary_any_number_of_fissions'] for a in r['sources'][side]) for r in rec['rows']),
            'retained_one_remaining_fission':sum(any(a['passes_necessary_one_remaining_fission'] for a in r['sources'][side]) for r in rec['rows']),
            'assignment_rejection_counts':dict(Counter(e for r in rec['rows'] for a in r['sources'][side] for e in a['rejections']))}
    rec['complete']=True; save(); print(json.dumps(rec['summary']),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('output');run(p.parse_args())
