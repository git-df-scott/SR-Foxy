# Targeted annulus and Norman-trick literature audit

Date: 18 September 2026. Scope: `research/14_marked_annulus_audit.md`,
`results/astra_2026_09_18_dual_path_frontier/README.md`,
`results/astra_2026_09_17_collar_boundary_audit/README.md`, and §6 of
`research/34_searchlight_and_the_general_stabilization.md`.

## Park: exact hypotheses and conclusion

Primary source: JungHwan Park, *A Construction of Slice Knots via Annulus
Modifications*, manuscript dated 18 November 2015, [arXiv:1512.00401](https://arxiv.org/abs/1512.00401),
[author PDF](https://math.rice.edu/~jp35/1.pdf). The author PDF is the version
containing Definition 2.1, Definition 3.1, and Theorem 3.3.

In Definition 2.1, let \(K\subset S^3\) have a chosen smooth slice disk
\(D^2\subset B^4\), let \(\eta_1\cup\eta_2\subset S^3-K\) be oriented, and let
\(\phi_A:S^1\times[0,1]\hookrightarrow B^4\) be a proper annulus with boundary
\(\eta_1\cup\eta_2\). Put \(\ell=\operatorname{lk}(\eta_1,\eta_2)\). The pair is
\(\ell\)-nice precisely when:

1. \(A=\operatorname{Im}\phi_A\) is disjoint from \(D^2\);
2. the boundary link is isotopic to Park's model \(L_\ell\) (Figure 5); and
3. for the auxiliary curve \(c\) in Figure 5 and a meridian \(\mu_1\) of
   \(\eta_1\),
   \[
   \langle [c]^n[\mu_1]\rangle
   =\langle[\mu_1]\rangle
   \quad\text{in }\pi_1(B^4-N(A)).
   \]
   This is the technical condition used to prove simple connectivity after
   the modification; it is not a ribbon condition.

Definition 3.1 says that \((\{\eta_1,\eta_2\},\phi_A)\) is \(\ell\)-standard when it
is \(\ell\)-nice and the annulus bounded by \(\eta_1\) and \(-\eta_2\) is smoothly
isotopic through proper embeddings to Park's standard annulus \(A_\ell\)
(Figure 7).

Theorem 3.3: if \(K\) is smoothly slice in the standard \(B^4\) and the pair
is \(\ell\)-standard, then surgery with coefficients
\[
\frac{n\ell+1}{n}\text{ on }\eta_1,
\qquad
\frac{n\ell-1}{n}\text{ on }\eta_2.
\]
It produces a smoothly slice knot \(K_{(\phi_A,n)}\subset S^3\), for every integer
\(n\). The proof transfers the ambient modification to the standard model and
shows the modified 4-manifold is diffeomorphic to \(B^4\). It does not produce
or assert a ribbon disk.

## Does standardness force ribbonness?

No such general theorem was found in this targeted primary-source check. Park's
introduction explicitly says that, beyond the separately treated examples, it
was not known whether slice knots obtained by annulus twists are ribbon. Thus
ℓ-standardness controls the annulus and the ambient diffeomorphism type, but
does not control the radial Morse function on the transported slice disk.

A relevant sufficient result is Abe--Tange, *A construction of slice knots via
annulus twists*, [arXiv:1305.7492](https://arxiv.org/abs/1305.7492). Their Lemma 5.1
says that if a handle diagram of \(B^4\) can be reduced to the empty diagram by
handle slides and adding/canceling 1/2-handle pairs, then the belt sphere of any
2-handle is ribbon. Their Theorem 5.4 verifies this handle criterion for the
\(n\ge 0\) annulus twists of \(8_{20}\), and gives an explicit ribbon
presentation. That special handle calculation is not a theorem for arbitrary
ℓ-standard pairs. Any proposed “extra collar/product” hypothesis would need a
relative handle or movie certificate of this kind; a proper annulus isotopy by
itself is insufficiently strong in the cited literature.

## Mixed bands: status and boundary test

The \(uv/vu\) construction is an existing proposal in `research/14`, not a new
literature result and not a certified mechanism. It pairs \(c_1^+\) with
\(c_2^-\) and \(c_2^+\) with \(c_1^-\), with intended based words \(uv\) and
\(vu\). They are conjugate because

\[
u^{-1}(uv)u=vu.
\]

Conjugacy does not certify an embedded annulus, its framing, standardness, or the
boundary surgery. Matching product annuli are a control: they produce a doubled
knot \(J\#(-J)\), the square-knot-type outcome.

The boundary requirement should be stated at the 3-dimensional level. A valid
Kirby/Rolfsen sequence may use blow-ups and blow-downs, so it can prove the
outgoing boundary knot is \(K_0\#(-K_1)\) without identifying the new 4-dimensional
surgery trace with the \((2,0)\)-framed Hopf-link trace. Those are different claims.
In particular, if the mixed diagram is represented by \(\pm1\) surgeries on an
unlink, its trace has odd diagonal form \(\langle1\rangle\oplus\langle-1\rangle\),
whereas the \((2,0)\) Hopf trace has even hyperbolic form \(H\); demanding a
trace diffeomorphism would therefore impose an unjustified, potentially
impossible condition. The intended \(D_{0,1}\) can instead be verified by any
correct 3-dimensional surgery identity, together with separate certificates for
the annulus, disk disjointness, and standard ambient \(B^4\).

**Falsifiable geometric insight.** A candidate joint rerouting succeeds only if
one can exhibit (i) the \(uv,vu\) marked words and an embedded annulus disjoint
from the disk, and (ii) a 3-dimensional Kirby/Rolfsen identity whose outgoing
knot is \(K_0\#(-K_1)\). A changed Alexander polynomial, or an outgoing exterior
identified with \(K_0\), is an immediate boundary failure and explains the
square-knot-type collapse. A mismatch of 4-dimensional intersection forms is
not by itself a boundary failure; it only rejects the stronger trace-diffeomorphism
claim.

## Norman-trick correction

Primary reference: R. A. Norman, *Dehn's Lemma for Certain 4-Manifolds*,
Inventiones Mathematicae 7 (1969), 143--147,
[doi:10.1007/BF01389797](https://doi.org/10.1007/BF01389797). Modern primary
discussions are Michael Klug and Benjamin Ruppik, *Deep and shallow slice knots
in 4-manifolds*, [arXiv:2009.03053](https://arxiv.org/abs/2009.03053), §4, and
Dave Auckly, Hee Jung Kim, Paul Melvin, Daniel Ruberman, and Hannah Schwartz,
*Isotopy of surfaces in 4-manifolds after a single stabilization*,
[arXiv:1708.03208](https://arxiv.org/abs/1708.03208), proof of the main theorem.
The latter explicitly uses immersed Norman tubing to parallel copies of a dual
sphere and records the resulting class as \(E+n\Sigma\), where \(n=E\cdot F\).

The blanket sentence in `research/34` §6 ("no choice of tubes avoids" a change
of \([C]\)) is not justified by the stated data. The following is conditional on
having a framed embedded dual sphere \(G\) (or parallel copies of such a sphere)
with \(F\cdot G=+1\), so that the required Norman tubes can actually be made
embedded and framed. Let \(p_i\in C\cap F\) have local signs
\(\varepsilon_i\in\{\pm1\}\). A tube at \(p_i\) into an oriented parallel copy
\(s_iG\), with \(s_i=-\varepsilon_i\), cancels that local intersection. The
relative class then changes by

\[
[C']=[C]+\sum_i s_i[G]
     =[C]-\left(\sum_i\varepsilon_i\right)[G]
     =[C]-(C\cdot F)[G].
\]

The audit records \(C\cdot F=\operatorname{lk}(K_0,c'_2)=0\). Therefore, if
opposite-sign intersections are present and the oppositely oriented framed
parallel copies are available, their homology changes cancel. If there are no
intersections, there is nothing to tube. To recover the claimed obstruction one
must add a separate geometric argument: for example, that all allowable tubes
are forced to have one orientation, or that the required opposite-orientation
tubes cannot be made simultaneously embedded and framed in this configuration.
The homology calculation alone does not provide that argument, and it does not
construct a destabilizing annulus.

Evidence status: Park's theorem and the Abe--Tange special ribbon criterion are
source-verified. The mixed-band construction remains an existing proposal, not
a result. The Norman formula is a conditional signed-intersection deduction;
it identifies a gap in the blanket §6 claim, not a completed destabilization.
