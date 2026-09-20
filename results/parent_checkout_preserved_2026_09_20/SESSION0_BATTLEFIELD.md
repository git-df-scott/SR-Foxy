# Session 0 — the Foxy battlefield

Cutoff: 2026-08-30. This report optimizes for correctness, not excitement.

## Binding result

**NO CE.** No explicit knot was verified to be both smoothly slice in the standard (B^4) and rigorously non-ribbon.

The battlefield is much narrower than the initial reconnaissance suggested:

1. The leading certified candidate is (K_{DG}=18_{nh}00000601). Oliveira-Smith proves it smoothly slice in standard (B^4) and fibered handle-ribbon [S01]. Its ribbon status remains unknown.
2. The fixed GST Figure 2 band sum (B_{3,1}) and broader fixed-band GST family are certified smoothly slice [S04], but their handle origins make homotopy-ribbon attacks logically irrelevant.
3. Abe–Tagami’s (K_n=A_n(6_3)) construction produces signed differences already proved non-ribbon, but smooth sliceness is unknown. The exact prerequisite is a smooth-concordance collision between distinct members [S06,S07].
4. Hom–Park supplies new explicit algebraically slice non-ribbon knots [S08], not smooth slice knots.
5. Dunfield–Gong’s Table 8 gives 24 knots rigorously obstructed from being topologically homotopy-ribbon, but none is known slice [S03]. The replication-data audit in `KDG_EXACT_AUDIT.md` found one with a recorded zero-friend, `19nh_001785287`; that friend is also slice-unknown [S23].

## Battlefield map

| lane | smooth slice in standard (B^4) | non-ribbon | exact weaker status | verdict |
|---|---:|---:|---|---|
| `18nh00000601` | proved [S01, Cor. 1.1.1] | unknown | fibered handle-ribbon [S01, Thm. 1.2] | **PRIMARY CANDIDATE** |
| GST (B_{3,1}) | proved [S04, §8] | unknown | explicit handle/belt-sphere disk [S04,S05] | **LIVE** |
| general fixed GST (B_{n,k,b}) | proved after fixing (b) | generally unknown | handle-theoretic disk | **LIVE, too broad until fixed** |
| Abe–Tagami (K_n\#(-K_m)) | unknown | proved for distinct permitted pair [S06,S07] | fibered connected sum | **WEAK/LIVE** |
| Hom–Park Cor. 1.3 sums | unknown | proved [S08] | algebraically slice | **WEAK/LIVE** |
| DG Table 8; first target `19nh_001785287` | unknown | proved [S03, Thm. 3.12] | not topologically homotopy-ribbon | **LIVE, SLICENESS-FIRST** |
| Abe–Tange (8_{20})-based family, (n\ge0) | proved | proved ribbon [S05] | ribbon | **CLOSED** |

## Central diagnosis

The best certified candidates survive because they are not merely slice. They already sit on the strong side of almost every classical “ribbon obstruction”:

\[
\text{ribbon}\Rightarrow\text{handle-ribbon}\Rightarrow\text{homotopy-ribbon}\Rightarrow\text{slice}.
\]

For `DG`, handle-ribbonness is a theorem. For GST, the slice-disk complement/handle presentation supplies the analogous structural reason. Consequently Casson–Gordon extension tests, π₁ epimorphism tests, metabelian restrictions and irregular-dihedral homotopy-ribbon bounds cannot prove non-ribbonness here. Classical Floer/gauge/lattice sliceness obstructions must vanish on the known disks.

The live distinction is the Miller–Zupan derivative gap [S02]:

| property | necessary and sufficient 3D datum |
|---|---|
| ribbon | an **unlink derivative** on some Seifert surface |
| handle-ribbon | an **R-link derivative** on some Seifert surface |

`DG` has the second datum. No theorem or complete calculation establishes or excludes the first.

## Ranked exact attack doors

### 1. `DG`: finite fibered-disk-to-unlink-derivative reduction

**OBJECT:** (K_{DG}=18_{nh}00000601).

**RIBBON NECESSITY:** Miller–Zupan [S02, Prop. 1.1]: every ribbon knot has an unlink derivative on a genus-(g) Seifert surface.

**CURRENT STATUS:** Smoothly slice and fibered handle-ribbon [S01]; an R-link derivative is explicit; no unlink derivative is known. [S09] gives finite enumeration of minimal monodromy compressions for fibered strong homotopy-ribbon predecessors, but not completeness for arbitrary ribbon disks.

**GAP:** Prove that every ribbon disk for this fibered knot is fibered (or directly that every unlink derivative is represented among the finite minimal compressions), then prove no enumerated derivative is an unlink.

**WHY FINITE:** The genus-five monodromy is explicit; [S09, Thm. 1.9 and Cor. 1.11] provide a finite compression enumeration up to symmetry. Each resulting surgery link can be checked by exact 3-manifold/link recognition.

**KILL CONDITION:** One explicit unlink derivative or ribbon band movie for `DG`; alternatively, failure of the ribbon-disk-to-fibered-disk reduction leaves this finite list non-complete and kills the proposed proof route.

**CE CONSEQUENCE:** By [S01, Cor. 1.1.1], exclusion of all unlink derivatives via [S02, Prop. 1.1] would make this explicit smoothly slice knot rigorously non-ribbon.

### 2. `DG`: global derivative-link obstruction

**OBJECT:** (K_{DG}) with the explicit genus-five fiber surface/handle diagram from [S01].

**RIBBON NECESSITY:** [S02, Prop. 1.1] requires an unlink derivative; Park–Powell [S17] supplies necessary triple-linking restrictions for specified homology-ribbon derivative systems.

**CURRENT STATUS:** No global derivative classification or Park–Powell calculation was found. A calculation on only the displayed R-link derivative cannot suffice.

**GAP:** Prove a finite completeness theorem for metabolizers/derivative systems on the fiber surface, and show each violates unlinkness (or a necessary derivative-link condition).

**WHY FINITE:** The Seifert matrix and surface group are finite explicit data; after a bound/classification of metabolizers, Milnor invariants and link recognition are exact computations.

**KILL CONDITION:** Infinitely many uncontrolled derivative orbits, a derivative satisfying all tests, or discovery of an unlink derivative terminates the lane.

**CE CONSEQUENCE:** Complete exclusion of unlink derivatives plus [S01] gives a CE.

### 3. GST Figure 2: normalize ribbon disks to GST handleslides

**OBJECT:** The exact Figure 2 band sum (B_{3,1}) of [S04].

**RIBBON NECESSITY:** [S02, Prop. 1.1] requires an unlink derivative.

**CURRENT STATUS:** Smoothly slice [S04]; handle/belt-sphere presentation explicit [S05]; ordinary ribbonness and associated unstabilized handleslide question unresolved. Stable results [S14] are inconclusive.

**GAP:** Prove the GST ribbon-completeness theorem formulated in `GST_AUDIT.md`: any unlink derivative/ribbon disk normalizes, without stabilization, to an ordinary handleslide trivialization of the associated framed GST link; then obstruct that trivialization.

**WHY FINITE:** Once normalization gives a bounded handle presentation, Kirby moves and resulting 3-manifolds can be certified combinatorially.

**KILL CONDITION:** An explicit ribbon disk/unlink derivative, or a proof of Abe–Tange Conjecture 6.1, closes the object/lane as ribbon. Failure of normalization kills the proposed bridge from Property R to ribbonness.

**CE CONSEQUENCE:** [S04] supplies the smooth slice disk; the necessity plus a nontriviality certificate would prove non-ribbonness.

### 4. Dunfield–Gong Table 8 trace standardization

**OBJECT:** `19nh_001785287` and its recorded 82-crossing zero-friend [S23].

**NON-RIBBON CERTIFICATE:** [S03, Theorem 3.12 and Table 8] proves that the base knot is not even topologically homotopy-ribbon.

**CURRENT STATUS:** The base and its recorded zero-friend are both smooth-slice unknown. It is the only one of the 24 Table 8 knots found in either zero-friend table [S23].

**GAP:** Reconstruct an exact zero-surgery homeomorphism/RBG link and standardize the associated trace sphere while tracking the base-knot cocore into a standard `B^4`.

**WHY FINITE:** The archive supplies finite PD/triangulation data for both knots. A proposed RBG certificate and Kirby slide movie can be checked by exact surgery recognition and handle calculus.

**KILL CONDITION:** A smooth-sliceness obstruction for either knot kills that trace route; inability to certify the numerical zero-surgery homeomorphism prevents promotion to a proof.

**CE CONSEQUENCE:** A standard `B^4` slice disk for the base, combined with the existing Theorem 3.12 obstruction, gives a CE immediately.

### 5. Abe–Tagami concordance collision

**OBJECT:** (D_{n,m}=A_n(6_3)\#(-A_m(6_3))), with (n\ne m) and (n+m\ne-1).

**RIBBON NECESSITY:** Miyazaki [S07, Thm. 5.5] as specialized in [S06, Cor. 4.3] forces the fibered summands of a ribbon signed sum to pair; the chosen distinct pair cannot.

**CURRENT STATUS:** Non-ribbon is proved; ([K_n]=[K_m]) and hence smooth sliceness is unknown.

**GAP:** Construct a smooth concordance between one permitted distinct pair.

**WHY FINITE:** A proposed concordance movie has a finite handle/Morse certificate; once verified, the signed sum yields an explicit slice disk and Miyazaki’s hypotheses are finite polynomial/primeness checks already carried out in [S06].

**KILL CONDITION:** Any smooth-concordance invariant distinguishing the selected pair kills it; pairwise distinction closes the family lane.

**CE CONSEQUENCE:** The concordance makes (D_{n,m}) smoothly slice, while [S06,S07] makes it non-ribbon.

## Ranking rationale

| rank | door | sharpness | auditability | finite path | learning if failure |
|---:|---|---|---|---|---|
| 1 | DG Table 8 trace | exact non-ribbon half | medium | finite after an exact RBG certificate | tests the only recorded zero-friend of a certified non-ribbon target |
| 2 | DG derivatives | high | high | medium | can explicitly ribbonize or sharpen the exact flagship gap |
| 3 | DG fibered reduction | high only after a missing completeness theorem | high | conditional | identifies whether fibered technology can separate ribbon/handle-ribbon |
| 4 | GST normalization | high | medium | conditional | resolves the logical relation between Property R and a fixed ribbon question |
| 5 | Abe–Tagami collision | exact but sliceness-side | high | finite for any proposed concordance | modern concordance computations kill pairs cleanly |

## Best first strike

Attack Door 4 first:

> Reconstruct and certify the zero-surgery homeomorphism between
> `19nh_001785287` and its recorded 82-crossing friend, then build the exact RBG
> trace diagram and try to standardize the resulting homotopy sphere while
> tracking the knot cocore.

This lane starts with rigorous non-ribbonness, so a successful standard trace
embedding ends the campaign. In parallel, the explicit Figure 9 R-link remains the
best way to try to ribbonize—and therefore eliminate—the current flagship.
