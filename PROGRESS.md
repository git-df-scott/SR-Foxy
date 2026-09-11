# Progress report: execution of the campaign (2026-09-11, session 2)

Honest status line: **no counterexample yet, and none of today's results moves any candidate closer to one.** What changed today is that the plan is now running as code against verified objects, several lanes were narrowed by theorems, and one dead end was closed for good. Every item below is either a certificate, a coverage statement, or a proof; nothing is "evidence".

## 1. Environment

- Sage-backed SnapPy works via `pip install passagemath-standard` (`snappy.sage_helper._within_sage` is True). The Dunfield–Gong band search, the HKL Casson–Gordon obstruction and Seifert matrices are all available.
- **Calibration passed.** The band search rediscovered the known ribbon disk of K_B (the 31-crossing 0-friend of K_G) on the first diagram in 0.9 s, with a certificate verified by `verify_ribbon_to_unknot` (`results/KB_calibration_shaken20_bands2.json`). So negatives on K_G from the same parameter box are real coverage.

## 2. K_G = 18nh00000601 (route A, lane 1)

| experiment | box | outcome |
|---|---|---|
| band search, one diagram | 2 bands, twists ≤ 2, length ≤ 6, shortest paths | 2161 one-band results; 1704 fail linking number, 387 fail signature, 68 fail Fox–Milnor; the only 2 survivors are K_G with a split unknot (trivial bands). **No plausibly-slice one-band move exists in this box**, so no two-band search can start. |
| band search, one diagram | 2 bands, twists ≤ 3, length ≤ 10, shortest | same: 0 survivors |
| shaken diagrams | 60 diagrams (backtrack 25), 2 bands, length ≤ 8 | running; 15 diagrams done, 0 survivors each |
| shaken diagrams | 30 diagrams, 3 bands, length ≤ 7 | running; 12 diagrams done, 0 survivors each |
| 'simple' band paths | 2 bands, length ≤ 8 | running |

Reading: with DG's own filter (an intermediate link in a ribbon movie must itself be a ribbon link, so must pass linking number, signature and Fox–Milnor), the first band of any ribbon disk for K_G is not a short band on these diagrams. Either the first band is long or the diagram must be far from these. This is a coverage statement, not an obstruction.

**The R-link derivative is not in the literature.** Oliveira-Smith's Theorem 1.2 obtains the derivative L⁺ from a Miller–Zupan existence theorem applied to the two-component R-link K_G ∪ U, and never draws L⁺; even K_G ∪ U is drawn with unexpanded twist boxes (`results/KG_derivative_extraction.md`). So the planned "handleslide search on L⁺" has no input. What was verified instead: the RBG link from DG Table 11 reproduces K_G exactly (fill R with +1 and B with 0 gives the K_G exterior, isometry certified), and K_B was extracted as a 31-crossing knot (`data/knots/K_B_0friend.json`).

**Seifert data.** Signature 0; Alexander polynomial = f(t)·f*(t) with f = t⁵ − t² + 2t − 1 irreducible and f ≠ ±f*.

## 3. Theory results (research/06, research/07)

Proved in this session (proofs written out, not yet refereed):

1. **Surface slides preserve derivatives.** Sliding one derivative component over another along an arc in the Seifert surface gives another derivative with the same 0-surgery. The surface-slide orbit of a derivative is exactly the set of meridian systems of the handlebody it determines.
2. **For a fibered knot, {metabolizers of the Seifert form} = {monodromy-invariant Lagrangians}.** One direction is the theory agent's Theorem 3.1; the converse (Lemma A in research/07) is a three-line argument from V = Vᵀφ and unimodularity.
3. **Two-lattice lemma for K_G.** Because Δ = f f* with f irreducible and f ≠ f*, every derivative of K_G on its fiber, unlink or R-link, has homology span equal to one of two explicit rank-5 lattices ker f(φ) and ker f*(φ). This is an exact linear-algebra filter for any future enumeration of cut systems on the fiber.
4. **All Milnor invariants of every R-link vanish** (Theorem 5.1). Consequence: no nilpotent-quotient or lower-central-series invariant of derivative links, including Park–Powell's triple-linking obstruction, can separate ribbon from handle-ribbon. Every R-link is a homology boundary link. This closes another door permanently.
5. **The gap is exactly Generalized Property R.** K ribbon iff some derivative has free link group; K handle-ribbon iff some derivative is an R-link. There is no intermediate derivative-level condition. For K_G: ribbon ⟸ Generalized Property R for the (unknown, but existing) 5-component R-link on the fiber.

What this means for the hunt: a non-ribbon proof for K_G needs a non-nilpotent invariant of R-links that vanishes on unlinks and is invariant under surface slides (link-group freeness, volume of the derivative exterior, Heegaard genus, finite-group representation counts), applied to *every* derivative. That enumeration requires the fiber and monodromy explicitly; not yet available.

## 4. Route-A generator: the r = 0 RBG pairs (lane 2)

All ten Manolescu–Piccirillo knots K_{B/G} for the five GHMR tuples were built from the authors' own DT-code notebook (parameter signs recovered by matching 44/44 published volumes and HFK ranks), and verified: each pair has isometric 0-surgeries and distinct exteriors (`data/knots/MP_*.json`, `data/knots/EXTRACTION_SUMMARY.md`).

- The three r = 0 pairs have **Alexander polynomial 1** (so they are topologically slice by Freedman) and genus 2; τ = ε = ν = signature = 0 on all ten knots. No cheap obstruction touches them.
- Ribbon searches on the six r = 0 knots are queued (12 shaken diagrams each, 2 bands). A hit certifies the partner smoothly slice in standard B⁴ with no inherited ribbon disk: a second route-A target. Results pending.

## 5. Route B (lanes 4–6)

- **(10_17)_{2,1}** built as the Seifert-framed (2,1)-cable (41 crossings), verified by genus 8 and Δ(t) = Δ_{10_17}(t²). τ = ε = ν = signature = 0. The HKL Casson–Gordon obstruction is running; a nonzero result would prove non-sliceness and kill the smallest live Miyazaki member.
- **Abe–Tagami K_n = A_n(6_3)**: no machine-readable diagram exists anywhere; the first extraction attempt stopped honestly. A second attempt is running that builds the 3-component link 6_3 ∪ c'₁ ∪ c'₂ (c'₁ ∪ c'₂ is a Hopf link, 6_3 their band sum) and obtains every K_n by Dehn filling, verified by the shared 0-surgery and K_{−1} = K_0 = 6_3. Side result already rigorous: no hyperbolic knot with ≤ 14 crossings other than 6_3 has the 0-surgery of 6_3, so the K_n are not table knots.
- Once K_n are in hand: the common-upper-bound concordance search of the plan (WS2.2) runs on D_{n,m}; a hit is a smooth concordance and an instant counterexample, since D_{n,m} is non-ribbon by Miyazaki.

## 6. GST (lane 3)

Regina's built-in Figure 2 knot (48 crossings) matches GST's `sliceknot.eps` (two full-twist boxes on four strands plus 24 crossings). Genus 10, τ = 0, Fox–Milnor holds. It is **not fibered** (top Alexander grading has rank 2), which the ledger correctly left open. A one-band search is running; Gukov et al. never ran the DG search on it.

## 7. Files added this session

`scripts/band_search.py`, `scripts/band_search_shaken.py`, `scripts/hkl_obstruction.py`, `scripts/run_queue.sh`; `data/knots/*.json` (K_G with Seifert matrix, K_B, ten RBG knots, cable, GST, 6_3); `results/*.json` (coverage records); `results/KG_derivative_extraction.md`; `research/06_theory_derivatives_on_fiber.md`, `research/07_two_lattice_lemma.md`.

## 8. What would change the picture next

1. A ribbon disk for K_G from the wider searches: lane closes, and the plan's own prediction ("the likelier headline") is confirmed.
2. A ribbon disk for one knot in an r = 0 pair: a fresh certified-slice, handle-ribbon, ribbon-unknown knot with Alexander polynomial 1.
3. A concordance hit for some D_{n,m}: a counterexample. This is the only search in the plan whose success is a proof.
4. HKL firing on (10_17)_{2,1}: the Miyazaki lane's smallest member dies and the next (K_{p,q} # −T_{p,q} with p odd) moves up.
