# What the missing mixed arrows can and cannot change

**Status: exact algebra on the calculator's stored complexes; no slice disk and no novelty claim.** The calculation gives a reason to stop spending effort on ordinary knot Floer local equivalence for this pair. It does not dispose of involutive structures, Khovanov refinements, or geometric concordance.

## Inputs and finite question

Use the actual K0 and K1 PDs from the September 12 audit, and the complete generator and differential tables saved in `results/chain_map_filter_wider.json`. The HFK Calculator returns the simplified complex over R = F2[U,V]/(UV), not the full polynomial-ring complex. The installed Spherogram 2.4.1 documentation specifies generator gradings (Alexander A, Maslov M), one generator per hat-HFK rank, and the horizontal/vertical differential. [Szabó, Culler, Dunfield and Goerner, HFK Calculator wrapper, version 1.2.2](https://github.com/3-manifolds/knot_floer_homology).

Let S = F2[U,V], with U of degree (-1,-2), V of degree (1,0), and d of degree (0,-1), in (A,M) order. A term U^a V^b e_j in d(e_i) must satisfy

    a = (M_j - M_i + 1)/2,    b = A_i - A_j + a.

Both powers must be nonnegative integers. Thus each ordered generator pair permits at most one monomial. All terms surviving modulo UV are fixed by the input; only terms with a,b > 0 are unknown.

K0 has all generators in delta = M-A = 0, so it permits no mixed differential terms. Its fixed differential already squares to zero over S. K1 has generators in delta = 0 or -2. There are 18 possible mixed terms, all directed from the lower delta level to the upper one. No two can compose, so d^2=0 is linear in their coefficients: 10 independent equations, eight free bits, 256 completions.

`audit_mixed_lifts.py` enumerates these completions and saves maps S -> C -> S. The separate standard-library-only verifier checks all 262,144 assignments of the 18 coefficients, reconstructs the equations, verifies completeness of the saved 256 cases, and checks every map's grading and polynomial identities. It uses neither the SAT solver nor a topology library. All 256 K1 completions and the unique K0 completion admit an S-chain retraction onto the unknot complex in degree (0,0).

## A uniform splitting, rather than 256 unrelated solver outputs

Use the K1 generator labels in the saved table. Let alpha be the sum in F2 of the coefficients of U^2 V e1 and U^2 V e10 in d(e0). Let beta be the sum of the coefficients of U V^2 e1 and U V^2 e10 in d(e7). Define

    i(1) = e1,
    p(e1) = p(e10) = 1,
    p(e2) = alpha U^2,
    p(e8) = beta V^2,
    p(ej) = 0 for all other j.

The displayed generator grades make both maps homogeneous. The differential of e1 is zero. Applying p to d(e0) and d(e7) gives zero by the definitions of alpha and beta. The coefficient equations in d^2(e2)=0 force the corresponding sum for d(e4) to equal alpha; those in d^2(e8)=0 force the sum for d(e12) to equal beta. Thus p also kills these two differentials. Inspection of the remaining fixed and allowed mixed arrows shows their targets are killed by p, or occur in the cancelling combination e1+e10. Consequently di=0, pd=0, and pi=1.

For explicit coverage of that last inspection: possible mixed arrows from e2 land only at e9; from e8 only at e6; from e3 and e11 only at e6 or e9. The projection kills both e6 and e9. The only remaining mixed-arrow sources are e0, e4, e7 and e12, already treated. There are no mixed arrows from the delta-zero block. This rules out the extra projected terms raised in the external model critique.

This formula is checked independently on every completion in `results/mixed_lift_uniform_check.json`. The unknot summand is therefore an explicit algebraic splitting, not merely a solver's SAT label.

## Why a minimal quotient basis can be lifted

Here is the algebraic argument needed to connect the finite enumeration to an actual full complex. Its input assumption is that the calculator's reduced free R-complex is the correct homogeneous chain-homotopy type of the knot's quotient complex.

Start with a finite free homogeneous S-complex for the knot. Cancel coefficient-1 differential arrows until its reduction modulo (U,V) has zero differential. Each cancellation removes two generators and uses a unit pivot; the procedure is finite and preserves the homogeneous chain-homotopy type. A homogeneous coefficient with a nonzero constant term cannot also contain positive-degree monomials, so such a pivot is exactly 1. The remaining generator gradings and counts are those of hat HFK.

Its quotient and the calculator's reduced R-model are homogeneous chain-homotopy equivalent. Reduce a homotopy equivalence modulo (U,V). Since both reduced differentials vanish, the resulting map is an isomorphism of graded vector spaces. On homogeneous bases ordered by delta, a degree-zero matrix is block triangular: a positive-degree polynomial entry can only join strictly different delta levels, because both U and V lower delta by one. Its diagonal blocks are constant invertible matrices. The strictly triangular part is nilpotent, so the original map has a finite polynomial inverse. It is a chain isomorphism, not only a homotopy equivalence.

Lift its entries from R to S by using the same constant and pure monomials. The triangular argument still gives an inverse over S. Conjugate the true full differential by this lifted change of basis. Its quotient is now exactly the calculator's stored differential, on the same homogeneous generators. Its remaining entries are among the mixed monomials enumerated above. This establishes the finite reduction under the stated software/input assumption.

## Interpretation and its boundary

For an actual knot complex, localization at U and V has one free homology tower. The degree-zero inclusion and projection above split off the unknot tower and hence give local equivalence with the unknot. The same holds for K0. Composing the respective inclusions and projections gives ordinary local-equivalence maps between the two full complexes. This is the precise sense in which restoring the missing mixed arrows does not rescue an ordinary local-equivalence obstruction here.

This says nothing about a geometric map realizing the algebraic maps. In particular, K0 has determinant 13 and is not slice, despite its unknot Floer summand. The missing slice disk for K0 # (-K1) remains missing. The retractions also do not preserve any uncomputed involution, so no conclusion about involutive Floer refinements follows.

The distinct experiment on the 60 common-successor targets asks for chain maps and homotopy retractions over R. Its necessary direction comes from Ian Zemke, *Knot Floer homology obstructs ribbon concordance*, arXiv:1902.04050 (2019), Section 4, equation (14), which gives the reverse-concordance composition homotopic to the identity on the two-variable minus complex. Tensoring that identity with R preserves it. All 60 targets passed; none became a geometric concordance certificate. [Primary source](https://arxiv.org/html/1902.04050).

## Most valuable falsification checks

Independently recompute the quotient complex of the actual K1 diagram, preferably in a separate implementation; a wrong calculator input or grading convention would undermine the knot-theoretic application. Keep the exact algebra above separate from that software dependency. For the counterexample campaign, prioritize a geometric concordance and Khovanov/odd refinements rather than repeating ordinary local-equivalence tests on this pair.

Two Opus critiques are preserved as advisory material. The second agreed with the lifting lemma but correctly stressed the shared input dependency. Its proposed determinant check applies to K1 individually; our counterexample target is K0 # (-K1), whose determinant is 169. The individual determinant 13 was already independently checked. An Alexander-polynomial match checks an alternating sum of ranks, not the entire grading table. We also do not adopt its blanket phrasing that all V_i vanish: the precise assertion here is agreement of the ordinary local-equivalence class with the unknot. Full-ring negative controls for the trefoil and T(3,4) are recorded separately.
