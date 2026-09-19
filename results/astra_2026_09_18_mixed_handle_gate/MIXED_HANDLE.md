# Change the compression curves, and retain the protected axis

18 September 2026. The question is whether the genus-two surface can be
compressed by matching its original and correction handles. Success requires
two embedded, mutually disjoint, surface-framed caps, with interiors disjoint
from the surface and the original slice disk. Equal words are insufficient.

## A new exact match

The native upper c2 is component 2 of the saved scaffold, oriented from its
lexicographically first port. Traversing it geometrically reads

    c2 = [4,-1,3,-4].

The new one-handle correction has A=[4,-3,-3,1]. Applying the already certified
finite Tietze and Schreier identities to this NEW native-component word gives

    c2 -> [2,-1,3,-2,1,-2],
    A  -> [2,-1,2,-3,1,-2].

These are literal inverses. Therefore A=c2^-1 in the recorded BOUNDARY group,
not merely after applying q0. No conjugator search or faithful-representation
assumption is involved. The native traversal, intermediate translations, and
input hashes are in CHECKS.json.

An independent replay found a shorter proof: the actual crossing-11
Wirtinger relator is [1,4,-1,-3], while c2*A freely reduces to
[4,-1,-3,1], its cyclic permutation. Thus this identity needs only ONE
geometric crossing relation, not the longer Schreier calculation.

This points to matching handles across the two constituent surfaces, rather
than trying to cap A alone. It does not identify embedded curves in the
complement of all marked objects.

## The actual geometry prevents the simplest collar match

Build axis a using the actual second band with `arc_is_under=[True,False]`:
the first crossed R arc lies under the band and the second lies over it.
Leave native upper c2 untouched. This is a finite four-component diagram;
its PD, tagged adjacency, orientation anchors, and band route are saved.
Axis a is unchanged when the other original band subsequently constructs b.

The only crossings between c2 and a are original crossings 25 and 26, both
positive. Hence lk(c2,a)=+1. Equivalently, the a-band joins upper c1 to lower
c2 and crosses only R; it preserves upper c2's linking with that pair.

The lost meridian is also located exactly: c2 passes UNDER a at port (26,2).
Keeping all protected objects, its above-based word encounters the meridians
at over-ports (19,1), (10,1), (26,1), (15,1), (21,1), with signs +,-,+,+,-.
The middle meridian belongs to a; the other four belong to R. Forgetting a
deletes that middle letter. The replay keeps the distinct local R-meridians;
it does not equate them across underpasses of the protected a component.

By contrast, the A-core in research/42's correction construction starts in a
small ball disjoint from a. Its disk-push isotopies fix a, even when they cross
R. Therefore lk(A_handle,a)=0. Reversing native c2 gives linking -1.

There can be NO ambient boundary isotopy fixing a that takes this A_handle
to reversed c2. In a product collar S3×I, any oriented trace making that
identification has algebraic intersection

    trace(A_handle -> -c2) · (a×I)
      = lk(-c2,a)-lk(A_handle,a) = -1

with the matching product-orientation convention. This is a necessary signed
total for a proposed trace, not a claim that we have drawn a trace with exactly
one intersection. Full-group intersection labels and its other intersections
have not been computed.

An equivalent variable change is to retain the doubly marked exterior
S3\(R union a). The prescribed A word has a-meridional exponent 0, whereas
native c2 has exponent +1. The based product A c2 is trivial after forgetting
a, but has exponent +1 before forgetting it. A connector and its inverse
cannot change that abelianization. Thus that collar representative has no
cap in the doubly marked three-dimensional exterior.

This failure is narrower than a four-dimensional obstruction. It does NOT
exclude a transfer deeper in W, a different handle system, or an annulus.
The protected product trace a×I is the specific collar sheet used by the
proposed shortcut; it is not an assumed dual sphere or a new global invariant.

## What the mixed compression curves must actually be

Abstractly, a genus-two surface with two boundary components is
boundary(H×I) minus two disks in the side annulus, where H is a punctured
torus. This supplies an abstract surface model, not an embedded product in W.
Choose two disjoint proper arcs r1,r2 cutting H into a disk. Their doubled
boundaries give two disjoint mixed compression curves; compressing both gives
an annulus. Their actual based words are

    r_i^(0) c_(q_i) (r_i^(1))^-1 c_(p_i)^-1.

The c-paths are the four actual side connectors on the surface. Their planar
region has the two external boundary holes. Changing a connector can insert
a boundary word, so substituting arbitrary products such as A c2 without
transporting these paths would be another marking error.

The two handle identifications must reverse intersection form. With both
bases assigned intersection +1, the naive diagonal pair has intersection 2
and cannot be disjoint. Reversing the correction surface makes the intended
contributions +1 and -1; this removes that algebraic defect but does not supply
the embedded caps. An actual embedded product H×I with the correct faces and
clean interior would supply the two rectangle caps. No such product was built.

## Next geometric action

Keep the genus-two construction. Draw its second mixed transfer with all four
connector paths, and compute its signed intersections with the SAME protected
a-collar. Determine whether it supplies an opposite contribution to the -1
above, then calculate the full-group labels before proposing a Whitney pair.
This is one directed geometric experiment. It is not a claim that the missing
positive intersection, Whitney circle, framed disk, or annulus already exists.
