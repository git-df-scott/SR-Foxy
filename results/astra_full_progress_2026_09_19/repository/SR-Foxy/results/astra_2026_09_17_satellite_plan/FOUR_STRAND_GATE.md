# The next degree-four calculation can be a low jet

**NO COUNTEREXAMPLE.** This is a symbolic reduction, not a satellite diagram.
It assumes the zero-framed conventions of LOW_WRAPPING_LEMMA.md.

Suppose a TWO-component ribbon pattern has integral annular bracket

    P = a z^4 + b z^2 + c.

Ribbonness of P(U) gives a delta^4+b delta^2+c=delta^2 C. Thus

    P(K)=a(B4(K)-delta^4)+b(B2(K)-delta^2)+delta^2 C.

Select the ribbon reference R0=6_1#6_1#6_1. The known KDG d and e2 residues
match those of R0. If B4(KDG) is divisible by delta^2, define

    f4(KDG) = [B4(KDG)/delta^2] at A=alpha, alpha^4=-1.

Because B4(R0) is divisible by delta^4, the difference between the candidate
satellite's Jones determinant and the reference's Jones determinant is

    common_writhe_unit * a(alpha) * f4(KDG)   modulo 32.

The b term cancels modulo 32 by the existing two-parallel calculation, and
the C term is identical. The required products of signed component
determinants agree by the winding-parity satellite formula. Hence the
congruence obstruction for this specified pattern is exactly the nonzero
residue of the expression above.

Do NOT divide a modular remainder without justification. First verify the
lower exact divisibility or provide the appropriate independent determinant
argument. An exact state-sum truncated modulo (A^4+1)^3 gives the lower
coefficients and f4 without needing the delta^4 leading quotient. A modular
state-sum in Z/32[A,A^{-1}]/((A^4+1)^3) can detect a NONZERO obstruction but
cannot certify exact vanishing of its lower coefficients. Store that
qualification explicitly. Compute more precisely only for a potential hit.

Consequences for resource allocation:

* If the actual pattern's a(alpha)=0 in Z[alpha]/32, this determinant test
  cannot distinguish the target, even though the diagram wraps four times.
* If f4(KDG)=0 modulo 32, every eligible two-component degree-four pattern
  passes the tested determinant congruence (assuming the lower divisibility
  needed to define it). Do not enumerate their diagrams after this scalar is
  known. This does not settle higher-component or degree-six patterns.
* A possible nonzero product must be checked in the cyclotomic coefficient
  ring; it is not enough to multiply rounded complex evaluations.
* A proof B4(KDG) is divisible by delta^4 makes f4 exactly zero and closes
  this particular two-component degree-four determinant route immediately.
  Conversely, even when a particular satellite test fails, four-parallel
  lower nullity would already be a direct ribbon obstruction.

Next concrete target: construct and audit one degree-four ribbon pattern,
calculate a(alpha), and implement the MINIMAL four-parallel jet only if it
has sensitivity. No full four-parallel polynomial is needed for this gate.
A Bing-pattern diagram is only a proposed input until its axis marking,
zero framing and unlink/ribbon control have actually been verified.
