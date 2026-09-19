# Bounded algebra review of the opposite-surgery response

Date: 18 September 2026. This is an algebra-only check of the archived
response; it does not identify any geometric band rerouting with the stated
matrix form.

Let
\[
R=\mathbb{Q}[t,t^{-1}],\qquad
\Delta=t^4-3t^3+5t^2-3t+1,\qquad
q=t(t^2-1),
\]
and assume \(\Delta\) is irreducible over \(\mathbb{Q}\). The archived longitude
response is
\[
B=\frac{q}{\Delta}J,\qquad
J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\]
The source response is \(\Delta_R=\Delta^2\). For opposite surgery with
\(D_n=\operatorname{diag}(n,-n)\), the displayed target expression is
\[
F_n=\Delta^2\det(I+D_nB).
\]
For \(P=I\), this is
\[
F_n=\Delta^2-n^2q^2.
\]
Since \(\gcd(\Delta,q)=1\) (indeed \(\Delta(0)=\Delta(1)=1\) and
\(\Delta(-1)=13\)), \(F_n\not\equiv0\pmod{\Delta}\) for every \(n\ne0\).

## Residue lemma

Suppose a modified response has the form
\[
B'=PBP^*+E,
\]
where \(E\in M_2(R)\), \(P\in M_2(R)\), and \(*\) is transpose together with
\(t\mapsto t^{-1}\). Because \(\Delta\) is reciprocal up to the unit \(t^4\),
the involution preserves the prime ideal \((\Delta)\). Thus \(P\) invertible
modulo \(\Delta\) implies \(P^*\) invertible modulo \(\Delta\).

Set
\[
A=\Delta B'=qPJP^*+\Delta E\in M_2(R).
\]
Then
\[
\Delta(I+D_nB')=\Delta I+D_nA.
\]
Reducing modulo \(\Delta\) gives
\[
\Delta(I+D_nB')\equiv D_nqPJP^*\pmod{\Delta}.
\]
Taking determinants,
\[
\det\!\bigl(\Delta(I+D_nB')\bigr)
\equiv
\det(D_n)\,q^2\,\det(P)\det(J)\det(P^*)
\equiv
-n^2q^2\det(P)\det(P^*)
\pmod{\Delta},
\]
since \(\det(J)=1\). If \(n\ne0\) and \(P\) is invertible modulo \(\Delta\), every
factor on the right is nonzero in the field \(R/(\Delta)\). Therefore
\[
\det\!\bigl(\Delta(I+D_nB')\bigr)\not\equiv0\pmod{\Delta}.
\]
As \(\det(\Delta M)=\Delta^2\det(M)\) for a \(2\times2\) matrix \(M\), this is
exactly
\[
\Delta^2\det(I+D_nB')\not\equiv0\pmod{\Delta}
\qquad(n\ne0).
\]
Equivalently, the determinant has an exact double pole at \(\Delta\), and the
double-pole residue is nonzero.

## Necessary degeneration for a target \(\Delta^2\)

If \(F_n=\Delta^2\) for some nonzero \(n\), then \(F_n\equiv0\pmod{\Delta}\).
The displayed residue formula forces
\[
\det(P)\det(P^*)\equiv0\pmod{\Delta}.
\]
Because the involution preserves \((\Delta)\), this is equivalent to
\[
\Delta\mid\det(P).
\]
Thus \(\det(P)=0\) modulo \(\Delta\) is necessary for a modified response of the
form \(PBP^*+E\) to produce the target \(\Delta^2\). It is not sufficient:
higher-order terms and the matrix \(E\) still need to be checked.

In particular, if \(P\) is unimodular over \(R\), then \(\det(P)\) is a unit
\(c t^k\), with nonzero rational \(c\), so it is invertible modulo \(\Delta\), and the target is excluded
for every \(n\ne0\). The same conclusion holds under the weaker assumption that
\(P\) is merely invertible modulo \(\Delta\).

## Scope of the conclusion

This proves the residue obstruction for the stated algebraic ansatz. It does
not prove that every geometric mixed-band rerouting has response
\(B'=PBP^*+E\), nor that its \(P\) is invertible modulo \(\Delta\). Establishing
that representation requires a geometric derivation of the induced longitude
map, including bases, orientations, and the collar/product identification.
Without that step, the lemma is a conditional obstruction, not a universal
no-go theorem for mixed bands.
