# Source Verification Audit — Slice–Ribbon Research Package (cutoff 2026-08-30)

Audit date: **2026-09-11**. Evidence labels: **VERIFIED** = primary text fetched and statement read; **PARTIALLY VERIFIED** = abstract/listing metadata only; **UNVERIFIED / NOT FOUND**.

All arXiv full texts below were retrieved as arXiv LaTeXML HTML (`arxiv.org/html/<id>v1`) or as the PDF with text extraction, except where noted. No claim in this report is asserted without a fetched source.

---

## 1. Per-source table

| id | exists? | authors (as printed) | exact title | version / date | claims verified | discrepancies | label | URL |
|---|---|---|---|---|---|---|---|---|
| **S01** | YES | Trevor Oliveira-Smith (UC Davis, advisor Abby Thompson) | *A Dunfield–Gong 4-Sphere is Standard* | v1 only, submitted Tue 24 Mar 2026 21:05:45 UTC; 15 pp., 10 figs; MSC 57R60 (primary), 57R65, 57K10 | Thm 1.1 ✔; Cor 1.1.1 ✔; Thm 1.2 ✔; ribbon status stated as unknown ✔ | (a) Package omits **Corollary 1.1.2** ("K_G is a potential counterexample to the Slice-Ribbon Conjecture"), which is the paper's own framing of the slice-ribbon consequence — it is a separate numbered corollary, not part of Cor 1.1.1. (b) The paper's own `\date` line reads **"Date: August 24, 2026"** while the only posted version is v1 of **24 March 2026** — an internal date inconsistency in the source; there is **no v2**. (c) The intro says the ribbon disk "has evaded detection," i.e. *not known*, and calls the knot a *potential* counterexample — it does **not** assert the knot is non-ribbon. | **VERIFIED** | https://arxiv.org/abs/2603.23717 , https://arxiv.org/html/2603.23717v1 |
| **S03** | YES | Nathan M. Dunfield, Sherry Gong | *Ribbon concordances and slice obstructions: experiments and examples* | v1 only, submitted Fri 26 Dec 2025 01:47:29 UTC; 62 pp., 24 figs, 12 tables | census ≤19 crossings ✔; 18nh00000601 sole survivor ✔; genus 5 ✔; fibered ✔; code availability ✔ (but see discrepancy) | (a) **"554 suspicious knots" is a package-computed figure, not a number printed in the paper.** §2.7 ("Obscure ribbon disks") says the expanded search covered "the 513 smoothly slice knots from the previous subsection, as well as 41 knots that are 0-friends with a ribbon knot" — 513 + 41 = 554. Correct arithmetic, but the paper never writes 554. (b) **Code is NOT on GitHub.** §1.19 "Code and data": data/code "permanently archived at [DG]"; reference [DG] = "N. M. Dunfield and S. Gong. *Ribbon concordances and slice obstructions: code and data.* **Harvard Dataverse, 2025.**" Key parts folded into the SnapPy development version (to ship in SnapPy 3.3). The only `github` string in the paper is `regina-normal.github.io` (the Regina software reference). Naming a GitHub repo would be fabrication. | **VERIFIED** | https://arxiv.org/abs/2512.21825 , PDF v1 |
| **S09** | YES | Ian Agol, Qiuyu Ren (both UC Berkeley) | *Ribbon concordance of fibered knots and compressions of surface homeomorphisms* | v1 only, submitted Wed 11 Mar 2026 15:29:05 UTC; 30 pp., 2 color figs; MSC 57K | Thm 1.4 (simplicial volume monotone) ✔; Thm 1.7 (strong homotopy-ribbon ⇔ monodromy compression) ✔ *as stated*; Thm 1.9 + Cor 1.11 (finiteness / algorithm) ✔ | (a) **Thm 1.7 is not the authors' result** — it is printed as "Theorem 1.7 ([CG83])", a consequence of **Casson–Gordon**. Attributing it to Agol–Ren is a misattribution. (b) **The paper says nothing about ribbon (non-homotopy-ribbon) disks as such, and contains no statement of the question "every ribbon disk of a fibered knot is fibered."** The string "handle-ribbon" does not occur anywhere in the paper. The only open questions raised are Question 1.15 (common fibered upper bound for concordant fibered knots) and the remark that it is open whether ≤_h is strictly finer than ≤. This package claim is **NOT FOUND** in the source. (c) Package omits the finiteness theorem's own number: finiteness of ribbon predecessors of a fibered knot is **Theorem 1.6** (Thm 1.9 is finiteness of *minimal compressions of a surface homeomorphism* up to symmetry; Cor 1.11 is the knot-level finiteness+algorithm for ≤_h). | **VERIFIED** (with one sub-claim NOT FOUND) | https://arxiv.org/abs/2603.10884 , https://arxiv.org/html/2603.10884v1 |
| **S08** | YES | Jennifer Hom, JungHwan Park | *Ribbon knots and iterated cables of fibered knots* | v1, Mon 28 Jul 2025 01:13:38 UTC | exists, authors, title ✔ | No theorem numbers were carried in the package excerpt, so none could be checked. Main result (verbatim abstract): "a connected sum of γ₀-sharp fibered knots is ribbon exactly when it is of the form K # −K. Consequently, either iterated cables of tight fibered knots are linearly independent in the smooth concordance group, or the slice–ribbon conjecture fails." | **PARTIALLY VERIFIED** (abstract/metadata) | https://arxiv.org/abs/2507.20455 |
| **S10** | YES | Jennifer Hom, JungHwan Park | *Ribbon concordance and cabling* | v1, Thu 6 Aug 2026 22:18:01 UTC | exists, authors, title ✔ | One-line result: conjectures that any nontrivial knot ribbon concordant to a (p,q)-cable is itself a (p,q)-cable; proved when the source knot is a cable of the same companion, a torus knot, or genus one, plus a broad class of target cables; proofs use a minimum-height invariant from immersed-curve knot Floer homology, which also implies any nontrivial knot ribbon concordant to a fibered cable knot is prime. | **PARTIALLY VERIFIED** (abstract/metadata) | https://arxiv.org/abs/2608.06625 |
| **S11** | YES | Hayato Imori, JungHwan Park, Masaki Taniguchi | *Unknotting number, ribbon concordance, and singular instantons* | v1, Tue 14 Jul 2026 13:41:20 UTC | exists, authors ✔ | **Title discrepancy**: package labels it via the three authors only; the actual title is *Unknotting number, ribbon concordance, and singular instantons* — it is an **unknotting-number** paper, not a slice-ribbon paper. Result: equivariant singular instanton Floer theory with Chern–Simons filtration obstructs same-sign unknotting; for a large class of slice knots obtained through ribbon concordance, any unknotting sequence of null-homologous twists must contain both signs; plus a 3-manifold analogue giving evidence for monotonicity of Dehn surgery number under ribbon homology cobordism. Gives **no ribbon-vs-slice obstruction**. | **PARTIALLY VERIFIED** (abstract/metadata) | https://arxiv.org/abs/2607.12768 |
| **S12** | YES | Yonghan Xiao | *Real link Floer homology* | v1 23 Apr 2026; **v2 30 May 2026; v3 18 Aug 2026** | exists, author ✔ | **Not a ribbon/slice-ribbon paper.** It defines real link Floer homology for strongly invertible and doubly periodic links, with a real grid-diagram combinatorial model; computer implementation by Zhenkun Li; appendix of 50+ small knots joint with Li. Any package claim that this bears on ribbonness is **NOT SUPPORTED** by the abstract. Also: package cites no version — three versions exist, the latest post-dating much of the package window. | **PARTIALLY VERIFIED** (abstract/metadata) | https://arxiv.org/abs/2604.21240 |
| **S13** | YES | Alexandra Kjuchukova, Kent E. Orr | *Extending Quotients of Knot Groups over Surfaces in $B^4$* | v1, Wed 1 Apr 2026 04:12:37 UTC | exists, authors ✔ | Title is **not** ribbon-specific. Result: a sharp obstruction to existence of a connected oriented smooth surface F ⊂ B⁴ with ∂F = K over whose exterior a given quotient ρ: π₁(E_K) ↠ G extends surjectively; for dihedral G the obstruction is computed by evaluating the Seifert form on a single *characteristic knot*; when the dihedral obstruction vanishes F is constructed explicitly. This is a **branched-cover / surface-in-B⁴** obstruction, not a ribbon-vs-slice obstruction. | **PARTIALLY VERIFIED** (abstract/metadata) | https://arxiv.org/abs/2604.00460 |
| **S14** | YES | Wenjie Diao, Haoqian Pan, Chunxing Yan | *Some experimental results on stable equivalence of GST Links for the Generalized Property R Conjecture* | v1, Mon 20 Apr 2026 02:50:10 UTC | exists, authors ✔ | Result: implements an algorithm constructing all GST (Gompf–Scharlemann–Thompson) / Meier–Zupan R-links explicitly; verifies stable handleslide triviality of some; shows many are stably handleslide equivalent. Abstract contains a **broken LaTeX citation** (`\cite{Knots in the fiber}`) — a sign the preprint is unrefereed/rough. This is the **only paper on record citing S01** (per Semantic Scholar, citationCount = 1). | **PARTIALLY VERIFIED** (abstract/metadata) | https://arxiv.org/abs/2604.17737 |
| **S02** | YES | Maggie Miller, Alexander Zupan | *Equivalent characterizations of handle-ribbon knots* | v1, 22 May 2020 | Prop 1.1 ✔; Thm 1.3 ✔; definitions recovered ✔ | **Theorem 1.4 is not a Miller–Zupan result** — it is printed as "Theorem 1.4 ([CG83])", the classical **Casson–Gordon** theorem. The Miller–Zupan generalization is **Theorem 1.5**. If the package attributes Thm 1.4 to Miller–Zupan, that is a misattribution. | **VERIFIED** | https://arxiv.org/abs/2005.11243 , https://arxiv.org/html/2005.11243 |
| **S20** | YES | V. G. Turaev | *Multiplace generalizations of the Seifert form of a classical knot* | Mat. Sb. (N.S.) **116(158)**:3(11) (1981) 370–397; Engl. transl. Math. USSR-Sb. **44**(3) (1983) 335–361; received 12 Sep 1980; DOI 10.1070/SM1983v044n03ABEH000971; mathnet id `sm2474` | Theorem H **recovered verbatim** ✔ | See §3 below — a substantive correction: Theorem H(ii) is an obstruction to **ribbonness only via homotopy-ribbonness**, and Theorem **J** of the same paper explicitly says Theorem H yields **no new obstruction to sliceness**. | **VERIFIED** (full English translation PDF fetched from mathnet.ru) | https://www.mathnet.ru/eng/sm2474 ; full text: `getFT.phtml?jrnid=sm&paperid=2474&what=fullteng` |

---

## 2. Exact statements recovered (verbatim)

### S01 — Oliveira-Smith, arXiv:2603.23717v1

> **Theorem 1.1.** The homotopy 4-sphere X_{DG} = E_{D_{K_B}} ∪_{ψ_{RBG}} \overline{X_0(K_G)} is diffeomorphic to S^4.
>
> **Corollary 1.1.1.** K_G is smoothly slice in B^4.
>
> **Corollary 1.1.2.** K_G is a potential counterexample to the Slice-Ribbon Conjecture.
>
> **Theorem 1.2.** The knot K_G bounds a fibered handle-ribbon disk in B^4.

Abstract: "…we show that the 18-crossing knot 18_{nh00000601}, **which is not known to be ribbon**, is slice in the standard 4-ball."

Intro: "While SnapPy was able to find a ribbon disk for the larger knot K_B, it was unable to find any such collection of bands for the much smaller knot K_G; thus leaving the sliceness of K_G unknown." … "**Since a ribbon disk for K_G has evaded detection, K_G would be a potential counterexample to the slice-ribbon conjecture.**"

Notation: K_G := 18nh00000601 (the small knot); K_B := the larger, *ribbon*, 0-surgery partner. Theorem 1.2 is proved in §3 "using work of Casson–Gordon, Meier–Zupan, and Miller–Zupan" via R-links, fibered homotopy-ribbon knots and derivative links. Numbered items: Thm 1.1, Cor 1.1.1, Cor 1.1.2, Thm 1.2, Lem 2.1, Lem 2.2 (Trace Embedding Lemma), Def 3.1, Thm 3.1, Cor 3.1.1, Lem 3.2, Thm 3.3.

**Bottom line for the package's load-bearing use:** the paper does *not* claim 18nh00000601 is non-ribbon, only that no ribbon disk has been found. A "fibered handle-ribbon disk" is strictly weaker than a ribbon disk, so Theorem 1.2 does **not** resolve the slice-ribbon question for this knot; if anything it makes a ribbon disk *more* plausible.

### S03 — Dunfield–Gong, arXiv:2512.21825v1

- Abstract: "There are **352.2 million** prime knots in the 3-sphere with at most **19 crossings**." Smooth sliceness determined for all but ≈11,400 (0.003%); topological for all but ≈1,400 (0.0004%); ≈1.6M (0.46%) smoothly slice/ribbon; ≈350.5M (99.54%) not topologically slice. **Theorem 1.1**: #K19 = 352,152,252; smoothly slice count ∈ [S, S+11,383] with S = 1,633,786; topologically slice ∈ [T, T+1429] with T = S + 22,412.
- **§2.7 "Obscure ribbon disks"** (the "suspicious knots" section): "This includes the **513** smoothly slice knots from the previous subsection, as well as **41** knots that are 0-friends with a ribbon knot by the method of Section 5. For these knots, we expanded the parameters of our search… **In all but one case, namely 18nh 00000601 from Theorem 1.12, we eventually found a ribbon disk.**"
- **Theorem 1.12**: "If 18nh 00000601 is not smoothly slice, or if any of {16n68278, 17nh 0010647, 18nh 00098198} are smoothly slice, then there is an exotic smooth 4-sphere." Followed by: "All four knots in Theorem 1.12 are topologically slice, and 18nh 00000601 is even smoothly slice in a homotopy 4-ball; see Theorem 5.14."
- **Table 5** ("The 25 fibered knots in PS19 whose slice status is not completely known"): row `18nh 00000601 | g₃ = 5 | smooth: — | top: n`-column note; the caption states "18nh 00000601 is topologically slice by Theorem 5.14. The genus of the fibered Seifert surface is listed for each knot." ⇒ **genus 5 and fibered, both confirmed.**
- Also verbatim: "Thus we have **identified no smoothly slice knots that are not known to be ribbon.** However, the knot K = 18nh 00000601 from Theorem 1.12 is intriguing… we tried very hard to find a ribbon disk for K to no avail. This makes K a plausible candidate for a knot that is smoothly slice but not ribbon."
- Also: "Of the topologically slice knots in Theorem 1.9, all but possibly 18nh 00000601 are in fact topologically homotopy ribbon."
- **§1.19 Code and data**: SnapPy, KnotJob, HFK Calculator, SageMath; "All data and code needed to check our results are permanently archived at [DG]" = **Harvard Dataverse, 2025**; key parts going into **SnapPy 3.3**. >100 CPU-years over 5 calendar years. PD codes for the 286 named knots included. **Not GitHub.**

### S02 — Miller–Zupan, arXiv:2005.11243, exact definitions

> **derivative**: "For a knot K ⊂ S³ and genus g Seifert surface F for [K], a *derivative* L for K in F is a g-component link such that L ⊂ F, F − L is a connected planar surface, and ℓk(L_i, L_j⁺) = 0 for all i,j, where L_j⁺ is a parallel copy of L_j pushed off of F."
>
> **R-link**: "An n-component link L ⊂ S³ is called an *R-link* if the manifold obtained by 0-surgery on each component of L is #ⁿ(S¹ × S²)."
>
> **handle-ribbon**: "A knot K ⊂ S³ is said to be *handle-ribbon* if K bounds a disk D in a homotopy 4-ball B such that the exterior of D can be built without 4-dimensional 3-handles." (= "strongly homotopy-ribbon" in [LM15, MZ19, HKP20]; see their Remark 2.2.)
>
> **Proposition 1.1.** A knot K ⊂ S³ is ribbon if and only if K has an unlink derivative U. *(stated as well-known; proof credited to [CD15])*
>
> **Conjecture 1.2** ([CD15], stable Kauffman conjecture). A knot K ⊂ S³ is slice if and only if K has a slice derivative L.
>
> **Theorem 1.3.** A knot K ⊂ S³ is handle-ribbon in a homotopy 4-ball if and only if K has an R-link derivative.
>
> **Theorem 1.4** ([CG83]). A fibered knot K ⊂ S³ is homotopy-ribbon in a homotopy 4-ball if and only if the fibration of the 0-surgery on K extends over handlebodies.
>
> **Theorem 1.5.** A knot K ⊂ S³ is handle-ribbon in a homotopy 4-ball if and only if there exists a singular fibration of the 0-surgery on K that extends over handlebodies. *(precise versions: Theorems 4.4 and 5.3)*

Note also: "Since every R-link is slice, it follows that handle-ribbon knots satisfy the stable Kauffman conjecture." And the GPRC (Kirby Problem 1.82) statement: "every R-link is handleslide equivalent to an n-component unlink."

### S09 — Agol–Ren, arXiv:2603.10884v1, exact numbering

> **Question 1.1** ([Gor81, Q 6.4]) simplicial volume; **Question 1.2** ([Gor81, Q 6.2]) descending chains; **Question 1.3** ([BS25, Q 1.1]) finiteness of predecessors.
> **Theorem 1.4.** If K is fibered and J ≤ K, then ‖S³∖J‖ ≤ ‖S³∖K‖.
> **Theorem 1.5.** If K is fibered and J ≤ K, then λ(J) ≤ λ(K).
> **Theorem 1.6.** If K is fibered, then there are finitely many J with J ≤ K.
> **Theorem 1.7 ([CG83]).** If J, K are fibered, then J admits a strongly homotopy-ribbon concordance to K in some homotopy I × S³ if and only if the monodromy of K compresses to that of J.
> **Theorem 1.8 ([CL85])** Casson–Long: (0) algorithm for nontrivial compression; (1)(2) finiteness/algorithm for minimal compressions of pseudo-Anosov φ.
> **Theorem 1.9.** (1) φ admits at most finitely many minimal compressions up to symmetries of (S, φ); (2) there is an algorithm to find all of them.
> **Corollary 1.10.** Every surface homeomorphism φ compresses to only finitely many φ′ (up to isotopy and conjugation); algorithm exists.
> **Corollary 1.11.** For any given fibered knot K, there are only finitely many knots J with J ≤_h K. Moreover, there is an algorithm to find all such J.
> **Theorem 1.13 / Corollary 1.14** (connected-sum characterization of ≤_h; slice-ribbon ⇒ ≤_h-minimal fibered representative unique; slice-ribbon + SPC4 ⇒ no fibered torsion of order > 2).
> **Question 1.15.** If K₁ and K₂ are concordant fibered knots, must there be a fibered knot K with K₁ ≤ K, K₂ ≤ K?

Independence notes in the paper: Theorems 1.4/1.5 obtained independently by **Baldwin–Sivek [BS25, Thm 1.5, Lem 2.6]**; Theorem 1.6 independently by **Baldwin–Hanselman–Sivek [BHS26, Cor 1.3]** (stronger: every knot has finitely many *fibered* ribbon predecessors). These two references should be in the package and were not flagged to me — worth adding as sources.

Direct relevance to 18nh00000601 (verbatim): "Corollary 1.11 in particular gives an algorithm to determine whether a fibered knot is strongly homotopy-ribbon in a homotopy B⁴. **Modulo the slice-ribbon conjecture and the smooth 4-dimensional Poincaré conjecture, this can in principle be used to determine the smoothly slice status of any fibered knot, in particular those in [DG25, Table 5]**."

Caution the package must respect: **Corollary 1.11's algorithm decides ≤_h (strongly homotopy-ribbon), not ribbonness.** It cannot by itself settle whether 18nh00000601 is ribbon.

---

## 3. S20 — Turaev 1983 "Theorem H" recovered in full

Fetched: mathnet.ru English translation PDF (27 pp., Math. USSR-Sb. 44(3) 1983, 335–361), text-extracted. The paper's theorem labels run **A, B, C, D, E, F, G, H, I, J**.

**Abstract (verbatim):** "On the fundamental group π of a Seifert surface A of a knot in the three-dimensional sphere, the author constructs, using the same scheme as for the Seifert form, a form πⁿ → Z, for n = 3, 4, …. The role of linking coefficient is played here by suitably chosen integral representatives of Milnor residues. It is shown that the form π³ → Z can obstruct **invertibility, ribbonness and two-sided null-cobordancy** of the knot ∂A (even when there is no obstruction by the Seifert form itself)."

**THEOREM H (verbatim, OCR of the English translation):**

> **THEOREM H.** Let K be an oriented knot in S³. Then:
> (i) The nil-form (l₁(−K), l₂(−K)), where the minus sign denotes change of orientation for the knot, is inverse to (l₁(K), l₂(K)); so that if the knot is invertible, then so is its nil-form (i.e., the latter is isomorphic to its own inverse).
> (ii) **If K is a ribbon knot, then F₂(l₁(K), l₂(K)) is metabolic.**
> (iii) If K is two-sidedly null-cobordant (see [13]), then F₂(l₁(K), l₂(K)) is hyperbolic.

Immediately following (verbatim): "The part of Theorem H that concerns l₁(K) is already known (see [7], [13] and [14]). **If K is of genus 1 or 2, then the nil-form F₂(l₁(K), l₂(K)) is determined up to isomorphism by the form F₁(l₁(K))**, and is invertible, metabolic or hyperbolic simultaneously with the latter (see §1.8). **For knots of genus ≥ 3, however, we can show that the conditions listed in Theorem H do not reduce to the same conditions on l₁(K).**"

**THEOREM I (verbatim, the realization/sharpness result):** for genus-3 Seifert surfaces A(p,q,r,s) built in §1.5 (with l₁(A) = matrix X hyperbolic, l₂(A)(x₁,x₃,x₅) = r, l₂(A)(x₂,x₄,x₆) = s):

> **THEOREM I.** Let p be either unity or a prime natural number, q a natural number, and r and s integers, with q ≠ 2 if p = 2. Let K = ∂A(p,q,r,s), and let L be an oriented (possibly trivial) knot in S³ whose Alexander polynomial is prime to that of K. Then: if r ≠ 0 and s ≠ 0, the nil-form F₂c(l₁(K#L), l₂(K#L)) **is not metabolic**; if r ≠ 0 or s ≠ 0, it is not hyperbolic; and if r = 0 and s ≠ 0, or if r ≠ 0 and s = 0, it is not invertible.

So Theorem H + Theorem I together give **explicit genus-3 knots that are algebraically slice (l₁ hyperbolic/metabolic) but provably NOT ribbon** by the trilinear obstruction. That is the operative ribbonness obstruction.

**CRITICAL CAVEAT — THEOREM J (verbatim):**

> "The following theorem shows that although slice knots are stably ribbon (see [17]),* **Theorem H yields no new obstructions to sliceness.**
> **THEOREM J.** If (l₁, l₂) is a special nil-form on a group of type (2, Q), with values in Q, and if the form l₁ is metabolic, then there exists a metabolic special nil-form (m₁, m₂) on a group of type (2, Q), with values in Q, such that the nil-form F₂((l₁,l₂) * (m₁,m₂)) is also metabolic."

(The footnote `*` is a translator's note correcting the translation of [17], p. 250: "an arbitrary slice knot, added with some ribbon knot, is ribbon.")

**Second critical caveat — what the proof of H(ii) actually uses (verbatim, §7.4):**

> "Part (ii) of the theorem follows from Lemmas 7.2 and 7.3 and the fact that **every ribbon knot K in S³ bounds a disk D in the ball B⁴ such that the inclusion homomorphism π₁(S³∖K) → π₁(B⁴∖D) is surjective** (see [3])."

⇒ Turaev's Theorem H(ii) is **really an obstruction to (homotopy-)ribbonness**, i.e. it obstructs the existence of a *π₁-surjective* slice disk. Combined with Theorem J, the honest characterization is:

- **It IS a genuine ribbon obstruction** in the sense that it can certify "not ribbon" for a knot with metabolic Seifert form (Theorem I).
- **It is NOT a tool for producing a slice-but-not-ribbon knot**, because (a) Theorem J says it adds nothing to slice obstructions after stabilization, and (b) it only obstructs via π₁-surjectivity, which every homotopy-ribbon disk supplies. A slice knot with a homotopy-ribbon disk will never be caught by Theorem H. For 18nh00000601 specifically, Oliveira-Smith's Theorem 1.2 gives it a **handle-ribbon** (hence homotopy-ribbon) disk, so **Turaev's Theorem H cannot obstruct its ribbonness.** This is the single most important consequence of the S20 recovery for the package's strategy.

**Later use of the multiplace form as a ribbon obstruction:** I could find **none**. Searches for restatements/uses by Kawauchi, Gilmer, Friedl, Orr, or anyone else returned no paper using Turaev's Theorem H as a ribbon obstruction. The only trace in the literature is the 2010 Low Dimensional Topology blog comment by **dmoskovich (2 Dec 2010, "Slice-Ribbon Conjecture in danger!")** citing "Theorem H of V. Turaev, *Multiplace generalizations of the Seifert form of a classical knot*, Math. USSR, Sb. **44**(3) (1983), 335–361" as "a completely different ribbon obstruction" and noting MathSciNet lists no citations for it. Status of "later restatement": **NOT FOUND** (strong negative evidence, not proof of absence).

Reference checked: https://ldtopology.wordpress.com/2010/12/02/slice-ribbon-conjecture-in-danger/ — the Turaev citation is in the comments, not in the post body. The package should cite it as a **comment by dmoskovich**, not as the blog post's claim.

---

## 4. Post-cutoff findings (2026-08-30 → 2026-09-11) and package gaps

**Method.** (i) arXiv API keyword queries on `slice-ribbon`, `slice ribbon conjecture`, `ribbon disk`, `handle-ribbon`, `18nh00000601`, `ribbon concordance`, `property R`, `annulus twist`, `GST link`, `ribbon knot`, `Dunfield`+`Gong`, sorted by submission date. (ii) A full dump of the most recent **600 math.GT entries**, spanning **2026-05-25 to 2026-09-10**, filtered for ribbon/slice/concordance/exotic keywords in title+abstract. (iii) Semantic Scholar citation graph for arXiv:2603.23717.

### (a) Any preprint proving 18nh00000601 ribbon — **NONE FOUND**
No arXiv math.GT submission between 2026-08-30 and 2026-09-10 mentions the knot, Dunfield–Gong, or the slice-ribbon conjecture. Semantic Scholar reports **exactly one** citation of arXiv:2603.23717, namely **arXiv:2604.17737 (Diao–Pan–Yan, S14)** — not a ribbonness resolution. The knot's ribbon status remains **open** as of 2026-09-11.

### (b) Any preprint proving a smoothly slice knot non-ribbon — **NONE FOUND**

### (c) New ribbon-specific obstruction — **NONE FOUND post-cutoff**. (Within the window May–Aug 2026, the closest are the immersed-curve minimum-height invariant of Hom–Park S10 and the singular-instanton method of S11, both obstructing *ribbon concordance*, not ribbonness-vs-sliceness.)

### (d) New certified smoothly-slice non-obviously-ribbon knots — **NONE FOUND**

### Papers the package appears to have MISSED (all pre-cutoff, all math.GT, all ribbon-relevant)

| arXiv | date | authors | title | one-line | label |
|---|---|---|---|---|---|
| 2607.14030 | 2026-07-15 | Benjamin Daniels | *Braid closure union braid axis is ribbon concordance minimal* | A ribbon-concordance-minimal fibered knot K generates ribbon-concordance-minimal links by adding any braid closure in S³∖K; any link can be made ribbon concordance minimal by adding one linked unknot. | PARTIALLY VERIFIED (abstract) |
| 2606.20802 | 2026-06-18 | Gary Dunkerley | *A ribbon partial order for links and minimality detection via Heegaard Floer* | Strong ribbon concordance is a partial order on links (extends Agol); certifies ribbon-minimality for some knots via knot Floer; first examples of ribbon minimal knots that are not [fibered/…]. | PARTIALLY VERIFIED (abstract) |
| 2606.02968 | 2026-06-02 | Michel Boileau, Teruaki Kitano, Yuta Nozaki | *A ribbon knot which is not a symmetric union* | Negative answer to the open question whether every ribbon knot is a symmetric union, via a ribbon Montesinos knot. **Directly relevant**: kills "symmetric union" as a universal certificate for ribbonness. | PARTIALLY VERIFIED (abstract) |
| 2606.02390 | 2026-06-01 | Akash, Corrado, Placke, Sanketh | *Symmetric ribbon numbers of low-complexity knots* | Computes the symmetric ribbon number r_s(K); background on Lamm's open problem (immersed ribbon disk ⇒ symmetric union?). | PARTIALLY VERIFIED (abstract) |
| 2607.04018 | 2026-07-04 | Jacob Migdail, Stephan Wehrli | *A module structure on odd Khovanov homology and the odd invariant for ribbon 2-knots* | Module structure on reduced odd Khovanov homology; odd invariant for ribbon 2-knots. Peripheral. | PARTIALLY VERIFIED (abstract) |
| (cited inside S09) | 2025–2026 | Baldwin–Sivek [BS25]; Baldwin–Hanselman–Sivek [BHS26] | — | Independent proofs of Agol–Ren Thms 1.4/1.5 (BS25) and of Thm 1.6, in the stronger form "every knot has finitely many fibered ribbon predecessors" (BHS26, their Cor 1.3). | UNVERIFIED (known only from S09's bibliography; arXiv IDs not resolved in this audit) |

### Negative results worth recording
- arXiv:2603.23717 has **no v2** as of 2026-09-11 (single version, 24 Mar 2026), despite the paper's internal date line reading "August 24, 2026".
- arXiv:2512.21825 has **no v2**.
- arXiv:2603.10884 has **no v2**.
- arXiv:2604.21240 (Xiao) is at **v3** (18 Aug 2026) — the package should pin a version.
- No GitHub repository for Dunfield–Gong exists per the paper; the archive is **Harvard Dataverse** and the toolchain lands in **SnapPy 3.3**.

---

## 5. Recommended corrections to the package

1. Add **Corollary 1.1.2** of S01; stop folding the slice-ribbon consequence into Cor 1.1.1.
2. Stop attributing **Agol–Ren Thm 1.7** and **Miller–Zupan Thm 1.4** to those authors — both are **Casson–Gordon [CG83]**. The Miller–Zupan new result is **Thm 1.5**.
3. Delete the claim that Agol–Ren address ribbon (non-homotopy-ribbon) disks or the question "every ribbon disk of a fibered knot is fibered" — **not in the paper**.
4. Replace "554 suspicious knots" with "513 + 41 = 554 (numbers as printed in §2.7; the total is not stated in the paper)".
5. Replace "GitHub repo" with "Harvard Dataverse archive [DG]; code merged into SnapPy 3.3".
6. Re-characterize **S11** (unknotting number), **S12** (real link Floer homology), **S13** (extending quotients over surfaces in B⁴) — none is a slice-ribbon or ribbon-vs-slice source.
7. Record the S20 caveat: Turaev's Theorem H(ii) obstructs via π₁-surjectivity and Theorem J says it gives **no new sliceness obstruction**; it therefore **cannot** obstruct ribbonness of 18nh00000601, which is handle-ribbon by S01 Thm 1.2.
8. Cite the Turaev "Theorem H" pointer as a **2010-12-22 comment by dmoskovich** on the ldtopology post, not as the post itself.
