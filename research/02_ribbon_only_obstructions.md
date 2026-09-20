# Catalog of Necessary Conditions for Ribbonness — Which Are Genuinely "Ribbon-Only"?

**Survey date:** 2026-09-11. **Target question:** find necessary conditions for a knot to be *ribbon*
that are (or might be) strictly stronger than *handle-ribbon* (= strongly homotopy-ribbon), so that they
could obstruct ribbonness of the current candidates (18nh00000601, GST band sums), which are already
**proved** handle-ribbon.

**Evidence labels used throughout:**
- **VERIFIED** — I read the primary text (arXiv full text / ar5iv HTML rendering of the paper) and the
  statement below is quoted or closely paraphrased from it.
- **PARTIALLY VERIFIED** — abstract or a reliable secondary citation only; statement not read in the
  primary source.
- **UNVERIFIED** — inferred, reported second-hand, or my own reasoning not backed by a read source.

Nothing below is invented; where I could not confirm a theorem number I say so explicitly.

---

## 0. Executive answer to the crux question

> *Is there ANY known invariant `I` with a theorem "K ribbon ⇒ I(K)=0" for which it is NOT also known
> that "K handle-ribbon ⇒ I(K)=0"?*

**Short answer: essentially no — for knots, I found no numerical/homological invariant `I` with a
vanishing theorem at the ribbon level that is not already known (or not trivially seen) to vanish at the
handle-ribbon level.** Every candidate I checked either (a) was explicitly upgraded to handle-ribbon /
homotopy-ribbon in the literature, or (b) is a *characterization* rather than a computable invariant, or
(c) is a *link* statement that degenerates for knots, or (d) is not of vanishing type (it bounds an
auxiliary quantity that only exists once you already know the knot is ribbon).

The three things that come closest to being genuinely ribbon-only are:

| # | Tool | Status |
|---|------|--------|
| **A** | **Miller–Zupan Prop. 1.1 + Thm 1.3** (unlink derivative vs R-link derivative) | The *only* clean, exactly-calibrated separator of ribbon from handle-ribbon. Not an invariant; it converts "non-ribbon" into "no Seifert surface of K carries an unlink derivative", which is an infinite search. **VERIFIED.** |
| **B** | **Eisermann's Jones-nullity / determinant theorems for ribbon LINKS** | Proof genuinely uses the band/ribbon combinatorics; no handle-ribbon or slice version is known. **But for a 1-component link (a knot) both statements are vacuous/implied.** Useless for our knot candidates; potentially alive for link versions. **VERIFIED (statements) / UNVERIFIED (that no handle-ribbon proof exists — it is simply absent from the literature).** |
| **C** | **Fusion number `F(K)` and its lower bounds (Juhász–Miller–Zemke torsion order; Friedl–Misev–Zupan ribbon-number bounds)** | Genuinely ribbon-only *data*: Aceto–Bodnár–et al./Hom-style cabling results show `F` and the handle-ribbon analogue `F_sh` differ arbitrarily. But these are *lower bounds on a quantity defined only for ribbon knots*, not vanishing obstructions, so they cannot show a knot is non-ribbon without an independent upper bound on `F`. **VERIFIED.** |

Everything else in the catalog dies at slice, homotopy-ribbon, or handle-ribbon level.

---

## 1. Summary table

| Obstruction / condition | Source | Dies at which level | Computable? | Ever applied to a candidate? |
|---|---|---|---|---|
| Fox–Milnor Δ(t)=f(t)f(t⁻¹); signatures; Arf; det=square | classical | **slice** | yes (Seifert matrix) | yes; all pass |
| Casson–Gordon invariants; metabelian/η/L²-η invariants; Cappell–Shaneson Rohlin of dihedral covers | Casson–Gordon 1978/86; Friedl math/0305402 | **slice** | yes in principle | yes; vanish |
| Kjuchukova Ξ_p ("ribbon obstruction for p-colored knots") | Kjuchukova; Cahn–Kjuchukova [arXiv:1812.09553], Fund. Math. 2021 | **homotopy-ribbon** (theorem is stated for homotopy ribbon) | yes: algorithm from colored diagram + Seifert surface + characteristic knot + linking numbers in dihedral cover | computed on 6₁, 8₁₁; **not** on GST/18nh knots (no record found) |
| Park–Powell Z[Z]-homology-ribbon obstruction / triple linking of derivatives | [arXiv:1802.00582], Israel J. Math | **≤ homotopy-ribbon** (Z[Z]-homology ribbon) | yes (Seifert surface, Milnor invariants) | no |
| Casson–Gordon: fibered ⇒ monodromy extends over a handlebody | Casson–Gordon, Invent. Math. 74 (1983) 119–137 | **homotopy-ribbon** (explicitly) | yes for fibered knots (Casson–Long algorithm; Agol–Ren generalization) | yes — GST/18nh knots are fibered and DO extend |
| Miller–Zupan: handle-ribbon ⟺ R-link derivative ⟺ singular fibration of 0-surgery extending over handlebodies | [arXiv:2005.11243], Comm. Anal. Geom. | **handle-ribbon** (it *is* the handle-ribbon criterion) | partially | yes — this is how candidates are certified handle-ribbon |
| **Miller–Zupan Prop 1.1: ribbon ⟺ unlink derivative** | [arXiv:2005.11243] | **RIBBON-ONLY** | not a finite algorithm (must range over all Seifert surfaces / all derivatives) | conceptually: GST links are R-links not known to be unlinks |
| Zemke: HFK injectivity under ribbon concordance | [arXiv:1902.04050] | **handle-ribbon** (Miller–Zemke [arXiv:1903.05772]) | yes | vacuous from the unknot |
| Levine–Zemke: Khovanov injectivity under ribbon concordance | [arXiv:1903.01546] | **handle-ribbon** (Gujral–Levine [arXiv:2009.03406]) | yes | vacuous from the unknot |
| Kang: injectivity for KhR / conic strong Khovanov–Floer theories | [arXiv:1909.06969] | ribbon (as stated); superseded in scope by Gujral–Levine for Kh | yes | vacuous from the unknot |
| Daemi–Lidman–Vela-Vick–Wong: ribbon homology cobordism obstructions (instanton, HF, character varieties, geometry) | [arXiv:1904.09721], Adv. Math. 408 (2022) | **handle-ribbon by definition** ("only 1- and 2-handles") | partly | no |
| Agol: ribbon concordance is a partial order | [arXiv:2201.03626] | ribbon; argument also gives strongly homotopy-ribbon partial order (stated in Baldwin–Sivek) | — | vacuous from the unknot |
| Baldwin–Sivek: finitely many hyperbolic fibered predecessors | [arXiv:2510.02214]; II: [arXiv:2602.21109] | **handle-ribbon** (their Remark 1.6 says proofs go through) | no algorithm claimed | no |
| Agol–Ren: simplicial volume & dilatation monotone under ribbon concordance of fibered knots; finitely many predecessors; algorithm for minimal compressions | [arXiv:2603.10884] (2026) | **handle-ribbon** (authors state results strengthen to ≤_h) | yes for the compression algorithm | no |
| Baker / Miyazaki minimality of tight fibered knots; connected sums of fibered knots ribbon ⇒ K#−K | Baker, J. Topol. 9 (2016); Miyazaki 1994; Baldwin–Sivek [arXiv:2210.04044] | **homotopy-ribbon** (Baker's argument is homotopy-ribbon) | yes (fiberedness, tightness) | no (candidates are not of this form) |
| Hom–Park: connected sums of γ₀-sharp fibered knots ribbon ⟺ K#−K | [arXiv:2507.20455] (2025) | uses homotopy-ribbon minimality + Miyazaki; **likely homotopy-ribbon**, not verified to be ribbon-only | yes (needs γ₀, fiberedness) | no |
| Eisermann: null V(L) = n−1 for ribbon links | [arXiv:0802.2287], G&T 13 (2009) | **RIBBON-ONLY as proved**, but vacuous for knots (n=1) | yes (Jones polynomial) | n/a for knots |
| Eisermann: det V(L) ≡ det(K₁)···det(Kₙ) mod 32, ≡1 mod 8 | same | same; for a knot reduces to det ≡ 1 mod 8, implied by det = square (all slice knots) | yes | n/a |
| Juhász–Miller–Zemke: Ord_U(K) ≤ F(K) (fusion number) | [arXiv:1904.02735] | bounds **F**, not **F_sh**; genuinely ribbon-level data but **not a vanishing obstruction** | yes (HFK torsion order) | no |
| Fusion number vs strong homotopy fusion number separation (F_sh=1, F=p for (p,1)-cables) | [arXiv:2003.02832] | **demonstrates ribbon-data ≠ handle-ribbon-data** | yes | no |
| Friedl–Misev–Zupan: lower bounds on ribbon number r(K) from det and Δ; finiteness/computability of {Δ : r ≤ r₀} | [arXiv:2408.11618] | **ribbon-only** (r(K) is defined only via ribbon disks) but bounds r, does not obstruct ribbonness | yes | no |
| Sarkar ribbon distance from Lee homology; Alishahi(-Dowlin)/Bar-Natan/α-homology versions | [arXiv:1903.11095]; [arXiv:2011.01190] | bounds number of saddles in a **ribbon** concordance; ribbon-level data, not a vanishing obstruction | yes | no |
| Grigsby: braid conjugacy class / Rudolph braided-banded surface ribbon obstructions | [arXiv:1801.07158] | aimed at ribbon-only; **author reports the Khovanov–Lee implementation gives no effective obstruction** | no | no |
| Turaev, "Multiplace generalizations of the Seifert form", Theorem H | Math. USSR Sb. 44(3) (1983) 335–361 | **UNKNOWN — possibly ribbon-only; essentially uncited** | unknown | no |
| Gilmer: ribbon concordance ⇒ partial order on S-equivalence classes / Alexander polynomial divisibility | Topology Appl. 18 (1984) 313–324 | ribbon concordance; likely extends to homotopy-ribbon (Alexander-module-level) — UNVERIFIED | yes (Seifert form) | vacuous from the unknot |
| Equivariant sliceness/ribbonness obstructions (Boyle–Issa, Dai–Mallick–Stoffregen, Di Prisa, Miller) | see §8 | obstruct **equivariant** ribbon/slice only | yes | no — and logically cannot obstruct plain ribbonness |
| Cornwell–Ng–Sivek Lagrangian concordance obstructions | [arXiv:1411.1364] | Lagrangian (Legendrian) category; opposite direction | yes (rulings) | no |
| Gompf/Andrews–Curtis: ribbon disk exterior handle presentations | see §10 | **handle-ribbon** (the AC/handle-slide data is exactly the handle-ribbon data) | AC-triviality undecidable in general | GST links: stable handleslide experiments [arXiv:2604.17737] |
| Beliakova–De Renzi–Faes quantum invariants of ribbon surfaces in 4-d 2-handlebodies | [arXiv:2512.15395] (2025) | invariants **of a given ribbon surface**, not of the knot; no existence obstruction | in principle | no |

---

## 2. Item-by-item

### 2.1 Miller–Zupan: unlink derivative vs R-link derivative (the exact ribbon/handle-ribbon gap)

**Source:** Maggie Miller, Alexander Zupan, *Equivalent characterizations of handle-ribbon knots*,
[arXiv:2005.11243], to appear/appeared in Comm. Anal. Geom.

**Statements (VERIFIED, read via ar5iv full text):**
- *Definition.* A **derivative** for `K` on a genus-`g` Seifert surface `F` is a `g`-component link
  `L ⊂ F` such that `F − L` is a connected planar surface and `lk(L_i, L_j^+) = 0` for all `i,j`.
  (`K` has a derivative iff `K` is algebraically slice.)
- *Definition.* An `n`-component link `L ⊂ S³` is an **R-link** if 0-surgery on every component yields
  `#ⁿ(S¹×S²)`.
- **Proposition 1.1.** "*A knot `K ⊂ S³` is ribbon if and only if `K` has an unlink derivative `U`.*"
- **Theorem 1.3.** "*A knot `K ⊂ S³` is handle-ribbon in a homotopy 4-ball if and only if `K` has an
  R-link derivative.*"
- **Theorem 1.5.** "*A knot `K ⊂ S³` is handle-ribbon in a homotopy 4-ball if and only if there exists a
  singular fibration of the 0-surgery on `K` that extends over handlebodies.*"
- **Theorem 2.5** (their statement of Casson–Gordon): "*A fibered knot `K ⊂ S³` is **homotopy-ribbon** in
  a homotopy 4-ball `B` if and only if the closed monodromy associated to `K` extends over a handlebody
  `H`.*"  ← note **homotopy-ribbon**, not ribbon.
- Hierarchy stated: `{ribbon} ⊂ {handle-ribbon} ⊂ {homotopy-ribbon} ⊂ {slice}`, and "*none of these
  containments is known to be strict.*"
- Remark 2.2: they prefer "handle-ribbon" to "strongly homotopy-ribbon" because it is the *handle
  decomposition* of the complement (no 3-handles) that is being asserted.

**What the gap is, precisely.** Unlink ⊂ R-link always. So:

> `K` ribbon ⟺ some derivative of `K` is an **unlink**;
> `K` handle-ribbon ⟺ some derivative of `K` is an **R-link**.

Therefore the ribbon-vs-handle-ribbon gap for a fixed knot is *exactly*: can every R-link derivative be
traded for an unlink derivative? A **Generalized Property R** (Kirby Problem 1.82) failure is precisely
an R-link that is not an unlink. This is the sharpest known formulation of a ribbon-only obstruction.
(VERIFIED for the two equivalences; the "therefore" is my own — UNVERIFIED as a literature statement,
though it is immediate.)

**Computability.** *Not* a finite algorithm as stated. To *prove* non-ribbon one must show that **no**
derivative on **any** Seifert surface (including arbitrarily stabilized ones) is an unlink. There is no
known finiteness theorem for the set of derivatives of a fixed knot. Even recognizing the unlink is
decidable (Haken), but the search space is infinite.

**"Which derivatives does a knot have?" literature:**
- Cochran–Davis, *Counterexamples to Kauffman's conjectures on slice knots*, [arXiv:1303.4418], Adv.
  Math. 274 (2015): there is a smoothly slice knot none of whose derivatives is slice. **PARTIALLY
  VERIFIED** (abstract/secondary). This is the key warning that "derivative of a slice knot" is a weak
  handle.
- Cha–Kim (and others), *Cut open null-bordisms and derivatives of slice knots*, [arXiv:1511.07295];
  *Milnor's triple linking numbers and derivatives of genus three knots*, [arXiv:1603.09163]; Park–Powell
  [arXiv:1802.00582] — all bound Milnor-invariant data of derivatives of homotopy-ribbon/doubly-slice
  knots. **PARTIALLY VERIFIED.** Park–Powell is explicitly a `Z[Z]`-homology-ribbon obstruction, hence
  weaker than homotopy-ribbon ⇒ **dead for our targets.**
- I found **no** paper that bounds or classifies the full set of derivative links of a fixed knot. This
  is the main missing ingredient for turning Prop 1.1 into a usable obstruction.

**Relation to the candidates.** Gompf–Scharlemann–Thompson, *Fibered knots and potential counterexamples
to the Property 2R and Slice-Ribbon Conjectures*, [arXiv:1103.1601], G&T 14 (2010) 2305–2347, construct a
family of R-links (the "GST links") that are probably not unlinks, and band sums along them give slice
knots not known to be ribbon. **PARTIALLY VERIFIED (abstract).** Follow-ups: Scharlemann–Thompson
*Fibered knots and Property 2R* [arXiv:0901.2319]; *Proposed Property 2R counterexamples classified*
[arXiv:1208.1299]; and, most recently, Diao–Pan–Yan, *Some experimental results on stable equivalence of
GST links for the Generalized Property R Conjecture*, [arXiv:2604.17737] (Apr 2026), who implement an
algorithm to build all these links and verify **stable handleslide triviality** for certain GST links
— i.e. they push in the direction of the links being *unlink-like*, not against it. **PARTIALLY
VERIFIED (abstract).**

### 2.2 "Is every ribbon disk of a fibered knot fibered?"

**Who states it (VERIFIED, ar5iv full text):** Meier–Zupan, *Knots bounding non-isotopic ribbon disks*,
[arXiv:2310.17564] (J. Topology 2025) state verbatim: "*It is an open question whether every ribbon disk
bounded by a fibered knot is a fibered, ribbon disk.*" They also say of their own construction: "*We do
not know whether the disk `D_{c/d}` bounded by `Q_{p,q}` is ribbon in general*", and their Theorem 1.3
produces infinitely many pairwise non-isotopic **fibered homotopy-ribbon** disks on every generalized
square knot `T_{p,q} # \bar T_{p,q}` with diffeomorphic exteriors; Theorem 1.6 shows `D_{2/(2m+1)}` on
`Q_{2k+1,2}` are ribbon.

**Antecedents and partial results:**
- **Casson–Gordon**, *A loop theorem for duality spaces and fibred ribbon knots*, Invent. Math. 74 (1983)
  119–137: main application is that a fibred knot which is (homotopy-)ribbon has monodromy extending over
  a handlebody. **PARTIALLY VERIFIED** from the journal abstract, which phrases it as "if a fibred knot
  in `S³` is a ribbon knot, then its monodromy extends over a handlebody"; but Miller–Zupan's Theorem 2.5
  (VERIFIED) states the sharp iff form with **homotopy-ribbon**. So: **dead for our targets** (a
  handle-ribbon knot is homotopy-ribbon, so its monodromy already extends).
- **Larson–Meier**, *Fibered ribbon disks*, [arXiv:1410.4854], J. Knot Theory Ramifications: characterize
  fibered homotopy-ribbon disks (fibers = handlebodies), give Stallings-twist analogues, and produce
  infinite families of distinct homotopy-ribbon disks with homotopy equivalent exteriors, "with potential
  relevance to the Slice-Ribbon Conjecture." **PARTIALLY VERIFIED (abstract).**
- **Meier**, *Extending fibrations on knot complements to ribbon disk complements*, [arXiv:1811.09639]:
  for prime fibered ribbon knots with ≤12 crossings, `K` bounds a ribbon disk `D` with `S⁴ ∖ ν(D)`
  fibered by handlebodies; every fibered ribbon 2-bridge knot bounds a fibered ribbon disk. **PARTIALLY
  VERIFIED (search snippet + title; not read in primary).**
- **Lecuona et al.**, *Fibered ribbon pretzels*, [arXiv:2408.03644] / Bull. LMS 2026. **PARTIALLY
  VERIFIED.**
- **Miyazaki**, *Nonsimple, ribbon fibered knots*, Trans. AMS (1994) — connected sums of iterated cables
  of torus knots are not ribbon unless of the form `K # −K`. **PARTIALLY VERIFIED (secondary).**
- **Baker**, *A note on the concordance of fibered knots*, J. Topol. 9 (2016) 1–4: tight fibered knots are
  minimal under **homotopy-ribbon** concordance among fibered knots. Secondary sources state explicitly
  that "while Baker's result is stated for ribbon concordance, the same argument applies to homotopy
  ribbon concordance." **PARTIALLY VERIFIED.** ⇒ **dead for our targets.**
- **Hom–Park**, *Ribbon knots and iterated cables of fibered knots*, [arXiv:2507.20455] (Jul 2025):
  Theorem 1.1 "*A connected sum of γ₀-sharp fibered knots is ribbon if and only if it is of the form
  K#−K*"; Cor 1.2 "*Either distinct iterated cables of tight fibered knots are linearly independent in
  the smooth knot concordance group, or the slice-ribbon conjecture is false*"; Cor 1.3 gives knots that
  are "algebraically slice but not ribbon." **VERIFIED (statements, from the arXiv HTML).** *Caveat:* the
  machinery is minimality under **homotopy-ribbon** concordance, so I could **not** confirm this is
  ribbon-only; I read the paper's own use of "homotopy ribbon concordant" as the working notion.
  **UNVERIFIED whether Thm 1.1 upgrades to handle-ribbon.** In any case, the candidates are not connected
  sums of fibered knots, so it does not apply.
- **Rudolph**, *A non-ribbon plumbing of fibered ribbon knots*, [arXiv:math/0105257]: a plumbing of two
  fibered ribbon knots along their fiber surfaces "may be algebraically slice yet not ribbon"
  (Livingston–Melvin/Miyazaki example). **PARTIALLY VERIFIED (abstract).** Note the knot is only
  *algebraically* slice, so this is not a slice-but-not-ribbon example.

**Why this matters for us.** If "every ribbon disk of a fibered knot is fibered" were **true**, then for
fibered knots the Casson–Gordon handlebody-extension criterion, plus Casson–Long / Agol–Ren's algorithm
for minimal compressions, would in principle *decide* ribbonness of a fibered knot — and would very
plausibly collapse ribbon = homotopy-ribbon for fibered knots, killing the candidates as counterexamples.
So this open problem is the single highest-leverage item for the fibered candidates (18nh00000601 is
stated in the literature to bound a **fibered** handle-ribbon disk). (Reasoning mine — **UNVERIFIED** as
a literature claim.)

### 2.3 Turaev multiplace Seifert forms; Kawauchi; Gilmer

- **Turaev, Theorem H**, *Multiplace generalizations of the Seifert form of a classical knot*, Mat. Sb.
  116(158) (1981) 370–397 / Math. USSR Sb. 44(3) (1983) 335–361. The only pointer I could find is the
  Low Dimensional Topology blog post *Slice-Ribbon Conjecture in danger!* (D. Moskovich, 2 Dec 2010),
  which calls Theorem H "a completely different ribbon obstruction" and notes it appears to be
  essentially uncited. **I could not obtain the statement of Theorem H** — the paper is not on arXiv and
  the translation is paywalled. **UNVERIFIED.** *This is the single most promising un-checked item in the
  whole survey*: an old, uncited, explicitly ribbon-labelled obstruction from before the homotopy-ribbon
  formalism existed, so it has never been tested against handle-ribbon. **Recommended action: obtain
  Math. USSR Sb. 44 (1983) 335–361 and read Theorem H.**
- **Kawauchi**, *Ribbonness on classical link*, [arXiv:2307.16483] (2023, revised through Dec 2024), and
  *Alternative proof of the ribbonness on classical link*: claims that every link bounding a proper
  oriented surface in the upper half 4-space bounds a proper oriented **ribbon** surface, in particular
  **claims to prove the Slice–Ribbon Conjecture**. **PARTIALLY VERIFIED (abstract only).** This claim is
  **not accepted by the community** — it has not appeared in a mainstream journal, the author has posted
  successive "alternative proofs", and all 2025–2026 papers surveyed here (Agol–Ren, Baldwin–Sivek,
  Hom–Park, Dunfield–Gong, Oliveira-Smith) continue to treat slice-ribbon as open. Treat as **not a
  usable result**, but note that if one were hunting a counterexample one should know where Kawauchi's
  argument is claimed to work.
- **Kawauchi's earlier work**: the `(2,0)`-cable / parallel link `P(K)`: if `P(K)` is concordant to a
  split link then `K` is algebraically slice (*On links not cobordant to split links*). **PARTIALLY
  VERIFIED (secondary).** This is a *concordance/algebraic* statement — **dies at slice level**.
- **Gilmer**, *Ribbon concordance and a partial order on S-equivalence classes*, Topology Appl. 18 (1984)
  313–324: ribbon concordance induces a partial order on S-equivalence classes; relates the (torsion)
  Alexander polynomial to ribbon concordance. **PARTIALLY VERIFIED (secondary).** The content is
  Alexander-module/Blanchfield-level, so I expect it to hold verbatim for homotopy-ribbon concordance
  (which is defined by π₁-injectivity and hence gives the same Alexander-module surjection/injection).
  **UNVERIFIED**, but almost certainly dead for our targets. Also, applied with `J = U`, it is vacuous.
- **Gilmer**, *Slice knots in S³*, Quart. J. Math 1983 — a slice obstruction (Casson–Gordon style).
  **Dies at slice level.**

### 2.4 Eisermann, *The Jones polynomial of ribbon links*

**Source:** M. Eisermann, [arXiv:0802.2287], Geom. Topol. 13 (2009) 623–660. **VERIFIED (statements read
in ar5iv full text).**

- **Theorem 1.** "*Every `n`-component ribbon link `L` satisfies `null V(L) = n − 1`.*"
  (`V(L)` divisible by `V(Oⁿ)`; nullity = order of vanishing of `V` at `t=1` in the appropriate sense,
  equal to the Seifert nullity for ribbon links.)
- **Theorem 2.** "*Every `n`-component ribbon link `L = K₁ ∪ ⋯ ∪ Kₙ` satisfies
  `det V(L) ≡ det(K₁)⋯det(Kₙ) mod 32`, and in particular `det V(L) ≡ 1 mod 8`.*"
- Open question in §7: whether the nullity equality generalizes to all links; the ribbon (band) structure
  is essential to the inductive proof. Eisermann explicitly notes that slice-vs-ribbon is Fox's Problem 25.

**Assessment.**
- For a **knot** (`n = 1`): `V(O¹) = 1`, so divisibility is vacuous; `null V = 0` is automatic; and
  `det V(K) = det(K) ≡ 1 mod 8` follows from `det(K)` being an odd square, which holds for every
  *algebraically* slice knot (Fox–Milnor). **⇒ Completely useless for knot candidates.**
- For **links**: the proof is combinatorial in the band presentation and there is, to my knowledge, **no
  handle-ribbon or slice version**. So this is the cleanest *existing* theorem whose hypothesis is
  genuinely "ribbon" with no known upgrade. If one ever produced a **link** counterexample candidate that
  is slice/handle-ribbon, `null V` and `det V mod 32` are the tools to try first. **VERIFIED for the
  statements; UNVERIFIED for "no handle-ribbon proof exists" (absence of evidence).**
- **Eisermann–Lamm** have joint work on *symmetric unions* (e.g. "Equivalence of symmetric union
  diagrams", "Symmetric union diagrams and refined spin models"), not an extension of the Jones-nullity
  ribbon theorem. **PARTIALLY VERIFIED.** Related and recent: *A ribbon knot which is not a symmetric
  union*, [arXiv:2606.02968] (2026) — relevant to the symmetric-union heuristic, not a ribbon obstruction.
- Related: *On the colored Jones polynomials of ribbon links, boundary links and Brunnian links*,
  [arXiv:1111.6408](https://arxiv.org/abs/1111.6408) (Sakie Suzuki), Banach Center Publications 100 (2014), 213–222, DOI [10.4064/bc100-0-12](https://doi.org/10.4064/bc100-0-12). **AUTHOR AND IDEAL THEOREMS VERIFIED, 2026-09-19.** Theorem 2.2 applies to ribbon and boundary links; Theorem 3.1 gives the principal cyclotomic ideal generators. This does not assert an extension to all slice links. The earlier attribution to Habiro–Massuyeau was incorrect.

### 2.5 Ribbon number / fusion number and their lower bounds

- **Fusion number** `F(K)` = minimal number of 1-handles (bands) in a ribbon disk for `K`.
  **Strong homotopy fusion number** `F_sh(K)` = minimal number of **2-handles** in a handle decomposition
  of a ribbon disk complement; and `F_h(K)` the homotopy version. Chain: `F_h(K) ≤ F_sh(K) ≤ F(K)`.
  **VERIFIED** (read in ar5iv of [arXiv:2003.02832], *Ribbon knots, cabling, and handle decompositions*).
- **Theorem 1.1 of [arXiv:2003.02832] (VERIFIED):** "*If `K` is ribbon with `F(K)=1`, then
  `F_sh(K_{p,1})=1` and `F(K_{p,1})=p`. Furthermore, `F_sh(K_{p₁,1;…;pₙ,1})=1` and
  `F(K_{p₁,1;…;pₙ,1}) = p₁p₂⋯pₙ`.*"
  ⇒ **`F` and `F_sh` differ arbitrarily.** This is the sharpest existing demonstration that *ribbon-level
  data is strictly finer than handle-ribbon-level data*, even though the two *classes* of knots are not
  known to differ. Very relevant: it shows the "handle-ribbon can't see ribbon" phenomenon is real at the
  level of invariants.
- **Juhász–Miller–Zemke**, *Knot cobordisms, bridge index, and torsion in Floer homology*,
  [arXiv:1904.02735], J. Topology: torsion order of `HFK⁻` gives `F(J) ≥ Ord_U(J)` for ribbon `J`.
  **VERIFIED (as quoted inside 2003.02832).** Key point: their bound does **not** bound `F_sh`. So this
  is genuinely ribbon-only *data* — but it is a lower bound on a quantity that only exists once `J` is
  ribbon, so **it cannot obstruct ribbonness**.
- **Friedl–Misev–Zupan**, *Bounding the ribbon numbers of knots and links*, [arXiv:2408.11618] (2024):
  the **ribbon number** `r(K)` = minimal number of ribbon intersections over all ribbon disks. New lower
  bounds from `det(K)` and `Δ_K(t)`; **the set of Alexander polynomials of knots with ribbon number ≤ r
  is finite and computable**; ribbon numbers computed for all ribbon knots with ≤11 crossings except
  three; Jones-polynomial lower bounds for links. **PARTIALLY VERIFIED (abstract + secondary).**
  Follow-up: *Ribbon numbers of 12-crossing knots*, [arXiv:2409.12910].
  **Assessment:** this is a genuinely ribbon-only family of constraints, and it is the *only* one with a
  finiteness/computability theorem. It gives statements of the form "if `K` is ribbon with `r(K) ≤ r₀`
  then `Δ_K` lies in an explicit finite set". To obstruct ribbonness outright you would need an a priori
  upper bound on `r(K)` — **none exists**. As you note, a lower bound can never exceed an upper bound;
  the real content is the finiteness theorem, which is a *potential* route if one could ever bound `r`
  (e.g. from a handle-ribbon disk's complexity — but no such implication is known, and 2003.02832 above
  shows such implications should be expected to fail).
- **Kanenobu** and others computed fusion numbers / ribbon presentations for small knots. **PARTIALLY
  VERIFIED.**

### 2.6 Ribbon concordance order and monotone invariants — and why it is essentially vacuous here

**Definitions/facts.** `J ≤ K` iff there is a ribbon concordance (only births and saddles) from `J` to
`K`. Then **`K` is ribbon ⟺ `U ≤ K`** (cap off the unknot end with a disk). Handle-ribbon concordance
`≤_h`: complement built from `S³∖J` with only 1- and 2-handles.

**The results.**
| Result | Source | Ribbon-only? |
|---|---|---|
| Gordon: ribbon concordance ⇒ `π₁(S³∖J) ↪ π₁(S³×I ∖ C)` injective, `π₁(S³∖K) ↠` surjective; conjecture that `≤` is a partial order | Gordon, Math. Ann. 257 (1981) 157–170 | **No** — π₁-injectivity is literally the *definition* of homotopy-ribbon concordance, so the group-theoretic content is shared |
| Zemke: HFK map injective under ribbon concordance | [arXiv:1902.04050] | **No** — Miller–Zemke [arXiv:1903.05772] prove it for **strongly homotopy-ribbon** concordances (VERIFIED via abstract: "We prove that the map on knot Floer homology induced by a strongly homotopy-ribbon concordance is injective.") |
| Levine–Zemke: Khovanov injective | [arXiv:1903.01546] | **No** — Gujral–Levine, *Khovanov homology and cobordisms between split links*, [arXiv:2009.03406]: "a strongly homotopy-ribbon concordance … induces an injection on Khovanov homology, which generalizes a result of the second author and Zemke" (VERIFIED via abstract) |
| Kang: KhR, conic strong Khovanov–Floer theories | [arXiv:1909.06969] | stated for ribbon concordance; Kh case already upgraded by Gujral–Levine |
| Daemi–Lidman–Vela-Vick–Wong, *Ribbon homology cobordisms*, Adv. Math. 408 (2022) 108580, [arXiv:1904.09721] | instanton/HF/character-variety/geometrization obstructions | **No** — their definition: "a cobordism `W` from `Y₁` to `Y₂` is **ribbon** if `W` admits a handle decomposition relative to `Y₁×I` consisting of just 1- and 2-handles", i.e. **handle-ribbon by definition** (PARTIALLY VERIFIED, definition quoted from secondary/abstract) |
| Agol: ribbon concordance is a partial order | [arXiv:2201.03626], Camb. J. Math / CAMS 2022 | argument also yields the statement for strongly homotopy-ribbon concordance (so stated in Baldwin–Sivek) |
| Baldwin–Sivek: only finitely many hyperbolic fibered `J ≤ K`; volume bounds | [arXiv:2510.02214] (2025); part II [arXiv:2602.21109] (2026) | **No** — their Remark 1.6 (VERIFIED via arXiv HTML): "*The results above remain true, via the same proofs, if 'J≤K' is replaced … by 'J is handle-ribbon concordant to K'*" |
| Agol–Ren, *Ribbon concordance of fibered knots and compressions of surface homeomorphisms*, [arXiv:2603.10884] (2026): simplicial volume and dilatation monotone; finitely many predecessors of a fibered knot; **algorithm to find all minimal compressions of a surface homeomorphism** (generalizing Casson–Long past pseudo-Anosov) | | **No** — authors state results can be strengthened by replacing `≤` with `≤_h` (VERIFIED via arXiv HTML) |
| Dunkerley, *A ribbon partial order for links and minimality detection via Heegaard Floer*, [arXiv:2606.20802] (2026): strong ribbon concordance is a partial order on links; SQP fibered links are strong-ribbon-minimal | | covers ribbon and **strong** ribbon (0- and 1-handle movies); PARTIALLY VERIFIED |
| Lobb, *Khovanov concordance minima and the (4,5) torus knot*, [arXiv:2602.12692] (2026): reduced rational `Kh(T_{4,5})` is a summand of `Kh(K)` for any `K` in its concordance class; frames "global ribbon minima" as a generalization of slice-ribbon | | PARTIALLY VERIFIED (abstract) |
| Imori–Park–Taniguchi, *Unknotting number, ribbon concordance, and singular instantons*, [arXiv:2607.12768] (2026): for a large class of slice knots obtained via ribbon concordance, any unknotting sequence of null-homologous twists must contain both signs | | stated for ribbon concordance; handle-ribbon version not addressed. PARTIALLY VERIFIED |
| Sarkar, *Ribbon distance and Khovanov homology*, [arXiv:1903.11095]; Sarkar, *Ribbon distance bounds from Bar-Natan homology and α-homology*, [arXiv:2011.01190]; Alishahi(-Dowlin) unknotting bounds | lower bounds on the number of saddles in a ribbon concordance | genuinely ribbon-level; but again bounds a quantity only defined once a ribbon concordance exists |

**The structural reason all of this is useless for our problem (my reasoning — UNVERIFIED as a literature
statement, but elementary):** `K` ribbon ⟺ `U ≤ K`, and `U` is the **minimum** of the order. A monotone
invariant `I` with `J ≤ K ⇒ I(J) ≤ I(K)` therefore yields only `I(U) ≤ I(K)` — vacuous for genus,
volume, dilatation, HFK rank, Kh rank, etc. Likewise injectivity `Kh(U) ↪ Kh(K)` is automatic. **The
ribbon-concordance partial-order machinery obstructs `J ≤ K` for nontrivial `J`, not ribbonness of `K`.**
The one place it *could* bite is via finiteness of predecessors: Agol–Ren / Baldwin–Sivek prove a fibered
`K` has finitely many predecessors and give an algorithm for minimal compressions — if that enumeration
were made effective *and* it distinguished `≤` from `≤_h`, it would decide ribbonness for fibered knots.
It does not: both papers explicitly state their results hold for `≤_h` as well.

### 2.7 Band-move / ribbon-move obstructions

- Sarkar's ribbon distance (above) and Alishahi–Lipshitz-style Khovanov/Bar-Natan `X`-action bounds
  constrain the *number* of saddles, not the existence of a sequence to the unlink. **PARTIALLY
  VERIFIED.**
- Grigsby, *On braided, banded surfaces and ribbon obstructions*, [arXiv:1801.07158]: explicitly aims at
  "potentially effective obstructions to a slice knot being ribbon" using Rudolph's braided-banded
  surfaces and braid conjugacy invariants — and reports that via Khovanov–Lee "we do not obtain effective
  ribbon obstructions." **PARTIALLY VERIFIED (abstract).** This is a documented **negative** result and is
  important to record: a serious attempt at a ribbon-only obstruction that failed.
- Tanaka / Kanenobu-style "ribbon-move" obstructions for **2-knots** (e.g. [arXiv:1003.2473], a new
  obstruction for ribbon-moves of 2-knots) live in the 2-knot world and do not obstruct 1-knot
  ribbonness. **PARTIALLY VERIFIED.**
- Beliakova–De Renzi–Faes, *Quantum invariants of ribbon surfaces in 4-dimensional 2-handlebodies*,
  [arXiv:2512.15395] (Dec 2025): unimodular-ribbon-category invariants of **ribbon surfaces** in 4-d
  2-handlebodies up to 1-isotopy, without semisimplicity. **PARTIALLY VERIFIED (abstract).** These
  invariate a *given* ribbon surface; they are not (yet) existence obstructions. Worth watching: an
  invariant of ribbon surfaces defined from a band presentation could in principle be shown to compute
  something knot-theoretic, giving a genuine ribbon-only quantity.

### 2.8 Symmetry-based (equivariant) obstructions — **structurally cannot help**

Papers: Boyle–Issa (butterfly link, equivariant concordance invariants); Dai–Mallick–Stoffregen,
*Equivariant knots and knot Floer homology*, [arXiv:2201.01875], J. Topology 2023 (lower bounds on
equivariant slice genus; strongly invertible slice knots with arbitrarily large equivariant slice genus);
Di Prisa, *Equivariant algebraic concordance of strongly invertible knots*, [arXiv:2303.11895], and *The
equivariant concordance group is not abelian*, [arXiv:2207.04985]; A. Miller, *Strongly invertible knots,
equivariant slice genera, and an equivariant algebraic concordance group*, J. LMS 2023;
*Equivariantly slicing strongly negative amphichiral knots*, [arXiv:2109.01198]; *Equivariant Q-sliceness
of strongly invertible knots*, [arXiv:2412.09322]. **PARTIALLY VERIFIED (abstracts/secondary).**

**Explicit caveat requested:** these obstruct **equivariant** sliceness/ribbonness. A knot can be ribbon
without any ribbon disk respecting its symmetry — a non-equivariant ribbon disk need not be preserved by
the involution. Hence *"K is not equivariantly ribbon" does not imply "K is not ribbon"*. These tools are
therefore **irrelevant to the slice–ribbon conjecture as stated**, and in particular useless against
18nh00000601 / GST band sums.

### 2.9 Casson–Gordon and π₁ conditions

- Casson–Gordon, *Cobordism of classical knots* (1975/1986) — the Casson–Gordon invariants obstruct
  **sliceness**. Dead.
- Gordon (1981) π₁ conditions: ribbon concordance gives `π₁` injectivity on the bottom and surjectivity
  on the top; homotopy-ribbon concordance is *defined* by exactly this injectivity. So the π₁ content is
  shared. **PARTIALLY VERIFIED (secondary).**
- "Strongly slice" / `π₁`-surjectivity of `π₁(S³∖K) → π₁(B⁴∖D)`: surjectivity holds for ribbon disks and
  also for handle-ribbon disks (the complement is built with only 0-,1-,2-handles relative to the knot
  exterior, so `π₁` is generated by the boundary). **UNVERIFIED (my reasoning).** Dead either way.

### 2.10 Andrews–Curtis / Gompf; handle-decomposition combinatorics

**The connection.** If `D` is a ribbon disk for `K` with `n` bands, the exterior `B⁴ ∖ ν(D)` has a handle
decomposition with one 0-handle, `n+1` 1-handles and `n` 2-handles (no 3-handles), giving a **balanced
presentation** of `π₁(B⁴∖D)` with deficiency 1; if additionally `π₁` is trivial (e.g. for the
Meier–Zupan/GST constructions where one caps off) one gets a **balanced presentation of the trivial
group**, and the link up to handle slides determines that presentation **up to Andrews–Curtis moves**.
**PARTIALLY VERIFIED** (this is the standard Gompf/Kirby-calculus story; the phrase "the link up to
handle slides determines a balanced presentation of the trivial group up to Andrews–Curtis moves" came
from a secondary source, not read in a primary text).

**Why it doesn't separate ribbon from handle-ribbon.** The *defining* property of handle-ribbon is
exactly "complement has a handle decomposition with only 0-,1-,2-handles". So the entire AC/handle-slide
package is available for handle-ribbon disks too. What ribbonness adds is that the 1- and 2-handles come
from an *embedded band picture in `S³`* — i.e., the Kirby diagram is an **unlink** with dotted circles
and 0-framed 2-handles arranged by bands, rather than merely an **R-link**. That is precisely the
Miller–Zupan gap again (§2.1), and precisely the Generalized Property R / Property 2R question that
GST address. Experimental status: Diao–Pan–Yan [arXiv:2604.17737] (2026) verify *stable handleslide
triviality* for certain GST links — evidence pointing **toward** ribbonness, not away.

**Decidability caveat.** AC-triviality of a balanced presentation is not known to be decidable, and the
Andrews–Curtis conjecture is open; so this route gives no algorithm.

### 2.11 Lagrangian / Legendrian

Cornwell–Ng–Sivek, *Obstructions to Lagrangian concordance*, [arXiv:1411.1364], AGT 16 (2016): Theorem
1.2 — a Legendrian knot with at least two normal rulings is not Lagrangian concordant to the unknot;
complete list of ≤14-crossing knots with Lagrangian-slice Legendrian representatives; and they prove the
`J = U` case of "ribbon concordance is a partial order" (later generalized by Agol). **PARTIALLY VERIFIED
(abstract/secondary).** Direction note: Lagrangian concordance/filling is *more restrictive* than smooth
concordance, so "Lagrangian slice ⇒ (conjecturally) ribbon" is the opposite implication from what we
need. Also: *Doubly slice knots and obstruction to Lagrangian concordance*, [arXiv:2207.02752]. These give
no obstruction to ribbonness.

### 2.12 Candidate-specific status (context, for completeness)

- **18nh00000601**: identified in Dunfield–Gong, *Ribbon concordances and slice obstructions: experiments
  and examples*, [arXiv:2512.21825] (Dec 2025) — a census of 352.2 million prime knots ≤19 crossings;
  ~1.6M smoothly slice (in fact ribbon), 350.5M not topologically slice; 500,000 pairs of 0-friends;
  "simplest knots with unknown sliceness status". **PARTIALLY VERIFIED (abstract).**
- Oliveira-Smith, *A Dunfield–Gong 4-sphere is standard*, [arXiv:2603.23717] (Mar 2026): standardizes the
  homotopy 4-sphere, so 18nh00000601 is slice in the **standard** `B⁴`; and it bounds a **fibered
  handle-ribbon** disk. **PARTIALLY VERIFIED (search snippet/abstract; not read in primary).** Because
  the disk is fibered and handle-ribbon, **every obstruction in this catalog that dies at homotopy- or
  handle-ribbon level is already known to vanish on it** — including Casson–Gordon's handlebody criterion,
  Ξ_p, all Floer/Khovanov injectivity, all DLVVW instanton obstructions, and Agol–Ren/Baldwin–Sivek.
- **GST band sums**: Gompf–Scharlemann–Thompson [arXiv:1103.1601]; the derivative R-links are the GST
  links; handle-ribbon by construction (§2.1). Only §2.1 (unlink vs R-link) speaks to their ribbonness.
- Gukov et al., *Searching for ribbons with machine learning*, [arXiv:2304.09304] / IOP MLST 2025: RL +
  Bayesian optimization searching for Reidemeister+band-move sequences to an unlink, successful up to ~70
  crossings. **PARTIALLY VERIFIED (abstract).** This is a *positive* search method (find a ribbon disk),
  not an obstruction; but failure of an exhaustive search is the only "evidence" currently available
  against ribbonness of candidates.

---

## 3. Conclusions

1. **There is no known ribbon-only vanishing obstruction for knots.** Every invariant-style obstruction
   in the literature that is labelled "ribbon" has been (or can be seen to be) upgraded to homotopy-ribbon
   or handle-ribbon: Casson–Gordon's fibered/handlebody theorem (homotopy-ribbon), Kjuchukova's Ξ_p
   (homotopy-ribbon), Park–Powell (Z[Z]-homology-ribbon), Zemke/Miller–Zemke HFK (handle-ribbon),
   Levine–Zemke/Gujral–Levine Khovanov (handle-ribbon), DLVVW instanton (handle-ribbon by definition),
   Agol partial order and Baldwin–Sivek / Agol–Ren finiteness (handle-ribbon, stated by the authors).

2. **The only exactly-calibrated ribbon-only statement is Miller–Zupan Prop 1.1** (`ribbon ⟺ unlink
   derivative`) against Thm 1.3 (`handle-ribbon ⟺ R-link derivative`). The gap is literally Generalized
   Property R. It is a characterization, not a computable invariant; no finiteness theorem for the set of
   derivatives of a fixed knot exists, so it currently yields no algorithm.

3. **The only genuinely ribbon-only *quantitative* theory is fusion/ribbon number** (`F`, `r`), where
   [arXiv:2003.02832] proves `F` and the handle-ribbon analogue `F_sh` differ arbitrarily, and
   Friedl–Misev–Zupan prove a finiteness/computability theorem for Alexander polynomials at bounded ribbon
   number. These are the only ribbon-only tools with a computability theorem attached — but they bound
   quantities defined only for ribbon knots and so cannot by themselves obstruct ribbonness.

4. **Two under-examined leads**, both worth chasing:
   - **Turaev's Theorem H** (1983), an explicitly-labelled ribbon obstruction from before homotopy-ribbon
     existed as a concept, apparently never cited or tested. Not obtainable online; needs library access.
   - **The open problem "is every ribbon disk of a fibered knot fibered?"** (Meier–Zupan, VERIFIED
     statement). If true, the Casson–Long/Agol–Ren compression algorithm plus Casson–Gordon would likely
     collapse ribbon = homotopy-ribbon for fibered knots, which would eliminate the fibered candidates.
     Conversely, a fibered slice knot with a provably non-fibered-only ribbon obstruction would be the
     first genuine ribbon-only tool.

5. **Documented failure to record:** Grigsby [arXiv:1801.07158] set out explicitly to build ribbon-only
   obstructions from Rudolph's braided-banded surfaces and reports that the Khovanov–Lee implementation
   gives none. Any new attempt should account for why it evades that obstruction.

---

## 4. Source list

- Miller–Zupan, *Equivalent characterizations of handle-ribbon knots*, [arXiv:2005.11243]
- Meier–Zupan, *Knots bounding non-isotopic ribbon disks*, [arXiv:2310.17564], J. Topology 2025
- Gompf–Scharlemann–Thompson, [arXiv:1103.1601], Geom. Topol. 14 (2010) 2305–2347
- Scharlemann–Thompson, [arXiv:0901.2319]; *Proposed Property 2R counterexamples classified*, [arXiv:1208.1299]
- Diao–Pan–Yan, [arXiv:2604.17737] (2026)
- Casson–Gordon, *A loop theorem for duality spaces and fibred ribbon knots*, Invent. Math. 74 (1983) 119–137
- Larson–Meier, *Fibered ribbon disks*, [arXiv:1410.4854]
- Meier, *Extending fibrations on knot complements to ribbon disk complements*, [arXiv:1811.09639]
- Lecuona et al., *Fibered ribbon pretzels*, [arXiv:2408.03644]
- Miyazaki, *Nonsimple, ribbon fibered knots*, Trans. AMS 341 (1994)
- Baker, *A note on the concordance of fibered knots*, J. Topol. 9 (2016) 1–4
- Baldwin–Sivek, *Ribbon concordance and the minimality of tight fibered knots*, [arXiv:2210.04044]
- Baldwin–Sivek, *Ribbon concordance and fibered predecessors*, [arXiv:2510.02214]; II, [arXiv:2602.21109]
- Agol–Ren, *Ribbon concordance of fibered knots and compressions of surface homeomorphisms*, [arXiv:2603.10884]
- Hom–Park, *Ribbon knots and iterated cables of fibered knots*, [arXiv:2507.20455]
- Hom–Park, *Ribbon concordance and cabling*, [arXiv:2608.06625]
- Rudolph, *A non-ribbon plumbing of fibered ribbon knots*, [arXiv:math/0105257]
- Turaev, *Multiplace generalizations of the Seifert form of a classical knot*, Math. USSR Sb. 44(3) (1983) 335–361 — **Theorem H, not obtained**
- Kawauchi, *Ribbonness on classical link*, [arXiv:2307.16483] — **claim not accepted**
- Gilmer, *Ribbon concordance and a partial order on S-equivalence classes*, Topology Appl. 18 (1984) 313–324
- Eisermann, *The Jones polynomial of ribbon links*, [arXiv:0802.2287], Geom. Topol. 13 (2009) 623–660
- Sakie Suzuki, *On the colored Jones polynomials of ribbon links, boundary links and Brunnian links*, [arXiv:1111.6408](https://arxiv.org/abs/1111.6408), Banach Center Publications 100 (2014), 213–222
- Friedl–Misev–Zupan, *Bounding the ribbon numbers of knots and links*, [arXiv:2408.11618]; *Ribbon numbers of 12-crossing knots*, [arXiv:2409.12910]
- Juhász–Miller–Zemke, *Knot cobordisms, bridge index, and torsion in Floer homology*, [arXiv:1904.02735]
- *Ribbon knots, cabling, and handle decompositions*, [arXiv:2003.02832]
- Gordon, *Ribbon concordance of knots in the 3-sphere*, Math. Ann. 257 (1981) 157–170
- Zemke, [arXiv:1902.04050]; Miller–Zemke, [arXiv:1903.05772]
- Levine–Zemke, [arXiv:1903.01546]; Gujral–Levine, [arXiv:2009.03406]
- Kang, [arXiv:1909.06969]
- Daemi–Lidman–Vela-Vick–Wong, [arXiv:1904.09721], Adv. Math. 408 (2022) 108580
- Agol, *Ribbon concordance of knots is a partial ordering*, [arXiv:2201.03626]
- Dunkerley, [arXiv:2606.20802]; Lobb, [arXiv:2602.12692]; Imori–Park–Taniguchi, [arXiv:2607.12768]
- Sarkar, [arXiv:1903.11095]; Sarkar, [arXiv:2011.01190]
- Grigsby, *On braided, banded surfaces and ribbon obstructions*, [arXiv:1801.07158]
- Cahn–Kjuchukova, *Computing ribbon obstructions for colored knots*, [arXiv:1812.09553], Fund. Math. 2021
- Park–Powell, *A ribbon obstruction and derivatives of knots*, [arXiv:1802.00582], Israel J. Math
- Cochran–Davis, [arXiv:1303.4418]; Cha–Kim, [arXiv:1511.07295], [arXiv:1603.09163]
- Boyle–Issa; Dai–Mallick–Stoffregen [arXiv:2201.01875]; Di Prisa [arXiv:2303.11895], [arXiv:2207.04985]; A. Miller (J. LMS 2023)
- Cornwell–Ng–Sivek, [arXiv:1411.1364]
- Beliakova–De Renzi–Faes, [arXiv:2512.15395]
- Dunfield–Gong, [arXiv:2512.21825]; Oliveira-Smith, [arXiv:2603.23717]
- Gukov et al., *Searching for ribbons with machine learning*, [arXiv:2304.09304]
- D. Moskovich, *Slice-Ribbon Conjecture in danger!*, Low Dimensional Topology blog, 2 Dec 2010
