# Sources and verification register

Cutoff: 2026-08-30. `PRIMARY` means that the cited paper itself was inspected. It does not mean that an unrefereed preprint is correct. The theorem labels below are the labels in the cited versions. A claim not supported here is marked `UNKNOWN` in the other artifacts.

## Load-bearing primary sources

**[S01] Trevor Oliveira-Smith, “A Dunfield–Gong 4-Sphere is Standard,” arXiv:2603.23717v1 (24 Mar 2026).** [HTML](https://arxiv.org/html/2603.23717v1) · [PDF](https://arxiv.org/pdf/2603.23717)

- Theorem 1.1 identifies the Dunfield–Gong homotopy sphere with the standard smooth (S^4).
- Corollary 1.1.1 proves that `18nh00000601` is smoothly slice in the standard (B^4), using the Trace Embedding Lemma (Lemma 2.2).
- Theorem 1.2 proves that the same knot bounds a fibered handle-ribbon disk in the standard (B^4).
- Corollary 1.1.2 states that (K_G) is a potential counterexample to the Slice-Ribbon Conjecture. Questions 3.3 and 3.4 ask whether the exhibited disk, and whether the knot, is ribbon.
- The introduction says a ribbon disk "has evaded detection"; the paper never claims non-ribbonness. Single version v1 (24 Mar 2026); no citing paper except [S14] as of 2026-09-11. Evidence: `PRIMARY PREPRINT` (re-verified 2026-09-11, see `ERRATA_2026-09-11.md`).

**[S02] Maggie Miller and Alexander Zupan, “Equivalent characterizations of handle-ribbon knots,” Communications in Analysis and Geometry 31 (2023), arXiv:2005.11243.** [PDF](https://arxiv.org/pdf/2005.11243)

- Proposition 1.1: a knot is ribbon iff some genus-(g) Seifert surface has a (g)-component unlink derivative.
- Theorem 1.3: handle-ribbon in a homotopy (4)-ball iff it has an R-link derivative.
- Theorem 1.4 is printed as "([CG83])": it is Casson–Gordon's theorem that a fibered knot is homotopy-ribbon in a homotopy 4-ball iff its zero-surgery fibration extends over handlebodies. Miller–Zupan's own generalization is Theorem 1.5 (singular fibrations).
- Proposition 1.1 is stated as well known, with proof credited to Cochran–Davis [CD15].
- The paper records `ribbon => handle-ribbon => homotopy-ribbon => slice` and says none of the containments is known to be strict. Evidence: `PEER-REVIEWED PRIMARY` (re-verified 2026-09-11).

**[S03] Nathan M. Dunfield and Sherry Gong, “Ribbon concordances and slice obstructions: experiments and examples,” arXiv:2512.21825 (2025).** [PDF](https://arxiv.org/pdf/2512.21825)

- Theorem 1.1 is their census statement for prime knots through 19 crossings.
- Section 2.7 reports that enhanced searches found ribbon disks for all of the 513 + 41 suspicious knots except `18nh00000601`; this failure is not a theorem of non-ribbonness. Band budget was at most four bands (§2.8). The authors expect "hundreds" of further obscure ribbon disks among the 11,383 unresolved knots.
- Code and data are archived on Harvard Dataverse (their reference [DG]); key parts ship in SnapPy 3.3. There is no GitHub repository.
- Theorem 1.12 was conditional before [S01]. Tables 3 and 5 record the knot as genus-five and fibered.
- Sections 3.2–3.3 distinguish rigorous certificates from obstruction/search evidence. Evidence: `PRIMARY PREPRINT`.

**[S04] Robert E. Gompf, Martin Scharlemann and Abigail Thompson, “Fibered knots and potential counterexamples to the Property 2R and Slice-Ribbon Conjectures,” Geometry & Topology 14 (2010), arXiv:1103.1601.** [Journal PDF](https://msp.org/gt/2010/14-4/gt-v14-n4-p13-s.pdf)

- Section 8 constructs the links (L_{n,k}) and proves smooth sliceness by identifying the dual 4-manifold with (B^4).
- Section 8 states the known ribbon cases (n=0,1), (k=0), and ((n,k)=(2,1)), and asks whether the remaining links and their band sums are ribbon.
- The displayed simplest unresolved case is the Figure 2 band sum associated to (L_{3,1}).
- The exhibited slice-link exterior is a regular neighborhood of a wedge of two circles. Evidence: `PEER-REVIEWED PRIMARY`.

**[S05] Tetsuya Abe and Motoo Tange, “A construction of slice knots via annulus twists,” arXiv:1305.7492v4.** [HTML](https://arxiv.org/html/1305.7492v4)

- Theorem 3.1: if a ribbon knot admits the specified annulus presentation, every annulus-twist member (K_n) is smoothly slice in standard (B^4).
- Theorem 5.4: the special family obtained from (8_{20}) is ribbon for (n\ge 0); it is not a live counterexample family in that range.
- Conjecture 6.1 predicts that every belt sphere of a 2-handle in a handle diagram of (B^4) without 3-handles is ribbon.
- Section 6 identifies GST band sums as such belt spheres after a handle slide. Evidence: `PRIMARY PREPRINT`; Conjecture 6.1 is not used as a theorem.

**[S06] Tetsuya Abe and Keiji Tagami, “Fibered knots with the same 0-surgery and the slice-ribbon conjecture,” arXiv:1502.01102v5.** [PDF](https://arxiv.org/pdf/1502.01102)

- Theorem 4.1 restates Miyazaki’s homotopy-ribbon connected-sum theorem, including the minimality/norm-factor hypotheses.
- Corollary 4.3: for the stated fibered knots with irreducible Alexander polynomials, ribbonness of (K_0\#(-K_1)) forces equality of the oriented knots.
- Section 5 defines (K_n=A_n(6_3)); Lemma 5.6 gives the common 0-surgery; Lemmas/remarks in that section establish fiberedness, common irreducible Alexander polynomial (1-3t+5t^2-3t^3+t^4), and (K_n=K_m) only when (n=m) or (n+m=-1).
- Their connected-sum convention uses the mirror of the second summand. This report uses the unambiguous concordance inverse (-K=r(\bar K)). Evidence: `PRIMARY PREPRINT`.

**[S07] Katura Miyazaki, “Nonsimple, ribbon fibered knots,” Transactions of the AMS 341 (1994).** [AMS](https://www.ams.org/journals/tran/1994-341-01/S0002-9947-1994-1176509-9/)

- Theorem 5.5 is the source behind [S06, Theorem 4.1]. It constrains homotopy-ribbon connected sums of prime fibered knots under the stated minimality or Alexander-polynomial norm-factor alternatives. Evidence: `PEER-REVIEWED PRIMARY`, checked through the original and the exact restatement in [S06].

**[S08] Jennifer Hom and JungHwan Park, “Ribbon knots and iterated cables of fibered knots,” arXiv:2507.20455 (2025; publication metadata 2026).** [HTML](https://ar5iv.labs.arxiv.org/html/2507.20455)

- Theorem 1.1: a connected sum of γ₀-sharp fibered knots is ribbon exactly under the stated mirror-pairing condition.
- Corollary 1.2 gives the “linear independence or Slice–Ribbon is false” dichotomy for distinct iterated cables of tight fibered knots.
- Corollary 1.3 gives explicit algebraically slice, non-ribbon knots. It does **not** prove them smoothly slice.
- Proposition 2.6 supplies preservation of γ₀-sharpness for the specified 1-bridge braid patterns. Evidence: `PRIMARY PREPRINT`.

**[S09] Ian Agol and Qiuyu Ren, “Ribbon concordance of fibered knots and compressions of surface homeomorphisms,” arXiv:2603.10884 (2026).** [HTML](https://arxiv.org/html/2603.10884v1)

- Theorem 1.4: simplicial volume is monotone under ribbon concordance between fibered knots. Theorem 1.6: a fibered knot has finitely many ribbon predecessors (proved independently by Baldwin–Hanselman–Sivek [BHS26]).
- Theorem 1.7 is printed as "([CG83])": Casson–Gordon's characterization of strong homotopy-ribbon concordance by monodromy compression. It is not an Agol–Ren result.
- Theorem 1.9 and Corollary 1.11 give an algorithmic/finiteness result for minimal compressions and strong homotopy-ribbon predecessors of a fixed fibered knot.
- The paper says nothing about ribbon disks as distinct from strongly homotopy-ribbon ones, and does not state the question "is every ribbon disk of a fibered knot fibered". Its own remark: modulo slice-ribbon and SPC4, Cor. 1.11 could decide smooth sliceness of the fibered knots in [S03, Table 5]. Evidence: `PRIMARY PREPRINT` (re-verified 2026-09-11).

**[S10] Jennifer Hom and JungHwan Park, “Ribbon concordance and cabling,” arXiv:2608.06625 (6 Aug 2026).** [HTML](https://arxiv.org/html/2608.06625)

- Introduces a minimum-height invariant from immersed-curve knot Floer theory and proves cabling constraints for ribbon concordances.
- No application to `18nh00000601`, GST band sums, or (A_n(6_3)) was found in the paper. Evidence: `PRIMARY PREPRINT`.

**[S11] Hayato Imori, JungHwan Park and Masaki Taniguchi, “Unknotting number, ribbon concordance, and singular instantons,” arXiv:2607.12768 (2026).** [Abstract](https://arxiv.org/abs/2607.12768)

- Uses equivariant singular instanton theory with a Chern–Simons filtration to constrain same-sign crossing changes and ribbon concordance.
- It does not state a general slice-versus-ribbon obstruction and was not applied to the ledger objects. Evidence: `PRIMARY PREPRINT ABSTRACT/THEOREM AUDIT`.

**[S12] Yonghan Xiao, “Real Link Floer Homology,” arXiv:2604.21240 (2026).** [Abstract](https://arxiv.org/abs/2604.21240)

- Constructs equivariant Floer structures for real/periodic links. No theorem in the inspected version was verified to obstruct ribbonness of a general smoothly slice knot. Evidence: `PRIMARY PREPRINT`; candidate applicability `UNKNOWN`.

**[S13] Alexandra Kjuchukova and Kent E. Orr, “Extending Quotients of Knot Groups over Surfaces in (B^4),” arXiv:2604.00460 (2026).** [PDF](https://arxiv.org/pdf/2604.00460)

- Theorem 1.1 gives a computable criterion for a dihedral quotient to extend over an orientable locally flat surface exterior.
- Theorem 7.1 restates the irregular-dihedral-cover obstruction for a (homotopy-)ribbon surface, including the Ξ inequality.
- It is a homotopy-ribbon obstruction; therefore it cannot obstruct knots already proved handle-ribbon. Evidence: `PRIMARY PREPRINT`.

**[S14] Wenjie Diao, Haoqian Pan and Chunxing Yan, “Some experimental results on stable equivalence of GST links,” arXiv:2604.17737 (2026).** [HTML](https://arxiv.org/html/2604.17737)

- Theorem 1.1 proves several finite ranges of stable handleslide equivalences for GST-related links.
- Stable equivalence is not ordinary handleslide triviality and does not by itself produce a ribbon disk for a specified GST band sum. Evidence: `PRIMARY PREPRINT`.

**[S15] Jeffrey Meier and Alexander Zupan, “Knots bounding non-isotopic ribbon disks,” arXiv:2310.17564; Journal of Topology (2025).** (Author corrected 2026-09-11; earlier versions of this register said Miller–Zupan.) [Abstract](https://arxiv.org/abs/2310.17564)

- Produces infinitely many fibered homotopy-ribbon disks for generalized square knots and, in a specified (q=2) subfamily, infinitely many ribbon disks.
- Records the open problem whether every ribbon disk bounded by a fibered knot is fibered. Evidence: `PEER-REVIEWED PRIMARY/PREPRINT`.

**[S16] Gukov, Halverson, Manolescu and Ruehle, “Searching for ribbons with machine learning,” arXiv:2304.09304v2.** [HTML](https://arxiv.org/html/2304.09304v2)

- The algorithms fail on some known ribbon GST examples as well as unresolved examples. Thus non-discovery is not a non-ribbon certificate.
- The paper includes searches on the (L_{3,1}) lane and the GST Figure 2 band sum. Evidence: `PRIMARY PREPRINT`.

**[S17] JungHwan Park and Mark Powell, “A ribbon obstruction and derivatives of knots,” Israel Journal of Mathematics 250 (2022), arXiv:1802.00582.** [Abstract](https://arxiv.org/abs/1802.00582) · [Journal](https://link.springer.com/article/10.1007/s11856-022-2338-y)

- Defines an obstruction to being ℚ[ℤ]-homology ribbon and restricts triple linking numbers of derivative links for homotopy-ribbon or doubly slice knots.
- The authors explicitly allow that their obstruction could fail on a slice knot. Candidate-specific derivative computations were not found. Evidence: `PEER-REVIEWED PRIMARY`; applicability to the ledger is uncomputed.

**[S18] Geske, Kjuchukova and Shaneson, “Signatures of topological branched covers,” arXiv:1901.05858.** [HTML](https://arxiv.org/html/1901.05858v3)

- Theorem 3 gives the irregular dihedral-cover Ξ bound used as an obstruction to homotopy-ribbon surfaces under its coloring/extension hypotheses. Evidence: `PRIMARY PREPRINT`.

**[S19] Stefan Friedl et al., “Homotopy ribbon concordance, Blanchfield pairings, and twisted Alexander polynomials,” arXiv:2007.15289.** [Abstract](https://arxiv.org/abs/2007.15289)

- Gives Blanchfield/twisted-Alexander divisibility restrictions for homotopy-ribbon concordance. It is not a general ribbon-only obstruction. Evidence: `PRIMARY PREPRINT`.

**[S20] Vladimir Turaev, “Multiplace generalizations of the Seifert form of a classical knot,” Mathematics of the USSR-Sbornik 44(3) (1983), 335–361.** [DOI](https://doi.org/10.1070/SM1983v044n03ABEH000971)

- Full English translation recovered 2026-09-11 from mathnet.ru (paper id `sm2474`, Math. USSR-Sb. 44(3) (1983) 335–361; Russian original Mat. Sb. 116(158) (1981) 370–397).
- Theorem H(ii): "If K is a ribbon knot, then F₂(l₁(K), l₂(K)) is metabolic." Theorem I realizes genus-3 algebraically slice knots for which this fails, so the obstruction is nonvacuous for genus ≥ 3.
- The proof of H(ii) (§7.4) uses only that a ribbon knot bounds a disk with π₁(S³∖K) → π₁(B⁴∖D) surjective. It is therefore an obstruction to homotopy-ribbonness, and cannot obstruct ribbonness of any knot already known handle-ribbon.
- Theorem J: "Theorem H yields no new obstructions to sliceness."
- No later paper uses the multiplace form as a ribbon obstruction. The 2010 pointer is a comment by dmoskovich on [D01], not the post itself. Evidence: `PEER-REVIEWED PRIMARY` (full text). Status for `DG`/`GST`: `HYPOTHESES FAIL`.

**[S21] Hans U. Boden et al., “On knots that divide ribbon knotted surfaces,” arXiv:2209.15577v5.** [HTML](https://arxiv.org/html/2209.15577v5)

- Proposition 6: ribbon implies half-ribbon; half-ribbon implies slice by definition/construction.
- Proposition 8: (2g_4(K)\le g_{hr}(K)\le g_{ds}(K)).
- The converse half-ribbon ⇒ ribbon remains open. Evidence: `PRIMARY PREPRINT`.

**[S22] Eisermann, “The Jones polynomial of ribbon links,” Geometry & Topology 13 (2009).** [Journal PDF](https://msp.org/gt/2009/13-2/gt-v13-n2-p01-s.pdf)

- Theorems 1–2 give Jones-nullity/divisibility and determinant congruences for ribbon links. For a one-component knot these do not provide the hoped-for general slice/ribbon separation. Evidence: `PEER-REVIEWED PRIMARY`.

## Sources added 2026-09-11

**[S23] Irving Dai, Sungkyung Kang, Abhishek Mallick, JungHwan Park, Matthew Stoffregen, “The (2,1)-cable of the figure-eight knot is not smoothly slice,” Invent. Math. 238 (2024) 371–390, arXiv:2207.14187.** Introduction quotes Miyazaki [Miy94, Ex. 2, Thm 8.6]: for K fibered, negative amphicheiral, with irreducible Alexander polynomial, K_{2n,1} (n ≠ 0) and K_{p,q} # −T_{p,q} (p ≠ 0) are not (homotopy) ribbon, while being strongly rationally slice. Thm 1.1 kills (4_1)_{2,1}; Thm 1.2 kills K_{2,k} # −T_{2,k} for K ∈ {6_3, 8_12, 8_17}, k odd. States 10_17 is the smallest such K not subsumed. Evidence: `PEER-REVIEWED PRIMARY` (intro read).

**[S24] Sungkyung Kang, JungHwan Park, Masaki Taniguchi, “Smooth concordance of cables of the figure-eight knot,” arXiv:2505.03720.** Every nontrivial cable of 4_1 has infinite order in the smooth concordance group. Evidence: `PRIMARY PREPRINT ABSTRACT`.

**[S25] Sergei Gukov, James Halverson, Ciprian Manolescu, Fabian Ruehle, “Searching for ribbons with machine learning,” arXiv:2304.09304 (= [S16]), §6.** Of Manolescu–Piccirillo's 3375 RBG pairs, five remain of unknown slice and ribbon status; the three with r = 0, K_{B/G}(0,0,0,1,2,−1), K_{B/G}(0,0,0,−1,2,1), K_{B/G}(0,0,−2,0,0,1), "might produce counterexamples to the Slice-Ribbon Conjecture": a ribbon disk for one knot of a pair certifies the other slice in standard B⁴ with no inherited ribbon disk. Evidence: `PRIMARY PREPRINT` (quoted).

**[S26] Ciprian Manolescu and Lisa Piccirillo, “From zero surgeries to candidates for exotic definite four-manifolds,” arXiv:2102.04391, J. LMS (2023).** RBG-link construction of 0-surgery homeomorphisms; Thm 1.2 every 0-friend pair arises this way. Evidence: `PRIMARY PREPRINT ABSTRACT`.

**[S27] Kouki Nakamura, “Trace embeddings from zero surgery homeomorphisms,” arXiv:2203.14270, J. Topology (2023).** Kills the Manolescu–Piccirillo topologically slice knots (not slice). Evidence: `ABSTRACT`.

**[S28] Allison N. Miller and Lisa Piccirillo, “Knot traces and concordance,” arXiv:1702.03974, J. Topology 11 (2018).** d-invariant obstructions to concordance of knots with diffeomorphic 0-traces; disproves a conjecture of Abe. Evidence: `ABSTRACT`. Candidate killer for the Abe–Tagami and Gompf–Miyazaki lanes; not yet applied here.

**[S29] Robert E. Gompf and Katura Miyazaki, “Some well-disguised ribbon knots,” Topology Appl. 64 (1995) 117–131.** Prop. 3.1 (as restated in Tagami arXiv:2010.13283): a pair of knots with homeomorphic 0-surgeries whose connected sum is not ribbon. Evidence: `SECONDARY RESTATEMENT`; full text not retrieved (403).

**[S30] JungHwan Park, “A construction of slice knots via annulus modifications,” arXiv:1512.00401, Topology Appl.** Smoothly slice and separately exotically slice knots via n-twist annulus modifications; smoothly slice knots with non-slice derivatives. Evidence: `ABSTRACT`. Generator only; use only the smoothly-slice half.

**[S31] Jeffrey Meier and Alexander Zupan, “Generalized square knots and homotopy 4-spheres,” arXiv:1904.08527.** Standardizes homotopy 4-spheres built on Q_{p,q}; produces nR-links, potential Generalized Property R counterexamples for all even n. Evidence: `ABSTRACT`.

**[S32] Marc Lackenby, “The stable Andrews–Curtis conjecture and thickenable presentations of the trivial group,” arXiv:2606.06122 (June 2026).** Thickenable balanced presentations satisfy the unstable Andrews–Curtis conjecture. Evidence: `ABSTRACT`. Action: check thickenability of the GST presentations ⟨x,y | yxy=xyx, x^{n+1}=y^n⟩.

**[S33] Stefan Friedl, Filip Misev, Alexander Zupan, “Bounding the ribbon numbers of knots and links,” arXiv:2408.11618.** Set of Alexander polynomials with ribbon number ≤ r is finite and computable. Evidence: `ABSTRACT`. Ribbon-only data, but bounds a quantity defined only for ribbon knots.

**[S34] “Ribbon knots, cabling, and handle decompositions,” arXiv:2003.02832, Thm 1.1.** F_sh(K_{p,1}) = 1 while F(K_{p,1}) = p for ribbon K with F(K) = 1: fusion number and strong-homotopy fusion number differ arbitrarily. Evidence: `PRIMARY` (ar5iv). Shows ribbon-level data is strictly finer than handle-ribbon-level data.

**[S35] Julia Elisenda Grigsby, “On braided, banded surfaces and ribbon obstructions,” arXiv:1801.07158.** A documented attempt at ribbon-only obstructions from Rudolph's braided-banded surfaces; author reports the Khovanov–Lee implementation gives no effective obstruction. Evidence: `ABSTRACT`.

**[S36] Baldwin–Sivek, “Ribbon concordance and fibered predecessors,” arXiv:2510.02214 and part II arXiv:2602.21109; Baldwin–Hanselman–Sivek [BHS26] (cited in [S09]).** Finitely many fibered ribbon predecessors; Remark 1.6 of [S36] states the results hold for handle-ribbon concordance. Evidence: `PRIMARY HTML` for Remark 1.6; BHS26 arXiv id unresolved.

**[S37] Kyle Larson and Jeffrey Meier, “Fibered ribbon disks,” arXiv:1410.4854, JKTR 24 (2015).** Characterizes fibered homotopy-ribbon disks (fibers are handlebodies). Evidence: `ABSTRACT`.

**[S38] Tetsuya Abe, In Dae Jong, Yuka Omae, Masanori Takeuchi, “Annulus twist and diffeomorphic 4-manifolds,” Math. Proc. Camb. Phil. Soc. 155 (2013), arXiv:1209.0361.** Evidence: `ABSTRACT`.

**[S39] Keiji Tagami, arXiv:2010.13283.** Dictionary between dualizable patterns, annulus/band presentations, and RGB diagrams. Evidence: `PRIMARY` (intro read).

## Discovery-only sources

**[D01] “Slice-Ribbon Conjecture in danger!” Low Dimensional Topology blog (2010).** [Post](https://ldtopology.wordpress.com/2010/12/02/slice-ribbon-conjecture-in-danger/)

Used only to locate the historical suggestions attributed to Agol, Friedl and Turaev. It is never authority for a theorem or current open status.

## Search-status discipline

“No application found” means: no application appeared in the inspected primary paper, its cited candidate discussion, targeted author/title searches, or the candidate papers’ references. It does **not** prove that no unpublished calculation exists. Such entries remain `NOT YET COMPUTED` or `UNKNOWN`.
