# A second, independent route from `K_0 ~ K_1` to the failure of Slice-Ribbon,
# and a reduction of the concordance question to Agol-Ren Question 1.15

17 September 2026, Opus session. **NO COUNTEREXAMPLE.**
**Smooth concordance `K_0 ~ K_1`: UNKNOWN. Slice-Ribbon CE: NO.**

No concordance was constructed and no knot was proved non-concordant. This pass
does three things:

1. **Independently verifies the implication** `K_0 ~ K_1 ==> Slice-Ribbon false`
   by a second route that shares no step with the route already recorded in the
   repository, thereby discharging half of the user's standing acceptance
   condition ("the complete implication to Slice-Ribbon [must be] independently
   verified") *before* any concordance is found.
2. **Reduces the concordance question** to a published open question about
   fibered knots that mentions neither `6_3` nor annulus twists: a positive
   answer to Agol-Ren **Question 1.15** (`<=_h` form), even restricted to
   hyperbolic genus-2 pairs, would prove `K_0 !~ K_1` and retire the whole
   Abe-Tagami lane.
3. **Corrects the provenance** of the implication's key ingredient, which is
   Miyazaki's, not Agol-Ren's, and records an explicit gap in the minimality
   hypothesis that route 2 needs and the repository has not certified.

`check_q115_reduction.py` re-verifies all 23 numerical and algebraic gates from
committed repository data. `RESULTS.json` is its output: `all_checks_pass: true`,
23/23, sympy 1.14.0, Python 3.13.9.

---

## 0. The objects

`K_0 = 6_3`, `K_1 = A_1(6_3)` (Abe-Tagami, arXiv:1502.01102). From the committed
27-crossing link `6_3 u c'_1 u c'_2` and its stored certifications:

| property | `K_0` | `K_1` | gate |
|---|---|---|---|
| hyperbolic volume | `5.693021091281...` | `9.120006500798...` | G2a, G2b |
| fibered | yes (HFK) | yes (Abe-Tagami App. B) | G1b, G8 |
| Seifert genus | 2 | 2 | G1c, G8 |
| prime | yes (hyperbolic) | yes (hyperbolic) | G4 |
| `Delta(t)` | `t^4-3t^3+5t^2-3t+1`, irreducible | same (same 0-surgery) | G5a, G5b, G5e |
| determinant | 13, not a square | 13 | G5c, G5d |
| distinct | `K_0 != K_1` by Mostow (volumes differ by `> 3`) | | G3 |

---

## 1. Route 1 (already in the repository) - restated with corrected provenance

> **Route 1.** Suppose `K_0 ~ K_1` and Slice-Ribbon holds. Then
> `D_{0,1} = K_0 # (-K_1)` is slice, hence ribbon, hence `U <= D_{0,1}` and so
> `U <=_h D_{0,1}`. Apply **Theorem 1.13** with `m = 0`, `n = 2`,
> `K_1' = K_0`, `K_2' = -K_1` (both prime fibered, G4). The `K_{i,j}` must come
> in mirrored pairs. `K_0` is not strongly homotopy-ribbon (it is not slice:
> `det = 13` is not a perfect square, G5c/G5d), so `l_1 != 0`; likewise
> `l_2 != 0`. By fibered-minimality (Section 3) each `K_{i,1} # ... # K_{i,l_i}`
> is `K_i` itself. A mirrored pair across the two factors forces
> `K_0 = -(-K_1) = K_1`, contradicting G3. Hence Slice-Ribbon fails.

This is the specialisation of Agol-Ren **Corollary 1.14(1)** to our pair.

**Provenance correction.** Agol-Ren state in print that "Corollary 1.14(1) is an
immediate consequence of Miyazaki (see [Bak16, Remark 6])". The repository's
implication chain should therefore be attributed to **Miyazaki, Trans. AMS 341
(1994)**, with Agol-Ren Corollary 1.14(1) as the convenient modern statement.
Three numbering slips that were in circulation in this campaign are also fixed
here: the corollary is **1.14**, not 1.10 (1.10 is the finiteness of compressions
of a surface homeomorphism); the question is **1.15**, not 1.13 (1.13 is the
connected-sum characterisation); and Theorem 1.7 is **Casson-Gordon's**, printed
by Agol-Ren as "Theorem 1.7 ([CG83])". `research/01_source_verification.md`
already had 1.15, 1.6 and 1.11 right; it did not record 1.13/1.14 verbatim, and
did not record the remark of Section 2 at all.

---

## 2. Route 2 (new) - through Question 1.15 and the characteristic-submanifold remark

Agol-Ren record, immediately after Question 1.15, an unnumbered remark:

> Using the characteristic submanifold theory in the spirit of the arguments in
> [Bon83], one can show that if `K_1, K_2` are hyperbolic knots with genus at
> most 3, and are each minimal with respect to `<=_h`, then the existence of a
> fibered knot `K` with `K_1 <=_h K`, `K_2 <=_h K` implies that `K_1 = K_2`.

Our pair satisfies every hypothesis of that remark: both hyperbolic (G2), both of
genus `2 <= 3` (G1c, G8), both `<=_h`-minimal (Section 3, with the caveat there),
and `K_0 != K_1` (G3). Therefore:

> **Proposition R2.** If `K_0 ~ K_1`, then the `<=_h` form of Agol-Ren
> Question 1.15 has a **negative** answer.
>
> *Proof.* A positive answer would supply a fibered `K` with `K_0 <=_h K` and
> `K_1 <=_h K`; the remark then forces `K_0 = K_1`, contradicting G3. []

> **Corollary R2'. (second route to the campaign's target)** If `K_0 ~ K_1`, the
> Slice-Ribbon conjecture is false.
>
> *Proof.* Agol-Ren observe that Question 1.15 "is implied by the slice-ribbon
> conjecture, since one could take `K = K_1 # K_2 # (-K_1)`". Combine with
> Proposition R2. []

**Why this is genuinely independent of Route 1.** Route 1 runs through Theorem
1.13, i.e. through the classification of minimal compressions of surface
homeomorphisms and the prime-decomposition bookkeeping that Miyazaki's Theorems
5.3/5.5 supply. Route 2 runs through Bonahon-style characteristic submanifold
theory and the `K = K_1 # K_2 # (-K_1)` observation. They share only the standing
hypotheses on `K_0, K_1` (fibered, hyperbolic, genus 2, minimal, distinct), all of
which are re-checked by the enclosed checker. A single error in Miyazaki's
pairing theorem would not damage Route 2, and conversely.

**Honesty caveat, and it is a serious one.** The genus-`<=3` statement is an
*unnumbered remark with no proof in the paper* ("one can show"). Route 2 is
therefore strictly weaker evidence than Route 1, which rests on a stated,
proved theorem with an independent classical source. Route 2 must be reported as
a corroborating route, never as a substitute. It should not be relied on at all
until the remark is either proved here or obtained from [Bon83] plus a written
argument.

---

## 3. The minimality hypothesis, and an explicit gap

Both routes need `K_0` and `K_1` to be minimal with respect to `<=_h`. What the
repository has certified is the following, and it is worth being exact about it.

> **Fibered-minimality (certified).** Let `J` be a *fibered* knot with
> `J <=_h K_i`, `i in {0,1}`. Then `J = K_i`.
>
> *Proof.* By Casson-Gordon (Agol-Ren Theorem 1.7), the monodromy of `K_i`
> compresses to that of `J`. The genus lemma proved in
> `results/opus_2026_09_17_2230_alexander_divisibility_settled/` -
> `chi(d_e C) = chi(d_i C) + 2(a-b)` with `b > a` for a nontrivial compression,
> and `chi(F) = 1 - 2g` for a fibered knot - gives `g(J) < g(K_i) = 2` unless the
> compression is trivial. So `g(J) <= 1`.
> `g(J) = 0` means `J = U`, i.e. `K_i` is strongly homotopy-ribbon, hence slice,
> hence `det(K_i)` is a perfect square (Fox-Milnor/Murasugi). But `det = 13`
> (G5c) is not a square (G5d).
> `g(J) = 1` and `J` fibered leaves `J in {3_1, m3_1, 4_1}`. Friedl-Powell
> arXiv:1907.09031 Theorem 1.1, settled for `<=_h` in the 2230 directory, forces
> `Delta_J | Delta_{K_i} = t^4-3t^3+5t^2-3t+1`. Neither `t^2-t+1` nor
> `t^2-3t+1` divides it (G6; `Delta` is irreducible, G5b). []

**Gap.** Full `<=_h`-minimality additionally requires excluding *non-fibered*
`J <_h K_i`. Friedl-Powell gives `Delta_J | Delta`, and `Delta` is irreducible of
degree 4, so `Delta_J` is `1` or `Delta` up to units - but a knot with
`Delta_J = 1` is not excluded by any argument in this repository, and the genus
lemma above used fiberedness twice. So `Delta_J = 1` predecessors are **UNKNOWN**.

Consequence, stated precisely:

* **Route 1 is unaffected.** Theorem 1.13 quantifies only over *prime fibered*
  knots `J_i, K_i, K_{i,j}`, so the minimality it consumes is exactly
  fibered-minimality. Route 1 is complete as stated.
* **Route 2 is conditional on closing this gap**, because the remark says
  "minimal with respect to `<=_h`" without a fiberedness restriction. It is
  plausible that the remark's own proof only ever sees fibered predecessors (the
  Casson-Gordon compression picture is a statement about handlebodies bounding
  the fiber), but with no proof printed we cannot assert that.

Closing the gap - showing that a knot with trivial Alexander polynomial cannot be
a `<=_h`-predecessor of `6_3` or of `A_1(6_3)` - is now a well-posed, bounded
sub-problem and is the cheapest outstanding item this note generates.

---

## 4. What this changes operationally

The concordance question has been circling annulus-twist geometry, where the
literal object is dead: `research/14` Section 3 proves `pi_1(W - C) = Z`, which
with `Delta != 1` forbids destabilising the Theorem A trace annulus, and
`research/34` Section 6 shows Norman's trick fails homologically. Any concordance
must be a *different* surface, and no search has produced one.

Proposition R2 moves the question off that terrain entirely:

> `K_0 ~ K_1` is **incompatible** with a positive answer to Agol-Ren
> Question 1.15 restricted to hyperbolic genus-2 fibered pairs.

Two directions follow, and they are the two best next moves this note can point at.

**(a) Kill the lane.** Prove Question 1.15 (`<=_h` form) for hyperbolic genus-2
fibered pairs. By Proposition R2 this yields `K_0 !~ K_1` outright, retiring the
Abe-Tagami family and freeing the campaign. By Casson-Gordon Theorem 1.7 the
statement is entirely about surface homeomorphisms: *given two pseudo-Anosov
homeomorphisms of `Sigma_{2,1}` whose mapping tori are the two knot exteriors, is
there a surface homeomorphism compressing to both?* The two monodromies are
explicit (Abe-Tagami Appendix B):

```
phi_0 = t_d^-1 t_b t_c^-1 t_a
phi_1 = t_{c'_1}^-1 t_{c'_2} t_d^-1 t_b t_c^-1 t_a
```

on the genus-2 one-boundary fiber of `6_3`. They differ by exactly the twist pair
`t_{c'_1}^-1 t_{c'_2}` - which is the annulus twist, now expressed purely in the
mapping class group. This is a concrete, finite-looking object and is the first
time the campaign's central question has been written without reference to a
4-manifold.

**(b) Build the common upper bound.** Conversely, exhibiting a fibered `K` with
`K_0 <=_h K` and `K_1 <=_h K` would *not* give the concordance, but it would
refute the genus-`<=3` remark, which is itself a publishable outcome and a strong
signal about where the truth lies. Agol-Ren Corollary 1.11 gives an algorithm for
the downward direction (all `J <=_h K` for fixed fibered `K`); it does not bound
`K`, so this direction needs a guess. The natural guess is a fibered knot whose
monodromy is a common "uncompression" of `phi_0` and `phi_1`, i.e. a
homeomorphism of a genus-3 or genus-4 surface admitting two distinct compressions
realising `phi_0` and `phi_1`.

---

## 5. Status ledger

| claim | status |
|---|---|
| `K_0 ~ K_1` | **UNKNOWN** |
| Slice-Ribbon counterexample | **NO** |
| `K_0 ~ K_1 ==> Slice-Ribbon false`, Route 1 (Miyazaki / Agol-Ren Cor 1.14(1)) | **PROVED**, modulo the cited theorem |
| `K_0 ~ K_1 ==> Slice-Ribbon false`, Route 2 (Question 1.15 + genus-3 remark) | **PROVED modulo an unnumbered, unproved remark** - corroborating only |
| `K_0 ~ K_1 ==> Question 1.15 (`<=_h`) is false` | **PROVED modulo the same remark** (Proposition R2) |
| `K_0, K_1` fibered-minimal for `<=_h` | **PROVED** (Section 3) |
| `K_0, K_1` minimal for `<=_h` against non-fibered predecessors | **UNKNOWN** - explicit gap, Section 3 |
| 23 numerical/algebraic gates | **COMPUTATIONALLY VERIFIED**, `check_q115_reduction.py`, 23/23 |

## Reproduce

```
python3 check_q115_reduction.py            # prints RESULTS.json content, exit 0
```

Standard library plus sympy only; reads `data/knots/AbeTagami_L_63_c1_c2.json`
from the repository root. No network, no SnapPy, no Regina: every geometric fact
it uses is a *stored* certification produced by an earlier pass, and is labelled
as such in the check details rather than re-derived.
