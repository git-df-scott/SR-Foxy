# All parallel multiplicities pass the Jones ribbon gates

19 September 2026. **No Slice–Ribbon counterexample constructed.**

This is a derivation from established colored-Jones identities, not a claim of historical novelty. It proves that every zero-framed parallel multiplicity of every knot passes both Eisermann conditions. Ordinary zero-framed Bing doubles and the specified comb iterates pass as well. It does **not** close other ribbon-preserving patterns, all boundary links, or the GST link construction.

## Conventions

Set `q=x^2`, `delta=x+x^{-1}`, `[N]=(x^N-x^{-N})/(x-x^{-1})`. Let `V_m` be the irreducible representation of dimension m+1. The unreduced, zero-framed invariant has `J_U(V_m)=[m+1]`. For an n-component link the ordinary positive-unlink-factor normalization is `V_L=J_L/delta`, and

```
D(L) = (J_L/delta^n)|_{x=i}
```

when the quotient is regular. Switching to the negative unlink-factor convention changes numerator and denominator by the same component-dependent sign. The knot value `d(K)=J_K(V_1)/delta|_{x=i}` is the **signed Jones determinant**, not the absolute determinant. Their squares agree. Eisermann's ribbon conditions are Jones nullity n-1 and `D(L)=product d(K_j) (mod 32)`.

Write C_n(K) for n Seifert-framed parallel copies. Its unreduced invariant is `J_K(V_1^n)`. Every formula below assumes zero framing.

## 1. Two parallels: a short proof

Habiro's integral cyclotomic expansion, in the convention of Beliakova–Blanchet–Lê §1.4, is

```
J'_K(N) = sum_{k=0}^{N-1} C_k(q) F_{N,k}(q),
F_{N,k} = product_{j=1}^k (1-q^(N+j))(1-q^(-N+j)),
C_k in Z[q,q^-1], C_0=1.
```

Put `c_k=C_k(-1)`. At N=2, `d(K)=1+4c_1`. At N=3, exact cancellation gives

```
(F_{3,1}/delta^2)|_{q=-1}=8,
(F_{3,2}/delta^2)|_{q=-1}=32.
```

Since `V_1^2=V_2+V_0` and `[3]=delta^2-1`,

```
D(C_2(K)) = 1-8c_1-32c_2,
D(C_2(K))-d(K)^2 = -16c_1(c_1+1)-32c_2.
```

The last expression is divisible by 32. D is odd, hence nonzero; the nullity is exactly one. Neither sliceness nor ribbonness was used.

This replaces the seven-knot empirical conjecture in `research/28_eisermann_cannot_be_made_to_bite_on_knots.md` with a proof **for this construction**. It does not reinstate that note's withdrawn blanket claim about arbitrary functorial constructions.

## 2. All multiplicities

### Proposition

For every knot K and every integer n>=1,

```
null V(C_n(K))=n-1,
D(C_n(K))=d(K)^n (mod 32).
```

Thus increasing parallel multiplicity cannot rescue either Eisermann gate.

### Regularity and the universal kernels

Use Habiro's zero-framed Hopf pairing

```
<V_a,V_b>=[(a+1)(b+1)]
```

and define

```
S_k = product_{r=1}^k (V_2-(q^r+1+q^-r)),
epsilon_k(q)=(-1)^k q^(k(k+1)/2).
```

Normalized Hopf evaluation is multiplicative. It sends V_2 to `q^N+1+q^-N` when paired with V_(N-1), so

```
[N] F_{N,k} = epsilon_k <V_(N-1),S_k>.
```

Expand `S_k=sum_{j=0}^k a_(k,j)(q)V_(2j)`. The coefficients are integral Laurent polynomials by the tensor-product rule. By linearity, the coefficient of C_k in `J_K(V_1^n)/delta^n` is

```
H_(n,k)(q)=epsilon_k sum_j a_(k,j)(q)[2j+1]R_j(x)^n,
R_j(x)=(x^(2j+1)+x^(-2j-1))/(x+x^-1).
```

Each R_j is a Laurent polynomial. Thus every H is an integral Laurent polynomial, in particular regular at x=i. The exact colored expansion truncates at k=n: V_1^n contains only dimensions <=n+1, while F_(N,k)=0 for k>=N. Hence

```
D(C_n(K))=sum_{k=0}^n c_k h_(n,k),
h_(n,k)=H_(n,k)|_{x=i}.
```

### Congruence: a finite proof of the infinite assertion

At x=i, `[2j+1]=(-1)^j` and `R_j(i)=lambda_j=(-1)^j(2j+1)`. Thus h_(n,k) is an **integral linear combination of odd integer powers lambda_j^n**. Every odd integer has eighth power 1 modulo 32. Consequently h_(n,k) is eight-periodic in n modulo 32, for every k.

Also, exactly,

```
h_(n,0)=1,
h_(n,1)=1-(-3)^n,
h_(n,k)=0 for k>n.
```

For any n set r=n mod 8. If k>r, periodicity and truncation give h_(n,k)=0 modulo 32. It therefore suffices to check the 21 pairs `2<=k<=r<=7`. The entire residue table is:

| r | h_(r,0) | h_(r,1) | all h_(r,k), 2<=k<=7 |
|---|---:|---:|---:|
| 0 | 1 | 0 | 0 |
| 1 | 1 | 4 | 0 |
| 2 | 1 | 24 | 0 |
| 3 | 1 | 28 | 0 |
| 4 | 1 | 16 | 0 |
| 5 | 1 | 20 | 0 |
| 6 | 1 | 8 | 0 |
| 7 | 1 | 12 | 0 |

An integer fusion recursion reproduces the table. Independent direct rational-function expansion of the Habiro kernels checks all 42 entries for n=2,...,8. These finite checks establish the all-parameter statement because periodicity and exact truncation were proved first, not inferred from examples.

We obtain

```
D(C_n(K))=1+(1-(-3)^n)c_1 (mod 32).
```

For every integer c,

```
(1+4c)^n=1+4nc+8n(n-1)c^2 (mod 32),
1-(-3)^n=4n-8n(n-1) (mod 32).
```

Their difference is `8n(n-1)c(c+1)`, divisible by 32. Since `d(K)=1+4c_1`, the proposition follows. D is odd, so regularity yields exactly n-1 zeros of normalized V. QED.

## 3. Bing doubles and comb iterates

Suzuki's Theorem 3.2 gives

```
x_(1,1)^0=0,
x_(1,1)^1=-{4},
x_(1,1)^2=-{1}{2},
x_(i,j)^l=0 for i!=j,
```

where `{r}=x^r-x^-r`. Expanding `V_1={1}P'_1+delta` gives the exact identity

```
J_B(K)=delta^2-(x-x^-1)^2(J_K(V_2)-[3]).
```

With s=x-x^-1, this is `J_B=delta^2(1+s^2)-s^2 J_C2`. Therefore

```
D(B(K))=4D(C_2(K))-3=1-32c_1-128c_2=1 (mod 32).
```

The components are unknots; the required product is one. D is odd, and the identity gives nullity one. Both gates are automatic for ordinary zero-framed Bing doubles of every companion.

For the comb B_n formed by repeatedly Bing-doubling one leaf, the off-diagonal vanishing forces the intermediate reduced color to remain P'_1. A zero leaf forces all leaves to be zero; equivalently every proper leaf sublink is an unlink. Induction gives

```
J_Bn-delta^n=(-s{4})^(n-2)(J_B2-delta^2),
D(B_n(K))=1+(-8)^(n-2)(D(B_2(K))-1), n>=2.
```

This also has nullity n-1 and D=1 modulo 32. **No extension to arbitrary Bing trees is asserted here.**

## 4. Controls and limitations

Published cyclotomic coefficients give these exact controls:

| companion | D(C_2) | D(B) | D(B_3 comb) |
|---|---:|---:|---:|
| unknot | 1 | 1 | 1 |
| either trefoil | -23 | -95 | 769 |
| figure eight | 25 | 97 | -767 |

The parallel values reproduce stored repository data. The Bing values are formula-derived, not independently computed from a traced Bing PD. No new disk or link diagram is certified.

The integer checker has 990 arithmetic checks and 42 independent rational-kernel comparisons. These are reproducibility counts, not a measure of proximity to a counterexample. The all-parallel proof uses the established Hopf and cyclotomic identities; the checker does not independently formalize those theorems.

The source campaign snapshot was `7585c92dc33f014bbbeaccbb1b721be0b1c2a8e5`. This note is additive and does not overwrite concurrent Opus work or a shared handoff.

## Primary sources

- K. Habiro, *A unified Witten–Reshetikhin–Turaev invariant for integral homology spheres*, arXiv:math/0605314, §§6.2–6.3, Hopf pairing and equations (6.7)–(6.11): https://arxiv.org/html/math/0605314
- A. Beliakova, C. Blanchet, T. T. Q. Lê, *Unified quantum invariants and their refinements for homology 3-spheres with 2-torsion*, arXiv:0704.3669, §1.4 equation (5) and examples: https://arxiv.org/html/0704.3669
- S. Suzuki, *Bing doubling and the colored Jones polynomial*, arXiv:1305.0602, Theorem 3.2 and §6.1: https://arxiv.org/html/1305.0602
- M. Eisermann, *The Jones polynomial of ribbon links*, arXiv:0802.2287, Theorems 1–2 and §6.4: https://arxiv.org/html/0802.2287

The all-parallel proposition is derived from these sources here; it is not quoted as an explicit theorem of Eisermann.