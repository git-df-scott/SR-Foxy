#!/usr/bin/env python3
"""d-invariants of L(p,q) by the Ozsvath-Szabo recursion.

Ozsvath-Szabo, "Absolutely graded Floer homologies and intersection forms
for four-manifolds with boundary", Adv. Math. 173 (2003), Proposition 4.8:

    d(-L(1,0), 0) = 0
    d(-L(p,q), i) = ((2i+1-p-q)^2 - pq)/(4pq) - d(-L(q, p mod q), i mod q)

for p > q >= 1 and 0 <= i < p+q, and d(L(p,q), i) = -d(-L(p,q), i).

This supplies one half of the branched-cover slice obstruction for
D01 = K_0 # (-K_1): Sigma_2(K_0) = Sigma_2(6_3) = L(13,5), because 6_3 is
the two-bridge knot S(13,5).  See research/21.
"""
from fractions import Fraction
import json, os, sys


def d_minus(p, q, i):
    if p == 1:
        return Fraction(0)
    q %= p
    return (Fraction((2*i + 1 - p - q)**2 - p*q, 4*p*q)
            - d_minus(q, p % q, i % q))


def spectrum(p, q):
    """The multiset {d(-L(p,q), i)}, indexed by spin^c structure."""
    return [d_minus(p, q, i) for i in range(p)]


CONTROLS = {
    # published values, used as regression controls
    (2, 1): ['1/4', '-1/4'],
    (3, 1): ['1/2', '-1/6', '-1/6'],
    (5, 1): ['1', '1/5', '-1/5', '-1/5', '1/5'],
}


def main(out_path):
    if os.path.exists(out_path):
        sys.exit('refusing to overwrite %s' % out_path)
    result = {'controls': {}, 'targets': {}}
    for (p, q), expected in CONTROLS.items():
        got = [str(x) for x in spectrum(p, q)]
        result['controls']['-L(%d,%d)' % (p, q)] = {
            'computed': got, 'expected': expected, 'agrees': got == expected}
    assert all(c['agrees'] for c in result['controls'].values())

    s = spectrum(13, 5)
    result['targets']['Sigma_2(K_0) = Sigma_2(6_3) = L(13,5)'] = {
        'd_of_minus_L': [str(x) for x in s],
        'multiset_sorted': sorted(str(x) for x in s),
        'orientation_independent': sorted(s) == sorted(-x for x in s),
        'note': ('The multiset is symmetric under negation, as it must be: '
                 '6_3 is negative amphichiral and L(13,5) = -L(13,5) because '
                 '5 * 8 = 1 mod 13.  So the obstruction below does not depend '
                 'on an orientation convention for Sigma_2(K_0).'),
    }
    result['obstruction'] = (
        'If D01 = K_0 # (-K_1) is smoothly slice then Sigma_2(D01) = '
        'L(13,5) # -Sigma_2(K_1) bounds a rational homology ball, so the '
        'd-invariants vanish on a coset of a metabolizer M of the linking '
        'form on H_1 = Z/13 + Z/13.  The linking form is nondegenerate on '
        'each factor, so M is a graph of an isomorphism Z/13 -> Z/13 and '
        'projects onto both factors.  Additivity of d under connected sum '
        'then forces the 13 d-invariants of Sigma_2(K_1) to equal, as a '
        'multiset, those of L(13,5).')
    with open(out_path, 'w') as fh:
        json.dump(result, fh, indent=1, sort_keys=True)
    print(json.dumps(result, indent=1, sort_keys=True))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1
         else 'results/lens_d_invariants.json')
