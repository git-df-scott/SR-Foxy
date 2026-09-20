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

## Tier B — non-ribbonness certified; smooth sliceness unresolved

| object | non-ribbon certificate | smooth-slice status | why it matters / barrier |
|---|---|---|---|
| (D_{n,m}=K_n\#(-K_m)), (K_j=A_j(6_3)), with (K_n\not\cong K_m) | Miyazaki [S07, Thm. 5.5] as applied in Abe–Tagami [S06, Thm. 4.1 and Cor. 4.3], using prime fibered summands and the common irreducible Alexander polynomial | **UNKNOWN**. It is slice if ([K_n]=[K_m]) in smooth concordance. No such equality was verified. | The implication to a CE is exact and sign-correct, but all the difficulty is transferred to a concordance collision. Same 0-surgery is not concordance. |
| Hom–Park (P(K,J,p,q_1,q_2)=K_{p,q_1}\#-K_{p,q_2}\#J_{p,q_2}\#-J_{p,q_1}) under Cor. 1.3’s hypotheses | Hom–Park [S08, Thm. 1.1, Cor. 1.3] | Algebraically slice; smooth sliceness **UNKNOWN** | A sharp modern ribbon obstruction with explicit knots, but not a certified-slice lane. |
| Dunfield–Gong Table 8 (24 named census knots) | Dunfield–Gong [S03, Thm. 3.12 and Table 8]: not even topologically homotopy-ribbon | Smooth and topological sliceness **UNKNOWN** | This is the cleanest non-ribbon-first lane. A full list and data audit are in `KDG_EXACT_AUDIT.md`. Exactly one, `19nh_001785287`, has a recorded extended-search zero-friend, whose sliceness is also unknown [S23]. |

## Status verdicts

1. **Primary lane:** (K_{DG}). Certified smooth slice, exact standard ambient (B^4), explicit handle/R-link data, ribbon status unresolved.
2. **Second lane:** fixed GST Figure 2 band sum (B_{3,1}). Certified smooth slice but diagrammatically large and structurally handle-ribbon-like.
3. **Abe–Tagami lane:** **WEAK/LIVE**. Non-ribbonness is rigorous; sliceness is not. A concordance equality would instantly create a CE, while any distinguishing concordance invariant kills only that pair.
4. **Hom–Park lane:** **WEAK/LIVE** for Foxy. It proves non-ribbonness but does not supply smooth slice disks.
5. **Dunfield–Gong Table 8 lane:** **LIVE**. Non-ribbonness is already stronger than
   required; `19nh_001785287` is the first trace-standardization target because it
   is the only one of the 24 with a recorded zero-friend in [S23].

## Ambient and operation audit

- “Smoothly slice” in this ledger always means a smooth disk in the **standard** (B^4). A disk in a homotopy ball was not silently promoted; [S01] first standardizes the relevant sphere.
- (-K=r(\bar K)) is the inverse in oriented smooth concordance. Mirrors, reversals, and connected sums are written explicitly.
- Stable handleslide equivalence, stabilization, homotopy-ribbonness, handle-ribbonness and half-ribbonness are never identified with ribbonness.
- Mutation and common 0-surgery do not preserve or imply smooth concordance without a separate theorem; no such inference is used.
