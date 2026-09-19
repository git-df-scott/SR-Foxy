# The full boundary correction is one commutator

18 September 2026. Source snapshot: `19cddf9f527f8d3487943b98bba2c7f355629426`.

**Counterexample: NO. New result: the actual recorded correction has commutator length one in the commutator subgroup of the recorded boundary presentation.**

No historical novelty is claimed. This improves the explicit thirteen-commutator construction in research/40; it does not produce a slice disk, an embedded modifying annulus, or a knot identification.

## 1. Exact statement and short answer

Let G be the eighteen-generator boundary Wirtinger presentation in `results/astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json`, using one-based signed boundary generators x1,...,x18. Let delta be the original 104-letter `correction_boundary_word` in `results/night_2026_09_18/word_correction.json`. These are boundary generators, not the source-knot generator labels.

With the convention [A,B]=A B A^-1 B^-1, define

```
A = [4,-3,-3,1]
B = [4,-9,-1,3,-1,8,-5,-8,1,1]
```

Equivalently,

\[
 A=x_4x_3^{-2}x_1,
 \qquad
 B=x_4x_9^{-1}x_1^{-1}x_3x_1^{-1}x_8x_5^{-1}x_8^{-1}x_1^2.
\]

Then **delta=[A,B] in G**, and both A and B have meridional exponent zero. An explicit representation of the full eighteen-generator group into SL(2,F11) shows delta is not the identity. Consequently

\[
\operatorname{cl}_{G'}(\delta)=1.
\]

Here commutator length counts commutators whose two factors belong to G'. This is NOT the minimum genus of all possible cobordisms between the embedded auxiliary axes: those problems include boundary representatives and latitude/conjugacy choices absent from this statement.

The same identity holds for research/40's 26-letter correction. The new checker starts from the original 104-letter input as well, so it does not need to trust the old shortening procedure.

## 2. A finite proof, not a normal-form black box

A boundary relation tuple (i,o,b,s,c), with zero-based indices, gives the one-based word

```
[-s*(b+1), i+1, s*(b+1), -(o+1)].
```

This convention was checked against the actual repository's `check_symbolic.py`, lines 136–139. The proof uses only original relators 1,...,8. No relation from the lower half is needed. Identities proved using this subset remain valid in the full group; injectivity of this subgroup is not assumed.

Seven recorded Tietze eliminations leave generators x3,x5 and the single relator

```
[5,-3,-5,-3,5,3,5,-3,-5,3,5,3,-5,-3,5,3,5,-3,-5,-3,5,3,-5,-3,-5,3].
```

Every elimination solves for a generator occurring exactly once in an existing relator. The independent checker substitutes its proposed replacement back into that relator and requires literal free cancellation to the empty word.

Put mu=x3 and y_k=mu^k x5 mu^(-k-1). Exponent-zero words admit the usual exact Schreier rewriting. Retain y_-1,y_0,y_1,y_2 as four formal basis letters, numbered 1,2,3,4. Only four additional y levels are needed for the original correction and the two short factors: -2,3,4,5. Each is eliminated using a shifted relator in which that level occurs exactly once. The finite dependency graph terminates in the four retained letters.

The resulting words are

```
f = [2,-1,2,-3,1,-2]
g = [2,-1,2,4,-3,2,-3,-1,2,3,-2,3,-4,-2,3,-2,1,-2,-2].
```

The translated original delta, translated 26-letter delta, and free reduction of f g f^-1 g^-1 are the SAME 42-letter word. Independently translating the short boundary A and B gives f and g respectively.

Thus the proof uses a finite chain of valid presentation relations followed by a free-group identity. It does not require a theorem that our retained four letters form a free basis of the actual boundary kernel, a complete word-problem solver, hyperbolicity, or a faithful representation.

`CERTIFICATE.json` records all seven Tietze steps, four finite Schreier rules, words at each stage, and final expansion. The JavaScript verifier also checks that shifting a Schreier relator really is conjugation by the stated meridian power in the original two-generator free group.

## 3. Exact nontriviality and the lower bound

The first finite witness gives

\[
\rho(A)=\begin{pmatrix}1&3\\1&4\end{pmatrix},\quad
\rho(B)=\begin{pmatrix}9&9\\3&8\end{pmatrix},\quad
\rho(\delta)=\begin{pmatrix}1&10\\3&9\end{pmatrix}
\quad(\bmod 11).
\]

All generator images have determinant one, and all eighteen original boundary relators evaluate to the identity. The final matrix is not the identity. This is a valid nontriviality witness even without knowing whether the representation is faithful.

For construction of the witness, the producer propagates the saved source representation from x1=[[1,1],[0,1]], x2=[[1,0],[6,1]] modulo 11, then substitutes the saved boundary words. It checks all nine source relators and all eighteen boundary relators. The separate JavaScript verifier needs only the displayed eighteen generator matrices and directly checks the full boundary presentation using BigInt arithmetic.

Additional consistent witnesses at (p,z)=(17,1),(17,9),(23,5),(23,21) are saved. They are redundant checks, not five new mathematical results. Nontriviality plus the one-commutator identity proves the exact commutator-length statement.

The abelianized Wirtinger relations identify every generator; a graph-connectivity check confirms G_ab=Z. A and B each have exponent sum zero, hence belong to G'.

## 4. What was actually run

The exploratory calculation transformed the 26-letter correction to the 42-letter representative and checked 12,104 algebraic cut candidates. A single cut left an empty residual word, giving one commutator. This took about one second in the present runtime. These are word decompositions, not tested knots or bands.

The final producer additionally processes the original 104-letter correction. Its two-generator expansion has 514 letters and its Schreier word 252 letters before the same 42-letter reduction.

Independent verification was performed in JavaScript, with no Python imports or knot library. Eight corrupted certificates were rejected: six word/rewrite corruptions and two finite-matrix corruptions. Elementary free-cancellation and nontrivial-commutator controls were also checked. A Python run with optimization enabled produced a byte-identical certificate.

A separate direct shortlex rewrite attempt on delta[A,B]^-1 stalled at a nonempty word. It is saved as `direct_identity_attempt.json`, an INCONCLUSIVE heuristic failure. The finite Tietze/Schreier proof resolves the identity independently; stalling was not an exclusion.

The exact saved compatibility

```
q0(delta b) = q0(x5)^-1 q0(a) q0(x5)
```

uses the seam meridian x5, distinct from the convenient Schreier meridian x3 in Section 2. It was separately replayed by literal free reduction for the original source and boundary words, in both Python and JavaScript. This checks the old algebraic repair, not the identification of q0 with a geometric inclusion.

## 5. Consequence for the geometric campaign

Research/42 takes a factorization delta=product [u_j,v_j] with exponent-zero handle words and gives a moving-boundary genus-g surface construction. Under that note's geometric argument, the entire repair now needs one handle pair instead of thirteen:

```
b_prime = [A,B] b.
```

`ONE_HANDLE_RECIPE.json` supplies both target handle words and the reverse insertion order required by successive left-multiplication disk pushes. It contains fourteen meridional insertion instructions, not fourteen verified diagrammatic moves.

For the two-boundary correction surface, genus one means chi=-2. It is not a concordance annulus, which would have chi=0. We have NOT compressed the previous genus-13 recipe; we have found an alternative factorization that permits a different genus-one recipe. Its embedded endpoint may be a different curve.

In particular:

- A word identity is not an isotopy of auxiliary axes.
- The recipe's preservation of the auxiliary unlink and exact E uses the construction in research/42; it was not independently implemented as a marked PD in this session.
- Preserving delta, or E, does not identify the surgery boundary.
- The short words do not supply an immersed-annulus movie, clean framed Whitney disks, a standard-ambient modification, or nonribbonness of a new boundary.

The direct benefit is a much smaller concrete geometric experiment: realize the FULL correction via these two handles, rather than begin with the tenth factor of a thirteen-factor decomposition.

## 6. Literature checked and what it does not supply

Bartholdi–Ivanov–Fialkovski, *On commutator length in free groups*, Groups Geom. Dyn. 18 (2024), 191–202, Theorem A and Corollaries B–C, gives constructive algorithms for commutator length. Its commutator convention is u^-1 v^-1 u v, unlike ours. The exact expansion above fixes our convention independently. Our bounded cut search is not claimed to implement the paper's complete algorithm.

Cochran–Orr–Teichner, *Knot concordance, Whitney towers and L2-signatures*, Annals of Mathematics 157 (2003), 433–519, Definition 7.9 and Lemma 7.10, concerns maps of gropes and derived-series membership. It supports the distinction between a genus-one mapped correction and the needed embedded geometry; it does not turn our word certificate into a slice disk.

Schneiderman, *Algebraic linking numbers of knots in 3-manifolds*, AGT 3 (2003), 921–968, Proposition 4.1.2 and the paragraph following Proposition 2.1.3, separates pairing intersections by Whitney disks from having disjointly embedded, framed disks with clean interiors. That distinction remains essential for the paired-clasp programme.

Precise URLs, dates and checked locations are in `SOURCES.json`. The browser supplied parsed text. Four requested PDF screenshots failed with cache-miss errors, and the attempted arXiv HTML version of the commutator paper was unavailable. No figure inspection is claimed.

## 7. Scope, artifacts, and the next action

Work was done in an isolated Linux runtime, not the user's Mac checkout. Repository inputs were read through the GitHub connector. No branch, commit, remote mutation, or Mac file change was made.

The local input files contain transcribed selected integer fields with pinned source locations and blob IDs, not byte-for-byte downloaded source files. Exact arithmetic validates these explicit inputs. `verify_against_checkout.py` additionally compares those fields against the frozen commit in a local checkout; that optional comparison has NOT been run on the user's machine. The reading register states the exact scope inspected.

**Strongest new verified result:** delta=[A,B] with A length four, B length ten, and cl_(G')(delta)=1.

**Still unresolved:** geometric marked q0; an explicit realization with the intended surgery boundary; an embedded correctly framed modifying annulus and standard-B4 conclusion; nonribbonness for that same actual boundary.

**Single highest-value next action:** construct one marked genus-one realization of these two exact handle words, and calculate its framed surgery boundary before attempting Whitney-disk cleanup. This experiment uses the full repair, not merely one factor of the old expression.
