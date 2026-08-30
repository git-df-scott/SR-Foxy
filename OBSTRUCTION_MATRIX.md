# Ribbon-obstruction matrix

Allowed cell labels are used verbatim. Parenthetical notes explain the classification. A sliceness obstruction that must vanish on every smooth slice knot is not advertised as a ribbon obstruction.

Abbreviations: `DG` = (18_{nh}00000601); `GST` = fixed Figure 2 band sum (B_{3,1}); `AT` = (D_{n,m}=A_n(6_3)\#(-A_m(6_3))), distinct; `HP` = a Hom–Park Corollary 1.3 knot.

| obstruction / necessity | DG | GST | AT | HP |
|---|---|---|---|---|
| Homotopy-ribbon π₁ epimorphism | **APPLIES BUT VANISHES** (handle-ribbon [S01]) | **APPLIES BUT VANISHES** (exhibited handle exterior [S04,S05]) | **APPLIES AND OBSTRUCTS** (Miyazaki pairing theorem [S06,S07]) | **APPLIES AND OBSTRUCTS** under γ₀-sharp hypotheses [S08] |
| Fibered monodromy extension/compression | **APPLIES BUT VANISHES** (fibered handle-ribbon disk [S01,S02]) | **UNKNOWN** (fiberedness of the exact band sum not certified here) | **APPLIES AND OBSTRUCTS** through Miyazaki’s fibered theorem, not a computed compression | **APPLIES AND OBSTRUCTS** via [S08]’s fibered structure |
| Casson–Gordon invariants | **APPLIES BUT VANISHES** as homotopy-ribbon obstruction | **APPLIES BUT VANISHES** at the homotopy-ribbon level | **COMPUTED / INCONCLUSIVE** for smooth sliceness; Miyazaki already settles non-ribbon | **NOT YET COMPUTED** candidate-by-candidate |
| Metabelian / twisted Alexander homotopy-ribbon restrictions | **APPLIES BUT VANISHES** logically | **APPLIES BUT VANISHES** logically | **NOT YET COMPUTED** | **NOT YET COMPUTED** |
| Irregular dihedral / Cappell–Shaneson Ξ | **HYPOTHESES FAIL** as an attack: handle-ribbon already supplies the extension | **HYPOTHESES FAIL** as an attack for the same reason | **NOT YET COMPUTED** (requires a suitable coloring/extension analysis) | **NOT YET COMPUTED** |
| Turaev multiplace Seifert form | **NOT YET COMPUTED**; exact Theorem H hypotheses need recovery [S20] | **NOT YET COMPUTED** | **NOT YET COMPUTED** | **NOT YET COMPUTED** |
| Derived-series / solvable / polycyclic refinements | **HYPOTHESES FAIL** for any obstruction only to homotopy-ribbon; ribbon-specific refinement `UNKNOWN` | **HYPOTHESES FAIL** at homotopy-ribbon level | **UNKNOWN** | **UNKNOWN** |
| Branched-cover symmetry / equivariant Floer | **UNKNOWN** (no verified symmetry/action package) | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** |
| Ordinary / involutive Heegaard Floer sliceness invariants | **APPLIES BUT VANISHES** (smooth slice) | **APPLIES BUT VANISHES** (smooth slice) | **NOT YET COMPUTED** for concordance equality | **NOT YET COMPUTED** for smooth sliceness |
| Instanton / monopole ribbon-concordance tools | **NOT YET COMPUTED**; [S11] hypotheses not matched | **NOT YET COMPUTED** | **NOT YET COMPUTED** | **NOT YET COMPUTED** |
| Donaldson / lattice embeddings from branched covers | **APPLIES BUT VANISHES** as a sliceness obstruction if correctly formulated | **APPLIES BUT VANISHES** as a sliceness obstruction | **NOT YET COMPUTED** for sliceness | **NOT YET COMPUTED** for sliceness |
| Unlink derivative criterion [S02, Prop. 1.1] | **NOT YET COMPUTED** globally; a non-unlink R-link derivative is known | **NOT YET COMPUTED** globally | **APPLIES AND OBSTRUCTS** by an independent fibered theorem, not derivative enumeration | **APPLIES AND OBSTRUCTS** via [S08], not explicit derivative enumeration |
| Park–Powell derivative triple-linking [S17] | **NOT YET COMPUTED** | **NOT YET COMPUTED** | **NOT YET COMPUTED** | **NOT YET COMPUTED** |
| Handle-ribbon criterion / R-link derivative [S02] | **APPLIES BUT VANISHES**; explicitly satisfied [S01] | **APPLIES BUT VANISHES**; handle construction supplies it | **UNKNOWN** | **UNKNOWN** |
| Half-ribbon invariants [S21] | **UNKNOWN**; handle-ribbon ⇒ half-ribbon is not cited | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** |
| Ribbon-concordance Floer injectivity/monotonicity | **COMPUTED / INCONCLUSIVE** in the sense slice-to-unknot is not the needed ribbon-concordance direction | **COMPUTED / INCONCLUSIVE** | **APPLIES AND OBSTRUCTS** through stronger fibered pairing theorem | **APPLIES AND OBSTRUCTS** [S08] |
| Minimum-height immersed-curve invariant [S10] | **HYPOTHESES FAIL** for the published cabling theorem; DG is not presented as its cable target | **UNKNOWN** | **NOT YET COMPUTED** | **NOT YET COMPUTED** |
| Ribbon number / fusion number | **COMPUTED / INCONCLUSIVE**: search found no disk, no completeness [S03] | **COMPUTED / INCONCLUSIVE**: algorithms fail even on known ribbon GST knots [S16] | **UNKNOWN** | **UNKNOWN** |
| Alexander / Fox–Milnor | **APPLIES BUT VANISHES** (smooth slice) | **APPLIES BUT VANISHES** (smooth slice) | **APPLIES BUT VANISHES** (algebraically slice by common polynomial/inverse sum) | **APPLIES BUT VANISHES** (constructed algebraically slice [S08]) |
| Twisted Alexander sliceness machinery | **APPLIES BUT VANISHES** for any valid slice-disk metabolizer | **APPLIES BUT VANISHES** | **NOT YET COMPUTED**; could disprove sliceness of a pair | **NOT YET COMPUTED**; could disprove sliceness |
| Stable handleslide / R-link computations [S14] | **COMPUTED / INCONCLUSIVE** (R-link derivative already known) | **COMPUTED / INCONCLUSIVE** (stable is not ordinary/ribbon) | **HYPOTHESES FAIL** | **HYPOTHESES FAIL** |

## Why the best certified candidates survive

The key fact is structural, not a shortage of classical computations. `DG` and the GST lane come with exceptionally simple disk exteriors/handle descriptions. They already satisfy the consequences tested by π₁-surjectivity, Casson–Gordon extension, metabelian homotopy-ribbon restrictions, and R-link derivatives. Smooth sliceness also forces the ordinary concordance package to vanish.

The remaining logical gap is the strict inclusion

\[
\text{unlink derivative (ribbon)}\ \subsetneq?\ \text{R-link derivative (handle-ribbon)}.
\]

No inspected theorem turns the known R-link derivative into an unlink derivative, and no complete procedure excludes every unlink derivative for either certified target. That is why adding more sliceness invariants or more homotopy-ribbon obstructions does not narrow the flagship lane.
