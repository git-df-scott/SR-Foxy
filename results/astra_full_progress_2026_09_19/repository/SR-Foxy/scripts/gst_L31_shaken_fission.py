#!/usr/bin/env python3
"""Recover GST's L_{3,1} as a one-band fission, searching many diagrams.

The single-diagram pass (scripts/gst_link_from_band_fission.py) enumerated
3209-4123 bands on Regina's diagram of the Figure 2 knot and produced three
candidates, all REJECTED by scripts/verify_L31_candidates.py: their components
were (genus 1, non-fibered) and (genus 5 or 2, fibered), not the square knot
(genus 2, fibered) with V_3 = 8_19 # -8_19 (genus 6, fibered).

That is the expected failure. The band of GST Figure 1 lives on GST's own
drawing of L_{3,1}; Regina's gst() is a different diagram of the same knot, so
the band need not be short there. Shaking the diagram gives it other chances.

Acceptance is on genus and fiberedness directly, not on determinant: 6_1 and
9_46 also have determinant 9, so the cheap screen admits impostors.
"""
import json, os, random, sys, time
import snappy
from spherogram.links.bands.core import (min_len_bands, add_one_band,
                                         normalize_crossing_labels)
from knot_floer_homology import pd_to_hfk

MAX_TWISTS = int(os.environ.get('GST_TWISTS', 2))
MAX_LEN = int(os.environ.get('GST_LEN', 7))
DIAGRAMS = int(os.environ.get('GST_DIAGRAMS', 40))
BACKTRACK = int(os.environ.get('GST_BACKTRACK', 30))
DEADLINE = float(os.environ.get('GST_SECONDS', 20000))
SEED = int(os.environ.get('GST_SEED', 20260915))

WANT = sorted([(2, True), (6, True)])       # square knot, V_3


def profile(L):
    L = L.copy()
    L.simplify('global')
    if not L.crossings:
        return (0, True, 1)
    h = pd_to_hfk([tuple(c) for c in L.PD_code()])
    return (h['seifert_genus'], h['fibered'], abs(int(L.determinant())))


def main(out_path):
    if os.path.exists(out_path):
        sys.exit('refusing to overwrite %s' % out_path)
    data = json.load(open('data/knots/GST_knot.json'))
    K = snappy.Link([tuple(c) for c in data['pd_code_snappy_0indexed']])
    random.seed(SEED)
    rec = {'source_knot': data['name'],
           'box': {'max_twists': MAX_TWISTS, 'max_band_len': MAX_LEN,
                   'diagrams': DIAGRAMS, 'backtrack': BACKTRACK,
                   'seed': SEED, 'deadline_seconds': DEADLINE},
           'acceptance': ('components (genus 2, fibered) and (genus 6, '
                          'fibered), linking number 0'),
           'counts': {'bands': 0, 'linking_zero': 0, 'det_9_9': 0,
                      'diagrams_done': 0},
           'hits': [], 'near_misses': [], 'stop': None,
           'scope': ('A hit is a NOMINATION. Sliceness does not follow from a '
                     'fission of a slice knot; it needs the R-link property, '
                     '0-surgery on both components giving #2(S^1 x S^2), and '
                     'even that gives a disk only in a homotopy 4-ball.')}
    t0 = time.time()
    try:
        for diagram in range(DIAGRAMS):
            if time.time() - t0 > DEADLINE:
                rec['stop'] = 'deadline'
                break
            D = K.copy()
            if diagram:
                D.backtrack(BACKTRACK)
                D.simplify('global')
                # Required: min_len_bands raises
                # ValueError('Link needs normalized crossing labels') on a
                # shaken diagram.  This script had never been run, so the
                # fault was latent.
                normalize_crossing_labels(D)
            for band in min_len_bands(D, max_twists=MAX_TWISTS,
                                      max_band_len=MAX_LEN):
                if time.time() - t0 > DEADLINE:
                    rec['stop'] = 'deadline'
                    break
                rec['counts']['bands'] += 1
                try:
                    L = add_one_band(D.copy(), band)
                    L.simplify('global')
                    if len(L.link_components) != 2:
                        continue
                    if L.linking_matrix()[0][1] != 0:
                        continue
                    rec['counts']['linking_zero'] += 1
                    profs = []
                    for i in range(2):
                        M = L.copy()
                        profs.append(profile(M.sublink([M.link_components[i]])))
                    if sorted(p[2] for p in profs) != [9, 9]:
                        continue
                    rec['counts']['det_9_9'] += 1
                    entry = {'diagram': diagram, 'profiles': profs,
                             'link_crossings': len(L.crossings),
                             'pd_code': L.PD_code()}
                    if sorted((p[0], p[1]) for p in profs) == WANT:
                        rec['hits'].append(entry)
                        print('*** L_{3,1} CANDIDATE ***',
                              json.dumps(profs), flush=True)
                    else:
                        rec['near_misses'].append(
                            {k: v for k, v in entry.items() if k != 'pd_code'})
                except Exception:
                    continue
            rec['counts']['diagrams_done'] = diagram + 1
            rec['elapsed_seconds'] = round(time.time() - t0, 1)
            json.dump(rec, open(out_path, 'w'), indent=1, default=str)
            print(json.dumps(rec['counts']), flush=True)
    finally:
        rec['stop'] = rec['stop'] or 'enumeration_finished'
        rec['elapsed_seconds'] = round(time.time() - t0, 1)
        json.dump(rec, open(out_path, 'w'), indent=1, default=str)
    print('HITS:', len(rec['hits']), 'near misses:', len(rec['near_misses']))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1
         else 'results/gst_L31_shaken_fission.json')
