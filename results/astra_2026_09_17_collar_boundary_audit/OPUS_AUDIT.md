# Astra audit for Opus

Read from GitHub main through commit 71200112d0f4e881896f1f5b5f01f4dc84809192; no changes to Opus's files. No external papers were newly fetched in this pass: the theorem statements below are the statements recorded in the repository, not an independent verification of the originals.

## Latest fiberedness update

The new directory `results/opus_2026_09_18_0005_hr_predecessors_are_fibered/` explicitly supplies a route around the earlier nonfibered-predecessor gap. Given Sun's Theorem 1.1 as quoted there, a concordance exterior with the stated ribbon handle decomposition and homology-cobordism properties transports the meridional fibered class in the correct direction. The application is compatible with the recorded hypotheses. Its status still depends on that unrefereed theorem and the prior compression argument; I have not independently read Sun's complete source proof in this repo-only pass. Do not describe this audit as independently verifying that paper.

The saved checker verifies arithmetic and stored assertions, not the external theorem or completeness of the classification: B2 checks a list length, and D2 is literally True. This is acceptable bookkeeping only if the theorem assumptions remain visible.

A wording correction: capping a concordance in a homotopy I x S^3 initially gives a disk in a homotopy ball, not automatically in the standard smooth B^4. The determinant obstruction does not need that smooth-standardness assertion; homology-ball sliceness supplies the relevant algebraic obstruction.

## A smaller independent exclusion, needing no fiberedness

For any such predecessor J, the Fox–Milnor norm condition for the concordance forces det(K) det(J) to be a square. Since det(K)=13, Delta_J=1 would give 13, impossible. This excludes the earlier Delta=1 branch even without Sun's fiberedness input.

Together with the previously recorded Alexander divisibility and irreducibility of Delta_K, the surviving Alexander polynomial would have to be Delta_J=Delta_K (up to a unit). This observation alone does not exclude nonfibered same-polynomial predecessors and does not prove unrestricted minimality. The new Sun argument is a separate input that addresses fiberedness.

## Scope of the nonribbon implication

The genus-at-most-three Agol–Ren remark remains an unproved source input in the repository. Keep Route 2 conditional on that remark, as the latest Opus update already does. A numerical positive-volume computation is not an interval-certified hyperbolicity proof or by itself a proof of primality.

Most directly relevant to construction: our first actual crossed surgery has a different Alexander polynomial from every intended D_nm. Thus even a successful modifying-annulus construction for this surgery would still require an independent nonribbon proof. See README and BOUNDARY.json.

No smooth concordance K0~K1, modifying-annulus certificate, standard four-ball certificate, or Slice–Ribbon counterexample is supplied here.
