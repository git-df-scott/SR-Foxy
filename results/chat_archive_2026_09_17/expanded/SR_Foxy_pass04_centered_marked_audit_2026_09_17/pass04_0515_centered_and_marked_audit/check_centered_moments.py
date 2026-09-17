#!/usr/bin/env python3
"""Exact regressions for the repaired reflection-centered kernel identity.

No knot library, floating point, or old transfer-checker implementation is used.
The all-degree proof is in MOMENT_CORRECTION.md; these are finite controls.
"""
from __future__ import annotations
from fractions import Fraction
from math import comb, factorial
from pathlib import Path
import argparse
import hashlib
import json
import time


def binomial(n: int, k: int) -> int:
    return comb(n, k) if 0 <= k <= n else 0


def multiplicity(n: int, r: int) -> int:
    if r < 0 or r > n or (n-r) % 2:
        return 0
    k=(n-r)//2
    return binomial(n, k)-binomial(n, k-1)


def functional(n: int, f) -> Fraction:
    epsilon=n % 2
    return sum((Fraction(multiplicity(n, r)*(-1)**((r-epsilon)//2))*f(r)
                for r in range(epsilon, n+1, 2)), Fraction(0))


def polynomial_binomial(x: Fraction, s: int) -> Fraction:
    value=Fraction(1)
    for k in range(s):
        value *= (x-k)/(k+1)
    return value


def basis_value(r: int, s: int) -> Fraction:
    return polynomial_binomial(Fraction(r+s, 2), s)


def chebyshev_polynomials(n_max: int) -> list[list[int]]:
    values=[[1]]
    if n_max:
        values.append([0,1])
    for n in range(2,n_max+1):
        p=[0]+values[-1]
        old=values[-2]
        for j,c in enumerate(old):
            p[j]-=c
        values.append(p)
    return values


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-degree',type=int,default=48)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if not 2 <= args.max_degree <= 128:
        parser.error('max-degree must be between 2 and 128')
    if args.output.exists():
        parser.error('refusing to overwrite an existing output')
    counts={}
    def require(condition: bool, family: str) -> None:
        if not condition:
            raise RuntimeError('FAIL '+family)
        counts[family]=counts.get(family,0)+1
    t0=time.monotonic()
    cheb=chebyshev_polynomials(args.max_degree)
    for n in range(args.max_degree+1):
        epsilon=n%2
        sign=(-1)**((n-epsilon)//2)
        for s in range(epsilon,n+1,2):
            value=functional(n,lambda r: Fraction((r+1)**s))
            expected=Fraction(sign*2**n*factorial(n) if s==n else 0)
            require(value==expected,'centered_moment')
            basis=functional(n,lambda r: basis_value(r,s))
            require(basis==(sign if s==n else 0),'basis_functional')
        # Reconstruct z^n from the recurrence, rather than from the closed formula.
        reconstructed=[0]*(n+1)
        for r in range(epsilon,n+1,2):
            for s,c in enumerate(cheb[r]):
                reconstructed[s]+=multiplicity(n,r)*c
                if s%2==r%2:
                    require(c==(-1)**((r-s)//2)*basis_value(r,s),
                            'closed_coefficients_vs_recurrence')
        require(reconstructed==[0]*n+[1],'chebyshev_inverse_identity')
    # Reflection and zero-range properties on points outside the support too.
    for s in range(args.max_degree+1):
        for r in (s%2,s,s+2,2*args.max_degree+s%2):
            require(basis_value(-r-2,s)==(-1)**s*basis_value(r,s),
                    'reflection_identity')
        for r in range(s%2,s,2):
            require(basis_value(r,s)==0,'out_of_range_zero')
    # Explicitly ensure the original incorrect printed formula is rejected.
    wrong=[]
    for n in (1,2,3,4,5,6):
        value=functional(n,lambda r:Fraction(r**n))
        claimed=Fraction((-1)**((n-n%2)//2)*2**n*factorial(n))
        require(value!=claimed,'reject_uncentered_identity')
        wrong.append({'n':n,'actual_L_r_power':int(value),
                      'incorrect_claim':int(claimed),
                      'correct_L_centered_power':int(functional(n,lambda r:Fraction((r+1)**n)))})
    result={'status':'CENTERED_IDENTITY_CONTROLS_PASS_ORIGINAL_FORMULA_REJECTED',
            'counterexample_found':False,'max_degree':args.max_degree,
            'checks_by_family':counts,'checks_passed':sum(counts.values()),
            'explicit_original_failures':wrong,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'seconds':time.monotonic()-t0,
            'scope':'Finite exact arithmetic controls. The all-n proof is separate. No knots, slice disks, or diagrams are enumerated.'}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':
    main()
