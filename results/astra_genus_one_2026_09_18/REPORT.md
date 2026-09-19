# An explicit genus-one correction and its framed surgery boundary

18 September 2026, Edmonton; computations continue into 19 September UTC.
Source snapshot: `ceb83c2c86c4b538599f95b62812587d2fa3c6fe` of
`git-df-scott/SR-Foxy`. No repository edits, branch creation, or Mac checkout access.

**NO SLICE–RIBBON COUNTEREXAMPLE.** This package constructs a particular embedded,
marked genus-one boundary correction and specifies an actual framed surgery knot
in S³. It verifies the auxiliary unlink, the exact longitude response and the
Alexander polynomial. It does not identify the new knot with D01, prove its
nonribbonness, or construct its smooth slice disk.

## 1. The new geometric object

The input is the repository's 0110 auxiliary pair `(a,b)` in the complement of
`R=K0#(-K0)`. In the saved one-based boundary Wirtinger generators, use

```
A = [4,-3,-3,1]
B = [4,-9,-1,3,-1,8,-5,-8,1,1]
```

Thus `A=x4 x3^-2 x1` and
`B=x4 x9^-1 x1^-1 x3 x1^-1 x8 x5^-1 x8^-1 x1^2`.
The prior one-commutator certificate, retained unchanged in `prior/`, proves
that `[A,B]` equals the original correction δ in the specified boundary group.
This session realizes those words geometrically instead of finding another word
factorization.

The construction is encoded in integer-coordinate triangles and polygons. Start
with a small marked disk at `(900,400,500)`. Attach two narrow bands to alternating
boundary intervals. The A band goes west to east; the B band is marked opposite
to its south-to-north geometric core. The marked boundary reads `[A,B]`.

Each of the fourteen signed letters is a specific meridional excursion about an
identified straight segment of R. The A routes lie at planning height 520 and the
B routes at height 540 except for their excursions; these are **three-dimensional
spatial heights**, not a four-dimensional concordance time. The band widths are
transported through the excursions. A separate joining band connects the patch
to the marked cut of b. An explicit collar from a displaced copy `b^-` to b closes
the construction into a surface S with boundary `b' - b^-`.

The displacement is exactly `z -> z-10^-5` on the old b polygon. It is important:
without that collar, an informal cut-and-insert description would share most of
its old and new boundary arcs and would not yet be a two-boundary surface.

The final surface, in `correction_cobordism_mesh.json`, has

```
V = 499, E = 1005, F = 504
χ = -2
boundary components = 2
orientable = true
```

Every vertex link is a circle or interval of the appropriate kind. The
construction is connected. Consequently this is a genus-one surface. All 2,134
triangle pairs with overlapping coordinate boxes were checked exactly; no
intersection beyond the common combinatorial face occurs. All 980 potentially
intersecting pairs between its triangles and R or a were checked exactly and are
disjoint. Its two boundary polygons agree with the specified b^- and b', allowing
only collinear subdivision. These checks certify a PL embedding; in this
three-dimensional setting it can be smoothed without changing the link or marks.

`check_mesh_independent.py` repeats the geometric intersection checks using a
separate rational segment-clipping algorithm. The producer instead uses
plane-intersection intervals and coplanar polygon clipping. The independent check
agrees and passes six synthetic adjacency/intersection controls.

Route planning used floating-point coordinates and visibility paths. The proof
object is the **saved integer model with common denominator 10^12**, not a claim
about numerical clearance. Reconstructing routes with another library version is
not a substitute for replaying that frozen model.

The spatial figure shows band centerlines because the certified strips are too
thin to see at the scale of the whole configuration. `marked_genus_one.obj`
contains the actual surface mesh and the R,a curves. Neither drawing is itself
the certificate.

## 2. Markings: the geometric words are the requested words

`check_spatial_marking.py` projects each marked handle loop and reads its signed
undercrossings with the native marked arcs of R. The two words are exactly A and
B above. It does not merely compare their Alexander classes.

After the joining band, the actual auxiliary words are exactly

```
a  = [4,-1,3,-4,11,14,-15,-11,1,-9]
b' = freely_reduce(A B A^-1 B^-1 b)
b  = [4,-1,-15,14,-13,17,3,-4]
```

The check uses the same basepoint, crossing signs and native generator names.
The initial planar embedding had the opposite planar orientation. It was
reflected **before** prescribing the signed meridional excursions. The failed
unreflected model and its failed word check are preserved in `attempt02/`; they
are not used for the final result.

The final exact generic projection has 675 crossings. This is a crossing count
of this deliberately explicit presentation, **not the crossing number of a
knot or a measure of candidate-search coverage**. The JavaScript verifier
reconstructs every crossing and its over/under choice from the integer polygons,
checks that no projected vertex/triple degeneracy occurs, orders the Gauss
words independently, and rereads the marked axis words.

The source diagram/native-arc convention is the archived 54-crossing scaffold
and the 0110 band choices. Native labels are transported by matching all eighteen
recorded R-crossing relations, rather than assuming that union-find root numbers
are invariant. The paper-figure-to-scaffold correspondence was not reaudited in
this session. The new construction is attached to the **stored marked input**.

## 3. The auxiliary pair is an unlink, not just a linking-zero pair

Forget R and take the actual polygonal sublink `(a,b')`. Construct its full
Wirtinger group directly from the Gauss diagram. No Gauss Reidemeister heuristic
is needed or used for this certificate.

There are 377 generators initially. Exactly 375 recorded Tietze eliminations
leave two generators, denoted `x46,x313`, and no relators. More importantly, the
preferred longitudes of **both** components reduce to the empty word. The
meridians map to

```
mu_a  -> x313 x46 x313^-1
mu_b' -> x313
lambda_a -> 1
lambda_b' -> 1.
```

`auxiliary_group_certificate.json` records every defining relator, substitution
and peripheral word. The independent verifier reconstructs the auxiliary
presentation from the polygon sublink and replays the transformations; it is not
checking an unrelated free-group presentation.

Here is the topological implication, including the ingredient that an ordinary
linking matrix would miss. A preferred longitude is a simple essential curve on
the corresponding boundary torus. Since it is nullhomotopic in the full link
exterior, Dehn's lemma supplies a properly embedded disk there. Joining it to the
component through its tubular-neighborhood collar gives a spanning disk avoiding
the other component. A regular neighborhood splits that unknot off. Applying the
same argument to the other component proves that the auxiliary pair is the
unlink. Alternatively the spanning disks can be made disjoint by innermost-circle
exchanges.

We use the boundary version of Dehn's lemma, explicitly stated and proved as a
consequence of Theorem 1 in Freedman–Scharlemann, *Dehn's Lemma for Immersed Loops*,
arXiv:1704.05507v2, 15 September 2017, first page. This is a theorem-based unlink
certificate, **not** a saved explicit isotopy of the whole framed link to round
circles. That missing isotopy matters for efficiently drawing the surgery knot.

## 4. Framing and actual surgery definition

Define K_new as the image of R after filling the explicit a and b' curves by

```
a:  (meridian, preferred-longitude) slope (1,1)
b': (meridian, preferred-longitude) slope (-1,1)
```

The latter is the same unoriented slope as `(1,-1)`. Thus these are +1 and -1
surgeries relative to the preferred zero framings. Since the auxiliary sublink
is an unlink, the resulting ambient three-manifold is S³. This is an actual knot
specified by polygons and framed surgery, even though its identification with a
named or previously stored knot remains unknown.

All ordinary pairwise linking numbers among R,a,b' are zero. In the saved generic
projection the self-writhes are `(0,0,-1)`. In particular, the b' preferred
longitude includes the correction for writhe -1; using the uncorrected diagram
transport word would be a framing error. In a blackboard rendering, the extra
framing twists needed for the displayed +1,-1 coefficients are +1 on a and 0 on
b'.

`surface_boundary_framing.json` additionally calculates
`lk(b^-,b')=0` exactly in both directions. For an oriented surface with these two
boundary components, the surface-induced framing on either boundary is the
negative of their mutual linking (with the compatible orientation convention).
It is therefore the preferred zero framing. This check is separate from the
integer surgery coefficients.

Do not confuse the three-dimensional conclusion with a four-dimensional one.
Attaching the two ordinary 2-handles to B⁴ gives intersection matrix
`diag(1,-1)` and H₂ of rank two. That trace is **not B⁴**. Returning S³ as a
boundary does not standardize that four-manifold or make K_new slice. Park's
annulus modification is a different construction whose embedded-standard-annulus
hypotheses still have to be supplied.

## 5. Exact longitude response and filled Alexander module

Use Λ=Z[t,t^-1], sending R-meridians to t and auxiliary meridians to 1. The full
675-generator Wirtinger presentation and every preferred longitude are retained
in `framed_fox_boundary.json`. Removing an R-reference column gives a presentation
on a basis for the kernel of the cellular d₁ map. This is legitimate integrally:
all R columns have d₁=t-1, the other columns have d₁=0, and t-1 is not a zero
divisor.

There are **670 Laurent-unit pivots**, each of the form ±t^k, reducing the problem
to three rows and four columns. The auxiliary meridians are retained throughout.
All pivot choices and observer-row transformations are recorded. Over Q(t) the
relation matrix has rank two and its kernel is parametrized by the two auxiliary
meridians. The preferred auxiliary longitude responses are exactly

```
E(t) = [[0,0],[0,0]].
```

These are exact rational functions, not Blanchfield classes modulo Laurent
polynomials and not evaluations at finitely many t values. The independent
verifier checks the meridian solution by polynomial multiplication and checks
that both longitude rows vanish on it. The nonzero filled minors independently
verify the required rank, so a hidden extra rational free variable is not being
ignored.

For the specified +1,-1 filling, the five maximal minors of the reduced 5-by-4
matrix are

```
0, 0, -t^-4 d(t)^2, t^-2 d(t)^2, -t^-3 d(t)^2,
d(t)=t^4-3t^3+5t^2-3t+1.
```

Therefore the monic Alexander polynomial is exactly

```
t^8 - 6t^7 + 19t^6 - 36t^5 + 45t^4 - 36t^3 + 19t^2 - 6t + 1.
```

Its determinant is 169. Because a maximal minor is a Laurent unit times d²,
this is a full maximal-minor certificate, not a generic-gcd calculation silently
specialized to a potentially exceptional parameter. A separate small Smith-form
calculation gives the same order.

### A genuine parameter extension

Replace the two slopes by `(1,x)` and `(1,y)` for arbitrary integers x,y, including
zero for meridional filling. The five maximal minors are now

```
0, 0, t^-4 d², -t^-2 d², t^-3 d²,
```

independent of x,y. Thus this **specific realized two-axis link** preserves d²
for every integer pair of reciprocal surgery parameters. The ambient manifold is
still S³, by its unlink certificate.

The Python calculation is symbolic. The independent integer checker uses a
separate exact proof: a determinant is affine in x and affine in y because each
appears in only one row; four corner evaluations determine all four coefficients.
The exact corner checks prove the parameter independence. This is not an
extrapolation from passing knot examples.

This does not say that all these knots are identical, ribbon, slice, or
concordant. It also does not identify K_new with D01. Matching d² is the required
boundary-polynomial check, **not** the missing nonribbon certificate.

## 6. A four-dimensional shortcut is conditionally obstructed

Before trying to remove the genus of the correction surface, we tested its
fundamental group map under the saved algebraic q0. This is an additional result,
not an identification of q0 with the actual disk-exterior inclusion.

Tietze elimination of the nine-generator source presentation leaves a
2-generator, 1-relator presentation (the second retained relator is cyclically
redundant). Reidemeister–Schreier rewriting with meridian x5 gives a relator in
levels -2 through 2, with each extreme occurring once. Its translates eliminate
all Schreier generators outside levels -1,0,1,2, with no remaining relations.
The source commutator subgroup is consequently free of rank four. The high-level
and low-level eliminations partition the translated relators and terminate,
which is the reason this is more than testing finitely many relators.

The images of A,B,b generate a subgroup whose folded graph has 16 vertices,
18 unoriented edges and rank three. It follows that the homomorphism

```
pi1(S)=F(A,B,b) -> source group
```

is injective: its image is free of rank three, and a surjection F3 to a free group
of rank three is an isomorphism (free groups are Hopfian). Equivalently the graph
folds preserve rank and the final labelled immersion is π₁-injective.

The independent subgroup checker replays the Tietze changes, the free-kernel
normal forms and the graph computation, with dependent and independent generator
controls. All nine source relators are checked.

**Conditional geometric conclusion:** if q0 is the geometric disk-exterior
inclusion for these markings, this particular surface has no compression disk,
since no essential loop on it is nullhomotopic in that exterior. Changing the
handle basis does not fix this. The statement is local to this surface and this
map. It does **not** exclude a separate immersed or embedded annulus between a
and b', which is the object Park's construction needs. In particular, the
correction surface connects b^- to b', not a to b'; these are different tasks.

## 7. Controls, failures and coverage

Completed independent exact replay includes the 675 crossings, native axis words,
preferred longitudes, all 670 Fox pivots, all five filled minors and all 375
auxiliary Tietze eliminations. Positive controls include the unlink and Hopf-link
peripheries. Negative tests reject a wrong framing, altered longitude, altered
Alexander polynomial and altered pivot sign. Separate mesh and subgroup checks
use different algorithms from their producers.

Preserved failures are not mathematical exclusions:

- `attempt01`: a routing turn created five unwanted surface intersections.
- `attempt02`: a planar orientation error invalidated the requested signed words.
- The first independent group replay dropped an unconstrained free generator
  from its substitution dictionary. It failed loudly; the dictionary was fixed
  to preserve every generator. The final replay passes. No target conclusion
  relies on the failed version.
- The bounded full *filled* group simplification produced no completed result
  before the external execution timeout. `filled_group_certificate.json` is
  TIMEOUT_UNKNOWN, not an identification or exclusion.
- A plotting write-permission failure was fixed; it was not a mathematical test.

This session did not recompute ordinary s, HKL, knot Floer homology, Jones
satellites, or the knot census. No knot table or hyperbolic identification was
obtained. The original stored K0/K1 theorem-to-diagram dependencies and the q0
geometric dependency were not closed here.

## 8. Exact remaining implication and next action

K_new is now concretely specified in S³, with a physically realized whole
correction, an auxiliary unlink certificate and the required exact polynomial.
The missing pieces are an identification with a knot carrying a global nonribbon
proof, plus an actual modifying annulus in the specified disk exterior satisfying
the standard-B⁴ hypotheses. Neither is supplied by the surface S or by E=0.

**Most valuable next action:** extract a marked unlink isotopy or explicit
spanning disks for this certified auxiliary pair and carry out the two Rolfsen
twists while transporting R. This gives an ordinary diagram of the actual filled
knot, enabling the nonribbon criterion to be checked on the correct object before
expensive Whitney-disk work. Preserve the concrete polygon and peripheral
certificates while doing so; do not restart a word or band census.

## Primary sources and exact usage

- Michael Freedman and Martin Scharlemann, *Dehn's Lemma for Immersed Loops*,
  arXiv:1704.05507v2, 15 September 2017. Theorem 1 and consequence (1), first page:
  a nullhomotopic simple boundary curve of a 3-manifold bounds a properly embedded
  disk. Used for the explicit peripheral unlink certificate. HTML and parsed PDF
  checked; the screenshot tool failed. https://arxiv.org/html/1704.05507v2
- JungHwan Park, *A Construction of Slice Knots via Annulus Modifications*,
  arXiv:1512.00401, originally December 2015. Definition 3.1 and Theorem 3.3:
  l-standard annulus modification has the standard-B⁴ conclusion. Used to state
  the exact outstanding geometric requirement, **not** invoked as an established
  sliceness theorem for the new link. https://arxiv.org/html/1512.00401
- Rob Schneiderman, *Algebraic linking numbers of knots in 3-manifolds*,
  Algebraic & Geometric Topology 3 (2003), 921–968, Proposition 4.1.2 and the
  surrounding annulus/Whitney discussion. Checked during this turn as background
  for why primary cancellation is not a clean Whitney-disk construction; no
  classification theorem for a general disk exterior is used.
  https://msp.org/agt/2003/3-2/agt-v3-n2-p10-p.pdf
- John R. Stallings, *Topology of finite graphs*, Inventiones Mathematicae 71
  (1983), 551–565, DOI 10.1007/BF02095993. Bibliographic identification only; the
  original PDF was not obtained. The finite-graph result used here is given by
  the direct fold/rank argument and explicit checker, not attributed to a
  newly verified theorem number from that paper.
