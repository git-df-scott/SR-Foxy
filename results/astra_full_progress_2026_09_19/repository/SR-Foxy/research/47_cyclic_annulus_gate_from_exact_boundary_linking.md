# Exact zero boundary linking forces the reduced cyclic annulus invariant to vanish

18 September 2026. Chain-level derivation extending research/46, independently
audited at the chain and local-intersection level. This is a
statement about an actual immersed annulus in an actual slice-disk exterior;
it does not identify the saved algebraic q0 with a geometric inclusion.

## Statement

Let D be a smooth properly embedded disk in B4, W its exterior, and R its
boundary. Let a,b be disjoint exponent-zero curves in the knot exterior,
with chosen framings and compatible lifts. Suppose all four entries of their
**exact** rational equivariant linking matrix E vanish. This is equality in
Q(t), not merely equality of Blanchfield classes modulo Z[t,t^-1].

If A is any properly immersed oriented annulus in W between those curves,
with exponent-zero core, then its reduced cyclic self-intersection invariant
vanishes. Its full-group invariant need not vanish. Together with the
surjectivity and geometric hypotheses of research/46, this permits boundary
clasp modifications that cancel the reduced full-group primary invariant.

## 1. The needed homology vanishing is elementary

Mayer--Vietoris for B4 = W union nu(D), with overlap homotopy equivalent to
D2 x S1, gives H2(W;Q)=0. Choose a finite cellular chain complex for the
infinite cyclic cover, over Q[t,t^-1]. Its specialization at t=1 is the
ordinary rational cellular chain complex of W.

For each boundary matrix, rank over Q(t) is at least its rank at t=1: a minor
nonzero after specialization was already a nonzero Laurent polynomial.
Writing c2 for the number of 2-cells gives

    dim_Q(t) H2(W;Q(t))
      = c2 - rank_Q(t)(d2) - rank_Q(t)(d3)
      <= c2 - rank_Q(d2(1)) - rank_Q(d3(1))
      = dim_Q H2(W;Q) = 0.

Thus H2(W;Q(t))=0. No assertion about the higher nonabelian covers is being
made, and no good-group assumption is needed.

## 2. Boundary linking computes the annulus/push-off intersection

Since the core has exponent zero, A lifts as a compact annulus. Choose its
lift; its boundary is z = a - t^k b for some k, with signs adjusted to the
boundary orientation. Take a generic normal push-off A+ that agrees with the
specified boundary framings. Its boundary is z+ = a+ - t^k b+.

The infinite cyclic Alexander module of a knot exterior is torsion, so z
bounds a rational 2-chain C there. The same chain is valid in boundary W,
which is the zero surgery on R. Rational equivariant linking is computed
using this chain. By sesquilinearity and E=0,

    lk_e(z,z+) = 0.                                         (1)

Choose a collar sufficiently small that A+ consists there only of its product
boundary collar z+ x [0,epsilon]. Push C to depth epsilon/2 and add its vertical
boundary collar. Its intersections with A+ are precisely those computing
C intersect z+. Make its boundary collar agree with that of A, so their
difference is an absolute rational 2-cycle supported in the interior. Clear
Laurent denominators first if a finite integral-chain model is preferred.
By the
previous step it bounds a rational 3-chain. Intersection with the relative
2-cycle A+ is consequently zero, giving, up to the fixed global orientation
sign,

    lambda_e(A,A+) = lk_e(z,z+) = 0.                         (2)

Equivalently this is the usual bounding-chain proof of the
linking/intersection formula, performed over Q(t). It does not require A to
be embedded, C to be a surface, or an integral Alexander-module class to
vanish. Exact representatives of linking, however, are essential: reducing
modulo Laurent polynomials before (1) would lose precisely the information
used in the next step.

## 3. Read the nonzero deck exponents

For every double point p of A let epsilon_p be its sign and n_p the exponent
of its double-point loop. A normal push-off contributes the two branch
intersections at n_p and -n_p. Zeros of its normal section contribute only
at exponent zero. Therefore

    lambda_e(A,A+) = e(normal A) +
                    sum_p epsilon_p (t^(n_p) + t^(-n_p)).    (3)

For each m>0, the coefficient of t^m in (3) is exactly the coefficient of
the generator |m| in the reduced cyclic primary invariant. Equations (2)
and (3) force each of these integers to be zero. The exponent-zero terms
are discarded by the reduced invariant, so no normal-framing conclusion
is silently inferred from them. Changes of the annulus double-point loop
by powers of its core do not change n_p, because that core has exponent zero.

This proves the stated reduced cyclic vanishing. It does not imply that
individual full-group labels pair, or that suitable Whitney disks are clean.

## What it advances and what remains

Research/46 initially left the cyclic projection as a separate hypothesis.
For actual exponent-zero annuli with exact E=0 in a slice-disk exterior, the
argument above supplies it. Under that note's surjective geometric inclusion,
paired clasps can then remove the remaining reduced primary full-group sum
while preserving the listed boundary data.

The present saved algebraic certificate still lacks the marked geometric q0
identification and an explicit annulus movie. There is also no proof that
the boundary after these permitted modifications yields a nonribbon knot.
Even after primary cancellation, smooth Whitney-disk geometry is an additional
problem. Thus this is progress on the first obstruction, not a counterexample
or a general annulus embedding theorem.

The next concrete check is a marked movie with its full signed double-point
words, followed by an explicit paired-clasp insertion and inspection of the
Whitney disks. A numerical zero-surgery match cannot replace those data.
