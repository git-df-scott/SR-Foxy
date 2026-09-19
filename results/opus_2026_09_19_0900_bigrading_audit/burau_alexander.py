#!/usr/bin/env python3
"""Alexander polynomial from the reduced Burau representation of a braid word.

Independent of the HFK calculator AND of spherogram's Seifert algorithm.
For a braid beta on n strands whose closure is the knot K,

    Delta_K(t) = det(I - Burau_red(beta)) * (1 - t) / (1 - t^n)    up to a unit.

Self-validating: run directly to check against tabulated Alexander polynomials.
A tool that fails its controls has decided nothing and must not be used.
"""
import sympy
from sympy import symbols, eye, zeros, Matrix, expand, simplify, Poly, cancel

t = symbols('t')


def normalise(coeffs):
    c = [int(x) for x in coeffs]
    while c and c[-1] == 0: c.pop()
    while c and c[0] == 0: c.pop(0)
    if c and c[0] < 0: c = [-x for x in c]
    return c


def burau_gen(n, i, inverse=False):
    """Reduced Burau matrix of sigma_i (1-indexed) on n strands: size (n-1)."""
    m = eye(n - 1)
    if not inverse:
        if i - 2 >= 0: m[i - 1, i - 2] = t
        m[i - 1, i - 1] = -t
        if i < n - 1: m[i - 1, i] = 1
    else:
        if i - 2 >= 0: m[i - 1, i - 2] = 1
        m[i - 1, i - 1] = -1 / t
        if i < n - 1: m[i - 1, i] = 1 / t
    return m


def alexander_from_braid(word, n):
    M = eye(n - 1)
    for g in word:
        M = M * burau_gen(n, abs(g), inverse=(g < 0))
    num = expand((eye(n - 1) - M).det() * (1 - t))
    den = expand(1 - t ** n)
    q = cancel(sympy.together(num / den))
    q = sympy.simplify(q)
    p = Poly(sympy.numer(sympy.cancel(q)), t)
    return normalise(p.all_coeffs())


CONTROLS = {'3_1': [1,-1,1], '4_1': [1,-3,1], '5_2': [2,-3,2], '6_1': [2,-5,2],
            '6_2': [1,-3,3,-3,1], '6_3': [1,-3,5,-3,1], '7_4': [4,-7,4],
            '8_8': [2,-6,9,-6,2], '9_46': [2,-5,2]}

if __name__ == '__main__':
    import snappy, sys
    ok = True
    for name, want in CONTROLS.items():
        L = snappy.Link(name)
        w = L.braid_word()
        n = max(abs(g) for g in w) + 1
        try:
            got = alexander_from_braid(w, n)
        except Exception as e:
            got = 'ERR ' + type(e).__name__
        good = (got == want) or (got == want[::-1])
        ok = ok and good
        print(('PASS ' if good else 'FAIL ') + f'{name}: got {got} want {want}')
    print('\ncontrols_pass =', ok)
    sys.exit(0 if ok else 1)
