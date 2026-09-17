# SR-Foxy: a fixed-axis conjugacy gate and the local-knotting limitation

**Status: NO COUNTEREXAMPLE.** This pass constructed no concordance and no slice disk. It obtained an exact, independently checked algebraic description of an existing construction obstruction, and derived its persistence under arbitrary interior local knotting of the starting disk. These are construction-level results, not obstructions to sliceness of D01. No claim of publication novelty is made.

Repository input was pinned to `b7ae7270ea6abc6976c0ec598067e2cac3602887`, the observed remote `main` at the start. Work took place in a separate Linux container, not the user's Mac. No branch was created; no repository or Mac files were modified; nothing was pushed. The attempted container download of a repository snapshot failed at DNS resolution. Subsequent reading used the authorized GitHub connector. This is not an exhaustive repository audit.

## 1. What was selected, and why

The selected problem was the actual marked-circle bottleneck in the annulus-modification proposal for the Abe–Tagami family. Reading `research/12`, `research/14`, `research/15`, and `research/20` established that the simplest product-disk construction and a relative destabilization of its fixed surgery trace had already been obstructed. Repeating either as a fresh construction would have been duplication.

The pivot was to extract more usable information from the marked group: determine exactly where abelian information loses the obstruction, provide a short exact nonabelian certificate, and test whether changing the starting disk by arbitrary local knotting could evade it. The answer to the last question is no, with the fixed-axis qualifications below.

The prior SL(2,F5) separation is not a new result. The free-by-cyclic rewriting, metabelian comparison, fiber-class-two certificate, and local-knotting retraction deduction were worked out in this pass. Their absence from all other repository files has not been established.

## 2. Inputs and the geometric dependency

The source is `research/14_marked_annulus_audit.md`, checked against the simplified presentation and peripheral words in lines 1–160 of `results/annulus_group_compact.json` at the pinned commit. Uppercase letters denote inverses:

```
G = < a,b | r >
r = aabbbaBAABabbbaabABBBAb
u = BabA
v = BBABabbbaBABabbbaBAA
mu = bba
```

The abelianization is `a -> -3`, `b -> 2`, so `mu -> 1` and both axes map to zero.

The upstream geometric interpretation is that G is the exterior group of the standard product disk for `K0 # (-K0)`, and u,v are the free homotopy classes of the fixed modifying circles. That interpretation still depends on the repository's marked diagram, peripheral extraction, and base-path audit. No independent SnapPy extraction from the PD was possible in this environment. The upstream PD hash in `inputs.json` is explicitly labeled reported, not recomputed.

A continuous annulus joining these circles in the disk exterior would make u conjugate to v or v inverse, depending on orientations. Thus a conjugacy obstruction is sufficient to reject this particular annulus construction. It does not reject every possible disk or concordance with the desired knot boundary.

## 3. Exact free-by-cyclic description

Set `t = b^2 a` and `x = b t^-2`. Then, already in the free group on a,b,

```
b = x t^2
a = t^-2 x^-1 t^-2 x^-1 t.
```

Let `x_i = t^i x t^-i`. Schreier rewriting of r, cyclic reduction, and an index shift give

```
R = x2^-1 x0^-1 x1 x2^-1 x1 x3 x2^-1 x3
    x4^-1 x2^-1 x3 x2^-1 x1.
```

Here x0 and x4 each occur exactly once. Solving `R=1` for x4 gives an endomorphism phi of the free group F on x0,x1,x2,x3:

```
phi(x0) = x1
phi(x1) = x2
phi(x2) = x3
phi(x3) = x2^-1 x3 x2^-1 x1 x2^-1 x0^-1
          x1 x2^-1 x1 x3 x2^-1 x3.
```

An explicit inverse is

```
phi^-1(x0) = x0 x1^-1 x0 x2 x1^-1 x2 x3^-1
             x1^-1 x2 x1^-1 x0 x1^-1
phi^-1(x1) = x0
phi^-1(x2) = x1
phi^-1(x3) = x2.
```

Both compositions freely reduce to the identity on each of the four generators; the checker verifies all eight identities. The original presentation, with the definitions of t and x added, can therefore be Tietze-transformed into the mapping-torus presentation

`G = F4 semidirect_phi Z`, with `t x_i t^-1 = phi(x_i)`.

To see that this is an isomorphism rather than a quotient, introduce x0 through x4 by their conjugate definitions, replace r by its conjugate R, eliminate x4 using its single occurrence, and use the verified inverse of phi. This leaves precisely the presentation of the stated semidirect product. Its meridian kernel is free of rank four. Since the original abelianization is Z, that kernel is G'.

On the abelianization of F4, phi has column matrix

```
M = [ 0  0  0 -1 ]
    [ 1  0  0  3 ]
    [ 0  1  0 -5 ]
    [ 0  0  1  3 ].
```

Its characteristic polynomial is

`Delta(t) = t^4 - 3t^3 + 5t^2 - 3t + 1`.

No root of this polynomial lies on the unit circle. Indeed, writing `z=t+t^-1`,

`Delta(t)/t^2 = z^2-3z+3 = (z-3/2)^2 + 3/4`,

which is positive when |t|=1, because z is then real. Consequently, for every nonzero integer k, both `M^k-I` and `M^k+I` are invertible over C. This is an all-integer argument, not a bounded numerical search over conjugator powers.

## 4. The two axes: metabelian agreement but actual nonconjugacy

After removing conjugating prefixes in their Schreier words and conjugating by powers of t, the axes have representatives

```
U = x0^-1 x1
V = x1^-1 x2 x3^-1 x0^-1 x1 x2^-1 x1 x3.
```

The index shifts are +6 and +8, respectively. Each representative is conjugate to its own original axis in G. Both have the same nonzero fiber abelianization

`w = (-1,1,0,0)`.

Any conjugator in G can be written as `h t^k`, with h in F4. If it conjugated U to V, abelianizing in the fiber would give `M^k w=w`. Section 3 forces k=0. Thus it would have to be a conjugacy in the free group F4. But U and V are cyclically reduced, with lengths 2 and 8. Conjugate cyclically reduced words in a free group have the same cyclic length. They cannot be conjugate.

For conjugacy to the inverse, the necessary equation is `M^k w=-w`. For k nonzero this is impossible by Section 3; for k=0 it is impossible because w is nonzero. Thus neither orientation works.

### A smaller nonabelian quotient also detects the failure

Use the class-two nilpotent quotient of the **fiber subgroup**, `N=F4/gamma_3(F4)`, and retain the semidirect Z action. The total quotient `N semidirect Z` is not being claimed nilpotent. This is not the ordinary class-two nilpotent quotient of the entire knot group.

Write normal forms as powers of x0,x1,x2,x3 followed by central commutators `[xi,xj]=xi xj xi^-1 xj^-1`, in pair order 01,02,03,12,13,23. The central coordinates are

```
U: ( 0, 0, 0, 0, 0, 0)
V: (-1, 1,-1,-1, 2,-1).
```

Conjugating an element of fiber abelianization w by an element of abelianization z changes its ij coordinate by `z_i w_j-z_j w_i`. Since w2=w3=0, the 23 coordinate is unchanged. Its values 0 and -1 therefore obstruct fiber conjugacy already at this level. The preceding monodromy argument still excludes all nonzero powers of t.

An independent implementation multiplies truncated noncommutative Magnus expansions, using `xi -> 1+Xi` and `xi^-1 -> 1-Xi+Xi^2`. It gives coefficients of X2 X3 equal to 0 and -1, and coefficients of X3 X2 equal to 0 and 1. The Malcev and Magnus implementations agree on all 4,681 words of length at most four over the eight signed generators. Those are arithmetic controls, not searches through knots or surfaces.

### Why Alexander-level checking misses this example

The abelianized Fox vectors satisfy the exact Laurent-polynomial identity

`Fox(v) = t^-2 Fox(u)`.

Conjugation by `b^-1` has precisely this action on the meridian-kernel abelianization. Thus the original u,v are conjugate in `G/G''`. Equivalently, the normalized U,V have the same image in the abelianized fiber. This does not imply that every metabelian invariant or every HKL test in the project is useless; it concerns this particular conjugacy test on these two fixed marked loops.

The existing finite certificate was also rechecked independently: the prescribed a,b matrices in SL(2,F5) satisfy r, generate 120 elements, and give axis traces 1 and 4. Trace remains unchanged on inversion. This reproduces, rather than upgrades, the prior construction obstruction.

## 5. New geometric deduction: local knotting cannot repair the fixed axes

**Retraction lemma.** Suppose a disk exterior E has two marked loops u,v that are not conjugate, even after inversion. If a modified exterior E* admits a homomorphism

`rho: pi1(E*) -> pi1(E)`

that sends its marked loops to the original marked loops, up to their appropriate base-path conjugacies, then those marked loops cannot cobound a continuous annulus in E* either.

**Proof.** Applying rho to a hypothetical conjugacy in pi1(E*) would produce the forbidden conjugacy in pi1(E). The orientation-reversed case is identical. This does not need rho to arise from a geometric map or require injectivity of the boundary group.

**Application to interior local knotting.** Let D* be obtained by taking the local connected sum of D in its interior with any smooth 2-knot S in standard S4, keeping the boundary and marked circles fixed. Let H be the 2-knot exterior group. Van Kampen gives

`pi1(E(D*)) = G *_{<mu>} H`,

where the meridians are identified with compatible orientation.

For completeness, remove a small ball meeting D in a trivial disk. The overlap of the old and replacement disk exteriors is the solid torus exterior of the boundary unknot. Restoring the original trivial disk glues in a group Z by an isomorphism on this overlap. Therefore the punctured old exterior has group G. The punctured 2-knot exterior similarly has group H. Gluing them produces the stated meridian amalgam.

The abelianization `epsilon_H:H -> Z` sends the oriented meridian to 1. Define rho to be the identity on G and

`rho(h)=mu^(epsilon_H(h))` for h in H.

These homomorphisms agree on the amalgamated meridian, so they extend to a retraction onto G. Reversing the meridian convention simply reverses the exponent on H. The retraction lemma now applies.

**Conclusion.** The fixed original twisting circles cannot cobound a disjoint annulus after *any* interior local knotting of the standard product disk, or after any finite sequence of such operations. This is an unbounded family of excluded repairs, conditional on the upstream marked-group identification. It is not a finite search result.

The same group argument applies to separate boundary-connected disk summands when the marked circles remain in the original factor and the exterior is the corresponding meridian amalgam. This does **not** exclude the Teichner route: a different disk with genuinely mixed geometry need not have this retraction. No blanket statement about arbitrary ribbon stabilizations follows.

The limitation does not cover nonlocal disk changes, new modifying circles, or operations that change the marked images so that the stated retraction condition fails. It does not obstruct a concordance between K0 and K1.

## 6. Comparison with two KDG obstruction directions

**Ribbon-pattern Jones tests.** Eisermann's Proposition 6.13 supplies the ribbon-preserving implication for a pattern whose image on the unknot is ribbon. Theorems 1 and 2 then give nullity and determinant-congruence necessities for the resulting link. The paper asks, rather than proves, whether these extend to all slice links (Question 7.1), and separately discusses boundary-link automaticity. I verified no theorem forcing all such tests to pass on every smooth slice knot, but also no pattern giving a violation on KDG. The existing three-parallel result is a pass, not a new run here. A nonparallel pattern would require a specified ribbon control and an actual calculation. That was not a better-defined bottleneck for this pass than the marked annulus group.

**Global unlink-derivative exclusion.** Miller–Zupan Proposition 1.1 characterizes ribbonness by existence of an unlink derivative on some Seifert surface; Theorem 1.3 gives the weaker R-link-derivative characterization of handle-ribbonness in a homotopy ball. Therefore a valid global exclusion must rule out every possible unlink derivative, not merely the exhibited R-link derivative or a bounded curve list. Their proposition does not assert that smooth sliceness supplies an unlink derivative. KDG's handle-ribbon disk is already supplied by Oliveira-Smith Theorem 1.2, so obstruction tools that only disprove handle-ribbonness cannot work on the correctly identified knot. No global derivative exclusion was obtained here.

These comparisons do not claim that either entire direction is impossible.

## 7. Counterexample dependencies and the next action

For the intended Abe–Tagami pair, Corollary 4.3 supplies the signed nonribbon implication when the distinct fibered knots and irreducible Alexander-polynomial hypotheses are matched to the exact diagrams. I checked the paper's statement and annulus-presentation figures, not an independent complete diagram identification. That remains a final-certificate dependency.

The stabilization implication is sound: if J and D01#J have ribbon disks in standard B4, then both are smoothly slice, so `[D01]=[D01#J]-[J]=0` in smooth concordance. The required two disks were not found. There is no inconsistency in seeking a ribbon disk for the stabilized knot while D01 itself is nonribbon.

For KDG, Oliveira-Smith's Corollary 1.1.1 identifies `18nh00000601` as slice in standard B4; this pass checked the statement and its dependence on standardizing the sphere, but did not independently replay all Kirby moves.

**Exact unresolved step:** a smooth concordance K0 -> K1 in standard S3 x I (or an equivalent standard-B4 slice disk for D01). For KDG the missing step remains global nonribbonness.

**Single next action:** audit one concrete changed-axis construction from Opus before any broad continuation search. Require the marked surgery link with actual band paths, oriented framings, and the resulting boundary knot. Check its based words against a disjoint-annulus claim. The algebraic suggestion `uv` versus `vu` already in research/14 passes free conjugacy automatically, but is not a geometric construction. A successful gate must then be followed by the actual embedded annulus and standard-ambient proof. If Opus instead keeps the original axes and merely locally knots the product disk, the lemma above rejects that repair without a new search.

## 8. Reproduction and limits

Run from this artifact directory, selecting a new output filename:

```
python3 verify_annulus_gate.py --output rerun.json
```

The checker is standard-library-only, deterministic, and refuses to overwrite results. It uses exact integers, free reductions, Laurent polynomials, finite matrices, and two independent implementations of the class-two arithmetic. The saved main run passed 44 named checks and 4,681 short-word arithmetic controls in about 0.22 seconds. No long-running process remains.

This is not a formal proof-assistant verification. It is an explicit human-checkable algebraic argument with reproducible exact calculations. The local-knotting result is proved by van Kampen and a retraction, not established by testing finitely many 2-knots. Source extraction, knot identification, smooth embedding, framing, boundary identification, and ambient standardness are separate obligations.

No Jones, HFK, HKL, s-invariant, band-frontier, or branched-cover search was repeated. Large generated frontier archives were not inspected programmatically in this pass; no coverage claim is made about them. See `coverage.json` for the actual reading scope.

## Sources used, with scope

1. Tetsuya Abe and Keiji Tagami, *Fibered knots with the same 0-surgery and the slice-ribbon conjecture*, arXiv:1502.01102 (2015), accessed 17 September 2026 UTC. Appendix A, Theorem 4.1 and Corollary 4.3; Appendix B, Figures 4–5 and Lemma 5.7. Used for the intended nonribbon criterion and annulus presentation, not a claimed concordance. https://arxiv.org/pdf/1502.01102
2. JungHwan Park, *A Construction of Slice Knots via Annulus Modifications*, arXiv:1512.00401v1 (1 December 2015), accessed 17 September 2026 UTC. Definitions 2.1 and 3.1; body Theorem 3.3. A disjoint modifying annulus and the specified standardness conditions are required. The introduction and body have inconsistent theorem numbering; the reference here is to body Theorem 3.3. https://arxiv.org/html/1512.00401v1
3. Michael Eisermann, *The Jones polynomial of ribbon links*, Geometry & Topology 13 (2009), 623–660, accessed 17 September 2026 UTC. Theorems 1–2; Proposition 6.13; Corollary 6.15; Example 6.16; Questions 7.1 and 7.8. Used only for the ribbon-specific necessities and their stated limitations; no assertion about resolution of those questions after the paper. https://pnp.mathematik.uni-stuttgart.de/igt/eiserm/publications/ribbonlinks.pdf
4. Trevor Oliveira-Smith, *A Dunfield–Gong 4-Sphere is Standard*, arXiv:2603.23717v1, arXiv submission 24 March 2026; displayed manuscript date 24 August 2026; accessed 17 September 2026 UTC. Theorem 1.1, Corollary 1.1.1, Theorem 1.2, Lemma 2.2. Preprint; exact knot identified in its abstract as 18nh00000601. The author has a hyphenated surname, not two separate authors Oliveira and Smith. https://arxiv.org/html/2603.23717v1
5. Maggie Miller and Alexander Zupan, *Equivalent characterizations of handle-ribbon knots*, arXiv:2005.11243v1 (22 May 2020), accessed 17 September 2026 UTC. Proposition 1.1 and Theorem 1.3. Used for the distinction between unlink derivatives and R-link derivatives, with the homotopy-ball qualification retained. https://arxiv.org/pdf/2005.11243
6. SR-Foxy, pinned commit as above: `research/14_marked_annulus_audit.md` and `results/annulus_group_compact.json`. Source of the exact group and marked words, not independently regenerated geometry. https://github.com/git-df-scott/SR-Foxy/blob/b7ae7270ea6abc6976c0ec598067e2cac3602887/research/14_marked_annulus_audit.md
