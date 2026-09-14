#!/usr/bin/env python3
"""Eisermann's ribbon-link obstructions, and where they can actually fire.

Markus Eisermann, "The Jones polynomial of ribbon links", Geom. Topol. 13
(2009) 623-660, arXiv:0802.2287, read 14 September 2026:

  Lemma 1.    Every n-component link satisfies 0 <= null V(L) <= n-1.
  Theorem 1.  Every n-component RIBBON link satisfies null V(L) = n-1.
  Theorem 2.  Every n-component RIBBON link L = K_1 u ... u K_n satisfies
              det V(L) = det(K_1)...det(K_n) mod 32, in particular = 1 mod 8.

Here null V(L) is the multiplicity of the zero of V(L) at q = i, and
det V(L) = [V(L)/V(O^n)] evaluated at q = i.

research/02 identifies these as the ONLY genuinely ribbon-only obstructions in
the whole catalog that are also computable: every other entry dies at
handle-ribbon or is not of vanishing type.  Eisermann does not prove either
statement for slice links (his Remark 3.6 gives only the classical nullity and
signature, and Delta(L) = 0 for n >= 2), so the slice case is open.

WHERE THE TESTS CAN FIRE.  Theorem 1 is VACUOUS on 2-component slice links.
A slice link with n >= 2 has Delta(L) = 0, hence det(L) = 0, hence
V(L)(q=i) = 0, hence null V(L) >= 1; Lemma 1 caps null V(L) <= n-1 = 1, so
null V(L) = 1 = n-1 automatically and no 2-component slice link can violate
Theorem 1.  CAMPAIGN_PLAN WS5 proposes exactly this test on GST's L_{3,1},
which has two components, so as written it cannot produce anything.

What remains live:
  (a) Theorem 2 on any slice link, including L_{3,1}: not implied by Delta = 0.
  (b) Theorem 1 on a slice link with n >= 3 components, where slice gives only
      null V >= 1 but ribbon demands n-1 >= 2.
"""
import json, os, sys
import sympy
from sympy import I
import snappy, spherogram


def _jones(L):
    return sympy.sympify(str(L.jones_polynomial(new_convention=True)).replace('^', '**'))


def nullity(L):
    """Multiplicity of the zero of V(L) at q = i."""
    e = _jones(L)
    syms = list(e.free_symbols)
    if not syms:
        return 0
    x = syms[0]
    num = sympy.expand(e * x**80)
    n = 0
    while n <= 16:
        if sympy.simplify(num.subs(x, I)) != 0:
            break
        num = sympy.cancel(num / (x - I))
        n += 1
    return n


def det_V(L, n):
    """[V(L)/V(O^n)] at q = i.  V(O^n) = (q + 1/q)^(n-1) in this normalization,
    fixed by requiring det V(O^n) = 1, which Theorem 2 forces since every
    component of an unlink has determinant 1."""
    e = _jones(L)
    syms = list(e.free_symbols)
    if not syms:
        return sympy.simplify(e)
    x = syms[0]
    quot = sympy.cancel(sympy.simplify(e / (x + 1 / x)**(n - 1)))
    return sympy.simplify(quot.subs(x, I))


def unlink(n):
    word = []
    for j in range(1, n):
        word += [j, -j]
    return spherogram.Link(braid_closure=word)


def report(label, L, n, ribbon, component_dets=None):
    nu = nullity(L)
    row = {'link': label, 'components': n, 'ribbon': ribbon,
           'null_V': nu, 'thm1_satisfied': nu == n - 1}
    if nu == n - 1:
        dv = det_V(L, n)
        row['det_V'] = str(dv)
        if component_dets is not None:
            try:
                expected = 1
                for d in component_dets:
                    expected *= d
                row['expected_mod_32'] = expected % 32
                row['thm2_satisfied'] = (int(dv) - expected) % 32 == 0
            except (TypeError, ValueError):
                row['thm2_satisfied'] = None
    else:
        row['det_V'] = 'undefined (Theorem 1 already fails)'
    return row


def main(out_path):
    if os.path.exists(out_path):
        sys.exit('refusing to overwrite %s' % out_path)
    rows = []
    for n in (2, 3, 4):
        rows.append(report('unlink O^%d' % n, unlink(n), n, True, [1] * n))
    for name, n in (('L2a1', 2), ('L5a1', 2), ('L6a1', 2),
                    ('L6a5', 3), ('L7a1', 2), ('L8a21', 3)):
        rows.append(report(name, snappy.Link(name), n, False))
    # The only two tabulated 2-component links (of 75 scanned) with
    # null V = 1, so the only ones on which Theorem 2 is testable at all.
    # Both components of each are unknots, so the product of determinants
    # is 1.  Both VIOLATE Theorem 2, which is what gives it teeth.
    # Neither is slice: linking number 4 and signature -6 / -4.
    for name in ('L9n18', 'L9n19'):
        r = report(name, snappy.Link(name), 2, False, [1, 1])
        L = snappy.Link(name)
        r['linking_matrix'] = str(L.linking_matrix())
        r['signature'] = int(L.signature())
        r['slice_ruled_out_by'] = 'linking number != 0 and signature != 0'
        rows.append(r)
    result = {
        'source': ('Eisermann, The Jones polynomial of ribbon links, Geom. '
                   'Topol. 13 (2009) 623-660, arXiv:0802.2287'),
        'rows': rows,
        # A ribbon link must satisfy BOTH theorems. A non-ribbon link must
        # fail at least one -- not necessarily Theorem 1: L9n18 and L9n19
        # satisfy Theorem 1 and are caught only by Theorem 2.
        'controls_pass': all(r['thm1_satisfied'] and r.get('thm2_satisfied')
                             for r in rows if r['ribbon'])
                         and all((not r['thm1_satisfied'])
                                 or (r.get('thm2_satisfied') is False)
                                 for r in rows if not r['ribbon']),
        'vacuity': ('Theorem 1 cannot fire on a 2-component slice link: slice '
                    'with n>=2 gives Delta(L)=0, hence det(L)=0, hence '
                    'null V >= 1, and Lemma 1 caps it at n-1 = 1. So '
                    'CAMPAIGN_PLAN WS5, which computes null V of the '
                    '2-component link L_{3,1}, is vacuous as written.'),
        'live_tests': ['Theorem 2 (det V mod 32) on any slice link, L_{3,1} '
                       'included', 'Theorem 1 on a slice link with n >= 3'],
        'theorem_2_has_teeth': ('Of 75 tabulated 2-component links only L9n18 '
                                'and L9n19 have null V = 1, and both VIOLATE '
                                'Theorem 2 (det V = 9 and 25 against a '
                                'component-determinant product of 1). Neither '
                                'is slice: linking number 4, signature -6 and '
                                '-4. So Theorem 2 is a sharp constraint, not a '
                                'formality.'),
        'L_3_1_prediction': ('GST L_{n,1} is the square knot Q interleaved '
                             'with V_n = T_{n,n+1} # mirror(T_{n,n+1}) (GST '
                             'Figure 1, Section 7; slice in Section 8). Both '
                             'components are of the form K # -K, hence ribbon, '
                             'with det(Q) = 9 and det(V_3) = 9. So if L_{3,1} '
                             'is ribbon then det V(L_{3,1}) = 81 = 17 mod 32. '
                             'Theorem 1 is automatic here, so this single '
                             'congruence is the whole test.'),
        'scope': ('Controls only. No slice link is tested here: GST L_{3,1} is '
                  'not in the repository and must be built from GST Figure 1 '
                  'before either live test can be run.'),
    }
    with open(out_path, 'w') as fh:
        json.dump(result, fh, indent=1, sort_keys=True)
    for r in rows:
        print(json.dumps(r))
    print('controls_pass =', result['controls_pass'])


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1
         else 'results/eisermann_ribbon_link_gate.json')
