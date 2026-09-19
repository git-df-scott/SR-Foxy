# Adversarial memo: before you hunt a Slice–Ribbon counterexample, read the graveyard

**To:** SR-Foxy counterexample team
**From:** skeptical senior topologist (adversarial reviewer role)
**Date:** 2026-09-11
**Subject:** Why every previous "slice but probably not ribbon" family died, what the belt-sphere/Andrews–Curtis heuristic actually says, and an honest probability estimate

**Evidence labels used throughout.**
- **VERIFIED** — I read the primary source text (or this repo's prior audit did, with the theorem number recorded) and the claim is stated there.
- **PARTIALLY VERIFIED** — the claim is stated in a secondary or search-derived source, or I read an abstract/metadata but not the theorem text.
- **UNVERIFIED** — reported as folklore, hearsay, or blog-level; not to be cited as fact.

Nothing in this memo is a quote unless it appears between quotation marks with a source. I have invented no papers, no theorem numbers, and no quotations. Where I could not recover a text I say so.

---

## 0. Standing terminology (read this first; half the graveyard is terminological)

For a knot $K \subset S^3$:

$$\text{ribbon} \Rightarrow \text{handle-ribbon} \Rightarrow \text{homotopy-ribbon} \Rightarrow \text{slice}$$

- **ribbon**: bounds a slice disk $D \subset B^4$ with no index-2 critical points of the radial/height function; equivalently bounds an immersed disk in $S^3$ with only ribbon singularities. (Definition as printed in Oliveira-Smith, arXiv:2603.23717v1, §1. **VERIFIED**)
- **handle-ribbon** (= *strongly homotopy-ribbon*): bounds a disk $D$ in a homotopy 4-ball $B$ such that the exterior of $D$ can be built without 4-dimensional 3-handles. (Miller–Zupan, arXiv:2005.11243, §1. **VERIFIED**, including their explicit remark that "handle-ribbon" and "strongly homotopy-ribbon" name the same condition and that they prefer the former.)
- **homotopy-ribbon**: bounds a disk with $\pi_1(S^3\setminus K) \twoheadrightarrow \pi_1(B^4\setminus D)$ surjective. (Standard; used in this sense by Dunfield–Gong §1.17, **VERIFIED**.)
- **derivative**: for a genus-$g$ Seifert surface $F$, a $g$-component link $L \subset F$ with $F - L$ connected planar and $\ell k(L_i, L_j^+) = 0$. (Miller–Zupan §1. **VERIFIED**.)

Two characterizations that structure this whole memo:

- **Prop. 1.1 (Miller–Zupan, attributed there to Cochran–Davis [CD15]):** *$K$ is ribbon iff $K$ has an **unlink** derivative.* **VERIFIED** (read in arXiv:2005.11243 §1).
- **Thm. 1.3 (Miller–Zupan):** *$K$ is handle-ribbon **in a homotopy 4-ball** iff $K$ has an **R-link** derivative* ($L$ with 0-surgery $= \#^n(S^1\times S^2)$). **VERIFIED**.

Note the quantifier in Thm 1.3: *in a homotopy 4-ball*. That caveat is a live trap (§6).

---

## 1. History of dead candidates, 1962–2026

Fox posed the problem in 1962 ("Some problems in knot theory", Proc. Georgia Institute 1961, published 1962 — the citation Oliveira-Smith gives as [FOX61]; **VERIFIED** as a reference, not read). Every publicly floated counterexample family since has died in one of four ways:

- **(A) shown ribbon** (band movie eventually found, or a handle-calculus proof);
- **(B) shown not slice** (so it was never a candidate);
- **(C) shown slice only in a homotopy ball, which was later standardized — and in the same breath ribbon-ness got proved**;
- **(D) never actually a candidate** — a terminological or logical confusion (e.g. non-ribbon proved but sliceness never was).

### 1962–1980: the prehistory

**1978 — Kirby–Melvin, "Slice knots and property R", Invent. Math. 45 (1978), 57–59.** **VERIFIED** (I read the full 3-page paper). Their theorem: if 0-framed 2-handle attachment along $K$ gives $\partial M \cong S^2\times S^1$, then (1) $K$ is slice and (2) $M \cong_{\text{homeo}} S^2\times B^2$. The Addendum (credited to Taylor and Freedman) strengthens (1): such a $K$ is a **"symmetric slice of the unknot"** — the intersection of the standard $S^3$ with an unknotted reflection-invariant $S^2 \subset S^4$. They cite Gordon–Sumners for the consequence that the infinite cyclic cover is acyclic, so $\Delta_K = 1$.

*Why this matters to us and why it is not a candidate source:* this was the original "slice for a 4-dimensional reason, with no band movie in sight" mechanism, and it is the direct ancestor of everything below (the Trace Embedding Lemma is the same idea). But Gabai's Property R theorem later made the hypothesis vacuous ($K$ must be the unknot). **Death mode: (D)/(B) — vacuous**. What survived is the *method*, not a candidate.

### 1985–1991: Akbulut–Kirby, and Gompf's kill

**1985 — Akbulut–Kirby, "A potential smooth counterexample in dimension 4 to the Poincaré conjecture, the Schoenflies conjecture and the Andrews–Curtis conjecture", Topology 24 (1985).** **PARTIALLY VERIFIED** (title/venue confirmed by search; I did not read the paper). The Akbulut–Kirby homotopy 4-sphere was built from a balanced presentation of the trivial group believed Andrews–Curtis nontrivial. Knots arising as belt spheres / attaching circles in such diagrams are exactly the "slice in a homotopy ball, no visible bands" shape.

**1991 — Gompf, "Killing the Akbulut–Kirby 4-sphere, with relevance to the Andrews–Curtis and Schoenflies problems", Topology 30 (1991), 97–115.** **VERIFIED as a citation** (confirmed independently in the Abe–Tange reference list as [G1] and in search; I did not read the full text). Gompf standardized the Akbulut–Kirby sphere. **Death mode: (C)** — the exotic ambient evaporated.

*Adversarial lesson #1, and it is the single most important lesson in this memo:* the Akbulut–Kirby episode establishes the base rate. A construction whose only claim to "probably exotic / probably not ribbon" is *"the associated balanced presentation looks Andrews–Curtis hard"* has, historically, standardized. Note the irony that Gompf's own 1991 handlebodies $H_{n,k}$ are the ones later reused to build the GST links (**VERIFIED**: Abe–Tange §6 explicitly identifies $H_{n,k}$ "given by Gompf [G1]" as the source of $L_{n,k}$).

### 1994–1995: Gompf–Miyazaki — the canonical "well-disguised ribbon" warning

**Gompf–Miyazaki, "Some well-disguised ribbon knots", Topology and its Applications 64 (1995), 117–131** (received 1991, revised 1992 and 1994). **PARTIALLY VERIFIED** (I could not retrieve the full text — ScienceDirect returned HTTP 403 — but the abstract content is consistent across two independent retrievals). Two results, and they point in *opposite* directions:

1. They construct satellite-type knots that bound smooth disks in $B^4$ and are **not obviously ribbon**, then prove they **are** ribbon. **Death mode (A)** for that family — and the title is a deliberate warning label.
2. They exhibit a connected sum $J(O)\#J^*(O)$ that is **non-ribbon** while **all then-known algebraic obstructions to sliceness vanish**. This is **not** a counterexample: non-ribbon was proved, sliceness was not. **Death mode (D)** for counterexample purposes.

*Lesson #2:* "I can't find bands" has a 30-year track record of being wrong, and the people who know this best are the ones who wrote the title.

*Related, same circle of ideas:* **Rudolph, "A non-ribbon plumbing of fibered ribbon knots", arXiv:math/0105257 (2001)** — an example of Livingston–Melvin later studied by Miyazaki, showing a plumbing of two fibered ribbon knots along fiber surfaces can be **algebraically slice yet not ribbon**. **PARTIALLY VERIFIED** (abstract read). Again Tier B: non-ribbon, sliceness unproved. *Flag:* one search summary I received mis-stated the Slice–Ribbon Conjecture as "every algebraically slice knot is ribbon". That is **false** and must never enter our writeups.

### 2009–2010: Cappell–Shaneson spheres get standardized

**Akbulut, "Cappell–Shaneson homotopy spheres are standard", Ann. of Math. 171 (2010), 2171–2175** (**VERIFIED as a citation**, appears in both Abe–Tange's and Oliveira-Smith's reference lists) and **Gompf, "More Cappell–Shaneson spheres are standard", Algebr. Geom. Topol. 10 (2010), 1665–1681** (**VERIFIED as a citation**, same lists; abstract **PARTIALLY VERIFIED**: Gompf shows a strictly larger family standard, uses "no Kirby calculus except through the relatively simple 1979 paper of Akbulut and Kirby", exploits hidden symmetries of the Cappell–Shaneson construction, and shows Gluck twists can sometimes be undone using symmetries of fishtail neighborhoods).

Consequence for us: the CS-derived knots — knots slice in a CS homotopy ball — became knots slice in $B^4$. Whether any of them are *known ribbon* is **UNVERIFIED** and family-dependent; the honest statement is that the exotic-ambient escape hatch closed. **Death mode: (C)**, partially.

*Note* — GST explicitly harvest this: "In light of Akbulut's recent work [Ak], more complicated potential counterexamples can also be generated by this same method; cf. [FGMW]." **VERIFIED quote** (arXiv:1103.1601, §8). [FGMW] = Freedman–Gompf–Morrison–Walker, *Man and machine thinking about the smooth 4-dimensional Poincaré conjecture*, Quantum Topol. 1:2 (2010), 171–208.

### 2010: GST — the flagship family, and exactly what is and is not dead

**Gompf–Scharlemann–Thompson, "Fibered knots and potential counterexamples to the Property 2R and Slice–Ribbon Conjectures", Geom. Topol. 14 (2010), 2305–2347; arXiv:1103.1601.** I read the extracted text. All of the following are **VERIFIED verbatim quotes**:

- Abstract: *"These links can be used to generate slice knots that are not known to be ribbon."* Note the wording: *not known to be*, not *not*.
- §1: *"We show in Section 7 that $L_{n,1}$ is a counterexample to the Generalized Property R Conjecture **provided that** the presentation $\langle x,y \mid yxy=xyx,\ x^{n+1}=y^n\rangle$ of the trivial group is Andrews–Curtis nontrivial, as is deemed likely by group theorists when $n\ge3$."*
- §1: *"For $n \ge 3$ there is no apparent reason for the resulting knots to be ribbon. Thus, we obtain potential counterexamples to the Slice–Ribbon Conjecture. This appears to be the only known method for constructing such examples."*
- §1, caption: Figure 2 is *"A slice knot that might not be ribbon"*, obtained from $L_{3,1}$ by the band move along the dotted arc of Figure 1.
- §8: *"Since the pictured 4-manifold is actually diffeomorphic to a 4-ball [Go1], it follows that $L_{n,k}$ is smoothly slice."* — **so the ambient here is standard $B^4$, constructively.**
- §8: *"The authors do not know whether $L_{n,k}$ is ribbon except in the special cases $n = 0, 1$ or $k = 0$ or $(n,k) = (2,1)$."* — **these are the known-ribbon cases, and GST say why: "In each of the special cases, the corresponding presentation is Andrews–Curtis trivial. (This is clear except for the last case, which is due to Gersten [Ge]...)"**, and they reproduce Gersten's trivialization of $\langle x,y \mid yxyx^{-1}y^{-1}x^{-1},\ x^3y^{-2}\rangle$ explicitly at the end of §8.
- §8, the mechanism of failure: *"In general, each component of $L_{n,k}$ is ribbon... Unfortunately, the individual ribbon disks seem to interfere with each other."* And: *"it seems likely that the 2-3 handle pair needed for canceling the handlebody creates troublesome local maxima. On the other hand, the given slice disks have the unusual property that their complement is a regular neighborhood of a wedge of two circles; perhaps there is a pair of ribbon disks whose complement has more complicated fundamental group."*
- §8, the open questions, stated as questions: *"For $n \ge 2$, $k \ne 0$ and $(n,k)\ne(2,1)$, is $L_{n,k}$ a ribbon link? Are the slice knots made by band-summing its components always ribbon? Are they ever ribbon?"*

**Status: LIVE but badly weathered.** Nothing has shown a GST band sum non-ribbon. What *has* happened to the program:

- **Scharlemann, "Proposed Property 2R counterexamples classified", arXiv:1208.1299 (2012).** **PARTIALLY VERIFIED** (abstract only; I could not extract theorem text). It resolves how the family $L_n$ fits the classification of 2-component links containing the square knot that surger to $\#^2(S^1\times S^2)$. I found **no statement** there about slice-ribbon status. Do not over-claim this one.
- **Gukov–Halverson–Manolescu–Ruehle, "Searching for ribbons with machine learning", arXiv:2304.09304; Machine Learning: Sci. Tech. (2025).** The load-bearing sentence, **VERIFIED** from the v2 HTML: *"The first two links in the GST family ($L_{1,1}$ with 18 crossings and $L_{2,1}$ with 40 crossings) were already known to be ribbon (see [GST10b]), but unfortunately our algorithms could not find bands to prove they are ribbon."* They also could not handle *"other GST examples from [GST10b], such as $L_{3,1}$ and the slice knot associated to it."* **This is the single most important calibration fact in the entire memo: their search failed on links that are provably ribbon.** Their search failure on $L_{3,1}$ therefore carries essentially zero Bayesian weight. (They did rule out many SPC4 candidates: of 3,375 RBG knot pairs, *"only two could still potentially produce counterexamples to SPC4"* — **VERIFIED** from the same fetch.)
- **Diao–Pan–Yan, "Some experimental results on stable equivalence of GST links", arXiv:2604.17737 (2026).** **PARTIALLY VERIFIED** via this repo's prior audit ([S14], Thm 1.1): finite ranges of **stable** handleslide equivalence. Stable $\ne$ ordinary; this is not a ribbon disk for any unstabilized band sum.

### 2011–2015: Omae / Abe–Jong–Omae–Takeuchi / Abe–Tange — the cleanest (C)-then-(A) death

**Abe–Jong–Omae–Takeuchi, Math. Proc. Camb. Phil. Soc. 155 (2013), 219–235**, constructed $K_n$ from a slice knot $K$ with an annulus presentation by $n$-fold annulus twist; they proved $K_n$ bounds a smooth disk **in a homotopy 4-ball $W(K_n)$**, not in $B^4$. **VERIFIED** from Abe–Tange arXiv:1305.7492v4 §1, which quotes the open Question: *"Is $W(K_n)$ diffeomorphic to the standard 4-ball $B^4$?"*

Then **Abe–Tange, "A construction of slice knots via annulus twists", arXiv:1305.7492v4 (2015)** killed it twice over. **VERIFIED verbatim:**
- **Theorem 3.1:** *"Let $K$ be a ribbon knot admitting an annulus presentation and $K_n$ ($n\in\mathbb{Z}$) the knot obtained from $K$ by the $n$-fold annulus twist. Then the homotopy 4-ball $W(K_n)$ associated to $K_n$ is diffeomorphic to $B^4$."* — **death mode (C)** for the exotic hope.
- **Theorem 5.4:** *"The slice knot $K_n$ ($n\ge0$) is ribbon."* (the $8_{20}$-based Omae family) — **death mode (A)**. They even produce an explicit ribbon presentation (their Figure 27) after "rather long" handle calculus, noting "Keeping track of $K_n$ through the handle calculus, though it is rather troublesome".
- The tool, **Lemma 5.1**, is the one to internalize: *"Let $HD$ be a handle diagram of $B^4$. Suppose that $HD$ is changed into the empty handle diagram of $B^4$ by handle slides, adding or canceling 1/2-handle pairs, and isotopies. Then the belt sphere of any 2-handle of $HD$ is a ribbon knot."*

This is the archetype: a family that looked non-ribbon for years, killed by a long but finite handle calculus. **Note the scope caveat**: Thm 5.4 covers $n\ge0$. This repo's ledger correctly records that the $8_{20}$ family is closed *in that range*.

### 2015: Abe–Tagami — a Tier B lane, still alive, still not a candidate

**Abe–Tagami, "Fibered knots with the same 0-surgery and the slice-ribbon conjecture", arXiv:1502.01102v5.** Via this repo's prior audit ([S06], **PARTIALLY VERIFIED** at theorem-number level): with $K_n = A_n(6_3)$, Miyazaki's Thm 5.5 (Trans. AMS 341, 1994) via their Cor. 4.3 forces fibered summands of a ribbon signed connected sum to pair, so $D_{n,m}=K_n\#(-K_m)$ is **non-ribbon** for admissible distinct pairs. Sliceness of $D_{n,m}$ is equivalent to $[K_n]=[K_m]$ in smooth concordance and **has never been proved**. **Death mode (D)** — as a *counterexample*, it is not a candidate; as a *lane*, it is live and it has the cleanest logical shape of anything on the board.

Also recorded via search (**PARTIALLY VERIFIED**): GST/Abe–Tagami show that *if* Slice–Ribbon is true *then* the modified Akbulut–Kirby conjecture ("knots with the same 0-surgery are concordant") is **false**. That is a genuine structural tension worth exploiting in either direction — but it cuts *against* naive 0-surgery-based candidate generation (§6).

### 2021–2024: Manolescu–Piccirillo and its shredding

**Manolescu–Piccirillo, "From zero surgeries to candidates for exotic definite four-manifolds", arXiv:2102.04391; J. LMS (2023).** **PARTIALLY VERIFIED**: by computer search they produced pairs of knots with the same 0-surgery, including **5 topologically slice knots such that if any were slice one would get an exotic $S^4$**.

**Nakamura, "Trace embeddings from zero surgery homeomorphisms", arXiv:2203.14270; J. Topology (2023).** **PARTIALLY VERIFIED**: Nakamura shows those knots are **not slice**, and that the techniques extend to the entire infinite family of MP zero-surgery homeomorphisms — while not completely ruling out the MP program. **Death mode (B)**.

*Lesson #3:* the MP machine is a **candidate generator with a high infant-mortality rate**, and the killer was a sliceness obstruction, not a ribbon obstruction.

### 2022–2024: Kawauchi's $(2,1)$-cable of the figure-eight

**PARTIALLY VERIFIED**: Kawauchi posed the $(2,1)$-cable of $4_1$ as one of the simplest potential Slice–Ribbon counterexamples. **Dai–Kang–Mallick–Park–Stoffregen, "The $(2,1)$-cable of the figure-eight knot is not smoothly slice", arXiv:2207.14187; Invent. Math. (Nov 2024)** proved it not smoothly slice (via its branched double cover bounding no equivariant homology ball). **Death mode (B)**.

Quanta covered this; the only on-record opinions I can verify from that article are in §2(d) below. Also note **Kawauchi, "Ribbonness of Kervaire's sphere-link in homotopy 4-sphere and its consequences to 2-complexes", arXiv:2212.02617 (2022, rev. 2024)**, whose abstract (**VERIFIED verbatim**) reads: *"In the use of the smooth unknotting conjecture and the smooth 4D Poincaré conjecture, any such sphere-link is shown to be a sublink of a free ribbon sphere-link in the 4-sphere."* — i.e. **conditional on two open conjectures**, and unrefereed. Treat as **UNVERIFIED** for any load-bearing use.

### 2024–2026: Calegari spheres, Dunfield–Gong, and the current frontier

- **Cha–Kim, "Calegari's homotopy 4-spheres from fibered knots are standard", arXiv:2411.10051 (cited as [CK26] by Oliveira-Smith).** **PARTIALLY VERIFIED** (citation only). Another family of homotopy spheres standardized. **Death mode (C)** for whatever candidates it supported.
- **Dunfield–Gong, "Ribbon concordances and slice obstructions: experiments and examples", arXiv:2512.21825v1 (26 Dec 2025).** I read the extracted text; the following are **VERIFIED**:
  - §1.17: *"we discovered more than 500 smoothly slice knots where repeated passes of our ribbon disk search had come up empty. However, we eventually found ribbon disks for all of them... Thus we have identified no smoothly slice knots that are not known to be ribbon."*
  - §2.7: the suspicious set is **513 + 41 = 554** (513 knots shown slice by connected-sum-with-$J$ tricks in §2.6, plus 41 that are 0-friends with a ribbon knot): *"In all but one case, namely $18_{\mathrm{nh}}00000601$ from Theorem 1.12, we eventually found a ribbon disk."*
  - The self-calibration, and it is brutal: *"Based on the success rate of the expanded search as compared to that of the original search, we expect there are hundreds of other similarly obscure ribbon disks among the 11,383 knots in $\mathcal{PS}_{19}$ whose smooth slice status is unknown."*
  - **Theorem 1.12 (verbatim):** *"If $18_{\mathrm{nh}}00000601$ is not smoothly slice, or if any of $\{16n68278, 17_{\mathrm{nh}}0010647, 18_{\mathrm{nh}}00098198\}$ are smoothly slice, then there is an exotic smooth 4-sphere."* Followed by: *"All four knots in Theorem 1.12 are topologically slice, and $18_{\mathrm{nh}}00000601$ is even smoothly slice in a homotopy 4-ball; see Theorem 5.14."*
  - §1.17, their own verdict on our target: *"we tried very hard to find a ribbon disk for $K$ to no avail. This makes $K$ a plausible candidate for a knot that is smoothly slice but not ribbon."*
  - **Death mode for the other 553: (A).** That is a 553/554 kill rate on the exact heuristic we are relying on.
- **Oliveira-Smith, "A Dunfield–Gong 4-Sphere is Standard", arXiv:2603.23717v1 (24 Mar 2026).** I read the extracted HTML. **VERIFIED**: Theorem 1.1 ($X_{DG}\cong S^4$), Corollary 1.1.1 ($K_G = 18_{\mathrm{nh}}00000601$ is smoothly slice in $B^4$), Corollary 1.1.2 (it is a potential counterexample), **Theorem 1.2** (*"The knot $K_G$ bounds a fibered handle-ribbon disk in $B^4$"*), and the closing text: *"Although we have exhibited a fibered handle-ribbon disk $D_{K_G}$ for $K_G$ through a trace embedding, we were unable to show that $D_{K_G}$ is ribbon."* His two closing questions are **Question 3.3** (is $D_{K_G}$ ribbon?) and **Question 3.4** (is $K_G$ ribbon?). Genus five, fibered, verified with `knot_floer_homology()` in SnapPy.

  **Note the (C)-shaped irony:** Oliveira-Smith's standardization is precisely the move that killed Akbulut–Kirby, Cappell–Shaneson, Omae and Calegari — except here it *promoted* the candidate instead of killing it, because the exotic-ambient hope and the non-ribbon hope were attached to *different* knots of the 0-friend pair. That asymmetry is the only reason `DG` is still standing.

### Summary table

| Family | Proposed | Status | Death mode |
|---|---|---|---|
| Kirby–Melvin $\partial = S^2\times S^1$ knots | 1978 | vacuous after Gabai | (D)/(B) |
| Akbulut–Kirby sphere knots | 1985 | Gompf 1991 standardized | (C) |
| Gompf–Miyazaki satellites | 1991–95 | proved ribbon by the authors | (A) |
| Gompf–Miyazaki $J(O)\#J^*(O)$ | 1995 | non-ribbon, sliceness never proved | (D) |
| Livingston–Melvin/Miyazaki/Rudolph plumbing | 2001 | alg. slice + non-ribbon; sliceness unproved | (D) |
| Cappell–Shaneson-derived | 1976–2010 | Akbulut 2010, Gompf 2010 standardized | (C) |
| GST $L_{n,k}$, $n\le1$ or $k=0$ or $(2,1)$ | 2010 | ribbon (AC-trivial, Gersten for $(2,1)$) | (A) |
| GST $L_{n,k}$, $n\ge2,k\ne0,(n,k)\ne(2,1)$ | 2010 | **LIVE**, untouched; ML searches uninformative | — |
| Omae / AJOT annulus-twist $K_n$ | 2011–13 | Abe–Tange: $W\cong B^4$ and ribbon ($n\ge0$) | (C) then (A) |
| Abe–Tagami $A_n(6_3)\#(-A_m(6_3))$ | 2015 | non-ribbon proved; slice unproved | (D), lane live |
| Manolescu–Piccirillo 5 knots | 2021 | Nakamura: not slice | (B) |
| Kawauchi $(2,1)$-cable of $4_1$ | ~2022 | DKMPS 2024: not smoothly slice | (B) |
| Calegari fibered-knot spheres | 2009 | Cha–Kim 2026 standardized | (C) |
| Dunfield–Gong 553 of 554 | 2025 | ribbon disks found | (A) |
| Hom–Park Cor. 1.3 knots | 2025/26 | non-ribbon proved; only alg. slice | (D) |
| **$18_{\mathrm{nh}}00000601$** | 2025/2026 | **LIVE — smoothly slice in $B^4$, fibered handle-ribbon, ribbon status open** | — |

**Bottom line of §1: in 64 years, the number of knots proved smoothly slice in standard $B^4$ and proved non-ribbon is zero.** Every claimed candidate either got a band movie, lost its sliceness, or lost its exoticity. This is not an argument that Slice–Ribbon is true; it is an argument that our prior on *any specific* candidate being the counterexample should be low and that our prior on *searches* is close to worthless.

---

## 2. The belt-sphere heuristic and Andrews–Curtis

### (a) Ribbon disks $\leftrightarrow$ 2-complexes $\leftrightarrow$ balanced presentations

The dictionary, as GST state it in §7 (**VERIFIED verbatim, lightly compressed**):

> *"Suppose $L$ is an $n$-component framed link that satisfies the hypothesis of Generalized Property R. Then surgery on $L$ yields $\#^n(S^1\times S^2)$, whose fundamental group $G$ is free on $n$ generators. Its basis $\{g_i\}$ is unique up to Nielsen moves. If we pick a meridian of each component of $L$... we obtain $n$ elements $\{r_i\}$ that normally generate $G$... Thus, we have a presentation $\langle g_1,\cdots,g_n \mid r_1,\cdots,r_n\rangle$ of the trivial group. Changing our choices in the construction changes the presentation by Andrews–Curtis moves. ... Thus, the link $L$ up to handle slides determines a balanced presentation of the trivial group up to Andrews–Curtis moves."*

And the frank admission that this is presently a **non-invariant**:

> *"Unfortunately, there is presently no way to distinguish Andrews–Curtis equivalence classes from each other. When such technology emerges, it should be able to distinguish handle-slide equivalence classes of links satisfying the hypothesis of Generalized Property R, such as the links $L_{n,k}$."* (**VERIFIED verbatim**, GST §7.)

Read that twice. **The entire "probably not ribbon" case for GST rests on an invariant that does not exist.** The AC-hardness belief is expert intuition about a presentation, not a computation of anything.

### (b) Abe–Tange Conjecture 6.1

**VERIFIED verbatim** (arXiv:1305.7492v4 §6):

> **Conjecture 6.1.** *"Let $HD$ be a handle diagram of $B^4$ without 3-handles. Then the belt-sphere of any 2-handle of $HD$ is a ribbon knot."*

> **Conjecture 6.2.** *"There exists a handle diagram $HD$ of $B^4$ without 3-handles such that we always have to add canceling 2/3-handle pairs when we change $HD$ into the empty handle diagram $B^4$ by a sequence of handle slides, adding or canceling handle pairs, and isotopies."*

with the immediately following sentence (**VERIFIED**): *"A promising candidate to Conjecture 6.2 is the handle diagram $H_{n,k}$ of $B^4$ given by Gompf [G1] (see the left half of Figure 28), where $n\ge3$ and $k\ne0$."*

And the punchline (**VERIFIED verbatim**): *"Each Gompf, Scharlemann and Thompson's slice knot is obtained from $L_{n,k}$ by attaching an arbitrary band. After a single 2-handle slide (along the band), it turns out that the slice knot is isotopic to the belt-sphere of a 2-handle of a certain handle diagram of $B^4$ without 3-handles. Therefore, if Conjecture 6.1 is true, these slice knots are also ribbon. In this sense, to solve Conjecture 6.1 is the first step toward an affirmative answer to the slice-ribbon conjecture."*

Their converse remark (**VERIFIED**, Remark 5.3): every ribbon knot *is* the belt sphere of a 2-handle in a $0,1,2$-handle decomposition of $B^4$ — so Conjecture 6.1 is exactly the converse direction.

**Adversarial reading.** Conjecture 6.1 is a *pro-Slice–Ribbon* conjecture that implies **both** the entire GST family **and** the entire Abe–Tange Thm 3.1 family are ribbon. Conjectures 6.1 and 6.2 are not formally in conflict (6.2 says the 2/3-pair is sometimes unavoidable in the *calculus*, not that the belt sphere is non-ribbon), but they pull in opposite directions in practice: Lemma 5.1 is the only proof technique we have for 6.1, and it requires exactly the 2/3-pair-free trivialization that 6.2 says can fail.

### (c) Andrews–Curtis and Generalized Property R

The logical chain, kept honest:

$$\text{framed link handleslide-trivializes} \ \Longrightarrow\ \text{band sums ribbon}$$
$$\text{band sum ribbon} \ \not\Longrightarrow\ \text{framed link handleslide-trivializes}$$

The first implication is GST §8 (**VERIFIED**: "Both conditions are preserved by (0-framed) handle slides... Band-summing link components to create a knot similarly preserves both conditions"). **The converse is not proved anywhere I could find.** This is precisely the "GST ribbon-completeness theorem" this repo's `GST_AUDIT.md` correctly identifies as missing. Consequently:

**Failure of Generalized Property R for $L_{n,k}$ would NOT prove any band sum non-ribbon.** Anyone on this team who writes otherwise has committed the central logical error of the field. Even a full disproof of the Andrews–Curtis conjecture for $\langle x,y \mid yxy=xyx,\ x^{n+1}=y^n\rangle$ would leave Slice–Ribbon completely untouched.

**Live 2026 development, cutting against us:** **Lackenby, "The stable Andrews–Curtis conjecture and thickenable presentations of the trivial group", arXiv:2606.06122 (4 June 2026)** (**PARTIALLY VERIFIED**, abstract only, unrefereed): an explicit upper bound on the number of stable AC moves converting *thickenable* balanced presentations to the standard one, plus a proof that *thickenable* balanced presentations satisfy the **unstable** AC conjecture. If the GST presentations are (or can be made) thickenable, the "AC-hard, therefore probably non-ribbon" story weakens further. **Action item: check thickenability of $\langle x,y\mid yxy=xyx,\ x^{n+1}=y^n\rangle$ against Lackenby's definition. I have not done this and cannot assert either way.**

### (d) What topologists actually say, with sources, and nothing invented

**GST themselves, on Generalized Property R** — **VERIFIED verbatim**, arXiv:1103.1601 abstract/§1:
> *"We conclude that the conjecture is probably false, and analyze potential counterexamples."*
> *"We exhibit a family of such links that are probably counterexamples to Generalized Property R."*

Note carefully: this is their opinion about **Generalized Property R**, not about Slice–Ribbon. On Slice–Ribbon their language is consistently conditional: "not known to be ribbon", "might not be", "no apparent reason", and §8 ends in **questions**, not assertions. **Do not quote GST as predicting Slice–Ribbon is false.** They did not.

**Blog-level (D-tier, do not cite as authority).** The Low Dimensional Topology post "Slice-Ribbon Conjecture in danger!" (dmoskovich, 2 Dec 2010) — **PARTIALLY VERIFIED** via fetch: the author reports bringing "my confidence in the veracity of the Slice-Ribbon Conjecture down from around 60% ... to around 5%", and the post attributes to the GST paper the suggestion that Generalized Property R "has about as much chance of being true as the Andrews-Curtis Conjecture". **UNVERIFIED** whether that last phrase is GST's wording — I did not find it in the paper text I extracted, and I could not confirm it; treat as the blogger's paraphrase. The comment thread contains **Ian Agol** asking for ribbon-obstruction references and **Stefan Friedl** raising homotopy-ribbon invariants and noting "presumably such invariants are not helpful in this case". These are blog comments from 2010 and are now **superseded**: `DG` is *proved* handle-ribbon, so homotopy-ribbon invariants are structurally dead against it (§4, and this repo's `ABANDONED_WEAPONS_2010_2026.md`).

**Quanta (Feb 2023), on the $(2,1)$-cable of $4_1$** — **PARTIALLY VERIFIED** verbatim quotes:
- Kristen Hendricks: *"I think there's actual legitimate controversy on whether it's going to turn out to be true or not."*
- Kristen Hendricks: *"Slice-ribbon conjecture, still going strong."*
- Arunima Ray: *"It would mean that the world is a little bit more structured than you might expect otherwise."*
The article contains no quotes from Gompf or Piccirillo.

**Dunfield–Gong's own posture** — **VERIFIED**: they call $18_{\mathrm{nh}}00000601$ *"a plausible candidate"*, and in the same breath forecast *"hundreds of other similarly obscure ribbon disks"* they have not found. That is a hedged, calibrated position, not an endorsement.

**Kirby problem list 1.33.** **UNVERIFIED.** Every source I found states only the conjecture's content (slice $\iff$ ribbon). I could **not** obtain the actual commentary text of Problem 1.33 from a primary copy. Do not attribute any opinion to Kirby's list until someone here reads the list itself. (Related and confirmed: GST cite *Problem 1.82* of Kirby's list for the Generalized Property R Conjecture — **VERIFIED**, arXiv:1103.1601 §1.)

**Gompf–Stipsicz, *4-Manifolds and Kirby Calculus*, GSM 20 (1999).** **UNVERIFIED** — I did not obtain the relevant page text and will not paraphrase a remark I have not read.

**Honest summary of (d):** there is *no* public record of a leading expert flatly predicting Slice–Ribbon is false. There is a record of (i) GST predicting **Generalized Property R** is false, (ii) Hendricks describing genuine controversy, (iii) a 2010 blogger at 5% confidence, and (iv) Abe–Tange publishing a conjecture whose truth would make Slice–Ribbon much more plausible. **If our internal narrative is "everyone expects it to be false", that narrative is not supported by the sources.**

---

## 3. Steelman: why $18_{\mathrm{nh}}00000601$ is probably ribbon

This is the case I would make if I were assigned to defend the conjecture, and I think it is the stronger case.

**3.1 The base rate is devastating.** 553 of 554 knots that passed exactly the same filter — "we have strong reason to believe it's slice, and repeated ribbon searches failed" — turned out ribbon (**VERIFIED**, DG §2.7). One survivor out of 554 is roughly what you'd expect from a search with a small per-knot failure probability, *not* evidence of a structurally different object. DG themselves predict *"hundreds"* more obscure ribbon disks lurk in their unknown pile.

**3.2 The search was not exhaustive, and its blind spot is known.** DG searched *diagrammatic* bands up to bounded number and length, on a bounded set of shaken diagrams, with a band budget of **at most 4** (**VERIFIED**, §2.8: *"we looked for ribbon disks needing up to four bands... Only 75 of the ribbon disks we found used four bands, so we did not search further than that"*). Their Table 7 fusion-number distribution over the ~1.63M ribbon disks they found is **VERIFIED**:

| # bands | # knots | % |
|---:|---:|---:|
| 1 | 1,249,604 | 76.5 |
| 2 | 381,869 | 23.4 |
| 3 | 2,238 | 0.14 |
| 4 | 75 | 0.0045 |

This looks like overwhelming evidence that ribbon disks are cheap — but it is **selection-biased in exactly the wrong direction**: it is the distribution of the disks a $\le 4$-band search *found*, not the distribution of fusion numbers among ribbon knots. A genus-5 knot needing 5, 6 or 7 bands, or needing a non-diagrammatic band, or needing a diagram far from any they shook, is invisible to this table and to the search that produced it. Note also DG's own §2.9 admission that they *"had to really struggle"* to find ribbon disks for some alternating knots that are *"straightforward with the techniques of [OS]"* (Owens–Swenton) — i.e. their search has documented method-specific blind spots. And GHMR's ML search **failed on provably ribbon GST links** (**VERIFIED**, §1 above). **Search failure here has near-zero evidential weight.**

**3.3 It is already handle-ribbon, in the standard $B^4$, with a fibered disk.** Oliveira-Smith Thm 1.2 (**VERIFIED**). Every step of the hierarchy above "ribbon" is satisfied. In every historical case where a knot sat this high in the hierarchy and someone did the long handle calculus (Abe–Tange Thm 5.4; Gompf–Miyazaki), the answer came back **ribbon**. The exterior is a handlebody bundle $H\times_\Phi S^1$ (**VERIFIED** from Oliveira-Smith §3.2) — about as structured and as un-exotic an exterior as a disk complement can be.

**3.4 Fibered ribbon-disk theory says fibered handle-ribbon disks are the *natural habitat* of ribbon disks, not an exotic outlier.** Larson–Meier, "Fibered ribbon disks", J. Knot Theory Ramifications 24 (2015), 1550066 (**PARTIALLY VERIFIED**, abstract): they characterize fibered homotopy-ribbon disks, give Stallings-twist analogues for fibered disks and 2-knots, and show any fibered ribbon 2-knot arises by doubling infinitely many different slice disks. Meier–Zupan, "Knots bounding non-isotopic ribbon disks", arXiv:2310.17564, J. Topology (2025) (**PARTIALLY VERIFIED**, abstract; *note: this repo's `SOURCES.md` [S15] misattributes this to **Miller**–Zupan — the authors are **Jeffrey Meier** and Alexander Zupan; fix that*): they classify fibered homotopy-ribbon disks for generalized square knots $T_{p,q}\#\overline{T}_{p,q}$ and show that when $q=2$ **infinitely many of these fibered homotopy-ribbon disks are in fact ribbon**. The one family where anyone has actually checked, the fibered homotopy-ribbon disks turned out ribbon in abundance.

**3.5 Everything about the knot is small.** 18 crossings, genus 5, hyperbolic volume 11.93 (**VERIFIED**, DG Table 3). Nobody has ever exhibited a non-ribbon slice knot at any size; asking the first one to be 18 crossings is asking a lot.

**3.6 How many band moves might be needed?** Honest answer: nobody knows a bound. A ribbon disk for a genus-$g$ knot corresponds to an unlink derivative on a genus-$g$ Seifert surface (Miller–Zupan Prop. 1.1, **VERIFIED**), so the natural band count for $K_G$ is **5** — one past DG's search ceiling of 4. **This is not a small observation.** If the relevant unlink derivative lives on the genus-5 fiber surface, a fusion-number-5 ribbon disk is exactly the object a $\le4$-band search structurally cannot find. Caveat (**important**): fusion number and genus are not equal in general, and a ribbon disk need not be carried by the minimal-genus surface — so this is a heuristic, **UNVERIFIED** as a theorem-level claim. But it is the most natural explanation of the data, and it is *cheap to test*: extend the band search to 5–7 bands on the fiber surface specifically.

**Steelman verdict:** the single most likely state of the world is that $K_G$ is ribbon via a 5-or-more-band disk, or a disk not visible in any shaken diagram DG tried, and that the "sole survivor of 554" status is a sampling artifact of a search whose ceiling happens to sit just below this knot's complexity.

---

## 4. Steelman the other side: why it might genuinely not be ribbon

**4.1 The gap it must exploit is real and is the *only* remaining gap.** After Oliveira-Smith, $K_G$ has an R-link derivative (handle-ribbon) and lacks a known unlink derivative (ribbon). By Miller–Zupan Prop. 1.1 + Thm 1.3, **ribbon vs. handle-ribbon is exactly "unlink derivative vs. R-link derivative"** (**VERIFIED**). Every R-link is slice, but no theorem converts an R-link into an unlink. Since an R-link with 0-surgery $\#^n(S^1\times S^2)$ that is *not* an unlink would itself be a Generalized Property R counterexample, the structural question "is this R-link derivative trivializable?" is *literally* the Generalized Property R question in derivative clothing — and GST believe **that** is *"probably false"* (**VERIFIED quote**). This is the one place where the GST pessimism transfers legitimately.

**4.2 Nobody has ever proved ribbon $=$ handle-ribbon, and the experts pointedly do not assert it.** Miller–Zupan record the implication chain with **no converses asserted** (**VERIFIED**). Meier–Zupan explicitly leave open whether their fibered homotopy-ribbon disks are always ribbon — **VERIFIED verbatim**: *"When $q=2$, we prove further that infinitely many of these disks are also ribbon; whether the disks are always ribbon is an open problem."* If ribbon $=$ handle-ribbon were expected to be easy or true, this would not be phrased as an open problem in a 2025 *Journal of Topology* paper.

**4.3 GST named the exact mechanism by which a handle-theoretic disk fails to be ribbon.** **VERIFIED verbatim**: *"it seems likely that the 2-3 handle pair needed for canceling the handlebody creates troublesome local maxima."* That is a *mechanism*, not a vibe: the cancellation that proves sliceness introduces exactly the index-2 critical points that ribbonness forbids. Abe–Tange's Conjecture 6.2 (**VERIFIED**) asserts this obstruction is sometimes unavoidable, and names Gompf's $H_{n,k}$, $n\ge3$, $k\ne0$, as the promising candidate. $K_G$'s disk arises the same way: from a **trace embedding**, i.e. a 4-dimensional cancellation argument, not from a band movie.

**4.4 The known non-ribbon technology is fibered-connected-sum technology, and $K_G$ is fibered.** Miyazaki's Thm 5.5 (Trans. AMS 341, 1994) and Hom–Park's $\gamma_0$-sharp theorem (arXiv:2507.20455) both prove **non-ribbonness** of fibered objects (**PARTIALLY VERIFIED** at theorem-number level via this repo's [S07],[S08]). Ribbon-only obstructions exist and bite; they have simply never been pointed at a certified-slice target. $K_G$ is fibered of genus 5 with explicit monodromy — it is *in principle* in range of exactly this machinery.

**4.5 The finiteness handle.** Agol–Ren, arXiv:2603.10884 (2026) (**PARTIALLY VERIFIED** via [S09]): Thm 1.7 characterizes strong homotopy-ribbon concordance by monodromy compression; Thm 1.9/Cor. 1.11 give algorithmic finiteness for minimal compressions and strong-homotopy-ribbon predecessors of a fixed fibered knot. **If** every ribbon disk of a fibered knot were fibered, this would convert "is $K_G$ ribbon?" into a finite check. That conditional is the crux and it is **open** — see §7.

**4.6 Anything known that is handle-ribbon but resisted ribbon-ness?** **UNVERIFIED / apparently nothing.** I found no example in the literature of a knot proved handle-ribbon and then proved non-ribbon. The honest reading of that silence cuts **both** ways: either the classes coincide, or nobody has a tool that can separate them. Given that Miller–Zupan, Meier–Zupan and Larson–Meier all leave the separation open rather than conjecturing collapse, I read it as the second — but that is a judgement, not a fact.

**4.7 A word on Hughes–Kim–Miller.** The team memo asked about "Isotopies of surfaces". The paper is **Hughes–Kim–Miller, "Isotopies of surfaces in 4-manifolds via banded unlink diagrams", Geom. Topol. 24(3) (2020), 1519–1569; arXiv:1804.09169** (**PARTIALLY VERIFIED**, abstract): a complete set of moves relating banded unlink diagrams of isotopic surfaces in an arbitrary 4-manifold. **Relevance, stated carefully:** this gives a *complete move set for deciding isotopy of two given banded diagrams*; it does **not** give a decision procedure for "does $K$ bound *some* ribbon disk", and the move set is not known to be effectively bounded. Do not let anyone in this project cite HKM as making the ribbon search finite. It does not.

---

## 5. "Truth case": what is actually proved, and what is NOT

### Classes where Slice–Ribbon is a theorem

- **Two-bridge knots.** **Lisca, "Lens spaces, rational balls and the ribbon conjecture", Geom. Topol. 11 (2007), 429–472; arXiv:math/0701610.** Every smoothly slice 2-bridge knot is ribbon, via Donaldson's theorem on definite intersection forms characterizing which lens spaces bound rational homology 4-balls. **PARTIALLY VERIFIED** (abstract/venue; corroborated independently by DG §1.14: *"recall Lisca showed that a 2-bridge knot is ribbon if and only if it is smoothly slice [Lis]"* — **VERIFIED**).
- **3-stranded pretzel knots.** **Greene–Jabuka, "The slice-ribbon conjecture for 3-stranded pretzel knots", Amer. J. Math. 133 (2011), 555–580; arXiv:0706.3398.** For $P(p,q,r)$ with $p,q,r$ odd, every knot of finite concordance order is ribbon. **PARTIALLY VERIFIED**.
- **Montesinos knots (large family).** **Lecuona, "On the Slice-Ribbon Conjecture for Montesinos knots", Trans. AMS 364 (2012), 233–285; arXiv:0910.4601.** Donaldson's theorem again. **PARTIALLY VERIFIED**.
- **Remaining 3-stranded gap, and partial kills.** The family $P(a,-a-2,-(a+1)^2/2)$, $a$ odd $>1$, was the exception; Lecuona–Miller showed these are not slice unless $a\equiv 1,11,37,47,59 \pmod{60}$, and Kim–Lee–Song reportedly killed four-fifths of the remainder. **PARTIALLY VERIFIED** (search-derived; I did not read these papers — **verify before citing**).
- **5-stranded odd pretzels: weaker statement only.** Bryant proved slice $\Rightarrow$ *mutant ribbon* for odd 5-stranded pretzel knots (arXiv:1511.07009). **PARTIALLY VERIFIED**. **This is a weaker conclusion than ribbon and must not be quoted as Slice–Ribbon for that class.**
- **Alternating pretzel links** and **4-stranded 2-component pretzel links**: results exist. **PARTIALLY VERIFIED**, unread.
- **Census-level, not a theorem but the best empirical datum we have.** DG determine sliceness smoothly for all but ~11,400 of the 352.2 million prime knots to 19 crossings, find ~1.6 million smoothly slice (all of them ribbon), and Theorem 1.7 completely determines ribbonness among prime *alternating* knots to 19 crossings. **VERIFIED** (abstract + §1.17: *"we have identified no smoothly slice knots that are not known to be ribbon"*).
- **Fibered knots: NO.** There is **no** theorem "fibered slice $\Rightarrow$ ribbon". Casson–Gordon (Invent. Math. 74 (1983), 119–137) give: *a fibered knot is homotopy-ribbon in a homotopy 4-ball iff the fibration of the 0-surgery extends over handlebodies* (**VERIFIED** as Miller–Zupan Thm 1.4). That is homotopy-ribbon, not ribbon. $K_G$ is a fibered knot and is the live candidate — which by itself proves the class is not settled.

### 2024–2026 additions

- **Horigome–Ichihara, "On two-bridge ribbon knots", arXiv:2402.07539 (Feb 2024, final May 2024).** **PARTIALLY VERIFIED**: $K(m^2, mk\pm1)$ with $m>k>0$, $(m,k)=1$, admits a symmetric union presentation with partial knot the two-bridge knot $K(m,k)$. This is a *structure* theorem for two-bridge ribbon knots, **not** a new slice-ribbon proof — the abstract does not mention the conjecture.
- **Lackenby, arXiv:2606.06122 (June 2026)** — AC for thickenable balanced presentations (see §2c). **PARTIALLY VERIFIED**, unrefereed.
- I found **no** 2024–2026 paper proving Slice–Ribbon for a genuinely new knot class. If one exists, I did not find it, and that is a search result, not a proof of nonexistence.

### The structural theorems the team asked me to check — and the corrections

This subsection exists to kill four specific claims I was asked to check. **All four are wrong or unverified. Do not use any of them.**

1. **"Every slice knot is topologically ribbon."** **FALSE as stated / category confusion.** Topologically slice $\ne$ ribbon. The correct statement is DG's, **VERIFIED verbatim** (§1.17): *"The topological slice-ribbon conjecture is that every topologically slice knot is topologically homotopy ribbon."* That is a **conjecture**, and the conclusion is **homotopy** ribbon. DG add (**VERIFIED**): all their topologically slice knots except possibly $18_{\mathrm{nh}}00000601$ are topologically homotopy ribbon, because $\Delta_K=1$ knots are topologically homotopy ribbon by Freedman–Quinn Thm 11.7B, and that was their main method. They also cite Gordon Lemma 3.1 for "any ribbon knot is topologically homotopy ribbon".
2. **"Every slice disk can be isotoped to be ribbon after [something]."** **NO SUCH THEOREM FOUND.** I searched specifically and found nothing of this form.
3. **"Every slice disk is a ribbon disk after one 1-handle stabilization."** **NOT A THEOREM I COULD VERIFY; I believe this is a conflation.** What exists is **1-handle stabilization *distance*** between two surfaces with the same boundary, and results showing this distance can be **large**: Miller–Powell use Alexander modules to produce disks with **arbitrarily large 1-handle stabilization distance** (**PARTIALLY VERIFIED**, search-derived). That is evidence *against* any "one stabilization suffices" statement about disks. Separately there are results that one (possibly twisted) stabilization suffices for pairs of 4-manifolds obtained by *surgery along* slice disks with the same boundary (**PARTIALLY VERIFIED**, search-derived) — a statement about 4-manifolds, **not** about making a disk ribbon. Related: *"One stabilization is not enough for closed knotted surfaces"* (arXiv:2304.01504) and *"For exotic surfaces with boundary, one stabilization is not enough"*. **Nothing here makes a slice disk ribbon.**
4. **"Regularly slice implies once-stably decomposably slice" is a slice$\to$ribbon stabilization theorem.** **NO — wrong category.** **Breen, arXiv:2410.21031 (Oct 2024)**, abstract **VERIFIED verbatim**: *"We investigate the relationship between regular and decomposable Lagrangian cobordisms in 4-dimensional symplectizations. First, we show that regular sliceness implies once-stably decomposable sliceness, and offer a stabilization-free strategy."* This is the **symplectic/Lagrangian** analogue of slice–ribbon, in symplectizations. It is a genuinely interesting parallel (decomposable Lagrangian fillings play the "ribbon" role) but it says **nothing** about smooth slice disks in $B^4$.

**The one genuine "slice becomes ribbon after an operation" fact**, and it is old and cheap: **VERIFIED verbatim** from DG §1.17 — *"Recall from e.g. [Tei, Lemma 2.5] that a knot $K$ is smoothly slice if and only if there is a ribbon knot $J$ so that $K\#J$ is ribbon."* This is a *reformulation* of sliceness, not a structure theorem, and DG used it as a *search strategy* (§2.6), which is how they produced 513 of their 554 suspicious knots. It is also the correct way to phrase any "stabilization" intuition here.

---

## 6. Trap list: how claimed counterexample proofs actually fail

Run every draft through this before it leaves the room.

1. **Homotopy ball vs. standard $B^4$.** The single most common death. A disk in $W$ with $\partial W \cong S^3$ is not a slice disk until $W\cong B^4$. Akbulut–Kirby (Gompf 1991), Cappell–Shaneson (Akbulut/Gompf 2010), AJOT/Omae (Abe–Tange Thm 3.1), Calegari (Cha–Kim) all died here. **Check:** does your sliceness certificate name the *standard* $B^4$? For $K_G$ it does (Oliveira-Smith Cor. 1.1.1, **VERIFIED**).
2. **Handle-ribbon "in a homotopy 4-ball" vs. in $B^4$.** Miller–Zupan Thm 1.3 is stated **in a homotopy 4-ball** (**VERIFIED**). Oliveira-Smith Thm 1.2 upgrades to $B^4$ for $K_G$. Do not silently transport the quantifier.
3. **Homotopy-ribbon $\ne$ handle-ribbon $\ne$ ribbon.** Three distinct conditions, no proved converses. Any obstruction whose conclusion is "not homotopy-ribbon" is **structurally incapable** of touching $K_G$ or the GST band sums, because those are *proved* handle-ribbon. This kills, a priori: Casson–Gordon extension tests, metabelian/twisted-Alexander homotopy-ribbon restrictions (Friedl et al.), irregular dihedral / Cappell–Shaneson $\Xi$ bounds (Geske–Kjuchukova–Shaneson; Kjuchukova–Orr), and derived-series refinements. Spending a campaign there is the classic waste. (This is the correct and important conclusion of this repo's `ABANDONED_WEAPONS_2010_2026.md`.)
4. **Using a conjecture as a theorem.** Abe–Tange Conj. 6.1 and 6.2 are conjectures. Generalized Property R is a conjecture. The smooth 4D Poincaré conjecture is a conjecture. Kawauchi's arXiv:2212.02617 is explicitly conditional on *two* open conjectures (**VERIFIED**). Andrews–Curtis nontriviality of the GST presentations is **believed**, not proved — and GST say outright there is *"presently no way to distinguish Andrews–Curtis equivalence classes"* (**VERIFIED**).
5. **Search failure is not an obstruction.** Empirically calibrated: GHMR's algorithms failed on the **provably ribbon** $L_{1,1}$ and $L_{2,1}$ (**VERIFIED**); DG's search missed 554 disks on the first pass and found 553 of them on the second (**VERIFIED**); DG predict *"hundreds"* more they still cannot find (**VERIFIED**). A search has evidential force only with a completeness theorem bounding band number, band length, and diagram class. We have none.
6. **Generalized Property R failure $\ne$ non-ribbonness.** The implication runs one way only (§2c). No converse is known. A disproof of AC for the GST presentation would prove nothing about Slice–Ribbon.
7. **Same 0-surgery $\ne$ concordant.** Nothing transports sliceness across 0-friends without a separate theorem. This is the exact gap in the Abe–Tagami lane ($[K_n]=[K_m]$ is unproved) and the exact reason Nakamura could kill the MP knots. Note the tension recorded above: Slice–Ribbon true $\Rightarrow$ the modified Akbulut–Kirby conjecture false (**PARTIALLY VERIFIED**).
8. **Mutation $\ne$ concordance.** And "slice implies *mutant* ribbon" (Bryant) is strictly weaker than "slice implies ribbon" — do not upgrade it.
9. **Mirror / reversal / orientation conventions.** $-K = r(\bar K)$ is the concordance inverse. Abe–Tagami's convention uses the mirror of the second summand; Miyazaki's pairing theorem is a statement about *specific* mirror/reversal pairings. A sign slip here silently converts a true theorem into a false one. This repo's `ABE_TAGAMI_AUDIT.md` gets this right; keep it that way.
10. **"Ribbon" for links means the disks are *disjoint*.** GST §8 (**VERIFIED**): *"A link ... is called ribbon if the disks can be chosen so that the radial function on $B^4$ restricts to a Morse function without local maxima on the disks."* Each GST component is individually ribbon; that is worthless, because — **VERIFIED verbatim** — *"the individual ribbon disks seem to interfere with each other."* Never argue component-wise.
11. **Immersed disk in $S^3$ with ribbon singularities vs. arbitrary immersed disk with clasps.** Clasp singularities are not ribbon singularities. A "ribbon presentation" must be checked to have only ribbon (not clasp) double-point arcs.
12. **Fusion number, ribbon number, and band count are different invariants.** Fusion number = minimal number of 1-handles in a ribbon disk = number of band moves to the unlink (**VERIFIED**, DG §2.8). It is not the genus, not the crossing number, and Table 7 is a distribution over *found* disks, not over ribbon knots.
13. **Stable $\ne$ unstable.** Stable handleslide equivalence, stable AC, stable Kauffman, one-stabilization results — all are strictly weaker than their unstable forms, and the unstable forms are what ribbonness needs.
14. **One derivative is not all derivatives.** Prop. 1.1 quantifies over *all* Seifert surfaces and *all* derivatives. Showing the *known* R-link derivative of $K_G$ is not an unlink proves nothing. A non-ribbon proof requires excluding **every** unlink derivative on **every** Seifert surface. No finite-completeness theorem for this exists.
15. **Author and attribution errors propagate.** Concrete instance found in this repo: `SOURCES.md` [S15] attributes "Knots bounding non-isotopic ribbon disks" to *Miller*–Zupan; the authors are **Meier**–Zupan. Fix before any external circulation.
16. **Preprint $\ne$ theorem.** Oliveira-Smith (2603.23717), Agol–Ren (2603.10884), Hom–Park (2507.20455, 2608.06625), Diao–Pan–Yan (2604.17737), Lackenby (2606.06122), Kawauchi (2212.02617) are all unrefereed as far as I can verify. Our entire flagship lane rests on **one unrefereed 2026 preprint** (Oliveira-Smith Cor. 1.1.1). If that standardization has an error, `DG` is not even known to be slice.

---

## 7. Verdict

### (i) Probability that a counterexample to Slice–Ribbon exists

**~45%.** Genuinely uncertain, and I decline to put it far from even. The honest reasons:

- *For existence:* the ribbon/handle-ribbon gap is a real, unbridged gap that experts repeatedly decline to close (Miller–Zupan assert no converses; Meier–Zupan call the ribbon-ness of their fibered disks "an open problem"). The mechanism by which a handle-theoretic disk fails to be ribbon is named explicitly by GST (2-3 handle pairs creating local maxima) and conjectured to be unavoidable by Abe–Tange (Conj. 6.2). Slice–Ribbon has no conceptual proof strategy — every positive result (Lisca, Greene–Jabuka, Lecuona) goes through Donaldson's theorem applied to *very* special classes, which is a technique with no prospect of generalizing.
- *Against existence:* 64 years, zero certified examples; a 553/554 resolution rate on the best modern candidate filter; Abe–Tange Conj. 6.1 would imply the two flagship families are ribbon and is stated by working experts as *"the first step toward an affirmative answer"*; and every prior "structurally must be non-ribbon" intuition (Akbulut–Kirby, Omae, CS spheres) proved wrong.
- I moved off 50% toward "exists" only slightly, because the *specific* structural gap (unlink vs. R-link derivative $\approx$ Generalized Property R) is one that its own discoverers call *"probably false"*.

### (ii) Probability that a counterexample is *provable* by 2028 with current tools

**~5%, and I would defend 3%.** This is where I am confident and where the team should recalibrate hardest.

A proof requires a knot that is (a) certified smoothly slice in standard $B^4$ **and** (b) certified non-ribbon. Today exactly one object has (a) with (b) open — $K_G$ — and proving (b) requires excluding **every** unlink derivative on **every** Seifert surface. **No finite-completeness theorem for that quantifier exists, for any knot.** The Tier B objects (Abe–Tagami $D_{n,m}$, Hom–Park Cor. 1.3, Gompf–Miyazaki $J(O)\#J^*(O)$, Rudolph's plumbing) all have (b) and none has (a); getting (a) for any of them means proving a *new smooth concordance equality*, which modern Floer/gauge technology is built to **disprove**, not prove. Two independent hard things have to break our way inside 27 months.

The asymmetric risk is worth stating plainly: **the far likelier 2026–2028 headline is "$18_{\mathrm{nh}}00000601$ is ribbon"** — from a 5-to-7-band search on the genus-5 fiber surface, or from someone tracing Oliveira-Smith's handle calculus by hand the way Abe–Tange traced theirs. If this team wants to be useful rather than merely hopeful, **run that search first**, because it is cheap, it is the highest-information experiment available, and if it succeeds it saves everyone a wasted campaign.

### (iii) The single missing theorem that would most change the picture

> **Fibered ribbon-disk completeness.** *Every ribbon disk bounded by a fibered knot is fibered.*

Recorded as open in Meier–Zupan (**PARTIALLY VERIFIED** via this repo's [S15]; the published open problem I could verify verbatim is the closely related *"whether the disks are always ribbon is an open problem"*).

Why this one and not the others:

- It is the **only** candidate theorem that converts the fatal universal quantifier ("every ribbon disk, every Seifert surface") into a **finite** object. Combined with Agol–Ren's algorithmic finiteness for minimal monodromy compressions of a fixed fibered knot (arXiv:2603.10884, Thm 1.9/Cor. 1.11), it would reduce "is $K_G$ ribbon?" to a finite, machine-checkable audit over an explicit genus-5 monodromy — the only path I can see to a *certificate-grade* non-ribbon proof rather than another search failure.
- It is **double-edged, which is a feature**: it would just as likely produce a ribbon disk (killing $K_G$ and the campaign cleanly) as exclude one. Either outcome is decisive, which is more than can be said for anything else on the board.
- The runner-up is **Abe–Tange Conjecture 6.1**, but note its asymmetry: proving it closes the GST lane *and* the annulus-twist lane *in favor of Slice–Ribbon*, while disproving it yields a non-ribbon belt sphere in a no-3-handle $B^4$ diagram — which would be a counterexample only if that belt sphere's sliceness is independently certified in standard $B^4$ (it is, by construction). So 6.1 is the higher-payoff target but has no known attack beyond Abe–Tange's own Lemma 5.1, which Conjecture 6.2 predicts must sometimes fail.
- Explicitly **not** the answer: any new *sliceness* obstruction (vanishes by hypothesis), any new *homotopy-ribbon* obstruction (structurally dead against a handle-ribbon target — trap #3), any Generalized Property R progress (no converse — trap #6), and any improved *search* (no completeness — trap #5).

---

### Recommended immediate actions

1. **Run the 5–7 band search on the genus-5 fiber surface of $K_G$**, with derivative-guided band selection from Oliveira-Smith's explicit R-link $L^+$, not generic diagrammatic bands. Cheapest decisive experiment available. If it finds a disk, we are done and we saved a year.
2. **Independently audit Oliveira-Smith arXiv:2603.23717v1** (unrefereed, single-author, and the sole certificate for our flagship's sliceness). If Theorem 1.1 fails, the whole lane collapses to "not even known slice".
3. **Check thickenability** of $\langle x,y\mid yxy=xyx,\ x^{n+1}=y^n\rangle$ against Lackenby arXiv:2606.06122. If thickenable, the AC-hardness story behind the GST lane weakens materially.
4. **Recover the two texts I could not obtain**: Kirby's Problem 1.33 commentary (primary list), and Turaev, *Multiplace generalizations of the Seifert form of a classical knot*, Math. USSR-Sb. 44(3) (1983) — "Theorem H". Both are currently **UNVERIFIED** in this project and one of them (Turaev) is the only allegedly *ribbon-specific* classical obstruction anyone has named. Do not compute with Theorem H before transcribing its hypotheses.
5. **Fix `SOURCES.md` [S15]**: Meier–Zupan, not Miller–Zupan.
6. **Stop writing "everyone expects Slice–Ribbon to be false."** The sources do not support it (§2d).

---

## Appendix: sources cited, with evidence level

**Read directly (full or extracted text) — VERIFIED:**
- Gompf–Scharlemann–Thompson, *Fibered knots and potential counterexamples to the Property 2R and Slice-Ribbon Conjectures*, Geom. Topol. 14 (2010), 2305–2347. [arXiv:1103.1601](https://arxiv.org/abs/1103.1601)
- Abe–Tange, *A construction of slice knots via annulus twists*. [arXiv:1305.7492v4](https://arxiv.org/abs/1305.7492)
- Dunfield–Gong, *Ribbon concordances and slice obstructions: experiments and examples*. [arXiv:2512.21825](https://arxiv.org/abs/2512.21825)
- Oliveira-Smith, *A Dunfield–Gong 4-Sphere is Standard*. [arXiv:2603.23717v1](https://arxiv.org/abs/2603.23717)
- Miller–Zupan, *Equivalent characterizations of handle-ribbon knots*, Comm. Anal. Geom. 31 (2023). [arXiv:2005.11243](https://arxiv.org/abs/2005.11243)
- Kirby–Melvin, *Slice knots and property R*, Invent. Math. 45 (1978), 57–59. [PDF](https://math.berkeley.edu/~kirby/papers/Kirby%20and%20Melvin%20-%20Slice%20knots%20and%20property%20R%20-%20MR0467754.pdf)
- Gukov–Halverson–Manolescu–Ruehle, *Searching for ribbons with machine learning*. [arXiv:2304.09304](https://arxiv.org/abs/2304.09304)
- "Slice-Ribbon Conjecture in danger!", Low Dimensional Topology blog, 2 Dec 2010 — **discovery only, never authority**. [link](https://ldtopology.wordpress.com/2010/12/02/slice-ribbon-conjecture-in-danger/)
- Quanta Magazine, 2 Feb 2023 — for attributed quotes only. [link](https://www.quantamagazine.org/mathematicians-prove-this-knot-cannot-solve-major-problem-20230202/)

**Abstract/metadata only — PARTIALLY VERIFIED:**
- Gompf, *Killing the Akbulut–Kirby 4-sphere...*, Topology 30 (1991), 97–115. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/0040938391900364)
- Gompf–Miyazaki, *Some well-disguised ribbon knots*, Topology Appl. 64 (1995), 117–131. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/016686419400103A) (403 on fetch)
- Akbulut, *Cappell–Shaneson homotopy spheres are standard*, Ann. of Math. 171 (2010). [arXiv:0907.0136](https://arxiv.org/abs/0907.0136)
- Gompf, *More Cappell–Shaneson spheres are standard*, AGT 10 (2010), 1665–1681. [arXiv:0908.1914](https://arxiv.org/abs/0908.1914)
- Scharlemann, *Proposed Property 2R counterexamples classified*. [arXiv:1208.1299](https://arxiv.org/abs/1208.1299)
- Lisca, *Lens spaces, rational balls and the ribbon conjecture*, Geom. Topol. 11 (2007). [arXiv:math/0701610](https://arxiv.org/abs/math/0701610)
- Greene–Jabuka, *The slice-ribbon conjecture for 3-stranded pretzel knots*, Amer. J. Math. 133 (2011). [arXiv:0706.3398](https://arxiv.org/abs/0706.3398)
- Lecuona, *On the Slice-Ribbon Conjecture for Montesinos knots*, Trans. AMS 364 (2012). [arXiv:0910.4601](https://arxiv.org/abs/0910.4601)
- Manolescu–Piccirillo, *From zero surgeries to candidates for exotic definite 4-manifolds*, J. LMS (2023). [arXiv:2102.04391](https://arxiv.org/abs/2102.04391)
- Nakamura, *Trace embeddings from zero surgery homeomorphisms*, J. Topology (2023). [arXiv:2203.14270](https://arxiv.org/abs/2203.14270)
- Dai–Kang–Mallick–Park–Stoffregen, *The (2,1)-cable of the figure-eight knot is not smoothly slice*, Invent. Math. (2024). [arXiv:2207.14187](https://arxiv.org/abs/2207.14187)
- Meier–Zupan, *Knots bounding non-isotopic ribbon disks*, J. Topology (2025). [arXiv:2310.17564](https://arxiv.org/abs/2310.17564)
- Larson–Meier, *Fibered ribbon disks*, JKTR 24 (2015). [arXiv:1410.4854](https://arxiv.org/abs/1410.4854)
- Hughes–Kim–Miller, *Isotopies of surfaces in 4-manifolds via banded unlink diagrams*, Geom. Topol. 24 (2020). [arXiv:1804.09169](https://arxiv.org/abs/1804.09169)
- Rudolph, *A non-ribbon plumbing of fibered ribbon knots*. [arXiv:math/0105257](https://arxiv.org/abs/math/0105257)
- Horigome–Ichihara, *On two-bridge ribbon knots*. [arXiv:2402.07539](https://arxiv.org/abs/2402.07539)
- Lackenby, *The stable Andrews–Curtis conjecture and thickenable presentations of the trivial group*. [arXiv:2606.06122](https://arxiv.org/abs/2606.06122)
- Breen, *Regularly slice implies once-stably decomposably slice*. [arXiv:2410.21031](https://arxiv.org/abs/2410.21031) — **symplectic, not smooth slice-ribbon**
- Kawauchi, *Ribbonness of Kervaire's sphere-link...*. [arXiv:2212.02617](https://arxiv.org/abs/2212.02617) — **conditional on two open conjectures**
- Cha–Kim, *Calegari's homotopy 4-spheres from fibered knots are standard*. [arXiv:2411.10051](https://arxiv.org/abs/2411.10051)
- Abe–Tagami [arXiv:1502.01102], Miyazaki Trans. AMS 341 (1994), Hom–Park [arXiv:2507.20455], Agol–Ren [arXiv:2603.10884], Diao–Pan–Yan [arXiv:2604.17737] — theorem numbers via this repo's prior `SOURCES.md` audit, not re-read here.

**UNVERIFIED — do not cite until recovered:**
- Kirby's Problem List, Problem 1.33 commentary (Problem 1.82, for Generalized Property R, *is* confirmed via GST §1).
- Gompf–Stipsicz, *4-Manifolds and Kirby Calculus*, GSM 20 (1999) — any specific remark.
- Turaev, *Multiplace generalizations of the Seifert form of a classical knot*, Math. USSR-Sb. 44(3) (1983), 335–361 — "Theorem H" statement and hypotheses.
- The "about as much chance of being true as the Andrews–Curtis Conjecture" phrasing — blogger's paraphrase, not located in GST's text.
- Lecuona–Miller and Kim–Lee–Song partial results on $P(a,-a-2,-(a+1)^2/2)$ — search-derived, unread.
- Miller–Powell arbitrarily-large 1-handle stabilization distance — search-derived, unread.
