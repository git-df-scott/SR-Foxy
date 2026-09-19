# Why the fixed cable stabilizer cannot supply the second ribbon disk

18 September 2026. This is a deduction from a cited preprint theorem and the
existing stored-knot certificates, not a formally verified theorem or a
nonsliceness result. It supersedes the earlier unknown ribbon status of
D01#J for the particular stabilizer in research/48.

## Precise question and hypotheses

Set d=t^4-3t^3+5t^2-3t+1, R=K0#(-K0), and J=C_(2,1)(R).
Can D01#J be ribbon, where D01 has stored prime summand types K0,-K1?
The input certificates establish that K0,K1 are prime fibered, have
irreducible polynomial d, and are distinct even after mirroring. The precise
orientation of the stored K1 summand does not affect the exclusion: its
unoriented type and its mirror are both distinct from K0.

**Answer, under the cited theorem: no. In fact U is not <=h D01#J.**
Here <=h means strongly homotopy-ribbon concordance in a homotopy S3×I.
This does not exclude a smooth slice disk with a more complicated exterior.

## External theorem input

Ian Agol and Qiuyu Ren, *Ribbon concordance of fibered knots and compressions
of surface homeomorphisms*, arXiv:2603.10884v1, 11 March 2026, is a preprint,
checked 18 September 2026. [Theorems 1.7, 1.13 and §7.2](https://arxiv.org/html/2603.10884).

We use two assertions: fibered <=h concordances correspond to monodromy
compressions; a strongly homotopy-ribbon connected sum of prime fibered
knots admits predecessor collections assigned to each target factor, with
all predecessor factors globally paired with their reversed mirrors.
The §7.2 construction permits these predecessors to be chosen fibered:
they arise from compressed monodromies and fibered prime decomposition.
We do not infer this from an unrestricted assertion about arbitrary
predecessors in exotic cobordisms.

The definitions in §2 retain the vertical-boundary marking for knot
monodromies. That marking matters for the product case below. The proof in
§7.2, especially its local-compression case, was checked in addition to the
theorem statement. No newness claim is made for the following consequence.

## The compression-body calculation

Let fibered S<=h K have connected once-punctured fibers of genera h and g.
Its relative compression body C retracts to F_S with g-h circles attached.
Consequently

    dim H1(C;Q) = g+h,
    dim ker(H1(F_K;Q) -> H1(C;Q)) = g-h.

The outer map is surjective, the inner-fiber map is injective, and both
intertwine monodromies. Therefore the lower monodromy is an invariant
subquotient of the upper one; Delta_S divides Delta_K over Q[t,t^-1].

If Delta_K is irreducible of degree 2g>0, the upper monodromy has no proper
nonzero invariant rational subspace. But the displayed kernel has dimension
between 0 and g, strictly less than 2g. It must vanish. Thus h=g, C has no
essential added 1-handles, and C is a product. The vertical boundary is fixed;
a basepoint arc there identifies the two based surface-group actions.
This yields monodromy conjugacy rel boundary, hence S=K. Merely forgetting
the boundary marking would leave a Dehn-twist ambiguity and would not justify
that conclusion.

Apply this to K0 and both orientations of mirrored K1: each is minimal among
the fibered predecessors used in the decomposition theorem. This argument
also rules out U as such a predecessor. No extension of an Alexander theorem
from standard S3×I to an exotic ambient manifold is silently assumed.

## Apply the paired predecessor collections

The companion R is fibered. The (2,1) pattern fibers, so J is fibered too,
with Delta_J=d(t^2)^2. One can see the fiber directly by attaching two copies
of the companion fiber to the two inner boundaries of the pattern's
two-holed-disk fiber. The return map swaps the copies, with its square
restricting to the companion monodromy. Its characteristic polynomial is
Delta_R(t^2)=d(t^2)^2. The genus is 8. No new HFK computation is needed.

Assume U<=h D01#J and prime-factorize J; its factors are fibered. The K0
target's predecessor sum must equal K0 by the preceding calculation. Unique
prime decomposition leaves precisely one nontrivial K0 in that collection.
The global pairing requires another occurrence of -K0. It cannot lie:

1. in the same collection, which has only one nontrivial prime factor;
2. under the mirrored K1 target, whose predecessor is itself, a distinct type;
3. under any prime factor of J: divisibility would force d|Delta_J.

The third possibility is impossible because gcd_Q[t](d,d(t^2))=1. A completely
integer witness is saved: u*d+v*d(t^2)=28, where

    u = 49+60t-67t^2-117t^3+37t^4+72t^5-11t^6-24t^7,
    v = -21+87t-61t^2+24t^3.

Thus every possible assignment fails. This excludes ALL ribbon disks for
the fixed D01#J, including mixed first bands, not just the prefix in research/48.
The argument never assumes the cable itself is prime. It also never treats
its norm polynomial as satisfying Miyazaki's irreducibility hypothesis.

## A necessary condition for another fibered stabilizer

More generally, if D01#T is ribbon for a fibered T, the missing mates of both
K0 and -K1 must be supplied among T's predecessor collections. Their combined
Alexander contribution is d^2. Multiplying the divisibilities over T's prime
factors gives the necessary condition

    d(t)^2 divides Delta_T(t) over Q[t,t^-1].

This is not sufficient. T need not be ribbon for this necessary condition;
requiring T ribbon only narrows the allowed constructions.

The whole family C_(p,1)(R), p>=2, fails even d-divisibility. If d shared a
root with d(t^p), irreducibility would imply d|d(t^p), so raising to the pth
power would carry every root of d into its finite root set. Yet d has a root
of modulus greater than 1: it is reciprocal, and on the unit circle

    t^-2 d(t) = y^2-3y+3 = (y-3/2)^2+3/4 > 0,
    y=t+t^-1 real.

Taking a root of maximal modulus contradicts closure under pth powers.
Hence changing cable multiplicity cannot rescue this stabilization strategy.
No partner sweep was performed, and no replacement stabilizer is proposed here.

## Limits

The theorem dependence is the March 2026 Agol–Ren preprint. The stored prime,
fibered and distinctness computations and the D01 factor identification retain
their previously stated software trust boundaries. The polynomial identity is
exactly replayed in this directory. Nonribbonness is not nonsliceness. A CE
would still require an actual smooth disk in standard B4.
