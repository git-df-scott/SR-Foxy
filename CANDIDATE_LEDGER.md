> **Opus update, 17 September 2026.** The Abe–Tagami row's "Same 0-surgery is not
> concordance" caveat is now sharpened in both directions by
> `research/33_one_stabilization_and_the_forced_collapse.md`: same 0-surgery *does*
> force equal algebraic concordance class (Lemma B), so no Seifert-form invariant
> can obstruct `D_{n,m}`; and the `n = 1` twist trace exhibits `D_{0,1}` bounding a
> smooth disk in `B⁴ # (S²×S²)` (Theorem A). `D_{0,1}` remains a CANDIDATE and
> this audit still finds **NO CE**.

# Certified candidate ledger

Cutoff: 2026-08-30. Binding terminology: **CE** means an explicit knot with both a proof of smooth sliceness in standard (B^4) and a proof of non-ribbonness. Every entry below is a **CANDIDATE**. This audit finds **NO CE**.

## Tier A — smooth sliceness certified; ribbonness unresolved

| object | smooth-slice certificate | explicit disk? | exact weaker status | ribbon status | why it survives / closure barrier |
|---|---|---:|---|---|---|
| (K_{DG}=18_{nh}00000601) | Oliveira-Smith [S01], Cor. 1.1.1, via Theorem 1.1 + Trace Embedding Lemma 2.2 | Yes, constructively through the standardization/trace handle calculus; [S01] also gives an R-link derivative | Fibered (genus 5); handle-ribbon in standard (B^4), [S01, Thm. 1.2]; hence homotopy-ribbon and slice | **UNKNOWN**; no ribbon disk or non-ribbon proof in [S01,S03] | It is the smallest and best documented certified object. All homotopy-ribbon and handle-ribbon obstructions are logically exhausted. Closure needs a genuinely ribbon-specific necessity, most concretely exclusion of every unlink derivative while an R-link derivative exists [S02]. |
| (B_{3,1}): the specific GST Figure 2 band sum associated to (L_{3,1}) | GST [S04, §8]: (L_{3,1}) is a smoothly slice link in standard (B^4); band-summing its disjoint slice disks gives a smooth slice disk | Yes, from the displayed link/band and the dual (B^4) handle description | Belt sphere in a no-3-handle (B^4) diagram after a handle slide [S05, §6]; this gives a handle-theoretic disk, but **half-ribbon is not inferred** | **UNKNOWN**; searches failed but also fail on known ribbon GST cases [S16] | Simplest legacy GST target with explicit diagrams. Its handle origin neutralizes group-epimorphism attacks. Closure again needs unlink-derivative exclusion or a converse tying ribbonness to the unresolved handleslide problem. |
| (B_{n,k,b}): a specified band sum (b) of GST (L_{n,k}), (n\ge2, k\ne0, (n,k)\ne(2,1)) | GST [S04, §8], as above | Yes after fixing the band (b) | Same belt-sphere/handle-diagram mechanism [S05, §6] | Generally **UNKNOWN**; status depends on the band. Do not treat the family symbol as one knot. | An infinite, explicitly generated certified-slice family. It is too broad for computation until ((n,k,b)) is fixed. Stable handleslide results [S14] are not ribbon proofs. |
| (A_j(J)), where (J) is a fixed ribbon knot with a specified annulus presentation | Abe–Tange [S05, Thm. 3.1] | Yes via (W(A_j(J))\cong B^4), constructively | Smoothly slice; further status depends on (J), presentation and (j) | **UNKNOWN in general**, but many subfamilies are ribbon | This is a candidate-production schema, not a promoted knot. It becomes serious only after fixing a diagram and verifying the subfamily was not already ribbonized. |

### Certified but closed/excluded sublanes

- The Abe–Tange (8_{20})-based family ℐ(_n), (n\ge0), is ribbon by [S05, Theorem 5.4]. It is closed as a Foxy lane.
- Dunfield–Gong’s stabilized search produced more than 500 plausible slice objects, but all received ribbon certificates except `18nh00000601` [S03, §2.7]. Search failure alone is not a ledger credential.
- Known GST special cases (n=0,1), (k=0), and ((n,k)=(2,1)) are ribbon [S04, §8].

### Tier A-generators added 2026-09-11 (see `ERRATA_2026-09-11.md`)

| object | mechanism | status | source |
|---|---|---|---|
| The r = 0 super-special RBG pairs. **Corrected 2026-09-11: GHMR's three pairs are only two.** (K_{B/G}(0,0,0,1,2,−1)) and (K_{B/G}(0,0,−2,0,0,1)) are the same pair (identical isometry signatures); it simplifies to 19 crossings, prime and hyperbolic, so it lies **inside** Dunfield–Gong's ≤19-crossing census and has already been searched to 4 bands. The distinct second pair (K_{B/G}(0,0,0,−1,2,1)) is 27/24 crossings, **outside** that census and never searched. All four knots have Alexander polynomial 1. | r = 0 gives diffeomorphic 0-traces, hence identical smooth slice status in **standard** (B^4). A ribbon disk for either knot certifies its partner slice with no inherited ribbon disk. | Both knots of each pair: slice status **UNKNOWN**, ribbon status **UNKNOWN**. Four distinct knots at 19, 19, 24, 27 crossings; all prime and hyperbolic. | [S25] §6, quoted; [S26] |
| Dunfield–Gong 0-friend pairs with r = 0 (unmined) | Same mechanism at census scale: filter DG's >500,000 0-friend pairs to super-special r = 0 RBG realizations, run ribbon search on one side. | Not yet executed. | [S03] §5.11 |
| Teichner-lemma sums (K # J) with (J) ribbon | (K) slice iff some ribbon (J) makes (K # J) ribbon. Certifies (K) slice in standard (B^4) **without** producing a handle-ribbon disk for (K) (the slice disk for (K) contains local maxima from the reversed ribbon concordance). This is the only known generator whose output is not automatically handle-ribbon. | DG ran it at ≤ 19 crossings; all 513 outputs later proved ribbon. | [S03] §2.6 |

## Tier B — non-ribbonness certified; smooth sliceness unresolved

| object | non-ribbon certificate | smooth-slice status | why it matters / barrier |
|---|---|---|---|
| Miyazaki cables (K_{p,q} # -T_{p,q}) and (K_{2n,1}), (K) fibered, negative amphicheiral, irreducible Δ; smallest live member **((10_{17})_{2,1})** | Miyazaki 1994, Ex. 2 / Thm 8.6, as quoted in [S23]: not (homotopy) ribbon | **UNKNOWN**; strongly rationally slice (Kawauchi), all HFK/involutive/s invariants vanish. Dead members: all cables of (4_1) [S23,S24]; (K_{2,k} # -T_{2,k}) for (K \in \{6_3, 8_{12}, 8_{17}\}), (k) odd [S23, Thm 1.2]. | Free non-ribbon certificate; the entire difficulty is a slice disk. Route-B lane with the deepest history. Killers: equivariant/real Floer (DKMPS, KPT), real 10/8 (Fukumoto–Taniguchi). |
| Gompf–Miyazaki Prop. 3.1 pair (J(O) # J^*(O)) | Gompf–Miyazaki 1995 [S29] | **UNKNOWN**; Miller–Piccirillo d-invariants [S28] may already kill it, unchecked | Prototype of the Abe–Tagami lane. |
| (D_{n,m}=K_n\#(-K_m)), (K_j=A_j(6_3)), with (K_n\not\cong K_m) | Miyazaki [S07, Thm. 5.5] as applied in Abe–Tagami [S06, Thm. 4.1 and Cor. 4.3], using prime fibered summands and the common irreducible Alexander polynomial | **UNKNOWN**. It is slice if ([K_n]=[K_m]) in smooth concordance. No such equality was verified. | The implication to a CE is exact and sign-correct, but all the difficulty is transferred to a concordance collision. Same 0-surgery is not concordance. |
| Hom–Park (P(K,J,p,q_1,q_2)=K_{p,q_1}\#-K_{p,q_2}\#J_{p,q_2}\#-J_{p,q_1}) under Cor. 1.3’s hypotheses | Hom–Park [S08, Thm. 1.1, Cor. 1.3] | Algebraically slice; smooth sliceness **UNKNOWN** | A sharp modern ribbon obstruction with explicit knots, but not a certified-slice lane. |

## Status verdicts

1. **Primary lane:** (K_{DG}). Certified smooth slice, exact standard ambient (B^4), explicit handle/R-link data, ribbon status unresolved.
2. **Second lane:** fixed GST Figure 2 band sum (B_{3,1}). Certified smooth slice but diagrammatically large and structurally handle-ribbon-like.
3. **Abe–Tagami lane:** **WEAK/LIVE**. Non-ribbonness is rigorous; sliceness is not. A concordance equality would instantly create a CE, while any distinguishing concordance invariant kills only that pair.
4. **Hom–Park lane:** **WEAK/LIVE** for Foxy. It proves non-ribbonness but does not supply smooth slice disks.

## Ambient and operation audit

- “Smoothly slice” in this ledger always means a smooth disk in the **standard** (B^4). A disk in a homotopy ball was not silently promoted; [S01] first standardizes the relevant sphere.
- (-K=r(\bar K)) is the inverse in oriented smooth concordance. Mirrors, reversals, and connected sums are written explicitly.
- Stable handleslide equivalence, stabilization, homotopy-ribbonness, handle-ribbonness and half-ribbonness are never identified with ribbonness.
- Mutation and common 0-surgery do not preserve or imply smooth concordance without a separate theorem; no such inference is used.

## Turaev Theorem I knots — 16 September 2026: NOT candidates, lane nearly empty

`research/29`, **as corrected**. An earlier version of this entry, written earlier
the same day, listed all five `data/knots/Turaev_A_*.json` knots as Tier-B
candidates. That was wrong and is withdrawn. `results/turaev_family_status.md`
(UPDATE, 12 September 2026) already settled the matter.

| object | `(p,q,r,s)` | cr | `mu_135,mu_246` | Theorem I obstructs | status |
|---|---|---|---|---|---|
| `Turaev_A_1_1_0_0` | (1,1,0,0) | 27 | (0,0) | **no** | **RIBBON** — one-band DG certificate, 1.3 s |
| `Turaev_A_1_3_0_0` | (1,3,0,0) | 37 | (0,0) | **no** | not a candidate |
| `Turaev_A_2_1_0_0` | (2,1,0,0) | 39 | (0,0) | **no** | not a candidate |
| `Turaev_A_3_1_0_0` | (3,1,0,0) | 51 | (0,0) | **no** | not a candidate |
| `Turaev_A_1_1_1_1` | (1,1,1,1) | 143 | (1,1) | **yes** | **DEAD** — `slice_obstruction_HKL` = (3,13), not topologically slice (12 Sep, reverified 25.3 s) |

Theorem I's conclusions are for `r≠0 and s≠0`, `r≠0 or s≠0`, and `r=0,s≠0` or
`r≠0,s=0`. **`r = s = 0` falls into none of them**, so the four `(0,0)` members carry
no non-ribbon certificate at all; `research/08` §4 says this outright. The `s = 0`
values computed on three of them on 16 September are correct computations with **no
evidential value**, and `A(1,1,0,0)` being ribbon made its own row a foregone
conclusion.

**What is still true.** Turaev Theorem I *is* a route-B certificate needing only one
knot to be smoothly slice — no concordance coincidence, no pair of fibered knots — so
`research/24` §4's "the only route on this board that escapes section 1" is wrong as
written. But the family has exactly **one** realised member, and it is dead. The next
smallest unbuilt members are `(1,3,1,1)` and `(2,1,1,1)`; the build pipeline exists,
and the expected outcome is another HKL kill. HKL needs Sage.
