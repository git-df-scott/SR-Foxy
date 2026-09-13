# Marked annuli: exact obstructions and a revised constructive target

13 September 2026. **No counterexample found.** This note supersedes the earlier recommendation to simplify the fixed annulus-twist trace relative to its annulus, and the recommendation to prioritize J149. It does not supersede the earlier input data or successful computations.

## Question and proof obligations

The audited difference K₁ # (−K₀) is nonribbon, where K₀=6₃ and K₁ is the stored Abe–Tagami annulus twist. A smooth disk in standard B⁴ would complete a counterexample. No such disk is known here. We tested two proposed constructions: modifying the standard product disk for K₀ # (−K₀), and removing the extra topology of the fixed two-handle surgery trace while preserving its annulus.

**New results:** an exact SL(2,F₅) certificate obstructs the first construction; a group calculation and a duality argument obstruct the second. Both are local to the specified constructions. An alternative construction for the same endpoints remains possible.

## 1. Which complement and which curves?

Remove a small ball meeting K₀ in a trivial arc, away from the surgery circles. Write the remaining knotted arc as α in B³. The product disk is D=α×I in B³×I, with boundary K₀ # (−K₀). Its exterior is (B³ minus ν(α))×I, and its group is G(K₀). Inclusion from either end ball induces an isomorphism. This also follows from the product-disk construction in Meier–Zupan [S3, §2.1].

Let L=K₀ ∪ c₁ ∪ c₂ be the saved 27-crossing input. Its cusp order is explicitly recorded in the input card. Filling both surgery-circle meridians with slope (1,0) restores the K₀ exterior. In that restored manifold, the old longitudes of c₁,c₂ represent their core curves, up to conjugation. Thus they give precisely the free homotopy classes needed for a modifying annulus in the product-disk exterior. Both stored PD fields are identical.

The group presentation/peripheral extraction uses SnapPy 3.3.2. Original geometric presentations, simplified presentations, generator maps, peripheral words, triangulations, seeds, and input hashes are preserved. This is a computer-assisted identification with the marked diagram, not a formally verified topology implementation.

## 2. A small exact certificate

The seed-0 presentation is G(K₀)=⟨a,b | r⟩, with capitals denoting inverses:

```
r = aabbbaBAABabbbaabABBBAb
u = BabA
v = BBABabbbaBABabbbaBAA
```

Here u,v represent c₁,c₂. Map the generators to SL(2,F₅):

```
        [0 1]          [0 2]
a  ->   [4 2]    b ->  [2 3]
```

The relator evaluates to the identity, and

```
        [2 2]          [4 3]
u  ->   [1 4]    v ->  [3 0].
```

Their traces are 1 and 4 modulo 5; their orders are 6 and 3. Trace is invariant under conjugation and, in SL(2), under inversion. Consequently u is conjugate to neither v nor v⁻¹ in G(K₀). The images generate all 120 elements of SL(2,F₅); surjectivity is checked, although not needed for the obstruction.

**Conclusion.** There is no continuous annulus in the product-disk exterior with boundary the specified two circles, in either orientation. In particular, there is no smoothly embedded annulus satisfying Park's disjointness condition for this disk [S2]. The argument is stronger than failure of a bounded geometric search.

This does not obstruct smooth sliceness of K₁ # (−K₀). A different disk for K₀ # (−K₀), or different modifying circles, changes the problem.

### Scope extensions and controls

1. The same obstruction applies to the integer twist-product disks Dₙ. The diffeomorphism (x,t)↦(rotation through 2πnt of x,t) fixes the end balls pointwise at t=0,1. Therefore the two marked circles have unchanged group images when transported to the product exterior. This is an explicit family of disk changes that does not help.
2. Put copies c₁⁺,c₂⁺ and c₁⁻,c₂⁻ in the two end balls. Cross-type annuli are obstructed as well: the inclusion from each end identifies the corresponding classes with u and v, up to orientation and conjugation. An annulus pairing must match c₁ with c₁ and c₂ with c₂.
3. The obvious matching product annuli cᵢ×I pass this necessary test. Applying matching product modifications that leave a standard product ambient ball yields another doubled knotted arc, hence a ribbon boundary J # (−J). This is a positive control and a warning against that specific construction, not a classification of all possible mixed-circle operations.
4. The trace search over SL(2,F₂) and SL(2,F₃) found no unequal-trace witness. Those are finite negative searches, not proofs of conjugacy. The F₅ witness is the decisive positive certificate.

## 3. The fixed surgery trace has cyclic complement group

Let W be obtained from S³×I by attaching the two 2-handles along c₁,c₂ with integral framings 2,0, and let C be the unchanged K₀ cylinder in W. Its outgoing boundary is K₁. The handle intersection matrix is [[2,1],[1,0]], equivalent over Z to the hyperbolic form. This alone says nothing about splitting the handles away from C.

The exterior E=W minus ν(C) is obtained from the K₀ exterior times I by adding the same 2-handles. Van Kampen therefore gives

π₁(E) = G(K₀) / normal-closure(u,v).

In the compact presentation, u=b⁻¹aba⁻¹ is a commutator of the two generators. Killing u makes a and b commute. The exponent sums of r are (2,3), while both u and v have exponent sums (0,0). Thus

π₁(E) ≅ ⟨a,b | [a,b], a²b³⟩ ≅ Z.

This is a reduction of the full group presentation, not just an abelianization calculation. The meridian-normalized map sends a↦−3 and b↦2.

### Lemma: cyclic-group concordance exteriors force trivial Alexander polynomials

Let X be the exterior of a concordance between knots J and K in standard S³×I, and suppose π₁(X)=Z. Then Δ_J=Δ_K=1 up to the usual units.

Here is the needed rational-coefficient proof. Set Λ=Q[t,t⁻¹], a PID, and use the meridian coefficient system.

* X is a homology circle. In a finite cellular chain complex, the rank of each differential over Q(t) is at least its rank after t=1. Since H₂(X;Q)=0, H₂(X;Λ) is Λ-torsion.
* The infinite cyclic cover is the universal cover, so H₁(X;Λ)=0. The universal coefficient sequence gives H²(X;Λ)=0: Hom of the torsion H₂ into Λ is zero, and Ext of H₁ is zero.
* Poincaré–Lefschetz duality, with the coefficient involution understood, gives H₂(X,∂X;Λ)=0. The pair exact sequence then gives H₁(∂X;Λ)=0.
* The boundary consists of the two knot exteriors joined through T²×I. Mayer–Vietoris identifies its Alexander module with A_J ⊕ A_K. The longitude maps to zero in each knot Alexander module; the H₀ map from the joining torus is injective. Thus A_J=A_K=0. Since knot Alexander polynomials are primitive, triviality over Q[t,t⁻¹] forces each polynomial to be a unit over Z[t,t⁻¹].

This is a derivation in this note, not an attributed new theorem. It is consistent with the usual cyclic-group slice-disk restriction discussed by Powell [S5].

### Consequence: the proposed relative destabilization is impossible

Removing an interior punctured S²×S² summand disjoint from C and filling its S³ boundary with B⁴ preserves the exterior's fundamental group: both replaced pieces are simply connected and the gluing sphere is simply connected. It would leave π₁=Z. If the resulting ambient manifold were standard S³×I, the lemma would force Δ_K₀=Δ_K₁=1. Instead both are

Δ(t)=t⁴−3t³+5t²−3t+1.

Therefore this operation cannot turn the fixed trace annulus into a concordance in standard S³×I. Its extra topology is essential relative to that annulus. This does not forbid changing the annulus by an operation that changes its complement group.

There is an instructive endpoint control: at n=−1 the analogous integral trace has the same attaching circles, hence the same cyclic exterior group, but K₋₁=K₀. Its fixed trace still cannot be destabilized in this fashion, although its endpoints certainly admit the product concordance. This explicitly prevents interpreting our local obstruction as nonconcordance of the endpoints.

## 4. What the ordinary intersection matrix was hiding

There is a sharper algebraic explanation. E has the homotopy type of a finite 2-complex, because a knot exterior has a 2-dimensional spine and we add two 2-handles. Over Λ, H₂(E;Λ) is free of rank two: H₀ and H₁ have Q(t)-rank zero, and χ(E)=2. Its equivariant intersection map is a map between rank-two free Λ-modules.

The boundary Alexander module is A_K₀ ⊕ A_K₁, of order Δ(t)². Its homology over Q(t) vanishes, so H₂(∂E;Λ) is torsion and maps trivially into free H₂(E;Λ). Duality and the universal coefficient theorem identify H₂(E,∂E;Λ) with the dual of H₂(E;Λ), since H₁(E;Λ)=0. The pair sequence therefore identifies the cokernel of the intersection map with A_K₀ ⊕ A_K₁. Consequently its determinant is Δ(t)² up to a nonzero rational Laurent unit.

This determinant is **deduced**, not obtained by constructing an explicit intersection matrix. Its nonunit status precludes a hyperbolic, unimodular form over Λ. At t=1, however, Δ(1)²=1, explaining why the ordinary integral matrix missed the obstruction.

The independent Fox calculation from r gives

```
∂r/∂a  ->  t^-3 (t+1) Δ(t)
∂r/∂b  ->  t^-6 (t²+t+1) Δ(t).
```

The two additional factors are coprime because (t²+t+1)−t(t+1)=1. This independently recovers the input Alexander polynomial from the saved group presentation. The normalized coefficients of Δ² are [1,−6,19,−36,45,−36,19,−6,1].

## 5. A constructive direction that escapes these particular failures

**Proposal, not a geometric result:** change the modifying circles themselves by band-summing components across the two summands. Aim for a new pair η₁,η₂ whose based words are uv and vu. These words are conjugate for an explicit reason:

u⁻¹(uv)u = vu.

This suggests bands joining c₁⁺ with c₂⁻ to form one new circle and c₂⁺ with c₁⁻ to form the other. These are band sums creating new circles, not the cross-type annuli already ruled out. Based paths and orientations determine the actual words; arbitrary bands need not realize the proposed words.

The 54-crossing, five-component marked input is saved in `data/knots/AbeTagami_marked_product_scaffold.json`. Its construction, component identities, planarity, PD roundtrip, and linking matrix are checked. It is explicitly labelled an input scaffold, not a candidate. No mixed bands or modifying annulus have yet been certified.

The next experiment must pass four gates in order:

1. Specify actual band paths and verify their words in the product-disk group. Reject an unintended nonconjugate pair immediately.
2. Identify the two-component surgery link, including framings. Conjugacy alone does not imply that the link bounds a standard annulus.
3. Determine the boundary surgery result. Seek an asymmetric, distinct pair covered by the existing nonribbon theorem. A new slice knot without a global nonribbon obstruction is not success, and another J # (−J) is a ribbon control.
4. Construct an embedded annulus disjoint from the disk and certify the ambient standardness required by Park's theorem. Standardness may be proved by an isotopy that crosses the disk; disjointness of the actual modifying annulus is a separate requirement.

This ordering prioritizes cheap rejection before difficult smooth geometry. There is no proof that the proposed bands can pass the gates.

## 6. Reproduction, failures, and priority correction

Run from the repository root:

```
../knot-venv/bin/python scripts/annulus_group_certificate.py
../knot-venv/bin/python scripts/annulus_group_certificate.py --seeds 0 --output results/annulus_group_compact.json
python3 scripts/check_annulus_group_certificate.py --output results/annulus_group_check.json
python3 scripts/check_annulus_group_certificate.py results/annulus_group_compact.json --output results/annulus_group_compact_check.json
python3 scripts/trace_complement_audit.py
../knot-venv/bin/python scripts/build_marked_product_scaffold.py
```

Four triangulation seeds agree on traces 1,4 and orders 6,3. The standalone checker uses a different matrix multiplication implementation and no SnapPy import. It checks all original relators (11 or 13), simplified relators, both generator maps in the finite representation, and simultaneous conjugacy of each original/simplified meridian-longitude pair. It enumerates conjugacy directly and includes a conjugated-word positive control. The source link/group identification still shares SnapPy across the runs.

An initial checker incorrectly required literal equality of peripheral images after presentation simplification. SnapPy peripheral words are only specified up to conjugation. Inspection found an explicit simultaneous conjugator for each pair; the checker was corrected to require that invariant condition. No unequal-trace conclusion changed. Tampered trace, matrix, and displayed-word records are rejected. An exploratory import omission and a relative-output-path error were also corrected; neither was a mathematical negative result. Numerical holonomy was used only to nominate the test, never as proof.

The initial scaffold used the generic connected-sum helper, whose cuts need not correspond under the mirror map. It was replaced by an explicit corresponding-endpoint gluing with the auxiliary-component orientations preserved. The final component order is R,c1_upper,c2_upper,c1_lower,c2_lower, with Hopf linking numbers +1 above and −1 below. This preserves the intended product construction instead of relying on an unmarked connected-sum identification.

**J149 correction:** the unnumbered claim after Question 1.15 in Agol–Ren [S4] excludes a fibered common upper bound for distinct minimal hyperbolic knots of input genus at most three. Raising the target genus does not evade that claim. Its proof has not been independently reconstructed here, so retain it as a strong priority warning, not a certified computational rejection. Older notes naming J149 as the best target are superseded on priority.

## Sources checked 12–13 September 2026

- **S1:** Tetsuya Abe and Keiji Tagami, *Fibered knots with the same 0-surgery and the slice-ribbon conjecture*, arXiv:1502.01102v5, initially 2015. Corollary 4.3 and the fixed annulus-twist family supply the nonribbon criterion and inputs. https://arxiv.org/html/1502.01102v5
- **S2:** JungHwan Park, *A construction of slice knots via annulus modifications*, manuscript 18 November 2015; arXiv:1512.00401. Definition 3.1 and Theorem 3.3 in this manuscript specify standard annuli and the standard-B⁴ conclusion. https://math.rice.edu/~jp35/1.pdf
- **S3:** Jeffrey Meier and Alexander Zupan, *Knots bounding nonisotopic ribbon disks*, Journal of Topology 18(4), e70047, first published 26 November 2025. Section 2.1 defines the product and twist-product disks used here. DOI: https://doi.org/10.1112/topo.70047
- **S4:** Ian Agol and Qiuyu Ren, *Ribbon concordance of fibered knots and compressions of surface homeomorphisms*, arXiv:2603.10884v1, 11 March 2026. Unnumbered claim following Question 1.15 supports the J149 priority warning. https://arxiv.org/html/2603.10884v1
- **S5:** Mark Powell, *A Second Order Algebraic Knot Concordance Group*, author monograph manuscript. Introduction, printed p.3, discusses the restriction on cyclic slice-disk groups. The concordance lemma above is proved here rather than attributed to this discussion. https://www.maths.gla.ac.uk/~mpowell/Second_Order_Alg_Conc_Gp_AMS.pdf
- **S6:** SnapPy 3.3.2 documentation, *Manifold* and *Additional Classes*. Documents Dehn-filled group presentations, original generator maps, and peripheral curves up to conjugation. https://snappy.computop.org/manifold.html and https://snappy.computop.org/additional_classes.html

The new obstructions are not a counterexample and do not establish the conjecture. The highest-value next construction uses changed, explicitly marked surgery circles and must retain both a standard-B⁴ disk certificate and a global nonribbon theorem.
