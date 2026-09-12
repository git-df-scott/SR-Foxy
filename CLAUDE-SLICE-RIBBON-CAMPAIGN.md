# Claude — Slice–Ribbon counterexample campaign: what happened

Master record. Everything the campaign did, found, got wrong, and left open.
Repository state: one branch, merged to `main`. 2026-09-11 to 2026-09-12.

---

## 0. The headline

**No counterexample was found.** No knot in this repository is one, and none is
close to one.

What the campaign produced instead: two obstruction families closed permanently with
proofs, a forty-year-old untested candidate family tested and closed, a structural
explanation for why every existing candidate is immune to every existing tool, three
live route-B candidates with the cheap invariants exhausted on all of them, ten
corrections to the inherited record, and reusable machinery for the step that had
blocked the problem twice.

**The Conjecture** (Fox 1962, Kirby Problem 1.33): every smoothly slice knot in S³ is
ribbon. A counterexample is an explicit knot with (a) a proof it bounds a smooth disk
in the **standard** B⁴, and (b) a proof it bounds no ribbon disk.

    ribbon ⇒ handle-ribbon ⇒ homotopy-ribbon ⇒ slice

No converse is known. Miller–Zupan state none of the inclusions is known to be strict.

---

## 1. The structural diagnosis (the campaign's main idea)

Every route-A generator — 0-surgery/RBG trace embeddings, GST band sums, annulus
twists, belt spheres of no-3-handle B⁴ diagrams — builds its candidate's slice disk
out of the exterior of a **ribbon** disk of a partner knot. So every candidate comes
out **handle-ribbon by construction**, hence homotopy-ribbon. And every classical
obstruction (Casson–Gordon extension, metabelian and twisted-Alexander restrictions,
the irregular-dihedral Ξ invariant, Park–Powell, Turaev's Theorem H) is an obstruction
to *homotopy*-ribbonness. They are logically inert against exactly the knots we care
about.

That is not bad luck. It is the architecture of the constructions, and it means
**improving the obstructions cannot help**. The escape is the Teichner sum, whose
disk runs a ribbon disk *backwards* inside a concordance and so carries local maxima
and needs 3-handles: its output is not automatically handle-ribbon.

**A tempting shortcut, and why it fails** (recorded because it looks right): one might
argue K → K#R is a ribbon concordance and K#R is ribbon, so compose and conclude K is
ribbon — which would prove the whole conjecture. It gives K ≤ K#R and U ≤ K#R, both
*below* K#R in Gordon's order, which says nothing about U ≤ K.

---

## 2. Theorems proved here

Written out in `research/06_theory_derivatives_on_fiber.md` and
`research/07_two_lattice_lemma.md`. Not refereed.

**T1 — Surface slides preserve derivatives.** Sliding one derivative component over
another along an arc *in the Seifert surface* yields another derivative with the same
0-surgery; the framing works because a derivative has lk(Lᵢ,Lⱼ) = lk(Lᵢ,Lⱼ⁺) = 0 for
i ≠ j. The slide orbit is exactly the set of complete meridian systems of the
associated handlebody. So surface slides preserve unlinkedness while arbitrary S³
slides do not — **that difference is Generalized Property R**.

**T2 + T3 — For a fibered knot, {metabolizers of the Seifert form} = {monodromy-
invariant Lagrangians}.** Forward uses Vᵀφ = V, symmetry of v on a Lagrangian, and
det(φ − I) = ±Δ_K(1) = ±1. The converse (new here) uses unimodularity: dim M^⊥ = g and
M ⊆ M^⊥ force M^⊥ = M, then v(φy,x) = v(x,y) = 0 puts φy in M^⊥ = M.

**T4 — Two-lattice lemma for 18nh00000601.** Its Alexander polynomial factors as f·f*
with f = t⁵ − t² + 2t − 1 irreducible and f ≠ ±f*, so every derivative on its fiber —
unlink or R-link — has homology span equal to one of exactly **two** explicit rank-5
lattices. An exact linear-algebra filter for any enumeration of cut systems.

**T5 — All Milnor invariants of every R-link vanish.** The meridian map F_n → π₁(S³∖L)
induces isomorphisms on all nilpotent quotients, so every longitude lies in every term
of the lower central series. **Every R-link is a homology boundary link.**
*Corollary:* no nilpotent or lower-central-series invariant of derivative links,
**Park–Powell's triple-linking obstruction included**, can separate ribbon from
handle-ribbon. Separation requires non-nilpotent data: freeness of the link group,
volume, Heegaard genus, or finite-group representation counts.

**T6 — The gap, exactly.** K is ribbon ⟺ some derivative has free link group ⟺ some
derivative has handlebody exterior. K is handle-ribbon ⟺ some derivative is an R-link.
There is **no intermediate derivative-level condition**; the whole gap is Generalized
Property R.

---

## 3. Lanes: what closed, what lives

| lane | object | slice in std B⁴ | non-ribbon | verdict |
|---|---|---|---|---|
| 1 | 18nh00000601 | **proved** (Oliveira-Smith Cor 1.1.1); fibered genus 5, handle-ribbon | open | live but **search-inert** |
| 2 | r = 0 RBG pairs | one ribbon disk certifies both | open | live; **two** distinct pairs, not three |
| 3 | GST Figure 2 band sum | proved (GST §8) | open | live; has a 1-band survivor |
| 4 | Miyazaki cable (10_17)_{2,1} | open | **proved** | live; Casson–Gordon found nothing |
| 5 | Abe–Tagami D_{n,m} | open | **proved** | **strongest**; whole battery exhausted |
| 6 | Gompf–Miyazaki Prop 3.1 | open | proved | weak, unchecked |
| 7 | **Hom–Park Cor 1.3** | open | **proved** | **live, built here** |
| — | **Turaev Theorem I** | — | proved not homotopy-ribbon | **CLOSED, tested here** |
| — | Turaev Theorem H as a weapon | — | — | **CLOSED, proof** |
| — | all nilpotent obstructions | — | — | **CLOSED, proof (T5)** |

---

## 4. The Turaev Theorem I lane, opened and closed

Turaev (Math. USSR-Sb. 44(3) 1983) Theorem I gives genus-3 knots that are
algebraically slice and, via Theorem H(ii) whose §7.4 proof uses only π₁-surjectivity,
**provably not homotopy-ribbon**. Theorem J says the obstruction gives nothing about
sliceness, so it does not rule them out. The paper is essentially uncited; nobody had
ever built them. Any member that is smoothly slice would be a counterexample
separating slice from homotopy-ribbon.

**Seifert matrix recovered** from page 341 and verified independently in sympy: the
alternating part is symplectic with determinant 1, Fox–Milnor holds identically, the
form vanishes on two complementary spans (algebraically slice, hyperbolic form), the
determinant (2q−1)² is always a square, and across a 29-row grid all Levine–Tristram
signatures vanish at every prime-power root of unity up to order 32.

**Built** as a disk with six untwisted bands, with Milnor's ribbon-linking move
(Figure 4) implemented as a commutator of meridians. **Two internal checks validated
it**: the Milnor triple invariants come out 0 for unloaded members and the requested
value for loaded ones, and all four unloaded members are **certified ribbon** with
one-band certificates — exactly right, since Theorem I obstructs only when both
parameters are nonzero.

**Every loaded member dies to Casson–Gordon.** Final tally: **12 dead, 4 timeout, 4
ribbon controls, 0 live.** Certificates: (1,1,·,·)→(3,13), (2,1,·,·)→(5,11),
(1,2,1,1)→(3,19), (1,3,·,·)→(7,2), (5,1,1,1)→(4,13), (7,1,1,1)→(7,2). The sharpest
test: the member with **double** the Milnor data dies by the **identical** character.
So **r and s never matter** — Casson–Gordon is blind to exactly the data Turaev's
obstruction is built from, and kills these knots for an unrelated reason.

**Residual doubt, honestly placed:** Turaev's surface is defined only up to
realization freedom. Other embeddings with the same data are different knots, covered
by the same theorem, untested. We killed our realizations, not the theorem's family.

---

## 5. Every experimental result

**Calibration (what makes the negatives meaningful).** The Dunfield–Gong band search
rediscovered the known ribbon disk of K_B, the 31-crossing 0-friend, **on the first
diagram in 0.9 seconds**, certificate verified.

**18nh00000601.** 104 shaken diagrams at 2 and 3 bands, ~2.2 CPU-hours, **zero
survivors**. The filter breakdown explains why: of 2161 one-band results, 1704 fail
linking number, 387 signature, 68 Fox–Milnor, and the only 2 survivors are trivial
bands. **The one-band stage kills everything, so no multi-band search can start.**
Its Floer **torsion order is 1** (the complex is δ-thin, all arrows exponent 1), so
the Juhász–Miller–Zemke bound gives no reason to expect a deep ribbon disk — removing
the campaign's own best explanation for the failures.

**Casson–Gordon, everything tested.**

| knot | result | meaning |
|---|---|---|
| Turaev A(1,1,1,1) | **(3,13)** | not topologically slice, dead |
| ...and 11 more loaded Turaev members | all fired | dead |
| D_{0,1} = K_0 # (−K_1) | **None** (0.8s) | survives |
| D_{0,2} = K_0 # (−K_2) | **None** (0.8s) | survives |
| (10_17)_{2,1} | **None** | survives |
| Hom–Park P (corrected) | **None** at specs 3, 5, 7, 11 | survives |

**Abe–Tagami separation test.** Levine–Tristram signatures — genuine concordance
invariants — are **identical and identically zero** across K_0, K_1, K_2 at nine roots
of unity. τ, ε, ν, signature and branched-cover homology also agree across the family.
No cheap invariant separates any pair. That is measured, not assumed, and it is why
the lane has stayed open since 2015.

**Filter diagnostic that redirected compute.** At one band: 18nh00000601 gives 2161
results, 2 survivors, both trivial. D_{0,1} # 6_1 gives 9427 results, **33 survivors**.
A real structural difference between the lanes.

**Teichner search.** One pair completed: D_{0,1} # 6_1, 31 crossings, 2 bands, **4.2
hours, no certificate**. At that rate the intended sweep is ~75 hours single-core. The
search was **sampled, not run**. The trefoil control produced no false certificate
across eight partners.

**Hom–Park knot, built here.** 88 crossings, signature 0, τ = 0. Every cabled piece
matches the Hedden–Hom formula exactly (τ = 2, 3, 5, 4 as predicted). Survives
Casson–Gordon to prime 11. **Third live route-B candidate**, and its non-ribbon
certificate comes from Hom–Park's γ₀-sharp pairing theorem rather than Miyazaki's, so
it and the Abe–Tagami lane cannot die to the same cause.

---

## 6. Corrections to the inherited record

| # | correction |
|---|---|
| E1 | Turaev's Theorem H is proved via π₁-surjectivity and his own Theorem J says it yields no sliceness obstruction — it cannot touch a handle-ribbon knot. Refined later: Theorem **I** is a *target*, not a weapon. |
| E2 | Agol–Ren do **not** state "every ribbon disk of a fibered knot is fibered"; that is Meier–Zupan's question. |
| E3 | arXiv:2310.17564 is **Meier**–Zupan, not Miller–Zupan. |
| E4 | Agol–Ren Thm 1.7 and Miller–Zupan Thm 1.4 are both **Casson–Gordon** restated. |
| E5 | Oliveira-Smith has a separate Cor 1.1.2 and closing Questions 3.3, 3.4; never claims non-ribbonness. |
| E6 | "554 suspicious knots" is our arithmetic; the paper prints 513 + 41. |
| E7 | Dunfield–Gong code is on **Harvard Dataverse**, not GitHub. |
| E8 | Three sources were mischaracterized as ribbon-relevant; none bears on ribbon-vs-slice. |
| E9 | Three Dunfield–Gong knots are *expected non-slice*, not slice-ribbon candidates. |
| E10 | The machine-learning ribbon search **failed on provably ribbon links** and killed zero GST members, so its failures carry no weight. |
| **new** | **Gukov et al.'s three r = 0 RBG pairs are only two** — identical isometry signatures on both sides — and the duplicated pair is **inside** Dunfield–Gong's census, already searched far harder than we can. |

**Claims retired:** "everyone expects slice-ribbon to be false" (unsupported; the
"probably false" in the literature is about Generalized Property R); "slice-ribbon is
known false for links" (no source); "one stabilization makes a slice disk ribbon" (no
such theorem); "search failure is evidence" (calibrated: it is not).

---

## 7. My own errors, corrected in place

Left visible in the files rather than edited away.

1. **"The q = 1 subfamily is immune to Casson–Gordon."** Wrong. Determinant 1 rules
   out only the Σ₂ flavour; the obstruction fired on the **3-fold** cover, and that
   member has q = 1.
2. **"Computability has a crossing-number cutoff."** Wrong, and I repeated it as a
   finding. Three later kills at 194, 202 and 226 crossings falsified it; outcomes
   interleave with size. The real variable is how deep the certifying character sits
   in the search.
3. **"The certificate depends only on (p,q)."** Too strong. At q = 1 the values run
   3, 5, 4, 7 with no pattern the data explains. Weakened to the negative statement
   the data supports.
4. **Handedness in the Hom–Park build.** The first build cabled the *mirrors*, since
   SnapPy's census trefoil is left-handed. Caught by ε = −1 on every piece. Since
   mirror(K)_{p,q} = mirror(K_{p,−q}), the result was neither the knot nor its mirror.
   The global τ still summed to zero, which is why a weaker check would have passed
   it. Rebuilt from explicit braids.
5. **The concordance search ran in a direction the tool cannot generate.** Spherogram
   produces only *splitting* bands, so the fusing band the search needed is never
   made. Diagnosed, not silently tolerated.

---

## 8. Code

| file | what it does |
|---|---|
| `scripts/band_search.py` | Dunfield–Gong band search with an explicit parameter box; records coverage, never "evidence" |
| `scripts/band_search_shaken.py` | the same over many perturbed diagrams; checkpoints per diagram |
| `scripts/hkl_obstruction.py` | Herald–Kirk–Livingston Casson–Gordon test; non-None proves not topologically slice |
| `scripts/torsion_order.py` | U-torsion order of HFK⁻ from the UV=0 complex; the Juhász–Miller–Zemke fusion bound |
| `scripts/concordance_search.py` | common-successor search; the one search whose success is a proof (blocked, see §9) |
| `scripts/teichner_certify.py` | Teichner certificates K # J; partner list restricted to **non-fibered** ribbon knots, since Miyazaki's pairing theorem makes fibered partners provably futile |
| `scripts/cable.py` | Seifert-framed cabling; triple-calibrated (genus, an independent rebuild, the Hedden–Hom τ formula) |
| `scripts/audit_all.py` | re-verifies every knot card from its PD code alone |
| `tools/surface_engine/` | **realizes an arbitrary Seifert matrix as a verified knot diagram** and implements Milnor's ribbon-linking move; self-tests pass from a clean interpreter |

A spherogram robustness bug was found and patched conservatively: the slice filter's
signature routine raises on split intermediate links, which connected sums hit where
single knots do not.

**Environment:** SnapPy 3.3.2 + Regina 7.4 inside SageMath via
`pip install --ignore-installed packaging passagemath-standard`. The band search, the
Casson–Gordon test, Seifert matrices and signatures are all `@sage_method` and
unavailable in bare CPython.

---

## 9. What each remaining lane needs

- **Abe–Tagami (strongest).** A **fusing-band generator**. Spherogram makes only
  splitting bands. Note the difficulty honestly: a certificate is equivalent to
  proving [K_n] = [K_m], so the search is for a certificate *of* the open problem, not
  a way around it.
- **Hom–Park.** The four-term cable relation to vanish in concordance — the published
  dichotomy at its smallest parameters.
- **18nh00000601.** The fiber and monodromy explicitly, then the T4 two-lattice filter
  over cut systems. A research subproject, not a script.
- **GST.** Abe–Tange Conjecture 6.1. Proving it closes the lane; **disproving it is a
  counterexample by construction**, since sliceness in the standard B⁴ comes free.
- **The highest-leverage theorem:** is every ribbon disk of a fibered knot fibered?
  (Meier–Zupan). It is the only route that makes the "every derivative on every
  Seifert surface" quantifier finite, and it is decisive either way.

---

## 10. Discipline the record keeps

- Search results are **coverage statements** with their exact parameter box. "Evidence"
  is never used for search failure.
- Positive results are certificates, verified independently.
- A timeout is **never** a survivor. No PD code is reported without verification; two
  extraction attempts stopped rather than guess, which was correct.
- Preprint theorems are cited as theorems *in that version*. The flagship's sliceness
  rests on one unrefereed 2026 preprint, and every dependent deliverable says so.

## 11. Complete file index

Every tracked file, so nothing in the repository is unlisted. 102 tracked files.

### Top-level records

| file | what it is |
|---|---|
| `CLAUDE-SLICE-RIBBON-CAMPAIGN.md` | this file — the master record |
| `FABLE-LOG-1.md` | the earlier master log, with all code inlined verbatim and a sessions 2–3 addendum |
| `CAMPAIGN_PLAN.md` | the original plan: lanes, workstreams, kill criteria |
| `SESSION0_BATTLEFIELD.md` | the eight "doors" framing, written before the audit; door 4 later closed by E1 |
| `CANDIDATE_LEDGER.md` | every candidate with its certificate and its missing half; the binding definition of CE |
| `OBSTRUCTION_MATRIX.md` | obstruction × candidate, with `HYPOTHESES FAIL` where the tool cannot apply |
| `SOURCES.md` | the 29 load-bearing sources, each re-fetched and read at theorem level |
| `ERRATA_2026-09-11.md` | corrections E1–E10; binding over every other file where they disagree |
| `STRATEGY_2026-09-11.md` | the post-audit strategy, where Turaev Theorem I became a target |
| `NEW_WEAPONS_2023_2026.md` | recent tools assessed for ribbon-specificity |
| `ABANDONED_WEAPONS_2010_2026.md` | tools tried in the literature and why they stalled |
| `ABE_TAGAMI_AUDIT.md` | the Abe–Tagami lane read at theorem level |
| `GST_AUDIT.md` | the GST lane read at theorem level |
| `PROGRESS.md` | session-2 progress report |
| `TOOLING.md` | the computational plan and its unmet item 6 (explicit fiber and monodromy) |
| `MANIFEST.md` | file manifest from session 1 |
| `.gitignore` | `__pycache__/`, `*.pyc` |

### `research/` — agent reports and proofs

| file | what it is |
|---|---|
| `01_source_verification.md` | every source checked against its actual text |
| `02_ribbon_only_obstructions.md` | the search for a genuinely ribbon-specific obstruction |
| `03_candidate_families.md` | candidate families with their certificates |
| `04_computational_tooling.md` | what software can actually decide |
| `05_adversarial_memo.md` | the case that the conjecture is true, argued seriously |
| `06_theory_derivatives_on_fiber.md` | T1, T2, T5, T6 — derivatives, surface slides, Milnor vanishing, the Generalized Property R identification |
| `07_two_lattice_lemma.md` | T3 (Lemma A) and T4 (Lemma B) — metabolizers are monodromy-invariant; two explicit lattices for 18nh00000601 |
| `08_turaev_theorem_I.md` | Theorem I read out of the Russian original; the construction that opened the lane |
| `09_turaev_grid.md` | the (p,q,r,s) grid and what each member is |

### `scripts/` — all executable code

`band_search.py`, `band_search_shaken.py`, `hkl_obstruction.py`, `torsion_order.py`,
`concordance_search.py`, `teichner_certify.py`, `cable.py`, `audit_all.py`,
`run_queue.sh` — described in §8.

### `tools/surface_engine/` — the Seifert-matrix realizer

`bands.py` (band/plat construction), `build.py` (matrix → verified diagram),
`milnor.py` (Milnor's ribbon-linking move), `README.md`, `PROVENANCE.md`.

### `data/knots/` — verified knot cards

Each card carries a PD code and the invariants that verify it; `scripts/audit_all.py`
re-derives every invariant from the PD code alone.

| group | files |
|---|---|
| route A, lane 1 | `18nh00000601.json`, `18nh00000601_seifert.json`, `K_B_0friend.json` |
| RBG pairs | ten `MP_KG_*.json` / `MP_KB_*.json`, one per side of each of the five Gukov-et-al tuples, plus `EXTRACTION_SUMMARY.md` |
| Abe–Tagami | `AbeTagami_K_0_K_-1__6_3.json`, `AbeTagami_K_1..K_3.json`, `AbeTagami_D_0_1/0_2/1_2.json`, `AbeTagami_L_63_c1_c2.json` (the 3-component link all K_n are filled from), `AbeTagami_recovered_raw/simp.json`, `AbeTagami_CONSTRUCTION.md`, `AbeTagami_K_n_NOTES.json` |
| Miyazaki | `10_17_2_1-cable.json` |
| Hom–Park | `HomPark_P.json` (the handedness-bugged first build, kept), `HomPark_P_corrected.json` |
| GST | `GST_knot.json`, `GST_B31_regina.json` |
| Turaev | five `Turaev_A_*.json` members of the grid |
| control | `CONTROL_3_1.json` — the trefoil, which must never get a certificate |

`data/turaev/`: `seifert_matrix.json` (the matrix from p. 341, verified in sympy),
`grid.json` (the parameter grid).

### `results/` — every recorded outcome

| file | outcome |
|---|---|
| `KB_calibration_shaken20_bands2.json` | **the calibration**: ribbon disk of K_B found on diagram 1 in 0.9 s, `unknot: True` |
| `KG_bands2_tw2_len6.json` | 2161 one-band results, 2 trivial survivors |
| `KG_bands2_tw3_len10.json` | wider box, 0 survivors |
| `KG_shaken30_bands3_tw2_len7_detached.json` | 30 diagrams, 3 bands, all `unknot: False` |
| `KG_shaken40_bands2_tw2_len8.json` | 14 diagrams completed, all `unknot: False` |
| `KG_shaken60_bands2_tw2_len8_detached.json` | 60 diagrams, all `unknot: False` |
| `KG_derivative_extraction.md` | why the R-link derivative is not in the literature — Oliveira-Smith never draws it |
| `HKL_turaev_1111_verify.json` | **(3,13)** — the kill that closed the Turaev lane |
| `HKL_AbeTagami_D_0_1.json`, `HKL_AbeTagami_D_0_2.json` | `None` in 0.8 s — both survive |
| `HKL_10_17_cable.json` | `None` — the Miyazaki cable survives |
| `HKL_HomPark_corrected.json` | `None` at specs 3, 5, 7, 11 — survives |
| `GST_bands1_tw2_len8_detached.json` | GST Figure 2 band search, no survivors |
| `teichner_AT_b2len5_detached.json` | D_{0,1} # 6_1, 2 bands, 4.2 h, no certificate |
| `teichner_r0_detached.json` | Teichner sweep over the r = 0 knots |
| `AT_conc_test.json`, `AT_concordance_smoke.json` | the concordance search and its smoke test — the runs that exposed the direction bug |
| `invariant_cards_MP_cable.json` | τ, ε, ν, signature across the RBG knots and the cable; all zero |
| `abe_tagami_lane.md` | the lane written up with its certificate chain |
| `abe_tagami_survives.md` | the Levine–Tristram separation test at nine roots of unity |
| `concordance_search_diagnosis.md` | spherogram generates only splitting bands; the fusing band is never made |
| `hompark_build.md` | the build, the handedness error, and the Hedden–Hom τ checks |
| `turaev_family_status.md` | 12 dead, 4 timeout, 4 ribbon controls, 0 live |
| `torsion_and_rbg_findings.md` | torsion order 1 for K_G; the RBG duplicate pair |
| `strikes_2026-09-12.md` | the session-3 strikes |
| `AUDIT_2026-09-12.md` | the manual audit that stopped stale tasks |
| `logs/` | 18 raw run logs, one per detached job, kept so every number above is traceable to a transcript |

---

## 12. Reproducing any of it

```sh
# environment: SnapPy 3.3.2 + Regina 7.4 inside SageMath
pip install --ignore-installed packaging passagemath-standard

# Seifert-matrix realizer self-tests: 20 members, "ALL CHECKS PASSED", exits nonzero on
# failure. Bare CPython is enough. Must run from its own directory (flat imports).
cd tools/surface_engine && python build.py

# re-verify every knot card from its PD code alone
sage -python scripts/audit_all.py

# Casson-Gordon on one card; writes the result as JSON. Sage-only
sage -python scripts/hkl_obstruction.py data/knots/<card>.json results/<out>.json
```

The `@sage_method` routines — `ribbon_concordant_links`, `slice_obstruction_HKL`,
`seifert_matrix`, `signature`, `hyperbolic_torsion` — do not exist in bare CPython.
Anything that calls them must run under `sage -python`.
