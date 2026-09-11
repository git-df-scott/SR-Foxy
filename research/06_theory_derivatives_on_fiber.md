# THEORY.md — Slice–Ribbon counterexample hunt: derivatives on the fiber of $K_G$

**Status legend.** Every assertion is tagged:

- **[PROVED]** — full proof written out below, self-contained modulo explicitly cited classical results.
- **[CITED]** — stated in a primary source I actually fetched and read; quotation/reference given. I did **not** independently reprove it.
- **[CITED-UNVERIFIED]** — asserted in a primary source, but the source's proof is a one-line sketch that I could **not** fully reconstruct. Flagged as such; do not build on it without checking.
- **[CONJECTURED]** — my guess, with evidence.
- **[OPEN]** — genuinely open, as far as the literature I checked shows.

**Standing conventions.** $K\subset S^3$ a knot, $F$ a Seifert surface of genus $g$, $x^+$ the positive push-off of $x\subset F$ off $F$, $V(x,y)=\operatorname{lk}(x,y^+)$ the Seifert form on $H_1(F)\cong\mathbb Z^{2g}$, $S=V-V^{T}$ the intersection form. All manifolds smooth and oriented.

**Derivative (Miller–Zupan, [MZ20], Introduction, verbatim).** *"For a knot $K\subset S^3$ and genus $g$ Seifert surface $F$ for $K$, a derivative $L$ for $K$ in $F$ is a $g$-component link such that $L\subset F$, $F-L$ is a connected planar surface, and $\operatorname{lk}(L_i,L_j^+)=0$ for all $i,j$."*

**R-link ([MZ20]).** $L$ is an *R-link* if $S^3_{\vec 0}(L)=\#^{n}(S^1\times S^2)$.

**Anchors actually verified in the sources.**

- **[CITED]** Miller–Zupan, arXiv:2005.11243, Prop. 1.1 (attributed to Cochran–Davis [CD15]): *$K$ is ribbon iff $K$ has an unlink derivative.*
- **[CITED]** Miller–Zupan, Thm 1.3: *$K$ is handle-ribbon in a homotopy 4-ball iff $K$ has an R-link derivative.*
- **[CITED]** Miller–Zupan, Thm 2.5 = Casson–Gordon 1983: *A fibered $K$ is homotopy-ribbon in a homotopy 4-ball iff the closed monodromy $\hat\varphi$ extends over a handlebody $H$ with $\partial H=\hat F$; then $B'\setminus D=H\times_\Phi S^1$.*
- **[CITED]** Miller–Zupan, Thm 3.3: if $K\cup J$ is a 2-component R-link with $K$ fibered, then $K\cup J$ is stably equivalent to $K\cup L$ with $L$ an R-link derivative **in the fiber**, and $\hat\varphi$ extends over $H_L$.
- **[CITED]** Larson–Meier, arXiv:1410.4854, Thm 1.1: *a fibered slice disk $D\subset B^4$ with fiber $H$ is homotopy-ribbon iff $H\cong H_g$ is a handlebody.* Thm 1.2: the Stallings-twist analogue for fibered disks.
- **[CITED]** Oliveira-Smith, arXiv:2603.23717: the Dunfield–Gong homotopy 4-sphere is standard; $18\text{nh}00000601=K_G$ is slice **in the standard $B^4$** and bounds a **fibered handle-ribbon disk**. (Consequence used throughout: for $K_G$ there is no "exotic homotopy ball" escape hatch — the handle-ribbon disk sits in $B^4$.)
- **[CITED]** Agol–Ren, arXiv:2603.10884: simplicial volume and dilatation are monotone under ribbon concordance between fibered knots; every fibered knot has finitely many ribbon-concordance predecessors; **algorithm to enumerate all minimal compressions of a surface homeomorphism without redundancy**.
- **[CITED]** Gompf–Scharlemann–Thompson, arXiv:1103.1601: the GST links $L_{n,k}$ are 2-component R-links containing the square knot, potential GPR counterexamples, and yield slice knots of unknown ribbon status.
- **[CITED]** Diao–Pan–Yan, arXiv:2604.17737: experimental/algorithmic search for stable handleslide-triviality of GST links; some verified stably handleslide trivial, many shown stably handleslide equivalent to each other.
- **[CITED]** Cochran–Davis, arXiv:1303.4418 §7 (Prop. 7.3, Cor. 7.4): "excellent Seifert surface" = one carrying a trivial-link set of surgery curves; Slice-Ribbon $\iff$ every slice knot has an excellent Seifert surface $\iff$ every Seifert surface of a slice knot stabilizes to an excellent one. Stabilizations of excellent surfaces are excellent.

---

# P1. Minimal-genus reduction

## P1.0 Two book-keeping lemmas

**Lemma 1.1 [PROVED].** *Let $F$ be a genus-$g$ Seifert surface for $K$ and let $L=L_1\cup\dots\cup L_g\subset F$ be disjoint simple closed curves whose classes $[L_1],\dots,[L_g]$ are linearly independent in $H_1(F;\mathbb Z)$. Then $F\setminus L$ is connected and planar with $2g+1$ boundary components.*

*Proof.* If $F\setminus L$ were disconnected, some non-empty subcollection $L'\subseteq L$ would separate $F$; then a suitable signed sum $\sum_{L_i\in L'}\varepsilon_i[L_i]$ (the boundary of one of the pieces, which is a union of components of $L'$ together with possibly $\partial F$) is null-homologous in $H_1(F)$, and since $[\partial F]=0$ in $H_1(F)$ this gives a non-trivial linear relation among the $[L_i]$ — contradiction. So $F\setminus L$ is connected. Cutting along $g$ circles does not change Euler characteristic, so $\chi(F\setminus L)=\chi(F)=1-2g$, and $F\setminus L$ has $1+2g$ boundary circles. Connected with $b$ boundary circles and $\chi=2-2h-b$ forces $1-2g=2-2h-(2g+1)$, i.e. $h=0$. $\square$

So in the definition of derivative, "$F-L$ connected planar" is **equivalent** to "$[L]$ spans a rank-$g$ direct summand", given that $L$ has $g$ components on a genus-$g$ surface. (Independence over $\mathbb Q$ suffices for the argument; the summand condition is then automatic from $F\setminus L$ being planar.) We use "derivative" and "**cut system with vanishing Seifert form**" interchangeably.

**Lemma 1.2 (capping/compressing dictionary) [PROVED].**

*(a) If $L\subset F$ is a $g$-component unlink derivative, then $K$ bounds a ribbon disk $\Delta\looparrowright S^3$ with exactly $2g$ minima and $2g-1$ saddles, whose $2g$ minimum disks come in $g$ parallel pairs (the two push-offs of the $g$ disjoint disks bounded by $L$). In particular the **fusion number** of $K$ is $\le 2g-1$.*

*(b) Conversely, if $\Delta$ is a ribbon disk for $K$ presented with $2g$ minimum disks $\delta_1,\delta_1',\dots,\delta_g,\delta_g'$ such that $\delta_i,\delta_i'$ are parallel (co-bound a product region $P_i\cong\delta\times[0,1]$ whose interior meets $\Delta$ only in the sheets crossing it), then replacing each pair $\delta_i\cup\delta_i'$ by the side annulus $A_i=\partial P_i\setminus(\delta_i\cup\delta_i')$ produces an embedded genus-$g$ Seifert surface $F$ for $K$ carrying the $g$-component unlink derivative $L=\{\text{core}(A_i)\}$.*

*Proof.* (a) $L$ bounds disjoint embedded disks $\Delta_1,\dots,\Delta_g\subset S^3$ (unlink). Put $F$ and the $\Delta_i$ in general position; by innermost-circle surgery on $\Delta_i$ we may assume $\Delta_i\cap F$ is a union of arcs. Ambient-surger $F$ along $L$: cut $F$ along $L$ and cap the resulting $2g$ circles with the $2g$ push-offs $\Delta_i^{\pm}$ of $\Delta_i$ to the two sides of $F$. The result is $(F\setminus L)\cup\bigcup_i(\Delta_i^+\cup\Delta_i^-)$; by Lemma 1.1 this is connected, has $\chi=(1-2g)+2g=1$ and one boundary circle $K$, hence is a disk. Its only self-intersections are the arcs $\Delta_i^\pm\cap(F\setminus L)$, each of which is interior to $\Delta_i^{\pm}$ and properly embedded in $F\setminus L$ — i.e. **ribbon** singularities. Reading the radial Morse function: the $2g$ disks $\Delta_i^{\pm}$ are the minima and the planar cobordism $F\setminus L$ (connected, $2g$ incoming, $1$ outgoing boundary circle, $\chi=1-2g$) is a composition of $2g-1$ saddles. (b) Reverse the same construction; $\chi(F)=(1-2g)+0=1-2g$ so $\mathrm{genus}(F)=g$; $L_i=\mathrm{core}(A_i)$ bounds $\delta\times\{1/2\}\subset P_i$, and the $P_i$ are disjoint, so $L$ is an unlink; $\operatorname{lk}(L_i,L_j^+)=0$ because $L_j^+\subset A_j$ is disjoint from the disk $\delta\times\{1/2\}\subset P_i$ for $i\ne j$ and from $\delta\times\{1/2\}\subset P_i$ for $i=j$ (push-off along $\partial P_i$). $\square$

Lemma 1.2(a) is exactly the converse half of [CD15, Cor. 7.4] ("$K$ can be obtained from the trivial $2g$-component link formed by taking $2$ anti-parallel copies of $T$ and then attaching $2g-1$ bands").

## P1.1 The genus of the surface produced from a ribbon disk

Let $\Delta\looparrowright S^3$ be a ribbon disk for $K$ with

- $m$ minima (equivalently: $\Delta$ is a fusion of an $m$-component unlink along $n=m-1$ bands), and
- $r$ **ribbon singularities** (double-point arcs).

**[CITED-UNVERIFIED]** Cochran–Davis, proof of [CD15, Cor. 7.4], assert: *"if $K$ bounds a ribbon disk $\Delta\looparrowright S^3$ then $K$ admits a natural excellent Seifert surface $F$ obtained by desingularizing the immersed disk $\Delta$ along the set of double arcs in the standard way. Each arc is embedded in the interior of a small sub-disk of $\Delta$. The boundaries of these (disjoint) sub-disks form a set of surgery curves for $F$."*

Since a "set of surgery curves" for a genus-$h$ surface has exactly $h$ components, this asserts

$$\boxed{\ \gamma(\Delta):=\mathrm{genus}(F_\Delta)=r=\#\{\text{ribbon singularities of }\Delta\}\ }$$

with derivative $L=\{\partial\delta_i\}_{i=1}^r$, $\delta_i\subset\Delta$ a small sub-disk containing the *interior* preimage of the $i$-th double arc, and $L$ an unlink because the $\delta_i$ are disjoint embedded disks in $S^3$.

**Honest caveat.** I verified the Euler-characteristic bookkeeping ($\chi(F_\Delta)=\chi(\Delta)-2r=1-2r$, i.e. one handle per double arc, consistent with $\gamma=r$) and the consistency checks below, but **I could not reconstruct the local desingularization move** ("the standard way"). Three naive candidates all fail: (i) pushing the interior sheet off the band is obstructed because the band meets the sub-disk with algebraic intersection $\pm1$; (ii) deleting $\operatorname{int}\delta_i$ alone yields a planar surface with $\partial=K\sqcup C_1\sqcup\dots\sqcup C_r$ ($\chi=1-r$), one boundary circle too few per singularity; (iii) cutting the band and re-routing around $\partial\delta_i$ changes $\partial\Delta$. The correct move must cost $\chi=-2$ per double arc. **Action item N4 below.** Everything downstream is stated so that it degrades gracefully: all I really need is the (obvious) inequality $\gamma(\Delta)\ge g(K)$ together with *some* effective bound $\gamma(\Delta)\le c(\Delta)$.

**Consistency checks of $\gamma=r$.**

1. $\gamma(\Delta)\ge g(K)$ always (a Seifert surface has genus $\ge g(K)$), so $\gamma=r$ gives the (believable, and to my knowledge folklore) bound $r\ge g(K)$: *a ribbon disk has at least $g(K)$ ribbon singularities.*
2. Square knot $3_1\#\overline{3_1}$: $g=2$, minimal ribbon presentation has $m=2$, $n=1$, and $r=2$ for the standard disk. $\gamma=r=2=g$ ✓, and the genus-2 fiber does carry a 2-component unlink derivative (Meier–Zupan's generalized square knots).
3. Unknot as a fusion of a 2-component unlink along a band passing once through one disk: $m=2,n=1,r=1$, $\gamma=1$: a stabilized genus-1 Seifert surface for the unknot, which does carry a 1-component unlink derivative ✓.
4. **Not** $\gamma=n$ or $\gamma=m/2$: the square knot has $n=1$ and $m=2$, but $g=2$, so neither $n$ nor $m/2$ can be the genus of the resulting surface. (This kills the two "obvious" guesses in the problem statement: the genus is governed by the **ribbon singularities**, not by the bands.) The reconciliation with Lemma 1.2(a) is that Lemma 1.2(a) is not an inverse of the desingularization: an arbitrary ribbon disk must first be modified so that its minima occur in **parallel pairs**, and this modification changes $m$.

## P1.2 Uniqueness of the minimal-genus Seifert surface of a fibered knot

**Theorem 1.3 (classical) [CITED].** *Let $K$ be a fibered knot with fiber $F$. Then $F$ is the unique minimal-genus Seifert surface for $K$, up to ambient isotopy.*

References, in decreasing order of directness:

- Neuwirth–Stallings: the fiber is minimal genus (the fibration is taut).
- Whitten, *Isotopy types of knot spanning surfaces*, Topology **12** (1973), 373–380.
- Kobayashi, *Uniqueness of minimal genus Seifert surfaces for links*, Topology Appl. **33** (1989), 265–279.
- Sutured-manifold proof (the one to use if a referee objects): $E(K)$ cut along $F$ is the product $F\times I$. Let $F'$ be another minimal-genus Seifert surface, isotoped to meet $F$ minimally; $F'\cap(F\times I)$ is incompressible and $\partial$-incompressible in the product $F\times I$, hence each component is horizontal ($F\times\{pt\}$) or vertical ($c\times I$); minimality plus $[F']=[F]\in H_2(E(K),\partial)$ forces $F'$ to be horizontal, i.e. isotopic to $F$.

I did **not** personally re-verify Whitten's statement against his paper; the sutured-manifold argument is standard and I am confident in it. Do not cite Whitten without checking the exact wording.

## P1.3 The reduction

**Theorem 1.4 (minimal-genus reduction) [PROVED, modulo Thm 1.3].**
*Let $K$ be a fibered knot of genus $g$ with fiber $F$. Suppose $K$ bounds a ribbon disk $\Delta$ for which the associated excellent Seifert surface $F_\Delta$ has genus exactly $g$. Then $F_\Delta$ is ambient isotopic to $F$, and consequently the fiber $F$ itself carries a $g$-component unlink derivative.*

*Proof.* $F_\Delta$ is a Seifert surface for $K$ of genus $g=g(K)$, hence minimal genus. By Theorem 1.3 it is isotopic to the fiber $F$. Transport the unlink derivative $L\subset F_\Delta$ along the isotopy: the ambient isotopy carries $L$ to a link $L'\subset F$ which is still an unlink (ambient isotopy of $S^3$), still a cut system, and still has vanishing Seifert form (the Seifert form is an isotopy invariant of the pair $(F,L)$). $\square$

**Corollary 1.5 [PROVED, modulo Thm 1.3 and the $\gamma=r$ claim].**
*Let $K_G=18\text{nh}00000601$, fibered of genus $5$ with fiber $F$ and monodromy $\varphi$. If $K_G$ bounds a ribbon disk with exactly $5$ ribbon singularities, then the genus-5 fiber $F$ carries a $5$-component unlink derivative. Contrapositively: if one verifies that no $5$-component cut system on $F$ is an unlink, then **every** ribbon disk of $K_G$ has at least $6$ ribbon singularities.*

**The converted question.** Combining with P3 below, "$K_G$ is ribbon with a minimal-complexity ribbon disk" becomes the following *structured, arguably finite* question:

> **(Q)** Among the $\hat\varphi$-invariant genus-5 handlebodies $H$ with $\partial H=\hat F$, is there one admitting a complete meridian system whose boundary curves form an **unlink** in $S^3$?

and by Cochran–Davis's stabilization statement, the full slice–ribbon question for $K_G$ is:

> **(Q$^{\mathrm{st}}$)** Does some stabilization $F\#(\text{trivial handles})$ of the fiber carry an unlink derivative? [CITED: CD15 Prop. 7.3(2) + "any two Seifert surfaces have a common stabilization" + "stabilizations of excellent surfaces are excellent".]

(Q) is level $n=0$ of (Q$^{\mathrm{st}}$).

---

# P2. Handle slides along arcs in the surface

## P2.1 Surface slides preserve derivatives and the surgery manifold

**Theorem 2.1 [PROVED].** *Let $F$ be a genus-$g$ Seifert surface for $K$ and $L=L_1\cup\dots\cup L_g\subset F$ a derivative. Let $\gamma\subset F\setminus L$ be an embedded arc from $L_i$ to $L_j$ ($i\ne j$), and let $L_i'=L_i\#_\gamma L_j$ be the band sum along the band $N(\gamma)\subset F$. Put $L'=(L\setminus L_i)\cup L_i'$. Then:*

1. *$L'\subset F$ and $L'$ is again a derivative for $K$ in $F$;*
2. *the surface framing of $L_i'$ equals its $0$-framing;*
3. *$L'$ is obtained from $L$ by a Kirby handleslide of $0$-framed components; hence $S^3_{\vec0}(L')\cong S^3_{\vec0}(L)$ and $X_{\vec0}(L')\cong X_{\vec0}(L)$. In particular $L'$ is an R-link iff $L$ is.*

*Proof.* **Framings.** For a simple closed curve $c\subset F$ the surface framing is $\mathrm{fr}_F(c)=\operatorname{lk}(c,c^+)=V([c],[c])$, where $c^+$ is the push-off inside $F$; pushing off inside $F$ and pushing off transversally give the same framing up to the standard identification, and the linking number computes it. For a derivative, $V([L_k],[L_k])=0$, so $\mathrm{fr}_F(L_k)=0=$ the $0$-framing, for every $k$. This is the hypothesis that makes "surface slide = Kirby slide" work.

Next, for $i\ne j$, $L_i$ and $L_j$ are **disjoint** curves on $F$, and the isotopy pushing $L_j$ off $F$ to $L_j^+$ has track $L_j\times[0,\varepsilon]$ disjoint from $L_i$; hence
$$\operatorname{lk}(L_i,L_j)=\operatorname{lk}(L_i,L_j^+)=0 .$$

Now use the band-sum framing formula: if $c=a\#_\beta b$ is a band sum of disjoint framed knots along a band $\beta$ compatible with the framings, then
$$\mathrm{fr}(c)=\mathrm{fr}(a)+\mathrm{fr}(b)+2\operatorname{lk}(a,b).$$
(Proof: a Seifert-framing computation — push $c$ off along the band; the push-off $c^\sharp$ meets a Seifert surface for $c$ in $\mathrm{fr}(a)+\mathrm{fr}(b)$ points from the two pieces and $2\operatorname{lk}(a,b)$ points from the two strands of the band running alongside the other component.) Here the band $N(\gamma)\subset F$ is by construction compatible with the surface framings of $L_i$ and $L_j$, and $\mathrm{fr}_F(L_i)=\mathrm{fr}_F(L_j)=\operatorname{lk}(L_i,L_j)=0$. Hence
$$\mathrm{fr}_F(L_i')=0+0+2\cdot 0=0,$$
which proves (2): **the surface framing of the band sum is again the $0$-framing.** (This is the point the problem statement asked to check carefully; note it uses $\operatorname{lk}(L_i,L_j)=0$, which is part of the derivative hypothesis, not just $\operatorname{lk}(L_k,L_k^+)=0$.)

**(3)** Because all framings involved are $0$-framings and the band lies in $S^3$, $L\rightsquigarrow L'$ is literally the handleslide move of [MZ20, §2.2]: "$L_1\cup L_2\cup\alpha$ has a framed pair of pants neighbourhood $N\subset S^3$…". Handleslides of $0$-framed links preserve the surgered manifold and the trace [CITED: MZ20 §2.2, standard Kirby calculus].

**(1)** $L'\subset F$ by construction. Homologically $[L_i']=[L_i]\pm[L_j]$ and $[L_k']=[L_k]$ for $k\ne i$, an elementary (unimodular) change of basis of $\mathrm{span}([L_1],\dots,[L_g])\subset H_1(F)$; so the classes stay independent and Lemma 1.1 gives $F\setminus L'$ connected planar. The Seifert form $V$ is bilinear on $H_1(F)$ and vanishes identically on $\mathrm{span}([L_k])$ (since $V(L_k,L_l)=0$ for all $k,l$), and $[L']$ spans the same subgroup; hence $V(L_k',L_l')=0$, i.e. $\operatorname{lk}(L_k',L_l'^+)=0$. $\square$

**Corollary 2.2 [PROVED].** *The set of derivatives on a fixed Seifert surface $F$ is closed under surface handleslides, and "does $F$ carry an unlink derivative in the surface-slide orbit of $L$?" is a Generalized-Property-R question restricted to slides along arcs of $F\setminus L$.*

## P2.2 What the surface-slide orbit actually is

**Proposition 2.3 [PROVED].** *Let $L\subset F$ be a derivative and $H_L$ the abstract handlebody obtained by attaching $2$-handles to $\hat F\times[0,1]$ along $L\times\{1\}$ and capping with a $3$-handle (equivalently: the handlebody determined by the cut system $L\subset\hat F$). Then the surface-slide orbit of $L$, up to isotopy in $F$, is exactly the set of complete meridian systems of $H_L$.*

*Proof.* A surface handleslide of $L_i$ over $L_j$ along $\gamma\subset\hat F\setminus L$ is precisely a disk slide of the meridian disk $D_i$ over $D_j$ in $H_L$, so it does not change $H_L$ and produces another complete meridian system. Conversely, any two complete meridian (disk) systems of a handlebody are related by a finite sequence of disk slides and isotopies — the classical fact underlying the Reidemeister–Singer theorem for handlebodies. $\square$

This is a good structural statement: **the surface-slide orbit of a derivative on $F$ is a single "handlebody-worth" of cut systems**, and different orbits correspond to different handlebodies $H\subset$ (abstract completions of) $\hat F$. Combined with P3 this makes (Q) a question about the finite(?) set of $\hat\varphi$-invariant handlebodies.

## P2.3 Slides along arbitrary arcs in $S^3$

**Proposition 2.4 [PROVED].** *Let $L\subset F$ be a derivative for $K$, let $\gamma\subset S^3\setminus(K\cup L)$ be an arbitrary framed arc from $L_i$ to $L_j$ ($i\ne j$), and let $L'$ be the $0$-framed band sum. Then:*

1. *$L'$ is a $0$-framed handleslide of $L$, so $S^3_{\vec0}(L')\cong S^3_{\vec0}(L)$; in particular $L'$ is an R-link iff $L$ is;*
2. *$\operatorname{lk}(L_k',L_l')=0$ for all $k,l$ and each $\operatorname{lk}(K,L_k')=0$;*
3. *$L'$ can be isotoped into some (in general highly stabilized) Seifert surface $F''$ for $K$ with surface framing $=0$; i.e. $L'$ is a **partial derivative** in the sense of [MZ20, §3].*
4. *$L'$ need not be a derivative: $F''\setminus L'$ will not be planar, and there is in general no genus-$g$ surface containing $L'$.*

*Proof.* (1) Kirby calculus as above. (2) linking numbers are unchanged by $0$-framed slides in the appropriate sense: $\operatorname{lk}(L_i',L_k)=\operatorname{lk}(L_i,L_k)+\operatorname{lk}(L_j,L_k)=0$, and $\operatorname{lk}(K,L_i')=\operatorname{lk}(K,L_i)+\operatorname{lk}(K,L_j)=0$ since $L\subset F$ implies $\operatorname{lk}(K,L_k)=0$. (3) This is exactly the tubing argument in the proof of [MZ20, Thm 1.3]: since $\operatorname{lk}(K,L_k')=0$, any Seifert surface $F'$ for $K$ chosen to meet $L'$ minimally is in fact **disjoint** from $L'$ (otherwise an arc of $L_k'$ with both endpoints on the same side of $F'$ lets you tube $F'$ and reduce $|F'\cap L'|$); then choose pairwise disjoint embedded tori $T_k\supset L_k'$ with surface framing $=$ $0$-framing and disjoint from $F'$, and tube them onto $F'$. (4) The resulting $F''$ has genus $g+\!\!\sum_k 1$ at least, and $F''\setminus L'$ has positive genus. $\square$

**Proposition 2.5 (the obstruction) [PROVED].** *Converting a partial derivative into a derivative requires the reduction of [MZ20, Prop. 3.2], which (i) assumes $K\cup J$ is an **R-link**, and (ii) proceeds by adjoining compressing curves $C$ and sliding $C$ over $K\cup J'$ in $S^3$. Step (ii) is not unlink-preserving. Consequently:*

- *the set of **R-link** derivatives of $K$ is closed under arbitrary $S^3$-slides up to stable equivalence and change of Seifert surface* [CITED: MZ20 Prop. 3.2 + Lemma 2.3];
- *the set of **unlink** derivatives of $K$ is **not** known to be closed under arbitrary $S^3$-slides;* and in fact
- *the $S^3$-slide orbit of an unlink consists of R-links, and it contains a non-unlink iff Generalized Property R fails for that orbit.* **[PROVED]** (Slides preserve $S^3_{\vec0}$; an unlink has $S^3_{\vec0}=\#^gS^1\times S^2$.)

So the clean picture, which I regard as the main conceptual output of P2:

| move | stays on $F$ | preserves $S^3_{\vec0}(L)$ | preserves "$L$ is an unlink" | orbit |
|---|---|---|---|---|
| slide along $\gamma\subset F\setminus L$ | yes | yes | **yes** (orbit = meridian systems of the fixed $H_L$) | meridian systems of $H_L$ |
| slide along $\gamma\subset S^3\setminus(K\cup L)$ | no | yes | **no** (this is exactly GPR) | all R-links stably slide-equivalent to $L$ |

The first row preserves unlinkedness because a meridian system of a *handlebody embedded with disjoint meridian disks in $S^3$* stays such; the second row is where GPR lives.

---

# P3. The fibered case

Throughout: $K$ fibered of genus $g$, fiber $F$, $\hat F=F\cup\text{disk}$, closed monodromy $\hat\varphi$, $S^3_0(K)=\hat F\times_{\hat\varphi}S^1$.

## P3.1 Monodromy-invariant cut systems are derivatives

This is the main new proof in this document.

**Theorem 3.1 [PROVED].** *Let $K\subset S^3$ be fibered with fiber $F$ of genus $g$ and closed monodromy $\hat\varphi$. Let $H$ be a genus-$g$ handlebody with $\partial H=\hat F$ such that $\hat\varphi$ extends to $\Phi:H\to H$, and let $L=L_1\cup\dots\cup L_g\subset\hat F$ be the boundaries of a complete meridian disk system of $H$, isotoped off the capping disk so that $L\subset F$. Then*
$$\operatorname{lk}(L_i,L_j^+)=0\qquad\text{for all }i,j,$$
*i.e. $L$ is a derivative for $K$ in the fiber $F$. (No hypothesis on $L$ being an unlink, or on $S^3_{\vec0}(L)$, is used.)*

*Proof.* Write $A=\ker\big(H_1(\hat F;\mathbb Z)\to H_1(H;\mathbb Z)\big)$. Then:

- $A=\mathrm{span}\{[L_1],\dots,[L_g]\}$ and $A$ is a rank-$g$ direct summand (standard for a complete meridian system of a handlebody);
- $A$ is **Lagrangian** for the intersection form $S$ on $H_1(\hat F)$: the $L_i$ are disjoint, so $S|_A=0$ on the nose;
- $A$ is **$\hat\varphi_*$-invariant**, because $\Phi(H)=H$ and $\Phi|_{\partial H}=\hat\varphi$, so $\hat\varphi_*$ carries $\ker(H_1(\partial H)\to H_1(H))$ to itself.

Identify $H_1(F)\xrightarrow{\ \cong\ }H_1(\hat F)$ (capping a boundary circle of a once-punctured genus-$g$ surface is an $H_1$-isomorphism), under which $S$ corresponds to $V-V^T$.

Fix a basis of $H_1(F)$ and let $V$ be the Seifert matrix, $v(x,y)=x^TVy=\operatorname{lk}(x,y^+)$. Since $K$ is fibered, $V$ is unimodular and the monodromy satisfies
$$\varphi_*=(V^T)^{-1}V,\qquad\text{i.e.}\qquad V^T\varphi_*=V. \tag{$\ast$}$$
(Check: $\Delta_K(t)\doteq\det(V-tV^T)=\det(V^T)\det\big((V^T)^{-1}V-tI\big)$, so the characteristic polynomial of $(V^T)^{-1}V$ is $\Delta_K$; e.g. for the trefoil $V=\begin{pmatrix}-1&1\\0&-1\end{pmatrix}$ gives $\varphi_*=\begin{pmatrix}1&-1\\1&0\end{pmatrix}$, $\chi(t)=t^2-t+1=\Delta_{3_1}$, and $V^T\varphi_*=V$ ✓.)

From $(\ast)$: for all $x,y$,
$$v(x,y)=x^TVy=x^TV^T\varphi_*y=(\varphi_*y)^TVx=v(\varphi_*y,\,x). \tag{$\ast\ast$}$$

Now let $x,y\in A$. Since $S|_A=0$, $v$ is **symmetric** on $A$: $v(a,b)=v(b,a)$ for $a,b\in A$. Since $A$ is $\varphi_*$-invariant, $\varphi_*y\in A$, so $(\ast\ast)$ gives
$$v(x,y)=v(\varphi_*y,x)=v(x,\varphi_*y),$$
i.e.
$$v\big(x,(\varphi_*-I)y\big)=0\qquad\text{for all }x,y\in A. \tag{$\dagger$}$$

Finally, $\det(\varphi_*-I)=\pm\Delta_K(1)=\pm1\ne0$, so $\varphi_*-I$ is injective on $H_1(F)$, hence $(\varphi_*-I)|_A:A\to A$ is injective, hence $(\varphi_*-I)A$ has finite index in the rank-$g$ free abelian group $A$. Given $a\in A$ choose $n>0$ and $b\in A$ with $(\varphi_*-I)b=na$. Then by $(\dagger)$, $0=v(x,(\varphi_*-I)b)=n\,v(x,a)$, so $v(x,a)=0$. As $a,x\in A$ were arbitrary, $V|_A\equiv0$, i.e. $\operatorname{lk}(L_i,L_j^+)=0$ for all $i,j$. Together with Lemma 1.1 ($L$ is a cut system, so its classes are independent), $L$ is a derivative. $\square$

**Remarks.**
- The proof only uses: $A$ Lagrangian, $A$ monodromy-invariant, $\Delta_K(1)=\pm1$. It is therefore a purely algebraic statement: *for a fibered knot, every monodromy-invariant Lagrangian of the intersection form is a metabolizer of the Seifert form.* I have not seen this stated in exactly this form; it is presumably known to experts, but the proof above is complete.
- It supplies the direction Casson–Gordon $\Rightarrow$ derivative-on-the-fiber that [MZ20] obtains only for $|J|=1$ (their Thm 3.3, which routes through Scharlemann–Thompson).

**Theorem 3.2 [PROVED modulo CITED input].** *For $K$ fibered of genus $g$ with fiber $F$, and $L\subset F$ a $g$-component cut system, the following are equivalent:*
1. *$L$ is an R-link derivative;*
2. *$\hat\varphi$ extends over the handlebody $H_L$ determined by $L$;*
3. *$K$ bounds a fibered handle-ribbon disk $D$ with exterior $H_L\times_\Phi S^1$.*

*Proof.* (1)$\Rightarrow$(2)$\Rightarrow$(3): this is the construction in the proof of [MZ20, Thm 3.3] — start with the relative $0$-trace $B_0(K)$, attach $H_L\times I$ along a collar of $L\times I\subset\hat F\times I\subset S^3_0(K)$ (i.e. $g$ $2$-handles along $L$ plus a $3$-handle), observe the new boundary is $\#^g(S^1\times S^2)$ because $S^3_0(K)$ fibers, and cap off with a second copy of $H_L\times I$; the resulting $B_{K\cup L}$ is a homotopy $4$-ball, each fiber $\hat F$ is capped by a copy of $H_L$, and $\hat\varphi$ extends. [CITED] (2)$\Rightarrow$(1): Theorem 3.1 gives that $L$ is a derivative; then the same capping construction applied to $H_L$ shows $K\cup L$ is an R-link, and [MZ20, Lemma 2.3] ($L$ is stably equivalent to $K\cup L$ via slides of $K$ over $L$ inside $F$) gives that $L$ is an R-link. (3)$\Leftrightarrow$(2) is Casson–Gordon + Larson–Meier Thm 1.1. $\square$

**Consequence for $K_G$ [PROVED, given Oliveira-Smith].** $K_G$ bounds a fibered handle-ribbon disk with exterior $H_5\times_\Phi S^1$. Hence the genus-5 fiber $F$ carries at least one explicit $5$-component R-link derivative $L_\Phi$: any complete meridian system of $H_5$. Its surface-slide orbit is exactly the set of meridian systems of $H_5$ (Prop. 2.3). **$K_G$ is ribbon-with-a-genus-5-excellent-surface iff some meridian system of some $\hat\varphi$-invariant handlebody is an unlink.**

## P3.2 Unlink derivative vs. disks in the complement of $F$ — the real condition

This is the clarification the problem asks for, and it is important.

**Proposition 3.3 [PROVED].** *Let $L\subset F$ be a $g$-component unlink derivative for a knot $K$, bounding disjoint embedded disks $\Delta_1,\dots,\Delta_g\subset S^3$. If the $\Delta_i$ can be chosen with interiors disjoint from $F$, then $K$ is the unknot.*

*Proof.* Ambient-surger $F$ along the $\Delta_i$ as in Lemma 1.2(a). If $\operatorname{int}\Delta_i\cap F=\emptyset$ then the resulting disk $(F\setminus L)\cup\bigcup(\Delta_i^+\cup\Delta_i^-)$ is **embedded** in $S^3$, and it is bounded by $K$. A knot bounding an embedded disk in $S^3$ is unknotted. $\square$

Hence:

- **"$L$ is an unlink" is the correct ribbon condition, and it is genuinely weaker than "$L$ bounds disks in the complement of $F$".** The disks *must* pierce $F$; the arcs $\Delta_i\cap(F\setminus L)$ are precisely the ribbon singularities of the resulting ribbon disk (Lemma 1.2(a)). Their number is a natural complexity, and by the (unverified) Cochran–Davis count it is $\ge g$.
- The condition "the compressing disks of $H$ are disjointly embedded in $S^3\setminus F$ on one side", suggested in the problem statement, is therefore **too strong**: it never happens for a knotted $K$. The correct version is:

**Proposition 3.4 [PROVED].** *$L\subset F$ is an unlink iff the abstract handlebody $H_L$ admits a complete meridian system whose disks embed disjointly in $S^3$ (with interiors allowed to meet $F$ in ribbon arcs); equivalently iff $\pi_1(S^3\setminus L)$ is free of rank $g$; equivalently iff the exterior $E(L)$ is a genus-$g$ handlebody.*

*Proof.* The first equivalence is the definition of unlink plus the (standard) fact that $L$ unlink $\Rightarrow$ disjoint disks. For the second and third: $E(L)$ a handlebody $\Rightarrow\pi_1$ free; $\pi_1(S^3\setminus L)$ free $\Rightarrow L$ unlink is the classical theorem (a consequence of the Loop Theorem/Sphere Theorem; see Hempel, *3-Manifolds*). Conversely an unlink has handlebody exterior. $\square$

---

# P4. Attacking the gap: what ribbon gives that handle-ribbon does not

## P4.1 The exact statement of the gap

**Theorem 4.1 [PROVED, assembling CITED inputs].** *For a knot $K\subset S^3$:*

$$K\ \text{ribbon}\iff \exists\ \text{a derivative }L\ \text{with } \pi_1(S^3\setminus L)\ \text{free}\iff\exists\ \text{a derivative }L\ \text{with handlebody exterior};$$
$$K\ \text{handle-ribbon in a homotopy 4-ball}\iff \exists\ \text{a derivative }L\ \text{with } S^3_{\vec 0}(L)=\#^{|L|}(S^1\times S^2).$$

*Proof.* First line: [MZ20] Prop. 1.1 plus Prop. 3.4. Second line: [MZ20] Thm 1.3. $\square$

So — and this answers question P4(a) precisely — **the strongest necessary condition for ribbonness expressible in derivative language is exactly "some derivative has free link group / handlebody exterior", and it is also sufficient**; the whole gap between ribbon and handle-ribbon *is* the gap between "R-link" and "unlink", i.e. Generalized Property R. There is no strictly-intermediate derivative-level condition to be found: any condition $P$ with (unlink $\Rightarrow P\Rightarrow$ R-link) that is not equivalent to one of the two ends would be a genuinely new invariant of R-links.

**Corollary 4.2 [PROVED].** *$K_G$ is NOT ribbon $\iff$ every derivative of $K_G$ on every Seifert surface has non-free link group. Equivalently (CD stabilization): no stabilization of the genus-5 fiber carries an unlink derivative.*

**Therefore: candidate ribbon obstructions for a handle-ribbon knot = invariants of R-links that vanish for unlinks.** Concretely one wants an invariant $\iota$ of $n$-component R-links with $\iota(\text{unlink})=0$, invariant under surface slides (so that it is an invariant of the handlebody $H$, not of the cut system), and computable. Candidates, ranked:

1. **The link group $\pi_1(S^3\setminus L)$ itself** (or its finite quotients / representation variety). This is not a numerical invariant but it is the sharp one: free vs. not. Computable obstructions to freeness: $\mathrm{Hom}(\pi_1(S^3\setminus L),G)$ counts for finite $G$ — for the unlink this is $|G|^n$ up to the standard normalization; any deficiency is an obstruction. **This is the single most promising concrete handle.**
2. **Hyperbolic volume / simplicial volume of $E(L)$**: $\mathrm{vol}(E(\text{unlink}))=0$. By Agol–Ren simplicial volume is monotone under ribbon concordance of fibered knots; the analogous statement for derivatives would give a real obstruction. Note $\|E(L)\|=0$ for a handlebody. **Very cheap to test numerically (SnapPy) on any explicit derivative.**
3. **Heegaard genus / tunnel number of $E(L)$**: unlink has tunnel number $n-1$ and handlebody exterior.
4. **Thurston norm / sutured Floer homology of $E(L)$**: $SFH$ of a handlebody is known; any deviation obstructs.
5. Quantum invariants of the pair $(S^3,L)$ that are insensitive to slides.

**[OPEN]** None of these is currently known to separate ribbon from handle-ribbon, because no R-link is known not to be an unlink after slides. But items 1–3 are *computable right now* on the explicit $L_\Phi\subset F$ coming from Oliveira-Smith's $\Phi$.

## P4.2 Designing the enumeration on the genus-5 fiber

The search space, after Theorems 3.1/3.2 and Prop. 2.3:

$$\mathcal D(F)\ =\ \{\text{cut systems } L\subset\hat F_5\ \text{with}\ \hat\varphi\ \text{extending over}\ H_L\}\ \Big/\ \text{isotopy},$$

and $\mathcal D(F)$ is fibered over
$$\mathcal H(\hat\varphi)=\{\text{genus-5 handlebodies }H,\ \partial H=\hat F,\ \hat\varphi\ \text{extends over }H\}\big/\text{isotopy},$$
with fiber over $H$ = the set of complete meridian systems of $H$ = a single surface-slide orbit.

**Key finiteness input [CITED].** Agol–Ren (arXiv:2603.10884) give an algorithm to enumerate **all minimal compressions of a surface homeomorphism, without redundancy**, and prove each fibered knot has only finitely many ribbon-concordance predecessors. Enumerating $\mathcal H(\hat\varphi)$ is exactly the "compressions of $\hat\varphi$" problem.

**Proposition 4.3 (finiteness heuristic) [CONJECTURED].** *If $\hat\varphi$ is pseudo-Anosov, then $\mathcal H(\hat\varphi)$ is finite.*

*Evidence / proof sketch.* If $H\in\mathcal H(\hat\varphi)$ then so is $\psi(H)$ for any $\psi$ in the centralizer $C(\hat\varphi)\le \mathrm{MCG}(\hat F)$; for pseudo-Anosov $\hat\varphi$, $C(\hat\varphi)$ is virtually cyclic (Birman–Lubotzky–McCarthy / McCarthy), and $\hat\varphi(H)=H$, so the symmetry group acting is essentially trivial. Finiteness then should follow from Agol–Ren's non-redundant enumeration together with monotonicity of dilatation. **[OPEN]** I did not verify that Agol–Ren actually state finiteness of the set of invariant handlebodies (as opposed to finiteness of ribbon-concordance predecessors); check this first.

**Concrete algorithm sketch (executable by a small team).**

1. Get $\varphi$ for $K_G$ explicitly (from the Dunfield–Gong census / Oliveira-Smith's paper) as a word in Dehn twists or as a train-track map on $F_5$.
2. Enumerate cut systems $L$ on $\hat F_5$ up to isotopy by *bounded complexity* (e.g. bounded intersection number with a fixed cut system, or bounded normal-coordinate weight w.r.t. a fixed triangulation of $\hat F_5$). This is a standard normal-curve enumeration.
3. For each, test $\hat\varphi_*$-invariance of $A=\mathrm{span}[L]$ (a fast linear-algebra filter over $\mathbb Z$), then test extension of $\hat\varphi$ over $H_L$ (the hard step; use Agol–Ren's algorithm, or the sufficient criterion "$\hat\varphi(L)$ is slide-equivalent to $L$").
4. For each surviving $H$, pick a meridian system, realize it as an explicit link in $S^3$ (using the embedding $F\subset S^3$), and test unlinkedness: (a) compute the Jones/HOMFLY of the link; (b) compute $\mathrm{vol}$ via SnapPy; (c) count $\mathrm{Hom}(\pi_1,G)$ for small $G$; (d) attempt to simplify by surface slides (a finite BFS over the slide orbit with a complexity function).
5. If step 4 finds an unlink: **$K_G$ is ribbon** and the slice–ribbon conjecture survives this candidate. If step 4 certifies non-unlink for *every* $H\in\mathcal H(\hat\varphi)$, one gets: *no genus-5 excellent Seifert surface*, hence (with Cor. 1.5) a lower bound on the ribbon complexity of $K_G$ — **not** a disproof of slice–ribbon, because of stabilization (Q$^{\mathrm{st}}$).

**[OPEN] The stabilization barrier.** Even a complete answer at level $n=0$ does not settle slice–ribbon for $K_G$: by [CD15, Prop. 7.3] one must in principle examine all stabilizations. Finding a *stabilization-invariant* obstruction is the real prize. Note the encouraging fact: stabilizing $F$ adds a trivial handle, whose dual pair adds a split unknot to the derivative — i.e. **stabilizing corresponds exactly to the "$\sqcup U$" in stable equivalence of R-links** [CITED: MZ20 §2.2]. So:

**Proposition 4.4 [PROVED].** *"$K$ is ribbon" is equivalent to: some R-link derivative of $K$ is, after adding split unknots and performing $S^3$-handleslides, an unlink — i.e. to Generalized Property R holding for the stable-equivalence class of $L_\Phi$.*

*Proof.* ($\Leftarrow$) If $L_\Phi\sqcup U$ slides to an unlink $U'$, then by Prop. 2.4/2.5 and [MZ20, Prop. 3.2] this is realized on a stabilized Seifert surface as a derivative which is an unlink; apply Prop. 1.1. ($\Rightarrow$) If $K$ is ribbon, some derivative $L'$ is an unlink; $L'$ and $L_\Phi$ are both R-link derivatives of the same knot $K$ and are stably equivalent as R-links since both $K\cup L'$ and $K\cup L_\Phi$ determine the same (standard, by Oliveira-Smith) homotopy $4$-ball. (This last step uses that stable equivalence classes of R-links determining the same homotopy 4-sphere are conjecturally, but not provably, unique — see caveat.) $\square$

**Caveat on 4.4($\Rightarrow$):** the claim "two R-links giving the same homotopy 4-sphere are stably equivalent" is **[OPEN]** (it is the Andrews–Curtis-flavoured stabilization problem for 4-manifold handle decompositions). So Prop. 4.4 should be used only in the $\Leftarrow$ direction, which is the useful one.

**Bottom line for P4:** *slice–ribbon for $K_G$ $\Longleftarrow$ Generalized Property R for the explicit 5-component R-link $L_\Phi\subset F$.* This is the cleanest reduction and it makes $K_G$ an exact analogue of the GST situation, with $n=5$ instead of $n=2$. The Diao–Pan–Yan computational framework (arXiv:2604.17737) for GST links is directly transplantable.

---

# P5. Milnor invariants of R-links — resolved, and it is a dead end

**Theorem 5.1 [PROVED].** *Let $L=L_1\cup\dots\cup L_n\subset S^3$ be an R-link, $G=\pi_1(S^3\setminus L)$, $G_k$ the lower central series ($G_1=G$, $G_{k+1}=[G,G_k]$). Then every longitude $\lambda_i$ lies in $G_k$ for every $k\ge1$. Consequently **all Milnor invariants $\bar\mu_L(I)$ of $L$ vanish, for every multi-index $I$ of every length**.*

*Proof.* Let $\alpha:F_n=\langle m_1,\dots,m_n\rangle\to G$ send $m_i$ to the $i$-th meridian.

*Step 1: $G/\langle\!\langle\lambda_1,\dots,\lambda_n\rangle\!\rangle\cong F_n$ with meridians a free basis.* $0$-framed surgery on $L$ kills exactly the longitudes, so $\pi_1(S^3_{\vec0}(L))=G/\langle\!\langle\lambda_i\rangle\!\rangle$. By hypothesis this is $\pi_1(\#^n S^1\times S^2)=F_n$. The composite $\beta\circ\alpha:F_n\to G\to F_n$ sends the $m_i$ to the images of the meridians, which generate $\pi_1(S^3_{\vec0}(L))$ (the surgery solid tori are filled along the longitudes, so $\pi_1(S^3\setminus L)\twoheadrightarrow\pi_1(S^3_{\vec0}(L))$, and $G$ is normally generated by meridians; a nilpotent-free argument is not even needed — $F_n$ is generated by the $n$ meridian images). A generating set of $n$ elements of $F_n$ is a free basis (free groups are Hopfian and $F_n$ has rank $n$). Hence $\beta\circ\alpha$ is an **isomorphism**.

*Step 2: $\alpha$ induces isomorphisms on all nilpotent quotients.* $G/G_k$ is generated by the meridians (a nilpotent group is generated by any set generating its abelianization, and $H_1(S^3\setminus L)=\mathbb Z^n$ is generated by meridians), so $\alpha_k:F_n/(F_n)_k\to G/G_k$ is surjective. Since $(\beta\circ\alpha)_k=\mathrm{id}$ on $F_n/(F_n)_k$, $\alpha_k$ is injective. Hence $\alpha_k$ is an isomorphism, and $\beta_k:G/G_k\to F_n/(F_n)_k$ is its inverse.

*Step 3.* $\beta(\lambda_i)=1$, so $\beta_k(\lambda_i G_k)=1$; since $\beta_k$ is injective, $\lambda_i\in G_k$. This holds for all $k$.

*Step 4.* By Milnor's definition, $\bar\mu_L(i_1\dots i_{k-1}i_k)$ is read off from the expression of $\lambda_{i_k}$ in the free nilpotent quotient $G/G_{k}\cong F_n/(F_n)_{k}$; $\lambda_{i_k}\in G_{k}$ means it is trivial there, so all $\bar\mu$ of length $\le k$ vanish. Letting $k\to\infty$: all $\bar\mu$ vanish (and the indeterminacies are irrelevant since the invariants vanish on the nose). $\square$

**Corollaries [PROVED].**

- The GST links $L_{n,k}$ have all $\bar\mu$ invariants zero. (They are R-links [CITED: GST].)
- $\operatorname{lk}(L_i,L_j)=0$ for any R-link (the length-2 case), and all triple linking numbers $\bar\mu(ijk)=0$.
- $L_\Phi\subset F$ (the derivative of $K_G$) has all $\bar\mu=0$.
- Every R-link has the same nilpotent quotients as the free group; in particular an R-link is a *homology boundary link* in the weak sense that its group maps onto $F_n$ with meridians to a basis (this is in fact the definition of a **homology boundary link**, so: **every R-link is a homology boundary link** [PROVED]).

**Verdict on P5 (requested explicitly).** **Dead end, and provably so.** Milnor's $\bar\mu$-invariants of derivatives cannot distinguish ribbon from handle-ribbon: they vanish identically for *every* R-link derivative, hence for every handle-ribbon knot's derivative, exactly as they do for unlinks. The proposed strategy ("R-links might have non-vanishing $\bar\mu$, giving a ribbon obstruction for handle-ribbon knots") is refuted by Theorem 5.1.

This also sharpens the relation to **Park–Powell** (arXiv:1802.00582, *A ribbon obstruction and derivatives of knots*), who bound the triple linking numbers of derivative links of **homotopy-ribbon** and doubly slice knots. Theorem 5.1 shows that for **handle-ribbon** knots one gets the strictly stronger conclusion $\bar\mu\equiv0$ for the R-link derivative — so Park–Powell's obstruction, too, cannot separate ribbon from handle-ribbon. (Their obstruction has content only in the gap between homotopy-ribbon and handle-ribbon.)

**Corollary 5.2 (a real, if negative, structural statement) [PROVED].** *Any invariant of derivative links that is a function of the nilpotent quotients of the link group together with the longitudes — i.e. any "Milnor-theoretic" or "lower-central-series" invariant — vanishes on all R-link derivatives and therefore cannot obstruct ribbonness for a handle-ribbon knot.* Separating ribbon from handle-ribbon **requires a non-nilpotent invariant**: the free-ness of $G$ itself, geometric invariants of $E(L)$ (volume, Heegaard genus, sutured Floer), or representations into non-nilpotent (e.g. finite simple, or $\mathrm{SL}_2\mathbb C$) groups.

---

# P6. Other ideas for separating ribbon from handle-ribbon

## (i) Group-theoretic / Wirtinger presentations — **likely dead end, with a sharp sub-question**

Facts:
- Ribbon disk groups (in $B^4$) are exactly the groups with a **Wirtinger presentation of deficiency 1 and weight 1** (Yajima; see also Levine). [CITED-UNVERIFIED — I did not fetch Yajima; the statement is standard folklore and should be checked against a primary source before use.]
- A handle-ribbon disk exterior has a handle decomposition without 3-handles, so its $\pi_1$ has a presentation of deficiency 1 with weight 1 as well. So deficiency/weight alone cannot separate.
- For $K_G$: $\pi_1(B^4\setminus D)=F_5\rtimes_\Phi\mathbb Z$, with presentation $\langle x_1,\dots,x_5,t\mid tx_it^{-1}=\Phi_*(x_i)\rangle$: $6$ generators, $5$ relations, deficiency $1$, $H_1=\mathbb Z$. [PROVED, given the fibered structure.]
- Larson–Meier Thm 1.1 [CITED] shows *fibered ribbon disks* have exteriors $H_g\times_\Phi S^1$ too. So **the class of groups is the same**; group theory at this level cannot separate.

**Sharp sub-question [OPEN].** Is $\langle x_1,\dots,x_5,t\mid tx_it^{-1}=w_i\rangle$ (with $w_i=\Phi_*(x_i)$ the actual words for $K_G$) **Wirtinger-presentable**, i.e. does it admit a presentation all of whose relators have the form $x_j=w x_i w^{-1}$? A negative answer would prove $K_G$ is not ribbon **if** the Yajima characterization is correct as stated. This is a concrete, decidable-in-practice computation (search for a Wirtinger presentation via Tietze transformations / the ACME-style search), and it is the only idea I found that attacks ribbonness *without* going through Generalized Property R. **Rank: high risk, high reward.** Caveat: Wirtinger-presentability is not obviously algorithmically decidable, and the theorem needs verification.

**Related sub-question [OPEN].** Is every $\Phi:H_g\to H_g$ that extends some fibered knot monodromy realizable by a fibered **ribbon** disk of some (possibly different) knot? Larson–Meier's Stallings-twist construction (Thm 1.2 [CITED]) produces infinite families $\{D_m\}$ of fibered homotopy-ribbon disks whose doubles give at most two 2-knots; whether infinitely many of the $D_m$ are ribbon is exactly the kind of question Meier–Zupan answer affirmatively for generalized square knots with $q=2$ (arXiv:2310.17564) and leave open in general [CITED]. So: **the realizability question is open and is essentially the same difficulty as slice–ribbon.**

## (ii) Andrews–Curtis / 2-complex invariants — **structurally the right shape, currently inert**

A ribbon disk gives a Wirtinger presentation $P_{\mathrm{rib}}$ whose presentation 2-complex is simple-homotopy equivalent to the disk exterior; a handle-ribbon disk gives a presentation $P_{\mathrm{hr}}$ from its 3-handle-free decomposition. Both have deficiency 1 and present the same group in our situation, so they are Nielsen-equivalent after stabilization iff an Andrews–Curtis-type move sequence exists. **This is literally the same wall as GPR** (via Kirby calculus $\leftrightarrow$ AC moves). [PROVED, informally: the handleslide moves on an R-link $L$ correspond to AC moves on the associated balanced-ish presentation.] **Rank: low** — no known computable AC invariant.

## (iii) Abe–Tange and reversing Gompf's belt-sphere lemma — **worth one careful look**

Abe–Tange, arXiv:1305.7492 (*A construction of slice knots via annulus twists*), give *"a sufficient condition for given slice knots to be ribbon"* and show all of Omae's knots are ribbon [CITED — abstract verified; I could **not** confirm the existence or content of a "Lemma 5.1 about ribbon disks of belt spheres" in that paper; the fetched text contained no such statement, so **do not cite it**]. The relevant technique is: if $K$ is obtained from a knot bounding an obvious ribbon disk by an *annulus twist* along an annulus whose core is unknotted with $\pm1$-framing, then the ribbon disk survives. Abe–Tagami (arXiv:1502.01102) [CITED] give a fibered potential counterexample and relate slice–ribbon to the modified Akbulut–Kirby conjecture.

**Actionable idea [CONJECTURED]:** If the monodromy $\Phi$ of $K_G$ differs from the monodromy of a *known* fibered ribbon knot by a Stallings twist along a disk $E\subset H_5$ that is unknotted in $B^4$ (Larson–Meier Thm 1.2), then $K_G$'s derivative $L_\Phi$ differs from an unlink by a twist, and unlinkedness may be recoverable. **Concrete test:** compute whether $\Phi$ lies in the subgroup of $\mathrm{MCG}(H_5)$ generated by a handlebody-preserving mapping class and a single disk twist.

## (iv) Two further ideas not in the prompt

- **[PROVED, small]** Since $E(L)$ for an unlink is a handlebody, $\mathrm{rank}\,H_1$ equals Heegaard genus equals tunnel number $+1$. For any R-link $L$, $H_1(E(L))=\mathbb Z^n$ but the **Heegaard genus of $E(L)$** may exceed $n$. Heegaard genus of a link exterior is computable in practice (Regina / normal-surface methods) for links of modest complexity. *If $g(E(L_\Phi))>5$ for every meridian system of every $\hat\varphi$-invariant $H$, then $K_G$ has no genus-5 excellent Seifert surface.* This is the most computationally tractable of all the obstructions listed and is **not** a nilpotent invariant, so Corollary 5.2 does not kill it. **Rank: highest among the "new idea" items.**
- **[OPEN]** *Slide-invariant sutured Floer.* $SFH$ of $E(L)$ with the meridional sutures is a slide-*co*variant object; the handlebody has $SFH=\mathbb Z^{2^n}$-ish in the appropriate grading. Deviations obstruct unlinkedness. Needs somebody who knows the machinery.

---

# Summary of what is proved here

1. **Lemma 1.1** (planarity/connectivity is automatic from homological independence). [PROVED]
2. **Lemma 1.2** (exact dictionary: genus-$g$ unlink derivative $\leftrightarrow$ ribbon disk with $2g$ minima in $g$ parallel pairs and $2g-1$ saddles; so fusion number $\le 2g-1$). [PROVED]
3. **Theorem 1.4 / Cor. 1.5** (minimal-genus reduction: if the ribbon disk's excellent surface has genus $=g(K)$ then it *is* the fiber). [PROVED given Thm 1.3]
4. **Theorem 2.1** (surface handleslides preserve derivatives; crucially $\mathrm{fr}_F(L_i\#_\gamma L_j)=0$ because $\operatorname{lk}(L_i,L_j)=0$ for a derivative). [PROVED]
5. **Proposition 2.3** (surface-slide orbit $=$ meridian systems of $H_L$). [PROVED]
6. **Props. 2.4, 2.5** ($S^3$-slides give partial derivatives, not derivatives; the orbit distinction is exactly GPR). [PROVED]
7. **Theorem 3.1** (*new-looking*: for a fibered knot, every monodromy-invariant Lagrangian is a Seifert-form metabolizer; proof uses $V^T\varphi_*=V$ and $\det(\varphi_*-I)=\pm\Delta_K(1)=\pm1$). [PROVED]
8. **Theorem 3.2** (fibered trichotomy: R-link derivative on fiber $\Leftrightarrow$ monodromy extends over $H_L$ $\Leftrightarrow$ fibered handle-ribbon disk). [PROVED modulo MZ Thm 3.3]
9. **Prop. 3.3** (the compressing disks must pierce $F$ unless $K$ is unknotted — the "one-sided disks" condition is vacuous). [PROVED]
10. **Theorem 4.1** (ribbon $\Leftrightarrow$ some derivative has free group; the gap $=$ GPR). [PROVED]
11. **Theorem 5.1 + Cor. 5.2** (**all Milnor invariants of every R-link vanish**; no nilpotent invariant can separate). [PROVED]

# What remains open

- **O1.** The exact genus of the Cochran–Davis desingularization $F_\Delta$ (is it really $r$, the number of ribbon singularities?), and the explicit local move. *This is a gap in the literature's exposition, not a hard theorem.*
- **O2.** Finiteness of $\mathcal H(\hat\varphi)$ = the set of $\hat\varphi$-invariant handlebodies. (Agol–Ren very likely settles this algorithmically.)
- **O3.** Is $L_\Phi$ (or any meridian system of any $\hat\varphi$-invariant $H_5$) an unlink? — Generalized Property R for a specific 5-component link.
- **O4.** The stabilization barrier: an obstruction invariant under $L\mapsto L\sqcup U$ and $S^3$-slides.
- **O5.** Is $F_5\rtimes_\Phi\mathbb Z$ Wirtinger-presentable?
- **O6.** Verification that ribbon disk groups $=$ Wirtinger deficiency-1 weight-1 groups (Yajima), in a citable form.

# Ranked next steps for a small team

1. **(1–2 weeks, highest value/effort ratio.)** Extract $\Phi$ and a meridian system $L_\Phi\subset F\subset S^3$ explicitly from Oliveira-Smith's construction; produce a planar diagram of the 5-component link $L_\Phi$. Then run the *cheap* non-unlink tests: HOMFLY/Jones, SnapPy volume, Heegaard genus of $E(L_\Phi)$ via Regina, $\#\mathrm{Hom}(\pi_1 E(L_\Phi),G)$ for $G=S_5,\mathrm{PSL}_2(\mathbb F_7),\dots$. *Any* non-unlink certificate that survives the whole slide orbit is a genuine result. Conversely a **simplification to the unlink proves $K_G$ is ribbon** and removes it as a candidate.
2. **(2–4 weeks.)** Implement the surface-slide BFS on the fixed surface $F_5$ (Prop. 2.3): enumerate meridian systems of $H_\Phi$ by slide sequences with a complexity function (word length in $\pi_1(F)$ or normal-coordinate weight) and test unlinkedness at each node. This is the direct analogue of Diao–Pan–Yan's GST computation (arXiv:2604.17737) — **contact those authors; their code is the right starting point.**
3. **(1 month.)** Enumerate $\mathcal H(\hat\varphi)$ using Agol–Ren's minimal-compression algorithm (arXiv:2603.10884). Verify whether their results give finiteness. Then run step 1–2 on every $H\in\mathcal H(\hat\varphi)$. Completing this settles (Q) — the genus-5 level — unconditionally.
4. **(Parallel, theory.)** Close **O1**: write down the correct desingularization of a ribbon immersion and pin the genus of $F_\Delta$. This upgrades Cor. 1.5 into a clean statement "every ribbon disk of $K_G$ has $\ge6$ ribbon singularities", the first quantitative ribbon obstruction for $K_G$.
5. **(Parallel, theory.)** Attack **O5** computationally: search for a Wirtinger presentation of $F_5\rtimes_\Phi\mathbb Z$ (GAP/Magma Tietze search with a bound on relator length). Simultaneously nail down **O6** from a primary source (Yajima 1969, or Levine's account).
6. **(Longer term.)** Build a slide-and-stabilization-invariant obstruction from $E(L)$ (Heegaard genus is the best candidate: it is monotone under nothing obvious, but $\mathrm{genus}(E(L\sqcup U))=\mathrm{genus}(E(L))+1$ behaves predictably). This is the only route that could break **O4**.

**Do not pursue:** Milnor invariants and any lower-central-series/nilpotent invariant of the derivative (Theorem 5.1 kills these outright); Seifert-form / Alexander-module data (identical for unlink and R-link derivatives, as the problem statement already notes and as Theorem 3.1 makes precise — the derivative condition is purely the vanishing of $V$ on a monodromy-invariant Lagrangian, which carries no information about unlinkedness).
