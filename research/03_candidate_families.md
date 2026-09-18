# 03 — Candidate families for counterexamples to the Slice–Ribbon Conjecture

Survey date: 2026-09-11. Prepared as an independent sweep against the existing SR-Foxy package
(`CANDIDATE_LEDGER.md`, `GST_AUDIT.md`, `ABE_TAGAMI_AUDIT.md`, `SOURCES.md`), whose tracked objects are
only: DG `18nh00000601`, GST `B_{3,1}`, Abe–Tange annulus twists, Abe–Tagami `A_n(6_3)`, Hom–Park `P`-sums.

## 0. Definitions and evidence labels used here

**CE** = an explicit knot `K ⊂ S^3` together with (i) a proof that `K` bounds a smooth disk in the
**standard** `B^4`, and (ii) a proof that `K` bounds **no ribbon disk**. Nothing in the literature is a CE.

Two production routes:
- **(A)** certified smoothly slice in standard `B^4`, ribbonness open → prove non-ribbon.
- **(B)** certified non-ribbon, sliceness open → prove smoothly slice (typically by proving a concordance).

Evidence labels attached to every substantive claim:
- **VERIFIED** — I read the primary text (full PDF/HTML extracted and quoted in this session).
- **PARTIALLY VERIFIED** — abstract, intro summary, or a reliable secondary restatement only.
- **UNVERIFIED** — asserted in search results / recollection; not confirmed against a primary source.

Ambient hygiene: every sliceness claim below is tagged `[std B^4]`, `[homotopy B^4]`, `[Z/2-homology ball]`,
or `[rationally slice]`. `ribbon ⇒ handle-ribbon ⇒ homotopy-ribbon ⇒ slice`; no converse is used.

---

## 1. Gompf–Scharlemann–Thompson (GST) links `L_{n,k}` and their band sums

**Construction** (PARTIALLY VERIFIED, ar5iv of arXiv:1103.1601, *Fibered knots and potential counterexamples
to the Property 2R and Slice-Ribbon Conjectures*, Geom. Topol. 14 (2010)): `L_{n,k}` is a 2-component link
consisting of the square knot `Q = T_{2,3} # T_{2,-3}` interleaved with the connected sum of the `(n,n+1)`
torus knot and its mirror, drawn as an `n`-stranded spiral with a ±1 full twist; `k` controls additional
twisting. The links are **R-links** (surgery on them gives `#^2 (S^1×S^2)`), hence each component, and each
**band sum** of the two components, is smoothly slice `[std B^4]` — the slice disk comes from the dual handle
description in which the exterior of the sliced link is a regular neighbourhood of a wedge of two circles.

- **Why slice**: §8 of GST identifies the dual 4-manifold with `B^4`; hence band sums bound smooth disks in the
  **standard** `B^4`. (PARTIALLY VERIFIED via ar5iv §8; the package records this as PEER-REVIEWED PRIMARY.)
- **Known ribbon (dead) members**: `n = 0, 1`; `k = 0`; `(n,k) = (2,1)`. (PARTIALLY VERIFIED.)
- **Open**: `L_{n,1}` for `n ≥ 3`, and band sums thereof. GST explicitly ask whether `L_{n,1}`, `n ≥ 3`, is a
  counterexample to Generalized Property R, and whether the associated slice knots are ribbon.
- **Best explicit smallest member**: the slice knot obtained as a band sum of `L_{3,1}` and displayed in
  GST's figure in the introduction. NOTE A DISCREPANCY: my ar5iv read reported "simplest unresolved case
  `n=3, k=1`, Figure 1"; the existing package (`GST_AUDIT.md`) and GHMR both refer to "the slice knot
  associated to `L_{3,1}` shown in **Figure 2** of [GST]". Both point at the same object; the figure number
  should be pinned from the journal PDF before citation. (PARTIALLY VERIFIED.)

**ML ribbon search — exactly what GHMR found** (VERIFIED: full text of arXiv:2304.09304 extracted and read):
> "The first two links in the GST family (`L_{1,1}` with 18 crossings and `L_{2,1}` with 40 crossings) were
> already known to be ribbon (see [GST10b]), but unfortunately our algorithms could not find bands to prove
> they are ribbon."

and, in the list of objects **whose ribbon status is unknown**:
> "other GST examples from [GST10b], such as `L_{3,1}` and the slice knot associated to it that is shown in
> Figure 2 of [GST10b]".

**Conclusion (important, and consistent with the package):** the ML search killed **no** GST member. It failed
even on `L_{1,1}` and `L_{2,1}`, which *are* ribbon. Therefore GHMR search failure is worthless as a
non-ribbon signal on this lane. (VERIFIED.)

**Subsequent work.**
- Scharlemann, *Generalized Property R and the Schoenflies Conjecture*, Comment. Math. Helv. 83 (2008) 421–449:
  the square knot is argued (via Andrews–Curtis considerations) to be a plausible Property 2R counterexample;
  a least-genus component of a 2-component Generalized-Property-R counterexample cannot be fibered.
  (PARTIALLY VERIFIED — abstract/summary.)
- Scharlemann–Thompson, *Fibered knots and Property 2R, II*, arXiv:0908.2795. (UNVERIFIED beyond title.)
- Gompf, *On Nash's 4-sphere and Property 2R*, arXiv:1102.3207. (UNVERIFIED beyond title.)
- Abe–Tange, arXiv:1305.7492, §6: GST band sums are **belt spheres of 2-handles in a handle diagram of `B^4`
  with no 3-handles** after a handle slide; their Conjecture 6.1 predicts all such belt spheres are ribbon.
  (PARTIALLY VERIFIED via package; Conjecture 6.1 is *not* a theorem, so it does not kill the lane — but it is
  the reason many experts expect GST band sums to be ribbon.)
- Diao–Pan–Yan, *Some experimental results on stable equivalence of GST links for the Generalized Property R
  Conjecture*, arXiv:2604.17737 (2026): proves finite ranges of **stable** handleslide equivalences.
  **Stable equivalence is not handleslide triviality and produces no ribbon disk.** (PARTIALLY VERIFIED.)

**Verdict: LIVE but structurally disadvantaged.** These knots are certified slice in std `B^4`, but their
sliceness proof is handle-theoretic in exactly the way that makes them *look* half-/handle-ribbon, so the
usual homotopy-ribbon obstruction battery is a priori exhausted. Diagram sizes (40+ crossings at `n=2`,
much larger at `n=3`) make direct computation painful.

---

## 2. Annulus twists: Abe–Tange, Abe–Jong–Omae–Takeuchi, Abe–Tagami, Park

### 2a. Abe–Tange `A_j(J)` slice knots
Abe–Tange (arXiv:1305.7492, Thm 3.1): if a **ribbon** knot `J` admits a suitable annulus presentation, every
annulus twist `A_j(J)` is smoothly slice `[std B^4]` — proved by showing the associated trace/2-handlebody
`W(A_j(J)) ≅ B^4`. (PARTIALLY VERIFIED via package `SOURCES.md` [S05].)
- **Killed sublane**: the `8_20`-based family is **ribbon** for all `n ≥ 0` (Abe–Tange Thm 5.4). DEAD.
- **Open**: general `J` + presentation + `j`. This is a *candidate generator*, not a single knot.
- **Verdict: LIVE as a generator, no promoted member.**

### 2b. Abe–Jong–Omae–Takeuchi, *Annulus twist and diffeomorphic 4-manifolds*, Math. Proc. Camb. Phil. Soc.
155 (2013) 219–235, arXiv:1209.0361 (+ sequel arXiv:1408.0092). Produces infinitely many framed knots with
diffeomorphic 4-manifolds; relates `n`-shake genus and 4-ball genus; builds homotopy 4-spheres from a slice
knot with unknotting number 1. (PARTIALLY VERIFIED — abstract.) This is machinery for *both* directions.

### 2c. JungHwan Park, *A construction of slice knots via annulus modifications*, arXiv:1512.00401 (Topology
Appl.). **MISSED BY THE PACKAGE.** Constructs *smoothly slice* and separately *exotically slice* knots via
`n`-twist annulus modifications, generalizing Osoinach/Abe–Tange annulus twists; an application is smoothly
slice knots with **non-slice derivatives** (bearing on the Kauffman/derivative circle of ideas). Ribbonness of
the produced knots is **not discussed** in the abstract. (PARTIALLY VERIFIED — abstract only.)
**This is a fresh candidate generator of route (A) type that the package does not track.** FLAG: the paper
explicitly separates "smoothly slice" from "exotically slice" — any member used must be taken from the
*smoothly slice* half, i.e. `[std B^4]`.

### 2d. Abe–Tagami `K_n = A_n(6_3)` (route B)
(PARTIALLY VERIFIED via package [S06] + Tagami arXiv:2010.13283 intro, VERIFIED.)
- `K_n` are fibered, share a 0-surgery, have common irreducible Alexander polynomial `1-3t+5t^2-3t^3+t^4`,
  and `K_n = K_m` only for `n=m` or `n+m=-1`.
- By Miyazaki (Trans. AMS 341 (1994), Thm 5.5) as applied in Abe–Tagami Cor. 4.3, `D_{n,m} = K_n # (-K_m)` is
  **not ribbon** (indeed not homotopy-ribbon) when `K_n ≇ K_m`.
- `D_{n,m}` is slice **iff** `[K_n] = [K_m]` in the smooth concordance group. This equality is **UNKNOWN**.
- **State of the art on distinguishing them**: I found **no** paper distinguishing `A_n(6_3)` members in smooth
  concordance. The relevant machinery that *does* kill sibling constructions is
  Miller–Piccirillo, *Knot traces and concordance*, J. Topology 11 (2018), arXiv:1702.03974: they use Heegaard
  Floer `d`-invariants to obstruct smooth concordance of knots with **diffeomorphic 0-traces**, disproving a
  conjecture of Abe; and there exist knots related by annulus twisting that are not smoothly concordant.
  (PARTIALLY VERIFIED — abstract/summary.) **No application to `A_n(6_3)` was found.**
- **Verdict: LIVE/WEAK.** Non-ribbonness is rigorous; sliceness is a concordance collision nobody has produced.
  Note the asymmetry: proving `[K_n]=[K_m]` yields an instant CE; any distinguishing invariant kills one pair only.

---

## 3. Hom–Park (arXiv:2507.20455) and the cable-independence dichotomy

(PARTIALLY VERIFIED — ar5iv theorem statements retrieved; full proofs not read.)

- **Thm 1.1**: a connected sum of `γ_0`-sharp fibered knots is ribbon **iff** it is of the form `K # -K`.
- **Prop 2.6**: if `K` is `γ_0`-sharp and `P` is a 1-bridge braid pattern, `P(K)` is `γ_0`-sharp; in particular
  every cable of a `γ_0`-sharp knot is `γ_0`-sharp.
- **Cor 1.2 (the dichotomy)**: *Either distinct iterated cables of tight fibered knots are linearly independent
  in the smooth knot concordance group, or the slice–ribbon conjecture is false.* ("Tight fibered" = supports
  the tight contact structure on its fiber surface.)
- **Cor 1.3**: for distinct iterated cables `K`, `J` of tight fibered knots and distinct `q_1, q_2` coprime to `p`,
  `P(K,J,p,q_1,q_2) := K_{p,q_1} # -K_{p,q_2} # J_{p,q_2} # -J_{p,q_1}` is **algebraically slice but not ribbon**.
  Smallest concrete instance reported: `K = T_{2,3}`, `J = T_{2,5}`, `p = 2`, `q_1 = 1`, `q_2 = 3`.

**Exactly which question must FAIL.** `P` is non-ribbon by Thm 1.1 (it is not of the form `K # -K` because the
four cable summands are pairwise distinct `γ_0`-sharp fibered knots). `P` is slice **iff**
`[K_{p,q_1}] - [K_{p,q_2}] = [J_{p,q_1}] - [J_{p,q_2}]` in `C`, i.e. iff the **cabling difference map**
`K ↦ [K_{p,q_1}] - [K_{p,q_2}]` fails to be injective on iterated cables of tight fibered knots. Equivalently:
a CE arises exactly if the set `{ K_{p,q} : K` an iterated cable of a tight fibered knot `}` is **linearly
dependent** in `C` in this specific 4-term pattern. So the failing statement is *not* "some cable family is
dependent" in general — it is the sharply specified: **the 4-term relation
`K_{p,q_1} - K_{p,q_2} - J_{p,q_1} + J_{p,q_2} = 0` holds for some distinct `K, J`.**

**State of the art on cable independence** (PARTIALLY VERIFIED — abstracts):
- Christopher W. Davis–JungHwan Park–Arunima Ray, *Linear independence of cables in the knot concordance group*,
  [arXiv:1806.06225](https://arxiv.org/abs/1806.06225), Trans. AMS 374 (2021), 4449–4479:
  infinite families whose sets of cables are linearly independent in `C`; these examples lie arbitrarily deep in
  the solvable and bipolar filtrations, and — critically — **the independence cannot be detected by any
  combination of algebraic concordance invariants, Casson–Gordon invariants, and `τ`, `ε`, `Υ`.** This is
  a result about their specified families; it does not establish the same invisibility for the Hom–Park
  four-term candidates without matching the hypotheses and parameters. (Attribution and scope corrected
  18 September 2026; see research/36 and ERRATA_2026-09-18_OPUS.md.)
- Hedden–Kim–Livingston / S. Kim–Livingston (after Hedden–Livingston–Ruberman): the relevant cokernel contains
  `Z^∞ ⊕ (Z/2)^∞`. (UNVERIFIED — search-result restatement.)
- Feller–Park–Ray: linear independence of a subfamily of mixed iterated cables. (UNVERIFIED.)
- Hom's `ε` and `Υ`: standard cable formulae exist. Their insufficiency for the Davis–Park–Ray families
  above does not by itself settle their values or sufficiency on the present four-term candidates.
- Figure-eight cable lane (relevant because `4_1` is *not* tight fibered, but the techniques transfer):
  Dai–Kang–Mallick–Park–Stoffregen, *The (2,1)-cable of the figure-eight knot is not smoothly slice*,
  Invent. Math. 238 (2024) 371–390, arXiv:2207.14187 (VERIFIED — intro read); and
  Kang–Park–Taniguchi, *Smooth concordance of cables of the figure-eight knot*, arXiv:2505.03720 (May 2025):
  **every nontrivial cable of the figure-eight knot has infinite order in `C`**, via new invariants `κ_R^{(k)}`
  from branched covers and real Seiberg–Witten Floer K-theory (PARTIALLY VERIFIED — abstract).
- Fukumoto–Taniguchi, arXiv:2501.07910: the 3-fold (resp. 6-fold) connected sum of the `(2,1)`-cable of `4_1`
  cannot bound a smooth nullhomologous disk in punctured `S^2 × S^2`, via the real 10/8-inequality
  (Konno–Miyazawa–Taniguchi). (PARTIALLY VERIFIED — abstract.)

**Verdict: LIVE/WEAK (route B).** Rigorous non-ribbon certificate, no slice disk. Everyone expects the
independence side of the dichotomy to hold, which is why this is a *theorem about a dichotomy* rather than a
candidate program. The practical value to Foxy is the **non-ribbon certificate machinery** (Thm 1.1 + Prop 2.6),
which is currently the sharpest general ribbon obstruction for connected sums of fibered knots.

---

## 4. Dunfield–Gong census (arXiv:2512.21825) — full status of every "suspicious" knot

**VERIFIED throughout this section**: the complete 62-page PDF was downloaded and text-extracted; quotations
below are literal (modulo PDF de-ligaturing).

**Theorem 1.1 / 1.9 scale.** 352.2M prime knots to 19 crossings (`PS19`). Smooth sliceness determined for all
but ~11,383; topological for all but ~1,429. 1,633,786 shown **ribbon** (Thm 2.1) — hence "all the smoothly
slice knots identified in Theorem 1.1 are indeed ribbon."

**§1.17 (the key paragraph):**
> "Using this method, we discovered more than 500 smoothly slice knots where repeated passes of our ribbon disk
> search had come up empty. However, we eventually found ribbon disks for all of them… Thus we have identified
> no smoothly slice knots that are not known to be ribbon. However, the knot `K = 18nh00000601` from Theorem 1.12
> is intriguing… Unless it and its 0-friend give a counterexample to the smooth 4D Poincaré conjecture, the knot
> `K` must be smoothly slice. However, we tried very hard to find a ribbon disk for `K` to no avail. This makes
> `K` a plausible candidate for a knot that is smoothly slice but not ribbon."

**§2.7 "Obscure ribbon disks" — the exact suspicious set and its disposition:**
- 513 knots found slice by the `T_{2,3} # T_{2,-3}` / `K_{4a1} # K_{4a1}` connected-sum-and-band trick
  (446 + 67) → **all 513 eventually shown ribbon.** DEAD.
- 41 knots shown to be 0-friends with a ribbon knot → **all but `18nh00000601` eventually shown ribbon.** Named
  examples that fell: `19nh000077044`, `19nh000187109`, `19nh003361975`. DEAD.
- Knots first shown slice via a **shared knot trace** with a ribbon knot, later found ribbon:
  `17nh0016322`, `17nh0026540`, `17nh0298397`. DEAD.
- `19nh051162051` — first found slice by §2.6, later found ribbon. DEAD.
- **Survivor: `18nh00000601` only.**
- Explicit self-assessment: "we expect there are hundreds of other similarly obscure ribbon disks among the
  11,383 knots in `PS19` whose smooth slice status is unknown." (i.e. DG themselves treat search failure as weak.)

**Theorem 1.12 / 5.14 (VERBATIM):**
> "If `18nh00000601` is not smoothly slice, or if any of `{16n68278, 17nh0010647, 18nh00098198}` are smoothly
> slice, then there is an exotic smooth 4-sphere. All four knots are topologically slice. The knot
> `18nh00000601` is moreover smoothly slice in a homotopy 4-ball."

**CRITICAL READING.** The three knots `16n68278`, `17nh0010647`, `18nh00098198` point the **opposite way**: their
0-friends have `s̃_c ≠ 0` (Table 11), so those three are *expected non-slice*. **They are NOT slice–ribbon
candidates.** DG yields exactly **one** SR candidate: `18nh00000601`.

**Table 11 data for `18nh00000601`** (VERIFIED): the super-special RBG link has DT code
`ycjkdnhQyUtMsaVweFIRCXOBgLJDkP`, framing `r = 1`, `b = g = 0`; the 0-friend `K'` is **ribbon**; and in the
paper's convention `K' = K_B`, `K = K_G` for Figure 4 — i.e. `18nh00000601` is the member whose sliceness is
*inherited* from the ribbon 0-friend. Because `r = 1` is **odd**, Theorem 5.8 gives only a 0-surgery
homeomorphism, **not** a trace diffeomorphism — hence only `[homotopy B^4]` from DG alone.

**Obstructions computed by DG** (VERIFIED, §1.9 breakdown + §3): twisted Alexander polynomials (HKL tests,
Herald–Kirk–Livingston metabelian representations), `d`-invariants of double branched covers, `τ`
(HFK Calculator), `s` (KnotJob/Khovanov), `Υ`, signatures, Casson–Gordon signatures (§6.6), Donaldson-type
Goeritz/bifactor tests, plus the ribbon-concordance graph propagation of §7. Remark 1.10: the topological HKL
tests were ~6.6× as effective as all smooth obstructions combined.

**Other DG items worth tracking (MISSED by the package):**
- `18nh00098373` — "We found 2-band ribbon disks for all but one of them, namely `18nh00098373`, and hence the
  rest have fusion number exactly two." A **ribbon knot with fusion number possibly > 2**; feeds the
  fusion-number lane (§9). (VERIFIED.)
- **Inscrutable sets** (§1.18): Table 1, the 55 knots ≤15 crossings of unknown *smooth* slice status (e.g.
  `K13n65, K13n3871, K13n3872, K13n3897, K13n3936, K13n4582, K14n3713*, K14n4425, K14n4621*, K14n5486, K14n9023,
  K14n10011, K14n11063, K14n18909, K14n18911, K14n21673, …`; `*` = also topologically unresolved, all with
  `Δ_K = (t^2-t+1)^2`); Table 2 (38 knots ≤16 crossings, topological); Table 3 (smallest-volume unknowns,
  led by `19nh000000055` at vol 8.66); Table 4 (12 non-hyperbolic unknowns, all satellites, e.g.
  `17ns29 = Fig8[1]`, `18ns51 = Trefoil[A(1/2,4/3)]`, `19ns244 = Fig8[-1/3]`); Table 5 (25 fibered unknowns,
  incl. `18nh00000601` at genus 5). These are *sliceness-unknown*, so not CE candidates, but they are the
  natural pool for route (A) once someone proves one slice by a non-ribbon method.
- **Theorem 6.3** (VERIFIED): `19nh000143796` is topologically but **not** smoothly slice, proved by the
  Allen–…–ACMPS-style genus-bound-in-`CP^2 # CP^2` argument with `K_1 = K(-3/2, 1/2, 1/15)` of genus 9 and
  Bryan's Corollary 1.7. Of ~12,000 mystery knots attacked this way, it was the only success (Remark 6.4).

**Earlier Dunfield ribbon-search work**: the `[DG]` code base and the "1705 knots with up to 14 crossings are
ribbon" result recovered independently by GHMR (VERIFIED via GHMR §7); `[DOR]` (Dunfield–Obeidin–Rudd?) supplies
the drilling/recognition machinery behind the 0-friend generation. (PARTIALLY VERIFIED — reference only.)

**`18nh00000601` promotion to `[std B^4]`**: Oliveira-Smith, *A Dunfield–Gong 4-Sphere is Standard*,
arXiv:2603.23717v1 (24 Mar 2026). Abstract read directly (VERIFIED):
> "we standardize a homotopy 4-sphere constructed by Dunfield and Gong. As a corollary, we show that the
> 18-crossing knot `18nh00000601`, which is not known to be ribbon, is slice in the standard 4-ball. Thus,
> `18nh00000601` serves as a potential counterexample to the Slice-Ribbon Conjecture. In addition, we show that
> the same knot bounds a fibered handle-ribbon disk in `B^4`."
Consequence (PARTIALLY VERIFIED, from §3 headings + package): it is **fibered, genus 5, handle-ribbon in std
`B^4`**, hence homotopy-ribbon. **Every homotopy-ribbon and handle-ribbon obstruction is therefore logically
dead on this knot.** Closure requires a genuinely ribbon-specific necessity — most concretely, via
Miller–Zupan (arXiv:2005.11243) Prop. 1.1: ribbon ⟺ some genus-`g` Seifert surface has a `g`-component
**unlink** derivative, while Thm 1.3 gives only an **R-link** derivative.

**Verdict: LIVE — best candidate in the literature.** Smallest, most documented, `[std B^4]` certified.

---

## 5. 0-surgery homeomorphisms / RBG links / Manolescu–Piccirillo

**Mechanism** (VERIFIED via DG §5.6–5.8 and GHMR §6): an **RBG link** `L = R ∪ B ∪ G` with framings `r,b,g`
encodes a pair of 0-friends `K_B, K_G` (Manolescu–Piccirillo, arXiv:2102.04391, Thm 1.2 — conversely every
0-friend pair arises this way). For **super-special** RBG links (`R∪B`, `R∪G` both Hopf links, `b=g=0`, `r ∈ Z`):
- `r` even ⇒ homeomorphic traces; **`r = 0` ⇒ diffeomorphic traces** ⇒ by the Trace Embedding Lemma the two
  knots have the **same smooth slice status**, and the slice disk lives in the **standard `B^4`**;
- `r` odd (+ trivial MCG of the common 0-surgery) ⇒ traces *not* homeomorphic ⇒ only `[homotopy B^4]`.

**THIS IS THE SHARPEST CANDIDATE GENERATOR IN THE FIELD, AND THE PACKAGE MISSES ITS BEST EXPLICIT OUTPUT.**

**GHMR §6 (VERIFIED, quoted):** of Manolescu–Piccirillo's 3375 RBG pairs, 2522 pairs were killed by algebraic
obstructions (non-slice, hence non-ribbon); the Bayesian random walker found 843 more ribbon; 5 more pairs were
completed by other means (one by a modified Dunfield–Gong program: `K_G(0,1,-1,-1,1,0)`, ribbon with 3 bands;
three by Piccirillo's R-link/Prop 2.3 argument: `K_B(0,1,2,0,-1,-1)`, `K_B(0,0,2,0,0,-1)`, `K_G(2,0,0,-1,2,-1)`).
**Five pairs (ten knots) remain of unknown slice AND ribbon status:**

    K_{B/G}(0, 0, 0, 1, 2, −1)      ← r = 0
    K_{B/G}(0, 0, 0, −1, 2, 1)      ← r = 0
    K_{B/G}(0, 0, −2, 0, 0, 1)      ← r = 0
    K_{B/G}(−2, 0, 0, −1, 2, −1)
    K_{B/G}(−1, 0, −1, −1, 2, −1)

GHMR's own conclusion, quoted verbatim:
> "In principle, while the three other pairs `K_{B/G}(0,0,0,1,2,−1)`, `K_{B/G}(0,0,0,−1,2,1)`,
> `K_{B/G}(0,0,−2,0,0,1)` cannot produce counterexamples to SPC4, they might produce counterexamples to the
> Slice-Ribbon Conjecture. Indeed, supposing one of the knots `K_1` in such a pair is found to be ribbon with a
> slice disk `Δ`, the decomposition `S^4 = E(Δ) ∪ (−X(K_1)) = E(Δ) ∪ (−X(K_2))` would show that `K_2` bounds an
> embedded disk in `B^4`, and is therefore slice (but it may not be ribbon)."

**These six knots (three `r=0` pairs) are explicit, named, small-ish (23–29 crossings in the sibling cases),
and are a pure route-(A) factory requiring only one ribbon disk to be found.** They are absent from
`CANDIDATE_LEDGER.md`. **Priority action item.**

Remaining two pairs (`r ≠ 0`) are SPC4 candidates, not SR candidates.

**Manolescu–Piccirillo's own 5 topologically slice knots** ("if any of them were slice, we would obtain an
exotic four-sphere") point the wrong way and are **not** SR candidates. (PARTIALLY VERIFIED — abstract.)

**Piccirillo's Conway-knot trace method** (arXiv:1808.02923) shows **non**-sliceness; it is a killer, not a
generator, and DG's Theorem 5.10 (25 knots not smoothly slice) is its industrialized form — using
Nakamura Thm 3.13 (conditional on his Conj. 2.15, established by Ren, Cor. 1.5) that `s_F(K_G) ≠ 0` obstructs
both `K_B` and `K_G`. (VERIFIED via DG §5.9–5.10.)

**Tagami, arXiv:2010.13283 (VERIFIED — intro read)**: draws explicit dictionaries among Gompf–Miyazaki
**dualizable patterns**, Abe–Jong–Omae–Takeuchi **band presentations/annulus presentations**, and
Piccirillo's **RGB-diagrams**; notes Piccirillo's Conway construction is itself an annulus twist. This is the
translation layer that lets an annulus-presentation candidate be re-expressed as an RBG candidate and vice
versa — i.e. the two generators in §2 and §5 are the same machine in different coordinates.

---

## 6. Akbulut–Kirby / Cappell–Shaneson / Gompf–Miyazaki — the historical pattern

The recurring history: a homotopy 4-sphere yields a knot that is slice `[homotopy B^4]` and looks non-ribbon;
then the sphere is standardized and the knot turns out ribbon.
- Gompf, *Killing the Akbulut–Kirby 4-sphere, with relevance to the Andrews–Curtis and Schoenflies problems*,
  Topology 30 (1991). (PARTIALLY VERIFIED — bibliographic.)
- Akbulut–Kirby, *A potential smooth counterexample in dimension 4 to the Poincaré conjecture…*, Topology 24
  (1985). (UNVERIFIED beyond citation.)
- Gompf, *Cappell–Shaneson homotopy spheres are standard*, arXiv:0907.0136 (Ann. of Math. 2010); Akbulut,
  *Cappell–Shaneson homotopy spheres are standard*. (PARTIALLY VERIFIED.)
- **Gompf–Miyazaki, *Some well-disguised ribbon knots*, Topology Appl. 64 (1995) 117–131** (PARTIALLY VERIFIED —
  abstract + Tagami's restatement, VERIFIED): studies satellites built from **dualizable patterns**; shows that
  certain knots that bound smooth disks in `B^4` and *appear* not to be ribbon **are in fact ribbon**; and
  separately shows that connected sums of certain satellite knots are **non-ribbon knots for which all known
  algebraic obstructions to sliceness vanish**. Tagami (VERIFIED) restates the second half: Gompf–Miyazaki
  [9, Prop. 3.1] give a pair of knots with homeomorphic 0-surgeries whose connected sum is **not ribbon**; in
  particular there is no ribbon concordance between them in either direction.
  **This is the historical prototype of the Abe–Tagami lane and is MISSED by the package.** It is a route-(B)
  candidate of exactly the `D_{n,m}` type: `K # -K'` non-ribbon, slice iff `K ≃ K'` in `C`.
  **Killer available**: Miller–Piccirillo (arXiv:1702.03974) used `d`-invariants to obstruct concordance for
  many dualizable-pattern pairs; whether the specific Gompf–Miyazaki Prop 3.1 pair is so obstructed
  is **NOT YET VERIFIED** here.
- **Kirby problem list 1.33** is the slice–ribbon conjecture itself, attributed to Fox (Problem 25 in Fox 1962);
  it is recorded as **open**. (PARTIALLY VERIFIED — multiple secondary sources, exact Kirby-list status text
  not retrieved.)

**Verdict: DEAD as a source of live candidates** (every historical member was standardized and then ribbonized),
but **the pattern is the strongest Bayesian prior against the whole `[homotopy B^4]` family of candidates** —
including, arguably, `18nh00000601`.

---

## 7. Corks, exotic contractible manifolds, exotic disks

- Hayden, *Exotically knotted disks and complex curves*, arXiv:2003.13681: exotic slice surfaces of all genera
  in `B^4`; among the outputs are **pairs of exotic ribbon disks**, whose double branched covers give exotic
  contractible Stein domains with the same contact boundary. (PARTIALLY VERIFIED — abstract/summary.)
  **These knots are ribbon.** They show ribbon *disks* are non-unique; they give **no** SR candidate.
- Hayden–Piccirillo, trace embedding lemma work; Hayden, *An atomic approach to Wall-type stabilization
  problems*, arXiv:2302.10127. (UNVERIFIED beyond title.)
- Hayden, *Corks, covers, and Casson–Gordon invariants*; Hayden–Kjuchukova–Krishna–Miller–Powell–Sunukjian,
  *Brunnian exotic surface links*. (UNVERIFIED beyond title.)
- *Strong corks derived from the Akbulut cork*, arXiv:2601.02230 (2026). (UNVERIFIED beyond title.)
- Akbulut–Yasui, *Corks, exotic 4-manifolds and knot concordance*, arXiv:1505.02551. (UNVERIFIED.)

**Key structural point.** A knot slice in a **cork / contractible manifold `W ≠ B^4`** is not a CE candidate at
all until `W` is shown to be `B^4`; and if `W` is shown to be `B^4` the knot usually becomes visibly ribbon
(§6 pattern). Kjuchukova–Orr (arXiv:2604.00460, Thm 1.1 / Thm 7.1) give an irregular-dihedral-cover `Ξ`
obstruction, but it is a **homotopy-ribbon** obstruction, so it is *a priori dead* on any object already known
handle-ribbon — in particular on `18nh00000601`. (PARTIALLY VERIFIED via package [S13], [S18].)

**Verdict: DEAD for candidate supply; LIVE only as tooling.**

---

## 8. Larson–Meier, Meier–Zupan: generalized square knots and non-isotopic ribbon disks

- Larson–Meier, *Fibered ribbon disks*, J. Knot Theory Ramifications 24 (2015). (PARTIALLY VERIFIED.)
- Meier–Zupan, *Generalized square knots and homotopy 4-spheres*, arXiv:1904.08527: for `Q_{p,q} = T_{p,q} #
  T_{-p,q}`, homotopy 4-spheres built with a 2-handle along `Q_{p,q}` are **standard**; and they *produce* large
  families, for all even `n`, of `nR`-links that are **potential counterexamples to Generalized Property R**.
  (PARTIALLY VERIFIED — abstract.) So this paper **kills** the `Q_{p,q}` homotopy-sphere lane while **creating**
  a new GST-like `nR`-link supply.
- Meier–Zupan, *Knots bounding non-isotopic ribbon disks*, arXiv:2310.17564, J. Topology (2025): every
  generalized square knot `Q_{p,q}` bounds infinitely many pairwise non-isotopic **fibered, homotopy-ribbon**
  disks in `B^4` with diffeomorphic exteriors; when `q = 2`, infinitely many of these are genuine **ribbon**
  disks. Records the open question whether every ribbon disk bounded by a fibered knot is fibered.
  (PARTIALLY VERIFIED — abstract + package [S15].)

**Relevance to SR.** For `q ≠ 2`, the infinitely many fibered **homotopy-ribbon** disks are **not known to be
ribbon disks**. This is a *disk-level* rather than *knot-level* gap (the knot `Q_{p,q}` is obviously ribbon), so
it yields **no CE**, but it is the cleanest explicit demonstration that homotopy-ribbon ⇏ visibly ribbon at the
disk level. **Verdict: DEAD for CEs; important as a warning about handle-ribbon evidence.**

---

## 9. Fusion number / ribbon number lanes

Logic: if one could prove a lower bound `fusion number ≥ N` that is *incompatible* with any ribbon disk for a
knot certified slice, one gets a CE. In practice only *upper* bounds on ribbon-disk complexity are computed, so
this lane currently supplies **evidence**, not proofs.
- DG Table 7 (VERIFIED): of 1,633,786 ribbon disks found, 1,249,604 used 1 band, 381,869 used 2, 2238 used 3,
  75 used 4; DG stopped at 4. This is an upper bound on fusion number for each knot.
- DG §2.8 (VERIFIED): `18nh00098373` is the one knot in its class where no 2-band ribbon disk was found — a
  concrete high-fusion-number target.
- Torsion order of knot Floer homology (`[JMZ]` = Juhász–Miller–Zemke) bounds fusion number from below; DG §2.8
  cites this literature. (PARTIALLY VERIFIED.)
- *The twisting number of a ribbon knot is bounded below by its doubly slice genus*, arXiv:2404.07619.
  (UNVERIFIED beyond title.)
- Boden et al., arXiv:2209.15577, Prop. 6/8: ribbon ⇒ half-ribbon; `2g_4(K) ≤ g_{hr}(K) ≤ g_{ds}(K)`;
  half-ribbon ⇒ ribbon is **open**. (PARTIALLY VERIFIED — package [S21].)

**Verdict: WEAK.** No family here; a *method* awaiting a sharp lower bound.

---

## 10. Kawauchi / Miyazaki / Casson–Gordon — **THE LARGEST MISS**

### 10a. Miyazaki's `(2n,1)`-cables of fibered negative amphicheiral knots

**VERIFIED** — quoted literally from the introduction of Dai–Kang–Mallick–Park–Stoffregen, arXiv:2207.14187v2:
> "Explicitly, in [Miy94, Example 2] Miyazaki showed that if `K` is a fibered, negative amphicheiral knot with
> irreducible Alexander polynomial, then the `(2n,1)`-cable of `K` is not (homotopy) ribbon for any `n ≠ 0`.
> On the other hand, these knots are known to be strongly rationally slice (and thus algebraically slice)
> [Kaw80, Cha07, KW18]. While such cables are generally believed not to be slice, the fact that no argument has
> appeared in the literature has left open the possibility that these generate counterexamples to the
> slice-ribbon conjecture."

and the more general family (VERIFIED, same source):
> "More generally, if `K` is a fibered, negative amphicheiral knot with irreducible Alexander polynomial, then
> `K_{p,q} # −T_{p,q}` is rationally slice for any choice of cabling parameter `(p,q)`… For such `K`, work of
> Miyazaki [Miy94, Theorem 8.6] again implies that `K_{p,q} # −T_{p,q}` is not ribbon, except in the trivial case
> when `p` is zero."

**This is a canonical, decades-old, explicitly-named slice–ribbon candidate family — and the SR-Foxy package
does not contain it at all.** It is route (B): certified non-ribbon (in fact non-homotopy-ribbon), sliceness
open, with a *structural* reason to expect sliceness (strong rational sliceness + vanishing of all HFK, involutive
HFK, and Khovanov `s` invariants — VERIFIED from the DKMPS intro).

**Which members are DEAD:**
- `K = 4_1`, `(p,q) = (2,1)`: **DEAD.** DKMPS Thm 1.1 (Invent. Math. 238 (2024) 371–390) — `(4_1)_{2,1}` is not
  smoothly slice, in fact infinite order in `C`, and not slice in any `Z/2Z`-homology ball (Rmk 5.4). Proof:
  `Σ_2` bounds no **equivariant** `Z/2Z`-homology ball. (VERIFIED.)
- `K = 4_1`, **all** nontrivial cables: **DEAD.** Kang–Park–Taniguchi, arXiv:2505.03720 — every nontrivial cable
  of `4_1` has infinite order in `C`, via `κ_R^{(k)}` (real Seiberg–Witten Floer K-theory). (PARTIALLY VERIFIED.)
- `K ∈ {6_3, 8_12, 8_17}`, `(p,q) = (2,k)` with `k` odd: **DEAD.** DKMPS Thm 1.2 — "Let `K` be a Floer-thin knot
  with `Arf(K) = 1` and let `k ∈ N` be odd. Then `K_{2,k} # −T_{2,k}` is not smoothly slice, and in fact has
  infinite order in the smooth concordance group… Theorem 1.2 can be applied to the next few of Miyazaki's
  examples after `K = 4_1`: these are `K = 6_3, 8_12,` and `8_17`." (VERIFIED, quoted.)
- Also dead-ish: `17ns29 = Fig8[1]` in DG's tables is exactly `(4_1)_{2,1}`; DG Thm 6.2 records it, and cite an
  alternate proof "[ACMPS]" via genus bounds in definite 4-manifolds. (VERIFIED.)

**BEST EXPLICIT SMALLEST LIVE MEMBER (VERIFIED, quoted from DKMPS):**
> "The smallest fibered, negative amphicheiral knot with irreducible Alexander polynomial which is not subsumed
> by Theorem 1.2 is `10_17`."

⇒ **`(10_17)_{2,1}`, the `(2,1)`-cable of `10_17`, is a named, live, route-(B) candidate**: not ribbon
(Miyazaki), strongly rationally slice (Kawauchi), smooth sliceness **UNKNOWN**. Also live: `K_{p,q} # −T_{p,q}`
for `p` odd or `p ≡ 0 mod 4` and `K ∈ {6_3, 8_12, 8_17, 10_17, …}`, since DKMPS Thm 1.2 only covers `(2, odd)`
and `K` Floer-thin with `Arf = 1`.

**Amphicheirality background** (PARTIALLY VERIFIED): Kawauchi (2009) — every **strongly** negative amphichiral
knot is rationally slice. Di Prisa–Lee–Şavk, *Every negative amphichiral knot is rationally slice*,
arXiv:2509.21140 (25 Sep 2025) — extends to negative amphichiral links whose amphichiral map preserves each
component, and answers a question of Kim–Wu (2016) on Miyazaki knots by proving **every fibered negative
amphichiral knot is strongly negative amphichiral**. (PARTIALLY VERIFIED — abstract.)
S. Kim (BLMS 2018), *On rational sliceness of Miyazaki's fibered, −amphicheiral knots*, arXiv:1604.04870 —
directly on this family. (UNVERIFIED — PDF unreadable in this session; **must be re-fetched**.)

### 10b. Casson–Gordon
*A loop theorem for duality spaces and fibred ribbon knots*, Invent. Math. 74 (1983): a fibered knot is
homotopy-ribbon iff its 0-surgery fibration extends over a handlebody. Restated as Miller–Zupan Thm 1.4.
(PARTIALLY VERIFIED — package [S02].) This is the criterion that makes the *fibered* candidates
(`18nh00000601`, GST band sums, the `A_n(6_3)` family, all of Miyazaki's cables) tractable — and it is exactly
why those objects are already known homotopy-/handle-ribbon and thus immune to that whole battery.

### 10c. Gordon–Litherland, Kawauchi "slice knots with …"
No candidate family located in this sweep. (UNVERIFIED — not searched to exhaustion.)

---

## 11. 2024–2026 sweep, and the slice–ribbon conjecture **for links**

**New in 2025–2026 relevant to the problem** (all PARTIALLY VERIFIED unless noted):
- Dunfield–Gong, arXiv:2512.21825 (Dec 2025) — §4 above. VERIFIED.
- Oliveira-Smith, arXiv:2603.23717 (Mar 2026) — promotes `18nh00000601` to `[std B^4]`. VERIFIED (abstract).
- Agol–Ren, *Ribbon concordance of fibered knots and compressions of surface homeomorphisms*, arXiv:2603.10884:
  simplicial volume monotone under ribbon concordance of fibered knots (Thm 1.4); strong homotopy-ribbon
  concordance ⟺ monodromy compression (Thm 1.7); algorithmic finiteness of minimal compressions (Thm 1.9,
  Cor 1.11); §7.1 explicitly treats the `(2,1)`-cable of the figure-8. Detects **strong homotopy-ribbon**, not
  ribbon-vs-handle-ribbon. (PARTIALLY VERIFIED; local HTML copy in scratchpad.)
- Hom–Park, *Ribbon concordance and cabling*, arXiv:2608.06625 (Aug 2026) — minimum-height invariant from
  immersed-curve knot Floer; cabling constraints on ribbon concordance. No application to any ledger object found.
- Imori–Park–Taniguchi, arXiv:2607.12768 — singular instantons, unknotting number, ribbon concordance.
- Xiao, *Real Link Floer Homology*, arXiv:2604.21240 — no verified ribbon obstruction.
- Kjuchukova–Orr, arXiv:2604.00460 — dihedral-cover `Ξ` obstruction (homotopy-ribbon only).
- Diao–Pan–Yan, arXiv:2604.17737 — stable equivalence of GST links.
- Dunkerley, *A ribbon partial order for links and minimality detection via Heegaard Floer*, arXiv:2606.20802
  (18 Jun 2026): **strong ribbon concordance is a partial order on links**, extending Agol's theorem; identifies
  ribbon-minimal knots that are not transfinitely nilpotent; infinite families of minimal links. Does **not**
  address slice-ribbon for links. (PARTIALLY VERIFIED — abstract.) **MISSED by the package.**
- Kang–Park–Taniguchi, arXiv:2505.03720; Fukumoto–Taniguchi, arXiv:2501.07910 — §3/§10 above.
- *Exotic disks and singular instanton Floer homology*, arXiv:2606.05819. (UNVERIFIED beyond title.)
- *Heegaard Floer knot trace invariants, exotic 4-manifolds, and symplectic obstructions*, arXiv:2608.09734.
  (UNVERIFIED beyond title.) Potentially a **killer** for `r=0` RBG pairs and trace-based candidates.
- *An algorithmic search for knots bounding Möbius bands in `B^4`*, arXiv:2607.23582. (UNVERIFIED.)

**No preprint in 2024–2026 claims a counterexample to the slice–ribbon conjecture.** (VERIFIED by negative
search over "counterexample to the slice-ribbon conjecture", "slice but not ribbon", "candidate counterexamples",
restricted to 2024–2026; the only hits are the candidate-producing papers listed above.)

**Slice–ribbon for links — status.**
- Definitions (VERIFIED from GHMR §1 and DG §1.2): a link is **slice** if it bounds disjointly embedded smooth
  disks in `B^4`; **ribbon** if those disks can be chosen with no interior local maxima for the radial function
  (equivalently, immersed in `S^3` with only ribbon singularities).
- **I found no theorem in the literature asserting that a slice link need not be ribbon, and no explicit
  slice-but-not-ribbon link.** The question appears to be treated as **OPEN**, and in the same breath as the
  knot case. (PARTIALLY VERIFIED — negative search; this is *not* a proof that no such theorem exists.)
  **Do not repeat the folklore claim that "slice-ribbon is known false for links" — I could not source it.**
- **Definition issues that genuinely bite** (PARTIALLY VERIFIED): for links one must distinguish
  (i) *slice* (disjoint disks, any homology classes), (ii) *strongly slice / boundary slice* (each component
  bounds and the disks are "compatible"), and (iii) ribbon. For a link, "slice" does **not** imply each
  component is slice-in-a-compatible-way, and the concordance-invariance statements differ. Any claim about
  links must fix which notion is in play.
- Constraints that do exist for **ribbon links**: Eisermann, *The Jones polynomial of ribbon links*, Geom. Topol.
  13 (2009), Thms 1–2 — Jones-nullity and determinant congruences for `n`-component ribbon links. For `n = 1`
  these degenerate and give no slice/ribbon separation. (PARTIALLY VERIFIED — package [S22].)
- Kawauchi, *Ribbonness on classical link*, arXiv:2307.16483. (UNVERIFIED beyond title — worth reading; it may
  contain exactly the link-level statement sought.)
- The `L_{n,k}` of §1 are **slice links not known to be ribbon** — so the GST lane is *simultaneously* a
  link-level SR candidate lane. **Best explicit link candidate: `L_{3,1}`.** (VERIFIED via GHMR quotation.)

---

## 12. "Opposite direction": certified non-ribbon, sliceness open

| object | non-ribbon certificate | slice status | structural reason to expect slice |
|---|---|---|---|
| `(10_17)_{2,1}` and `K_{p,q} # −T_{p,q}`, `K` fibered neg.-amph., irred. `Δ` | Miyazaki 1994 Ex. 2 / Thm 8.6 (VERIFIED via DKMPS) | **UNKNOWN** | strongly **rationally slice** (Kawauchi); all HFK, `ι`-HFK, `s` vanish |
| `D_{n,m} = A_n(6_3) # −A_m(6_3)` | Miyazaki Thm 5.5 via Abe–Tagami Cor 4.3 | UNKNOWN (slice ⟺ `[K_n]=[K_m]`) | same 0-surgery; Akbulut–Kirby-style expectation |
| Gompf–Miyazaki Prop. 3.1 pair `K # −K'` | Gompf–Miyazaki 1995 (PARTIALLY VERIFIED via Tagami) | UNKNOWN | homeomorphic 0-surgeries; all known algebraic slice obstructions vanish |
| Hom–Park `P(K,J,p,q_1,q_2)` | Hom–Park Thm 1.1 / Cor 1.3 | UNKNOWN; **algebraically slice** | only if a 4-term cable relation holds — expected false |
| `18nh00098198`, `16n68278`, `17nh0010647` | — (not non-ribbon; these are *expected non-slice*) | UNKNOWN | **NOT SR candidates** — listed to prevent misuse |

**Are Miyazaki's examples topologically slice?** `(4_1)_{2,1}` and friends are **algebraically slice**
(VERIFIED via DKMPS) but their Alexander polynomials are not 1, so the Freedman criterion does not apply and
topological sliceness is **not** established by it. (PARTIALLY VERIFIED; no source found either way.)

**The generic killer for this whole tier**: Miller–Piccirillo `d`-invariants (arXiv:1702.03974) for
same-0-trace pairs; DKMPS/Kang–Park–Taniguchi equivariant and real-Floer-theoretic obstructions for cables;
Fukumoto–Taniguchi real 10/8 for connected sums. Each kills specific members and none kills a family.

---

## 13. Ranked table of explicit candidate objects

Ambient key: `S` = std `B^4`; `H` = homotopy `B^4` only; `Q` = rationally slice only; `?` = unknown.

| # | object | source | smooth slice (ambient) | non-ribbon status | what killed it / blocks it | verdict |
|---|---|---|---|---|---|---|
| 1 | `18nh00000601` | DG 2512.21825 Thm 5.14 + Oliveira-Smith 2603.23717 Cor 1.1.1 | **YES, `S`** (fibered, genus 5, handle-ribbon) | UNKNOWN; exhaustive search failed | alive; all homotopy-/handle-ribbon obstructions logically dead | **LIVE — rank 1** |
| 2 | `K_{B/G}(0,0,0,1,2,−1)` (both knots) | MP 2102.04391 family; GHMR 2304.09304 §6 | one ⟹ other, `r=0` ⟹ **`S`** once either is ribbon | UNKNOWN; both unknown even for sliceness | needs one ribbon disk found | **LIVE — rank 2 (MISSED)** |
| 3 | `K_{B/G}(0,0,0,−1,2,1)` | same | same | same | same | **LIVE (MISSED)** |
| 4 | `K_{B/G}(0,0,−2,0,0,1)` | same | same | same | same | **LIVE (MISSED)** |
| 5 | `(10_17)_{2,1}` | Miyazaki Ex. 2; DKMPS intro | **UNKNOWN** (`Q` yes) | **YES — proved non-(homotopy-)ribbon** | needs a slice disk; DKMPS Thm 1.2 does not reach `10_17` | **LIVE (route B) — rank 3 (MISSED)** |
| 6 | `K_{p,q} # −T_{p,q}`, `K ∈ {6_3,8_12,8_17,10_17}`, `(p,q)` outside `(2,odd)` | Miyazaki Thm 8.6 | UNKNOWN (`Q` yes) | **YES** | same | **LIVE (MISSED)** |
| 7 | GST band sum of `L_{3,1}` (`B_{3,1}`) | GST 1103.1601 §8 | **YES, `S`** | UNKNOWN; GHMR search failed (but also failed on known-ribbon `L_{1,1}, L_{2,1}`) | Abe–Tange Conj 6.1 predicts ribbon; huge diagram | **LIVE (weak)** |
| 8 | `L_{3,1}` as a **link** | GST §8; GHMR §7 | **YES, `S`** (slice link) | UNKNOWN | same | **LIVE (link-level)** |
| 9 | `B_{n,k,b}` general GST band sums, `n≥2, k≠0, (n,k)≠(2,1)` | GST §8 | **YES, `S`** per fixed band | UNKNOWN, band-dependent | not one knot; must fix `(n,k,b)` | **LIVE (generator)** |
| 10 | `D_{n,m} = A_n(6_3) # −A_m(6_3)` | Abe–Tagami 1502.01102 | UNKNOWN | **YES** (Miyazaki Thm 5.5) | needs `[K_n]=[K_m]` in `C` | **LIVE/WEAK (route B)** |
| 11 | Gompf–Miyazaki Prop 3.1 connected sum | Gompf–Miyazaki 1995 | UNKNOWN | **YES** | Miller–Piccirillo `d`-invariants may already kill it — **UNCHECKED** | **LIVE/WEAK (MISSED)** |
| 12 | Hom–Park `P(T_{2,3},T_{2,5},2,1,3)` | HP 2507.20455 Cor 1.3 | UNKNOWN; **algebraically slice** | **YES** | 4-term cable relation expected false (DHST) | **WEAK (route B)** |
| 13 | `A_j(J)`, `J` ribbon w/ annulus presentation | Abe–Tange 1305.7492 Thm 3.1 | **YES, `S`** | UNKNOWN in general | many subfamilies already ribbon | **LIVE (generator)** |
| 14 | `A_n(8_20)`, `n ≥ 0` | Abe–Tange Thm 5.4 | YES, `S` | **RIBBON** | proved ribbon | **DEAD** |
| 15 | `L_{1,1}`, `L_{2,1}`, `L_{n,0}`, `L_{2,1}` band sums | GST §8 | YES, `S` | **RIBBON** | proved ribbon in GST | **DEAD** |
| 16 | `(4_1)_{2,1} = 17ns29` and all `4_1` cables | Kawauchi/Miyazaki | **NOT SLICE** | non-ribbon | DKMPS Invent. 2024; Kang–Park–Taniguchi 2505.03720 | **DEAD** |
| 17 | `(6_3)_{2,k}`, `(8_12)_{2,k}`, `(8_17)_{2,k}`, `k` odd | Miyazaki | **NOT SLICE** | non-ribbon | DKMPS Thm 1.2 | **DEAD** |
| 18 | DG's 513 + 41 + 4 "suspicious" knots (`19nh051162051`, `17nh0016322`, `17nh0026540`, `17nh0298397`, `19nh000077044`, `19nh000187109`, `19nh003361975`, …) | DG §2.6–2.7 | YES, `S` | **RIBBON** | expanded band search found disks | **DEAD** |
| 19 | GHMR/MP knots `K_G(0,1,−1,−1,1,0)`, `K_B(0,1,2,0,−1,−1)`, `K_B(0,0,2,0,0,−1)`, `K_G(2,0,0,−1,2,−1)` | GHMR §6 | YES, `S` | **RIBBON** | 3-band search / Piccirillo R-link argument | **DEAD** |
| 20 | `K_{B/G}(−2,0,0,−1,2,−1)`, `K_{B/G}(−1,0,−1,−1,2,−1)` | GHMR §6 | UNKNOWN | UNKNOWN | `r ≠ 0` ⟹ these are **SPC4** candidates, not SR | **not an SR candidate** |
| 21 | Akbulut–Kirby / Cappell–Shaneson-derived knots | Gompf 1991, Gompf 2010, Akbulut | YES, `S` after standardization | **RIBBON** | standardized, then ribbonized | **DEAD** |
| 22 | Hayden exotic ribbon disk pairs | Hayden 2003.13681 | YES, `S` | **RIBBON knots** | knots are ribbon; only the disks are exotic | **DEAD** |
| 23 | `Q_{p,q}` non-isotopic fibered homotopy-ribbon disks, `q ≠ 2` | Meier–Zupan 2310.17564 | knot is ribbon | knot RIBBON; *disks* not known ribbon | disk-level, not knot-level | **DEAD for CE** |
| 24 | Owens–Swenton **bounty knots**: `16a158248, 16a288139, 16a289378, 16a300620, 16a309401, 16a346626, 17a82415` | Owens–Swenton 2102.11778 + bounty page | **UNKNOWN** (expected *obstructed*, i.e. non-slice) | n/a | GHMR also failed; OS "expect them to be obstructed in some way" | **not an SR candidate** (MISSED, worth tracking) |
| 25 | DG Table 1 inscrutables (`K13n65`, …, `K14n21673`, 55 knots ≤15 cr.) | DG §1.18 | UNKNOWN | n/a | sliceness unknown | **pool, not candidates** |
| 26 | `18nh00098373` | DG §2.8 | YES, `S` (ribbon) | RIBBON; **fusion number ≥ 3?** | ribbon | **DEAD for CE; LIVE for fusion-number lane** |
| 27 | positive Whitehead double of the left-handed trefoil | GHMR §7 | **UNKNOWN** (widely expected non-slice) | UNKNOWN | no ribbon disk found; sliceness unknown | **not an SR candidate** |
| 28 | knots slice in a cork / contractible `W ≠ B^4` | Hayden, Akbulut–Yasui | `W`, not `S` | UNKNOWN | ambient not standard ⟹ disqualified until standardized | **DEAD until standardized** |

---

## 14. Candidate generators — mechanical recipes for fresh `[std B^4]`-slice knots with non-automatic ribbonness

**G1. `r = 0` super-special RBG links (STRONGEST).** Build a super-special RBG link with `b = g = 0` and
**`r = 0`**. Then `K_B` and `K_G` have **diffeomorphic traces** (DG Thm 5.8), so by the Trace Embedding Lemma
they have the **same smooth slice status in the standard `B^4`**. Find a ribbon disk for one; the other is then
certified slice in **std `B^4`** with **no inherited ribbon disk**. This is the only generator in the literature
that yields `[std B^4]` *by construction* without a standardization step. Existing unmined stock: the three
GHMR `r = 0` pairs (rows 2–4 above). Fresh stock: DG generated **>500,000 0-friend pairs** and a search method
(§5.11) for the RBG links realizing them; filtering those to `r = 0` and running the ribbon search on one side is
a directly executable program. **(VERIFIED mechanism.)**

**G2. `r` odd / general 0-friends + standardization.** Same but `r` odd: yields only `[homotopy B^4]`; a separate
standardization (à la Oliveira-Smith's handle calculus on `X_{DG}`) is needed to promote to `[std B^4]`. This is
exactly the `18nh00000601` pipeline and is reproducible on other DG 0-friend pairs whose ribbon side is known.

**G3. GST band sums with varying bands.** Fix `(n,k)` with `n ≥ 3`; vary the band `b` joining the two components
of `L_{n,k}`. Each band gives a distinct knot `B_{n,k,b}`, each slice in **std `B^4`**, each with independent
ribbon status. Meier–Zupan's `nR`-links for even `n` (arXiv:1904.08527) give a *second*, different supply of such
links. **Caveat**: all are belt spheres in no-3-handle `B^4` diagrams, hence hostages to Abe–Tange Conj. 6.1.

**G4. Belt spheres of 2-handles in no-3-handle handle diagrams of `B^4`** (Abe–Tange §6/Conj 6.1). Any such belt
sphere is slice in **std `B^4`**. If Conj. 6.1 is **false**, this construction is where a CE lives; if true, the
whole lane (including G3) collapses. **A deliberate attempt to falsify Conj. 6.1 is therefore a high-value
research direction in its own right.**

**G5. Annulus twists / annulus modifications of ribbon knots with special presentations.** Abe–Tange Thm 3.1
(`A_j(J)` for `J` ribbon with annulus presentation) and Park's `n`-twist annulus modifications (arXiv:1512.00401)
— but **use only the "smoothly slice" outputs, never the "exotically slice" ones**. Tagami arXiv:2010.13283 gives
the explicit dictionary annulus presentation ↔ dualizable pattern ↔ RGB-diagram, so any G5 output can be
re-coordinatized as a G1/G2 output and vice versa.

**G6. `K # J` with `J` ribbon (DG §1.17's Teichner Lemma 2.5 trick).** `K` is smoothly slice iff there is a ribbon
`J` with `K # J` ribbon. Choosing `J` so `K # J` is ribbon-concordant to something simpler than `K` certifies `K`
slice in **std `B^4`** without exhibiting a ribbon disk for `K`. DG got 513 knots this way — all ended up ribbon,
but the *mechanism* is a clean route-(A) certifier and is cheap to run at higher crossing number.

**G7. Miyazaki cables of fibered negative amphicheiral knots (route B).** For `K` fibered negative amphicheiral
with irreducible `Δ_K` and `(p,q)` outside the resolved range, `K_{p,q} # −T_{p,q}` comes with a **free non-ribbon
certificate**. The work is then all on the slice side. Start at `K = 10_17`, `(p,q) = (2,1)`.

**G8. Miyazaki/Abe–Tagami 0-surgery pairs (route B).** Any two knots `K, K'` with the same 0-surgery, both prime
fibered with a common irreducible Alexander polynomial, give `K # −K'` **non-ribbon for free** (Miyazaki Thm 5.5).
A CE follows from any proof that `K ≃ K'` in `C`. Stock: Abe–Tagami `A_n(6_3)`; Gompf–Miyazaki dualizable-pattern
pairs; DG's 500,000 0-friend pairs filtered to fibered-prime-common-`Δ`.

**G9. Whitehead doubles — NOT recommended.** The positive Whitehead double of the left-handed trefoil is on
GHMR's unknown list, but its *sliceness* is unknown (and generally expected false), so it is a route-(B) object
with no non-ribbon certificate — the worst of both worlds.

---

## 15. What the existing package MISSED (action list, ordered)

1. **Miyazaki's `(2n,1)`-cables / `K_{p,q} # −T_{p,q}` of fibered negative amphicheiral knots, live member
   `(10_17)_{2,1}`.** The canonical historical SR candidate family, completely absent from `CANDIDATE_LEDGER.md`.
   Certified non-ribbon, strongly rationally slice, smooth sliceness open.
2. **The three `r = 0` Manolescu–Piccirillo/GHMR pairs** `K_{B/G}(0,0,0,1,2,−1)`, `K_{B/G}(0,0,0,−1,2,1)`,
   `K_{B/G}(0,0,−2,0,0,1)` — six named knots, explicitly flagged by GHMR as potential SR (not SPC4)
   counterexamples, requiring only one ribbon disk to promote.
3. **Gompf–Miyazaki 1995, Prop. 3.1** — the prototype non-ribbon connected sum of same-0-surgery knots, the
   direct ancestor of the Abe–Tagami lane.
4. **JungHwan Park, arXiv:1512.00401** — annulus *modifications* as an independent slice-knot generator.
5. **Meier–Zupan arXiv:1904.08527 `nR`-links** — a second GST-like supply of slice links, for all even `n`.
6. **Owens–Swenton bounty knots** (7 named alternating knots) and DG's `18nh00098373` (fusion-number lane).
7. **Kang–Park–Taniguchi arXiv:2505.03720 and Fukumoto–Taniguchi arXiv:2501.07910** — the current frontier of
   killers on the cable lane; they define exactly how far the Miyazaki family has been cleared.
8. **Dunkerley arXiv:2606.20802** — ribbon partial order for **links**; the natural home for a link-level
   slice–ribbon attack, and the package has no link-level section at all.
9. **DG's own quantitative caveat** — "we expect there are hundreds of other similarly obscure ribbon disks
   among the 11,383 knots whose smooth slice status is unknown" — should be recorded in the ledger as the
   authors' own discount on search-failure evidence.

## 16. Global verdict

**No counterexample exists in the literature as of 2026-09-11.** (VERIFIED by exhaustive negative search.)
Exactly one object is certified slice in the **standard** `B^4` with genuinely open ribbon status and a small
explicit diagram: **`18nh00000601`**. The three `r = 0` RBG pairs are the cheapest new route-(A) targets. The
Miyazaki `(10_17)_{2,1}` cable is the cheapest new route-(B) target and carries a *free* non-ribbon certificate.
The strongest structural warning is §6: every previous `[homotopy B^4]` candidate that was standardized
subsequently turned out to be ribbon.
