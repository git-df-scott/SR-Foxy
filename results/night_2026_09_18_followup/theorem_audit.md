# Theorem audit: geometry-free non-ribbon certificate

Audit date: 2026-09-18.  This note checks the claims in
`results/opus_2026_09_19_0000_geometry_free_certificate/` against the original
theorem statements and records the orientation-sensitive HFK test.  It audits
the non-ribbon half only; it does not identify the stored 19-crossing diagram
with the intended annulus-twist knot, and it says nothing about sliceness.

## Ni's fiberedness criterion

Yi Ni, *Knot Floer homology detects fibred knots*, arXiv:math/0607156 v4
(15 September 2007), published in *Inventiones Mathematicae* 170 (2007),
577--608, DOI [10.1007/s00222-007-0075-9](https://doi.org/10.1007/s00222-007-0075-9),
states Theorem 1.1 in the following form:

* \(K\) is null-homologous in a closed, oriented, connected 3-manifold \(Y\);
* \(Y-K\) is irreducible;
* \(F\) is a genus-\(g\) Seifert surface; and
* \(\widehat{HFK}(Y,K,[F],g)\cong\mathbb Z\).

Then \(K\) is fibered and \(F\) is a fiber.  The source is available at
<https://arxiv.org/abs/math/0607156> and the theorem is printed in the HTML
version at lines 55--67.  For knots in \(S^3\), the complement hypothesis is
automatic, but the coefficient and genus hypotheses still have to be stated.

Ni's *Corrigendum to “Knot Floer homology detects fibred knots”*,
arXiv:0808.0940 (7 August 2008), <https://arxiv.org/abs/0808.0940>, corrects
the JSJ/product-region citation and replaces the relevant technical statement
by a maximal-product-pair version.  It says explicitly that the proof of the
original Theorem 1.1 is only slightly modified; it does **not** change Theorem
1.1's statement or hypotheses.  The corrigendum should therefore be cited when
using Ni, but it does not invalidate the fiberedness implication.

The stronger primary rank formulation needed for the local certificate is
András Juhász, *Floer homology and surface decompositions*, arXiv:math/0609779,
published in *Geometry & Topology* 12 (2008), 299--350, DOI
[10.2140/gt.2008.12.299](https://doi.org/10.2140/gt.2008.12.299);
published PDF:
<https://msp.org/gt/2008/12-1/gt-v12-n1-p07-p.pdf>.  Theorem 9.11 (published
p. 349) says that for a null-homologous \(K\) in an oriented \(Y\), with
\(Y\setminus K\) irreducible and \(S\) a Seifert surface,
\[
\operatorname{rk}\widehat{HFK}(Y,K,[S],g(S))=1
\quad\Longrightarrow\quad
K\text{ is fibered with fiber }S.
\]
This is a free-rank statement in Juhász's integral sutured-Floer framework; it
does not require the entire top group to be isomorphic to \(\mathbb Z\).
The proof uses Theorem 1.4, which gives a \(\mathbb Z\) direct summand for a
taut balanced sutured manifold, and Theorem 1.5, which identifies
\(SFH(Y(S))\) with the top HFK group.

For the stored checker output, the displayed HFK ranks are
\(\mathbb F_2\)-dimensions.  Universal coefficients give free integral rank
\(\leq 1\) in the top Alexander grading when the displayed dimension is 1;
possible odd torsion is invisible and need not be excluded.  The monic
Alexander polynomial has leading Euler-characteristic coefficient
\(\pm1\), so the free rank is also \(\geq1\).  Thus Juhász's rank hypothesis is
met without claiming that integral \(\widehat{HFK}\) is torsion-free.

The genus used by the checker is also forced to be 2.  The computed Alexander
polynomial has breadth 4, so the genus inequality gives \(g(K)\geq2\).  If a
minimal Seifert surface had genus \(>2\), its sutured complement would be taut;
Juhász Theorems 1.4 and 1.5 would then give nonzero top HFK, hence nonzero
\(\mathbb F_2\)-HFK, above Alexander grading 2.  The exact computed tables have
no support above 2.  Therefore \(g(K)=2\), and Juhász 9.11 closes the
fiberedness step.  Ni's theorem remains a corroborating original criterion;
the corrigendum should still be cited, but an unknown odd-torsion summand is
no longer a gap in this certificate.

## Miyazaki's theorem and the orientation convention

The primary source is Katura Miyazaki, *Nonsimple, ribbon fibered knots*,
*Transactions of the American Mathematical Society* 341 (1994), 1--44,
DOI [10.1090/S0002-9947-1994-1176509-4](https://doi.org/10.1090/S0002-9947-1994-1176509-4).
The original AMS copy was not retrievable in this audit (the repository records
the access failure), so the exact theorem text below is checked against the
accessible secondary restatement, not silently attributed to a directly read AMS
PDF.

Abe--Tagami, *Fibered knots with the same 0-surgery and the slice-ribbon
conjecture*, arXiv:1502.01102 v5 (8 September 2016), published in *Mathematical
Research Letters* 23 (2016), 303--323, <https://arxiv.org/abs/1502.01102>,
Appendix A, Theorem 4.1, explicitly labels its statement as Miyazaki's Theorem
5.5.  For every summand \(K_i\), the hypotheses are universal: \(K_i\) must be
a **prime fibered knot in a homotopy 3-sphere** and must satisfy at least one of

1. minimality for the homotopy-ribbon order \(\geq\) among fibered knots in
   homology spheres; or
2. there is no \(f(t)\in\mathbb Z[t]\setminus\{\pm t^k\}\) with
   \(f(t)f(t^{-1})\mid\Delta_{K_i}(t)\).

If the connected sum is homotopically ribbon, its prime summands pair as
\(K_{i_s}=\overline{K_{j_s}}\).  In the \(S^3\) case Abe--Tagami state the
consequence directly (Corollary 4.3): if \(K_0,K_1\) are fibered knots in
\(S^3\) with irreducible Alexander polynomials and
\(K_0\#\overline{K_1}\) is ribbon, then \(K_0=K_1\).

Thus two **distinct** prime fibered knots with a common irreducible Alexander
polynomial \(d\) do give the desired non-ribbon conclusion, provided the knot
types are actually distinct and the \(S^3\) orientation convention is fixed.
In fact, “common” is stronger than needed for Corollary 4.3: irreducibility of
each polynomial is enough.  The polynomial is used to verify alternative (2),
and prime/fibered hypotheses remain per-summand hypotheses.  This is a
sufficient obstruction, not an iff characterization of ribbonness.

Here \(\overline K\) is Abe--Tagami's mirror-image convention: the appendix
defines it as the pair with both ambient and knot orientations reversed, and
the introduction calls \(K_0\#\overline{K_1}\) the connected sum with the
mirror image of \(K_1\).  Repository notation such as \(-K_1\) must therefore
be translated explicitly; reversing only the orientation of the knot is not
the same operation as mirroring the ambient \(S^3\).

## What the absolute bigraded HFK comparison proves

Ozsváth--Szabó, *Holomorphic disks and knot invariants*, arXiv:math/0209056
(revised 11 June 2003), *Advances in Mathematics* 186 (2004), 58--116,
<https://arxiv.org/html/math/0209056>, gives the classical-knot symmetries in
its introduction:

\[
\widehat{HFK}_{M,A}(K)\cong
\widehat{HFK}_{-M,-A}(\overline K),
\qquad
\widehat{HFK}_{M,A}(K)\cong
\widehat{HFK}_{M,A}(-K).
\]

The first is mirror duality (the source writes the equivalent indexing
direction); the second says total orientation reversal leaves the bigraded
groups unchanged.  Consequently:

* a direct mismatch of absolute \(A,M\)-rank tables rules out equality with
  \(K\) and with the reverse \(K^r\);
* to rule out a mirror, compare one table with the other after
  \((A,M)\mapsto(-A,-M)\);
* a match after that transformation cannot be used to distinguish a knot from
  its mirror using HFK alone.

For the stored certificate data, \(K_0\) has ranks
\[
(-2,-2):1,\ (-1,-1):3,\ (0,0):5,\ (1,1):3,\ (2,2):1,
\]
while \(K_1\) has the eight entries recorded in `RESULTS.json`, including
\((-2,-4):1\), \((-1,-3):2\), and \((2,0):1\).  Hence the direct tables differ.
Their \(\delta=M-A\) supports are respectively \(\{0\}\) and \(\{-2,0\}\).
After mirroring \(K_1\), the latter becomes \(\{0,2\}\), still different from
the \(K_0\) table.  Subject to the coefficient/grading caveat above, the HFK
data therefore distinguish \(K_0\) from \(K_1\), from \(K_1^r\), and from
\(\overline{K_1}\).  The reversal statement itself is not a distinction:
HFK is expected to agree for \(K_1\) and \(K_1^r\).

## Audit verdict

The Miyazaki/Abe--Tagami logical route is valid for distinct prime fibered
\(S^3\) knots with irreducible Alexander polynomials, and the HFK tables give
the needed direct knot-type distinction plus a separate mirror check.  The
theorem-level repair is to cite Juhász 9.11 (and its published Theorems 1.4--1.5)
for the rank-one fiberedness step, while recording the \(\mathbb F_2\)
coefficient convention and the genus argument above.  No integral
torsion-freeness claim is needed.  Ni's corrigendum remains relevant background.
The accessible source for Miyazaki is a restatement; the original 1994 paper
should be marked as not directly checked.


## Bounded audit of the integral word correction

The follow-up artifact `followup/integral_correction.json` and its independent
stdlib checker report an exact integer Laurent-coefficient identity expressing
the full Fox row of the correction word δ as a combination of **all** source and
boundary relator rows.  The checker also verifies the integer polynomial
arithmetic, every column, the exponent sum, and mutation failures.  This is a
stronger certificate than merely seeing zero coordinates in the rational
Alexander module.

The group-theoretic implication is conditional only on the stated presentation
conventions.  For a connected Wirtinger presentation with abelianization
φ:G→Z, the infinite cyclic cover has fundamental group
\(G'=\ker\phi\), and
\[
H_1(\widetilde X;\mathbb Z)\cong G'/[G',G']=G'/G''.
\]
The lifted loop for a word with exponent sum zero is closed in this cover.  Its
Fox 1-chain is the evaluated Fox row; an integral Laurent combination of relator
rows puts that chain in \(\operatorname{im}\partial_2\).  Therefore the artifact
supports \(\delta\in G''\) **for the presented group**, assuming the checker uses
the same left/right Fox convention and the relators really present the intended
G.  It does not produce an embedded disk, an unlink axis, a band, an annulus,
or a boundary-knot identity, and it should not be promoted to any of those
geometric claims.
