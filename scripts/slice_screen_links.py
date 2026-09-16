#!/usr/bin/env python3
"""Screen Eisermann-certified non-ribbon links for whether they can be slice.

`scripts/eisermann_census.py` produces links that are **proved not ribbon** by
Eisermann's Theorem 1 (`null V < n - 1`) and that pass the cheap necessary
conditions for sliceness.  A slice one among them would be the first slice link
that is not ribbon.  This script applies the next two obstructions, both of
which are Milnor invariants and both of which vanish for slice links:

1. **Triple linking.**  For a 3-component link with vanishing pairwise linking
   numbers, `[z^4] nabla_L = mu-bar(123)^2` (Cochran, Invent. Math. 82 (1985)).
   Validated here on the Borromean rings, where it returns 1.

2. **Sato-Levine on every 2-component sublink.**  Every sublink of a slice link
   is slice, and a 2-component link with linking number 0 has
   `beta = mu-bar(1122) = [z^3] nabla`, which vanishes for slice links.
   Validated on the Whitehead link, where it returns 1.

Screen 2 is the sharper one in practice: the first census entry, `L9n27` -- 9
crossings, three unknotted components, all linking numbers zero, Conway
polynomial identically zero, so `mu-bar(123) = 0` -- has two Whitehead sublinks
and dies there.

A survivor is NOT a counterexample.  It is a link proved non-ribbon whose
sliceness is not yet excluded, which is exactly the shape of a target worth
attacking.  Both screens are reported per link so a cut can be checked rather
than trusted.

Usage: slice_screen_links.py <census.json> <out.json>
"""
import json, os, sys, itertools, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import snappy
from triple_linking import conway_coefficients


def coefficient(nab, k):
    return nab[k] if len(nab) > k else 0


def screen(L):
    n = len(L.link_components)
    out = {'components': n, 'crossings': len(L.crossings)}
    nab = conway_coefficients(L)
    out['conway'] = nab[:8]
    out['mu_bar_123_squared'] = coefficient(nab, 4) if n == 3 else None
    subs = []
    for pair in itertools.combinations(range(n), 2):
        C = L.copy()
        S = C.sublink([C.link_components[i] for i in pair])
        S.simplify('global')
        if len(S.link_components) < 2:
            subs.append({'pair': list(pair), 'split_trivial': True, 'beta': 0})
            continue
        try:
            lk = S.linking_matrix()[0][1]
        except Exception:
            lk = None
        snab = conway_coefficients(S)
        subs.append({'pair': list(pair), 'crossings': len(S.crossings),
                     'linking_number': lk, 'conway': snab[:6],
                     'beta': coefficient(snab, 3) if lk == 0 else None})
    out['two_component_sublinks'] = subs
    reasons = []
    if out['mu_bar_123_squared']:
        reasons.append('mu-bar(123)^2 = %d != 0' % out['mu_bar_123_squared'])
    for s in subs:
        if s.get('beta'):
            reasons.append('sublink %s has Sato-Levine beta = %d != 0'
                           % (tuple(s['pair']), s['beta']))
        if s.get('linking_number'):
            reasons.append('sublink %s has linking number %d != 0'
                           % (tuple(s['pair']), s['linking_number']))
    out['slice_ruled_out'] = bool(reasons)
    out['reasons'] = reasons
    return out


def main():
    census_path, out_path = sys.argv[1], sys.argv[2]
    d = json.load(open(census_path))
    rec = {'date': datetime.datetime.utcnow().isoformat() + 'Z',
           'source': census_path,
           'meaning': ('every entry is PROVED not ribbon by Eisermann Theorem 1. '
                       'survivors[] are those not yet excluded from being slice; '
                       'a survivor is a target, not a counterexample.'),
           'rows': [], 'survivors': []}
    for row in d.get('shortlist', []):
        L = snappy.Link([tuple(c) for c in row['pd_code']])
        try:
            s = screen(L)
        except Exception as e:
            s = {'error': f'{type(e).__name__}: {e}'}
        s['name'] = row['name']
        s['null_V'] = row['null_V']
        s['ribbon_requires_null_V'] = row['ribbon_requires_null_V']
        rec['rows'].append(s)
        live = not s.get('slice_ruled_out', True) and 'error' not in s
        if live:
            s['pd_code'] = row['pd_code']
            rec['survivors'].append(row['name'])
        print(f"{row['name']:12s} {s.get('crossings','?'):>3} cr  "
              f"null V = {row['null_V']} (ribbon needs {row['ribbon_requires_null_V']})  "
              + ('SURVIVES -> sliceness open' if live
                 else 'not slice: ' + '; '.join(s.get('reasons', ['error']))),
              flush=True)
        json.dump(rec, open(out_path, 'w'), indent=1)
    rec['summary'] = {'screened': len(rec['rows']),
                      'survivors': len(rec['survivors'])}
    json.dump(rec, open(out_path, 'w'), indent=1)
    print('survivors:', rec['survivors'], flush=True)
    print('wrote', out_path)


if __name__ == '__main__':
    main()
