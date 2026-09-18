# Realizing the correction by an embedded surface with exact linking control

18 September 2026. Continuation of research/40--41.

## Question and status

Can the *whole* second-derived correction be realized by changing the second
auxiliary axis, preserving both the auxiliary unlink and its exact equivariant
linking matrix? The argument below gives an existence construction in three
dimensions. It is a mathematical argument with independently audited local
steps, not a machine-certified diagram or a counterexample to Slice--Ribbon.
No historical novelty is claimed.

The key change is to construct a surface with a moving boundary, rather than
to select a convenient representative of its boundary word. This controls the
peripheral data that the point-pushing prototype in research/41 failed to
control. It does not assert that the previously saved physical axis already
has this geometry.

## 1. Precise realization statement

Let R be an oriented knot in S3, M=S3 minus R, and G=pi1(M). Use the
abelianization e:G -> Z given by linking with R. Let a and b be a marked
auxiliary unlink disjoint from R, with e(a)=e(b)=0. Fix zero-framed push-offs
and lifts to the infinite cyclic cover of M. Suppose

    delta = product(j=1,...,g) [u_j,v_j],       e(u_j)=e(v_j)=0,

where [u,v]=u v u^-1 v^-1 and the words are based at the same marked root.
Then there is a new embedded curve b' in M, with an embedded oriented genus-g
surface S in M from b to b', such that:

1. The marked boundary relation is b'=delta b in G.
2. a union b' is an unlink in S3.
3. Every loop on S has exponent zero.
4. With lifts matched through S and preferred zero framings, the exact
   rational equivariant linking matrix of (a,b') equals that of (a,b).

The choice of b' is part of the construction. This is not a claim about every
representative of delta b. The statement also does not say S is an annulus:
its genus is g.

## 2. Start with a fixed zero-framed collar

Take a small zero-framed parallel b0 of b, joined to b by an embedded annulus
disjoint from R and a. Stabilize this annulus g times in a small ball on its
b0 side, keeping an annular collar of b fixed. This produces a standard genus-g
surface S0 with boundary b0-b. Its 2g marked handle loops are initially trivial
in G. The remaining generator of pi1(S0) is the old boundary b.

Choose a disk-and-band marking for the handles. Each handle generator traverses
one designated band, and its root paths lie in a fixed part of the surface.
Choose the boundary orientation and order so the surface relation reads
b0=(product [u_j,v_j]) b after prescribing its handle loops. These markings
fix the order and conjugating paths; equality is based, not just cyclic.

Throughout the construction keep the old collar, b, a, and the root paths
fixed. All moving bands and their free boundary lie away from that collar.
Initially a union b0 is an unlink. We will move S0 by ambient isotopies of S3
fixing a and b **when R is omitted from the moving configuration**. The moving
surface may cross the fixed R during such an isotopy. Both endpoint surfaces
are disjoint from R. Thus the ordinary auxiliary link type is preserved while
the words in G may change.

## 3. A disk-push prescribes one handle word

Write a selected marked handle loop as c=p a0 q, where a0 is a short subarc in
the interior of its designated band. No other marked handle uses this subarc.
Choose a whisker from a0 to a small meridian disk of R. Ribbon-connect that
disk to a tiny half-disk based on a0. After shrinking the neighborhoods, this
gives an embedded disk D with

    boundary D = a0 union a1,
    int(D) disjoint from S and the fixed auxiliary curves,
    D transverse to R in exactly one point.

Slide the full width of the band across D. This is an ambient isotopy after
forgetting R, supported away from the other bands and the old collar. Its
endpoint is again an embedded surface disjoint from R. The selected loop
becomes c'=p a1 q, and therefore

    c' c^-1 = p (a1 a0^-1) p^-1.

This is the conjugated meridian determined by the whisker, with either sign
available. Every other marked handle loop is fixed. The *free boundary edges
of the selected band move too*. Holding the entire surface boundary fixed
would invalidate this argument.

Why can the required whisker avoid S without changing its class in G? Start
with the desired path in M, avoiding the fixed auxiliary curves by general
position. At any transverse crossing of S, run a detour on the two sides of
a thin surface strip ending at the moving boundary b0, and pass around its
free edge. This replaces the crossing by a path avoiding S. The replacement
is homotopic to the original path in a neighborhood of that strip disjoint
from R and the fixed auxiliary curves: the moving boundary is *not* deleted
from M. Repeat finitely many times. The path can then be made embedded, and
the one-dimensional fixed root paths can also be avoided. At the initial
point, use the appropriate side of the selected band. The thickened whisker
and meridian disk may be chosen sufficiently thin to keep the required
disjointness.

Meridians normally generate a knot group. Consequently successive disk-pushes
can insert any finite product of conjugated meridians into the chosen loop.
They act by left multiplication; read the factors in reverse order to obtain
the prescribed target word. Starting with the trivial handle loops, carry out
these moves independently for all 2g words u_j,v_j.

This proves the prescribed based boundary relation and embeddedness. Every
move is an isotopy of the whole marked surface relative to a and b after
forgetting R. Therefore a union b' retains its original unlink type. Notice
that this proof supplies finite geometric instructions, not coordinates or a
new planar diagram. The finite word list alone would not establish the claim
without this disk-push and free-edge argument.

## 4. Exact equivariant linking, including the diagonal

Now pi1(S) is generated by the old b and the prescribed handles, all of
exponent zero. The cyclic covering restricted to S is trivial: each component
of its preimage maps homeomorphically onto S. Choose one compact lift S~.
Its deck translates are pairwise disjoint and its boundary is

    boundary S~ = b'~ - b~.

Take a sufficiently small normal push S+ downstairs. It is disjoint from S;
thus every lift of S+ is disjoint from every lift of S. Because the old
zero-framed collar was fixed from the beginning, this push restricts at b to
the original b+. It restricts at b' to a framing denoted b'^+.

For compact chains, the bounding-chain definition of equivariant linking gives
the **exact** identity

    lk_e(boundary C, z) = sum_k (C intersect t^k z) t^k,

in the convention chosen for the deck variable. Alexander torsion causes no
Laurent-polynomial ambiguity here: multiply by an annihilator to define
linking, then cancel it in the rational function field. Applying the identity
to S~, and to S~+ using hermitian symmetry for the second variable, gives

    lk_e(b' - b, b+) = 0,
    lk_e(b', b'^+ - b+) = 0.

All the relevant intersections vanish by the tubular-neighborhood construction.
Adding the identities proves

    lk_e(b',b'^+) = lk_e(b,b+).

The mixed entries with a and its sufficiently small push-off are unchanged
because S is disjoint from a; choose the neighborhoods small enough that the
push-off also avoids S. The aa entry is unchanged because a is fixed. This
proves equality of the full matrix, not merely equality modulo Laurent
polynomials.

Finally the surface-induced framing of b' is its preferred zero framing:
specializing the diagonal equality at t=1 gives ordinary self-linking zero,
as for b. For knot exteriors an Alexander annihilator with nonzero value at
1 is available, so this specialization is legitimate. The matching of lifts
through S is essential; independent deck shifts would change displayed
off-diagonal entries.

## 5. Application to the saved correction

Research/40 independently verifies thirteen commutators of exponent-zero
boundary words whose product equals the 26-letter correction delta in G.
Use those exact ordered words as the handle instructions above. This yields
an existence construction of a modified 0110 pair with:

    actual auxiliary unlink; exact E=0; based b'=delta b.

Under the **saved algebraic** map q0, the existing word certificate then gives

    q0(b') = mu^-1 q0(a) mu.

Thus the three-dimensional requirements are compatible for a new choice of
representative. The saved map still needs identification with a particular
marked disk exterior. Its peripheral test in research/41 passes for every
q_n, but a necessary-condition pass is not that identification.

The recipe in `results/night_2026_09_18_geometric_gate/surface_recipe.json`
records every target handle word and reverse insertion order. Its checker
only validates the finite algebraic inputs and ordering. It does not pretend
to verify a geometric embedding computationally.

## Evidence and remaining falsification targets

| Claim | Evidence | Limit |
|---|---|---|
| Entire correction has the required handles | Archived independent free-word replay | Based on the saved boundary presentation |
| New representative preserves unlink and exact E | Disk-push construction and lifted-surface proof above; separate agent audit | No explicit marked PD generated |
| Saved q0 images become conjugate | Existing exact word correction | q0 geometry still unidentified |
| Embedded annulus in the disk exterior | Not established | A genus-13 boundary surface is not an annulus |
| Resulting boundary is a nonribbon slice knot | Not established | Neither standard-B4 disk nor actual boundary identification supplied |

The most valuable next attack is now to identify the product disk exterior
geometrically and draw an immersed annulus realizing the certified conjugacy,
recording its double-point loops and framings. Vanishing abelianized data
does not give Whitney disks with clean interiors. A smooth embedded annulus,
standardness of the subsequent modification, and a nonribbon certificate for
the *actual* resulting knot remain separate requirements. A second useful
audit is to turn one disk-push into a marked local diagram and check its
longitude; it must differ peripherally from the defective braid in research/41.

This note's realization proof is our derivation, not an attribution to the
papers cited in research/40--41. Independent review notes are preserved with
the computation artifacts.
