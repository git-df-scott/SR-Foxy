# External model critique: mixed lift

This is advisory model output, not a source or a proof. Its suggestions require independent checking.

## Prompt

Audit this narrow algebraic claim skeptically. Do not invent references. Distinguish an algebraic lemma from an unverified software assumption. No tools or repo edits.

We have a finite free bigraded knot Floer complex over S=F2[U,V], with d degree (A,M)=(0,-1), U=(-1,-2), V=(1,0). A calculator returns a minimal free quotient complex over R=S/(UV), with 13 homogeneous generators (ranks equal hat HFK) and no constant arrows. The coefficient of each differential entry is uniquely determined up to its F2 coefficient by the source/target grades. For the particular K1 diagram all generators have delta=M-A either 0 or -2. There are exactly 18 possible missing mixed U^a V^b arrows, from lower delta to higher; none can compose with another. The fixed pure arrows square to zero already over S. d^2=0 imposes rank 10 linear equations, leaving 256 completions. All 256 have exact maps S -> C -> S whose composition is identity; independently verified in plain Python by exhaustive enumeration of all 2^18 assignments. No actual mixed differential is computed.

Questions:
1. Is every actual full complex compatible with this minimal quotient represented by one of these completions? Proposed argument: cancel coefficient-1 arrows in an actual free full complex to obtain the minimal hat-rank model. Such cancellations are finite graded elementary operations. Its quotient is homotopy equivalent to the calculator's minimal R complex; a homotopy equivalence between minimal graded free complexes is a chain isomorphism. Sort basis by delta: U,V both lower delta by 1, so any degree-zero map has block triangular matrices and constant diagonal blocks. Invertibility mod(U,V) therefore implies actual invertibility by a finite nilpotent expansion. Lift the quotient basis-change matrix to S; it is still invertible by the same triangular reasoning. Conjugating the true differential yields the calculator's fixed pure arrows plus the enumerated mixed terms. Where could this fail?
2. If that lifting argument works, what precisely may be concluded from the S summand for an actual knot? It does NOT prove slice: the same phenomenon occurs for the thin tau-zero knot 6_3 with nonsquare determinant 13. Is it justified to say the ordinary local-equivalence obstruction cannot distinguish these two complexes, provided specializing V=1 gives HF^-(S3) for each actual knot? Avoid claiming involutive or all Floer-theoretic obstructions vanish.
3. Give the most valuable falsification check, not broad suggestions.

There is also a uniform splitting formula for every completion in the stored generator labels. The delta-zero part has d(e5)=U e6+V e9, d(e6)=V(e1+e10), d(e9)=U(e1+e10), and e1,e10 cycles. The lower part includes d(e0)=V e2+U e3+mixed, d(e4)=V e2+U e3+mixed, d(e2)=U(e0+e4)+mixed; similarly d(e7)=U e8+V e11+mixed, d(e12)=U e8+V e11+mixed, d(e8)=V(e7+e12)+mixed. All other lower differentials land in generators killed by the following projection. Let alpha be the sum of coefficients of U^2 V e1 and U^2 V e10 in d(e0), and beta the sum of coefficients of U V^2 e1 and U V^2 e10 in d(e7). Include 1->e1 and project e1,e10->1, e2->alpha U^2, e8->beta V^2, all others->0. d^2=0 gives the equal coefficient sums for e4 and e12, so this is a chain retraction. This formula was checked on all 256 completions.


## Response

## 1. The lifting argument

**What it actually proves (this part is a genuine lemma, and it is correct):**

> Let $C$ be a finitely generated free bigraded complex over $S=\mathbb F_2[U,V]$ with $\deg U=(-1,-2)$, $\deg V=(1,0)$, $\deg d=(0,-1)$. Suppose $C\otimes_S R$ ($R=S/UV$) is bigraded homotopy equivalent to the calculator's minimal complex $C_{\mathrm{calc}}$. Then $C$ is homotopy equivalent to some $(S^{13},d')$ with $d'\equiv d_{\mathrm{calc}}\pmod{UV}$ and $d'^2=0$.

Each step checks out:

- Cancellation of constant arrows is valid over any ring (unit entry), preserves bigrading, terminates, and yields $C_{\min}$ with $\operatorname{rank}=\dim\widehat{HFK}$. $C_{\min}\otimes R$ is still minimal because $(UV)\subset(U,V)^2$.
- Minimal $\Longrightarrow$ homotopy equivalence is iso: standard graded-Nakayama, and here you don't even need it in the abstract — the delta-triangularity argument suffices.
- Monomial rigidity is real: $\deg U=(-1,-2)$ and $\deg V=(1,0)$ are $\mathbb Z$-linearly independent, so a bidegree determines $U^aV^b$ uniquely ($a=-M/2$, $b=A+a$). Note the lattice they span has index 2 in $\mathbb Z^2$, so some bidegree gaps admit *no* monomial — the slot count is parity-sensitive.
- Triangularity: for a degree-preserving map, entry $x\to U^aV^b y$ forces $\delta(y)=\delta(x)+(a+b)$, so sorting by $\delta$ gives block-triangular with constant diagonal. With only two $\delta$ levels the strictly-triangular part squares to zero, so $\Phi=D+N$ with $D$ invertible gives $\Phi^{-1}=(I+D^{-1}N)D^{-1}$ exactly. Invertibility mod $(U,V)$ really does imply invertibility over $S$.
- The conjugation step is cleaner than stated: $\tilde\Phi$ need not be a chain map and the lift need not be canonical. Reduction mod $UV$ is a ring map, so $\tilde\Phi d\tilde\Phi^{-1}\bmod UV=\psi d_R\psi^{-1}=d_{\mathrm{calc}}$ automatically. Pure monomials lift uniquely, so the pure part of $d'$ *equals* $d_{\mathrm{calc}}$'s, and the ambiguity is confined to the mixed slots.

Also worth noting the error direction is favorable: you need the 256 to be a **superset** of realizable completions. Over-counting (unrealizable completions included) is harmless; only *under*-counting is fatal. So the risks are exactly the things that could shrink the enumerated set.

**Where it can fail.** Two are software assumptions, three are checkable algebraic facts you have asserted but not (as described) proved:

1. **(Software, unproven, load-bearing for everything.)** Nothing in the argument establishes that $C_{\mathrm{calc}}$ is the $UV=0$ reduction of the true $CFK_{UV}(K_1)$ *with correct absolute bigradings*. A uniform grading shift is harmless; a **relative** grading error is fatal, because it changes which pairs admit a mixed monomial. A convention mismatch (mirror, or $U\leftrightarrow V$) would silently swap $\alpha\leftrightarrow\beta$.
2. **(Software, and the "independent" check is not independent.)** The calculator and the plain-Python enumerator presumably consume the same generator/grading table. Agreement between them rules out arithmetic bugs, not a bad input table.
3. **$d_{\mathrm{pure}}^2=0$ over $S$, not just over $R$.** You assert this. If $d_{\mathrm{pure}}^2$ were a nonzero multiple of $UV$, the $d^2=0$ system becomes *inhomogeneous* — the solution set is then an affine coset (possibly empty), and "rank 10, so 256" is the wrong count.
4. **$\delta\in\{0,-2\}$ for all 13.** This is what makes mixed arrows non-composable and $d^2=0$ linear in the 18 unknowns. A single generator at $\delta=-1$ or $-4$ breaks both the "18 slots" enumeration and the linearity, and $18-10=8$ would no longer be the right dimension count.
5. **The count 18 itself** is a derived fact from the $(A,M)$ table, recomputable by hand. $\delta$ drop of 2 forces $a+b=3$, i.e. only $U^2V$ and $UV^2$ — consistent with your $\alpha,\beta$.

On the splitting formula: the reason $\alpha,\beta$ are defined as *sums* over $e_1,e_{10}$ is structural, and it works — every pure arrow into the top block lands on $e_1+e_{10}$, which the projection sends to $1+1=0$, which is what kills the cross terms in $d^2$. But "$d^2=0$ gives the equal coefficient sums for $e_4$ and $e_{12}$" is only part of what $\pi$ being a chain map needs: you also need the $\sigma$-sum of $U^2V\{e_1,e_{10}\}$ coefficients to vanish in $d(e_2)$, $d(e_8)$, and every other lower generator. $d^2=0$ appears to give this only in *combinations* (e.g. $d^2(e_0)$ couples $d(e_2)$ and $d(e_3)$), not termwise. Treat the uniform formula as a verified property of the 256, not as a proved lemma — which is fine for the conclusion, but don't present it as a proof.

## 2. What may be concluded

$\pi\iota=\mathrm{id}_S$ makes $e=\iota\pi$ an idempotent bigraded chain map, so $C_{\min}\cong S\oplus A$ **as bigraded $S$-complexes**. After inverting $U,V$, both homologies are free of rank 1 and $\pi_*\iota_*=\mathrm{id}$, so $\iota_*$ is multiplication by a unit, hence an iso. Therefore $\iota,\pi$ are local maps and $[C]=[S]$ in the ordinary local equivalence group.

So the justified statement is: **every concordance invariant that factors through the ordinary (non-involutive) local equivalence class of $CFK_{UV}$ vanishes** — $\tau$, $\varepsilon$, $\nu^+$, $V_i$, $\Upsilon\equiv0$, the $\varphi_{i,j}$-type invariants, and large-surgery $d$-invariants agree with the unknot. Equivalently: $K_1$ and $6_3$ are locally equivalent, so no such invariant separates them. That is exactly the right phrasing; do not upgrade it.

Two corrections to the framing:
- The proviso should be **"$H_*(C[U^{-1},V^{-1}])$ is free of rank 1,"** not "$V=1$ gives $HF^-(S^3)$." For a genuine knot complex this is automatic, so it is not an extra hypothesis for $K_1$; it is only needed if you treat the 256 as abstract complexes.
- Also required, and worth confirming explicitly: $\iota$ and $\pi$ must have bidegree exactly $(0,0)$, i.e. $e_1$ and $e_{10}$ sit at $(0,0)$, $e_2$ at $(-2,-4)$, $e_8$ at $(2,0)$. The stated formula is internally consistent with this, but if the checker did not enforce degree-0, the whole retraction search is meaningless.

Untouched: the involutive theory ($\iota_K$, $\bar d/\underline d$), anything using the full homotopy type rather than the local class ($\widehat{HFK}$ ranks, $\Delta_K$, thickness, fiberedness), and all non-Floer obstructions.

## 3. The single most valuable falsification check

**Compute $\det(K_1)$ from the stored bigradings and test Fox–Milnor.** It is already forced by the data you quoted, and it is bad news.

$\Delta_K(t)=\sum_x(-1)^{M(x)}t^{A(x)}$, so $\Delta_K(-1)=\sum_x(-1)^{M(x)+A(x)}=\sum_x(-1)^{\delta(x)}$. You state all 13 generators have $\delta\in\{0,-2\}$ — both even — so **every term is $+1$ and $\det(K_1)=|\Delta_K(-1)|=13$**, with no cancellation possible. A slice knot has $\Delta=f(t)f(1/t)$, hence $\det=f(-1)^2$, an odd square. 13 is not.

So one of these must be true, and the check tells you which:
- the grading table is wrong (some $\delta$ is odd, or the rank isn't 13), which also invalidates the 18-slot enumeration and hence the 256; **or**
- $K_1$ is not slice, and the trivial local class is precisely the $6_3$ phenomenon you already identified — same determinant 13, same conclusion.

Run it as: (a) recompute $\sum(-1)^{M}$ over the 13 generators and confirm $\Delta_K(1)=\pm1$ (7 even-$M$, 6 odd-$M$); (b) recompute $\sum(-1)^{M+A}$; (c) compare $\Delta_K(t)$ against the Alexander polynomial of $K_1$ from a Seifert matrix or Alexander module, computed outside the Floer calculator. Step (c) validates the entire $(A,M)$ table — the sole input to the slot count — against an independent source, which is exactly the assumption the algebra cannot check for itself.

Secondary, cheap, and worth doing once: a **negative control through the identical code path**. Feed the pipeline the $UV=0$ complex of a knot with $\tau\neq0$ and several $\delta$ levels (a torus-knot staircase, where $CFK_{UV}$ is fully known) and require the retraction search to return *no* completion admitting $S\to C\to S$ with $\pi\iota=1$. If the searcher can never say "no" — most likely because it isn't enforcing bidegree $(0,0)$ on $\iota$ and $\pi$ — then "all 256 retract" is vacuous.
