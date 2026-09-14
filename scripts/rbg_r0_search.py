#!/usr/bin/env python3
"""Ribbon (band) search on the never-searched r = 0 RBG pair.

CANDIDATE_LEDGER Tier-A generators records the pair
K_{B/G}(0,0,0,-1,2,1) as 24/27 crossings, outside the Dunfield-Gong
<= 19-crossing census, and never searched.  Both knots have Alexander
polynomial 1, genus 2 and vanishing tau/nu/epsilon.

Because r = 0 the two knots have diffeomorphic 0-traces, so a ribbon disk
for either one certifies its partner smoothly slice in standard B^4 with no
inherited ribbon disk: a fresh Tier-A candidate.

A positive result ('unknot' reached) is a certificate and is verified with
verify_ribbon_to_unknot.  A negative result is a coverage statement over the
stated parameter box only, never an obstruction.

Usage: rbg_r0_search.py <knot.json> <n_diagrams> <max_bands> <max_twists>
                        <max_band_len> <seconds_per_diagram> <out.json>
"""
import json, sys, time, datetime, hashlib, random
import snappy
from spherogram.links.bands.search import ribbon_concordant_links, verify_ribbon_to_unknot

knot_file, n_diagrams, max_bands, max_twists, max_band_len, budget, out = sys.argv[1:8]
n_diagrams, max_bands = int(n_diagrams), int(max_bands)
max_twists, max_band_len, budget = int(max_twists), int(max_band_len), float(budget)

d = json.load(open(knot_file))
pd = d.get('pd_code_snappy_0indexed') or d['pd_code']
pd_hash = hashlib.sha256(json.dumps(pd, sort_keys=True).encode()).hexdigest()[:16]

import snappy.sage_helper as sh
within_sage = bool(sh._within_sage)

def fresh(seed):
    K = snappy.Link([tuple(c) for c in pd])
    if seed is not None:
        random.seed(seed)
        K.simplify('global')
        K.backtrack(steps=25)
        K.simplify('global')
    else:
        K.simplify('global')
    return K

record = {
    'knot': d['name'], 'pd_sha256_16': pd_hash,
    'date': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'within_sage': within_sage,
    'box': {'n_diagrams': n_diagrams, 'max_bands': max_bands,
            'max_twists': max_twists, 'max_band_len': max_band_len,
            'paths': 'shortest', 'seconds_per_diagram': budget,
            'filter_for_plausibly_slice': within_sage},
    'diagrams': [], 'unknot_found': False, 'certificates': [],
}

t_all = time.time()
for i in range(n_diagrams):
    seed = None if i == 0 else 1000 + i
    K = fresh(seed)
    entry = {'index': i, 'seed': seed, 'crossings': len(K.crossings)}
    t0 = time.time()
    try:
        res = ribbon_concordant_links(
            K, max_bands=max_bands, max_twists=max_twists,
            max_band_len=max_band_len, paths='shortest',
            filter_for_plausibly_slice=within_sage,
            use_ribbon_link_cache=True, certify=within_sage,
            print_progress=False)
        entry['results'] = len(res)
        entry['unknot'] = 'unknot' in res
        # Persist the frontier itself. Values are spherogram's replayable
        # [starting PD code, band descriptor, endpoint name] triples.
        # A list, not a dict keyed by str(link): the Link repr is not unique.
        entry['frontier'] = [{'label': str(k), 'certificate': v}
                             for k, v in res.items()]
        if 'unknot' in res:
            record['unknot_found'] = True
            cert = res['unknot']
            ok = None
            try:
                ok = bool(verify_ribbon_to_unknot(K, cert))
            except Exception as e:
                ok = 'error: %s' % e
            record['certificates'].append(
                {'diagram': i, 'seed': seed, 'verified': ok,
                 'certificate': [str(c) for c in cert]})
    except Exception as e:
        entry['error'] = '%s: %s' % (type(e).__name__, e)
    entry['seconds'] = round(time.time() - t0, 1)
    record['diagrams'].append(entry)
    print(json.dumps({k: v for k, v in entry.items() if k != 'frontier'}), flush=True)
    if record['unknot_found']:
        print('RIBBON DISK FOUND', flush=True)
        break

record['total_seconds'] = round(time.time() - t_all, 1)
json.dump(record, open(out, 'w'), indent=1, default=str)
print(json.dumps({k: v for k, v in record.items() if k != 'diagrams'}, indent=1))
