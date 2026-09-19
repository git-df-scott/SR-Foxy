# Two explicit low-degree sliceness gates for D01

**No counterexample, and no sliceness obstruction for D01 was obtained.**
The calculations here test the nonribbon/slice-unknown candidate, not KDG's
already-established sliceness. A failure would reject D01 as a slice candidate;
it would not itself be a slice-ribbon counterexample.

## A standalone derivation, not dependent on the all-degree moment lemma

Write t=delta=-A^2-A^-2 and B_n for the unnormalized bracket of a zero-framed
n-parallel, with B_0=1 and B_1=t E_1. For full divisibility write B_n=t^n E_n
and e_n=E_n(alpha), alpha^4=-1. Then e_1 is the signed knot determinant.
All companions have zero blackboard writhe. The irreducible colors are
S_1(z)=z, S_2(z)=z^2-1, S_3(z)=z^3-2z.

The generic colored connected-sum rule, before specializing at the root, gives

```
B_2(A#B)=(B_2(A)-1)(B_2(B)-1)/(t^2-1)+1,
B_3(A#B)=(B_3(A)-2B_1(A))(B_3(B)-2B_1(B))/(t^3-2t)
          + 2 B_1(A)B_1(B)/t.
```

When B_n of both factors has full divisibility for n<=3, putting a_j=E_j(A)
and b_j=E_j(B) factors these identities as

```
B_2(A#B)=t^2 * (t^2 a_2 b_2-a_2-b_2+1)/(t^2-1),
B_3(A#B)=t^3 * (t^2 a_3 b_3-2(a_3 b_1+a_1 b_3-a_1 b_1))/(t^2-2).
```

The denominators are valuation units over Q at t=0. These are identities of
generic rational functions representing integral link brackets; Gauss's lemma
returns the asserted integral divisibilities. Root specialization gives

```
e_2(A#B)=e_2(A)+e_2(B)-1,
e_3(A#B)=e_3(A)d(B)+d(A)e_3(B)-d(A)d(B).
```

The factor 2 in the second identity is canceled in characteristic zero BEFORE
any reduction modulo 32. There is no division by 2 modulo 32.

For completeness these laws give sliceness necessities without relying on the
proposed all-degree theorem. For slice K, choose ribbon J with X=K#J ribbon
(the stable-ribbon fact recorded by Livingston). The two-parallel of any knot
has the needed divisibility: with opposite orientations it bounds a zero-framed
annulus with Seifert matrix [0], so its ordinary link determinant is zero;
Jones and Alexander agree at the determinant evaluation. This refers to the
ordinary determinant, not the reduced Jones determinant.

For n=3, in the unfactored identity the coefficient on B_3(K) is
`(t^2 E_3(J)-2 E_1(J))/(t^2-2)`, a valuation unit with root value d(J).
The other summand has valuation at least three. Because X and J are ribbon,
B_3(X) and B_3(J) have full divisibility; hence B_3(K) does too.

Put d=d(K), e=d(J). Both are odd squares, hence 1 modulo 8. Eisermann's ribbon
congruence on X and J, together with the displayed laws, implies

```
e_2(K)-d^2 = (d^2-1)(e^2-1)             modulo 32,
e_3(K)-d^3 = d(d^2-1)(e^2-1)            modulo 32.
```

Both right sides vanish. Thus the two tests used below really are necessary
for sliceness, subject to these explicit published dependencies and conventions.
This paragraph is a derivation, not a claim that an external paper states it
in these exact terms. The full all-degree proof is not needed here.

## Exact summand computations performed in this pass

Inputs are the K0 and K1 PD fields at pinned main
`7a74678daccd9f3148b25a22a3f84a82eb1d374b`; paths and source blob IDs are in
`inputs.json`. The complete source files were read via the authorized connector;
the JSON here transcribes only their PD fields. No full-source-byte hash is
claimed for the transcription.

| Input | Cable crossings after zero-writhe normalization | Reduced determinant | Status |
|---|---:|---:|---|
| K0, 1-parallel | 6 | 13 | Signed normalization control |
| K1, 1-parallel | 22 | 13 | Signed normalization control |
| K0, 2-parallel | 24 | -23 | Previously known control, reproduced |
| K1, 2-parallel | 88 | -23 | Computed here |
| K0, 3-parallel | 54 | -1067 | Computed here |
| K1, 3-parallel | 198 | -1067 | Computed here |
| D01, 2-parallel | 112 | -47 | Direct check against the summand formula |

Every entry has exact divisibility, a nonzero real root quotient, and thus
normalized nullity n-1. The largest new contraction took approximately
10.17 seconds and retained at most 170,993 states. Each job had a 2 GiB
address-space limit and a 15- or 30-second wall limit. No job in this pass
returned a timeout or an invalid invariant.

The directly computed three-parallel residue for K1 is

```
[0,-103407,0,-414695,0,-623643,0,-416829,0,-104474]
```

in Z[x]/((x^2+1)^5), x=A^2. The exact remainder on division by (x^2+1)^3
vanishes. Dividing by delta^3 and evaluating at x=i gives -1067. Raw PDs,
crossing orders, coefficient arrays, logs, input hashes and resource bounds
are saved in `direct/`.

These calculations reuse the prior portable PD cabler and C++ bracket engine;
they are not independent topology-library calculations. The diagram-to-paper
identification is still an upstream dependency. No fifth KDG parallel, s,
HKL, Floer, or broad band search was repeated.

## Apply to the concordance inverse, with signs retained

For the full-divisibility quotients of these parallel links, mirror inversion
q -> q^-1 preserves the reduced determinant: the normalized Jones polynomial
and its unlink factor have the same parity, so their ratio is unchanged at
i versus -i. Orientation reversal of the knot does not change these values.
Thus the inverse -K1 contributes the same real e_j as K1.

The signed determinant of D01 is 13*13=169. The connected-sum laws give

```
e_2(D01) = -23-23-1 = -47,
e_3(D01) = 13*(-1067)+13*(-1067)-169 = -27911.
```

The first was also computed directly on the stored D01 diagram. The second
is DERIVED, not a direct three-parallel calculation on that diagram.

```
-47    - 169^2 = -28608   = -894*32,
-27911 - 169^3 = -4854720 = -151710*32.
```

Both gates pass. Exact agreement of e_2 and e_3 for K0 and K1 is NOT evidence
of a concordance. It neither produces a slice disk nor excludes the candidate.
No assertion that these coefficients are determined by the Alexander polynomial
or that all knots must pass is made from this finite agreement.

`check_d01_gates.py` symbolically verifies the generic formulas, checks all
recorded exact result statuses, compares the direct D01 calculation, and
rejects a deliberately perturbed leading coefficient.
