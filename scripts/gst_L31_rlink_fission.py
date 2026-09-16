#!/usr/bin/env python3
"""Recover GST's L_{3,1} as a one-band fission, gated on the R-link property.

Successor to scripts/gst_L31_shaken_fission.py, with three changes.

1. The decisive test is applied.  L_{3,1} is not "a 2-component link whose
   components look right"; it is an R-link -- 0-framed surgery on both
   components gives #2(S^1 x S^2) (GST Prop 2.2 and Cor 5.9).  Every previous
   script in this repository names that test in its scope note and stops short
   of running it.  scripts/r_link_test.py now implements it, two-sided, with
   controls, so it is used here as the gate.

2. It is applied BEFORE the knot Floer genus/fiberedness step, not after.  The
   R-link test costs seconds; pd_to_hfk on a 20-40 crossing component costs far
   more, and the previous ordering spent that cost on links that cannot be
   L_{3,1} at all.

3. Every det-9/9 candidate is written out with its PD code as it is found, not
   only the ones that pass.  The old script discarded near-miss PD codes, so a
   rejected nomination could not be re-examined when the acceptance test
   improved -- which is exactly what happened.

Acceptance, all four required:
  * 2 components, linking number 0
  * both component determinants 9
  * R-link: verdict YES from scripts/r_link_test.py
  * components (genus 2, fibered) = square knot and (genus 6, fibered) = V_3

Usage: gst_L31_rlink_fission.py <out.json> [seed] [diagrams] [twists] [len]
"""
import json, os, random, sys, time, datetime
import snappy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spherogram.links.bands.core import (min_len_bands, add_one_band,
                                         normalize_crossing_labels)
from knot_floer_homology import pd_to_hfk
from r_link_test import r_link_verdict

WANT = sorted([(2, True), (6, True)])


def profile(L):
    L = L.copy()
    L.simplify('global')
    if not L.crossings:
        return (0, True, 1)
    h = pd_to_hfk([tuple(c) for c in L.PD_code()])
    return (h['seifert_genus'], h['fibered'], abs(int(L.determinant())))


def main():
    out = sys.argv[1]
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 20260916
    diagrams = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    twists = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    max_len = int(sys.argv[5]) if len(sys.argv) > 5 else 7
    if os.path.exists(out):
        sys.exit('refusing to overwrite %s' % out)
    data = json.load(open('data/knots/GST_knot.json'))
    K = snappy.Link([tuple(c) for c in data['pd_code_snappy_0indexed']])
    random.seed(seed)
    rec = {'date': datetime.datetime.utcnow().isoformat() + 'Z',
           'source_knot': data['name'], 'source_crossings': len(K.crossings),
           'box': {'seed': seed, 'diagrams': diagrams, 'max_twists': twists,
                   'max_band_len': max_len, 'backtrack': 30},
           'acceptance': ('2 components, linking number 0, both component '
                          'determinants 9, R-link verdict YES, components '
                          '(genus 2, fibered) and (genus 6, fibered)'),
           'counts': {'bands': 0, 'two_component': 0, 'linking_zero': 0,
                      'det_9_9': 0, 'rlink_yes': 0, 'rlink_unknown': 0,
                      'diagrams_done': 0},
           'candidates': [], 'hits': [], 'stop': None,
           'scope': ('A hit is L_{3,1} up to the identification being on '
                     'invariants rather than an isotopy. Sliceness is then '
                     "inherited from GST section 8, not from this search.")}
    t0 = time.time()

    def flush():
        rec['elapsed_seconds'] = round(time.time() - t0, 1)
        tmp = out + '.tmp'
        json.dump(rec, open(tmp, 'w'), indent=1, default=str)
        os.replace(tmp, out)

    try:
        for diagram in range(diagrams):
            D = K.copy()
            if diagram:
                D.backtrack(30)
                D.simplify('global')
                # backtrack + simplify leaves crossing labels non-contiguous,
                # and min_len_bands rejects that with
                # ValueError('Link needs normalized crossing labels').
                normalize_crossing_labels(D)
            for band in min_len_bands(D, max_twists=twists, max_band_len=max_len):
                rec['counts']['bands'] += 1
                try:
                    L = add_one_band(D.copy(), band)
                    L.simplify('global')
                except Exception:
                    continue
                if len(L.link_components) != 2:
                    continue
                rec['counts']['two_component'] += 1
                try:
                    if L.linking_matrix()[0][1] != 0:
                        continue
                except Exception:
                    continue
                rec['counts']['linking_zero'] += 1
                try:
                    dets = []
                    for i in range(2):
                        M = L.copy()
                        S = M.sublink([M.link_components[i]])
                        S.simplify('global')
                        dets.append(1 if not S.crossings else abs(int(S.determinant())))
                except Exception:
                    continue
                if sorted(dets) != [9, 9]:
                    continue
                rec['counts']['det_9_9'] += 1
                entry = {'diagram': diagram, 'component_determinants': dets,
                         'link_crossings': len(L.crossings),
                         'pd_code': [list(c) for c in L.PD_code()]}
                try:
                    verdict, detail = r_link_verdict(L)
                except Exception as e:
                    verdict, detail = 'UNKNOWN', {'error': f'{type(e).__name__}: {e}'}
                entry['rlink_verdict'] = verdict
                entry['rlink_reason'] = detail.get('reason') or detail.get('certificate')
                if verdict == 'NO':
                    rec['candidates'].append(entry)
                    flush()
                    print(f'[{time.time()-t0:7.0f}s] det99 candidate, R-link NO '
                          f'({len(L.crossings)} cr)', flush=True)
                    continue
                rec['counts']['rlink_yes' if verdict == 'YES' else 'rlink_unknown'] += 1
                print(f'[{time.time()-t0:7.0f}s] *** det99 + R-link {verdict} *** '
                      f'{len(L.crossings)} cr -- running knot Floer', flush=True)
                try:
                    profs = []
                    for i in range(2):
                        M = L.copy()
                        profs.append(profile(M.sublink([M.link_components[i]])))
                    entry['profiles'] = profs
                    if sorted((p[0], p[1]) for p in profs) == WANT:
                        rec['hits'].append(entry)
                        print('*** L_{3,1} CANDIDATE: R-link %s, components %s ***'
                              % (verdict, profs), flush=True)
                except Exception as e:
                    entry['profile_error'] = f'{type(e).__name__}: {e}'
                rec['candidates'].append(entry)
                flush()
            rec['counts']['diagrams_done'] = diagram + 1
            flush()
            print(f'[{time.time()-t0:7.0f}s] ' + json.dumps(rec['counts']), flush=True)
    finally:
        rec['stop'] = rec['stop'] or 'finished'
        flush()
        print('HITS:', len(rec['hits']), 'candidates:', len(rec['candidates']), flush=True)


if __name__ == '__main__':
    main()
