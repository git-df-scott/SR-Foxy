# Bounded review of the 18 September upstream notes

Date: 18 September 2026. Scope: results/opus_2026_09_18_2200_delta_r_nogo/README.md
and PLAN_CE_2026_09_18.md. This note records corrections only; it does not
promote a CE or a new conjecture.

## Logical corrections

**Miyazaki alternative 1 remains a possible route.** The Delta_r note
incorrectly treats minimality as incompatible with the desired counterexample.
If a nontrivial fibered knot \(B_r\) is independently shown to be slice and
minimal for the relevant homotopy-ribbon order, that minimality is precisely
what can obstruct a homotopy-ribbon disk: a homotopy-ribbon disk would place the
unknot below \(B_r\). The sentence “if \(B_r\) is slice via a
homotopy-ribbon disk, minimality fails” assumes the disk whose nonexistence is
being sought. It cannot be used to discard alternative 1. The algebraic
polynomial alone does not establish that \(B_r\) is prime or fibered, so those
hypotheses would still need separate verification.

The claim in PLAN_CE_2026_09_18.md that a Slice--Ribbon counterexample is
“exactly” a concordance class containing two distinct minimal fibered knots is
also too strong. The cited results give a targeted sufficient mechanism (and
the Hom--Park cable dichotomy), not a characterization of every possible CE.
A general CE need not be fibered or arise from two minimal representatives.
For the explicitly defined Hom--Park sum \(P\), “\(P\) is slice iff the
displayed four-term concordance relation holds” is a valid family-specific
identity; it must not be promoted to a global CE iff statement. See
[Hom--Park, arXiv:2507.20455](https://arxiv.org/abs/2507.20455), whose abstract
states the dichotomy, not the converse characterization.

Algebraic sliceness does not imply \(\tau=0\). Algebraic sliceness concerns a
metabolic Seifert form, whereas \(\tau\) is a smooth Floer concordance
invariant. The displayed values \(2,3,4,5\) and
\(2-3+5-4=0\) for the torus-knot cable example are a separate cabling-formula
calculation (with the needed epsilon/cabling hypotheses); they are not a
consequence of Corollary 1.3's algebraic-slice conclusion.

The DHST sentence is overgeneralized and the cited paper is misattributed.
arXiv:1806.06225 is by Christopher W. Davis, JungHwan Park, and Arunima Ray,
not Dai--Hom--Stoffregen--Truong. Its abstract produces selected infinite
families of linearly independent cables and says that *those results* cannot
be reached by combinations of algebraic, Casson--Gordon, \(\tau\),
\(\epsilon\), and \(\Upsilon\) invariants:
[Davis--Park--Ray, arXiv:1806.06225](https://arxiv.org/abs/1806.06225).
This does not prove that the Hom--Park four-term relation is invisible to
those invariants, or that zero entries in the repository's particular
obstruction matrix are forced. Each zero remains a calculation or an
unproved inference until checked on that exact family.

Finally, the plan's involutive-Floer lane is not uncomputed. The repository
already contains results/involutive_structure_independent_check_v2.json and
results/involutive_structure_audit.json: 256 mixed gauges, the stated
diagonal enumerations, and 4096 full-\(\iota\) projection cases were checked.
The recorded status is conditional on the supplied quotient complex, grading
data, and full-ring lifting argument, and explicitly says it is not a slice
certificate. The defensible conclusion is that the stored \(K_0,K_1\)
complexes have the same ordinary/involutive local-equivalence class under
those assumptions, so invariants factoring through that class do not separate
them. This does not prove \(D_{0,1}\) slice, concordance, or vanishing of
invariants outside that local-equivalence package. It should be listed as a
conditional completed audit rather than P5 “live and uncomputed.”

## Irreducibility of \(f_r\) for every integer \(r\)

Write
\[
d(t)=t^4-3t^3+5t^2-3t+1,\qquad
f_r(t)=d(t)+r(t^3-t)
=t^4+(r-3)t^3+5t^2-(r+3)t+1.
\]
For every \(r\in\mathbb Z\), \(f_r\) is monic and primitive. By Gauss's
lemma, a factorization over \(\mathbb Q[t]\) would give one over
\(\mathbb Z[t]\).

There is no linear factor: a monic polynomial with constant term \(1\) could
only have the integer roots \(1\) or \(-1\), but
\[
f_r(1)=1,\qquad f_r(-1)=13.
\]
For a quadratic factorization, after making both monic write
\[
f_r=(t^2+at+c)(t^2+bt+e),\qquad c,e\in\mathbb Z,\quad ce=1.
\]
Thus \(c=e=1\) or \(c=e=-1\). If \(c=e=1\), coefficient comparison gives
\[
a+b=r-3=-(r+3),\qquad ab+2=5.
\]
Hence \(r=0\), \(a+b=-3\), and \(ab=3\), which has no integer solutions.
If \(c=e=-1\), the \(t^3\) and \(t\) coefficients of the product are
\(a+b\) and \(-(a+b)\), whose sum is zero; the corresponding coefficients of
\(f_r\) have sum
\[
(r-3)-(r+3)=-6,
\]
an immediate contradiction. Therefore \(f_r\) is irreducible in
\(\mathbb Q[t]\) for every integer \(r\), strengthening the bounded
\(\lvert r\rvert\leq6\) computation in the upstream note. Its reciprocal
\(f_r^*(t)=t^4f_r(t^{-1})\) is irreducible by the same argument. For
\(r\ne0\), \(f_r\) and \(f_r^*\) are distinct monic polynomials, so the
factorization \(\Delta_r=f_rf_r^*\) has exactly these two nonassociate
irreducible factors over \(\mathbb Q[t]\).
