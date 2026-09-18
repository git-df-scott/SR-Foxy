# Hosokawa-Yanagawa 1965: the gap is the unlink-derivative question, and always was

19 September 2026, Opus. **CE: NO.** A source reading, not a computation.

**Correction, 18 September 2026:** Fox's *Characterizations of slices and
ribbons*, Osaka J. Math. 10 (1973), p.69 footnote 1, explicitly reports the
authors' acknowledgement of an error in the second paragraph of p.380 of
the 1965 paper. That paragraph concerns triple-point elimination. Moreover,
the appendix continues beyond repeated Dehn's lemma with a ball/homeomorphism
argument for mutual disjointness. The historical diagnosis in sections 1--3
below is therefore superseded; the original text is retained as an audit trail.
See [research/39](../../research/39_fox_locates_the_hosokawa_yanagawa_error.md)
and [Fox's published paper](https://www.i-repository.net/contents/osakacu/sugaku/111F0000002-01001-8.pdf).

**Hosokawa, F. and Yanagawa, T., _Is every slice knot a ribbon knot?_,
Osaka J. Math. 2 (1965), 373-384.** Text extracted from the Project Euclid PDF
(12 pages) and read in full.

Verbatim from the introduction:

> "R. H. Fox presented a problem 'Is every slice knot a ribbon knot?' in his
> paper [2]. **The purpose of this paper is to give an affirmative answer to the
> problem.**"

and, at the end of §2:

> "Thus we can obtain a ribbon modified from `sigma` with the boundary `K`.
> Therefore we have **Theorem. Every slice knot is a ribbon knot.**"

So this is a claimed *proof* of the slice-ribbon conjecture.

---

## 1. Status, stated carefully

The conjecture is **open**. Gukov-Halverson-Manolescu-Ruehle (2022) state it as
"Conjecture 2.1 (Slice-Ribbon Conjecture, [Fox62]). Every slice knot is ribbon"
and call it "a famous unsolved problem"; Agol-Ren (2026) treat it as a
conjecture throughout. The 1965 proof is therefore not accepted by the field.

**I did not find a published erratum or a documented refutation**, and I am not
asserting one. What follows identifies which step carries the weight — not a
proof that the step is false.

## 2. The argument, and where the weight sits

1. **Lemma 1** puts the spanning 2-cell in `(-1,1)`-canonical form: all elliptic
   critical points of type I (births) at `t = -1`, all of type II (deaths) at
   `t = 1`, saddles in between. This is the standard normal form for a surface in
   4-space and is **not** where the problem is, despite the thin justification
   given ("since `H^4[-1,1] - e^2` is arcwise connected, it is easy to modify").
2. **Lemma 2** is the real structural content, and it is correct and familiar:
   > "If a knot `K` is a slice knot in `R^3`, there exists in `R^3 - kappa` a
   > collection of `r` mutually disjoint, non-singular 2-cells
   > `sigma_1, ..., sigma_r` such that `K` and the boundary circles
   > `a_1, ..., a_r` bound a **perforated ribbon** in `R^3`."
3. The Theorem then follows **if** the remaining singular disks can be replaced
   by *mutually disjoint* embedded ones. That is the **Appendix Lemma**:
   > "If `D_1, ..., D_r` is a set of normal, canonical Dehn-disks such that
   > `dD_i ∩ D_j = ∅` (`i != j`) in a 3-manifold `M`, then there exists a set of
   > **mutually disjoint**, non-singular disks `delta_1, ..., delta_r` such that
   > `delta_i` is identical with `D_i` in a sufficiently small neighborhood of
   > `dD_i`."
   >
   > *Proof.* "By making use of Dehn's lemma repeatedly ..."

Dehn's lemma applied repeatedly makes each disk **embedded**. It does not make
them **mutually disjoint**. Disjointness of a whole disk system is a strictly
stronger demand than embeddedness of each member, and it is the only step in the
paper doing real work.

## 3. Why this matters to the campaign

Read in modern language, Lemma 2 says a slice knot has a **derivative link**
`a_1 ∪ ... ∪ a_r` bounding disjoint disks in the complement, with `K` and the
`a_i` cobounding a perforated ribbon; and the Appendix Lemma asserts that the
associated disk system can always be made disjoint — i.e. in effect that **the
derivative can always be taken to be an unlink**.

> **The 1965 gap and the campaign's M1 wall are the same gap.**

`research/02`, `research/06`-`07` and `research/22` identify the missing
ingredient as exactly this: no theorem converts a known R-link derivative into an
unlink derivative, and "no unlink derivative" is an infinite search with no
bounding theorem. That is not a modern artifact of Floer-theoretic technique.
It is the step at which the original attempted proof stalls, and it has stood for
**sixty-one years**.

**Consequence for a counterexample.** Any CE must be a knot whose derivative disk
system is *unavoidably* linked — the obstruction is the impossibility of
disjointing a system of embedded disks, not a property of any single disk. That
is a 3-dimensional condition, while almost every tool the campaign holds is
4-dimensional, which is a plausible reason the board looks the way it does.

**A caution worth recording.** The paper's stated corollary — that a slice knot's
Alexander polynomial has the form `f(t) f(t^{-1})`, via Terasaka's theorem for
ribbon knots — **is true**, and was proved independently by Fox-Milnor (1966). A
flawed proof can carry true corollaries, so agreement of a consequence is not
evidence for the argument.

## 4. What this is not

* Not a refutation of the Appendix Lemma. I identify it as load-bearing; I have
  not shown it false, and the obvious Borromean-rings counterexample to a naive
  "disjoint Dehn's lemma" **does not apply**, because its hypothesis
  `dD_i ∩ D_j = ∅` fails there.
* Not a new obstruction, construction, or candidate. No computation was run.
* Not a claim about the historical literature beyond what is quoted; no erratum
  was located.
