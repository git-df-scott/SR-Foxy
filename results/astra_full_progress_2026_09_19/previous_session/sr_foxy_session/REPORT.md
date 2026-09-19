# SR-Foxy: arbitrary Bing trees and an independent ribbon-pattern probe

**Status: no Slice–Ribbon counterexample established.**

Repository snapshot: `git-df-scott/SR-Foxy`, main at
`53f800feb98faf177b4cb89c5204bb0fcbb4fa3b` (19 September 2026 UTC).
This is new local work, not a claim that the entire repository was read,
that a seven-hour run was completed, or that anything was pushed to GitHub.

## 1. Completed work and precise scope

The pinned repository proves that all zero-framed parallel multiplicities,
ordinary Bing doubles, and comb-shaped Bing iterates pass the specified Jones
ribbon conditions. Its `results/astra_2026_09_19_extended/parallel_bing/REPORT.md`
explicitly does not assert the arbitrary-tree extension.

Here I derive that extension. The argument below covers every finite binary tree
of ordinary, untwisted, zero-framed Bing operations on one knot, not just the
8,861 shapes checked computationally. This is a derivation from established
colored-Jones identities, not a claim of historical priority or external review.

I also implemented a separate annular Temperley–Lieb calculation and tested
2,171 distinct certified braid presentations of unlink patterns. They have
2–4 components and at most 8 braid strands. Each produces a ribbon-preserving
satellite construction. Every tested presentation passes the Jones congruence
for all companions whose signed determinant is an odd square. The latter is a
bounded sample, not an all-pattern theorem or a census of isotopy classes.

Neither calculation constructs a new slice disk or proves a candidate nonribbon.

## 2. An all-binary-tree formula

Use the repository conventions

    q=x^2, z=x+x^-1, [N]=(x^N-x^-N)/(x-x^-1), J_U(V_m)=[m+1].

For an n-component link put D(L)=(J_L/z^n)|_(x=i), provided this quotient is
regular. The ordinary Jones polynomial is V_L=J_L/z. These are signed values.

Let T be a rooted full binary tree with n>=2 leaves. Replace each internal
vertex by an ordinary untwisted Bing operation, obtaining the link B_T(K).
Let b(T) count internal vertices whose TWO children are themselves internal.
A comb has b(T)=0; the balanced four-leaf tree has b(T)=1.

Write Habiro's cyclotomic expansion, with the conventions of
Beliakova–Blanchet–Lê, as

    J'_K(N)=sum_(k=0)^(N-1) C_k(q) product_(j=1)^k
                 (1-q^(N+j))(1-q^(-N+j)),
    C_k(q) in Z[q,q^-1], C_0=1, c_k=C_k(-1).

Then the formula derived here is

    D(B_T(K))
      = 1 - 32 (-8)^(n-2) (-3)^b(T) (c_1+4c_2).             (A)

Consequently, for EVERY knot K and EVERY such tree,

    D(B_T(K)) = 1 (mod 32),
    null V(B_T(K)) = n-1.

Every component of these Bing links is an unknot, so the required product of
component determinants is 1. These two Eisermann conditions therefore cannot
obstruct ribbonness of the companion using this entire construction family.
This does not say that the links themselves are ribbon or slice.

### Proof: the Bing operation in a polynomial basis

Set v=V_1, so V_2=v^2-1, and define

    z_j=x^(2j+1)+x^(-2j-1),
    N_i(v)=product_(j=0)^(i-1)(v-z_j),
    {i}!=product_(j=1)^i(x^j-x^-j),
    S_i(v)=product_(j=1)^i(v^2-2-x^(2j)-x^(-2j)).

Suzuki, Theorem 3.2 and Proposition 6.2, imply

    beta(P'_i,P'_j)=0                 if i != j,
    beta(P'_i,P'_i)=(-1)^i S_i,
    P'_i=N_i/{i}!.

Thus if X=sum a_i N_i and Y=sum b_i N_i, then

    beta(X,Y)=sum_i (-1)^i a_i b_i ({i}!)^2 S_i.             (B)

All coefficients in (B) are integral polynomials in z: z_j is a Chebyshev
polynomial in z, and

    ({i}!)^2 = (z^2-4)^i product_(j=1)^i U_(j-1)(z/2)^2.

Its z-adic order is 2 floor(i/2). Also

    S_1(v)=v^2-z^2,
    S_2(v)|_(z=0)=v^2(v^2-4).

Let X_T be the annular skein polynomial obtained by placing v at every leaf
and applying (B) at every internal vertex. We prove by induction that

    X_T = z^(n-2) (P_T(v)+O(z^2)),
    X_T(z,z)=z^n,                                      (C)

where P_T has only v^2 and possibly v^4 terms. Write q_T=[v^2]P_T.
The O(z^2) assertion is coefficientwise in Z[v][[z]].

For a two-leaf tree, direct substitution gives

    X_T=z^2-(z^2-4)(v^2-z^2),  P_T=4v^2,  q_T=4.

Every non-leaf X_T is even in v, and satisfies
X_T(v,-z)=(-1)^n X_T(v,z). This follows from (B), since the Newton nodes change
sign and the squared factorials and S_i are even in z. This establishes the
parity needed in (C). Evaluation at v=z is multiplicative under beta: S_i(z)=0
for i>=1 and a_0=X(z). Hence X_T(z,z)=z^n exactly.

Suppose a child has m>=2 leaves and leading coefficient q. The first Newton
coefficients satisfy

    a_0=z^m,
    a_1=-2q z^(m-1)+O(z^(m+1)),
    a_2= q z^(m-2)+O(z^m).

Indeed z_0=z and z_1=z^3-3z, so the divided difference of q v^2 contributes
q(z_0+z_1)=-2qz+O(z^3). For even i>=2, a_i=O(z^(m-2)); for odd i>=3,
a_i=O(z^(m-1)). The latter gain comes from the evenness in v and the fact that
all Newton nodes are O(z).

If one child is a leaf, its only Newton coefficients are a_0=z and a_1=1.
Equation (B) then gives

    P_T=-8q_child v^2,  q_T=-8q_child.                     (D)

If both children are internal, with coefficients q_L,q_R, only i=1 and i=2
can contribute to order z^(n-2). Every i>=3 contributes order at least z^n.
Their contributions are, respectively,

    16q_Lq_R v^2,
    16q_Lq_R v^2(v^2-4).

Therefore

    P_T=16q_Lq_R(v^4-3v^2),  q_T=-48q_Lq_R.               (E)

This proves (C), (D), and (E) inductively for all trees. Solving the scalar
recursion gives

    q_T=4(-8)^(n-2)(-3)^b(T).                             (F)

### Proof: apply the companion functional

For an even polynomial Y(v), the difference J_K(Y)-J_U(Y) is O(z^2).
This follows directly from the cyclotomic formula: its irreducible colors have
odd dimension N, and every nonconstant summand contains the j=1 factor of
order z^2. The first two particular evaluations are

    J_K(v^2)-z^2 = (-8c_1-32c_2)z^2+O(z^3),
    J_K(v^4)-z^4 = O(z^4).                               (G)

For completeness, v^2=V_2+V_0 and v^4=V_4+3V_2+2V_0.
At odd dimensions N=3 and N=5, the z^2 coefficients in J_K-J_U are,
respectively, -8c_1-32c_2 and 24c_1+96c_2. They cancel in the second expression
in (G). More precisely the coefficient of each C_k is divisible by z^4 there:
for k=1,2 the residual symmetric polynomials have no z^2 term; for k>=3 the
j=1 and j=3 factors already provide z^4. Thus unknown derivatives of C_k at
q=-1 are not being set to zero.

By (C), the remainder contributes O(z^(n+2)) to J_K(X_T)-J_U(X_T).
Only the v^2 coefficient in P_T contributes to its z^n term, by (G). Since
J_U(X_T)=z^n, we obtain

    D(B_T(K))=1+q_T(-8c_1-32c_2).

Substitute (F) to obtain (A). Integrality of c_1,c_2 gives D=1 mod32, hence
D is nonzero. The order of J is exactly n, and that of V=J/z is n-1. QED.

### Examples and a useful distinction

For n=4 the comb and balanced tree need not have the same D:

    comb:     D=1-2048(c_1+4c_2),
    balanced: D=1+6144(c_1+4c_2).

Their deviations from 1 differ by a factor -3. Both still pass the congruence.
Thus the all-tree result is not an assumption that every tree is a comb or has
the same Jones polynomial.

## 3. Computation supporting the proof

`bing_tree_probe.py` implements (B) with exact Gaussian-integer Taylor series at
x=i(1+h). Each coefficient of each C_k is calculated separately. It checks
that every coefficient below the required order vanishes before taking the
quotient, so derivatives of C_k cannot be inadvertently omitted.

The saved run enumerates all unordered full binary tree shapes with 2–15 leaves:
8,861 shapes. All pass. The finite computation supports but does not replace the
inductive proof above.

`check_bing_symbolic.py` is an independent implementation in exact polynomials
Z[z,v], using SymPy, without importing the Gaussian-series engine. Eight shapes,
including two different six-leaf shapes, pass complete symbolic checks of the
leading polynomial, companion coefficients, and exact unknot evaluation. It
also verifies the distinct balanced/comb formulas.

Neither implementation independently formalizes the quantum-topological
identification in Suzuki's theorem; that is an explicit literature dependency.

## 4. A separate search of certified ribbon patterns

`ribbon_pattern_probe.py` starts with the identity n-braid, n in {2,3,4}, whose
closure is U_n. It records conjugations and positive or negative Markov
stabilizations. Inverse cancellations are also recorded implicitly in the
replay. These moves certify that every final ordinary braid closure is U_n.
The braid axis is retained, so these are generally different annular patterns.

The search requested 3,000 samples with a fixed pseudorandom seed 190926 and
retained 2,171 distinct (component count, braid width, freely reduced word)
tuples. Counts by components are 765,707,699. Widths range from 3 to 8, and the
longest retained braid word has 58 letters. Distinct tuples need not represent
distinct satellite patterns up to isotopy. This is not an exhaustive search of
braids at these widths or lengths.

The annular calculation uses

    R_i = x^-1 I - x^-2 e_i,
    R_i^-1 = x I - x^2 e_i,
    e_i^2=(x+x^-1)e_i.

Each Temperley–Lieb diagram is closed in an annulus. Contractible circles
contribute z, and essential circles contribute v. Signed seam traversal, not
ordinary planar component counting, distinguishes these two types.

The resulting annular polynomial is evaluated using the companion's formal
cyclotomic coefficients. For every retained presentation the coefficients of
all powers below z^n vanish separately. Its D is therefore an integral linear
combination of c_k=C_k(-1), with no unresolved derivative terms.

Let o be the number of components with odd braid-axis winding. Each component
of P(U) is an unknot. The satellite Alexander formula gives product of signed
component determinants d(K)^o. Here d(K)=1+4c_1.

Every retained presentation satisfies:

* all coefficients of c_k for k>=2 are divisible by 32;
* the remaining expression agrees with (1+4c_1)^o modulo 32 for every even c_1.

A slice companion has signed determinant an odd square, so c_1 is even. Thus
this congruence test is automatic for every slice companion on these sampled
patterns, without needing its unknown colored-Jones coefficients. The same
calculation gives an odd D and hence exact nullity n-1 for these companions.

The 2,171 entries are **not 2,171 candidate counterexample knots**. They are
certified pattern presentations tested symbolically on a whole class of
companions. No one of these presentations supplies a nonribbon certificate.
No conclusion about all other ribbon patterns is warranted.

Controls check inverse crossings and braid relations, recover the trefoil's
signed determinant -3, reject a Hopf link masquerading as an unlink pattern,
and reject an incorrectly indexed Markov stabilization. The pattern engine
shares its Gaussian-series arithmetic and cyclotomic evaluator with the first
engine; its full search was not independently replayed by a second topology
implementation. The independent symbolic checks concern the Bing calculation.

## 5. Geometric and covering-space checks

The stored genus-one correction surface is not the missing modifying annulus.
Its report gives a rank-three folded subgroup for the images of A,B,b, and an
injective map of its free fundamental group under the specified q0. Thus a
change of handle basis does not produce a compression for that particular
surface and map. The combined genus-two mixed-handle construction is a different
object; the rank-three conclusion must not be applied to exclude it.

The mixed-handle note also identifies a protected-axis obstruction to the
simplest collar matching: the A handle and reversed native c2 have different
linking with a. Equality after deleting a is not a marked geometric isotopy.
No new mixed caps, transported connectors, or Whitney disks were constructed
here. The 675-crossing framed surgery knot was not reduced to a new ordinary PD.

I investigated Cahn–Kjuchukova's dihedral signature-defect obstruction as a
possible additional route on the already-slice knot 18nh00000601. Its hypothesis
matters: the obstruction concerns colorings extending over a homotopy-ribbon
disk, with a rational-homology-sphere condition in its simplest numerical form.
Oliveira-Smith's preprint supplies a handle-ribbon disk in standard B4 for this
knot; handle-ribbon implies homotopy-ribbon. Therefore this obstruction cannot
prove that knot is globally non-homotopy-ribbon while accepting that theorem.
A bad value for some nonextending coloring would not suffice. No Xi value was
computed or asserted in this session.

This does not prove the knot ribbon: a genuinely ribbon-only obstruction is
still logically relevant. It prevents wasting a new computation on an invariant
whose target property is already satisfied.

## 6. What is still missing for a counterexample

For the genus-one surgery construction: an actual standard-B4 sliceness
construction and an independent nonribbon argument on the same knot are still
missing. The polynomial d^2 and auxiliary unlink do not provide them.

For the Abe–Tagami/Teichner lane: a verified ribbon movie on the required
stabilized target would be constructive evidence; none was produced here.

For 18nh00000601: accepting the cited standardization theorem supplies
sliceness, but nonribbonness is not established here. The Jones patterns tested
above and a homotopy-ribbon obstruction do not supply it.

No statement here excludes a different annulus, a different ribbon pattern,
a different stabilizer, or a Slice–Ribbon counterexample.

## 7. Sources and repository dependencies

Primary literature checked in HTML:

1. S. Suzuki, *Bing doubling and the colored Jones polynomial*, arXiv:1305.0602,
   Theorem 3.2, Proposition 6.2, and the definition of P'_i. These supply (B).
2. A. Beliakova, C. Blanchet, T. T. Q. Lê, *Unified quantum invariants and their
   refinements for homology 3-spheres with 2-torsion*, arXiv:0704.3669, §1.4,
   equation (5). This supplies the integral cyclotomic convention.
3. M. Eisermann, *The Jones polynomial of ribbon links*, arXiv:0802.2287,
   Theorems 1–2 and Proposition 6.13. These supply the ribbon gates and the
   ribbon-pattern satellite implication, not the new all-tree formula.
4. P. Cahn and A. Kjuchukova, *Computing ribbon obstructions for colored knots*,
   arXiv:1812.09553v2, introduction, equation (1), and Theorem 1. Exact coloring
   extension and covering-space hypotheses were retained.
5. T. Oliveira-Smith, *A Dunfield–Gong 4-Sphere is Standard*, arXiv:2603.23717,
   Corollary 1.1.1, Theorem 1.2, and §3.1. This is a preprint dependency; its
   Kirby-calculus proof was not independently reconstructed here.

Exact repository dependencies read at the pinned commit include:

- `results/astra_2026_09_19_extended/parallel_bing/REPORT.md`;
- `results/astra_genus_one_2026_09_18/README.md` and `REPORT.md`;
- `results/astra_2026_09_18_mixed_handle_gate/MIXED_HANDLE.md`;
- `research/13_fox_goeritz_hkl.md`;
- `research/46_paired_clasps_and_the_primary_annulus_obstruction.md`;
- `research/48_marked_product_model_and_one_stabilizer_pivot.md`;
- `research/49_stabilizer_exclusion_and_mixed_handle_marking.md`;
- `data/knots/18nh00000601.json`;
- the current brief and several handoff files.

This is a substantive but incomplete repository review. Old handoff claims were
not treated as current when contradicted by later notes. No private credential
was used, no remote job was launched, and no repository branch or file was changed.
