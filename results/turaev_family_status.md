# Turaev's Theorem I family: an explicit, live, never-tested counterexample family
2026-09-11

## What it is

Turaev (Math. USSR-Sb. 44(3) (1983) 335-361) constructs a genus-3 Seifert surface
A(p,q,r,s). Its Seifert matrix, read from page 341 of the English translation, is

        [ 0  1   0   1  0  0 ]
        [ 0  0   p   0  0  0 ]
    X = [ 0  p   0   q  0  1 ]
        [ 1  0  q-1  0  p  0 ]
        [ 0  0   0   p  0  0 ]
        [ 0  0   1   0 -1  0 ]

The parameters r and s do **not** appear in X. They are Milnor-triple (l_2) data,
installed by Milnor's ribbon-linking move applied to the band triples (1,3,5) and
(2,4,6). The move leaves X unchanged, so the (r,s) members all share one Seifert
matrix and are distinguished only by the nil-form.

## Independently verified here (sympy, from the matrix alone)

| claim | result |
|---|---|
| alt(X) = X^T - X is symplectic | determinant **1**, so X is genuinely realizable by a genus-3 surface |
| Alexander polynomial | det(X - tX^T) = t^3 rho(t) rho(1/t), rho(t) = p t^3 - (p+q) t^2 - (p-q+1) t + p |
| Fox-Milnor | **holds identically**, for every (p,q) |
| metabolizers | X vanishes identically on span(x1,x3,x5) **and** on span(x2,x4,x6) |
| determinant | abs(Delta(-1)) = (2q-1)^2, **always a square** |

So the form is hyperbolic over Z and the family is algebraically slice, for every
parameter value, for a structural reason rather than by coincidence.

## The classical battery cannot kill any member

Over a 29-row grid (p in {1,2,3,5,7}, q in 0..5, the excluded case p=q=2):
Fox-Milnor holds, the determinant is a square, Arf is 0, and **all Levine-Tristram
signatures vanish at every prime-power root of unity tested up to order 32**. Every
member passes every classical necessary condition for sliceness.

## Why this is a counterexample family

- Theorem I: for **r != 0 and s != 0** the nil-form F_2(l_1, l_2) is **not
  metabolic**.
- Theorem H(ii): if K is ribbon then F_2 is metabolic. Section 7.4's proof uses only
  that a ribbon knot bounds a disk with pi_1(S^3 - K) -> pi_1(B^4 - D) surjective,
  and Lemma 7.2's sole hypothesis is that this map is an epimorphism. So H(ii) is
  literally an obstruction to **homotopy-ribbonness**.
- Theorem J: Theorem H yields **no** new obstruction to sliceness, so it does not
  rule these knots out from being slice.

Therefore every member with r, s both nonzero is **algebraically slice, provably not
homotopy-ribbon, and unobstructed by every classical sliceness test**. If any one of
them is smoothly slice, it is a counterexample to the Slice-Ribbon Conjecture, and a
stronger one than required: it separates slice from homotopy-ribbon, not merely from
ribbon.

Smallest candidates: (p,q,r,s) = (1,1,1,1), (1,3,1,1), (2,1,1,1).

## A subfamily immune to the usual killer

For **q = 1** the determinant is (2*1-1)^2 = 1, so H_1 of the double branched cover
is trivial and that cover is a homology sphere. The standard Casson-Gordon test,
which runs over characters on H_1(Sigma_2), is vacuous there. Whatever kills the
q = 1 members must come from elsewhere.

## The blocker, stated precisely

**No PD code exists.** Turaev never draws A(p,q,r,s); section 1.5 is a realization
theorem, and the surface is defined on page 342 by appeal to it. Without a diagram
we cannot run Casson-Gordon/HKL, tau, s, or any Floer invariant, which is exactly
what the family now needs.

Realizing it honestly requires two steps:
1. draw the genus-3 surface as a disk with six bands realizing X (standard: band
   linkings and self-twists are read off the matrix), giving the (r,s) = (0,0) knot;
2. implement Milnor's ribbon-linking move on that diagram for the triples (1,3,5)
   and (2,4,6) to install r and s.

Step 1 alone gives the (0,0) member, which Theorem I does **not** obstruct, so it
cannot substitute: the Alexander polynomial is identical for all (r,s), so no
polynomial check can certify that a diagram has r, s nonzero. The agent that
recovered the matrix declined to guess a diagram for exactly this reason, which was
the right call.

## Honest assessment

This is the sharpest target the campaign has produced: explicit, small, genus 3,
with a stronger certificate than any other lane, and untested for forty years in an
essentially uncited paper. It remains most likely that these knots are simply not
slice, because most algebraically slice knots are not, and Casson-Gordon is the
classical tool that kills exactly this kind of family. The point is that nobody has
looked, and the test is now well defined.
