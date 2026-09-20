# Small fibered difference audit — 20 September 2026

Question: find a precisely identified smooth knot that bounds a smooth disk in standard B4 but admits no ribbon disk. No such disk or counterexample was found. These are computational deductions with an explicit mathematical bridge, not independently refereed results.

## Recorded results

For D = K # (-J), where minus is the concordance inverse:

| K | J | double-cover H1 of each | nonzero character pairs modulo independent signs | result |
|---|---|---|---|---|
| K7a2 | K10n4 | Z/19 | 81 | all have non-norm witnesses |
| K8a5 | K12n13 | Z/29 | 196 | all have non-norm witnesses |
| K11n91 | K13n16 | Z/31 | 225 | all have non-norm witnesses |
| K9n4 | K14n282 | Z/7 | 9 | three exact polynomial matches remain |

Names use the SnapPy/Spherogram census convention; saved PD codes, presentations and cocycles remove naming ambiguity. Selection rebuilt bins from the full 16,970-row earlier census, using genus two, identical Alexander polynomial, matching tau/nu/epsilon, and prime determinant. The saved census `pairs` list contains only the first 2,000 pairs and must not be treated as exhaustive. These four exhaust this selected binning, not all possible counterexamples.

## Nonsliceness deduction for the first three rows

The double branched cover of D has H1 = F_q^2 with the orthogonal sum of two nonsingular one-dimensional linking forms. A metabolizer has dimension one. Neither coordinate axis is isotropic. Thus every nonzero character annihilating a metabolizer has both coordinates nonzero. Testing every nonzero pair deliberately overcounts possible metabolizers and avoids needing their exact linking-form coordinates.

The recorded reduced twisted Alexander polynomials are monic integral quadratics F_A(t) = t^2 + A(zeta_q)t + 1. Coefficients are fixed by complex conjugation. Nonzero characters are scalar substitutions zeta_q -> zeta_q^a; the deck involution identifies signs. Connected-sum discriminants multiply modulo conjugate-reciprocal norms. Passing to the concordance inverse inverts the class, which has the same parity obstruction; the normalization factor (t-1)^2 is itself a norm up to Laurent unit.

The sliceness norm theorem requires a metabolizer on whose annihilating characters the relevant discriminants are norms. Consequently, a non-norm witness for every nonzero coordinate pair excludes every metabolizer. Subject to the recorded presentation-to-invariant computation and connected-sum normalization, the first three differences are not locally flat slice, hence are not smoothly slice.

Here is the finite arithmetic witness. Reduce at a prime ell congruent to -1 modulo q, so cyclotomic conjugation reduces to Frobenius on F_(ell^2). The symmetric coefficients A and B land in F_ell. If A differs from B and either A^2-4 or B^2-4 is a nonsquare, the corresponding quadratic splits into distinct roots r,r^-1 in F_(ell^2), with r^ell = r^-1. Its linear factors are fixed by conjugate reciprocity. They occur with odd multiplicity in F_A F_B: the other quadratic cannot share a root, since subtracting their equations gives (A-B)r = 0. A norm has even multiplicity at every such fixed factor. Therefore this product is not a norm.

Reduction is valid here because the characteristic-zero polynomial is monic, integral, and has constant term one. A monic factor has integral coefficients by integral closedness of the cyclotomic integer ring; its constant coefficient is a unit. Reduction preserves degrees and nonzero constant terms. A characteristic-zero norm factorization would therefore reduce to a norm factorization, up to an irrelevant constant.

The independent elementary checker uses only integer arithmetic: set S_0=2, S_1=w, S_n=w S_(n-1)-S_(n-2), and take w=zeta+zeta^-1 in F_ell with S_q(w)=2, w != 2. A symmetric cyclotomic coefficient is evaluated via these S_n. `ELEMENTARY_NORM_CERTIFICATE.json` records all 81 q=19 witnesses; first witnesses occur at ell=37 (69 pairs), 113 (9), 227 (2), 379 (1). For q=29 the primes through 811 exclude all 196 pairs; for q=31 the primes through 991 exclude all 225 pairs. Exact inputs and per-pair witnesses are in the accompanying JSON files.

## Controls and limitations

The q=19 audit matched 72 exact/modular evaluations and checked conjugation invariance. An initial assertion that independently simplified presentations would agree failed; `INITIAL_AUDIT_FAILURE.json` preserves that failure. Full Galois-orbit comparison repaired the comparison, and all-pair tests then used a consistent exact basis. No direct equality of raw generator markings is claimed. The elementary checker is independent of FLINT polynomial factorization, but still depends on the same exact Fox inputs. Earlier implementation controls include known ribbon examples and a published non-norm polynomial. Outside review of the topology-to-torsion conventions remains valuable.

## Sources and attribution

- Nathan Dunfield and Sherry Gong, *Ribbon concordances and slice obstructions: experiments and examples*, arXiv:2512.21825 (2025), https://arxiv.org/pdf/2512.21825, Theorem 3.3: metabolizer/norm sliceness obstruction for odd-prime characters; section 3.11 discusses the coefficient-field issue. Consulted 20 September 2026.
- Matthew Hedden, Paul Kirk and Charles Livingston, *Non-slice linear combinations of algebraic knots*, JEMS 14 (2012), 1181–1208, DOI 10.4171/JEMS/330, https://arxiv.org/html/0909.1247: Casson–Gordon discriminants, orientation behavior and connected-sum additivity (sections 3–5). Consulted 20 September 2026.

The census exclusions and elementary certificates above are this investigation's deductions, not claims attributed to these papers.
