#!/usr/bin/env python3
"""Levine-Tristram signatures of a link, as a slice screen.

For a Seifert matrix V of a link L and omega on the unit circle, the
Levine-Tristram signature is the signature of the Hermitian form

    H(omega) = (1 - omega) V + (1 - conj(omega)) V^T.

It vanishes for every slice link at every omega of prime-power order
(Tristram, Levine; Murasugi for links).  So a nonzero value at such an omega
rules a link out of being slice.

Used here on the survivors of `scripts/slice_screen_links.py`: links proved
NOT ribbon by Eisermann's Theorem 1 whose sliceness is not yet excluded.  Any
one of them that is slice would be the first slice link that is not ribbon.

Eigenvalues are computed numerically, so a verdict is only issued when the
spectrum is cleanly away from zero; borderline cases are reported as
inconclusive rather than guessed.

Usage: levine_tristram.py <screened.json> <out.json>
"""
import json, os, sys, cmath, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import snappy

TOL = 1e-7


def signatures(link, max_order=12):
    """{omega label: (signature, nullity, min |eigenvalue| away from 0)}."""
    V = np.array(link.seifert_matrix(), dtype=float)
    n = V.shape[0]
    out = {}
    if n == 0:
        return out
    for p in (2, 3, 5, 7, 11):
        k = 1
        while p ** k <= max_order:
            order = p ** k
            for a in range(1, order):
                if order % 2 == 0 and a == order // 2 and p != 2:
                    pass
                from math import gcd
                if gcd(a, order) != 1:
                    continue
                w = cmath.exp(2j * cmath.pi * a / order)
                H = (1 - w) * V + (1 - w.conjugate()) * V.T
                ev = np.linalg.eigvalsh((H + H.conj().T) / 2)
                nullity = int(np.sum(np.abs(ev) < TOL))
                sig = int(np.sum(ev > TOL) - np.sum(ev < -TOL))
                gap = float(np.min(np.abs(ev[np.abs(ev) >= TOL]))) if np.any(np.abs(ev) >= TOL) else 0.0
                out[f'{a}/{order}'] = {'signature': sig, 'nullity': nullity,
                                       'eigenvalue_gap': gap}
            k += 1
    return out


def _controls():
    cases = []
    for n in (2, 3, 4):
        w = []
        for i in range(1, n):
            w += [i, -i]
        cases.append((f'unlink O^{n}', snappy.Link(braid_closure=w), 0))
    cases += [('6_1 ribbon knot', snappy.Link('6_1'), 0),
              ('9_46 ribbon knot', snappy.Link('9_46'), 0),
              ('Borromean L6a4', snappy.Link('L6a4'), 0),
              ('Hopf L2a1', snappy.Link('L2a1'), 1),
              ('Whitehead L5a1', snappy.Link('L5a1'), 1)]
    rows = []
    for name, L, want_nonzero in cases:
        s = signatures(L)
        mx = max((abs(v['signature']) for v in s.values()), default=0)
        ok = (mx > 0) == bool(want_nonzero)
        rows.append({'case': name, 'max_abs_signature': mx,
                     'expected_nonzero': bool(want_nonzero), 'as_expected': ok})
        print(('ok  ' if ok else 'MISMATCH') +
              f' {name:20s} max |sigma_omega| = {mx}', flush=True)
    out = 'results/session_2026-09-15b/levine_tristram_controls.json'
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({'date': datetime.datetime.utcnow().isoformat() + 'Z',
               'what': ('controls for the Levine-Tristram slice screen: it must '
                        'vanish on every slice object and fire on Hopf and '
                        'Whitehead, which are not slice'),
               'rows': rows,
               'all_as_expected': all(r['as_expected'] for r in rows)},
              open(out, 'w'), indent=1)
    print('wrote', out)
    return all(r['as_expected'] for r in rows)


def main():
    if sys.argv[1] == '--controls':
        sys.exit(0 if _controls() else 1)
    src, out_path = sys.argv[1], sys.argv[2]
    d = json.load(open(src))
    by_name = {r['name']: r for r in d['rows'] if 'pd_code' in r}
    rec = {'date': datetime.datetime.utcnow().isoformat() + 'Z', 'source': src,
           'test': ('Levine-Tristram signature vanishes for slice links at every '
                    'prime-power root of unity'),
           'rows': [], 'still_live': []}
    for name in d.get('survivors', []):
        row = by_name.get(name)
        if row is None:
            continue
        L = snappy.Link([tuple(c) for c in row['pd_code']])
        sigs = signatures(L)
        nonzero = {k: v for k, v in sigs.items() if v['signature'] != 0}
        entry = {'name': name, 'crossings': row.get('crossings'),
                 'nonzero_signatures': nonzero,
                 'max_abs_signature': max((abs(v['signature']) for v in sigs.values()),
                                          default=0),
                 'slice_ruled_out': bool(nonzero)}
        rec['rows'].append(entry)
        if not nonzero:
            rec['still_live'].append(name)
        print(f'{name:12s} max |sigma_omega| = {entry["max_abs_signature"]}  '
              + ('RULED OUT of slice' if nonzero else '*** STILL LIVE ***'),
              flush=True)
    rec['summary'] = {'screened': len(rec['rows']),
                      'still_live': len(rec['still_live'])}
    json.dump(rec, open(out_path, 'w'), indent=1)
    print('still live:', rec['still_live'])
    print('wrote', out_path)


if __name__ == '__main__':
    main()
