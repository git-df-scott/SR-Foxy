# Evidence and trust boundaries

Research date: 18 September 2026. Original checkout `19cddf9`; fast-forwarded
to `ceb83c2` when the one-commutator publication arrived. No branch was created,
no existing research/data artifact was overwritten, and no external process
or search shard was changed. All new results are in this directory and
research/48. The fixed diagram and factor producers each have a 30-second CPU
cap and completed in under one second. No knot-invariant or census search ran.

## Sources used

* Jeffrey Meier and Alexander Zupan, *Knots bounding nonisotopic ribbon disks*,
  Journal of Topology 18 (2025), e70047,
  [DOI 10.1112/topo.70047](https://doi.org/10.1112/topo.70047), Section 2.1.
  Supports the punctured-knot product ribbon-disk model. The collar/whisker
  identification in this package is our additional argument. Consulted during
  this session; a later publisher-page fetch timed out.
* Jennifer Hom, Sungkyung Kang, JungHwan Park, *Ribbon knots, cabling, and
  handle decompositions*, arXiv:2003.02832v2, 25 March 2020,
  [Proposition 2.1 and proof](https://arxiv.org/pdf/2003.02832).
  Supports the parallel-ribbon-disks and joining-bands construction for
  (p,1)-cables. Checked 18 September 2026. It does not certify D01#J.
* Dror Bar-Natan's *Knot Atlas*, [6_3 entry](https://www.math.toronto.edu/~drorbn/private/KAtlas/Knots/6.3.html),
  undated, checked 18 September 2026. The listed fully amphicheiral symmetry
  implies invertibility, needed when relating the mirrored braid block to
  the oriented inverse knot. This is a cited table fact, not a new symmetry
  computation. Two elementary diagram-symmetry trials gave no map; those
  trials do not obstruct knot invertibility.
* Katura Miyazaki, *Nonsimple, ribbon fibered knots*, Transactions AMS 341
  (1994), 1–44, [DOI 10.1090/S0002-9947-1994-1176509-4](https://doi.org/10.1090/S0002-9947-1994-1176509-4),
  Theorem 5.5. We reuse the precise hypotheses and source-access limits already
  recorded in `results/night_2026_09_18_followup/theorem_audit.md`; no new
  claim of having read an inaccessible original PDF. Its application is only
  to the four prime fibered summands of D01#R, not to D01#J.

## Reused evidence, without rerunning its computations

* Research/38 and `night_2026_09_18_followup/geometry_free_audit.json`:
  stored K0 and K1 are prime, fibered, with the same irreducible Alexander
  polynomial. The HFK backend and coefficient/theorem bridge are documented
  there; these are software computations, not formally verified proofs.
* `night_2026_09_18_jones/RESULTS.json` and `inputs.json`: exact distinction
  of K1 from K0 and its mirror. Polynomial distinction supplies no sliceness.
* Research/42: the moving-boundary surface realization. Its existence argument
  is reused explicitly; this session did not create its endpoint PD.
* Research/44: SnapPy 3.3.2 topology-preserving retriangulation trust audit.
  The new D01 factor identification verifies its FINAL face map independently;
  upstream moves and peripheral matrices remain kernel-trusted.
* Commit `ceb83c2`, `astra_one_commutator_2026_09_18/`: exact one-commutator
  certificate. This session verifies its bundle and correspondence to the
  checkout, then evaluates its two handles in the newly specified model.

## Failed constructions and controls

The two named old compression loops and both named new handle loops have
nonidentity finite images. This proves those four caps impossible, not all
possible compressions or annuli. One actual cable-splitting saddle was
performed; its component obstruction prevents that specified ribbon prefix.
The second stabilizer ribbon certificate is absent.

Whole-diagram comparisons did not identify the stored D01 with a freshly
assembled sum; cutting its actual neck and positively identifying its factor
resolved that dependency. No negative isometry test was used. Checker mutation
controls reject a reversed collar sign, a trivialized handle word, a wrong
saddle, and a false even tetrahedron map.

Full-surface relative framing, actual repaired-axis PDs, annulus double-point
labels, Whitney disks, and a standard-B4 annulus modification are absent.
No nonribbon certificate is transferred to an unidentified surgery boundary.
