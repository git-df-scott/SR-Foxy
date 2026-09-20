# A marked surface construction for the two mixed curves

18 September 2026. Independent bounded geometric audit. This note constructs
curves on the already constructed genus-two surface; it does not construct
compression disks, an ambient product between its handles, or a new PD for
the correction surface. The endpoint identifications below were supplied by
the main task's port replay, not independently recomputed here.
The four tracks are a relative geometric prescription on Research42's
realization with its fixed b-root. There is no coordinate-recorded 14-push
correction diagram or full handle-transfer movie in this note.

## 1. The second handle of the original surface

Write F for the genus-one, two-boundary surface formed from the two native
product annuli and the two actual bands. Let u,v be inward-pushed native
upper c1,c2 cores, respectively. Use these actual paths:

* B1 goes from upper c2 to lower c1.
* rho1 goes from that lower c1 attachment to B2's upper c1 attachment.
  The saved mirror sends (41,0) to (14,1), on the same edge as (13,2),
  so rho1 can be strictly vertical on this product annulus.
* B2 goes from upper c1 to lower c2.
* rho2 first goes vertically from (52,0) to the source edge containing
  (25,3) and (19,2), then follows the positive native c2 arc through
  crossings 19,10,26,17 to the B1 attachment on edge 15.

Put z0=B1 rho1 B2 rho2. Push any boundary portions slightly into F and smooth
the corners. The rho2 corner can be rounded inside its product annulus.
The two product annuli are disjoint and the actual bands have disjoint
interiors, so this is an embedded surface curve. Each rho crosses an
interior annulus core once. The displayed direction already gives
v intersect z0 = +1: if theta follows native c2 and s goes upper to lower,
F has orientation -dtheta wedge ds on the second annulus, and the ordered
tangents of v and the rho2 leg are (+theta,-s).

There is a new directed choice z1: replace rho1 by a spanning arc with one
positive winding around native c1, fixing its endpoints. A monotone s
coordinate makes this winding arc embedded. Then [z1]=[z0]+[u], and
v intersect z1 remains +1. Below z denotes the chosen z0 or z1; the
connector construction works for either. Their group images need not agree.

The native/mirror orientation convention in GEOMETRY.md gives [a]=[u]+[v].
Consequently u intersects z with sign -1, and (v,z,[a]) is an integral basis
of H1(F). This distinguishes the actual second handle from an unspecified
second generator. Changing the two spanning-arc windings changes z by
k1 u+k2 v=(k2-k1)v+k1 a in homology; it need not preserve its based word.

## 2. Isolate the handles and their actual connecting planar region

Let Sigma be F glued to the inverse one-handle correction along b. Take
H_F to be a sufficiently small regular neighborhood in F of v union z.
It is a once-punctured torus. The closure of F minus H_F is a pair of pants
with boundaries a,b,eta_F. Similarly isolate the correction's marked
handle pair in a once-punctured torus H_C, leaving a pair of pants with
boundaries b,b',eta_C. Their union along the actual b seam is a four-holed
sphere P with boundaries a,b',eta_F,eta_C.

Orientation correction, added after the new z1 computation: the relation
b'=[A,B]b with oriented boundary b'-b means A intersects B with sign -1 in
S, not +1. Indeed a positively intersecting torus basis has induced
punctured-torus boundary [A,B]^-1: the polygon boundary goes counterclockwise
around the deleted disk, opposite its induced boundary orientation.
Therefore A intersects B with sign +1 on the inverse correction -S.

Use c=-A and d=+B as the oriented correction basis. Now c intersects d
with sign -1 in Sigma, opposite the sign of (v,z). The corresponding formal
diagonals are v A and z B^-1. My earlier assignment d=-B used an unsupported
opposite sign for the original correction basis and has been corrected.

## 3. Four specified endpoint intervals, with the orientation check

The following is a local construction inside these actual subsurfaces.
At the crossing point of v,z, choose an oriented vertex disk whose outgoing
half-arms have cyclic order

    v+, z+, v-, z-.

Remove a smaller vertex disk together with a thin channel to eta_F, with
the channel in the sector between z+ and v-. This is the upper/backward-
native sector at the chosen intersection near upper edge19. Removing this
boundary-attached
notch leaves another once-punctured torus, and enlarges P by that notch.
The truncated v and z curves are disjoint proper arcs r_v,r_z. They form a
complete cutting system. On the new boundary interval I_F, oriented as a
boundary interval of the enlarged P, their endpoints occur as

    v-, z-, v+, z+.

At the correction crossing, the positive Sigma orientation gives half-arm
order c+,d-,c-,d+, since c intersects d negatively. Put its channel in the
sector between c- and d+ (the physical A+,B+ sector). The correction endpoint
interval I_C, again
oriented as boundary of P, then has order

    d+, c+, d-, c-.

The two enlarged handle pieces still have complementary four-holed sphere
P. Choose an actual embedded arc tau in P from I_F to I_C, crossing the old
b seam once. One way to choose it is to concatenate an arc in each of the
two pairs of pants through the fixed b-root interval, then smooth there.
Record these arcs; they are new surface marking data, not global whiskers.
Thicken tau to a rectangle T, extending its end intervals along the boundary
to contain the four endpoints. The holes a,b' remain outside T. End-interval
adjustments and their collars are carried along in this construction.

The induced boundary orders at opposite ends of an oriented rectangle are
opposite. Hence four parallel tracks in T pair precisely

    v+ -> c+,  z+ -> d+,  v- -> c-,  z- -> d-.

Call these four paths K_v+,K_z+,K_v-,K_z-, oriented F to correction. The
orders above are the explicit noncrossing check. Pairing two bases with
the same surface intersection sign would fail this check.

There is a choice of tau and of the boundary collars. This is a construction
of a marking, not a claim that the previous files already recorded those
choices. To extract numerical group words, the chosen tau and end collars
must be saved and transported through the existing charts. In particular,
passing a different side of a or b' can change the words.

## 4. The two actual closed curves

Orient the truncated arcs r_v:v+ to v-, r_z:z+ to z-, r_c:c+ to c-, and
r_d:d+ to d-. Define the following paths on Sigma:

    Gamma_v = r_v K_v- r_c^-1 K_v+^-1,
    Gamma_z = r_z K_z- r_d^-1 K_z+^-1.

All four tracks in T are disjoint; the two arcs in each handle piece are
disjoint. Consequently Gamma_v and Gamma_z are disjoint embedded curves
after smoothing their corners. This conclusion uses the constructed
subsurface paths, not equality of words in the disk-exterior group.

Their projections to the F handle homology are the two basis elements v,z.
The complement of their union is connected: a separating union would give
a nonzero relation among these projections, since the two exterior boundary
classes project to zero. Cutting along both therefore gives a genus-zero
surface with six boundary components. Abstractly compressing both produces
an annulus. Geometrically this requires two embedded, mutually disjoint,
surface-framed cap disks with interiors disjoint from Sigma and the original
slice disk. None is supplied here.

There is a stronger group statement for THIS coherent-strip construction.
Let p_F,p_C be the two vertex-disk centers, and close the four proper arcs
through their respective vertex disks. This recovers the original free
homotopy classes v,z,c,d. Close each track K to p_F and p_C by paths in these
disks. The rectangle T and its two end intervals show that all four resulting
paths p_F to p_C are homotopic to one path lambda. The end intervals lie on
the small vertex disks; the required endpoint homotopies do not go around
the holes a,b'. Thus, with this vertex basing,

    [Gamma_v] = v lambda c^-1 lambda^-1,
    [Gamma_z] = z lambda d^-1 lambda^-1.

Changing tau can change lambda, but cannot insert an independent boundary
word into just one of these expressions. Existing global basings add their
recorded access paths; free conjugacy remains unchanged. In particular,
nullhomotopy of Gamma_z would require z to be conjugate to d=B in pi1(W).
A representation with different traces for z and B rejects this
specific second curve, irrespective of the choice of tau. This conclusion
uses the single rectangle and vertex-disk closures, not arbitrary previously
chosen connector paths.

The main task reports trace(q(z0))=1 versus trace(q(B))=2 over F17,
rejecting the original zero-winding second curve. It now reports an exact
source-relator replay z1 B^-1=1 after the single positive winding. That is
the sign required by this corrected oriented construction. The earlier
trace mismatch for z0 does not reject z1. The replay itself is not duplicated
in this conceptual note.

To obtain q(lambda)=1, choose the actual strip root corridor as follows.
Put the F vertex near the upper end of rho2 at edge19. Its short vertical
access to that upper edge retracts to a point in the product exterior.
Follow the upper native arc back to the b-anchor (7,1), then the fixed
correction root path. If the main task's port traversal confirms that this
access arc crosses only a and has no R underpasses, its above-based closure
has trivial word after deleting only R. This proves q(lambda)=1 for that
chosen corridor. It does not erase the protected a-meridian, prove collar
disjointness, or follow merely from the existence of four parallel tracks.

Thus the new construction has the correct orientation to match both handle
classes: v=A^-1 and z1=B, with the short marked root corridor supplying the
common trivial connector in pi1(W), subject to the main task's finite path
and word replay. This yields two nullhomotopy candidates with a specified
surface cut system. It supplies neither the full mixed-transfer movies nor
embedded, mutually disjoint, correctly framed compression disks.

## 5. What the correction construction preserves

Research42 moves its whole marked surface by ambient isotopies of S3 fixing
a and b while allowing passage through R. It therefore preserves its entire
ordinary Seifert form, marked curve knot types, and linking with a and b.
In particular every correction surface homology class has linking zero with
a: this is true initially for its handles and boundary generator. Word
prescription cannot independently alter these data. A numerical Seifert
matrix requires the initial oriented basis and push-off convention; this
note does not invent one.

Suppose, additionally, that all mixed-curve pieces and their connector
system have a COMMON boundary-collar realization, defining an additive
linking functional ell with the same protected axis a. Then ell(v)=1,
ell is zero on the correction handle homology, and the preferred boundary
classes have ell=0. For any two mixed curves whose projections to the F
handle homology form a unimodular matrix M, their linking values are

    M (1, ell(z))^T.

They cannot both vanish; their greatest common divisor is one. Hence both
curves cannot have clean caps in that collar complement. Opposite totals
on two different proposed caps do not by themselves form a cancellable
Whitney pair: the boundary-determined total of each individual cap remains.

This last obstruction is CONDITIONAL on the common collar realization.
The actual z above uses the product annuli in the interior of W. Its
boundary-collar representative and compatible transport have not been
constructed here. Therefore this argument is not a global obstruction to
the two disks in W, to other compression systems, or to an annulus.

## 6. Sign of a product vertical in the Dehn marking

Let u be the above access path to an upper point, v the below access path
to its corresponding lower point, and V the product vertical from upper to
lower. The global lower access path is P0 v. Hence the based upper-to-lower
loop is

    u V (P0 v)^-1 = u V v^-1 P0^-1 = P_f P0^-1 = D_f.

The reversed, lower-to-upper vertical contributes D_f^-1, with the same
access paths. This verifies the sign convention in the main task's directed
word computation; its complete port traversal and matrices must be checked
in that computation's own artifact. Reversing z to fix its surface
intersection sign does not change its trace in an SL2 representation.
