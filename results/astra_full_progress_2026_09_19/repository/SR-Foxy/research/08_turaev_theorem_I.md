# Turaev 1981/1983: recovering A(p,q,r,s) and testing it against classical slice obstructions

Primary source obtained and read: V. G. Turaev, "Multiplace generalizations of the Seifert form of
a classical knot", Mat. Sb. 116(158):3 (1981) 370-397; English translation Math. USSR-Sbornik
44:3 (1983) 335-361. PDF downloaded from mathnet.ru (`paperid=2474`, `what=fullteng`) to
`turaev_eng.pdf` (27 pages). Note: mathnet.ru returns HTTP 403 + a "page does not exist" body to a
default curl UA; a browser User-Agent plus the abstract page as Referer is required.

Labels below: **VERIFIED** = transcribed from a 300-400 dpi rendering of the page that I read
directly; **OCR-ONLY** = taken from the PyMuPDF text layer (mediocre 1983 OCR) without an image
check; **COMPUTED** = produced here by sympy/Sage from VERIFIED input.

---

## 1. The construction

### 1.1 Section 1.5 (p. 339), VERBATIM — VERIFIED (read from page image `p05.png`)

> **1.5. Realization of nil-forms by Seifert surfaces.** It is known (see [11]) that if *A* is a
> sphere with *n* handles and one hole, and if x_1,...,x_{2n} are generators of its fundamental
> group, represented by the loops indicated in Figure 3, then *A* can be imbedded into S^3 in such
> a way that the numbers l_1(x_i, x_j), i <= j, take arbitrary preassigned (integral) values. The
> numbers l_2(x_i, x_j, x_k), for i < j < k, can also take on arbitrary values: the ribbon-linking
> operator illustrated in Figure 4 changes l_2(x_{i_0}, x_{j_0}, x_{k_0}) by 1 and leaves
> unchanged the numbers l_2(x_i, x_j, x_k) for all other i < j < k (see [8]). As regards the
> numbers l_1(x_i, x_j) for i > j and l_2(x_i, x_j, x_k) for i >= j or j >= k, these are determined
> by l_1(x_i, x_j) for i <= j and l_2(x_i, x_j, x_k) for i < j < k by (4)-(6). From this follows,
> in particular, the fact, already established in [11], that a bilinear form l: Z^n x Z^n -> Z is
> isomorphic to the Seifert pairing for a Seifert surface in S^3 if and only if its
> skew-symmetrization alt(l) (i.e., the form (x,y) |-> l(y,x) - l(x,y): Z^n x Z^n -> Z) is
> nonsingular. A similar result holds for nil-forms of degree 3. Let us say that a nil-form
> (l_1, l_2) on a group pi, with values in a commutative ring R, is *special* if the pairing
> l_1^1: H_1(pi)^2 -> R induces a bilinear form l: H_1(pi;R)^2 -> R, with nonsingular
> skew-symmetrization, for which there exists a mapping nu: pi^2 -> H_1(pi;R) such that for the
> natural homomorphism h: pi -> H_1(pi;R) and any alpha, beta, gamma in pi the relations (5) and
> (6) hold with h o lambda replaced by nu and l_1^1 by l. Below (in Section 4) it is shown that nu
> exists if and only if a certain trilinear form H_1(pi;R)^2 -> R, constructed from (l_1,l_2),
> vanishes.

**Important:** section 1.5 contains NO surface called A(p,q,r,s). It is a pure realization
theorem. The surfaces A(p,q,r,s) are introduced on p. 342, *by appeal to* section 1.5 (see 1.3
below). So A(p,q,r,s) is defined only implicitly: it is *any* genus-3 surface realizing the stated
l_1 and l_2 values, which exists by 1.5. There is no picture of A(p,q,r,s) in the paper.

### 1.2 Figures — VERIFIED (I looked at page 339, rendered at 250 dpi)

* **Figure 3** (p. 339): the standard picture of a sphere with n handles and one hole drawn as a
  disk in the plane with 2n bands attached along its boundary, the bands arranged in consecutive
  pairs (1,2), (3,4), ..., (2n-1, 2n); each band is drawn as a loop leaving and returning to the
  boundary, pairs of consecutive bands interlock (each pair forms one handle). 2n oriented core
  loops, labelled 1, 2, 3, 4, ..., 2n-1, 2n, all emanate from a single base point marked on the
  boundary of the disk at the bottom centre, each running once through its band and back; these
  represent the free generators x_1,...,x_{2n} of pi_1(A, a). The "..." indicates the pattern
  repeats for the remaining handles.
* **Figure 4** (p. 339): the *ribbon-linking operator*. Left: three parallel vertical bands
  (each drawn as a doubled/ribbon line), labelled i_0, j_0, k_0 at the bottom. Right: the same
  three bands after the move — the i_0 band is pulled out, made to spiral around and through the
  j_0 and k_0 bands (it crosses over/under them and wraps, a Borromean-type ribbon clasp), and
  returns. Milnor's isotopy-of-links move [8]. This changes l_2(x_{i_0}, x_{j_0}, x_{k_0}) by 1 and
  changes nothing else. **This is the move that installs the parameters r and s.**

### 1.3 The definition of A(p,q,r,s) (p. 341-342), VERBATIM — VERIFIED (page images `page07_low.png`, `p08_top.png`)

> ... For knots of genus >= 3, however, we can show that the conditions listed in Theorem H do not
> reduce to the same conditions on l_1(K). Indeed, for integers p != 0 and q, let X and Y denote,
> respectively, the matrices

```
        | 0   1    0   1   0   0 |            | 0  1  0     0    0     0    |
        | 0   0    p   0   0   0 |            | 1  0  0     0    0     0    |
   X =  | 0   p    0   q   0   1 |      Y =   | 0  0  0    p^-1  0     0    |
        | 1   0   q-1  0   p   0 |            | 0  0  p     0    0     0    |
        | 0   0    0   p   0   0 |            | 0  0  0     0    0    p^-2  |
        | 0   0    1   0  -1   0 |            | 0  0  0     0   p^2    0    |
```

> By the results of Section 1.5, for any integers r and s there exists in S^3 a Seifert surface
> A = A(p, q, r, s), of genus three, such that in the generators x_1,...,x_6 of its fundamental
> group represented by the loops indicated in Figure 3 (with n = 3), l_1(A) is given by the matrix
> X, while l_2(A)(x_1, x_3, x_5) = r, l_2(A)(x_2, x_4, x_6) = s. The form l_1^1(A): H_1(A)^2 -> Z
> is hyperbolic: if i = j (mod 2), then l_1(A)(x_i, x_j) = 0. From the equality Y^T X Y = X^T,
> where T is transposition, it follows that the tensor product of the form l_1^1(A) by Z[1/p] is
> invertible. By Theorem G, the form F_1^c(l_1(dA)) is hyperbolic and invertible.

So: **p, q are the Seifert-form parameters (they alone determine X and hence every classical
invariant); r, s are the Milnor-triple/nil-form parameters, installed by applying the Figure-4
ribbon-linking operator r times to the triple of bands (1,3,5) and s times to (2,4,6). They do not
change the Seifert matrix at all.**

### 1.4 Theorem I (p. 342), VERBATIM — VERIFIED

> **THEOREM I.** *Let p be either unity or a prime natural number, q a natural number, and r and s
> integers, with q != 2 if p = 2. Let K = dA(p, q, r, s), and let L be an oriented (possibly
> trivial) knot in S^3 whose Alexander polynomial is prime to that of K. Then: if r != 0 and
> s != 0, the nil-form F_2^c(l_1(K # L), l_2(K # L)) is not metabolic; if r != 0 or s != 0, it is
> not hyperbolic; and if r = 0 and s != 0, or if r != 0 and s = 0, it is not invertible.*

> Observe that p and q are invariants of the knot dA(p, q, r, s), since its Alexander polynomial is
> rho(x) rho(x^-1), where rho(x) = p x^3 - (p+q) x^2 - (p-q+1) x + p. The numbers r and s, up to
> multiplication by -1 and powers of p, are likewise invariants of the knot (see Section 9). We
> note also that the last part of Theorem I is proved here without recourse to the
> number-theoretical technique used in [14] and [15] to prove noninvertibility of bilinear forms.

### 1.5 Theorem H (p. 341), VERBATIM — VERIFIED

> **THEOREM H.** *Let K be an oriented knot in S^3. Then:*
> *(i) The nil-form (l_1(-K), l_2(-K)), where the minus sign denotes change of orientation for the
> knot, is inverse to (l_1(K), l_2(K)); so that if the knot is invertible, then so is its nil-form
> (i.e., the latter is isomorphic to its own inverse).*
> *(ii) If K is a ribbon knot, then F_2^c(l_1(K), l_2(K)) is metabolic.*
> *(iii) If K is two-sidedly null-cobordant (see [13]), then F_2^c(l_1(K), l_2(K)) is hyperbolic.*

### 1.6 Theorem J (p. 342), VERBATIM — VERIFIED

> The following theorem shows that although slice knots are stably ribbon (see [17]),* Theorem H
> yields no new obstructions to sliceness.
>
> **THEOREM J.** *If (l_1, l_2) is a special nil-form on a group of type (2,Q), with values in Q,
> and if the form l_1^1 is metabolic, then there exists a metabolic special nil-form (m_1, m_2) on
> a group of type (2,Q), with values in Q, such that the nil-form F_2((l_1,l_2) * (m_1,m_2)) is
> also metabolic.*
>
> (* Translator's note. In the translation of [17], p. 250, line -4 should read: "... an arbitrary
> slice knot, added with some ribbon knot, is ribbon.")

**Reading of Theorem J (mine, not the paper's):** J says the nil-form obstruction is *stably*
vacuous: for a knot whose Seifert form is metabolic one can always connect-sum a suitable
(nil-form-realizing) knot to make the nil-form metabolic. Since slice implies "stably ribbon" (K # R
ribbon for some ribbon R, [17]), Theorem H(ii) applied to K # R gives no constraint on K itself.
It does **not** say that a slice knot's own nil-form is metabolic. So H(ii) remains a genuine
obstruction to *K itself* being ribbon / homotopy-ribbon.

### 1.7 Definitions — VERIFIED unless noted

* **nil-form** (Section 1.3, p. 337, OCR-ONLY): a set of maps l_1: pi^2 -> R, ..., l_N: pi^{N+1} -> R
  satisfying relation (2) for all 0 <= r < n <= N and all a_1..a_n, beta, gamma in pi, is called a
  nil-form of degree N+1 on pi with values in R. (Relation (2) is the multi-place cocycle identity
  defined in Section 1.2; I did not transcribe it from the image.)
* **l_1, l_2** (Section 1.2, p. 336-337, OCR-ONLY): defined by induction via formula (1) from the
  Magnus coefficients (y_0 / x_{r_1},...,x_{r_m}) of the loop d^{-1} f_0 d in pi_1(S^3 \ Gamma, b),
  where Gamma is the graph made of pushed-off copies of the loops. Explicitly the paper states:
  "l_1(a_0, a_1) = (y_0/x_1) and l_2(a_0, a_1, a_2) = (y_0/x_1,x_2) + (y_0/x_2) l_1(a_1, a_2)."
  l_1(A) is the ordinary Seifert form (formula (4): l_1(beta,alpha) - l_1(alpha,beta) = alpha . beta).
  l_2 is the degree-3 piece; its value on a triple is the corresponding Milnor-type invariant.
* **hyperbolic / metabolic** (p. 341, OCR-ONLY): "A nil-form l of degree N+1 on a group pi, with
  values in a commutative ring R, is called *hyperbolic* [*metabolic*] if there exist subgroups
  pi_1 and pi_2 of pi such that: pi = F_N(pi_1 * pi_2) (i.e., the natural homomorphism
  pi_1 * pi_2 -> pi induces an isomorphism F_N(pi_1 * pi_2) -> pi); the R-modules H_1(pi_1;R) and
  H_1(pi_2;R) are isomorphic; and l|_{pi_1} = 0 and l|_{pi_2} = 0 [respectively l|_{pi_1} = 0]."
* **special nil-form**: see the verbatim Section 1.5 above.
* **group of type (n,Q)** (p. 341, OCR-ONLY): "for any n >= 1 the group F_n^c(G) is isomorphic to
  the rationalization of a finitely generated free nilpotent group of nilpotency class n. Such
  groups will be called groups of type (n,Q)." Here F_n = free nilpotent quotient functor of class
  n, and c = Mal'cev rationalization; F_n^c = their composite (Section 1.3).
* **F_2(l_1,l_2)** : by Proposition 1.3.1, the unique nil-form on F_2(pi) inducing (l_1,l_2);
  F_2^c is its rationalized version.
* **inverse nil-form** (Section 1.7, p. 341, VERIFIED): (a_0,...,a_n) |-> l_n(a_n^{-1},...,a_1^{-1},a_0^{-1}).

### 1.8 Section 7.4 — does H(ii) use only pi_1-surjectivity? YES — VERIFIED (page image `p22_bot.png`)

> **7.4. Proof of (ii) and (iii).** Part (ii) of the theorem follows from Lemmas 7.2 and 7.3 and
> the fact that every ribbon knot K in S^3 bounds a disk D in the ball B^4 such that the inclusion
> homomorphism pi_1(S^3 \ K) -> pi_1(B^4 \ D) is surjective (see [3]). [...]

and Lemma 7.2 (p. 355, OCR-ONLY) begins:

> **7.2. LEMMA.** Let K be an oriented knot in S^3 bounding a (smooth) disk in the ball B^4; W an
> open tubular neighborhood of the disk; G and H the commutator subgroups of pi_1(S^3 \ W, v) and
> pi_1(B^4 \ W, v), respectively, with v in S^3 cap dW; and phi_n and psi_n the inclusion
> homomorphisms F_n^c(G) -> F_n^c(H) and Q_n(G) -> Q_n(H), respectively, for n >= 1. **If phi_1 is
> an epimorphism**, then dim H_1(H;Q) = 1/2 dim H_1(G;Q) and (for every n >= 1) phi_n^c is an
> epimorphism, F_n^c(H) is a group of type (n,Q), and [...]

**Conclusion (VERIFIED):** the only input about ribbonness is the existence of a smooth disk in B^4
whose complement's pi_1 is hit by pi_1(S^3\K). That is exactly the definition of a *homotopy-ribbon*
disk (Casson-Gordon [3] is cited for the fact that ribbon disks are homotopy-ribbon). Therefore
Theorem H(ii) is, verbatim in its own proof, an obstruction to **homotopy-ribbonness**, and the
knots of Theorem I with r != 0 and s != 0 are **provably not homotopy-ribbon**, hence not ribbon.

---

## 2. The Seifert matrix — RECOVERED

The paper gives the Seifert form directly as the matrix X. Taking V = X (V_ij = l_1(A)(x_i,x_j)):

```
          | 0   1    0   1   0   0 |
          | 0   0    p   0   0   0 |
V(p,q) =  | 0   p    0   q   0   1 |
          | 1   0   q-1  0   p   0 |
          | 0   0    0   p   0   0 |
          | 0   0    1   0  -1   0 |
```

r and s do NOT appear: they are the l_2 (Milnor-triple) data, invisible to V. All four parameters
matter for the knot, but only p,q for its Seifert matrix / S-equivalence class.

Checks (COMPUTED, sympy, script `verify.py`):

| claim | status |
|---|---|
| alt(V) = V^T - V is the standard symplectic form on pairs (1,2),(3,4),(5,6); det = 1 | VERIFIED COMPUTED. By Seifert's realization theorem (quoted in 1.5 above) V *is* a Seifert matrix. |
| Y^T X Y = X^T identically in p,q | VERIFIED COMPUTED (paper's claim confirmed) |
| det(V - tV^T) = t^3 * rho(t) * rho(1/t), rho(t) = p t^3 -(p+q)t^2 -(p-q+1)t + p | VERIFIED COMPUTED (paper's claim confirmed) |
| V vanishes identically on span(x1,x3,x5) and on span(x2,x4,x6) | VERIFIED COMPUTED |
| rho_1(x) = (-p x^3 + (p+1-q)x^2 + (p+q)x - p)/p and rho_2(x) = -x^3 rho_1(x^-1) (Section 9.1, p. 359) | VERIFIED (page image `p25_top.png`); note -p*rho_1(x) is the reversal of rho(x), consistent |

---

## 3. Classical slice obstructions over the parameter grid

Grid: p in {1,2,3,5,7}, q in {0,...,5} (excluding p=2,q=2, which Theorem I excludes; note q=0 is
outside Theorem I if "natural number" means q>=1 — flagged in the table file). r,s arbitrary
nonzero integers; they do not affect anything in this section. Script `compute.py`, data
`grid.json`.

**Every single member passes every classical necessary condition for sliceness, for a structural
reason, not by accident:**

1. **Metabolic Seifert form over Z (algebraic sliceness).** span(e1,e3,e5) is a rank-3 unimodular
   direct summand of Z^6 on which V vanishes identically — and so is span(e2,e4,e6). So the Seifert
   form is not merely metabolic but *hyperbolic over Z*, for every p,q. (Exactly what Turaev says:
   "The form l_1^1(A) is hyperbolic".) Hence K is algebraically slice and all Levine invariants vanish.
2. **Fox-Milnor.** Delta(t) = t^3 rho(t) rho(1/t) identically, so Delta(t) = f(t)f(1/t) with
   f = rho, for all p,q — VERIFIED COMPUTED (also checked factor-by-factor with a reciprocal-pairing
   test in `compute.py`).
3. **Levine-Tristram signatures.** sigma_omega = signature((1-omega)V + (1-omega-bar)V^T) = 0 for
   omega a primitive n-th root of unity, n in {2,3,4,5,7,8,9,11,13,16,25,27,32}, for every
   (p,q) in the grid — COMPUTED. (Forced: a metabolic Seifert form has vanishing signature
   function.)
4. **|Delta(-1)| a square.** det = |Delta(-1)| = rho(-1)^2 is a perfect square for every (p,q)
   — COMPUTED; values 1, 9, 25, 49, 81, ... appear.
5. **Arf = 0** for every (p,q) — COMPUTED (via |Delta(-1)| = +-1 mod 8).

Sample of the table (full data in `grid.json`; all rows identical in verdict):

| p | q | Delta(t) = det(V - tV^T) up to units | det=\|Delta(-1)\| | square? | Fox-Milnor | sigma_omega (all tested) | Arf | rho_1 irreducible /Q |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | t^6-3t^5-t^4+7t^3-t^2-3t+1 | 1 | yes | yes | 0 | 0 | yes |
| 1 | 3 | t^6-3t^5-7t^4+19t^3-7t^2-3t+1 | 25 | yes | yes | 0 | 0 | yes |
| 2 | 1 | 4t^6-10t^5-4t^4+21t^3-4t^2-10t+4 | 1 | yes | yes | 0 | 0 | yes |
| 2 | 3 | 4t^6-10t^5-10t^4+33t^3-10t^2-10t+4 | 25 | yes | yes | 0 | 0 | yes |
| 3 | 2 | 9t^6-21t^5-11t^4+47t^3-11t^2-21t+9 | 9 | yes | yes | 0 | 0 | yes |
| 5 | 4 | 25t^6-55t^5-37t^4+135t^3-37t^2-55t+25 | 49 | yes | yes | 0 | 0 | yes |
| 7 | 5 | 49t^6-105t^5-69t^4+251t^3-69t^2-105t+49 | 81 | yes | yes | 0 | 0 | yes |

Also COMPUTED: rho_1 (hence rho_2) is irreducible over Q for every grid point, i.e. the hypothesis
actually used in Turaev's Section 9.1 proof holds throughout the grid (including q=0 and q=1).

---

## 4. Verdict: live candidates

**Every** (p, q, r, s) with p = 1 or p prime, q a natural number, q != 2 if p = 2, and
**r != 0 and s != 0** is a live candidate:

* **Algebraically slice** — in fact hyperbolic Seifert form over Z (COMPUTED).
* **Fox-Milnor satisfied, all Levine-Tristram signatures zero at all prime-power roots of unity
  tested, determinant a perfect square, Arf = 0** (COMPUTED). No classical obstruction kills any of
  them.
* **Not homotopy-ribbon**, by Theorem I + Theorem H(ii) + the Section 7.4 proof (VERIFIED reading of
  the primary text): r != 0 and s != 0 => F_2^c(l_1,l_2) is not metabolic => K is not
  homotopy-ribbon, hence not ribbon.

So if any of these knots is smoothly slice, it is a counterexample to the slice-ribbon conjecture
(indeed to the stronger "slice => homotopy-ribbon" conjecture). Conversely, proving all of them
non-slice requires a non-classical obstruction (Casson-Gordon, twisted Alexander, Heegaard Floer /
Upsilon, or the Rasmussen s-invariant), none of which is computed here.

The smallest candidates to try first: (p,q,r,s) = (1,1,1,1), (1,1,1,-1), (1,3,1,1), (2,1,1,1),
(3,1,1,1). Note Theorem I also says r and s are knot invariants only up to sign and powers of p,
so distinct (r,s) with the same p,q may give the same knot; and r=0 or s=0 members are *not*
candidates (they are only non-invertible / non-hyperbolic, not non-metabolic).

**Caveat that must not be lost:** A(p,q,r,s) is only defined up to the realization freedom of
section 1.5. Turaev's theorems constrain the boundary knot through (l_1, l_2) only. Different
choices of realizing embedding with the same X, r, s may give different knots, all of them equally
good candidates.

---

## 5. Explicit knot diagram (task 5) — NOT PRODUCED

Not done, deliberately, rather than guessed. The obstacle is specific: a diagram realizing the
Seifert matrix X alone is not enough — it would realize the (r,s) = (0,0) member, which is exactly
the member for which Theorem I gives *no* obstruction. To get a live candidate one must additionally
apply Milnor's ribbon-linking operator (Figure 4) r times to bands (1,3,5) and s times to bands
(2,4,6); that move changes the knot but leaves X (and therefore every invariant computed in
section 3) unchanged, so a PD code produced this way could not be validated by the Alexander-
polynomial check suggested in the task. Building it correctly requires implementing the Figure-4
ribbon move on a disk-with-6-bands diagram and reading off the boundary; that is a real but separate
piece of work, and any shortcut here would amount to fabricating a knot. Recommended next step:
implement the band-diagram -> Gauss/PD pipeline, validate on (r,s)=(0,0) against
Delta(t) = t^3 rho(t) rho(1/t) and genus 3, then apply the Figure-4 move to install r,s.

---

## Files

* `turaev_eng.pdf` — the English translation (1.8 MB, 27 pp.), from mathnet.ru.
* `eng_text.txt` — full PyMuPDF text layer (OCR quality: usable, formulas garbled).
* `page07_low.png`, `p08_top.png`, `p05.png`, `p25_top.png`, `p22_bot.png` — page renderings I read.
* `seifert_matrix.json` — the matrix X, the matrix Y, the l_2 data, and the verified identities.
* `grid.json` — the full parameter table (Alexander polynomials, determinants, signatures, Arf,
  Fox-Milnor detail, metabolizer flags).
* `verify.py`, `compute.py` — the scripts.
