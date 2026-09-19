# Session 0 — the Foxy battlefield

Cutoff: 2026-08-30. This report optimizes for correctness, not excitement.

> **Superseded in part on 2026-09-11.** See `ERRATA_2026-09-11.md` and `CAMPAIGN_PLAN.md`. Door 4 (Turaev π³ form) is **closed**: Theorem H obstructs only homotopy-ribbonness. Door 1's completeness lemma is real but is **not** supplied by Agol–Ren [S09]; it is the open question stated by Meier–Zupan [S15]. Two lanes missing from this map were added: Miyazaki cables (route B, live member (10_17)_{2,1}) and the r = 0 RBG pairs (route-A generator).

## Binding result

**NO CE.** No explicit knot was verified to be both smoothly slice in the standard (B^4) and rigorously non-ribbon.

The battlefield is much narrower than the initial reconnaissance suggested:

1. The leading certified candidate is (K_{DG}=18_{nh}00000601). Oliveira-Smith proves it smoothly slice in standard (B^4) and fibered handle-ribbon [S01]. Its ribbon status remains unknown.
2. The fixed GST Figure 2 band sum (B_{3,1}) and broader fixed-band GST family are certified smoothly slice [S04], but their handle origins make homotopy-ribbon attacks logically irrelevant.
3. Abe–Tagami’s (K_n=A_n(6_3)) construction produces signed differences already proved non-ribbon, but smooth sliceness is unknown. The exact prerequisite is a smooth-concordance collision between distinct members [S06,S07].
4. Hom–Park supplies new explicit algebraically slice non-ribbon knots [S08], not smooth slice knots.
5. Dunfield–Gong’s large census leaves no unexamined pile of certified small slice escapees: among their suspicious set, every object except `DG` eventually received a ribbon disk; non-discovery for `DG` remains evidence, not proof [S03].

## Battlefield map

| lane | smooth slice in standard (B^4) | non-ribbon | exact weaker status | verdict |
|---|---:|---:|---|---|
| `18nh00000601` | proved [S01, Cor. 1.1.1] | unknown | fibered handle-ribbon [S01, Thm. 1.2] | **PRIMARY CANDIDATE** |
| GST (B_{3,1}) | proved [S04, §8] | unknown | explicit handle/belt-sphere disk [S04,S05] | **LIVE** |
| general fixed GST (B_{n,k,b}) | proved after fixing (b) | generally unknown | handle-theoretic disk | **LIVE, too broad until fixed** |
| Abe–Tagami (K_n\#(-K_m)) | unknown | proved for distinct permitted pair [S06,S07] | fibered connected sum | **WEAK/LIVE** |
| Hom–Park Cor. 1.3 sums | unknown | proved [S08] | algebraically slice | **WEAK/LIVE** |
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

### 4. Turaev π³ form on one fixed certified target

**OBJECT:** First `DG`; if surface data prove unusable, fixed GST (B_{3,1}).

**RIBBON NECESSITY:** Turaev [S20, reported Theorem H] is described in the primary abstract as a ribbonness obstruction from the multiplace π³ Seifert form.

**CURRENT STATUS:** Not computed. The exact theorem statement/hypotheses were not recovered to primary-text standard, so this door begins with source verification.

**GAP:** Obtain and formally restate Theorem H; prove its invariance/necessity hypotheses for the chosen surface; calculate the form and show the ribbon condition fails.

**WHY FINITE:** For a fixed finite surface-group presentation, nilpotent quotients and Milnor residues are exact finite algebra once the theorem specifies the quotient and choices.

**KILL CONDITION:** Theorem H turns out only to obstruct a property already satisfied, its hypotheses fail, or the computed obstruction vanishes.

**CE CONSEQUENCE:** A verified ribbon obstruction on `DG` or (B_{3,1}), combined with [S01] or [S04], gives a CE.

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
| 1 | DG fibered reduction | highest | high | high conditional on one clean lemma | identifies whether fibered technology can ever separate ribbon/handle-ribbon |
| 2 | DG derivatives | high | high | medium | maps exact derivative orbit complexity |
| 3 | GST normalization | high | medium | medium conditional | resolves the logical relation between Property R and a fixed ribbon question |
| 4 | Turaev π³ | uncertain until source recovery | high after recovery | medium | definitively classifies an allegedly neglected weapon |
| 5 | Abe–Tagami collision | exact but sliceness-side | high | finite for any proposed concordance | modern concordance computations kill pairs cleanly |

## Best first strike

Attack Door 1, but split it into a theorem task before computation:

> Determine whether every ribbon disk of the specific fibered knot `18nh00000601` is represented by the finite monodromy-compression list of [S09].

Without that completeness lemma, computation cannot prove non-ribbonness. With it, the campaign becomes a finite, certificate-driven unlink-derivative audit.
