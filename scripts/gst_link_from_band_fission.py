#!/usr/bin/env python3
"""Recover GST's link L_{3,1} as a one-band fission of the Figure 2 knot.

GST (arXiv:1103.1601), p.2: "Figure 2 shows a simple potential counterexample
obtained from L_{3,1} by the band-move following the dotted arc in Figure 1."
Regina's ExampleLink.gst() is that Figure 2 knot, 48 crossings, already in
data/knots/GST_knot.json.  So L_{3,1} is a one-band fission of a knot we hold,
and enumerating bands recovers it without transcribing Figure 1 by eye --
which matters, because a subtly mis-read diagram would give a wrong Jones
polynomial and could masquerade as an Eisermann violation.

Acceptance test, from GST p.2 and Figure 14.  L_{n,1} is the square knot
interleaved with T_{n,n+1} # mirror(T_{n,n+1}); the components are
algebraically unlinked (Prop 2.2).  So for n = 3 a candidate must have:
  * exactly 2 components,
  * linking number 0,
  * one component the square knot: determinant 9, genus 2, fibered,
  * the other T_{3,4} # mirror(T_{3,4}) = 8_19 # -8_19: determinant 9,
    genus 6, fibered.
Determinant 9 twice is cheap to screen on; the genus/fibered test is the
expensive confirmation and runs only on survivors.
"""
import json, os, sys, time
import snappy
from spherogram.links.bands.core import min_len_bands, add_one_band

MAX_TWISTS = int(os.environ.get('GST_TWISTS', 2))
MAX_LEN = int(os.environ.get('GST_LEN', 6))
DEADLINE = float(os.environ.get('GST_SECONDS', 6000))


def component_data(L):
    """(determinant, crossings) for each component, after simplification."""
    out = []
    for i in range(len(L.link_components)):
        M = L.copy()
        S = M.sublink([M.link_components[i]])
        S.simplify('global')
        if len(S.crossings) == 0:
            out.append((1, 0))
        else:
            out.append((abs(int(S.determinant())), len(S.crossings)))
    return out


def main(out_path):
    if os.path.exists(out_path):
        sys.exit('refusing to overwrite %s' % out_path)
    data = json.load(open('data/knots/GST_knot.json'))
    K = snappy.Link([tuple(c) for c in data['pd_code_snappy_0indexed']])
    rec = {'source_knot': data['name'],
           'source_crossings': len(K.crossings),
           'box': {'max_twists': MAX_TWISTS, 'max_band_len': MAX_LEN,
                   'deadline_seconds': DEADLINE},
           'target': ('L_{3,1}: 2 components, linking number 0, both '
                      'component determinants 9 (square knot and '
                      '8_19 # -8_19)'),
           'counts': {'bands': 0, 'two_component': 0, 'linking_zero': 0,
                      'det_9_9': 0},
           'candidates': [], 'complete': False, 'stop': None,
           'scope': ('A candidate here is a NOMINATION, not L_{3,1}. It still '
                     'needs component genus/fiberedness and, decisively, the '
                     'R-link property: 0-surgery on both components giving '
                     '#2(S^1 x S^2).')}
    t0 = time.time()
    for band in min_len_bands(K, max_twists=MAX_TWISTS, max_band_len=MAX_LEN):
        if time.time() - t0 > DEADLINE:
            rec['stop'] = 'deadline'
            break
        rec['counts']['bands'] += 1
        try:
            L = add_one_band(K.copy(), band)
            L.simplify('global')
        except Exception:
            continue
        if len(L.link_components) != 2:
            continue
        rec['counts']['two_component'] += 1
        try:
            lk = L.linking_matrix()[0][1]
        except Exception:
            continue
        if lk != 0:
            continue
        rec['counts']['linking_zero'] += 1
        try:
            dets = component_data(L)
        except Exception:
            continue
        if sorted(d for d, _ in dets) != [9, 9]:
            continue
        rec['counts']['det_9_9'] += 1
        rec['candidates'].append({
            'band': str(band), 'linking_number': lk,
            'component_determinants': [d for d, _ in dets],
            'component_crossings': [c for _, c in dets],
            'link_crossings': len(L.crossings),
            'pd_code': L.PD_code()})
        print('CANDIDATE', json.dumps(rec['candidates'][-1])[:200], flush=True)
        json.dump(rec, open(out_path, 'w'), indent=1, default=str)
    else:
        rec['complete'] = True
        rec['stop'] = rec['stop'] or 'enumeration_finished'
    rec['elapsed_seconds'] = round(time.time() - t0, 1)
    json.dump(rec, open(out_path, 'w'), indent=1, default=str)
    print(json.dumps(rec['counts']), 'candidates:', len(rec['candidates']),
          'stop:', rec['stop'], flush=True)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1
         else 'results/gst_L31_band_fission.json')
