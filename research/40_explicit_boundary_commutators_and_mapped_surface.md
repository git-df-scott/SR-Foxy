# Explicit boundary commutators for the correction

18 September 2026. Constructive continuation of research/37--38.

## Question, assumptions, and success criterion

Can the integral second-derived certificate be turned into explicit handle
loops in the boundary presentation, rather than merely an existence argument?
Here G is precisely the 18-generator Wirtinger presentation in the archived
collar certificate. Every generator maps to 1 under G -> Z. The connected
abelianization graph verifies that this is the full abelianization.

Success for this step means an explicit product of commutators of exponent-zero
words equal to the existing correction delta in G, with an independent finite
certificate. An embedded modifying annulus, a framed geometric clasper, and its
exact longitude response are subsequent requirements, not consequences of this
word identity.

## 1. A shorter word in the actual boundary presentation

The earlier 20-letter simplification was in the source presentation and did
not automatically give a shorter boundary connector. Applying the same
deterministic, length-nonincreasing rewrite rule directly to the boundary
presentation gives this 26-letter representative:

    [4,-2,-1,3,-4,1,4,4,2,-3,4,-2,-2,-4,-8,4,2,1,2,-4,-2,-4,2,1,-4,-4]

All 64 moves from the original 104-letter boundary correction are recorded.
No enumeration of group words, completion algorithm, or shortest-word claim is
involved. This is equality in the presented group, not an isotopy certificate
for a particular embedded auxiliary curve.

In zero-based boundary-relator indexing the new integral Fox certificate is

    c1=-t-1, c2=t^-1-1, c3=-t^2+t, c4=-t^2, c7=-2, c8=-t,

with all other coefficients zero. These are ten signed monomial terms. They
involve only relators whose letters belong to upper-half generators 1 through
9. The subsequent factorization uses these same relators; it introduces no
lower-half generators.

## 2. An explicit product of thirteen commutators

Put mu=x3. Each signed monomial epsilon*t^k in c_i specifies the relator word

    mu^k r_i^epsilon mu^-k.

Let P be the ordered product of these ten words in the saved certificate.
Then P=1 in G. The full Fox identity ensures that delta P^-1 has zero
abelianization in the kernel of the free-group exponent map. Concretely,
rewrite it in the Schreier generators

    y_(i,k) = mu^k x_i mu^(-k-1),  i != 3.

The resulting freely reduced word has 56 letters with balanced exponent
counts for every y. A finite cut-and-reorder procedure factors it into thirteen
commutators. For clarity, the elementary identity used is the following. If

    w = a U b V a^-1 X b^-1 Y,     Z = X V U,

then

    w = [a U Z^-1, Z b V U Z^-1] (X V U Y),

where [u,v]=u v u^-1 v^-1. Expanding the right side and freely canceling
proves the identity. It removes four letters from the residual balanced word;
rotations are recorded as conjugations of the emitted factors. Free
cancellations remove additional letters. We claim no optimal genus.

The output lists all thirteen pairs (u_j,v_j) as explicit boundary words and
verifies the stronger free-group identity

    product_j [u_j,v_j] = delta P^-1.

Each u_j and v_j has exponent sum zero, hence lies in G'. Since P=1 in G,
this is an explicit commutator factorization of delta in G''. A separate
standard-library checker verifies the boundary rewrites, original relator
provenance, full abelianization, every handle's exponent sum, and the final
identity by literal free reduction. It does not use Fox calculus, Laurent
arithmetic, SymPy, or the producer's Schreier factorization. Altered handle
and relator-sign certificates are both rejected.

## 3. What geometric object this specifies

A genus-13 oriented surface with one boundary component has boundary word a
product of thirteen commutators of its symplectic basis loops. Map those loops
to the displayed u_j,v_j. The certified relation extends this to a surface map
into the presentation complex and hence into the knot exterior. Its boundary
represents delta. Its handle loops lie in G', so they can in turn bound mapped
surfaces. Thus it extends to a map of a height-two grope. Only the bottom-stage
handle words are explicitly listed here; second-stage fillings are existential.

This interpretation agrees with Tim D. Cochran, Kent E. Orr, Peter Teichner,
*Knot concordance, Whitney towers and L2-signatures*, Annals of Mathematics
157 (2003), 433--519, Definition 7.9 and Lemma 7.10, printed pp. 497--498:
membership in the nth derived subgroup is equivalent to bounding a **map**
of a height-n grope. [Author-hosted published paper](https://math.berkeley.edu/~teichner/Papers/COT1.pdf).
Source checked 18 September 2026, with an independent literature pass.

There is no embedding, disjointness, or framing assertion in this application.
The mapped surface does not supply the intersection data required to perform
embedded surgery. In particular, thirteen null-homologous handle pairs are
not thirteen pairs of disjoint disk boundaries.

## 4. Why the exact linking response is still a separate calculation

Delphine Moussard, *Rational Blanchfield forms, S-equivalence, and null
LP-surgeries*, Bulletin de la Societe Mathematique de France 143 (2015),
403--431, DOI [10.24033/bsmf.2693](https://doi.org/10.24033/bsmf.2693), proves
that null Lagrangian-preserving surgery induces a canonical Alexander-module
isomorphism preserving the rational Blanchfield form. Its converse realizes
a specified form-preserving isomorphism up to a power of t by a sequence of
such surgeries. [Published article and abstract](https://www.numdam.org/articles/10.24033/bsmf.2693/).
Source checked 18 September 2026.

Our interpretation: these statements do not determine the exact Laurent
representatives of the marked auxiliary curves' linking response. The
Blanchfield form is quotient-valued, and the geometric markings and framings
must also be tracked. A generic null-clasper appeal would therefore lose the
information needed for the surgery determinant from research/37.

## Evidence ledger and next attack

| Result | Evidence | Scope |
|---|---|---|
| Boundary word 104 -> 26 | 64 original-relator/free moves replayed | Group equality, not isotopy |
| Thirteen commutators of G' words | Direct free identity modulo ten explicit relators | Mapped genus at most 13, not minimal |
| Height-two grope interpretation | Explicit bottom loops plus COT Lemma 7.10 | A map; upper surfaces not constructed |
| Linking response remains uncomputed | No framed geometric realization supplied | Blanchfield preservation alone does not compute it |

The tenth factor gives a particularly small first test:

    [x3^-1 x4, x1^-1 x3].

Both proposed handle loops are just a difference of two meridians. The next
useful geometric attempt is to realize this factor as a local move on the
marked auxiliary curve, tracking the full Laurent linking response and the
unlink condition together. Its position in the full ordered product must be
preserved; replacing delta by this factor alone would not give the original
repair. A realization lemma for one move would be more useful than further
free-word shortening. All artifacts are in
`results/night_2026_09_18_surface/`.
