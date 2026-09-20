# Sources and verification register

Cutoff: 2026-08-30. `PRIMARY` means that the cited paper itself was inspected. It does not mean that an unrefereed preprint is correct. The theorem labels below are the labels in the cited versions. A claim not supported here is marked `UNKNOWN` in the other artifacts.

## Load-bearing primary sources

**[S01] Trevor Oliveira-Smith, “A Dunfield–Gong 4-Sphere is Standard,” arXiv:2603.23717v1 (24 Mar 2026).** [HTML](https://arxiv.org/html/2603.23717v1) · [PDF](https://arxiv.org/pdf/2603.23717)

- Theorem 1.1 identifies the Dunfield–Gong homotopy sphere with the standard smooth (S^4).
- Corollary 1.1.1 proves that `18nh00000601` is smoothly slice in the standard (B^4), using the Trace Embedding Lemma (Lemma 2.2).
- Theorem 1.2 proves that the same knot bounds a fibered handle-ribbon disk in the standard (B^4).
- The introduction says no ribbon disk is known. Evidence: `PRIMARY PREPRINT`.

**[S02] Maggie Miller and Alexander Zupan, “Equivalent characterizations of handle-ribbon knots,” Communications in Analysis and Geometry 31 (2023), arXiv:2005.11243.** [PDF](https://arxiv.org/pdf/2005.11243)

- Proposition 1.1: a knot is ribbon iff some genus-(g) Seifert surface has a (g)-component unlink derivative.
- Theorem 1.3: handle-ribbon in a homotopy (4)-ball iff it has an R-link derivative.
- Theorem 1.4 (Casson–Gordon formulation): a fibered knot is homotopy-ribbon iff its zero-surgery fibration extends over a handlebody.
- The paper records `ribbon => handle-ribbon => homotopy-ribbon => slice`; converses are not asserted. Evidence: `PEER-REVIEWED PRIMARY`.

**[S03] Nathan M. Dunfield and Sherry Gong, “Ribbon concordances and slice obstructions: experiments and examples,” arXiv:2512.21825 (2025).** [PDF](https://arxiv.org/pdf/2512.21825)

- Theorem 1.1 is their census statement for prime knots through 19 crossings.
- Section 2.7 reports that enhanced searches found ribbon disks for all 554 suspicious knots except `18nh00000601`; this failure is not a theorem of non-ribbonness.
- Sections 2.2–2.3 state that no band-arc complexity bound is known and describe the
  finite simple-path search. Section 2.8 says the search went through at most four
  bands and then stopped; this does not exclude all disks with at most four bands.
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

- Theorem 1.4: simplicial volume is monotone under ribbon concordance between fibered knots.
- Theorem 1.7: strong homotopy-ribbon concordance is characterized by monodromy compression.
- Theorem 1.9 and Corollary 1.11 give an algorithmic/finiteness result for minimal compressions and strong homotopy-ribbon predecessors of a fixed fibered knot.
- This detects strong homotopy-ribbon structure, not the difference between ribbon and handle-ribbon. Evidence: `PRIMARY PREPRINT`.

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

**[S15] Maggie Miller and Alexander Zupan, “Knots bounding non-isotopic ribbon disks,” arXiv:2310.17564; Journal of Topology (2025).** [Abstract](https://arxiv.org/abs/2310.17564)

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

**[S20] Vladimir Turaev, “Multiplace generalizations of the Seifert form of a classical knot,” Mathematics of the USSR-Sbornik 44(3) (1983), 335–361.** [MathNet primary record and PDF](https://www.mathnet.ru/eng/sm2474) · [DOI](https://doi.org/10.1070/SM1983v044n03ABEH000971)

- Theorem H(ii) says the relevant two-place form is metabolic for a ribbon knot.
- In its proof, Lemma 7.2 gives metabolicity for a smooth slice disk when the
  induced commutator-quotient map is surjective. That hypothesis follows from the
  full knot-group epimorphism of a handle-ribbon disk [S02], so it is neutralized
  for `18nh00000601` [S01]. Evidence: `PEER-REVIEWED PRIMARY`, theorem and proof
  inspected.

**[S21] Hans U. Boden et al., “On knots that divide ribbon knotted surfaces,” arXiv:2209.15577v5.** [HTML](https://arxiv.org/html/2209.15577v5)

- Proposition 6: ribbon implies half-ribbon; half-ribbon implies slice by definition/construction.
- Proposition 8: (2g_4(K)\le g_{hr}(K)\le g_{ds}(K)).
- The converse half-ribbon ⇒ ribbon remains open. Evidence: `PRIMARY PREPRINT`.

**[S22] Eisermann, “The Jones polynomial of ribbon links,” Geometry & Topology 13 (2009).** [Journal PDF](https://msp.org/gt/2009/13-2/gt-v13-n2-p01-s.pdf)

- Theorems 1–2 give Jones-nullity/divisibility and determinant congruences for ribbon links. For a one-component knot these do not provide the hoped-for general slice/ribbon separation. Evidence: `PEER-REVIEWED PRIMARY`.

**[S23] Dunfield–Gong, replication archive for [S03], Harvard Dataverse, DOI 10.7910/DVN/YBDTBT.** [Dataset landing page](https://doi.org/10.7910/DVN/YBDTBT)

- The archive supplies the exact PD code and census row for `18nh00000601`, the
  three RBG certificates connecting it to 31-crossing ribbon knots, and the code
  used for the bounded band searches.
- `unknown_with_0-friend_final.csv` marks the 31-crossing partners ribbon; that
  flag does not mark the base knot ribbon.
- Streaming audits of `zero_friends.csv.bz2` and `more_zero_friends.csv.bz2` found
  only `19nh_001785287` from [S03, Table 8], and its recorded friend remains
  `slice=0`, `ribbon=0`. Evidence: `PRIMARY REPLICATION DATA`.

## Discovery-only sources

**[D01] “Slice-Ribbon Conjecture in danger!” Low Dimensional Topology blog (2010).** [Post](https://ldtopology.wordpress.com/2010/12/02/slice-ribbon-conjecture-in-danger/)

Used only to locate the historical suggestions attributed to Agol, Friedl and Turaev. It is never authority for a theorem or current open status.

## Search-status discipline

“No application found” means: no application appeared in the inspected primary paper, its cited candidate discussion, targeted author/title searches, or the candidate papers’ references. It does **not** prove that no unpublished calculation exists. Such entries remain `NOT YET COMPUTED` or `UNKNOWN`.
