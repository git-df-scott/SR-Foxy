# Bounded isotropic-module algebra review

Date: 18 September 2026. This is an algebra check of
results/night_2026_09_18/collar_module.json; it does not identify a new
geometric collar or a new boundary knot.

Let
\[
d=t^4-3t^3+5t^2-3t+1,\qquad q=t(t^2-1),
\]
and work in \(F=\mathbb Q[t^{\pm1}]/(d)\). With
\[
B_{0000}=\begin{pmatrix}0&q/d\\-q/d&0\end{pmatrix},\qquad
M=\begin{pmatrix}1&-t^{-1}\\ t^{-1}&-1\end{pmatrix},\qquad
H=\operatorname{diag}(t^2/d,-t^2/d),
\]
the exact rational-function identity
\[
MHM^*=B_{0000}
\]
holds, where \({}^*\) is transpose followed by \(t\mapsto t^{-1}\). Indeed,
\(d(t^{-1})=t^{-4}d(t)\), so \(H^*=H\), and
\[
MHM^*=\frac{t^2}{d}
\begin{pmatrix}0&t-t^{-1}\\-(t-t^{-1})&0\end{pmatrix}
=\begin{pmatrix}0&q/d\\-q/d&0\end{pmatrix}.
\]

The determinant of \(M\) is \(t^{-2}-1\). It is invertible modulo \(d\)
because \(d(1)=1\) and \(d(-1)=13\), but it is not a Laurent unit globally.
Thus \(M\) is a valid change of basis in the \(F\)-module, while the displayed
identity is not a unimodular Laurent-basis congruence. The justified
Blanchfield conclusion is therefore modulo Laurent polynomials: \(H\) is a
representative of the native pairing after the module-coordinate change.

The \(0110\) axes have source coordinates
\[
(1,-1),\qquad t^{-1}(1,-1).
\]
They lie on the same isotropic \(F\)-line; they are not an \(F\)-basis of the
two-dimensional module. The saved kernel line
\(\langle(t^n,1)\rangle\) is also isotropic for \(H\), since
\[
(t^n,1)H(t^n,1)^*=0.
\]
Its determinant with \((1,-1)\) is \(-(t^n+1)\), so the two lines are
transverse whenever \(t^n+1\ne0\) in \(F\). This holds for every integer
\(n\). To see it without a search, write \(x=t+t^{-1}\); then
\[
d/t^2=x^2-3x+3,
\]
whose roots are \((3\pm i\sqrt3)/2\), not real numbers in \([-2,2]\).
Consequently \(d\) has no unit-circle roots, hence no root of unity; an
identity \(t^n=-1\) modulo \(d\) is impossible (negative \(n\) reduces to
positive \(-n\)).

For the winding-coordinate pair
\[
v_1=(1,-t^{k-1}),\qquad v_2=(t^{-1},-t^\ell),
\]
both self-pairings under \(H\) vanish exactly, and the cross-pairing is
\[
v_1Hv_2^*=\frac{t^2}{d}\bigl(t-t^{\,k-\ell-1}\bigr).
\]
Its class in \(\mathbb Q(t)/\mathbb Q[t^{\pm1}]\) vanishes if and only if
\(k-\ell=2\). The forward implication is immediate. Conversely, if the
class vanishes, a root \(\alpha\) of \(d\) would satisfy
\(\alpha^{k-\ell-1}=\alpha\); since \(\alpha\ne0\) and is not a root of
unity, the exponent must be \(1\).

For any actual longitude/pairing representative \(E=(E_{ij})\) of such a
pair whose Blanchfield matrix vanishes modulo Laurent polynomials, one has
\(E_{ij}\in\mathbb Q[t^{\pm1}]\), subject to the geometric framing and
adjoint conventions. Opposite surgery weights \(D_r=\operatorname{diag}(r,-r)\)
then give
\[
\det(I+D_rE)
=1+r(E_{11}-E_{22})-r^2\det E.
\]
This equals \(1\) for every integer \(r\) exactly when
\[
E_{11}=E_{22}\quad\text{and}\quad\det E=0.
\]
In particular, \(E=0\) satisfies the criterion; the \(0110\) zero-response
calculation therefore reproduces the target \(d^2\) polynomial rather than
obstructing it.

The module computation alone does not prove that these coordinate lines are
embedded geometric axes, that the saved words realize a common collar, or that
the chosen longitude representatives are the surgery responses. It also does
not permit replacing \(M\) by a globally unimodular Laurent matrix. Those are
the remaining geometric and representative-level hypotheses.

## Word-level correction audit

The saved word_correction.json passes a stronger free-word identity for the
existing \(0110\) words. The source images use only generators \(5,6,8\), whose
literal upper-boundary lifts are \(3,4,8\). With
\(\mu=\) boundary generator \(5\), \(a,b\) the existing axis words, and
\[
\delta_{\rm src}
=\operatorname{red}\!\left(\mu^{-1}q_0(a)\mu q_0(b)^{-1}\right),
\]
the lift \(\delta\) satisfies:

* its boundary push-forward is exactly \(\delta_{\rm src}\);
* its two-coordinate Alexander-module class is \((0,0)\);
* its source \(F=\mathbb Q[t]/(d)\) class is zero; and
* for \(b'=\delta b\), free reduction gives
  \[
  q_0(b')=\mu^{-1}q_0(a)\mu
  \]
  exactly, not merely after applying the trace or Alexander-module map.

Thus the correction is compatible with the intended conjugacy relation and
does not change the checked \(F\)-coordinates of the second axis. This remains
a word/group calculation. Zero class in the rational Alexander module, even
together with exponent sum zero, does **not** by itself prove
\(\delta\in G''=[G',G']\) in the integral complement group; that would require
an additional integral derived-series argument. Nothing here certifies
embedded unlink axes, a Laurent longitude response, a disk or annulus, or the
boundary-knot identity.
