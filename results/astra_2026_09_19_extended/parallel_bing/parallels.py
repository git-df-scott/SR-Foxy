#!/usr/bin/env python3
"""Independent direct Habiro kernels for zero-framed parallels, n=2,...,8.
Uses SymPy, not the integer Hopf recursion in hopf_parallels.py.
Run this before hopf_parallels.py to enable all 42 cross-checks.
"""
import json
import time
from functools import lru_cache
from pathlib import Path
import sympy as S

x = S.symbols('x')
q = x*x
d = x + x**-1


@lru_cache(None)
def F(N: int, k: int):
    if k >= N:
        return S.Integer(0)
    return S.prod((1-q**(1+N+j))*(1-q**(1-N+j)) for j in range(k))


@lru_cache(None)
def qdim(N: int):
    return sum(x**(N-1-2*j) for j in range(N))


def mult(n: int, j: int):
    return S.binomial(n, j) - (S.binomial(n, j-1) if j else 0)


def main() -> None:
    rows = {}
    for n in range(2, 9):
        start = time.monotonic()
        vals, factors = [], []
        for k in range(n+1):
            a = S.cancel(sum(mult(n,j)*qdim(n-2*j+1)*F(n-2*j+1,k)
                             for j in range(n//2+1))/d**n)
            _, den = S.fraction(a)
            # Check regularity before substituting; never silently discard a pole.
            if S.rem(S.Poly(den,x), S.Poly(x*x+1,x)).is_zero:
                raise ArithmeticError(f'Kernel H({n},{k}) has a pole at x=i: {a}')
            v = S.cancel(a.subs(x,S.I))
            if not v.is_Integer:
                raise ArithmeticError(f'Nonintegral specialized kernel H({n},{k}): {v}')
            vals.append(int(v))
            factors.append(None)
        print(n, vals, 'seconds', round(time.monotonic()-start,3), flush=True)
        rows[n] = {'evaluated_universal_kernels': vals, 'singular_kernels': factors}
    Path(__file__).with_name('PARALLEL_KERNELS.json').write_text(
        json.dumps(rows,indent=2)+'\n')


if __name__ == '__main__':
    main()
