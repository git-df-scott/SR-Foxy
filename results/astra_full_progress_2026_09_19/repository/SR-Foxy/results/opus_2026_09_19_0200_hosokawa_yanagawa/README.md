# Hosokawa-Yanagawa 1965 — CORRECTED: Fox located the error, and I had it wrong

19 September 2026, Opus. **CE: NO.** A source reading, not a computation.

> **Correction, same night.** The first version of this note (a) located the gap
> in the Appendix Lemma and (b) said no published erratum was found. **Both are
> wrong.** Astra's `research/39` found Fox's published report; I then verified it
> from the primary source, and it places the error somewhere else entirely. The
> structural synthesis I drew from my misplacement — that the 1965 gap "is" the
> unlink-derivative wall — is **withdrawn**. What survives is marked below.

---

## 1. The paper

**Hosokawa, F. and Yanagawa, T., _Is every slice knot a ribbon knot?_,
Osaka J. Math. 2 (1965), 373-384**,
<https://projecteuclid.org/euclid.ojm/1200691465>. Read in full.

> "R. H. Fox presented a problem 'Is every slice knot a ribbon knot?' in his
> paper [2]. **The purpose of this paper is to give an affirmative answer.**"
>
> "... **Theorem. Every slice knot is a ribbon knot.**"

The conjecture is open, so the proof fails. The question is *where*.

## 2. Where the error actually is — Fox, 1973, verbatim

**Ralph H. Fox, _Characterizations of slices and ribbons_, Osaka J. Math. 10
(1973), 69-76**, footnote on p. 69
(<https://www.i-repository.net/contents/osakacu/sugaku/111F0000002-01001-8.pdf>),
fetched and text-extracted here:

> "**The proof presented in [4] has an error in the second paragraph of p. 380.**
> This fact was communicated to me by the authors, who cited diagram 2 to
> illustrate the difficulty. Diagram 1, from which diagram 2 may be generated was
> communicated to me by I. Johansson."

So the error was **known by 1973 and reported by the authors themselves**.

**What is on p. 380.** The page opens with "Fig. 8 **[II] Triple points**", and its
second paragraph is the start of triple-point elimination:

> "Now, we will consider triple points on double lines of ribbon type. By the
> considerations about singularities of `sigma` in section 2, one of the three
> inverse images of every triple point does not belong to `l`-line. By cutting
> `sigma` along the image of an arc starting from a boundary point and disjoint
> with `l`-lines, we may suppose that `E'G'` is a subarc of an `l`-line ... and
> `G'A` does not contain any inverse image of triple points ..."

That is **§3 [II], before the Appendix Lemma is ever invoked** — the appendix is
applied later, in §4.

## 3. What I got wrong, and how

I read the paper, judged the Appendix Lemma ("by making use of Dehn's lemma
repeatedly" ⟹ *mutually disjoint* embedded disks) to be the only step doing real
work, and built on it: that the 1965 gap and the campaign's M1 wall are the same
gap, and that a counterexample must therefore have an unavoidably linked
derivative disk system.

The reasoning was plausible and the conclusion was unsupported. I had not
established that the Appendix Lemma fails — I said so at the time — and then
reasoned from it anyway. Astra's `research/39` further notes that the appendix
continues past the Dehn's-lemma appeal with an ambient-motion argument, and that
its hypotheses are stronger than arbitrary nullhomotopy.

**This is the third time tonight I have built a structural claim on a step I had
not verified** — after the framing-to-polynomial corollary and the blanket form of
Proposition N (`ERRATA_2026-09-18_OPUS.md`, E18-1 and E18-2). The pattern is the
same each time: a bounded derivation generalised into a universal statement
without checking it against something checkable.

## 4. What survives

* **Lemma 2 is correct and is the derivative-link picture in the 1965 source**:
  > "If a knot `K` is a slice knot in `R^3`, there exists in `R^3 - kappa` a
  > collection of `r` mutually disjoint, non-singular 2-cells `sigma_1,...,sigma_r`
  > such that `K` and the boundary circles `a_1,...,a_r` bound a **perforated
  > ribbon** in `R^3`."
  That observation stands on its own and does not depend on where the proof
  fails.
* **Lemma 1's canonical form** (births, then saddles, then deaths) is the standard
  normal form for a surface in 4-space, and is not the problem.
* **A caution worth keeping.** The paper's corollary — a slice knot's Alexander
  polynomial has the form `f(t)f(t^{-1})`, via Terasaka — **is true**, proved
  independently by Fox-Milnor in 1966. A flawed proof can carry true corollaries,
  so a consequence checking out is not evidence for the argument. Given how much
  of this campaign is consequence-checking, that is the most useful thing in this
  note.
* Fox's own paper is worth reading for its own sake: it proves **Theorem A**, that
  `K` is slice iff `K & 0 & ... & 0` is a weak ribbon link for large enough `mu`,
  citing Murasugi and Hosokawa-Yanagawa Lemma 2 — i.e. the corrected 1973 form of
  what the 1965 paper was reaching for.

## 5. Withdrawn

* "The 1965 gap and the M1 wall are the same gap."
* "A CE must be a knot whose derivative disk system is unavoidably linked."
* "I found no published erratum" — Fox published one in 1973; my search simply
  failed to surface it.

Neither the location of the error nor Fox's pictured difficulty (diagrams 1 and 2)
has been reconstructed here.
