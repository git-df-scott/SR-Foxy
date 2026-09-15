#!/usr/bin/env python3
"""Decide whether a band-fission candidate really is GST's L_{3,1}.

Required, from GST p.2 and Prop 2.2: two components, linking number 0, one
component the square knot Q = 3_1 # -3_1 (genus 2, fibered, determinant 9,
Alexander (t - 1 + 1/t)^2), the other V_3 = T_{3,4} # mirror(T_{3,4})
= 8_19 # -8_19 (genus 6, fibered, determinant 9, Alexander Delta_{8_19}^2).

Determinant 9 alone proves nothing: 6_1 and 9_46 also have determinant 9.
Genus and fiberedness are the discriminating tests, so they run here.
"""
import json, os, sys
import snappy
from knot_floer_homology import pd_to_hfk


def knot_profile(L):
    L = L.copy()
    L.simplify('global')
    if len(L.crossings) == 0:
        return {'crossings': 0, 'genus': 0, 'fibered': True, 'det': 1,
                'alexander': '1'}
    h = pd_to_hfk([tuple(c) for c in L.PD_code()])
    return {'crossings': len(L.crossings),
            'genus': h['seifert_genus'], 'fibered': h['fibered'],
            'det': abs(int(L.determinant())),
            'total_rank': h['total_rank'], 'tau': h['tau']}


def reference_profiles():
    Q = snappy.Link('3_1')
    Q = Q.connected_sum(snappy.Link('3_1').mirror())
    V = snappy.Link('8_19')
    V = V.connected_sum(snappy.Link('8_19').mirror())
    return {'square_knot Q = 3_1 # -3_1': knot_profile(Q),
            'V_3 = 8_19 # -8_19': knot_profile(V)}


def main(out_path):
    if os.path.exists(out_path):
        sys.exit('refusing to overwrite %s' % out_path)
    refs = reference_profiles()
    print('REFERENCES:')
    for k, v in refs.items():
        print('  %-28s %s' % (k, json.dumps(v)))
    want_Q = (refs['square_knot Q = 3_1 # -3_1']['genus'],
              refs['square_knot Q = 3_1 # -3_1']['fibered'])
    want_V = (refs['V_3 = 8_19 # -8_19']['genus'],
              refs['V_3 = 8_19 # -8_19']['fibered'])

    seen, rows = set(), []
    for src in ('results/gst_L31_band_fission.json',
                'results/gst_L31_fission_len8.json',
                'results/gst_L31_fission_tw3.json'):
        if not os.path.exists(src):
            continue
        for cand in json.load(open(src))['candidates']:
            key = tuple(sorted(cand['component_crossings']))
            if key in seen:
                continue
            seen.add(key)
            L = snappy.Link([tuple(c) for c in cand['pd_code']])
            profs = []
            for i in range(len(L.link_components)):
                M = L.copy()
                profs.append(knot_profile(M.sublink([M.link_components[i]])))
            got = sorted((p['genus'], p['fibered']) for p in profs)
            row = {'source': src.split('/')[-1],
                   'component_crossings': cand['component_crossings'],
                   'linking_number': cand['linking_number'],
                   'component_profiles': profs,
                   'matches_L31': got == sorted([want_Q, want_V])}
            rows.append(row)
            print('CANDIDATE %-18s profiles=%s  -> is L_{3,1}? %s'
                  % (str(cand['component_crossings']),
                     [(p['genus'], p['fibered'], p['det']) for p in profs],
                     row['matches_L31']))
    result = {'references': refs, 'candidates': rows,
              'any_match': any(r['matches_L31'] for r in rows),
              'scope': ('Genus + fiberedness + determinant is strong but not '
                        'a proof of knot type. A positive still needs the '
                        'R-link property: 0-surgery on both components giving '
                        '#2(S^1 x S^2).')}
    json.dump(result, open(out_path, 'w'), indent=1, default=str)
    print('ANY MATCH:', result['any_match'])


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1
         else 'results/L31_candidate_verification.json')
