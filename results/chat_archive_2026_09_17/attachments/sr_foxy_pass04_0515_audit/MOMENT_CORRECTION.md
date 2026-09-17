# Correct the all-degree proof's reflection-centered moment

**No counterexample. A false displayed identity was found and repaired.**
This is an audit of the locally supplied `PROPOSED_TRANSFER_THEOREM.md`, not a
claim that the proof had already received an independent mathematician's review.

## The actual error

Section 3, equation (2) of the original report claimed

```
L_n(r^n) = (-1)^((n-epsilon)/2) 2^n n!,  epsilon=n mod 2.
```

This is false already at n=1, and at n=2 one has

```
L_2(f)=f(0)-f(2),   L_2(r^2)=-4,   claimed value=-8.
```

The earlier 4,832 passing finite checks did not test this incorrectly printed
identity. Their success was not a certificate for every line of the proof.

## Correct statement, with an all-degree proof

Set y=r+1 and

```
P_s(r) = binom((r+s)/2,s),
mu_nr = binom(n,(n-r)/2)-binom(n,(n-r)/2-1),
L_n(f) = sum_(r=epsilon,epsilon+2,...,n) mu_nr (-1)^((r-epsilon)/2) f(r).
```

The binomial defining P_s is its polynomial extension over Q. It has degree s,
leading coefficient 1/(2^s s!), and reflection parity

```
P_s(-r-2) = (-1)^s P_s(r).
```

For a fixed parity epsilon, the polynomials P_s with s<=n and s=epsilon mod 2
form a basis of the degree-at-most-n polynomials f satisfying
`f(-r-2)=(-1)^epsilon f(r)`. Indeed, in coordinate y these are precisely the
even or odd polynomials, and the P_s have nonzero leading coefficients and
strictly increasing degrees.

The Chebyshev recurrence S_0=1, S_1=z, S_(r+1)=z S_r-S_(r-1) gives

```
[z^s] S_r(z) = (-1)^((r-s)/2) P_s(r),
z^n = sum_r mu_nr S_r(z).
```

For s>r of the same parity the displayed P_s(r) is zero. Comparing coefficients
of z^s yields

```
L_n(P_s) = 0                    when s<n,
L_n(P_n) = (-1)^((n-epsilon)/2).
```

Consequently, for EVERY polynomial f of this reflection parity and degree at
most n,

```
L_n(f) = (-1)^((n-epsilon)/2) 2^n n! * [y^n] f(y-1).
```

In particular the corrected moment identity is

```
L_n((r+1)^n) = (-1)^((n-epsilon)/2) 2^n n!,
L_n((r+1)^s) = 0 for s<n of the same parity as n.
```

The uncentered monomial r^n is generally NOT in this reflection-parity
subspace. It cannot be substituted into the formula.

## Effect on the proposed proof

The coefficient polynomials to which the original kernel argument actually
applies L_n do have the required reflection parity. The even case is a product
of reflection-even polynomials. In the odd case P_j P_k/P_1 is a polynomial of
odd reflection parity: each odd P_s is divisible by P_1=(r+1)/2. Multiplication
by the even reciprocal coefficients preserves that parity. The argument
therefore uses the corrected functional statement above, not the false raw
monomial statement.

For clarity the top-degree reciprocal-series descriptions should also be
written in the centered coordinate: `cos(yt/2)` and `sin(yt/2)/(yt/2)`, with
y=r+1. Extracting a polynomial's leading coefficient is unchanged by this
translation. Thus this repair does not alter the filtered-kernel conclusion,
the even/odd leading connected-sum laws, or their 2-integrality calculation.

I found no further fatal gap in the inspected algebra and source-normalization
steps. This is a same-assistant adversarial review, NOT outside peer review,
proof-assistant verification, or a literature-wide novelty determination. The
corrected all-degree statement should be cited as a research derivation with
this amendment; the original equation (2) must not be used.

## Executed checks

`check_centered_moments.py` is a new standard-library exact-rational checker;
it does not import the old transfer checker. Through degree 48 it passes
7,602 arithmetic checks, including 625 centered moment identities, coefficient
comparisons against a separately generated Chebyshev recurrence, reflection
identities, and six explicit rejections of the old formula. These are finite
arithmetic checks, not 7,602 knots or constructions. The proof above supplies
the all-degree conclusion.

```
python3 check_centered_moments.py --output NEW_MOMENT_RESULTS.json
```

Original input: the conversation attachment `PROPOSED_TRANSFER_THEOREM.md`,
archived with its hash in this package. The colored-skein source dependencies
are listed in `SOURCES.md`; the moment correction itself is proved here.
