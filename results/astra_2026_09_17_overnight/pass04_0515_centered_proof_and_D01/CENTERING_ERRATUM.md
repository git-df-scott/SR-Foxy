# A repairable centering error in the proposed transfer proof

17 September 2026 UTC. **NO COUNTEREXAMPLE.** The original proposed proof is preserved. This note corrects one false displayed identity; it does not claim a new slice disk, a published theorem, or external referee verification.

## The error is explicit

In section 3, equation (2), of the original `PROPOSED_TRANSFER_THEOREM.md`, define

```
epsilon = n mod 2
mu(n,r) = binom(n,(n-r)/2) - binom(n,(n-r)/2-1)
L_n(f) = sum_{0<=r<=n, r=epsilon mod 2}
           mu(n,r) (-1)^((r-epsilon)/2) f(r).
```

The displayed assertion

```
L_n(r^n) = (-1)^((n-epsilon)/2) 2^n n!
```

is FALSE. Its first three left sides are 1, -4, -25, whereas the proposed right sides are 2, -8, -48. Finite tests of the connected-sum kernel did not catch this separate error in the written proof.

## Correct identity and all-degree proof

The correct statement is

```
L_n((r+1)^n) = (-1)^((n-epsilon)/2) 2^n n!.
```

Set u=r+1. The polynomial

```
P_s(r) = binom((r+s)/2,s)
```

has parity s under r -> -r-2, equivalently ordinary parity s in u. Its leading coefficient in u is 1/(2^s s!). For fixed parity, these polynomials are a triangular basis of the corresponding centered polynomial space.

The exact Chebyshev decomposition `z^n = sum_r mu(n,r) S_r(z)` and the coefficient formula `[z^s]S_r(z)=(-1)^((r-s)/2)P_s(r)` imply

```
L_n(P_s) = 0                  for s<n with the same parity,
L_n(P_n) = (-1)^((n-epsilon)/2).
```

Consequently L_n annihilates every polynomial in u with the appropriate parity and degree below n. Applying it to the highest term of P_n proves the corrected identity. It does not in general annihilate the inappropriate reflection-parity terms introduced by expanding r^n=(u-1)^n. That is why the original displayed identity fails.

## Effect on the rest of the proof

The lower-valuation kernel argument already used reflection parity about r=-1; its reasoning does not require the false identity. In the leading-law extraction, use the centered variable u throughout. The top-degree reciprocal series are `sec(ut/2)` and `(ut/2)/sin(ut/2)`. The corrected moment identity supplies exactly the factor needed for the stated leading laws. Their formulas do NOT change:

```
e2(K#J) = e2(K) + e2(J) - 1

e3(K#J) = e3(K)d(J) + d(K)e3(J) - d(K)d(J).
```

The subsequent odd-denominator argument, ribbon-stabilization induction, and characteristic-zero Vandermonde argument can therefore be retained with this repair. The corrected full draft is `CORRECTED_TRANSFER_THEOREM.md`. Its claimed scope remains only the two Eisermann necessities on ribbon-pattern satellites of smooth slice companions, not all slice links or every quantum invariant. This pass found no additional gap in those arguments; it is not an external mathematical review or formal verification.

## Independent finite audit

`audit_centered_kernel.py` does not import the old checker. It clears the full Chebyshev denominator product using exact integer polynomials and checks the resulting orders and leading coefficients. This differs from the old reciprocal-series kernel calculation.

The completed degree-20 run passed 2792 checks: 20 centered leading moments, 100 lower centered moments, 890 cleared-denominator order tests, 890 leading-coefficient comparisons, 890 odd-denominator tests, and two deliberate rejections of the uncentered identity. These are finite algebraic controls, not a proof of all degrees.

The generic colored identities were also checked against new direct diagram evaluations of D01 through its three-parallel, including the reflected K1 jet. Their cleared residuals vanish modulo `(x^2+1)^5`. A deliberate leading-coefficient mutation is rejected. This is a distinct validation route for the algebra, while sharing the same previously audited diagram cabler and bracket evaluator.
