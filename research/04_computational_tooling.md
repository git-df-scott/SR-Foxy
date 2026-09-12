# 04 — Computational Tooling Survey for the Slice–Ribbon Campaign

Compiled 2026-09-11. Every claim is labelled **[V]** VERIFIED (I ran it, or read the repo/docs/paper
text myself), **[PV]** PARTIALLY VERIFIED (seen in a reliable secondary source — search-result
summary, abstract, or a paper's bibliography — but not exercised), or **[U]** UNVERIFIED
(plausible, asserted nowhere I could confirm; treat as a research question, not a fact).

Nothing in this document is a tool, repo, function or capability I invented. Where a tool the
campaign would *want* does not exist, I say so explicitly rather than name a plausible substitute.

Environment used for live checks: Linux, Python 3.11.15, `pip install snappy regina` →
**snappy 3.3.2**, **regina 7.4**, no SageMath, no GAP. All timings on that box.

---

## 0. Headline results established while writing this (all [V], reproducible)

### 0.1 The target knot 18nh00000601 is fully in hand

Burton's census row (range-fetched from the authoritative CSV, see §1):

```
name      18nh_00000601
knot_sig  sabcdbefghijkglmhijknopqreanopqdcrmlflRSuvwT+5bdd
dt_code   fpqGmiHCrLNOeJKabd
```

Round-tripped through Regina and SnapPy:

| quantity | value | how |
|---|---|---|
| crossings | 18, non-alternating, 1 component | `regina.Link.fromKnotSig(sig)` |
| Regina PD (1-indexed) | `[[2,32,3,31],[4,1,5,2],[5,25,6,24],[8,16,9,15],[10,18,11,17],[12,8,13,7],[13,34,14,35],[16,10,17,9],[18,12,19,11],[19,26,20,27],[21,28,22,29],[23,32,24,33],[25,1,26,36],[27,20,28,21],[29,22,30,23],[30,4,31,3],[33,14,34,15],[35,6,36,7]]` | `L.pdData()` |
| SnapPy PD (0-indexed) | `[(1,31,2,30),(3,0,4,1),(4,24,5,23),(7,15,8,14),(9,17,10,16),(11,7,12,6),(12,33,13,34),(15,9,16,8),(17,11,18,10),(18,25,19,26),(20,27,21,28),(22,31,23,32),(24,0,25,35),(26,19,27,20),(28,21,29,22),(29,3,30,2),(32,13,33,14),(34,5,35,6)]` | `snappy.Link(pd).PD_code()` |
| signed DT | `(4,30,-24,12,16,18,-34,8,10,-26,-28,-32,-36,-20,-22,2,-14,-6)` | `Link.DT_code()` |
| **braid word** (7 strands, 34 letters) | `[-1,-2,-3,-4,-3,-5,4,3,2,1,3,3,3,3,-4,5,-6,5,4,-3,-3,-3,-3,2,3,-4,3,-2,-3,4,-5,4,6,-3]` | `Link.braid_word()` |
| Alexander polynomial | `t^10-2t^9+t^8-t^7+4t^6-7t^5+4t^4-t^3+t^2-2t+1` | `regina.Link.alexander()` |
| determinant | 25 | `|Δ(-1)|` |
| **HFK** | `seifert_genus=5`, `fibered=True`, `tau=0`, `epsilon=0`, `nu=0`, `L_space_knot=False`, `total_rank=25` | `Link.knot_floer_homology()`, **<0.01 s** |
| HFK ranks (all on the diagonal M=A, δ=0) | `{(-5,-5):1,(-4,-4):2,(-3,-3):1,(-2,-2):1,(-1,-1):4,(0,0):7,(1,1):4,(2,2):1,(3,3):1,(4,4):2,(5,5):1}` | idem |
| UV=0 complex | 25 generators, 28 differentials | `knot_floer_homology(complex=True)` |
| exterior | 14 tetrahedra, **vol = 11.9345081499** | `Link.exterior()` + `simplify()` |
| H₁(Σ₂) | **Z/25** (cyclic) | `M.covers(2,cover_type='cyclic')` → `Z/25 + Z` |
| H₁(Σ₃) | (Z/7)² | `M.covers(3,...)` → `Z/7+Z/7+Z` |
| H₁(Σ₅) | (Z/31)² | `M.covers(5,...)` → `Z/31+Z/31+Z` |
| diagram minimality | `Link.simplify('global')` returns False at 18 crossings | SnapPy |

**Genus 5 and fiberedness are confirmed independently of the literature.** That the HFK is
supported entirely on the diagonal is exactly the δ=0 ("thin-like") shape expected of a slice knot
and gives no obstruction.

### 0.2 Regina ships the GST knot as a built-in [V]

`regina.ExampleLink.gst()` — docstring, verbatim: *"Returns a 48-crossing potential counterexample
to the slice-ribbon conjecture, as described by Gompf, Scharlemann and Thompson. Specifically, this
knot is Figure 2 from their paper 'Fibered knots and potential counterexamples to the property 2R
and slice-ribbon conjectures', Geometry & Topology 14 (2010), 2305–2347."*

Computed (PD round-trip to SnapPy verified isometric, `is_isometric_to` → True):
48 crossings (irreducible under both `regina.simplify()` and `snappy.simplify('global')`),
Δ of degree 16, `writhe=2`, exterior 28 tetrahedra, **vol = 23.8448997956**, HFK in **0.6 s** with
`seifert_genus=10`, `total_rank=189`, `tau=epsilon=nu=0`, and — **flag this** —
`fibered=False`, with the top Alexander grading A=10 carrying rank 2 (`(10,13):1, (10,14):1`).

> **Open discrepancy the campaign must resolve before relying on this object.** GST's knots are
> described in the literature as fibered, and Δ has degree 16 (Alexander genus 8) against Seifert
> genus 10. The PD→SnapPy conversion is *not* the culprit: the two exteriors are certified
> isometric. So either Regina's `gst()` encodes a different member/presentation than the fibered
> family the campaign wants, or the fibered claim attaches to a different knot in that paper. Do
> **not** propagate "Regina's gst() = the fibered GST knot" until checked against GST Figure 2 by
> hand. (Status of the discrepancy itself: **[V]** as a computation, **[U]** as to cause.)

### 0.3 The single biggest environment constraint [V]

**SnapPy's entire Dunfield–Gong ribbon pipeline, its HKL slice obstruction, Seifert matrices and
signatures are `@sage_method`-decorated and raise `SageNotAvailable` outside SageMath.**
Confirmed by running them:

```
Link.ribbon_concordant_links(...)  -> spherogram.sage_helper.SageNotAvailable
Manifold.slice_obstruction_HKL(...) -> snappy.sage_helper.SageNotAvailable
Link.seifert_matrix() / Link.signature() / Manifold.alexander_polynomial() -> SageNotAvailable
```

`snappy.sage_helper._within_sage` is `False` under plain CPython. **Plan the whole campaign inside
SageMath**, not inside bare Python. (What *does* work in bare CPython: `knot_floer_homology`,
`PD_code`/`DT_code`/`braid_word`, `simplify`, `exterior`, `covers`, `is_isometric_to`,
`verify_hyperbolicity`, `RibbonLinks`, `add_band`, and all of Regina.)

---

## 1. Getting the knot: censuses, names, and where the data lives

### Naming convention — settled [V]

The scheme is **Burton's**, documented on Regina's data page as `c[an][tsh]_k`:
crossing number, then `a`/`n` = alternating / non-alternating, then `t`/`s`/`h` = torus /
satellite / **hyperbolic**, then a sequential index. So **`18nh` = 18 crossings, non-alternating,
hyperbolic**; `00000601` is the index zero-padded to 8 digits. Regina's CSV writes it
`18nh_00000601` (underscore); Dunfield–Gong write `18nh00000601` (subscripted index, no
underscore). Same object. I confirmed the correspondence by pulling row 601 out of Burton's
`18n-hyp.csv.bz2` and getting a knot that reproduces every published property of DG's knot
(18 crossings, non-alternating, genus 5, fibered, det 25).

`K18n…` is **not** a valid alias: that's SnapPy/Hoste–Thistlethwaite notation, which stops at 15
crossings. `snappy.Manifold('18nh00000601')` and `snappy.Manifold('K18n00000601')` both raise
`OSError: manifold file not found` **[V]**.

### Is it in SnapPy? — No [V]

SnapPy 3.3.2's censuses, with live sizes:

| census | size | coverage |
|---|---|---|
| `HTLinkExteriors` | 180,511 | knots ≤14 (≤15 with `snappy_15_knots`), links ≤14 |
| `LinkExteriors` | 1,216 | Rolfsen, knots ≤11 |
| `CensusKnots` | 3,116 | ≤10 tetrahedra |
| `AlternatingKnotExteriors` | (callable, no `len`) | alternating through 16 crossings |
| `NonalternatingKnotExteriors` | (callable, no `len`) | non-alternating through 16 crossings |
| **`RibbonLinks`** | **12,184** (12,143 with `cusps=2`) | **new: DG's ribbon-link table, §2.5 of DG** |

Nothing reaches 18 crossings. **18nh00000601 must come from Burton's census or DG's archive.**

### KnotInfo / LinkInfo — No [PV]

KnotInfo tops out at 12 crossings for the full invariant table, with 13-crossing data partially
present. There is no 18-crossing entry and there will not be one. KnotInfo *does* have a
"monodromy" column for small fibered knots (relevant to §3) **[PV]**.

### Authoritative sources — both [V]

**(a) Burton's classical knot census** (the `18nh` names originate here).
Landing page: `https://regina-normal.github.io/data.html`.
File pattern: `https://people.smp.uq.edu.au/BenjaminBurton/knots/[crossings][a|n]-[hyp|torus|satellite].csv.bz2`
(the older `www.maths.uq.edu.au/~bab/knots/...` URLs 301-redirect there).

- `18n-hyp.csv.bz2` — **1,330,480,533 bytes**, 39,866,095 knots, Last-Modified 2018-05-29,
  **`Accept-Ranges: bytes`**.
- Columns: `name,knot_sig,dt_code` (torus/satellite files add `structure`; ≤12-crossing files add
  `dt_name` cross-referencing KnotInfo/Knotscape).
- Bundles: `all_3-12.tar.bz2` (56 KB), `all_13-16.tar.bz2` (41 MB).

> **Practical trick that saves 1.3 GB [V].** The CSV is sorted by index and bzip2 blocks decompress
> independently, so a low-index knot is reachable with a Range request:
> `curl -r 0-3000000 -o head18.bz2 <url>; bunzip2 -c head18.bz2 | sed -n '602p'`
> — that is exactly how I obtained the row above, in seconds.

**(b) Dunfield–Gong code and data — Harvard Dataverse [V]**
`doi:10.7910/DVN/YBDTBT` → `https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/YBDTBT`
Title: *"Ribbon concordances and slice obstructions: code and data"*, Dunfield (UIUC) & Gong
(Texas A&M), deposited 2025-12-22, V1 released 2025-12-29.
**Exactly one file: `plausibly_slice_V1.zip`, 1,022,355,830 bytes, md5 `7f6dc1df595ba1b4dbb1a9b338798b0b`, file id 13283715.**
(Ranged access to the Dataverse download endpoint returned 404 for me — expect to pull the whole GB.)

From DG §1.19 (read directly from the PDF) **[V]**: *"We include in [DG] a quick-access list of PD
codes for all 286 knots in PS19 mentioned in this paper by name."* **18nh00000601 is one of those
286** — so its PD code ships in that zip, and DG's ribbon certificates (§2.10) ship there too.
There is **no GitHub repo** for this; `github.com/NathanDunfield` has `montesinos`, `quadrics`,
etc., not a ribbon/slice repo **[PV]**.

**(c) A free bonus the paper gives away** — DG Table 11 prints the DT code of the RBG link realising
18nh00000601's 0-friend: `ycjkdnhQyUtMsaVweFIRCXOBgLJDkP`, with `r = 1`, annotated "ribbon" **[V,
read from the PDF]**. This is the object behind Theorem 5.14 (K is smoothly slice in a homotopy
4-ball, hence topologically slice) and Theorem 1.12 (if K is *not* smoothly slice there is an
exotic S⁴).

---

## 2. Ribbon-disk / band search software

**Completeness statement, up front: no tool in this section is complete.** Every one of them is a
bounded search over diagrams, bands, twists and path lengths. A negative result from any of them —
including all of them run together — is evidence that a knot is hard to ribbon, never a proof that
it is not ribbon. DG themselves stopped at 4 bands ("only 75 of the ribbon disks we found used four
bands, so we did not search further than that") and never found a disk for 18nh00000601 **[V]**.

### 2.1 SnapPy 3.3+ `spherogram.links.bands` — the DG search, shipped [V]

This is the single most important find. The Dunfield–Gong band machinery is **in SnapPy 3.3.2 today**.

```python
Link.add_band(band)                  # band = (path, over/under flags, half-twists); DG Figure 7 encoding
Link.ribbon_concordant_links(max_bands=, max_twists=, max_band_len=,
                             paths='shortest'|'simple',
                             filter_for_plausibly_slice=True, certificates=True)
snappy.RibbonLinks                   # 12,184-entry census, each with .ribbon_cert
spherogram.links.bands.verify_ribbon_to_unknot(link, certificate)   # -> bool
spherogram.links.bands.{Band, core, search, merge_links, normalize_crossing_labels}
```

Docstring facts **[V]**: band length = strands crossed + 2; `filter_for_plausibly_slice` keeps only
links with vanishing linking numbers and signature and Fox–Milnor Alexander polynomial, stops at
the unlink, and *short-cuts through `RibbonLinks`*; `certificates=True` returns
`{new_link: [D₁, b₁, D₂, …]}`; the unknot comes back as the literal string `'unknot'`.

`verify_ribbon_to_unknot` is the **certifier** — and its own docstring admits its limit verbatim:
*"TODO: Sometimes doesn't work when some intermediate link is non-hyperbolic… The below should
return True but might fail occasionally."* **[V]** So certification is reliable when the
intermediate links are hyperbolic (SnapPy settles the isotopies by `is_isometric_to`) and can fail
open on satellite/composite intermediates.

**Requires Sage** (see §0.3) **[V]**.

### 2.2 Owens–Swenton, via KLO [V/PV]

- Paper: *An Algorithm to Find Ribbon Disks for Alternating Knots*, Exp. Math. (arXiv:2102.11778).
  Donaldson-diagonalisation-driven; follows band moves compatible with Goeritz-matrix
  factorisations **[PV]**.
- Data: `https://cat.middlebury.edu/~mathanimations/klo/ribbondisks/` — `.rb` files openable in KLO
  via *Computation → Ribbon Disks*: ≤16 cr (3,679 knots), 17 cr (6,513), 18 cr (19,071),
  19 cr (52,325), 20 cr (150,408), 21+ on request; plus 1,730 "escapees" (12x–21x). 231,996
  alternating knots resolved ribbon ≤20 crossings; **586 prime alternating knots unresolved**
  (7 at 16–17 crossings, with a $10 bounty) **[PV]**.
- **Limited to alternating knots.** 18nh00000601 is non-alternating → **this method does not
  apply to the primary target.** Useful only for lane-B alternating comparanda.

### 2.3 KLO (Kirby Link/Knot-Like Objects calculator, Frank Swenton) [PV]

`http://www.klo-software.net` (302 → `https://community.middlebury.edu/~mathanimations/klo`).
Windows `.zip` and macOS `.dmg` (64-bit Intel); **version 0.979 alpha**. Supports Reidemeister
I/II/III by clicking faces and dragging strands, 2-handle slides, 1-handles/surgery, blow-ups and
blow-downs, band-slides and band-swims, meta-Reidemeister moves; computes linking-form signature
for Kirby diagrams, Seifert invariants, HOMFLY, hyperbolic structure. Ad-hoc ribbon test on
`ctrl-B`. **No documented scripting/batch interface, no license statement, no Linux build.** Treat
KLO as an interactive workbench for a human, not a pipeline stage. (Every specific claim here is
from the KLO site / Owens–Swenton page, not from running it — I have no GUI in this environment.)

### 2.4 Gukov–Halverson–Manolescu–Ruehle ML band search [V]

`https://github.com/ruehlef/ribbon` — GPL-3.0, 18 stars, 96 commits, Python 3.8–3.10, core shipped
as **pre-compiled closed-source Cython binaries**. Install:
`pip install --user git+https://github.com/ruehlef/ribbon.git`. Entry points: CLI `test_ribbon.py`
(flags for max bands / size / steps / tries) and `ribbon_example.ipynb`. Core class `RandomWalker`
with `invalid_action_mask()` and `step(action)`; band notation `s#/a#/o#/u#/t±`. Optional Sage +
snappy for Fox–Milnor filtering. Ships CSV databases of ~200 generated ribbon knots per crossing
level, 15–70 crossings. Paper: arXiv:2304.09304, published *Mach. Learn.: Sci. Technol.* 6(2),
2025-06-18. DG report GHMR independently reproduced the same list of 1705 ribbon knots ≤14
crossings **[V, read in DG]**.
**Limit: reinforcement learning / Bayesian optimisation — a heuristic searcher with closed-source
internals. It produces candidate band sequences; it certifies nothing.**

### 2.5 Regina [V]

Regina has **no ribbon or band search**. Its `Link` API (7.4, enumerated live) has no `addBand`, no
ribbon anything. Its contribution is diagram simplification (`simplify`, `simplifyExhaustive`,
`rewrite`, `improveTreewidth`, `useTreeDecomposition`), signatures (`knotSig`, `sig`,
`tightEncoding`), polynomials (`alexander`, `jones`, `homfly`, `arrow`, `bracket`), and the
`complement()` → normal-surface bridge (§4).

### 2.6 "knotjob" [V]

KnotJob is **not** a band searcher — see §9. DG use it purely for Khovanov-side invariants.

### 2.7 What does *not* exist

No tool enumerates band moves / fusion presentations **exhaustively up to N crossings** with a
completeness guarantee **[V, by absence: DG, who had 100 CPU-years and wrote the best such tool,
state their search is bounded at 4 bands and failed on this knot]**. Anyone claiming otherwise is
mistaken.

---

## 3. Fiber surface, monodromy, and compressions

| need | tool | status |
|---|---|---|
| Is it fibered, what is the fiber genus | `Link.knot_floer_homology()['fibered'] / ['seifert_genus']` | **[V]** — ran it; 18nh00000601 → `True`, 5, in <0.01 s |
| Seifert matrix from a diagram | `snappy.Link.seifert_matrix()` (Collins' algorithm via braid closure) | **[V]** exists; **Sage-only** |
| Thurston norm / fibered faces | `Manifold.alexander_polynomial()`, `Manifold.hyperbolic_torsion()`, `Manifold.hyperbolic_SLN_torsion()`, `Manifold.hyperbolic_adjoint_torsion()` | **[V]** methods exist; **Sage-only**. SnapPy has **no** `fibration()` / explicit fiber-surface extractor |
| Explicit monodromy as a mapping class | **flipper** (Mark Bell; PyPI; laminations via ideal-triangulation coordinates, builds layered veering triangulations of mapping tori), **curver** (curve complex), **Twister** (builds 3-manifold triangulations from mapping classes; now maintained by Bell) | **[PV]** — from Bell's software page and flipper's docs; not exercised here |
| Seifert surface in Regina | — | **[V] does not exist**: no `seifertSurface` in Regina 7.4's `Link` API. `seifertCircles()` exists but that is Seifert's algorithm circle count, not a surface object |
| Bar-Natan `KnotTheory\`` (Mathematica) | `SeifertMatrix`, etc. | **[U]** — I did not reach katlas.org this session; long-unmaintained, Mathematica-only. Do not rely on it |

**Honest assessment of the hard part.** Getting an explicit monodromy φ ∈ MCG(Σ₅,₁) for
18nh00000601 as a word in Dehn twists is **not** a solved push-button computation. SnapPy gives you
fiberedness and genus but not the surface; flipper/Twister go the other way (mapping class →
manifold), so the campaign faces an *inverse* problem: search mapping classes whose mapping torus
SnapPy certifies `is_isometric_to` the 14-tetrahedron exterior (vol 11.9345081499). That search is
exactly how Bell et al. produced monodromy data for small fibered knots **[PV]**, and at genus 5 it
is expensive. Budget this as **a genuine research subproject, not a script.**

### Agol–Ren — the theoretically right tool, with no code [V]

arXiv:2603.10884, Ian Agol & Qiuyu Ren, *Ribbon concordance of fibered knots and compressions of
surface homeomorphisms* (11 Mar 2026, 30 pp). Proves simplicial volume and dilatation are monotone
under ribbon concordance between fibered knots; every fibered knot has finitely many
ribbon-concordance predecessors; **gives an algorithm to enumerate, up to symmetry, all minimal
compressions of a surface homeomorphism** (extending Casson–Long), yielding an algorithm to find
all knots strongly homotopy-ribbon concordant to a given fibered knot in some homotopy I×S³.

**No released implementation.** No GitHub, no software repo, no complexity bound in the abstract.
This is the most valuable *unbuilt* tool for the campaign: 18nh00000601 is fibered of genus 5 and
bounds a fibered handle-ribbon disk, which is precisely Agol–Ren's setting. Implementing their
enumeration is a candidate flagship deliverable — but it depends on the monodromy problem above
being solved first.

Adjacent fibered-ribbon theory with no code either: Baldwin–Sivek *Ribbon concordance and fibered
predecessors* I/II (arXiv:2510.02214, 2602.21109) **[PV]**.

---

## 4. Derivative links and metabolizers

### 4.1 The lattice side

There is **no off-the-shelf "enumerate metabolizers of a Seifert form" package** **[V, by absence]**.
Build it in Sage from `Link.seifert_matrix()` (Sage-only) using `matrix(ZZ)`,
`.smith_form()`, `.kernel()`, `.saturation()`, `IntegralLattice`, `free_module`. This is ~100 lines,
not a dependency.

### 4.2 Size of the problem for genus 5 — the honest answer

Over **Z** the question "how many rank-5 Lagrangian direct summands does Z¹⁰ have for the
unimodular symplectic intersection form?" has the answer **infinitely many** — Sp(10,Z) is infinite
and acts transitively on them. There is no "2^k metabolizers" count. Any enumeration must be
*bounded* (by coefficient height, or by realisability as embedded curves on a fixed genus-5
surface after a bounded number of MCG moves), and a bounded search is a search, not a
classification.

The **finite** reduction is to the linking form λ on H₁(Σ_n(K)) — and for this knot the numbers are
tiny and I computed them **[V]**:

| cover | H₁ | order-√|H| subgroups | metabolizer candidates |
|---|---|---|---|
| Σ₂ | **Z/25 (cyclic)** | 1 (the unique order-5 subgroup) | **≤ 1** |
| Σ₃ | (Z/7)² | 8 lines in F₇² | ≤ 8 |
| Σ₅ | (Z/31)² | 32 lines in F₃₁² | ≤ 32 |

So the *branched-cover* metabolizer search for 18nh00000601 is trivially small — H₁(Σ₂) is cyclic
of order 25, so there is exactly one candidate metabolizer and no combinatorial explosion at all.
The general remark that "Lagrangian count grows with the number of primes dividing det" is right in
spirit (det = 25 = 5², a single prime, one cyclic factor → the minimal case), but for this knot it
is moot. **The blow-up is not in the algebra; it is in realising a metabolizer as an embedded
multicurve on Σ₅ and identifying the resulting derivative link.**

### 4.3 Certifying an unlink — exact API status [V]

**Correction to a common assumption: Regina 7.4 has NO `Link.isUnknot()` and NO `Link.isUnlink()`.**
I enumerated the full `regina.Link` method list; neither exists. The real route is via the
complement and normal-surface theory on `Triangulation3`:

```python
c = link.complement(); c.simplify()
c.isSolidTorus()      # unknot  <=> complement is a solid torus   (rigorous)
c.isSphere(); c.isBall(); c.isHandlebody(g)   # isHandlebody/recogniseHandlebody exist in 7.4
c.isIrreducible(); c.isZeroEfficient(); c.isOneEfficient(); c.isHaken()
c.nonTrivialSphereOrDisc()
regina.NormalSurfaces(...)   # full normal-surface enumeration
```

**n-component unlink ⇔ complement is a genus-n handlebody**, and `Triangulation3.isHandlebody(n)` /
`recogniseHandlebody()` are present in 7.4 **[V, methods enumerated]**. That is the rigorous
certificate to use; `Link.simplify()` reaching 0 crossings is a *heuristic* success, and its
failure proves nothing (SnapPy's `simplify` docstring even warns it silently discards unknotted
unlinked components and does not preserve `link_components` order **[V]**).

**Cost warning, measured [V].** `regina.ExampleLink.gordian()` (the classic hard unknot diagram)
did **not** finish `simplifyExhaustive()` + `complement().isSolidTorus()` within a 110-second
budget on this box. Unknot/unlink certification on an adversarial diagram is genuinely expensive;
always `simplify()` hard first and only fall back to normal surfaces on the residue.

SnapPy's complementary route: `Link.exterior()` → `Manifold.fundamental_group()` (trivial π₁ ⇒ …
only heuristically), `Manifold.is_isometric_to` (rigorous for hyperbolic pieces),
`Manifold.verify_hyperbolicity()` (interval-arithmetic **proof** of hyperbolicity **[V, ran it]**),
`Link.deconnect_sum()`, `Link.split_link_diagram()`, `Link.unlinked_unknot_components()`.

---

## 5. Group theory, Alexander modules, Milnor invariants

| need | tool | status |
|---|---|---|
| Nilpotent quotients of link groups | **GAP `nq`** (`github.com/gap-packages/nq`; ANU NQ, Nickel; C implementation, computes successive lower-central-series quotients) and **GAP `lpres`** (1.1.1, 2024-07-12; generalises Nickel's algorithm to L-presented groups, pure GAP) | **[PV]** — repo + manual seen, not run |
| Knot/link group presentation | `snappy.Manifold.fundamental_group()`, `snappy.Link.knot_group()`, `regina.Link.group()` / `.groups()` / `.extendedGroup()` | **[V]** all present |
| Alexander polynomial | `regina.Link.alexander()` (bare Python **[V]**), `snappy.Link.alexander_polynomial()` / `alexander_matrix()` / `Manifold.alexander_polynomial()` (Sage) | **[V]** |
| Fox calculus / Alexander module | `snappy.snap.fox_milnor` — `fox_derivative`, `alexander_data`, `fox_milnor_test`, `poly_is_a_norm`, `MapToFreeAbelianization`, `MapToGroupRingOfFreeAbelianization` | **[V]** — module enumerated live. Undocumented but real |
| **Twisted Alexander** | `Manifold.hyperbolic_torsion()`, `hyperbolic_SLN_torsion()`, `hyperbolic_adjoint_torsion()` — the Dunfield–Friedl–Jackson invariant (twist by a lift of the holonomy rep) | **[V] methods exist on `Manifold`; Sage-only.** ⚠️ There is **no** `snappy.twisted_alexander` top-level function and no `hyperbolic_torsion` in `snappy.snap` — I checked both; use the `Manifold` methods |
| **Casson–Gordon via HKL** | **`Manifold.slice_obstruction_HKL(primes_spec, verbose=, check_in_S3=, method='basic'\|'advanced', ribbon_mode=)`** in `snappy.snap.slice_obs_HKL` | **[V]** — this is DG §3 shipped in SnapPy. Returns the first `(p,q)` with a nonzero obstruction (⇒ not topologically slice) or `None`. Docstring example: `M.slice_obstruction_HKL([(10,[0,20]),(20,[0,10])], method='basic')` → `(3,7)` for `K12n813`. **Sage-only** |
| Milnor invariants μ̄ | **no package** | **[V, by absence]** — no maintained "Milnor invariants" or "clasper" software surfaced. Build from nilpotent quotients (nq/lpres) or from the unipotent Magnus embedding described in arXiv:1709.07335 **[PV]**. For a *knot* all μ̄ vanish; this matters only for derivative **links** in §4 |

---

## 6. Heegaard Floer and immersed curves

| need | tool | status |
|---|---|---|
| HFK (ranks, τ, ε, ν, genus, fibered) | **`snappy.Link.knot_floer_homology(prime=2, complex=False)`** — Szabó's HFK Calculator, wrapped | **[V] — confirmed the function exists and ran it.** 18 cr: <0.01 s. 48 cr: 0.6 s. Works over F_p for any prime < 2¹⁵ |
| UV=0 chain complex | same, `complex=True` → `{'generators': {name:(A,M)}, 'differentials': …}` | **[V]** — ran it; 18nh00000601 gives 25 generators / 28 differentials |
| standalone HFK | `pip install knot-floer-homology` (`github.com/3-manifolds/knot_floer_homology`) | **[PV]** |
| Immersed curves for CFK | **`github.com/hanselman/CFK-immersed-curves`** — Hanselman–Rasmussen–Watson algorithm; `BifilteredComplex`, `KnotTrainTrack` (arrow-sliding); scripts `compute-immersed-curves.py`, `check-cosmetic-surgery-conjecture.py`, `check-hyperbolic-invariants.py` | **[PV]** — repo read. ⚠️ **Python 2.7**, 9 commits, **no license**, input is text files from a *modified* Szabó HFKcalc (**not** SnapPy's dict), bundled complexes only ≤12 crossings, **local systems not implemented**, SVG output unreliable. Expect to write an adapter and port to Py3 |
| d-invariants of branched covers | **no single tool** | **[V, by absence]**. Assemble: `Manifold.covers(n, cover_type='cyclic')` for the homology **[V, ran it]** + Dehn filling; d-invariants themselves would need HFhat of the closed cover, which SnapPy does not compute |
| γ₀-sharpness (Hom–Park) from HFK output | — | **[U] — I could not confirm this.** The concern is real: SnapPy returns the **UV=0** quotient complex, and whether Υ / γ₀ are determined by CFK_{UV=0} rather than the full CFK^∞ is **not something I verified**. Do not assume `complex=True` suffices for γ₀; settle this question mathematically before writing the script |

---

## 7. Instanton / Casson–Gordon / dihedral

- **Casson–Gordon, practical:** the HKL route in `snappy.snap.slice_obs_HKL` (§5) is the only
  production-grade implementation I found, and it is the one that obstructed 2,211,761 knots for DG
  **[V]**. There is no package named `cg_invariants`.
- **Kjuchukova–Orr, arXiv:2604.00460**, *Extending Quotients of Knot Groups Over Surfaces in B⁴*
  (posted 2026-04-01) — sharp obstruction to a knot bounding a connected oriented smooth surface in
  B⁴ via extension of knot-group quotients **[PV]**. **No code availability confirmed** — the
  search results do not mention a repo, and I did not find one.
- Related dihedral-invariant work with partial implementations: *Computing Ribbon Obstructions for
  Colored Knots* (arXiv:1812.09553), *Algorithms for Computing Invariants of Trisected Branched
  Covers* (arXiv:2308.11689) **[PV]** — read these before writing anything from scratch.
- **Instanton-theoretic slice obstructions: no software exists.** **[V, by absence]** Nothing in
  DG, nothing on CompuTop. Do not plan a lane around computing instanton invariants.

---

## 8. Handle calculus and 4-manifolds

- **KLO** — the only interactive Kirby-calculus environment; see §2.3. Handle slides, band
  slides/swims, blow-up/down, linking-form signature. GUI-only, alpha, no Linux **[PV]**.
- **Regina 4-manifolds** — `regina.Triangulation4` and `regina.Example4` exist **[V, confirmed]**,
  but the recognition surface is thin: `isClosed`, `isConnected`, `isOrientable`, `isIdeal`,
  `isValid`, `isIsomorphicTo`, `isoSig` and variants — **no** 4-dimensional sphere/ball recognition
  (none is possible in general). Useful for bookkeeping and isomorphism signatures, **not** for
  deciding anything 4-dimensional.
- **"Kirby diagrams in SnapPy"** — **does not exist** **[V, by absence]**.
- **Verifying a claimed ribbon-band movie** — the real answer is
  `spherogram.links.bands.verify_ribbon_to_unknot(link, certificate)` (§2.1), which checks the
  chain of isotopies using SnapPy's `is_isometric_to` on hyperbolic exteriors and is documented to
  be flaky on non-hyperbolic intermediates **[V]**. Back it with Regina `isHandlebody`/`isSolidTorus`
  on the final link (§4.3) for a normal-surface-grade certificate.
- **GST links, concretely:**
  - `regina.ExampleLink.gst()` — 48 crossings, built in **[V]** (caveat in §0.2).
  - arXiv:2604.17737, Diao–Pan–Yan, *Some experimental results on stable equivalence of GST Links
    for the Generalized Property R Conjecture* (20 Apr 2026, 14 pp, 15 figs): implements an
    algorithm building L(p,q;c/d) explicitly (c/d path in a 2pq-gon annulus, sliding model arcs
    from the fiber surfaces F± of generalized square knots Q_{p,q}), verified with **SnapPy inside
    SageMath** using isometry signatures. Results: L_n stably equivalent to L(n+1,n;2/3) for
    **2≤n≤36**; L(3,2;4/d) stably handleslide trivial for **1≤d≤39**; L(3,2;6/(6n±1)) ≃
    L(3n±1,3;2/3) for **n≤7**. **No public repository; the authors state the algorithm's details
    are deferred to another paper** **[PV]**. Contacting them for the code is likely faster than
    reimplementing.
- **Abe–Tagami annulus-twist knots A_n(6₃): no software exists** **[V, by absence]**. Source is
  Abe–Tagami, *Fibered knots with the same 0-surgery and the slice-ribbon conjecture*,
  arXiv:1502.01102, Math. Res. Lett. 23(2), 303–323 (2016) — they give a **fibered potential
  counterexample to slice–ribbon** and show slice–ribbon ⇒ the modified Akbulut–Kirby conjecture is
  false **[PV]**. Background: Abe–Jong–Omae–Takeuchi, *Annulus twist and diffeomorphic 4-manifolds*,
  Math. Proc. Camb. Phil. Soc. 155(2), 219–235 (2013) **[PV]**. ⚠️ Most of the literature attaches
  the annulus-twist slice family to **8₂₀** (K_n from 8₂₀, all shown ribbon); the 6₃ annulus
  presentation appears in the characterizing-slopes context. **Verify which family the campaign
  actually means before building on it.** Implementation path: an annulus twist is a local diagram
  operation, so code it directly as PD surgery in spherogram/Regina — it is a script, not a
  dependency.

---

## 9. Concordance-invariant battery (lane B: testing [K_n] = [K_m])

| invariant | tool | entry point | status |
|---|---|---|---|
| τ, ε, ν, genus, fibered | SnapPy/Szabó | `Link.knot_floer_homology()` | **[V]** ran it |
| **s (Rasmussen)** | **KnotJob** (Dirk Schütz), Java | GUI `.jar` | **[V from the KnotJob page]** — s over **fields up to characteristic 211**, plus an **integral** s, for knots *and links* |
| Khovanov (even + odd), sl(3) homology, sl(3) s-invariants, Bar-Natan–Lee–Turner spectral sequence (char ≤211), Lipshitz–Sarkar Sq¹/Sq² refinements of s mod 2, **Dunfield–Lipshitz–Schütz refinements** (the LEO invariant s̃_c), Alexander, Jones, signature, determinant | KnotJob | idem | **[V]** — list taken from the KnotJob page, last modified 2025-08-15 |
| KnotJob practicalities | requires **Java 23** for the jar (source builds on Java 11; an older Java 8 build has fewer invariants). **No documented CLI/batch mode and no documented input formats or size limits** | — | **[V]** — the page simply does not say. Budget time to script around a GUI, or read the bundled source |
| X-torsion order (Khovanov) ⇒ fusion-number lower bound | KnotJob; Schütz arXiv:2412.05156 | — | **[PV]** — DG computed it for all of PS19 over Q, F₃, F₅ **[V, read in DG]** |
| **s̃_c (LEO) is the strongest** | DG cite Dunfield–Lipshitz–Schütz §6: if any of s_Q, s_{F₂}, s_{F₃}, s_o^{Sq¹} obstructs, so does s̃_c | — | **[V, read in DG]** — so run s̃_c, not the four separately |
| Υ (Upsilon) | **no verified tool.** Candidates: arXiv:2002.09210 *An algorithm for computing the Υ-invariant and the d-invariants of Dehn surgeries* | — | **[PV] paper only — no repo confirmed.** See the §6 caveat about UV=0 vs CFK^∞ |
| ν⁺ | — | — | **[U]** no tool confirmed |
| d-invariants of Σ₂ | assemble by hand | `Manifold.covers(2,cover_type='cyclic')` for homology **[V]** | **[U]** for the d-invariants themselves |
| Levine–Tristram signatures | Sage from `Link.seifert_matrix()`: eigen-signature of (1-ω)V + (1-ω̄)Vᵀ | ~20 lines | **[V]** the matrix is available (Sage-only); the σ_ω loop is yours to write |
| Casson–Gordon / Herald–Kirk–Livingston metabelian | **`Manifold.slice_obstruction_HKL`** | §5 | **[V]** |
| twisted Alexander | `Manifold.hyperbolic_torsion()` etc. | §5 | **[V]** Sage-only |
| Khoca | — | — | **[U]** — I did not verify Khoca this session. Prefer KnotJob, which DG actually used |

---

## 10. Feasibility, hardware, and where it blows up

Measured on one ordinary Linux box, single core, CPython 3.11 + snappy 3.3.2 + regina 7.4:

| computation | object | measured | verdict |
|---|---|---|---|
| HFK | 18nh00000601 (18 cr) | **< 0.01 s** | trivial |
| HFK + UV=0 complex | 18nh00000601 | < 0.1 s, 25 gens / 28 diffs | trivial |
| HFK | `ExampleLink.gst()` (48 cr) | **0.6 s**, total_rank 189 | easy |
| exterior + volume | 18 cr → 14 tets | < 0.1 s | trivial |
| exterior + volume | 48 cr → 28 tets | < 0.1 s | trivial |
| cyclic covers n=2,3,5 + H₁ | 18 cr | < 1 s | trivial |
| `verify_hyperbolicity()` (interval arithmetic **proof**) | 18 cr | < 1 s, True | trivial |
| PD→SnapPy→Regina round-trip + `is_isometric_to` | 48 cr | < 1 s | trivial |
| `simplifyExhaustive()` + `isSolidTorus()` | `ExampleLink.gordian()` (hard unknot) | **timed out > 110 s** | **expensive — the real bottleneck** |
| Range-fetch + decompress Burton row 601 | 1.33 GB file | **~3 MB downloaded, seconds** | trivial with the Range trick |

**Where it actually blows up, in priority order.**

1. **Unknot/unlink certification on adversarial diagrams** (measured above). This is the rigor
   bottleneck of the whole derivative-link lane, not HFK.
2. **Band search combinatorics.** DG's cost model: 100 CPU-years over 5 calendar years for 3.87 M
   knots to 4 bands, and it still failed on this one knot. Ribbon-disk band counts they found:
   1 band 1,249,604 (76.5 %), 2 bands 381,869 (23.4 %), 3 bands 2,238 (0.14 %), 4 bands 75
   (0.0045 %) **[V, read from DG Table 7]**. Extending to 5 bands is a different order of problem,
   and "5 bands" is precisely where 18nh00000601 might live.
3. **Monodromy extraction at genus 5** (§3) — an inverse search, not a computation.
4. **Metabolizers: not a bottleneck for this knot.** H₁(Σ₂) = **Z/25 cyclic** ⇒ **one** candidate
   metabolizer; Σ₃ ≤ 8; Σ₅ ≤ 32 **[V, computed]**. The integral rank-10 Lagrangian problem is
   infinite and must be bounded artificially — but the branched-cover reduction makes the
   arithmetic free. Spend the compute on realising curves on Σ₅ and recognising the derivative
   link, not on lattice enumeration.
5. **HFK is not a bottleneck at all** at these crossing numbers. Stop worrying about it.

---

## 11. Proposed environment spec

The decisive constraint is §0.3: **SageMath is mandatory**, because `ribbon_concordant_links`,
`slice_obstruction_HKL`, `seifert_matrix`, `signature` and `hyperbolic_torsion` are all
`@sage_method`.

```yaml
# environment.yml  — conda-forge is the reliable route to Sage + SnapPy together
name: sr-foxy
channels: [conda-forge]
dependencies:
  - python=3.11
  - sage=10.7               # [V] sagemath-standard 10.7 is current on PyPI; conda-forge preferred
  - pip
  - openjdk>=23             # [V] KnotJob's jar requires Java 23
  - pip:
      - snappy==3.3.2          # [V] installed and exercised
      - snappy_15_knots        # [PV] optional: extends HTLinkExteriors to 15-crossing knots
      - regina==7.4.1          # [V] 7.4 installed and exercised (7.4.1 is latest on PyPI)
      - knot-floer-homology    # [PV] standalone Szabó wrapper; SnapPy already bundles it
      - pypi: pypdf, requests, numpy, networkx   # glue
```

Alternative if conda is unavailable: **`passagemath-*` wheels on PyPI** (10.8.11 current **[V, saw
the version list]**) give a pip-installable Sage distribution. Untested against SnapPy's
`sage_method` detection — **verify `snappy.sage_helper._within_sage is True` before trusting it**.

Not pip-installable, install separately:

| component | source | note |
|---|---|---|
| **GAP 4.13.1+** with **`nq`** and **`lpres`** | gap-system.org; `github.com/gap-packages/nq` | DG used GAP 4.13.1 **[V]**. Only needed for §5 nilpotent quotients |
| **KnotJob** (gray version) | `https://www.maths.dur.ac.uk/users/dirk.schuetz/knotjob.html` | Java 23 jar + source (Java 11). **GUI; no documented batch mode** **[V]** |
| **KLO 0.979 alpha** | `http://www.klo-software.net` | **Windows / macOS-Intel only — no Linux.** GUI-only **[PV]** |
| **ruehlef/ribbon** | `pip install --user git+https://github.com/ruehlef/ribbon.git` | Python **3.8–3.10** only; closed-source Cython core. **Isolate in its own venv** **[V]** |
| **CFK-immersed-curves** | `github.com/hanselman/CFK-immersed-curves` | **Python 2.7, no license** — vendor and port **[PV]** |
| **flipper / curver / Twister** | PyPI (Mark Bell) | for §3 mapping classes **[PV]** |
| **Magma** | commercial | DG note it is the only implementation of Galois groups over non-Q base fields **[V, read in DG]**; they also show how to *avoid* needing it (DG Lemma 3.19). **Try hard to avoid this dependency** |

Data to stage locally:

| artifact | size | URL |
|---|---|---|
| DG code + data | **1,022,355,830 B** | `doi:10.7910/DVN/YBDTBT` (single file `plausibly_slice_V1.zip`) |
| Burton `18n-hyp.csv.bz2` | **1,330,480,533 B** | `https://people.smp.uq.edu.au/BenjaminBurton/knots/18n-hyp.csv.bz2` (supports Range) |
| Burton `all_13-16.tar.bz2` | 41 MB | same directory |
| Owens–Swenton `.rb` ribbon disks | ≤8.2 MB per crossing file | `https://cat.middlebury.edu/~mathanimations/klo/ribbondisks/` |

---

## 12. First 10 scripts the campaign should write

Each entry gives **inputs → outputs** and a **rigor note** separating *proof* from *search*. The
ordering is dependency-respecting: 01–03 are cheap and unblock everything else.

---

**01 — `fetch_census_row.py` — canonical knot loader**
*In:* a Burton name (`18nh00000601`, `19nh000077044`, …).
*Out:* `{name, knot_sig, dt_code, regina_pd, snappy_pd, signed_dt, braid_word}` as JSON, cached.
*How:* HTTP Range request into `NNx-hyp.csv.bz2` (bzip2 blocks decompress independently and the CSV
is index-sorted), then `regina.Link.fromKnotSig` → `pdData()` → `snappy.Link`.
*Rigor:* **Certifies nothing mathematical.** It is a data-fidelity script. Its one real job is the
round-trip assertion `regina.Link.fromDT(dt).knotSig() == knot_sig` (**[V]** — holds for our target)
plus `snappy_exterior.is_isometric_to(regina_complement)` (**[V]** — holds for gst()). If either
fails, every downstream number is garbage.

**02 — `invariant_card.py` — one-page dossier per knot**
*In:* a knot from 01. *Out:* a row with genus, fibered, τ, ε, ν, total_rank, HFK ranks, Δ, det,
signature, volume, tetrahedra, `verify_hyperbolicity`, H₁(Σ₂/Σ₃/Σ₅).
*Rigor:* HFK values are **exact** (Szabó's algorithm over F_p, p<2¹⁵ — but note these are
characteristic-p answers; τ/ε over F₂ by default). `verify_hyperbolicity()` is a **proof** by
interval arithmetic. Volume is a **numerical approximation** — never compare volumes for equality,
use `is_isometric_to`.

**03 — `env_assert.py` — refuse to run in the wrong interpreter**
*In:* nothing. *Out:* exit 0/1 plus a report.
*How:* assert `snappy.sage_helper._within_sage is True`; call `Link('K6a3').ribbon_concordant_links(max_twists=1)`
and require it not to raise `SageNotAvailable`; assert `regina.__version__`, Java ≥23 on PATH.
*Rigor:* pure hygiene — but it converts the §0.3 failure mode from "a silent six-hour detour" into
"a five-second error." Write this **first**.

**04 — `band_search.py` — the DG search, driven hard at one knot**
*In:* knot; a grid over `max_bands ∈ {1..5}`, `max_twists`, `max_band_len`, `paths ∈ {shortest, simple}`,
and a corpus of shaken/alternative diagrams.
*Out:* for each hit, the certificate `[D₁,b₁,D₂,…,'unknot']`; otherwise a negative record stamped
with the exact parameter box searched.
*How:* `Link.ribbon_concordant_links(..., certificates=True, filter_for_plausibly_slice=True)`
(Sage-only), short-cutting through `snappy.RibbonLinks` (12,184 entries).
*Rigor:* **A positive result is a certificate; a negative result is only the statement "no ribbon
disk exists inside this parameter box from these diagrams."** Record the box in the output schema,
because that box *is* the result. DG already searched to 4 bands and found nothing — this script
earns its keep only by going to 5 bands or by feeding in diagrams DG did not generate.

**05 — `verify_certificate.py` — the proof-grade checker**
*In:* a certificate from 04 (or one lifted out of DG's `plausibly_slice_V1.zip`).
*Out:* PASS / FAIL / INCONCLUSIVE, per step.
*How:* `spherogram.links.bands.verify_ribbon_to_unknot(link, cert)`, **plus** an independent
belt-and-braces pass: for each claimed isotopy, `is_isometric_to` on hyperbolic exteriors, and for
the terminal unlink, Regina `complement().simplify().isHandlebody(n)`.
*Rigor:* **This is the only script in the list that can prove ribbon-ness.** Its documented failure
mode is non-hyperbolic intermediate links (the docstring says so outright) — that is exactly why the
Regina fallback is not optional. Classify such cases INCONCLUSIVE, never PASS.

**06 — `unlink_certify.py` — reusable rigorous unlink oracle**
*In:* a link diagram. *Out:* `UNLINK(n)` / `NOT_UNLINK` / `TIMEOUT`, with the witness.
*How:* `snappy.Link.simplify('global')` → `deconnect_sum` / `split_link_diagram` →
`regina.Link.simplify()` → `simplifyExhaustive()` under a wall clock → `complement().isHandlebody(n)`
(or `isSolidTorus()` for n=1).
*Rigor:* `isHandlebody`/`isSolidTorus` are **normal-surface decision procedures — proofs**.
`simplify` reaching 0 crossings is a **heuristic**. **`TIMEOUT` must be a distinct return value and
must never be silently coerced to `NOT_UNLINK`** — measured: `gordian()` exceeded 110 s.

**07 — `obstruction_battery.py` — kill candidates cheaply before spending on search**
*In:* knot list. *Out:* per-knot verdict + which test fired.
*How:* Fox–Milnor + σ (`snappy.snap.fox_milnor.fox_milnor_test`); then
`Manifold.slice_obstruction_HKL(spec, method='advanced')` over a (p,q) grid; then shell out to
KnotJob for s̃_c (DG: s̃_c dominates s_Q, s_{F₂}, s_{F₃}, s_o^{Sq¹}) and the X-torsion order for a
fusion-number lower bound.
*Rigor:* Every firing test is a **proof of non-sliceness** (topological for HKL, smooth for s̃_c).
Silence proves nothing. DG's own finding is worth encoding as the default ordering: **HKL was ~6.6×
as effective as all smooth obstructions combined, so run HKL first even when you only care about
smooth sliceness** **[V, read in DG §1.10]**.

**08 — `metabolizers.py` — derivative-link enumeration for the genus-5 lane**
*In:* `Link.seifert_matrix()` (Sage) and the cyclic-cover homology from 02.
*Out:* candidate metabolizers, curve systems on Σ₅, and the resulting derivative links.
*How:* branched-cover side first — H₁(Σ₂)=Z/25 gives **exactly one** candidate, Σ₃ ≤ 8, Σ₅ ≤ 32
(**[V, computed]**). Integral side: `matrix(ZZ).smith_form()`, kernel/saturation, bounded-height
Lagrangian enumeration.
*Rigor:* The finite branched-cover enumeration is **complete**. The integral Lagrangian enumeration
is **inherently incomplete** (infinitely many Lagrangians; the bound is arbitrary) — and realising
an algebraic metabolizer as an *embedded* multicurve on the surface is an extra, unautomated step.
Label every output with which regime produced it. Pipe every derivative link through **06**.

**09 — `gst_family.py` — build and separate the GST band sums**
*In:* `regina.ExampleLink.gst()` as ground truth; parameters (n,k) / (p,q;c/d).
*Out:* PD codes for L_{n,k}, invariant cards, pairwise `is_isometric_to` / isometry-signature
comparisons.
*First task, before anything else:* **resolve the §0.2 discrepancy** — Regina's `gst()` computes as
genus 10, **non-fibered**, Δ of degree 16, vol 23.8448997956. Reconcile against GST Figure 2 by hand.
*Then:* reimplement Diao–Pan–Yan's construction (arXiv:2604.17737) — or, far cheaper, **email the
authors for the code**, since they state the algorithm is deferred to a future paper and released
nothing.
*Rigor:* `is_isometric_to` on hyperbolic exteriors is a **rigorous** distinctness proof; equal
volumes are **not**. Stable-handleslide-triviality results are **searches**, bounded in their paper
at n≤36, d≤39.

**10 — `annulus_twist.py` — the A_n(6₃) generator**
*In:* a base knot with an annulus presentation, plus n. *Out:* PD codes for A_n(K) and invariant cards.
*How:* implement the twist as a **local PD surgery** in spherogram/Regina — no package exists
(**[V, by absence]**), and none is needed; it is a diagram operation.
*Rigor:* The construction is **exact** (a definition, not a search). The concordance claims about
the family are **not** — they route back through 07 and, for [K_n]=[K_m], through the §9 battery.
⚠️ **Pin down the source first:** most of the literature attaches the annulus-twist slice family to
**8₂₀** (and proves those K_n ribbon); the **6₃** presentation shows up in the
characterizing-slopes setting. Confirm which family the campaign means — via Abe–Tagami
arXiv:1502.01102 — before writing a line.

---

## 13. Residual unknowns — things I could not verify, stated as such

1. **Whether γ₀ (Hom–Park) is computable from SnapPy's UV=0 complex.** SnapPy returns
   CFK_{UV=0}, not CFK^∞. Whether that determines γ₀ (or Υ) is **[U]**. Settle mathematically
   before scripting.
2. **Regina's `gst()` fiberedness discrepancy** (§0.2) — computation **[V]**, cause **[U]**.
3. **Which Abe–Tagami family "A_n(6₃)" denotes** — the literature I reached foregrounds 8₂₀ **[U]**.
4. **Kjuchukova–Orr arXiv:2604.00460 code availability** — no repo found, not proven absent **[U]**.
5. **KnotJob batch/CLI interface, input formats, crossing limits** — the page is silent **[V that it
   is silent; U as to the answer]**. Read the bundled source.
6. **Khoca** — not verified this session **[U]**. KnotJob is the tool DG actually used; prefer it.
7. **`passagemath` wheels + SnapPy's `_within_sage` detection** — untested **[U]**.
8. **Bar-Natan `KnotTheory\`` current state** — not reached **[U]**.
9. **Υ and ν⁺ implementations** — arXiv:2002.09210 describes an algorithm; **no repo confirmed [U]**.
10. **d-invariants of double branched covers** — no end-to-end tool found **[U]**; SnapPy gives the
    covers' homology **[V]** but not HF⁺ of the closed cover.

---

## Sources

- [Dunfield & Gong, *Ribbon concordances and slice obstructions*, arXiv:2512.21825](https://arxiv.org/abs/2512.21825)
- [Dunfield & Gong, code and data, Harvard Dataverse doi:10.7910/DVN/YBDTBT](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/YBDTBT)
- [Oliveira-Smith, *A Dunfield–Gong 4-Sphere is Standard*, arXiv:2603.23717](https://arxiv.org/abs/2603.23717)
- [Regina — Supporting Data (knot census, naming convention, download URLs)](https://regina-normal.github.io/data.html)
- [Burton, *The Next 350 Million Knots*, SoCG 2020](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2020.25)
- [SnapPy — Census manifolds](https://snappy.computop.org/censuses.html)
- [SnapPy](http://snappy.computop.org)
- [ruehlef/ribbon — GHMR band search code](https://github.com/ruehlef/ribbon)
- [Gukov–Halverson–Manolescu–Ruehle, *Searching for ribbons with machine learning*, arXiv:2304.09304](https://arxiv.org/abs/2304.09304)
- [KnotJob (Dirk Schütz)](https://www.maths.dur.ac.uk/users/dirk.schuetz/knotjob.html)
- [KLO / Kirby Calculator (Frank Swenton)](https://community.middlebury.edu/~mathanimations/klo)
- [Owens/Swenton ribbon disk data](https://cat.middlebury.edu/~mathanimations/klo/ribbondisks/)
- [Owens & Swenton, *An algorithm to find ribbon disks for alternating knots*, arXiv:2102.11778](https://arxiv.org/pdf/2102.11778)
- [Agol & Ren, *Ribbon concordance of fibered knots and compressions of surface homeomorphisms*, arXiv:2603.10884](https://arxiv.org/abs/2603.10884)
- [Diao, Pan & Yan, *Stable equivalence of GST Links*, arXiv:2604.17737](https://arxiv.org/abs/2604.17737)
- [Abe & Tagami, *Fibered knots with the same 0-surgery and the slice-ribbon conjecture*, arXiv:1502.01102](https://arxiv.org/abs/1502.01102)
- [hanselman/CFK-immersed-curves](https://github.com/hanselman/CFK-immersed-curves)
- [3-manifolds/knot_floer_homology](https://github.com/3-manifolds/knot_floer_homology)
- [gap-packages/nq](https://github.com/gap-packages/nq)
- [GAP lpres package manual](https://docs.gap-system.org/pkg/lpres/doc/chap1.html)
- [Kjuchukova & Orr, *Extending Quotients of Knot Groups Over Surfaces in B⁴*, arXiv:2604.00460](https://arxiv.org/html/2604.00460)
- [Mark Bell — software (flipper, curver, Twister)](https://www.markcbell.co.uk/_sources/software.rst.txt)
- [CompuTop.org software archive](https://nmd.web.illinois.edu/computop/)
- [KnotInfo](https://knotinfo.org/descriptions/crossing_number.html)
