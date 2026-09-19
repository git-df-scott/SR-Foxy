# An explicit marked product disk and the failed direct compression

18 September 2026. Continuation of research/44--47, not a new campaign.

## What is now specified

Let J° be the source knot punctured along the restored diagram edge
`(0,2)--(1,1)`. Use the product disk J° x I in B3 x I, and its exterior
(B3 minus nu(J°)) x I. Corners are smoothed. B3 x I is a standard smooth
four-ball. The source diagram is the upper 27-crossing marked link with its
cut edge restored; auxiliary components are not deleted from the markings.

The previously saved sector `(0,2)` identifies a side of this cut, but endpoint
data alone did not specify a path through the spherical collar. We now give
that path explicitly. This completes a specified product model; it does not
retroactively identify an unspecified historical disk from its boundary PD.
The completion uses the saved side, with no extra meridional turns. We do not
choose it by evaluating the axis obstruction.

Near the puncture take coordinates (x,y,z), with the cut strand on the x-axis,
z above the source projection, and y>0 the saved region-0 side. Put

    S_y(x,y,z) = (x,-y,z),    S_z(x,y,z) = (x,y,-z).

The target connected-sum picture glues its two diagram balls through a
reference planar neck using S_y. This fixes both puncture endpoints, preserves
height, and exchanges the two neck faces. The product boundary is mapped to
this target by identity on the upper ball, S_z on the lower ball, and on the
ENTIRE puncture-sphere collar by

    Phi(p,s) = (R_(pi chi(s)) p, s),
    R_theta(x,y,z) = (x, y cos(theta)-z sin(theta),
                        y sin(theta)+z cos(theta)).

Here chi is smooth, monotone, and constant 0 and 1 near the respective ends.
For example, normalize the integral from 0 to s of a nonnegative smooth bump
supported in (1/4,3/4). The charts glue because S_y R_pi = S_z. Thus this is a
map of the whole spherical collar and both balls, not a proposed group map.
It is a diffeomorphism of the product boundary with the specified diagram
three-sphere. The product disk and its exterior are retained in B3 x I; this
boundary parametrization does not change the ambient four-manifold.

The lower S_z chart reverses crossing heights and preserves planar cyclic
order. Normalizing undercrossing ports gives the saved odd port rotations.
The 108 transported port adjacencies and the two seam edges are recorded in
`transport.json`. The face circuits verify the required exchange: upper
region 0 joins lower-source region 6, and upper 6 joins lower-source 0.

## Based meridians: pull back the whisker, not the normal vector

A globally-above target neck path has reference coordinate q=(0,0,r).
Its PRODUCT pullback is

    R_(-pi chi(s)) q = (0,r sin(pi chi(s)),r cos(pi chi(s))).

This travels through y>0, hence through the saved bridge P0. Using the forward
rotation here would give the wrong sign. As a control, replacing the collar
rotation by -pi chi(s) has identical endpoint maps but the above whisker pulls
back through region 6. That is a different relative marking and gives q1.

Let P_f go from the above source basepoint to the below source basepoint
through region f, using the fixed above/below access paths. Set D_f=P_f P0^-1.
An upper meridian is P_R P_L^-1. A lower meridian has reversed order and is
based below; transport through the actual P0 gives

    P0 (P_L^-1 P_R) P0^-1 = D_L^-1 D_R.

This is exactly the saved q0 formula, now obtained from the specified collar.
The upper factor supplies all source meridians, so this inclusion is surjective.
All full-group words below use this single construction and these whiskers.

The product-disk model is the one in Meier--Zupan, *Knots bounding nonisotopic
ribbon disks*, J. Topology 18 (2025), e70047, Section 2.1,
[DOI 10.1112/topo.70047](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/topo.70047).
Our marked chart and whisker calculation is additional work, not a statement
attributed to that paper. Source checked 18 September 2026.

## Both actual 0110 ribbons are transported

Keep the target PD bands as saved, including their normal fields and the 0110
crossing heights. Define their representatives in the product boundary by
Phi^-1. This carries a material ribbon vector by D(Phi^-1), rather than
replacing the band by an unspecified straight product band.

The two core routes are:

    B1: (15,2), (16,2), (2,2), (41,0); heights [over,under]
    B2: (13,2), (27,0), (32,2), (52,0); heights [under,over].

Both have the saved zero twist. The successive ports share unique faces.
B1 crosses the neck in its region-0 face; B2 in its region-6 face. On the
neck one may choose target cores at q=+y and q=-y respectively. Their
pullbacks are (+cos(theta),-sin(theta)) and (-cos(theta),+sin(theta)) in the
(y,z) plane. A target transverse vector +z pulls back to
(sin(theta),cos(theta)). Hence the cores go through opposite hemispheres;
neither ribbon's framing is silently reset after the half-turn.

`transport.json` records the full face routes and every oriented traversal
step of both resulting axes, including each encountered boundary meridian and
its image. Their words match the saved 0110 inputs exactly. Transporting the
saved correction word gives q0(b')=mu^-1 q0(a) mu as before. The representative
b' supplied by research/42 still has no new planar diagram in this package;
we do not represent that word calculation as a drawn repaired axis.

## The actual surface attempt and its precise failure

The native curves c1,c2 in the source ball give disjoint product annuli
c1 x I and c2 x I in the disk exterior. Attach the two ACTUAL transported
band rectangles in a sufficiently small boundary collar, away from the
product annuli except at their attaching arcs. Their interiors avoid the disk.
After smoothing, this gives an embedded surface between the 0110 axes.

With the saved native orientations, a follows +c1_upper and -c2_lower,
whereas b follows +c2_upper and -c1_lower. The mirror correspondence reverses
both native orientations. Orient the first product annulus positively and
the second negatively; the band orientations agree and the surface has
boundary a-b. The first band connects the two annuli; the second attaches
to that connected surface. Thus chi=-2 and there are two boundary components:
this is genus ONE, not an annulus.

Reverse the orientation of the genus-13 correction surface of research/42,
so its boundary is b-b', and glue along b. The resulting surface has genus 14
between a and b'. This is a geometric surface construction using that note's
disk-push existence construction; it is not a fully coordinate-recorded
genus-14 diagram or an immersed-annulus movie.

The local ribbon vectors above are tracked, but the relative normal Euler
number of this entire genus-14 surface has not been computed. In particular
there is no claimed correctly framed modifying annulus.

The attempted next move was to compress a designated correction handle,
starting with factor 10. Its two marked candidate loops are

    u=x3^-1 x4,    v=x1^-1 x3.

They are genuine handle loops of the specified surface marking. In the now
specified disk exterior q0(u)=x5^-1 x6. Specialize the saved source matrix
representation to z=1 over F_17; its defining polynomial evaluates to 17.
All nine source relators evaluate to identity. Both u and v have matrix
trace 3, whereas identity has trace 2. Consequently neither loop is
null-homotopic in this exterior. Neither can bound even an immersed
compression disk there. In particular there are no Whitney-disk interior
intersections or framings to list for these nonexistent proposed caps.

This is a definite failure of the two specified direct compressions. It does
NOT exclude other handle systems, a different surface, or an annulus between
the axes. It also does not measure the primary invariant of an annulus:
none was constructed. Research/46--47 cannot be invoked as a replacement
for that missing movie. No paired clasp was applied to the target boundary,
so no new surgery boundary is claimed or assigned D01's nonribbon certificate.

The computation is deliberately small: exact finite diagrams, two band routes,
and one explicit finite quotient. No knot invariant or census was rerun.
