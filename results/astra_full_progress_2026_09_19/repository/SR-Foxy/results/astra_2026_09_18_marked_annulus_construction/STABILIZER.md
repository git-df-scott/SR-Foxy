# One constructive pivot: retain the collar half-turn in a ribbon stabilizer

18 September 2026. J is ribbon; D01#J is NOT certified ribbon or slice here.

## The fixed design

The direct genus-14 compression attempt in GEOMETRY.md failed on its two
specified handle loops. For the single permitted pivot, retain the explicit
product ribbon disk D for R=K0#(-K0), its zero normal framing, and the marked
half-turn from the collar construction.

Take two disjoint small normal parallel copies D_+,D_- of D. Attach one
oriented band between their boundaries in the marked cut-arc ball. Specify
the band, rather than inferring it from the existence of two strands: its
two cable positions exchange by one positive half-turn and there are NO
additional full turns. Away from this ball the two boundary strands are
the preferred-zero parallels of R. In coordinates on nu(R), they are the
two branches of a pair of opposite normal vectors that rotate through pi
once around R. The unordered two-point configuration therefore has one
positive braid generator. This defines the (2,1)-cable

    J = C_(2,1)(R).

This is a new, explicit design using the collar's framed half-turn. It is
not a claim that the prior crossed-band movie automatically selected this
satellite pattern, or that cabling cancels its nontrivial handle loops.

The surface D_+ union band union D_- is connected, orientable, embedded, and
has chi=2-1=1. Its two input disks are ribbon; their small parallel copies
remain ribbon, and the joining band adds a saddle without a maximum. This
is the geometric ribbon certificate for J in standard B4. It uses actual
parallel disk blocks and a specified boundary band, not a numerical slice
invariant. We have not expanded the product-disk blocks into a list of
elementary planar ribbon moves in this package.

For comparison, this is the construction in Hom--Kang--Park, *Ribbon knots,
cabling, and handle decompositions*, arXiv:2003.02832v2 (25 March 2020),
[Proposition 2.1 and its proof](https://arxiv.org/pdf/2003.02832).
The proof uses parallel ribbon disks and half-twisted bands. Source checked
18 September 2026. The predicted Alexander polynomial is d(t^2)^2, where
d=t^4-3t^3+5t^2-3t+1. This is a satellite-formula consequence, not a new
invariant computation and not a certificate for D01#J.

## Finite diagrams and the one attempted ribbon prefix

The producer records the six-crossing K0 braid

    alpha = [1,-2,1,-2,-2,1].

Its braid conversion comes from Spherogram's deterministic diagram routine;
that software conversion remains trusted. Joining it to its mirrored copy
on a block sharing one strand gives a five-strand braid beta for R. The
identification with K0#(-K0) also uses the invertibility of 6_3: mirroring a
braid by itself does not reverse its knot orientation. The
[Knot Atlas 6_3 entry](https://www.math.toronto.edu/~drorbn/private/KAtlas/Knots/6.3.html)
lists it as fully amphicheiral, hence invertible (source checked 18 September
2026). This is a cited knot-type fact, not a symmetry certificate produced
by this package. The companion has writhe zero. Replace each crossing
sigma_i by the four-crossing
two-parallel block

    sigma_(2i) sigma_(2i-1) sigma_(2i+1) sigma_(2i),

using the inverse block for a negative crossing. Append sigma_1 to insert
the specified single positive cable half-turn. Thus J has a saved
49-crossing PD. The stored 25-crossing D01 gives a fixed 74-crossing
diagram of D01#J. No diagram simplification or search is hidden in these
numbers.

The first attempted descending ribbon move was the obvious inverse of the
joining band: the oriented saddle at the final cable crossing. In the
connected-sum diagram that crossing has tag `(48,2)`. Its exact reconnections
and the resulting 73-crossing, two-component PD are saved.

Removing the final sigma_1 leaves the two preferred-zero parallels of R.
An independent color traversal of the doubled braid projects EACH component
to beta; the mixed signed crossing sum is zero. The D01 connected-sum
insertion lies away from the removed crossing and stays on one component.
The output component knot types are consequently

    R,       D01#R.

This is a component identification, NOT a claim that the two-component link
is split. Isolating the actual output components gives 12 and 37 crossings,
consistent with that exact construction.

## Why this specific prefix cannot finish as a ribbon disk

The stored knots K0 and K1 already have the required prime, fibered,
irreducible-Alexander certificates. Research/44 and the exact Jones package
from the preceding session remove any need here for unequal unverified
hyperbolic signatures. In particular K1 is distinct from both K0 and its
mirror.

We additionally checked the ACTUAL stored D01 decomposition, instead of
trusting its filename. The two cut edges `(3,1)--(6,0)` and `(0,0)--(22,2)`
share both incident faces, giving a dual bigon and a connected-sum sphere.
Restoring each factor gives a six-crossing port graph identical to K0 and a
19-crossing factor positively identified with mirrored K1. The latter uses
12-tetrahedron triangulations with all 48 directed face gluings checked
independently. See `factor_identification/certificate.json` and
`check_factor_identification.py`. As in research/44, the upstream PD
triangulation and retriangulation steps remain kernel-trusted; there is no
standalone Pachner-move log. No numerical signature inequality is used.
Knot orientation was not independently transported in this last comparison;
unoriented summand types suffice for the exclusion below. Thus this use of
the nonribbon theorem does not need the paper-to-L diagram identification.

D01#R has prime summands

    K0 # (-K1) # K0 # (-K0).

All four satisfy the existing Miyazaki pairing hypotheses. The lone K1-type
summand has no possible mirror partner among the other three. Hence this
particular knot is nonribbon, by precisely the same certified pairing
argument used for D01. This does not apply directly to D01#J: J has the
nonunit norm polynomial d(t^2)^2, and we do not drop the theorem's hypotheses
to obtain an exclusion for it.

If a ribbon disk for D01#J began with the specified split saddle, the part
after that saddle would consist of two ribbon disks, one for each output
component. To see the component requirement, the prefix is a pair of pants
in a disk. Its complement consists of two disks: joining its two outgoing
circles in one complementary surface would add genus. Ribbonness passes to
these future disks, since their movies retain no maxima in the ascending
direction. A ribbon cap for D01#R is impossible. Therefore **this particular
first saddle cannot be the start of a ribbon certificate**.

This is a global obstruction to completing a specified prefix, not a failed
timeout, and not an obstruction to all ribbon disks for D01#J. The construction
does give a ribbon certificate for J, but the second required certificate is
missing. No inference of sliceness of D01 is made.

## One next action

Keep this J fixed. Construct a first splitting band that genuinely mixes the
D01 part with a cable sheet before the cable-joining band is removed. The
new one-handle update supplies a shorter candidate A whisker than factor 10;
see `ONE_HANDLE_UPDATE.md`. Save and identify its
two output components before any continuation search. The specified inverse
joining band has been ruled out as this first move; arbitrary bands in that
ball have not been classified. Transferring the old whisker onto this new
PD requires its own marked route; that route has not yet been supplied.
