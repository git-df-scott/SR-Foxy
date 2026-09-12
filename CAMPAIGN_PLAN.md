# Campaign plan: a counterexample to the Slice–Ribbon Conjecture

Date: 2026-09-11. Supersedes `SESSION0_BATTLEFIELD.md` where they conflict. Every factual claim below traces to `SOURCES.md` (`[Sxx]`) or to the five audit reports in `research/`. Assumption stated up front: "gsd knots" in the tasking is read as **GST knots** (Gompf–Scharlemann–Thompson).

## 0. Binding result, stated first

**No counterexample exists in the literature as of 2026-09-11**, and **no known invariant can prove one.** Sixty-four years of candidates have died in exactly four ways (shown ribbon, shown non-slice, exotic ambient standardized, or never a candidate). Every obstruction ever labelled "ribbon obstruction" is now known to obstruct at the homotopy-ribbon or handle-ribbon level, and the only certified-slice candidates are already proved handle-ribbon. Therefore:

> **A counterexample proof requires at least one new theorem.** No amount of computation with existing invariants can finish the job. The campaign is designed to (1) produce that theorem or discover it is unnecessary, (2) run the few cheap experiments that can decisively kill or promote candidates, and (3) keep a candidate pipeline alive so a new tool has targets.

Calibration from the adversarial memo (`research/05_adversarial_memo.md`): roughly even odds that a counterexample exists, around 5% that one is provable by 2028 with current tools. The likelier near-term headline is "18nh00000601 is ribbon". The plan is built so that outcome is found fast and cheaply rather than after a wasted year.

## 1. What the conjecture says and what a counterexample is

**Conjecture (Fox 1962, Kirby Problem 1.33).** Every smoothly slice knot in S³ is ribbon.

Definitions, all as printed in [S01], [S02]:

| term | definition | certificate that proves it |
|---|---|---|
| smoothly slice | bounds a smoothly embedded disk D in the **standard** B⁴ | an explicit disk, or a trace-embedding / handle-calculus argument that names standard B⁴ |
| ribbon | bounds a slice disk with no local maxima of the radial function; equivalently an immersed disk in S³ with only ribbon singularities; equivalently a band-move movie from K to an unlink | a band movie, or an unlink derivative on some Seifert surface ([S02, Prop 1.1]) |
| handle-ribbon (= strongly homotopy-ribbon) | bounds a disk in a homotopy 4-ball whose exterior has no 4-dimensional 3-handles | an R-link derivative ([S02, Thm 1.3]) |
| homotopy-ribbon | bounds a disk with π₁(S³∖K) → π₁(B⁴∖D) surjective | for fibered knots: monodromy extends over a handlebody (Casson–Gordon 1983) |

Hierarchy: **ribbon ⇒ handle-ribbon ⇒ homotopy-ribbon ⇒ slice.** No converse is known; [S02] says none of the inclusions is known to be strict.

**A counterexample (CE)** is an explicit knot K together with
- (a) a proof that K is smoothly slice in standard B⁴, and
- (b) a proof that K bounds no ribbon disk.

Two production routes:
- **Route A**: start from a certified-slice knot with unknown ribbon status, prove (b).
- **Route B**: start from a certified non-ribbon knot, prove (a), usually by proving a smooth concordance equality.

**The structural obstacle.** Every known generator of Route-A candidates (0-surgery/RBG trace embeddings, GST band sums, annulus twists, belt spheres of no-3-handle B⁴ diagrams) manufactures knots whose slice disk exterior is built from the exterior of a *ribbon* disk of a partner, and is therefore **handle-ribbon by construction**. The single exception is the Teichner-lemma sum K # J (DG §2.6), whose output disk is not automatically handle-ribbon. Consequently, for every candidate in the ledger, proving (b) means separating **ribbon from handle-ribbon**, and the only exactly calibrated separator known is

> unlink derivative (ribbon) versus R-link derivative (handle-ribbon), [S02, Prop 1.1 vs Thm 1.3],

which for the derivative link is literally the Generalized Property R question and quantifies over *all* Seifert surfaces. No finiteness theorem exists for that quantifier.

Full trap list: `research/05_adversarial_memo.md` §6. The five that killed the most candidates: homotopy ball vs standard B⁴; homotopy-ribbon vs ribbon; conjecture used as theorem; search failure as evidence; same 0-surgery treated as concordance.

## 2. Board state after the 2026-09-11 audit

| lane | object | (a) slice in std B⁴ | (b) non-ribbon | route | verdict |
|---|---|---|---|---|---|
| 1 | `18nh00000601` = K_G | **proved** [S01, Cor 1.1.1], fibered genus 5, handle-ribbon [S01, Thm 1.2] | open; ≤4-band searches failed | A | **primary** |
| 2 | r = 0 RBG pairs K_{B/G}(0,0,0,1,2,−1), (0,0,0,−1,2,1), (0,0,−2,0,0,1) | one ribbon disk on either side certifies both | open | A-generator | **new, cheap** |
| 3 | GST band sum B_{3,1} and family B_{n,k,b} | proved [S04 §8] | open; Abe–Tange Conj 6.1 predicts ribbon | A | live, secondary |
| 4 | Miyazaki cables, live member (10_17)_{2,1}; K_{p,q} # −T_{p,q}, K ∈ {6_3, 8_12, 8_17, 10_17} outside (2, odd) | open; strongly rationally slice | **proved** (Miyazaki via [S23]) | B | **new, deepest history** |
| 5 | Abe–Tagami D_{n,m} = A_n(6_3) # −A_m(6_3) | open; slice iff [K_n] = [K_m] | **proved** [S06,S07] | B | live/weak |
| 6 | Gompf–Miyazaki Prop 3.1 pair | open | proved [S29] | B | weak, unchecked killer |
| 7 | Hom–Park P(K,J,p,q₁,q₂) | open; algebraically slice | proved [S08] | B | weak |
| dead | Turaev π³ door; 4_1 cables; DG's 553; Abe–Tange 8_20 family; MP's 5 topologically slice knots | | | | closed |

## 3. Campaign architecture

Six workstreams, three phases, hard gates. Each workstream has an owner role, deliverables, and a kill condition. Nothing advances past a gate on search failure alone.

```
Phase 0 (weeks 0–4)   Foundations: environment, data, independent audit of [S01]
Phase 1 (weeks 4–16)  Decisive experiments on K_G; route-B invariant battery; generators
Phase 2 (weeks 16–52) Theory program for a ribbon-only necessity; scaled searches
Gate G1 after Phase 1: is K_G still standing? Is any route-B object still standing?
Gate G2 after Phase 2: has a ribbon-only necessity (or finiteness theorem) been proved?
```

### WS0. Foundations and verification hygiene

1. **Independent audit of Oliveira-Smith [S01].** The flagship's sliceness rests on one unrefereed single-author preprint. Re-derive Thm 1.1 (standardization of X_DG) and Cor 1.1.1 step by step; reproduce the handle calculus in a Kirby-calculus tool; confirm the trace-embedding lemma is applied with the correct framing and orientation. Deliverable: `audits/S01_audit.md` with every diagram move checked. **Kill condition:** an error in Thm 1.1 demotes K_G to "slice in a homotopy ball" and the whole Route-A board collapses to zero certified objects.
2. **Obtain primary data.** `18nh00000601` is **done**: `data/knots/18nh00000601.json` (Burton census row 602, knot signature, PD codes, braid word, HFK, volume, cover homology, reproduced twice). Remaining: the six r = 0 RBG knots from [S26]/[S25]; GST L_{3,1} and the Figure 2 band (reconcile Regina's built-in `ExampleLink.gst()`, which computes as genus 10 and non-fibered, with the paper's figure); A_n(6_3) for |n| ≤ 4 from the annulus presentation in [S06, §5]; (10_17)_{2,1}. Store each as `data/knots/*.json` with PD code, source, and an isometry check against the source.
3. **Environment.** See §5. Pin versions; every result must be reproducible from `env/` by a fresh machine.
4. **Textual recoveries still open.** Kirby list Problem 1.33 commentary (primary); Gompf–Miyazaki 1995 full text (Prop 3.1 exact statement); Baldwin–Hanselman–Sivek [BHS26] arXiv id; Kim arXiv:1604.04870 on rational sliceness of Miyazaki knots.

### WS1. K_G decisive experiments (Route A, lane 1)

The purpose is to resolve K_G one way or the other as cheaply as possible. Order matters: the cheap kill first.

**1.1 Extended band search, 5 to 7 bands, derivative-guided.** DG's search stopped at 4 bands; K_G has genus 5, so a ribbon disk whose natural Seifert surface is the fiber would have 5 bands and is structurally invisible to their search. Steps:
- Compute the genus-5 fiber surface F and monodromy φ explicitly (WS0.2 data, SnapPy/Regina + flipper/curver).
- Extract the R-link derivative L⁺ ⊂ F exhibited in [S01, §3]. Verify it is an R-link (0-surgery on L⁺ is #⁵ S¹×S²) by exact recognition in Regina.
- Search for handleslide trivializations of L⁺ as a framed 5-component link (KLO or a custom handleslide enumerator with a move budget; also the stable version à la [S14]). **If L⁺ handleslides to the unlink, K_G is ribbon and the lane closes.**
- Search unlink derivatives on F directly. The algebra is small: H₁(Σ₂) = Z/25 is cyclic, so the double-branched-cover linking form has exactly one candidate metabolizer (Σ₃: ≤ 8, Σ₅: ≤ 32). The integral rank-5 Lagrangians of the Seifert form on Z¹⁰ are infinitely many, so enumerate them under an explicit height bound, realize each class as an embedded multicurve on F via the mapping-class-group action, and certify unlink-ness with Regina normal surfaces (`isHandlebody(5)` on the complement). Report the bound and the coverage honestly.
- Run a diagrammatic band search with budget 5–7 bands on shaken diagrams of K_G, seeded by the bands dual to L⁺.
- Deliverable: `results/KG_band_search.md` with the exact search space covered. **Search failure is recorded as coverage, never as evidence.**

**1.2 Hand trace of the handle calculus (Abe–Tange style).** Abe–Tange killed the Omae family by tracing the belt sphere through a "rather troublesome" handle calculus to an explicit ribbon presentation [S05, Thm 5.4, Lemma 5.1]. Apply Lemma 5.1's method to the no-3-handle diagram of B⁴ from [S01]: attempt to reduce it to the empty diagram by slides and 1/2-cancellations only. Success proves K_G ribbon. Failure with a documented obstruction (a forced 2/3 pair) is the first concrete data point for Abe–Tange Conj 6.2.

**1.3 The minimal-genus reduction (theory task, small).** Prove or refute: *for a fibered knot of genus g, any ribbon disk whose associated Seifert surface (in the sense of the proof of [S02, Prop 1.1]) has genus g is carried by the fiber surface, up to isotopy.* Ingredients: uniqueness of the minimal-genus Seifert surface of a fibered knot; the exact genus bookkeeping in the Cochran–Davis/Miller–Zupan construction (genus of the surface produced by a disk with n bands versus ribbon number). If true, "K_G has a 5-band ribbon disk" becomes a statement about multicurves on one explicit surface, and WS1.1's derivative enumeration is complete for that band count. **This lemma is the campaign's first theorem-grade deliverable and is plausibly provable in weeks.**

**1.4 Casson–Long/Agol–Ren compression enumeration.** Enumerate the finitely many minimal compressions of φ up to symmetry ([S09, Thm 1.9]). This lists all strong homotopy-ribbon predecessors ([S09, Cor 1.11]); it does **not** decide ribbonness (Errata E2). Its value: each compression corresponds to a handlebody extension and a candidate disk; every one of them is a target for WS1.1's unlink test. Record which compression realizes the [S01] disk.

**Gate G1 for K_G:** either a ribbon disk (lane closed, publish the disk), or a fully documented negative with the WS1.3 lemma proved and the genus-5 derivative orbit exhausted under an explicit complexity bound.

### WS2. Route-B battery and concordance search (lanes 4–7)

Route B needs a smooth concordance or slice disk for a knot everyone expects to be non-slice. Modern tools are built to disprove; the plan uses them as a cheap filter and then attacks survivors constructively.

**2.1 Kill battery** on (10_17)_{2,1}; K_{p,q} # −T_{p,q} for K ∈ {6_3, 8_12, 8_17, 10_17} with (p,q) outside DKMPS's range; D_{n,m} for |n|,|m| ≤ 3; the Gompf–Miyazaki pair; Hom–Park P(T_{2,3}, T_{2,5}, 2, 1, 3). Invariants: τ, ε, Υ, ν⁺ (HFK calculator via SnapPy), s (KnotJob/Khoca), d-invariants of branched covers (Dunfield–Gong/SnapPy 3.3 code), Levine–Tristram and Casson–Gordon signatures, twisted Alexander (HKL), Miller–Piccirillo trace d-invariants for the same-0-trace pairs [S28], DKMPS-style equivariant d-invariants of Σ₂, real Seiberg–Witten K-theoretic κ_R (by literature lookup, not computed). Each row of `results/routeB_battery.csv` records value, tool, and what it obstructs. **Kill condition per object:** any nonvanishing invariant.
**2.2 Common upper-bound search (constructive).** [K_n] = [K_m] holds if there is a knot J with K_n ≤ J and K_m ≤ J in the ribbon-concordance order (both ribbon concordant to J). Enumerate J = K_n banded with one or two unknotted components (all band positions up to a diagram budget), canonicalize by SnapPy isometry signature, and intersect with the analogous set for K_m. A hit is a smooth concordance and an instant CE for D_{n,m} (by [S06, Cor 4.3]). This is the only search in the plan whose success is a proof rather than evidence. Same search for the Gompf–Miyazaki pair. Related: Agol–Ren Question 1.15 asks exactly whether such a common fibered upper bound must exist for concordant fibered knots.
**2.3 Direct slice-disk search for (10_17)_{2,1}.** Its slice disk, if it exists, is non-ribbon, so band searches cannot find it. Search instead for J ribbon with (10_17)_{2,1} # J ribbon (Teichner lemma, DG §2.6 method), J ranging over small ribbon knots. Success proves sliceness; combined with Miyazaki this is a CE.

### WS3. Candidate generators (Route A pipeline)

**3.1 The six r = 0 RBG knots.** Run the full DG ribbon search plus WS1.1-style 5–7 band search on each. A ribbon disk on either side of a pair certifies the partner slice in standard B⁴ ([S25] §6 mechanism). The partner is then handle-ribbon by construction (exterior = ribbon-disk exterior of the partner), so it lands exactly where K_G sits, but as a second, independent target. Also run the standard non-slice battery first; a nonvanishing obstruction on either knot kills the pair.
**3.2 DG 0-friend pairs filtered to r = 0.** Using the Dataverse data and DG §5.11's RBG-realization method, filter the >500,000 0-friend pairs to super-special r = 0 realizations where one side is known ribbon. Each such pair yields a certified-slice knot with no inherited ribbon disk. Expect most to be ribbon quickly; keep survivors.
**3.3 Teichner-lemma sums at 20–21 crossings.** The only generator whose output is not automatically handle-ribbon, so the classical homotopy-ribbon battery (Casson–Gordon extension, Kjuchukova Ξ [S13], Friedl twisted-Alexander [S19]) becomes **live** on its outputs. Run on the DG unresolved pile (11,383 knots) with J ∈ {small ribbon knots}. Survivors get the homotopy-ribbon battery; a nonvanishing homotopy-ribbon obstruction on a Teichner-certified slice knot is a CE.
**3.4 GST lane maintenance.** Fix B_{3,1} exactly (pin the figure number from the journal PDF). Check thickenability of ⟨x,y | yxy = xyx, x^{n+1} = y^n⟩ against Lackenby [S32]; if thickenable, the AC-hardness story weakens and the lane is deprioritized further. Do not run more ML band searches (calibrated worthless, Errata E10).

### WS4. Theory program: a ribbon-only necessity

This is the workstream a counterexample proof cannot do without. Ranked by leverage.

**4.1 Fibered ribbon-disk completeness.** Open question (Meier–Zupan [S15]): is every ribbon disk bounded by a fibered knot fibered? If yes, then for fibered knots ribbon disks correspond to handlebody-fibered disks, i.e. to monodromy compressions, and the finite list from [S09] contains every ribbon disk of K_G up to the relevant equivalence. Combined with an exact unlink test this gives a certificate-grade decision procedure for K_G. Attack: study the Larson–Meier characterization [S37]; try to prove that a ribbon disk for a fibered knot can be isotoped to a fibered one by pushing minima into the fiber structure; alternatively look for a counterexample among Meier–Zupan's non-fibered constructions. **Double-edged by design:** either outcome is decisive for K_G.
**4.2 Derivative finiteness on a fixed surface.** Prove that for a fixed Seifert surface F, unlink derivatives fall into finitely many mapping-class orbits, or that unlink-ness forces bounded curve complexity. This is what would make WS1.1 complete beyond the minimal genus.
**4.3 Wirtinger-presentation lead (to be verified before use).** Ribbon disk exteriors have π₁ presentations of Wirtinger type with deficiency 1 (Yajima-type results for ribbon 2-knots; the disk version needs checking); handle-ribbon exteriors have deficiency-1 presentations without the Wirtinger form. Question: does the free-by-cyclic group π₁(H ×_Φ S¹) of K_G's disk exterior admit a Wirtinger deficiency-1 presentation? Caveat: if a ribbon disk with the same exterior group exists, no π₁-only invariant can separate. Low priority, one-week feasibility check.
**4.4 Abe–Tange Conjecture 6.1.** Prove or disprove: every belt sphere of a 2-handle in a no-3-handle diagram of B⁴ is ribbon. Proof closes lanes 1–3 and the annulus-twist lane in favour of the conjecture. Disproof is a CE by construction (sliceness certified in standard B⁴). Only known proof technique is [S05, Lemma 5.1]; Conj 6.2 predicts it sometimes fails. WS1.2's hand trace is the pilot.
**4.5 Ribbon-only quantitative theory.** Fusion number F versus strong-homotopy fusion number F_sh differ arbitrarily [S34]; ribbon number bounds are computable [S33]. None obstructs ribbonness outright, but a theorem of the form "handle-ribbon with exterior complexity c forces F ≤ f(c)" would convert the finiteness in [S33] into an obstruction. Investigate whether [S34]'s cabling examples refute any such bound.
**4.6 Explicitly not pursued** (proved dead against handle-ribbon targets): Turaev π³ (Errata E1), Casson–Gordon extension tests, metabelian/twisted-Alexander homotopy-ribbon restrictions, irregular dihedral Ξ, Park–Powell, Zemke/Levine–Zemke/Gujral–Levine injectivity, DLVVW instanton ribbon-cobordism, Agol–Ren/Baldwin–Sivek monotonicity (all hold for ≤_h), equivariant ribbon obstructions (a ribbon disk need not respect a symmetry), Lagrangian-concordance obstructions (wrong direction). Grigsby's braided-banded attempt [S35] is a documented negative. See `research/02_ribbon_only_obstructions.md`.

### WS5. Link-level lane (optional, low cost)

The slice-ribbon question for links is open (no source found asserting otherwise). GST's L_{3,1} is a slice link not known to be ribbon. Eisermann's Jones-nullity and determinant-mod-32 theorems [S22] are genuinely ribbon-only for links with ≥ 2 components and have no known handle-ribbon upgrade. Compute null V(L_{3,1}) and det V mod 32; a violation would be a link-level CE. One afternoon of computation; expected to vanish.

### WS6. Reporting discipline

- Every result file states: object, exact certificate type (proof / search coverage / invariant value), tool and version, and a reproduction command.
- Search results are reported as coverage statements. The word "evidence" is not used for search failure.
- Preprint theorems are cited as theorems in that version. Unrefereed load-bearing results ([S01], [S09], [S08], [S14], [S32]) are flagged in every deliverable that depends on them.
- Orientation and mirror conventions: −K = r(K̄) throughout; Miyazaki pairing is checked against [S06, Cor 4.3] explicitly for every route-B object.

## 4. Schedule and gates

| week | milestone | gate |
|---|---|---|
| 0–2 | environment pinned; knot data ingested and isometry-checked; [S01] audit started | |
| 2–4 | [S01] audit complete; fiber surface and monodromy of K_G computed; L⁺ verified as R-link | G0: K_G remains certified slice |
| 4–8 | WS1.1 handleslide search on L⁺; WS1.3 lemma drafted; WS2.1 battery on all route-B objects; WS3.1 battery + ribbon search on the six r = 0 knots | |
| 8–12 | WS1.1 derivative enumeration on the fiber; WS1.2 hand trace; WS2.2 common-upper-bound search on D_{n,m} and the Gompf–Miyazaki pair | |
| 12–16 | WS1.4 compression enumeration; WS3.2 DG r = 0 filter; WS5 Eisermann check | **G1**: board review |
| 16–32 | WS4.1 and 4.2 theory push; WS3.3 Teichner sums at 20–21 crossings with homotopy-ribbon battery on survivors | |
| 32–52 | WS4.4 Conj 6.1 attack informed by WS1.2 data; writeup of whichever theorem-grade result exists | **G2**: theory review |

Gate G1 decisions: if K_G is ribbon, promote lane 2/3 targets and continue WS4 with a different fibered target. If a route-B object survives the full battery, move it to the front and put WS2.2/2.3 on it full time. If nothing survives anywhere, the campaign's deliverable becomes the WS4 theorem program plus a published negative census.

## 5. Environment and tooling

See `TOOLING.md` (condensed from `research/04_computational_tooling.md`). Three facts from it shape the schedule: the whole DG band pipeline and HKL obstruction live inside SageMath only; rigorous unlink certification (Regina normal surfaces) is the measured bottleneck, not Floer homology; and extracting K_G's genus-5 monodromy explicitly is an inverse search, so WS1.4 and WS4.1 depend on a subproject that has no push-button tool. The target knot's data card is already in `data/knots/18nh00000601.json`, reproduced twice this session.

## 6. Kill conditions for the whole campaign

- A ribbon disk for K_G **and** for all six r = 0 knots **and** every route-B object killed by an invariant: no live object remains; the campaign becomes WS4 only, and it should say so publicly.
- Proof of Abe–Tange Conjecture 6.1: lanes 1, 2, 3 and all annulus-twist lanes close; only Teichner-lemma outputs (WS3.3) and route B remain.
- Proof that every ribbon disk of a fibered knot is fibered, followed by an exact unlink derivative among the [S09] compressions of K_G: K_G is ribbon, and the same machine decides every fibered candidate.

## 7. What would constitute success

1. A knot K, a certificate of smooth sliceness in standard B⁴ that a referee can check, and a non-ribbon proof resting on a theorem, not a search.
2. Short of that: the WS1.3 lemma, a resolution of WS4.1, or a disproof of Conj 6.1, each of which is publishable and changes the field's map.
3. Short of that: a public, reproducible negative census (K_G's derivative orbits, the six r = 0 knots, the route-B battery) so the next team starts here instead of at Session 0.
