# An exhaustive involutive local-equivalence audit for K1

12 September 2026. **Conditional result:** the stored K0 and K1 have the same
involutive knot-Floer local-equivalence class, namely that of the figure-eight.
Consequently invariants factoring through this class cannot distinguish their
smooth concordance classes. This is not a smooth concordance, a slice disk, or
a counterexample to Slice–Ribbon. Branched-cover and satellite information is
not covered by this conclusion.

The condition is the same input/lifting dependency stated in
[`09_full_ring_floer_audit.md`](09_full_ring_floer_audit.md): the calculator's
minimal quotient complex, absolute bigradings, and the lift to a homogeneous
minimal full complex must be correct. The new calculation does not guess a
geometric involution. It quantifies over every algebraic involution satisfying
the required axioms on the identified complex.

## 1. The mixed differential ambiguity is a change of basis

Work over S=F2[U,V], with generator grading (A,M), degrees U=(-1,-2), V=(1,0),
and differential degree (0,-1). The earlier audit found 18 possible mixed
entries and an eight-dimensional space of square-zero completions.

There are ten allowable degree-zero maps N with entries divisible by UV.
They all run from the δ=M−A=-2 part to the δ=0 part, so N²=0. The linear map
`N -> d0 N + N d0` has image of dimension eight, exactly the mixed-differential
cycle space. For every one of the 256 completions d0+m, the saved certificate
provides N such that

`(Id+N)^2=Id` and `(Id+N)(d0+m)(Id+N)=d0`.

Thus every completion is isomorphic to the zero-mixed full complex. This is
stronger than merely finding an unknot local summand in each completion.

Conjugation also transports a genuine iota. Formal derivative maps are natural
under a basis change **up to chain homotopy**, so the equation
`iota^2 ~ Id + Phi Psi` remains valid after transport. We use this homotopy
statement, not an incorrect strict conjugacy assertion for Phi or Psi.
The gradings are preserved throughout; all homotopies that could affect this
calculation run from δ=-2 to δ=0. None can alter the diagonal block equations.

## 2. A small explicit model

A verified constant change of basis identifies the full complex with

`C = E ⊕ B_- ⊕ B_+`.

E has generators a,e,z in grading (0,0), b in (1,1), and c in (-1,-1), with

`d(a)=U b+V c`, `d(b)=V z`, `d(c)=U z`, `d(e)=d(z)=0`.

Each B is a four-generator box with the same displayed differential, omitting
the free generator e. Their gradings are:

| Box | a,z | b | c |
|---|---|---|---|
| B_- | (-1,-3) | (0,-2) | (-2,-4) |
| B_+ | (1,-1) | (2,0) | (0,-2) |

E lies at δ=0 and both other boxes at δ=-2. This model and its complete map to
the original 13 generators are saved in the audit result.

## 3. All possible diagonal involutions

Iota swaps U,V and sends (A,M) to (-A,M-2A), so it preserves δ. A term from x
to U^u V^v y requires u+v=δ(y)-δ(x). Hence E cannot map to B_-⊕B_+, and the
diagonal blocks have constant coefficients. A degree-(0,+1) diagonal homotopy
would require u+v=-1 and is impossible. Therefore the square axiom holds
strictly on those blocks.

Exhaustive calculation gives precisely two choices on E:

`i(a)=a+e+βz`, `i(e)=e+z`, `i(z)=z`, `i(b)=c`, `i(c)=b`, with β∈F2.

They are conjugate by e↦e+z. These are the figure-eight involution in the
standard model. On B=B_-⊕B_+, there are precisely two choices:

`i(a_-)=a_+ + λz_+`, `i(a_+)=a_- +(1+λ)z_-`, with λ∈F2;

the z generators exchange, b_- exchanges with c_+, and c_- with b_+.

The generating calculation enumerates cycle spaces. The independent checker
instead brute-forces all **2,048** grading-allowed constant matrices on E and
all **16,384** on B, recovering exactly the same two choices on each.

## 4. Every off-diagonal term admits a local projection

Write the remaining block as a skew chain map Q:B→E. Its cycle space has
dimension ten. For each of the four diagonal choices, every Q in this space
satisfies the square axiom up to an allowed homotopy.

More importantly, for every such Q we solve

`Q + X i_B + i_E X = d_E Y + Y d_B`,

where X:B→E is an ordinary degree-zero chain map and Y is a skew homotopy of
degree (0,+1). X here ranges over the full allowed chain-map space; it is not
restricted to the UV-divisible maps N used in Step 1.

The equations are linear once the diagonal choice is fixed. Verified solutions
on all ten Q-basis vectors therefore supply solutions on every Q. A second
implementation independently checks **all 4,096 combinations**, including the
square and projection-homotopy identities. It represents polynomial maps as
binary operators modulo (U^5,V^5). Every exponent in the checked identities is
at most four, so this truncation loses no coefficient of a generator image.
It also independently checks the dimensions, completeness, grading constraints,
all 256 mixed basis changes, and the constant basis isomorphism.

Now take the inclusion E→C and P=(Id_E,X):C→E. Both are chain maps, P restricts
to the identity on E, and both intertwine iota up to the displayed homotopy.
After inverting U,V, the two B boxes are contractible; for example z is the
boundary of V^-1 b. Thus inclusion and P induce homology isomorphisms. They
satisfy exactly the definition of involutive local equivalence. No inverse
chain homotopy equivalence over S itself is claimed or needed.

## 5. Comparison with K0

The stored K0 is thin, τ=0, and has determinant 13. Its thin model has three
boxes: one central box and a reflected pair. In the notation of
Hendricks–Manolescu, r(t)=1-t-t^-1, so r0=1. Their Proposition 8.1 puts the
involution in the standard form; the central free generator plus box is E and
the exchanged pair can be discarded by local maps. This identifies K0 with the
same figure-eight local class. Section 8.2 of that paper explicitly gives the
two E maps above, so this comparison is source-backed rather than inferred from
the equality of a few numerical correction terms.

Opus independently reviewed the algebra and found no countermodel. Its request
to substantiate the K0 step was resolved by checking Proposition 8.1 and Section
8.2 in the primary paper. The review is supplementary; the proof dependencies
are the cited results, input/lifting audit, and explicit finite calculations.

## Evidence and reproduction

* `scripts/audit_involutive_structure.py` generates the certificates in
  `results/involutive_structure_audit.json`.
* `scripts/verify_involutive_structure.py` is a separate standard-library
  implementation. Its strict result is
  `results/involutive_structure_independent_check_v2.json`.
* All source-complex and certificate hashes are checked before verification.
* Primary: Ian Zemke, *Connected sums and involutive knot Floer homology*,
  Proceedings of the London Mathematical Society 119 (2019), 214–265,
  [arXiv:1705.01117v2](https://arxiv.org/abs/1705.01117), Definitions 2.2/2.4,
  Lemma 2.8 and Corollary 2.9: axioms, local equivalence, and basis naturality.
* Primary: Kristen Hendricks and Ciprian Manolescu, *Involutive Heegaard Floer
  homology*, Duke Mathematical Journal 166 (2017), 1211–1299,
  [author PDF](https://web.stanford.edu/~cm5/hfi.pdf), Section 8.2 and Proposition
  8.1: figure-eight model and thin-knot involution classification.

A later calculation resolves the double-cover linking-form/character
correspondence without obtaining an obstruction; see
[the Fox–Goeritz audit](13_fox_goeritz_hkl.md). Further obstructions must use
additional information.
Repeating invariants that factor through the class just identified cannot
settle the missing smooth concordance.
