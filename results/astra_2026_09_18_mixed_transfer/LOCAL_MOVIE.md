# Two explicit local transfer patches at crossing 26

This is a **local control**, not the requested pair of complete handle
transfers. Its endpoints are two crossing-switched parallel arcs, not the
unrealized correction cores. It cannot supply the missing global movie by
itself. It makes the sheet-incidence and framing bookkeeping testable.

Crossing 26 in the stored scaffold is the native c2 underpass of a. Both
v and the upper leg of z1 follow this segment, with the same native direction.
The prospective transfer of A to -v reverses that direction; the prospective
transfer of B to z1 retains it. Take disjoint parallel tracks in a small
crossing ball, with no R in the ball. Use coordinates (x,y,z,t), ambient
orientation dx dy dz dt, and the fixed protected sheet

    P(s,t) = (s,0,0,t),          orientation ds dt.

Put x_-=-1/4, x_+=1/4 and beta(u)=(1-u^2)^2 for -1<=u<=1. Two explicit
crossing-change strips are

    T_-(u,t) = (x_-,u,1-2t beta(u),t),
    T_+(u,t) = (x_+,u,1-2t beta(u),t),       0<=t<=1.

Orient T_+ by dt du (so its boundary at t=1 follows positive u), and T_-
by -dt du. The end arcs at u=+-1 are fixed; beta and beta' vanish there.
The strips can be smoothed into fixed outside collars without introducing
intersections. There is precisely one intersection of each T with P:

| point | sheets | (x,y,z,t) | sign |
|---|---|---|---|
| p_- | T_-, P | (-1/4,0,0,1/2) | -1 |
| p_+ | T_+, P | (+1/4,0,0,1/2) | +1 |

Indeed y=0 forces u=0, then z=0 forces t=1/2. With the displayed orientations
the ordered tangent determinant for (T_+,P) is +2, and that for (T_-,P)
is -2. Recovering u,t from the y,t coordinates proves that each strip is
embedded. Their different constant x coordinates prove they are disjoint.
The only other object in this local model is P; R and other surfaces lie
outside this chosen ball. This is **not** a claim that the unsupplied global
extensions avoid those objects.

The normal fields

    n1=(1,0,0,0),
    n2=(0,2t beta'(u),1,2 beta(u))

are pointwise perpendicular to both tangent vectors of each T and everywhere
independent. Thus the displayed endpoint normal framings extend over each
patch: relative Euler number zero for THESE framings. Their identification
with the global surface/Whitney framings has not been made.

For based labels in this local model, take o=(0,0,2,0). Run the P whisker
from o vertically to (0,0,0,0), then on P to each point. Run the T whisker
at t=0 from o to (x_+/- ,0,1,0), then on the corresponding T to its point.
All resulting comparison loops lie in this contractible box. Their labels
are therefore 1 in its ambient group, and remain 1 under its inclusion in
W, with THESE local whiskers. The axes and strips are included as intersecting
objects when defining these labels. In the punctured-strip complement that
deletes P, a small loop around each missing point is an a-meridian, with the
recorded sign; it is not silently set to 1. Global whiskers transported from
the two surface roots have not been substituted for these local ones.

Despite opposite signs and these equal ambient labels, this pair is not yet
a Whitney pair on either proposed cap. Its sheet sets are {T_-,P} and
{T_+,P}. There is no arc on T_- disjoint union T_+ joining the points.
The P arc s from -1/4 to +1/4 at t=1/2 is explicit, but its required partner
arc is absent. Joining the strips by a new handle would change the surfaces
and must be specified globally before it gives a Whitney circle. No such
joining, Whitney circle, or Whitney disk is claimed here.

This control shows exactly what must be attached to the actual handle
transfer construction. It does not infer a global +1 from the earlier
linking total, and it does not assign its two-point ledger to the genus-two
surface without those attachments.
