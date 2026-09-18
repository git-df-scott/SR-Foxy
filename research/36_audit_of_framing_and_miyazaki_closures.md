# Two claimed lane closures do not follow

18 September 2026. **CE: NO.** This audits the three commits that reached
origin/main during this session: 1110c67, e9616a6, aa2df2c. They were
fast-forwarded and preserved. Their historical raw RESULTS.json files remain
unchanged. The issue is mathematical scope, not whether their arithmetic ran.

## 1. A concrete counterexample to the framing-to-polynomial inference

The new framing-dichotomy note claims that zero linking forces every mixed
band design to have the same non-target polynomial. The repository already
contains a counterexample to that implication: **the 0110 band choice** in
`results/astra_2026_09_18_local_band_no_go/README.md`.

It uses precisely the same two paths, endpoints, and zero internal twists,
but changes their four over/under bits to 0110. Its auxiliary link is the
unlink by the archived certificate, its linking matrix is zero, and at surgery
parameter r=1 its Alexander polynomial is **d^2**, the target polynomial.

We independently reran the Fox order for this exact diagram:
`results/night_2026_09_18/repair_0110_response.jsonl`.
The order is

    t^8-6t^7+19t^6-36t^5+45t^4-36t^3+19t^2-6t+1.

The rational longitude response is even more informative:

    0000: B = [[0,q/d],[-q/d,0]],
    0110: B = [[0,0],[0,0]],

where d=t^4-3t^3+5t^2-3t+1 and q=t(t^2-1).
**Same ordinary linking, different equivariant linking.** Ordinary linking
is the t=1 specialization; both matrices specialize to zero. It cannot
determine the entire t-dependent matrix or its surgery determinant.

This refutes the purported universal polynomial argument even if Proposition L's
linking-zero conclusion is granted. It does not require settling Proposition L
for every possible pair of sequential bands. Such a proof must also track
orientations and justify both band-sum homologies in the required complements.

The 0110 repair is **not** a counterexample to slice-ribbon and is not identified
with D01. Its axis traces fail every source-centralizer conjugation covered by
the earlier local-band audit. That earlier conclusion is scoped to its explicit
family and survives. What fails is the extrapolation to every mixed-band design.
Different framed surgery descriptions can also describe the same boundary pair;
a mismatch of coefficients is not itself a knot-identification obstruction.

## 2. The quartic irreducibility gap can be filled exactly

The new Delta_r note verified irreducibility only for |r|<=6 but used it in an
all-integer assertion. In fact there is a short proof for all integers, so no
search expansion is needed. Set

    f_r=t^4+(r-3)t^3+5t^2+(-r-3)t+1.

It is monic with constant 1. Any rational linear factor gives an integer root
+/-1, excluded by f_r(1)=1 and f_r(-1)=13. A remaining factorization over Q
would, by Gauss's lemma, be into monic integral quadratics. Their constant
terms must both be +1 or both be -1.

- Constants +1: `(t^2+a t+1)(t^2+b t+1)` has equal t^3 and t coefficients.
  Comparing forces r=0, then a+b=-3 and ab=3. The discriminant -3 excludes
  integer a,b.
- Constants -1: `(t^2+a t-1)(t^2+b t-1)` has opposite t^3 and t coefficients.
  Their sum is zero, but f_r's corresponding coefficient sum is -6.

Thus f_r is irreducible over Q **for every integer r**. For r!=0 its reciprocal
is f_-r, a different monic irreducible factor. Consequently the only symmetric
divisors of f_r f_-r, up to units, are 1 and the whole product. In particular
any fibered knot with that polynomial has at most one nontrivial prime summand.
This is a polynomial argument; it does not establish fiberedness of a new knot.

## 3. Miyazaki alternative 1 is still available in principle

The norm-free alternative fails on the single nontrivial prime summand, since
its polynomial is the nonunit norm f_r f_-r. That is a valid exclusion of
**alternative 2**.

It does **not** exclude the separate minimality alternative. A proof that a
specified nontrivial prime fibered boundary knot is minimal in Miyazaki's
required homotopy-ribbon order would enable that alternative. The theorem
would then obstruct a homotopy-ribbon disk. Combined with an independently
constructed smooth slice disk, that would be precisely a counterexample.

The sentence "if its disk is not homotopy-ribbon, the counterexample is already
proved and needs no Miyazaki certificate" is circular: using Miyazaki could be
how the non-homotopy-ribbon property gets proved. Ordinary smooth sliceness does
not supply U below the knot in the homotopy-ribbon order; that requires the
additional disk property under investigation.

**Correct conclusion:** the polynomial rules out the norm-free route and the
specific two-symmetric-summand route. No minimality proof is supplied for the
new boundary, but minimality has not been proved impossible. This audit does
not assert that it holds. The blanket Proposition N is unsupported.

## 4. Corrections to PLAN_CE_2026_09_18.md

The plan remains a historical proposal; the following claims are not binding
mathematical exclusions:

1. Two distinct concordant minimal fibered knots are a **sufficient route** to
   a counterexample, not a proved characterization of every counterexample.
   Likewise, a vanishing specified four-term cable relation would be sufficient;
   a hypothetical counterexample need not come from that family.
2. Every counterexample need not be composite or fibered. Those conditions
   describe one use of Miyazaki's norm-free alternative, not the conjecture.
3. Algebraic sliceness does not force tau=0. The displayed cabling computation
   can establish its own value 0; algebraic sliceness is not the reason. For
   a concrete control, the positive untwisted Whitehead double of the positive
   trefoil has Alexander polynomial 1 (hence is algebraically slice) and tau=1
   by Hedden's formula, with twisting 0<2 tau(trefoil)=2. Source: Matthew
   Hedden, *Knot Floer homology of Whitehead doubles*, Geometry & Topology 11
   (2007), 2277--2338, DOI 10.2140/gt.2007.11.2277,
   [primary paper](https://msp.org/gt/2007/11-4/gt-v11-n4-p08-p.pdf).
4. The plan misattributes arXiv:1806.06225: it is Davis--Park--Ray,
   *Linear independence of cables in the knot concordance group*, Trans. AMS
   374 (2021), 4449--4479, [primary record](https://arxiv.org/abs/1806.06225).
   Its theorem about a specified family does not force every proposed
   Hom--Park example to pass the same invariants. Identify the families and
   parameters before transferring such a vanishing statement. The claimed
   blanket prohibition is unproved here.
5. The involutive K0/K1 local-equivalence computation is already recorded in
   research/11 and reproduced in SESSION_2026-09-16 section 2, **conditional
   on its stored lifting/input assumptions**. It is not wholly uncomputed.
   Auditing those assumptions is distinct from starting over from HFK ranks.
6. The fixed trace annulus cannot be removed unchanged by the previously
   specified relative destabilization. That is not a theorem that no changed
   annulus or other construction can work.

This is a targeted logical audit, not an exhaustive independent verification
of every external result cited by the new plan. It does not supply a new
construction or recommend broad invariant/census reruns.

## Next useful action

Use the corrected gate order: a concrete physical design, actual collar map,
boundary polynomial and identity, embedded annulus/compression, standard B4,
and global nonribbonness. Neither ordinary linking nor failure of one
Miyazaki alternative closes all of those possibilities.
