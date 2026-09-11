# K_G: attempt to extract the R-link derivative from Oliveira-Smith arXiv:2603.23717 (2026-09-11)

Outcome: **the 5-component derivative L⁺ is not in the paper.** Every item below was checked against the TeX source and the ten rendered figures.

## What the paper actually contains (VERIFIED)

- Theorem 1.2 is proved in §3.2 by an existence argument: the two-component R-link L = K_G ∪ U (U a 0-framed unknot linking the band of the Dunfield–Gong ribbon disk of K_B) is, by Miller–Zupan Thm 3.3 (restated as Thm 3.3), *stably equivalent* to a link K_G ∪ L⁺ with L⁺ a Casson–Gordon derivative on the fiber. No handleslide sequence, no diagram and no fiber surface are drawn. "Five components" is forced only by genus(K_G) = 5.
- The only picture of the R-link is Figure 3.3: K_G ∪ U with three unexpanded twist boxes (−1 on a four-strand block, −1/2 on a two-strand block, −1 on a lower block). Expanded it exceeds roughly 100 crossings. Not transcribable reliably from the raster, and U is defined only through the pictorial DG band.
- R-link property is proved structurally: the upside-down handle decomposition of the exterior of the K_B ribbon disk is K_B⟨0⟩ ∪ U⟨0⟩ ∪ two 3-handles ∪ 4-handle, so 0-surgery on L caps off with a genus-2 handlebody.
- Statements confirmed: Thm 3.1 (Casson–Gordon 5.1), Cor 3.1.1 (Casson–Gordon 5.4), Lemma 3.2 (Miller–Zupan 3.1: handle-ribbon in some homotopy ball iff a component of some R-link), Thm 3.3 (Miller–Zupan 3.3), Questions 3.1–3.4.

## What was verified computationally (bare CPython, snappy 3.3.2, regina 7.4)

| check | result |
|---|---|
| DT code `ycjkdnhQyUtMsaVweFIRCXOBgLJDkP` | 3-component, 25-crossing link; linking matrix [[0,−1,−1],[−1,0,2],[−1,2,0]] |
| component identification | all three unknotted; sublinks (0,1) and (0,2) are Hopf links, so R = component 0 |
| Regina, ⟨1,0⟩ surgery on R∪B and on R∪G | one-tetrahedron triangulations, `isSphere()` True |
| fill R(+1), B(0) | volume 11.9345081499, 14 tetrahedra, `is_isometric_to` the K_G exterior: **True** (so G = component 2 and r = +1; slope −1 gives the wrong volume) |
| fill R(+1), G(0) | volume 11.5729287764, 13 tetrahedra; `exterior_to_link` gives a 31-crossing knot K_B (matches Figure 1.1b's crossing count); genus 5, fibered, HFK rank 25; saved as `data/knots/K_B_0friend.json` |
| S³₀(K_B) vs S³₀(K_G) | equal volume 8.7838564748, equal length spectra, equal cover homology through degree 4; combinatorial homeomorphism certificate not found (20 vs 21 tetrahedra) |

## Consequence for the plan

WS1.1's "handleslide search on L⁺" cannot start from the paper's data. Two replacements:

1. **Work with the two-component R-link L = K_G ∪ U directly.** By the upside-down argument, K_G is the belt sphere of a 2-handle in a no-3-handle diagram of B⁴ built from L. Abe–Tange Lemma 5.1 then says: if that diagram reduces to the empty diagram by slides, 1/2-cancellations and isotopy, K_G is ribbon. So Generalized Property R for the specific two-component link L would prove K_G ribbon. Obtaining L needs a transcription of Figure 3.3 with the twist boxes expanded, or a reconstruction from the RBG data (U is the 0-framed meridian of the DG band). This is a careful hand task, not a script.
2. **Construct a derivative on the fiber ourselves.** Requires the genus-5 fiber and its monodromy (TOOLING.md item 6), then the Casson–Gordon extension. Research subproject.

The pictures rendered from the paper are not committed (copyright); the scripts `step2*.py`/`step3*.py` in the session scratchpad reproduce the table above from the DT code alone.
