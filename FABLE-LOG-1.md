# FABLE-LOG-1

Complete log of the Slice–Ribbon counterexample campaign through 2026-09-12.
Self-contained: every result, every line of code, and the exact next steps.
Single branch: `claude/slice-ribbon-counterexample-dva3g0` (verified: `main` is an ancestor of `HEAD`; no other branch carries work).

---

## 0. Bottom line

**No counterexample.** Nothing in this log is one, and nothing here is close to one.

Two things are now settled that were not settled before:

1. **No existing invariant can prove a counterexample.** Every obstruction ever labelled "ribbon obstruction" is now known to obstruct only at the homotopy-ribbon or handle-ribbon level. Both certified-slice candidates are already *proved* handle-ribbon, so the entire classical battery is logically inert against them. A counterexample proof requires a new theorem. This is not a research mood; it is the content of §3 and §4 below.
2. **The gap is exactly Generalized Property R.** A knot is ribbon iff some derivative link has free link group; handle-ribbon iff some derivative is an R-link. There is no intermediate condition. So "prove K_G is not ribbon" = "prove Generalized Property R fails for every derivative of K_G, on every Seifert surface".

Calibrated estimate carried forward from the adversarial memo: roughly even odds a counterexample exists, roughly 5% that one is *provable* by 2028 with current tools. The likeliest near-term headline remains "18nh00000601 is ribbon".

---

## 1. What a counterexample is

**Conjecture (Fox 1962, Kirby Problem 1.33).** Every smoothly slice knot in S³ is ribbon.

| term | definition | how you certify it |
|---|---|---|
| smoothly slice | bounds a smooth disk in the **standard** B⁴ | explicit disk, or trace embedding / handle calculus that names standard B⁴ |
| ribbon | slice disk with no local maxima of the radial function; equivalently a band-move movie to an unlink | a band movie; or an unlink derivative on some Seifert surface |
| handle-ribbon | disk in a homotopy 4-ball whose exterior has no 3-handles | an R-link derivative |
| homotopy-ribbon | disk with π₁(S³∖K) ↠ π₁(B⁴∖D) | for fibered knots: monodromy extends over a handlebody |

ribbon ⇒ handle-ribbon ⇒ homotopy-ribbon ⇒ slice. No converse known; Miller–Zupan state none of the inclusions is known to be strict.

**A counterexample (CE)** = an explicit knot K with (a) a proof it is smoothly slice in standard B⁴, and (b) a proof it bounds no ribbon disk.

- **Route A**: certified slice, prove non-ribbon.
- **Route B**: certified non-ribbon, prove slice (usually via a smooth concordance).

**The structural trap.** Every known generator of route-A candidates (0-surgery / RBG trace embeddings, GST band sums, annulus twists, belt spheres of no-3-handle B⁴ diagrams) produces knots whose slice-disk exterior is built from a *ribbon* disk exterior of a partner knot, hence handle-ribbon by construction. The one exception is the Teichner-lemma sum K # J, whose output is not automatically handle-ribbon.

---

## 2. Board state

| lane | object | slice in std B⁴ | non-ribbon | route | verdict |
|---|---|---|---|---|---|
| 1 | `18nh00000601` = K_G | **proved** (Oliveira-Smith Cor 1.1.1), fibered genus 5, handle-ribbon (Thm 1.2) | open | A | **primary** |
| 2 | r = 0 RBG pairs: **two** distinct pairs, four knots (GHMR's three include a duplicate) | one ribbon disk on either side certifies both | open | A-generator | **live**; the 19-crossing pair is inside DG's census, the 27/24 pair is not |
| 3 | GST Figure 2 band sum | proved (GST §8) | open; Abe–Tange Conj 6.1 predicts ribbon | A | live, secondary |
| 4 | Miyazaki cables, smallest live member (10_17)_{2,1} | open; strongly rationally slice | **proved** (Miyazaki) | B | live |
| 5 | Abe–Tagami D_{n,m} = A_n(6_3) # −A_m(6_3) | open; slice iff [K_n] = [K_m] | **proved** | B | live |
| 6 | Gompf–Miyazaki Prop 3.1 pair | open | proved | B | weak |
| 7 | Hom–Park P(K,J,p,q₁,q₂) | open; algebraically slice | proved | B | weak |
| dead | Turaev π³ door; all 4_1 cables; DG's 553; Abe–Tange 8_20 family; MP's 5 topologically slice knots | | | | closed |

---

## 3. Corrections to the prior package (2026-09-11 audit)

Every load-bearing source was re-fetched and read at theorem level. All eleven arXiv sources exist as claimed. What changed:

| # | correction | consequence |
|---|---|---|
| E1 | **Turaev's Theorem H recovered in full** (mathnet.ru, Math. USSR-Sb. 44(3) 1983). H(ii) is proved in §7.4 using only π₁-surjectivity of the disk inclusion. Turaev's own **Theorem J** says Theorem H yields no new sliceness obstruction. | **Door 4 closed.** Cannot obstruct ribbonness of any handle-ribbon knot. |
| E2 | Agol–Ren say nothing about ribbon (as opposed to strongly homotopy-ribbon) disks; the string "handle-ribbon" never appears; they do not state "every ribbon disk of a fibered knot is fibered". | The completeness lemma the plan needs is real and open, but it is **Meier–Zupan's** question, not theirs. |
| E3 | arXiv:2310.17564 is **Meier**–Zupan, not Miller–Zupan. | attribution |
| E4 | Agol–Ren Thm 1.7 and Miller–Zupan Thm 1.4 are both printed "([CG83])" — Casson–Gordon. Miller–Zupan's own generalization is Thm 1.5; Agol–Ren's finiteness is Thm 1.6. | attribution |
| E5 | Oliveira-Smith has a separate **Cor 1.1.2** ("potential counterexample") and closing **Questions 3.3, 3.4**. Never claims non-ribbonness. | cite correctly |
| E6 | "554 suspicious knots" is our arithmetic; DG print 513 + 41. | wording |
| E7 | DG code is on **Harvard Dataverse** (doi:10.7910/DVN/YBDTBT, 1.02 GB), not GitHub; parts ship in SnapPy 3.3. | tooling |
| E8 | S11 is an unknotting-number paper; S12 is real link Floer homology; S13 is a surface-in-B⁴ obstruction. None bears on ribbon-vs-slice. | demote |
| E9 | DG Thm 1.12's other three knots are *expected non-slice*; they are SPC4 candidates, not SR candidates. | do not ledger |
| E10 | The Gukov et al. ML search **failed on the provably ribbon** L_{1,1} and L_{2,1} and killed zero GST members. | search failure has no evidential weight |

**Candidate lanes the prior package missed**, now added: Miyazaki cables of fibered negative amphicheiral knots (free non-ribbon certificate; smallest live member (10_17)_{2,1}); the three r = 0 RBG pairs; Gompf–Miyazaki 1995 Prop 3.1.

**Claims retired:** "everyone expects slice-ribbon to be false" (no source supports it; GST's "probably false" is about Generalized Property R); "slice-ribbon is known false for links" (no source); "one stabilization makes a slice disk ribbon" (no such theorem; stabilization distance can be arbitrarily large); "search failure is evidence" (calibrated: it is not).

---

## 4. Theorems proved in this campaign

Written out in `research/06_theory_derivatives_on_fiber.md` and `research/07_two_lattice_lemma.md`. Not yet refereed.

**T1 (surface slides).** Sliding one derivative component over another along an arc *in the Seifert surface* yields another derivative with the same 0-surgery. The framing check works because a derivative has lk(L_i, L_j) = lk(L_i, L_j⁺) = 0 for i ≠ j. The surface-slide orbit of a derivative is exactly the set of complete meridian systems of the handlebody it determines — so surface slides preserve unlinkedness, while arbitrary S³ slides do not. *That difference is Generalized Property R.*

**T2 (monodromy-invariant Lagrangians).** For a fibered knot, every monodromy-invariant Lagrangian of the intersection form is a metabolizer of the Seifert form. Proof uses V ᵀφ = V, symmetry of v on a Lagrangian, and det(φ − I) = ±Δ_K(1) = ±1.

**T3 (converse, new here).** For a fibered knot, every metabolizer of the Seifert form is monodromy-invariant. Proof: unimodularity gives dim M^⊥ = g and M ⊆ M^⊥, so M^⊥ = M; then v(φy, x) = v(x, y) = 0 puts φy in M^⊥ = M.

T2 + T3: **for a fibered knot, {metabolizers of V} = {φ-invariant Lagrangians}.**

**T4 (two-lattice lemma for K_G).** Δ_{K_G} = f·f\* with f = t⁵ − t² + 2t − 1 irreducible over Q and f ≠ ±f\*. Hence H₁(F;Q) has exactly two φ-invariant 5-dimensional subspaces, and **every derivative of K_G on its fiber — unlink or R-link — has homology span equal to one of two explicit rank-5 lattices.** An exact linear-algebra filter for any future enumeration of cut systems on the fiber.

**T5 (Milnor invariants of R-links vanish).** For any R-link L, the map F_n → π₁(S³∖L) sending meridians to meridians induces isomorphisms on all nilpotent quotients, so every longitude lies in every term of the lower central series, so **all μ̄ invariants of every R-link vanish**. Every R-link is a homology boundary link.
*Corollary:* no nilpotent / lower-central-series invariant of derivative links — Park–Powell's triple-linking obstruction included — can separate ribbon from handle-ribbon. **Another door closed permanently.** Separation requires non-nilpotent data: freeness of the link group itself, volume of the derivative exterior, Heegaard genus, or finite-group representation counts.

**T6 (the gap, exactly).** K ribbon ⟺ some derivative has free link group ⟺ some derivative has handlebody exterior. K handle-ribbon ⟺ some derivative is an R-link. **There is no intermediate derivative-level condition.** For K_G: ribbon ⟸ Generalized Property R for the 5-component R-link on the fiber. K_G is the exact analogue of the GST situation with n = 5 instead of n = 2.

**Flagged open (O1).** The Cochran–Davis genus count (genus of the surface produced from a ribbon disk = number of ribbon singularities) could not be verified from their one-line proof. The alternatives "= #bands" and "= #minima/2" were killed by the square knot. T4's application to *genus-5* ribbon disks depends on this.

---

## 5. Experimental results

### 5.1 Environment

Sage-backed SnapPy via `pip install --ignore-installed packaging passagemath-standard`; `snappy.sage_helper._within_sage` is True. That unlocks the Dunfield–Gong band search, the HKL Casson–Gordon obstruction, Seifert matrices and signatures. Regina 7.4 alongside. 4 cores, 15 GB.

### 5.2 Calibration (this is what makes the negatives meaningful)

The band search **rediscovered the known ribbon disk of K_B** — the 31-crossing 0-friend of K_G — on the first diagram in **0.9 seconds**, certificate verified by `verify_ribbon_to_unknot`. The same pipeline, same box, finds nothing on K_G.

### 5.3 K_G = 18nh00000601

| experiment | box | result |
|---|---|---|
| single diagram | 2 bands, twists ≤ 2, length ≤ 6 | 0 survivors |
| single diagram | 2 bands, twists ≤ 3, length ≤ 10 | 0 survivors |
| shaken diagrams | 2 bands, twists ≤ 2, length ≤ 8 | **74 diagrams**, 0 survivors |
| shaken diagrams | 3 bands, twists ≤ 2, length ≤ 7 | **30 diagrams**, 0 survivors |

Totals to date: **104 shaken diagrams, ~2.2 CPU-hours, zero survivors at every
band count tried.** In every box, the one-band stage already kills everything, so
the two- and three-band stages never get a non-trivial link to extend.

**Filter breakdown on one diagram** (2161 one-band results): 1704 fail linking number, 387 fail signature, 68 fail Fox–Milnor, **2 survive** — and both survivors are K_G itself with a split unknot capped off, i.e. trivial bands.

Reading: an intermediate link in a ribbon movie must itself be a ribbon link, so it must pass linking number, signature and Fox–Milnor. **No non-trivial first band of a ribbon disk for K_G exists inside these boxes.** Either the first band is long, or the diagram must be far from any of these 46. This is a coverage statement, not an obstruction.

**The R-link derivative is not in the literature.** Oliveira-Smith's Theorem 1.2 gets L⁺ from a Miller–Zupan *existence* theorem applied to the two-component R-link K_G ∪ U, and never draws L⁺. Even K_G ∪ U is drawn with three unexpanded twist boxes; expanded it exceeds ~100 crossings. So the planned "handleslide search on L⁺" has no input. Detail in `results/KG_derivative_extraction.md`.

What was verified instead, from the DG Table 11 DT code `ycjkdnhQyUtMsaVweFIRCXOBgLJDkP` alone:

| check | result |
|---|---|
| RBG link | 3 components, 25 crossings, linking matrix [[0,−1,−1],[−1,0,2],[−1,2,0]] |
| component roles | all three unknotted; (0,1) and (0,2) are Hopf links ⇒ R = component 0 |
| Regina, ⟨1,0⟩ surgery on R∪B and R∪G | `isSphere()` True |
| fill R(+1), B(0) | vol 11.9345081499, 14 tets, **isometric to the K_G exterior** (slope −1 gives the wrong volume, confirming r = +1) |
| fill R(+1), G(0) | vol 11.5729287764; `exterior_to_link` gives a **31-crossing K_B**, genus 5, fibered, HFK rank 25 |
| S³₀(K_B) vs S³₀(K_G) | equal volume 8.7838564748, equal length spectra, equal cover homology to degree 4; combinatorial certificate not found |

**Seifert data (computed here):** 28×28 Seifert matrix from the braid closure, signature 0, Δ = f·f\* as in T4.

### 5.3b Floer torsion order of K_G: the JMZ fusion bound is vacuous

Juhasz-Miller-Zemke give F(J) >= Ord_U(J) for ribbon J, so a large torsion order
would prove any ribbon disk needs many bands. Computed here for the first time on
K_G from the UV=0 complex (25 generators, 28 arrows): **every generator has M = A**,
the complex is delta-thin, and all U- and V-arrows have exponent exactly 1. Hence
the V=0 differential is U*B with B over F_2, so every elementary divisor is U^1 and
**Ord_U(K_G) = 1**. The JMZ bound gives only F(K_G) >= 1.

This cuts against the campaign's own steelman. The best explanation for DG's
failure was "genus 5 suggests a 5-band disk, one past their ceiling of 4"; Floer
homology gives that no support whatever. Calibration: K_B has raw exponents [1,5]
but fusion number 1 (its certificate is a single band to the unlink), so the raw
maximum exponent is not the torsion order in general - only the all-exponents-1
case licenses the conclusion. Detail and script: `results/torsion_and_rbg_findings.md`,
`scripts/torsion_order.py`.

### 5.4 The r = 0 RBG pairs (lane 2)

All ten Manolescu–Piccirillo knots K_{B/G} for the five GHMR tuples were built **from the authors' own DT-code notebook** (`DTcodes.nb`, linked from the paper's companion page), auto-transpiled rather than hand-copied. The notebook's parameters are sign-flipped relative to the paper: paper (a,b,c,d,e,f) = notebook `KX(a,−b,−c,−d,−e,−f)`. This was pinned by reproducing the volume **and** total HFK rank of all 22 knots in the companion `PromisingKnots.txt` — **44/44 numbers exact**.

Per pair, verified: isometric 0-surgeries, non-isometric exteriors, 1 component, hyperbolic.

**Correction to the candidate list.** GHMR name three r = 0 pairs, but
K_{B/G}(0,0,0,1,2,-1) and K_{B/G}(0,0,-2,0,0,1) are the **same pair**: identical
isometry signatures on both sides, `is_isometric_to` True. Lane 2 holds **four
distinct knots, not six**. Moreover that pair simplifies to **19 crossings, prime,
hyperbolic**, so it lies inside Dunfield-Gong's census of all prime knots with at
most 19 crossings, which they already searched to 4 bands with ~100 CPU-years:
re-searching it is strictly weaker than what exists, and its survival of that
search makes it a *better* candidate than recorded. The remaining pair, at 27 and
24 crossings, lies outside DG's census and has never been through the DG band
search; the queue was redirected onto it.

| knot | crossings | genus | HFK rank | vol | Δ |
|---|---|---|---|---|---|
| KB(0,0,0,1,2,−1) | 19 | 2 | 33 | 13.824520 | **1** |
| KG(0,0,0,1,2,−1) | 19 | 2 | 33 | 13.990717 | **1** |
| KB(0,0,0,−1,2,1) | 27 | 2 | 97 | 20.495415 | **1** |
| KG(0,0,0,−1,2,1) | 26 | 2 | 97 | 20.353874 | **1** |
| KB(0,0,−2,0,0,1) | 19 | 2 | 33 | 13.824520 | **1** |
| KG(0,0,−2,0,0,1) | 19 | 2 | 33 | 13.990717 | **1** |
| KB(−2,0,0,−1,2,−1) | 31 | 2 | 113 | 18.955571 | 4t⁻²−20t⁻¹+33−20t+4t² |
| KG(−2,0,0,−1,2,−1) | 30 | 2 | 113 | 19.383723 | same |
| KB(−1,0,−1,−1,2,−1) | 25 | 2 | 81 | 18.689290 | 3t⁻²−12t⁻¹+19−12t+3t² |
| KG(−1,0,−1,−1,2,−1) | 30 | 2 | 81 | 18.920182 | same |

τ = ε = ν = signature = 0 on all ten. The three r = 0 pairs have **Alexander polynomial 1**, hence are topologically slice by Freedman, and no cheap obstruction touches them. Ribbon searches on the six r = 0 knots are queued.

### 5.5 Route B

- **(10_17)_{2,1}** built as the Seifert-framed (2,1)-cable of 10_17 (41 crossings, doubled braid + σ₁^{1−2w}, w = 0). Verified: 1 component; genus 8 = 2·g(10_17); Δ_cable(t) = Δ_{10_17}(t²) exactly; exterior non-hyperbolic as a satellite must be. τ = ε = ν = signature = 0.
  **The Herald–Kirk–Livingston Casson–Gordon obstruction returns None** over the
  (10,[0,20]),(20,[0,10]) grid after 30 minutes: no obstruction fired, so the
  smallest live Miyazaki member survives its first kill test. This is coverage, not
  a proof of sliceness — the obstruction simply did not fire in that grid.
- **Abe–Tagami K_n = A_n(6_3):** no machine-readable diagram exists in any e-print. The first extraction attempt stopped honestly rather than guess a PD code. A second attempt is running that builds the 3-component link 6_3 ∪ c'₁ ∪ c'₂ (c'₁ ∪ c'₂ a Hopf link, 6_3 their band sum) and obtains every K_n by Dehn filling, verified by shared 0-surgery and K_{−1} = K_0 = 6_3. **Rigorous side result:** all 59937 hyperbolic knots with ≤ 14 crossings were 0-filled; the only manifold isometric to the 0-surgery of 6_3 is 6_3 itself, so the K_n are not table knots.

### 5.6 GST

Regina's built-in Figure 2 knot (48 crossings) matches GST's `sliceknot.eps`. Genus 10, τ = 0, Fox–Milnor holds. **Not fibered** (top Alexander grading has rank 2), which the ledger correctly left open. Gukov et al. never ran the DG search on it; we did.

**A structural difference from K_G.** The one-band search (twists ≤ 2, length ≤ 8,
65 minutes) found **one surviving plausibly-slice link** and no unknot. K_G under
the same filter has *zero* non-trivial one-band survivors. So on GST the search can
actually be continued to a second band, and that two-band run is now going, whereas
on K_G there is nothing to extend. This is the first computational respect in which
the two flagship candidates behave differently.

---

## 6. All code

### 6.1 `scripts/band_search.py`

```python
#!/usr/bin/env python3
"""Run the Dunfield–Gong band search (shipped in SnapPy 3.3, spherogram.links.bands)
on one knot with an explicit parameter box, and record the outcome as a coverage
statement.  Requires SnapPy inside Sage (passagemath works) for the slice filter.

Usage: python3 band_search.py <knot.json> <max_bands> <max_twists> <max_band_len> <paths> <out.json>

A positive result is a certificate (checked with verify_ribbon_to_unknot).
A negative result means only: no ribbon disk inside this parameter box.
"""
import json, sys, time, datetime
import snappy
from spherogram.links.bands.search import ribbon_concordant_links, verify_ribbon_to_unknot

knot_file, max_bands, max_twists, max_band_len, paths, out = sys.argv[1:7]
max_bands, max_twists, max_band_len = int(max_bands), int(max_twists), int(max_band_len)
d = json.load(open(knot_file))
pd = d.get('pd_code_snappy_0indexed') or d['pd_code']
K = snappy.Link([tuple(c) for c in pd])
import snappy.sage_helper as sh
assert sh._within_sage, 'run inside Sage: the slice filter needs it'

t0 = time.time()
res = ribbon_concordant_links(K, max_bands=max_bands, max_twists=max_twists,
                              max_band_len=max_band_len, paths=paths,
                              filter_for_plausibly_slice=True,
                              use_ribbon_link_cache=True, certify=True,
                              print_progress=True)
elapsed = time.time() - t0
record = {
    'knot': d['name'], 'date': datetime.datetime.utcnow().isoformat() + 'Z',
    'box': {'max_bands': max_bands, 'max_twists': max_twists,
            'max_band_len': max_band_len, 'paths': paths,
            'filter_for_plausibly_slice': True, 'use_ribbon_link_cache': True},
    'seconds': round(elapsed, 1),
    'survivor_links': len([k for k in res if k != 'unknot']),
    'unknot_found': 'unknot' in res,
}
if 'unknot' in res:
    cert = res['unknot']
    record['certificate'] = [c if isinstance(c, str) else c for c in cert]
    try:
        record['certificate_verified'] = bool(verify_ribbon_to_unknot(K, cert))
    except Exception as e:
        record['certificate_verified'] = f'error: {e}'
json.dump(record, open(out, 'w'), indent=1, default=str)
print(json.dumps({k: v for k, v in record.items() if k != 'certificate'}, indent=1))
```

### 6.2 `scripts/band_search_shaken.py`

```python
#!/usr/bin/env python3
"""Band search over many randomly perturbed ("shaken") diagrams of one knot,
following the Dunfield–Gong practice of searching several diagrams because the
band moves available depend on the diagram.

Usage: python3 band_search_shaken.py <knot.json> <n_diagrams> <backtrack_steps> <max_bands> <max_twists> <max_band_len> <paths> <out.json> [seed]
"""
import json, sys, time, random, datetime
import snappy
from spherogram.links.bands.search import ribbon_concordant_links, verify_ribbon_to_unknot
import snappy.sage_helper as sh
assert sh._within_sage

knot_file, n_diag, steps, max_bands, max_twists, max_band_len, paths, out = sys.argv[1:9]
seed = int(sys.argv[9]) if len(sys.argv) > 9 else 0
n_diag, steps, max_bands, max_twists, max_band_len = map(int, (n_diag, steps, max_bands, max_twists, max_band_len))
random.seed(seed)
d = json.load(open(knot_file))
pd = d.get('pd_code_snappy_0indexed') or d['pd_code']
K0 = snappy.Link([tuple(c) for c in pd])

runs = []
t0 = time.time()
found = None
for i in range(n_diag):
    K = K0.copy()
    if i > 0:
        K.backtrack(steps)
        # partially simplify so diagrams stay small but differ
        K.simplify('basic')
    t = time.time()
    res = ribbon_concordant_links(K, max_bands=max_bands, max_twists=max_twists,
                                  max_band_len=max_band_len, paths=paths,
                                  filter_for_plausibly_slice=True,
                                  use_ribbon_link_cache=True, certify=True)
    rec = {'diagram': i, 'crossings': len(K.crossings), 'seconds': round(time.time() - t, 1),
           'survivors': len([k for k in res if k != 'unknot']), 'unknot': 'unknot' in res}
    if 'unknot' in res:
        cert = res['unknot']
        rec['certificate'] = cert
        rec['certificate_verified'] = bool(verify_ribbon_to_unknot(K, cert))
        rec['start_pd'] = K.PD_code()
        found = rec
    runs.append(rec)
    print(json.dumps({k: v for k, v in rec.items() if k not in ('certificate', 'start_pd')}), flush=True)
    json.dump({'knot': d['name'], 'date': datetime.datetime.utcnow().isoformat() + 'Z',
               'box': {'n_diagrams': n_diag, 'backtrack_steps': steps, 'max_bands': max_bands,
                       'max_twists': max_twists, 'max_band_len': max_band_len, 'paths': paths, 'seed': seed},
               'seconds': round(time.time() - t0, 1), 'runs': runs, 'unknot_found': found is not None},
              open(out, 'w'), indent=1, default=str)
    if found:
        break
print('DONE unknot_found =', found is not None)
```

### 6.3 `scripts/hkl_obstruction.py`

```python
#!/usr/bin/env python3
"""Herald-Kirk-Livingston / Casson-Gordon slice obstruction (Dunfield-Gong implementation in SnapPy 3.3, Sage only).
Usage: python3 hkl_obstruction.py <knot.json> <out.json>
A nonzero result proves the knot is not topologically slice (hence not smoothly slice)."""
import json, sys, time, snappy
import snappy.sage_helper as sh; assert sh._within_sage
d=json.load(open(sys.argv[1])); pd=d.get('pd_code_snappy_0indexed') or d['pd_code']
M=snappy.Link([tuple(c) for c in pd]).exterior()
t=time.time()
spec=[(10,[0,20]),(20,[0,10])]
try:
    res=M.slice_obstruction_HKL(spec, method='basic', verbose=False)
except Exception as e:
    res=f'error: {e}'
out={'knot':d['name'],'spec':spec,'method':'basic','result':str(res),'seconds':round(time.time()-t,1),
     'meaning':'None = no obstruction found in this spec; (p,q) = NOT topologically slice'}
json.dump(out,open(sys.argv[2],'w'),indent=1); print(out)
```

### 6.4 `scripts/run_queue.sh`

```bash
#!/bin/bash
# Sequential queue of shaken band searches on the r=0 RBG knots (both sides of each pair).
cd /home/user/SR-Foxy
for k in MP_KB_0_0_0_1_2_-1 MP_KG_0_0_0_1_2_-1 MP_KB_0_0_-2_0_0_1 MP_KG_0_0_-2_0_0_1 MP_KB_0_0_0_-1_2_1 MP_KG_0_0_0_-1_2_1; do
  python3 scripts/band_search_shaken.py data/knots/$k.json 12 25 2 2 8 shortest results/RBG_${k}_shaken12_bands2_detached.json 5 > results/logs/RBG_$k.log 2>&1
done
echo QUEUE_DONE >> results/logs/RBG_queue.log
```

### 6.5 Environment setup

```bash
pip install --ignore-installed packaging passagemath-standard   # Sage via pip; ~10 min
python3 -c "import sage.all; import snappy.sage_helper as s; print(s._within_sage)"   # must print True
# snappy 3.3.2 and regina 7.4 from pip; Python 3.11.
```

The critical constraint: `Link.ribbon_concordant_links`, `Manifold.slice_obstruction_HKL`, `Link.seifert_matrix`, `Link.signature` and `Manifold.hyperbolic_torsion` are all `@sage_method` and raise `SageNotAvailable` in bare CPython.

### 6.6 Reproduce the K_G invariant card from scratch

```python
import snappy, regina
sig = "sabcdbefghijkglmhijknopqreanopqdcrmlflRSuvwT+5bdd"   # Burton census 18n-hyp.csv row 602
L = regina.Link.fromKnotSig(sig)
K = snappy.Link([tuple(i-1 for i in c) for c in L.pdData()])
print(K.knot_floer_homology())       # genus 5, fibered True, tau=eps=nu=0, rank 25
M = K.exterior(); M.simplify()
print(M.volume(), M.num_tetrahedra(), L.alexander())   # 11.9345081499, 14
```

### 6.7 Reproduce the RBG / K_B identification

```python
import snappy
L = snappy.Link('DT:ycjkdnhQyUtMsaVweFIRCXOBgLJDkP')   # DG Table 11
M = L.exterior()
MG = M.copy(); MG.dehn_fill([(1,1),(0,1),(0,0)])       # R(+1), B(0)  -> K_G exterior
MB = M.copy(); MB.dehn_fill([(1,1),(0,0),(0,1)])       # R(+1), G(0)  -> K_B exterior
KB = MB.filled_triangulation().exterior_to_link(); KB.simplify('global')
print(len(KB.crossings), KB.knot_floer_homology())     # 31 crossings, genus 5, fibered
```

### 6.8 Reproduce the two-lattice lemma input

```python
import sympy as sp
t = sp.symbols('t')
f = t**5 - t**2 + 2*t - 1
print(sp.Poly(f, t).is_irreducible)                    # True
print(sp.expand(f * sp.expand(t**5 * f.subs(t, 1/t)))) # = -Delta_{K_G}(t)
```

### 6.9 Filter-breakdown instrumentation (how the "0 survivors" number is produced)

```python
import snappy, json, collections
from spherogram.links.bands.core import banded_links, normalize_crossing_labels
from spherogram.links.bands.search import linking_nums_all_zero
pd = json.load(open('data/knots/18nh00000601.json'))['pd_code_snappy_0indexed']
K = snappy.Link([tuple(c) for c in pd]); normalize_crossing_labels(K)
stats = collections.Counter()
for L, spec in banded_links(K, 2, 6, 'shortest'):
    stats['total'] += 1
    if not linking_nums_all_zero(L): stats['lk!=0'] += 1; continue
    L.simplify('global'); L.unlinked_unknot_components = 0
    if len(L.link_components) == 0: stats['UNLINK!'] += 1; continue
    if L.signature() != 0: stats['sig!=0'] += 1; continue
    if not L.exterior().fox_milnor_test(): stats['FM fail'] += 1; continue
    stats['survive'] += 1
print(dict(stats))   # {'total':2161,'lk!=0':1704,'sig!=0':387,'FM fail':68,'survive':2}
```

---

## 7. Repository layout (one branch, `claude/slice-ribbon-counterexample-dva3g0`)

```
FABLE-LOG-1.md              this log
CAMPAIGN_PLAN.md            six workstreams, gates, kill conditions
PROGRESS.md                 session-2 narrative report
ERRATA_2026-09-11.md        corrections E1-E10 to the Session 0 package
TOOLING.md                  environment, tool survey, first ten scripts
MANIFEST.md                 artifact index with evidence levels
SOURCES.md                  S01-S39 verification register
SESSION0_BATTLEFIELD.md     prior session, partly superseded
CANDIDATE_LEDGER.md         tiered candidates + generators
OBSTRUCTION_MATRIX.md       which obstruction can touch which object
ABE_TAGAMI_AUDIT.md  GST_AUDIT.md  NEW_WEAPONS_2023_2026.md  ABANDONED_WEAPONS_2010_2026.md
candidate_ledger.csv  obstruction_matrix.csv
research/01_source_verification.md
research/02_ribbon_only_obstructions.md
research/03_candidate_families.md
research/04_computational_tooling.md
research/05_adversarial_memo.md
research/06_theory_derivatives_on_fiber.md      T1, T2, T5, T6
research/07_two_lattice_lemma.md                T3, T4
scripts/band_search.py  band_search_shaken.py  hkl_obstruction.py  run_queue.sh
data/knots/18nh00000601.json + _seifert.json    K_G, full card
data/knots/K_B_0friend.json                     31-crossing ribbon partner
data/knots/MP_K{B,G}_*.json                     ten Manolescu-Piccirillo knots
data/knots/10_17_2_1-cable.json                 Miyazaki lane
data/knots/GST_knot.json  GST_B31_regina.json
data/knots/AbeTagami_K_0_K_-1__6_3.json  AbeTagami_K_n_NOTES.json
data/knots/EXTRACTION_SUMMARY.md
results/*.json                                  coverage records, one per box
results/KG_derivative_extraction.md             why L+ is not in the literature
```

Commit history (8 commits, all on the one branch):

```
a79c045 Add PROGRESS.md: session-2 execution report
0c7db88 Ingest verified candidate knots: 10 MP RBG knots, (10_17)_{2,1}, GST, 6_3
839c909 Add theory notes: derivatives on the fiber, R-link Milnor invariants, two-lattice lemma
750c27f Ignore in-progress detached search outputs
c8081d4 Add K_B 0-friend data card, K_G derivative extraction report, shaken search script
271e040 Add band-search script, K_G Seifert data, GST knot card, first coverage result
577f649 Add tooling audit, environment spec, and 18nh00000601 data card
4eaf551 Add slice-ribbon counterexample campaign plan and 2026-09-11 errata
```

---

## 8. Where we go next

Ordered by expected information per unit of work. Items 1–4 are running or immediately runnable; 5–7 are the theory program, and only they can actually produce a counterexample proof.

**1. Finish the r = 0 RBG ribbon searches (running).** Four distinct knots, of which only the 27/24-crossing pair is outside DG's census and worth our compute; 15 shaken diagrams each. A hit certifies the partner smoothly slice in standard B⁴ with no inherited ribbon disk — a second route-A target with Alexander polynomial 1. Cheap, decisive either way.

**2. Finish the Abe–Tagami construction (running).** Build 6_3 ∪ c'₁ ∪ c'₂ and get every K_n by Dehn filling. This unblocks the single most valuable search in the whole plan:

**3. The common-upper-bound concordance search on D_{n,m}.** [K_n] = [K_m] holds if some knot J is ribbon-concordant to both. Enumerate J = K_n banded with one or two unknotted components, canonicalize by isometry signature, intersect with the K_m set. **A hit is a smooth concordance, hence a counterexample**, since D_{n,m} is non-ribbon by Miyazaki. This is the only search in the campaign whose *success is a proof* rather than evidence. Same machine applies to the Gompf–Miyazaki Prop 3.1 pair.

**4. Push K_G searches past the current wall.** The blocker is specific: no non-trivial first band survives the ribbon-link filter in any box tried. Three ways past it — longer bands (length 12–16, expensive), many more diagrams from genuinely different presentations (not `backtrack` perturbations of one diagram), and the Teichner route (search K_G # J for small ribbon J, where the intermediate link filter is different). Also run HKL on the r = 0 knots to check none is secretly obstructed.

**5. Resolve O1 (the Cochran–Davis genus count).** Small, self-contained, and it is what licenses T4's application to genus-5 ribbon disks. Reconstruct the desingularization move and count the genus of the surface produced from a ribbon disk. Weeks, not months.

**6. Extract the fiber and monodromy of K_G.** This is the gating subproject for everything structural. SnapPy gives fiberedness and genus but not the surface; extraction is an inverse search over mapping classes whose mapping torus is certified isometric to the 14-tetrahedron exterior. With φ in hand: apply the T4 filter (two lattices), enumerate cut systems by bounded normal-coordinate weight, and test each derivative for **non-nilpotent** separation — link-group freeness, exterior volume, Heegaard genus, finite-group representation counts. T5 says nothing less will work.

**7. The two theorems that would change everything.**
- *Fibered ribbon-disk completeness* (Meier–Zupan's open question): is every ribbon disk of a fibered knot fibered? If yes, Agol–Ren's finite compression enumeration contains every ribbon disk of K_G and the question becomes a finite audit. Double-edged by design: it would just as likely produce a ribbon disk as exclude one, and either outcome is decisive.
- *Abe–Tange Conjecture 6.1*: is every belt sphere of a 2-handle in a no-3-handle diagram of B⁴ ribbon? Proving it closes lanes 1–3 and the annulus-twist lane in favour of the conjecture. **Disproving it yields a counterexample by construction**, since sliceness in standard B⁴ comes free. Highest payoff on the board; no known attack beyond Abe–Tange's own Lemma 5.1, which their Conjecture 6.2 predicts must sometimes fail.

**Explicitly not to be pursued**, each for a proved reason: Turaev π³ (E1); Casson–Gordon extension tests, metabelian and twisted-Alexander homotopy-ribbon restrictions, irregular dihedral Ξ (all die at homotopy-ribbon, and both flagship candidates are handle-ribbon); Park–Powell and any nilpotent-quotient invariant (T5); Zemke / Levine–Zemke / Gujral–Levine injectivity and DLVVW instanton obstructions (all hold for handle-ribbon concordance, and are vacuous from the unknot anyway); equivariant ribbon obstructions (a ribbon disk need not respect a symmetry); Lagrangian concordance (wrong direction); more ML band searches (calibrated worthless by E10).

---

## 9. Standing discipline

- Search results are **coverage statements**, recorded with their exact parameter box. The word "evidence" is never used for search failure.
- Positive band-search results are certificates, verified by `verify_ribbon_to_unknot` plus a Regina normal-surface check on the terminal unlink.
- Preprint theorems are cited as theorems *in that version*. The flagship's sliceness rests on one unrefereed single-author 2026 preprint; every deliverable depending on it says so.
- Orientation convention: −K = r(K̄) throughout; Miyazaki's pairing hypotheses are re-checked per route-B object.
- No PD code is reported without a verification block. Two extraction attempts stopped rather than guess a diagram; that is the correct outcome, and it is recorded as such.


---

# SESSION 2-3 ADDENDUM (2026-09-11 to 2026-09-12)

## What was accomplished

**Two doors closed permanently, with proofs, not with searches.**
- All Milnor invariants of every R-link vanish (T5), so no nilpotent or
  lower-central-series invariant of derivative links -- Park-Powell's triple-linking
  obstruction included -- can ever separate ribbon from handle-ribbon. Separation
  needs non-nilpotent data.
- Turaev's Theorem H obstructs only homotopy-ribbonness, so it cannot touch any
  handle-ribbon candidate.

**A forty-year-old untested family was tested and closed.** Turaev's Theorem I
produces genus-3 knots that are algebraically slice and provably not
homotopy-ribbon. The paper is essentially uncited and nobody had ever built them.
We built 20 members, validated the construction by two independent internal checks,
and killed every loaded one with Casson-Gordon. Final: 12 dead, 4 timeout, 4 ribbon
controls, 0 live.

**The structural diagnosis.** Every route-A generator builds its candidate's slice
disk from the exterior of a *ribbon* disk of a partner knot, so every candidate is
handle-ribbon by construction and the entire classical battery is logically inert.
That is why no amount of obstruction-improving helps, and it identifies the one
escape: the Teichner sum, whose disk runs a ribbon disk backwards and so is not
automatically handle-ribbon.

**Three theorems** (T1-T4 above): surface slides preserve derivatives; for a fibered
knot the metabolizers of the Seifert form are exactly the monodromy-invariant
Lagrangians (both directions); and the two-lattice lemma pinning every derivative of
18nh00000601 on its fiber to one of two explicit rank-5 lattices.

**Corrections to the inherited record** (E1-E10 plus): Gukov et al.'s three r = 0
pairs are only two, and the duplicate pair sits inside Dunfield-Gong's census where
it was already searched far harder than we can; several attributions were wrong; the
Dunfield-Gong data is on Dataverse, not GitHub.

**Infrastructure that outlives the lanes.** A surface-to-diagram engine
(`tools/surface_engine/`) that realizes an arbitrary Seifert matrix as a verified
knot diagram and implements Milnor's ribbon-linking move. That step blocked this
campaign twice, since neither Turaev nor Abe-Tagami publish a usable diagram. Also a
Seifert-framed cabling routine (`scripts/cable.py`), calibrated against genus on
three knots, and the Abe-Tagami family reconstructed and verified from figures.

## Measurements that redirected effort

**The filter diagnostic.** At one band, 18nh00000601 gives 2161 results of which two
survive and both are trivial, so no two-band search can even start there -- which
explains why every such search was doomed before it began. The Miyazaki sum
D_{0,1} # 6_1 gives 9427 results of which 33 survive. That is a measured structural
difference, and it is why compute moved.

**The Floer torsion order of 18nh00000601 is 1**, so the Juhasz-Miller-Zemke bound
gives no reason to expect a deep ribbon disk. This removed the campaign's own best
explanation for the search failures.

**The Abe-Tagami sums survive what closed the Turaev lane.** Casson-Gordon kills
every loaded Turaev member, several in seconds; on D_{0,1} and D_{0,2} it returns
nothing in 0.8 seconds each. With tau, epsilon, nu and signature all vanishing, the
standard battery is exhausted on them. They are the strongest route-B candidates.

## Two corrections I made to my own claims

1. I said the q = 1 Turaev subfamily was immune to Casson-Gordon because its
   determinant is 1. That rules out only the Sigma_2 flavour; the obstruction fired
   on the 3-fold cover.
2. I asserted a crossing-number cutoff for computability and repeated it as a
   finding. Three later kills at 194, 202 and 226 crossings falsified it. The real
   variable is how deep the certifying character sits in the search, not knot size.
   Both errors are left visible in the files rather than edited away.

## Current board

| lane | status |
|---|---|
| Turaev Theorem I | **CLOSED** for our realizations; residual doubt only in Turaev's realization freedom |
| Abe-Tagami D_{n,m} | **strongest route B**; non-ribbon proved, sliceness open, whole battery exhausted |
| Miyazaki cable (10_17)_{2,1} | live; HKL returned None |
| Hom-Park Cor 1.3 | **built this session** for the first time; battery running |
| 18nh00000601 | live but search-inert: nothing survives band one |
| GST Figure 2 | live; one 1-band survivor exists, unlike 18nh00000601 |
| r = 0 RBG | two distinct pairs, one inside the DG census |

## No counterexample

None of the above is one. What the campaign produced is a sharper map: which doors
are shut and why, which lane is strongest and why, and working tools for the steps
that previously blocked everything.
