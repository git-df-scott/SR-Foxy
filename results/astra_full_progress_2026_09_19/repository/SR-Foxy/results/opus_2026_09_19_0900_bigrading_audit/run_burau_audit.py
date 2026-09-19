#!/usr/bin/env python3
"""Independent bigrading audit for the Abe-Tagami family, written incrementally.

Checks, per knot, that the graded Euler characteristic of the STORED HFK
bigradings equals Delta computed with no Floer code and no Seifert surface --
from the braid word via the reduced Burau representation (burau_alexander.py,
9/9 controls) -- plus the HFK symmetry rank(A,M) = rank(-A,M-2A), Alexander
support [-g,g], and rank 1 at the top grading for a fibered knot.

This settles risk 1/2 of research/opus_mixed_lift_review.md, which a relative
Alexander error, a mirror convention flip or a U<->V swap would each break, and
which had stayed open only because every recomputation used the same engine.

Writes one JSON line per knot as it finishes.  The first version of this audit
accumulated in memory and dumped at the end; a container restart during K_2
therefore lost the completed K_0 and K_1 rows, which had to be recovered from a
log.  Cheapest knots first, so a restart costs the least.

Usage: run_burau_audit.py <out.jsonl>
"""
import json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
sys.path.insert(0, HERE)

import snappy
from burau_alexander import alexander_from_braid, normalise

KNOTS = [('K_0', 'AbeTagami_K_0_K_-1__6_3.json'),
         ('K_1', 'AbeTagami_K_1.json'),
         ('K_2', 'AbeTagami_K_2.json'),
         ('K_3', 'AbeTagami_K_3.json')]


def euler(ranks):
    p = {}
    for k, v in ranks.items():
        A, M = (int(x) for x in k.split(','))
        p[A] = p.get(A, 0) + ((-1) ** M) * v
    lo, hi = min(p), max(p)
    return normalise([p.get(a, 0) for a in range(hi, lo - 1, -1)]), lo, hi


def symmetry_violations(ranks):
    R = {}
    for k, v in ranks.items():
        A, M = (int(x) for x in k.split(','))
        R[(A, M)] = v
    return [(A, M) for (A, M), v in R.items() if R.get((-A, M - 2 * A), 0) != v]


def main():
    out = sys.argv[1]
    stored = json.load(open(os.path.join(
        ROOT, 'results', 'opus_2026_09_18_0040_hfk_delta_law', 'RESULTS.json')))['hfk']

    done = set()
    if os.path.exists(out):
        for line in open(out):
            try:
                done.add(json.loads(line)['knot'])
            except Exception:
                pass

    fh = open(out, 'a')
    t0 = time.time()
    for name, fn in KNOTS:
        if name in done:
            continue
        d = json.load(open(os.path.join(ROOT, 'data', 'knots', fn)))
        pd = d.get('pd_code_snappy_0indexed') or d['pd_code']
        L = snappy.Link([tuple(c) for c in pd])
        w = L.braid_word()
        n = max(abs(g) for g in w) + 1
        print(f'{name}: {len(L.crossings)} crossings, braid on {n} strands, '
              f'word length {len(w)}', flush=True)
        try:
            burau = alexander_from_braid(w, n)
        except Exception as e:
            row = dict(knot=name, error=f'{type(e).__name__}: {e}'[:200])
            fh.write(json.dumps(row) + '\n'); fh.flush(); os.fsync(fh.fileno())
            print(f'  {name}: ERROR {type(e).__name__}', flush=True)
            continue
        h = stored[name]
        e, lo, hi = euler(h['ranks'])
        sv = symmetry_violations(h['ranks'])
        top = sum(v for k, v in h['ranks'].items() if int(k.split(',')[0]) == hi)
        match = (e == burau) or (e == burau[::-1])
        row = dict(knot=name, crossings=len(L.crossings), braid_strands=n,
                   braid_length=len(w),
                   euler_from_stored_hfk=e, alexander_from_burau=burau,
                   euler_matches_alexander=bool(match),
                   symmetry_violations=len(sv),
                   alexander_support=[lo, hi], genus=h['genus'],
                   support_is_pm_genus=bool(hi == h['genus'] and -lo == h['genus']),
                   top_grading_rank=top, fibered=h['fibered'],
                   fibered_top_rank_one=bool(top == 1),
                   all_pass=bool(match and not sv and hi == h['genus']
                                 and -lo == h['genus'] and top == 1),
                   seconds=round(time.time() - t0, 1))
        fh.write(json.dumps(row) + '\n'); fh.flush(); os.fsync(fh.fileno())
        print(f'  {name}: euler={e} burau={burau} match={match} '
              f'sym_viol={len(sv)} ALL_PASS={row["all_pass"]}', flush=True)
    fh.close()


if __name__ == '__main__':
    main()
