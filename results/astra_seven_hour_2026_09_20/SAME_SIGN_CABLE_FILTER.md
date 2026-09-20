# A filter for every distinct same-sign trefoil cable pair

20 September 2026. Status: an explicit research deduction, checked below but
not independently peer reviewed. This extends our (-9,-3) audit; it is not a
published theorem attribution, a counterexample, or a claim about all cable
families.

Let Q be either trefoil, let C_{2,q}(Q) denote its cable and U_{2,q} the torus
knot. Define

    D_Q(q1,q2) = C_{2,q1}(Q) - C_{2,q2}(Q) + U_{2,q2} - U_{2,q1}.

Claim: if q1 and q2 are distinct odd integers of the same sign, then D_Q is
not slice and its smooth four-genus is exactly one. In particular, changing
(-9,-3) to another distinct negative pair with the trefoil as companion does
not evade this obstruction.

## Source inputs and distinction from our extension

Matthew Hedden, Paul Kirk and Charles Livingston, *Non-slice linear
combinations of algebraic knots*, JEMS 14 (2012), 1181–1208,
DOI 10.4171/JEMS/330, https://arxiv.org/html/0909.1247 (checked 2026-09-20).
Lemma 2.2 supplies the marked cyclic linking form; Proposition 3.1 supplies
the satellite formula. Section 4 supplies the slice-metabolizer condition.
Theorem 5.1 and Appendix A relate discriminant parity to the Casson–Gordon
class. Section 8 supplies the genus-one upper bound. We extend the Fox
calculation from Lemma 5.2 to arbitrary odd q below; the published lemma
itself is restricted to prime q. We do not invoke the coprimality-dependent
Theorem 6.5. The unequal-valuation argument below is our deduction.

## Reduction and a character for every metabolizer

Mirror/inverse changes Q to its opposite trefoil and changes both q signs.
Thus assume q1,q2 positive. Reordering the parameters changes only the
concordance inverse. Distinct positive integers have different valuations at
some prime. Because both are odd, choose an odd p and reorder so that

    r = v_p(q1) > s = v_p(q2) >= 0.

Write q1=p^r*m1 and q2=p^s*m2, with m1,m2 prime to p. In the p-primary
subgroup, using m1 and m2 times the marked cyclic generators, the linking
form is

    H_p = Z/p^r(A) + Z/p^s(B) + Z/p^s(E) + Z/p^r(D),
    lambda = diag(m1, -p^(r-s)*m2, p^(r-s)*m2, -m1)/p^r.

When s=0, omit B and E. Any metabolizer of the full linking form decomposes
into its primary subgroups; its p-part V is isotropic. Let Vbar be its image
in H_p/pH_p and W its annihilator under the ordinary character pairing.

Suppose W had no character with a nonzero and b zero. Then a=k*b on W for
some k in F_p. Duality puts (1,-k,0,0) in Vbar. An isotropic lift would obey

    m1*(A^2-D^2) + p^(r-s)*m2*(E^2-B^2) = 0 mod p^r.

Modulo p this says m1*(A^2-D^2)=0, impossible for A=1 and D=0. If s=0, the
same argument uses a identically zero on W and the residue vector (1,0).
Thus every metabolizer admits a character with nonzero first cable phase
and zero second cable phase. The passage from these p-primary generators
to the source's marked generators multiplies phases by units modulo p.
Scale the entire character to make the first source phase exactly one.
The second phase stays zero.

## A discriminant root that torus summands cannot cancel

Put z=exp(2*pi*i/p), eta=exp(2*pi*i/6), and omega=eta/z. The companion
contribution to the Casson–Gordon class for our character is

    alpha_Q(z*t) + alpha_Q(z^-1*t) - 2*alpha_Q(t).

Both trefoils have Alexander polynomial Delta(t)=t^2-t+1, with simple roots
eta and eta^-1. At t=omega the first shifted factor has a simple zero. The
second does not: eta*z^-2 could equal a root only if z^2=1 or z^2=eta^2.
Neither is possible for an odd prime p (including p=3). The unshifted term
occurs twice. Therefore the total discriminant valuation is odd. For p=3
the three valuations are (1,0,1); for p>=5 they are (1,0,0).

It remains essential to check all torus terms, not assume they cancel.
For odd positive q, use the presentation <alpha,beta | alpha^2 beta^q>.
For a character of phase d, its two-dimensional metabelian representation
can be put in the form

    rho(alpha) = t^((q-1)/2) [[0,1],[t,0]],
    rho(beta)  = t^-1 diag(z^d,z^-d).

If p divides q every d is allowed; otherwise only d=0 is allowed. The
relator holds in either case. The determinant of the Fox alpha column is
1-t^q; the beta-I determinant is, up to a monomial,
(t-z^d)(t-z^-d). This reproduces the local part of the cited Fox method
without assuming q prime. A change of the marked generator only permutes
the allowed phases. At omega, the beta-I matrix is invertible, so the H0
correction is a local unit as well.

The order of omega is six for p=3 and 6p for p>=5. It is therefore even.
Since q is odd, 1-omega^q cannot vanish. Nor can omega equal a p-th root;
the denominators and all (1-t) corrections are units. Every torus
Casson–Gordon discriminant consequently has valuation zero at omega,
whatever its sign and character. The companion's odd parity survives.

A norm f(t)*conjugate(f(t^-1)) has even valuation at each unit-circle root,
including omega. Hence this Casson–Gordon class is nonzero. We have
constructed such a class for every metabolizer, contradicting the slice
condition. Combined with the source's genus-one surface, this proves the
claimed genus value, subject to the stated independent-review limitation.

## Falsification checks and boundaries

`audit_parameter_extension.py` exhaustively checks eight small linking-form
cases: p=3 or 5, unequal exponents including s=0, all units for the
p=3,r=2,s=1 test, and an equal-exponent negative control. The negative
control correctly finds metabolizers without the required witness. It
would be a serious error to drop r>s: when q1=q2 the knot is ribbon by
cancellation. `PARAMETER_EXTENSION_CONTROLS.json` preserves the results.

Exact rational-angle arithmetic also checks the discriminant root at ten
odd primes and 976 torus local-unit cases, q odd from 1 through 99. These
finite checks support the preceding all-parameter argument; they do not
replace it. The previous q3/q9 audit separately checks the representation
matrices over a cyclotomic field.

This result does not address every nontrivial companion, distinct
companions, other cabling indices, arbitrary linear combinations, GST,
or all possible smooth concordance relations. Opposite-sign parameters
are not part of the statement. The next useful cable step is to find a
source-backed nonribbon family outside these assumptions and audit its
sliceness obstructions before proposing a disk search.
