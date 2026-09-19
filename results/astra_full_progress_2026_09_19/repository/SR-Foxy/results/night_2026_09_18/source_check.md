# Conway--Piccirillo--Powell source check

Date: 18 September 2026.  Primary source: Anthony Conway, Lisa
Piccirillo, and Mark Powell, “4-manifolds with boundary and fundamental
group \(\mathbb Z\),” *Commentarii Mathematici Helvetici* 100 (2025),
323--420, DOI [10.4171/CMH/587](https://doi.org/10.4171/CMH/587).
The checked versions are the [EMS PDF](https://ems.press/content/serial-article-files/50353)
and [Powell's author PDF](https://www.maths.gla.ac.uk/~mpowell/CHM-realisation-4-manifolds-pi1-Z.pdf).

## The notation in Proposition 3.8 and Theorem 5.8

Proposition 3.8 (printed p. 345, §3.2) assumes a 3-manifold \(Y\), an
epimorphism \(\phi:\pi_1(Y)\twoheadrightarrow\mathbb Z\), and torsion
Alexander module \(H_1(Y;\mathbb Z[t^{\pm1}])\).  For disjoint simple
closed curves \(\widetilde a,\widetilde b\subset Y^\infty\), it gives
sesquilinearity, Hermitian symmetry (with the paper's adjoint convention),
and
\[
 [\operatorname{lk}_{\mathbb Q(t)}(\widetilde a,\widetilde b)]
 =\operatorname{Bl}_Y([\widetilde b],[\widetilde a])
 \quad\text{in }\mathbb Q(t)/\mathbb Z[t^{\pm1}].
\]
Thus the proposition identifies equivariant linking only modulo Laurent
polynomials.  It does not identify a preferred rational-function lift.
The authors explicitly warn that adjoint/module conventions can switch
variables.

The printed line of Theorem 5.8 (p. 363, §5.2) literally reads
\[
 \text{“If }H_1(Y_L;\mathbb Q(t))=0\text{ and }\det(A_{\widetilde L})\ne0,
 \text{ then }\Delta_{Y'}=\det(A_{\widetilde L})\Delta_Y.”
\]
This is present in both the EMS and author PDFs; it is not an OCR artefact.
It is internally inconsistent with the same section.  Construction 5.5
(p. 360) says, under \(H_*(Y;\mathbb Q(t))=0\), that
\[
 H_1(Y_L;\mathbb Q(t))\cong\mathbb Q(t)^n
\]
with basis the meridians of \(L\).  Lemma 5.6 (p. 361) assumes
\(H_1(Y;\mathbb Q(t))=0\), and the proof immediately before Theorem 5.8
(p. 363) says “since by assumption \(H_1(Y;\mathbb Q(t))=0\).”  Therefore
the mathematically used hypothesis is \(H_1(Y;\mathbb Q(t))=0\), together
with \(\det(A_{\widetilde L})\ne0\); the occurrence of \(Y_L\) in the
printed theorem should be flagged as a source typo unless the authors issue
a correction.  The theorem cannot literally require
\(H_1(Y_L;\mathbb Q(t))=0\) for a nonempty surgery link in this setup.

## What Proposition 3.8 does and does not imply for \(B'\)

Let \(R_{\mathbb Q}=\mathbb Q[t^{\pm1}]\), \(F=R_{\mathbb Q}/(\Delta)\), and
suppose the archived axes \(e_1,e_2\) really are an \(F\)-basis of the
relevant rational Alexander module.  If the new lifted axes are disjoint,
lie in the same infinite cyclic cover in covering general position, and
their classes satisfy
\[
 [e'_i]=\sum_j p_{ij}[e_j],\qquad p_{ij}\in R_{\mathbb Q},
\]
then Proposition 3.8 gives, entrywise modulo \(R_{\mathbb Q}\),
\[
 [B']=[PBP^*]\quad\text{in }M_2\bigl(\mathbb Q(t)/R_{\mathbb Q}\bigr).
\]
After choosing representatives, this is exactly
\[
 B'=PBP^*+E,\qquad E\in M_2(R_{\mathbb Q}).
\]
Here \(P\) is any Laurent-polynomial lift of the \(F\)-coordinate matrix,
and \(P^*\) is the transpose with \(t\mapsto t^{-1}\) under the paper's
sesquilinear convention.  If the new axes also form a basis, \(P\) is
invertible modulo \(\Delta\), but it need not be unimodular over
\(R_{\mathbb Q}\).

This is a conditional algebraic consequence, not a geometric rerouting
theorem.  One must still verify that the proposed axes are disjoint
embedded lifts, null for the covering homomorphism, and that their classes
really have the displayed \(F\)-coordinates.  If “basis of
\((\Delta)^2\)” is only a computed presentation and not a verified
geometric basis, Proposition 3.8 does not supply that missing step.
Framing changes and alternate rational representatives are precisely the
Laurent-polynomial ambiguity recorded by \(E\).

Finally, Theorem 5.8 is a determinant/Alexander-ratio result for the
paper's covering-space surgery setup and its invertibility hypothesis.
The annulus slopes \((n\ell+1)/n\) and \((n\ell-1)/n\) are rational
3-dimensional Dehn coefficients.  Applying the theorem to them requires
an explicit identification with the allowed covering surgery (or an
integer-framed continued-fraction replacement, with all added components
and units tracked).  The denominator \(n\) cannot simply be substituted
into an integer-surgery determinant argument without that bridge.
