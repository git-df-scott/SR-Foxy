# Source and dependency ledger

All web checks below: 18 September 2026. No historical novelty is claimed.

| Source | Precise use | Status |
|---|---|---|
| Ian Agol, Qiuyu Ren, *Ribbon concordance of fibered knots and compressions of surface homeomorphisms*, arXiv:2603.10884v1, 11 March 2026, [primary text](https://arxiv.org/html/2603.10884) | Theorems 1.7 and 1.13; §2 marked relative compression bodies; §7.2 supplies fibered predecessor factors. §7.1 describes the fibered (2,1) cable pattern. | Preprint; statements and relevant proof portions checked. Not formally verified or represented as peer-reviewed here. |
| Stefan Friedl, Mark Powell, *Homotopy ribbon concordance and Alexander polynomials*, arXiv:1907.09031v3, 22 July 2020, [primary text](https://arxiv.org/html/1907.09031) | Inspected Theorem 1.1 and its definition of the standard ambient concordance. | NOT used in the proof: avoid silently extending its stated ambient hypothesis to the homotopy ambient allowed by Agol–Ren. The compression-body subquotient argument supplies the divisibility needed here. |
| `research/38` and `results/night_2026_09_18_followup/geometry_free_audit.json` | Prime fibered K0,K1 and their irreducible polynomial. | Existing exact/software certificate reused; no HFK or Fox rerun. |
| `results/night_2026_09_18_jones/RESULTS.json` | Distinction from K0, its mirror, and reversals, since the knot Jones polynomial is orientation-insensitive. | Existing exact certificate reused. |
| `results/astra_2026_09_18_marked_annulus_construction/factor_identification/` | Actual stored D01 prime summand types. | Existing positive combinatorial certificate, with upstream kernel trust as stated there. |
| `research/42` | The prescribed handle core starts split from a and its disk-push isotopies fix a. | Mathematical construction reused. No new endpoint PD for that surface is claimed. |
| `results/astra_one_commutator_2026_09_18/` | The short A word and prior finite translation rules. | Bundle reused with pinned inputs; the new A=c2^-1 identity also has a direct one-relator proof independent of those translations. |

Two independent agent reviews checked the decomposition-theorem application
and the scope of the linking obstruction. The root checked the primary text,
the compression-body dimension argument, and the actual crossing data.
The mathematical argument remains distinct from the finite-data replay.

Failed or unfinished work is retained: the diagram probe completed an
unmarked local isotopy but not the proposed cable-whisker transfer; no map
was found in its direct even-rotation comparison. Neither failure distinguishes
knots. Two inspection calls requested nonexistent Spherogram helper names;
available functions were then inspected directly. These were API lookup
errors, not failed mathematical tests. No long-running process was started.
