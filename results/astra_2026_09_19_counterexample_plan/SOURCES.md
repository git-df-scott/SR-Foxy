# Source ledger

Accessed 19 September 2026. Primary-source statements are distinguished from calculations and proposals in PLAN.md. Preprints are not treated as peer-reviewed merely because they are recent. No external author or collaborator was contacted.

| Source | Date / status | Precisely supported use |
|---|---|---|
| Robert Gompf, Martin Scharlemann, Abigail Thompson, [Fibered knots and potential counterexamples to the Property 2R and Slice–Ribbon Conjectures](https://arxiv.org/html/1103.1601) | Geometry & Topology 14 (2010), 2305–2347; arXiv version 2011 | Original GST figures and §8 standard-ball slice construction; slice/ribbon preservation under handle slides. Does not prove the unresolved band sum nonribbon. |
| Michael Eisermann, [The Jones polynomial of ribbon links](https://arxiv.org/html/0802.2287) | Geometry & Topology 13 (2009); arXiv 2008 | Necessary Jones nullity and determinant-congruence conditions for ribbon links. Passing is not a ribbon certificate. |
| Wenjie Diao, Haoqian Pan, Chunxing Yan, [Some experimental results on stable equivalence of GST Links for the Generalized Property R Conjecture](https://arxiv.org/html/2604.17737) | 20 April 2026, preprint | Theorem 1.1 finite stable-equivalence ranges and stabilization definitions. §2.1 defers algorithm details. The suggested Eisermann test on a stable representative is our inference from this plus GST preservation, not a result of this paper. |
| Trevor Oliveira-Smith, [A Dunfield–Gong 4-Sphere is Standard](https://arxiv.org/html/2603.23717v1) | Submitted 24 March 2026, preprint; accessed HTML displays an August internal date | Corollary 1.1.1 gives standard-B⁴ sliceness of DG18nh00000601; Theorem 1.2 supplies fibered handle-ribbon structure. Does not assert nonribbonness. |
| Ian Agol, Qiuyu Ren, [Ribbon concordance of fibered knots and compressions of surface homeomorphisms](https://arxiv.org/html/2603.10884v1) | 11 March 2026, preprint | Fibered ribbon-concordance/compression structure and hypotheses. No unrestricted finite classification of arbitrary ribbon disks is inferred. |
| Jennifer Hom, JungHwan Park, [Ribbon concordance and cabling](https://arxiv.org/html/2608.06625) | 6 August 2026, preprint | Same-companion cable rigidity and prime predecessors under stated hypotheses; not a general sliceness obstruction. |
| Gary Dunkerley, [arXiv:2606.20802, full text](https://arxiv.org/html/2606.20802v1) | 18 June 2026, preprint | §6's named Whitehead-double/15-crossing examples fail sliceness; ribbon minimality by itself is not a slice counterexample. |
| Sungkyung Kang, JungHwan Park, Masaki Taniguchi, [arXiv:2505.03720](https://arxiv.org/abs/2505.03720) | 2025 preprint; abstract inspected | Claimed infinite concordance order for nontrivial figure-eight cables. Full proof not replayed here. |
| Junghwan Park, Mark Powell, [Ribbon obstructions and derivatives of knots](https://www.maths.gla.ac.uk/~mpowell/ribbon-obstr-derivs010118.pdf) | January 2018 draft consulted; later Israel Journal of Mathematics 250 (2022) publication | Homotopy-ribbon/derivative obstruction scope in the draft. Do not substitute it for an obstruction to ribbonness of a knot already known handle/homotopy ribbon. |
| Marc Lackenby, [arXiv:2606.06122](https://arxiv.org/abs/2606.06122) | 4 June 2026 preprint; abstract inspected | Stable Andrews–Curtis/thickenable-presentation result has hypotheses; not automatic standardization of every proposed homotopy ball. |
| Dror Bar-Natan and Scott Morrison / Knot Atlas contributors, [6₃ database entry](https://katlas.org/wiki/6_3) | Living database, retrieved 19 September 2026 | Explicit PD, bridge index 2 and fully amphicheiral symmetry type. Supports invertibility used for the single 6₃ factor reversal in our Whitehead identity. Exact factor-to-6₃ signature checked computationally. KnotInfo direct result pages were unavailable through the web tool. |

The Hom–Park gamma-zero family paper was also cross-checked at [arXiv:2507.20455](https://arxiv.org/abs/2507.20455) and its [2026 journal page](https://link.springer.com/article/10.1007/s00209-026-04050-3). This does not supersede the repository's candidate-specific HKL obstruction.

## Repository provenance and source recovery

Final inspected remote tree: [SR-Foxy at def9f21](https://github.com/git-df-scott/SR-Foxy/tree/def9f2192ce6e80393a45c289b77eceb1c3617a2). The working checkout was deliberately not fast-forwarded during concurrent work.

The copied `pd_algebra.py` and `pd_moves.py` came from `research/gst_2026_09_19_exact/` at `0a1b585`. The Whitehead input/replay came from `results/astra_2026_09_19_infection_gate/`; their contents are retained with this session's output, and the session manifest hashes them. The copied cyclic-cover witness/checker came from `results/astra_2026_09_19_live_checkpoint_audit/`. Freshly replayed fixed witnesses do not equal an independent replay of that entire endpoint audit.

GST source artifact: GitHub Actions run **35421212838**, artifact **10577708079**, name `astra-gst-primary-1103-1601v1`. Source archive and PDF were downloaded from that existing artifact and hashes checked:

- `1103.1601v1-source.tar`: `74916438512928f99f2969c096c9d3fb4acee2a4d65e01a2fb986d3fa7405354`
- `1103.1601v1.pdf`: `47921a77d6520d3ecbb79ce62e22244a6a21826c57bb4465cdf01e77ce40a9ec`

The local PDF is [the GST paper](gst_primary/1103.1601v1.pdf). The source extraction includes original vector figures and TeX labels. The hash check establishes preservation of the downloaded artifact; the title/content establish its research relevance. The link diagram still needs combinatorial tracing.

## Verification scope

- New Whitehead band output regenerated from the pinned target and descriptor; split movie found and replayed. Remaining connected-sum factors checked with reflection prohibited; only 6₃ needs orientation reversal. Regina's third signature argument permits rotation, not component permutation. Producer and checker share topology dependencies.
- GST polynomial reciprocal relation, irreducibility mod 2, Bézout identity, resultant, mod-43 gcd/order, Smith diagonal, determinant and cover-order resultant independently recalculated in `replay_gst_algebra.py`.
- Stored Hom–Park norm obstruction arithmetic rechecked in `HP_NORM_REPLAY.json`.
- Stored compact degree-four cyclic-cover witnesses rechecked with their standard-library verifier; corruption controls rejected.
- Local mixed-transfer geometry and local-movie checkers passed, without constructing the missing global caps/annulus.
- General Eisermann controls recounted from raw rows; this was not a rerun of all Jones computations.
- GST 15,794-band/50-movie results and Floer package inspected as prior research; not re-executed in full this session.
- Newer GPT claims about the 192-dart bridge, extra binary Bing trees and edge-preserving enumeration remain chat-reported until their exact attachments are recovered/replayed.

## Reproduction environment

Python 3.11.15 in `/tmp/sr-foxy-20260919-leads-venv`. Direct dependencies are pinned in `requirements.txt`. A missing tkinter warning affects Plink's GUI and did not prevent headless computations. This is a temporary environment; recreate it from requirements rather than relying on `/tmp` persistence.

No unsuccessful search, matching polynomial, failed API call, damaged database or time-limited computation is promoted to a mathematical impossibility result.
