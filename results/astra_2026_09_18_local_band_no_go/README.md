# Astra: local band repairs and an all-parameter target-compatibility obstruction

**No Slice–Ribbon counterexample.** This pass tests a concrete repair of the crossed-band construction. It identifies one repair with the desired Alexander polynomial, then proves that repair fails the axis-conjugacy gate for a substantially larger class of identifications.

Inputs were read from remote main at 100963acdbe68897e21a562ca289b3e94f653261. All changes here are additive. No branch was created, historical patch applied, or local research checkout used as an input.

## Exact question and scope

Keep the two archived band paths a40a423e and d0826c36, their endpoints, and zero internal twist. Vary their four over/under choices in order: first band's two bits, then second band's two bits. There are exactly sixteen choices.

For the saved candidate collar map q0, fix the upper factor and conjugate the lower factor by mu^n lambda^m, where mu is the seam meridian and lambda its preferred longitude, and n,m are arbitrary integers. The surgery parameter r is separate: fill the two axes with preferred slopes (1,r),(-1,r).

The intended target family has Delta_target=(t^4-3t^3+5t^2-3t+1)^2. A useful local repair needs both conjugate axis images and this polynomial. Neither condition by itself proves an embedded annulus, a slice disk, or nonribbonness.

## 1. Sixteen choices, eight exact unlink certificates

Every choice was reconstructed from the archived PD and checked by Fox calculus at r=1. All have zero pairwise linking.

The eight choices beginning with 0 have exactly the same two-axis sublink after deleting R, with the archived three-move Reidemeister-II unlink certificate. For choices beginning with 1, this checker found no RII certificate; their unlink status is UNKNOWN, not disproved.

Only 0110 and 1110 give Delta_target at r=1. Of these, 0110 has the unlink certificate. Its axis words are:
eta1=[4,-1,3,-4,11,14,-15,-11,1,-9],
eta2=[4,-1,-15,14,-13,17,3,-4].
All words use the prior certificate's one-based signed boundary-generator convention.

Thus a genuine algebraic repair exists at the polynomial level. It must still pass the disk-group gate.

## 2. Meridional AND longitudinal changes fail to rescue the repair

Use the exact degree-six field F and source representation from the previous Astra certificate:
R(z)=z^6+3z^5+5z^4+4z^3+2z^2+z+1, F=Q[z]/(R).
The previous independent checker certifies R irreducible and every source and boundary relation.

At the seam, mu=I+N, N^2=0. Direct traversal of the closed upper knot gives the preferred longitude word
[3,6,-5,2,3,-2,-3,-6,9,-2],
with total exponent zero, and
rho(lambda)=-(I+L(z)N),
L(z)=4z^5+12z^4+16z^3+8z^2+2.

Therefore conjugation by mu^n lambda^m has the same matrix action as I+sN with s=n+mL(z), for all integers n,m. This includes negative powers exactly.

The JavaScript BigInt implementation reconstructs every axis trace polynomial in s. Substituting s=n+mL and reducing modulo R yields six polynomial equations over Q. Their Groebner bases are:

| bits (first bit 0) | basis | possible trace equality |
|---|---|---|
| 0000 | n,m | n=m=0 only |
| 0011 | n,m | n=m=0 only |
| 0001,0010,0100,0101,0110,0111 | 1 | none |

Flipping the first bit leaves the axis words unchanged, as explicitly checked. Thus the same trace obstructions apply to the remaining eight choices. Trace inequality also obstructs conjugacy to the inverse in SL(2).

In particular, the polynomial repair 0110 fails for every peripheral change in this family, not just every meridian power. This result does not prove that every possible geometric collar parametrization is in this family.

## 3. Stronger obstruction for 0110: every centralizer conjugation

For 0110 the trace difference at a general parameter s in F is c(z)+a(z)s+b(z)s^2:
c=4-4z+8z^2+8z^3-4z^4-12z^5,
a=4z^3+10z^4+6z^5,
b=-2z^4-2z^5.

Its discriminant, reduced in F, is
D=-572-268z-804z^2-1816z^3-1652z^4-336z^5.
The field norm is exactly 199282855936, strictly between
446411^2=199282780921 and 446412^2=199283673744.
Thus D is not a square in F, since the norm of a square in F is a rational square. The quadratic has no root in F.

Every SL(2,F) matrix commuting with the nontrivial unipotent I+N has form +/- (I+sN); its scalar sign does not affect conjugation. Consequently no such centralizer conjugation of the lower factor makes these two axis traces equal. In particular, no conjugation by any source-group element commuting with the seam meridian can fix this repair.

The norm was checked both by a SymPy resultant and independently by JavaScript BigInt multiplication matrices and fraction-free determinant elimination. This argument needs no faithfulness of the representation.

## 4. Exact formula for every surgery parameter in the surviving two choices

For 0000 and 0011, the only peripheral identification surviving the trace gate is n=m=0. For both, the surgery Alexander polynomial for every integer r is

Delta_r=(t^4-3t^3+5t^2-3t+1)^2-r^2 t^2(t^2-1)^2.

This is not extrapolation from finitely many values. The original Fox matrix is reduced with 55 pivots that are units +/- t^k in Z[r,t,t^-1], leaving a 7 by 6 matrix. Its seven maximal minors are either zero or +/- t^k Delta_r, and five are nonzero unit multiples. These identities survive every integer specialization of r, because elimination never divides by a polynomial in r. The script regenerates and checks all minors.

Hence Delta_r differs from Delta_target for every nonzero integer r. Both are normalized with constant and leading coefficient 1, so multiplication by an Alexander-polynomial unit cannot hide the difference.

The new family nevertheless satisfies the Fox–Milnor necessary condition for every r: write f_r=t^4-3t^3+5t^2-3t+1+r(t^3-t); then Delta_r=f_r(t)t^4 f_r(t^-1). Its determinant is always 169. This is not a sliceness proof.

**Local conclusion:** among the eight explicitly unlinked zero-twist over/under choices on these fixed band paths, no nonzero surgery parameter and no peripheral change q_(n,m) can simultaneously pass the axis-trace gate and reproduce the intended target polynomial.

This is a target-compatibility obstruction for the specified local family. It does not exclude other paths, internal twists, other geometric identifications, or the possibility that a new boundary outside the old target family is slice and nonribbon.

## 5. Reproduction and next falsification step

Run with assertions enabled from this directory:

```sh
python3 check_local_bands.py
node check_traces.mjs
python3 check_peripheral.py
python3 check_discriminant.py
python3 check_all_surgeries.py
```

Python calculations used SymPy 1.14.0. The optional diagram producer uses SnapPy 3.3.2 and seed 1729. Its 20-second attempt for 0110 at r=1 timed out; no boundary-knot identification is claimed from the polynomial match. The exact Fox and group calculations completed.

The best next constructive directions are genuinely different band paths or a geometric slice certificate plus an independent nonribbon obstruction for the new Delta_r family. A local over/under repair or an extra peripheral twist cannot meet both old-target gates in this family.
