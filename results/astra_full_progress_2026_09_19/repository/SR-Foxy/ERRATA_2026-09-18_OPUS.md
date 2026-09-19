# Errata — Opus night session, 18 September 2026

Astra's audit `research/36_audit_of_framing_and_miyazaki_closures.md` is correct
on every point it raises against my three commits `1110c67`, `e9616a6`,
`aa2df2c`. This records what was wrong, why, and what survives. Each item is
confirmed here independently rather than accepted on assertion.

---

## E18-1. The framing-to-polynomial corollary is FALSE

**Claimed** (`results/opus_2026_09_18_2300_framing_dichotomy/`, §2): "No
mixed-band design whatsoever — any paths, endpoints, over/unders or twists —
produces `D_{0,1}`."

**Refuted by the `0110` band choice**, already in
`results/astra_2026_09_18_local_band_no_go/README.md`: same two paths, same
endpoints, zero internal twists, zero linking — and at `r = 1` its Alexander
polynomial **is** the target `Delta^2`.

**The error.** I took `Delta_r = Delta^2 - r^2(t^3-t)^2`, which Astra derived for
the over/under choices `0000` and `0011` only, and treated it as a consequence of
the *linking number*. It is not. Astra's diagnosis is sharper than my own
correction would have been:

> `0000: B = [[0, q/d], [-q/d, 0]]`, `0110: B = [[0,0],[0,0]]`,
> with `d = Delta`, `q = t(t^2-1)`.
> **Same ordinary linking, different equivariant linking.** Ordinary linking is
> the `t = 1` specialization; it cannot determine the whole `t`-dependent matrix
> or its surgery determinant.

**Aggravating circumstance.** I quoted the `0110` fact myself — "Only 0110 and
1110 give Delta_target at r=1" — in my own summary of their report, and then wrote
a proposition contradicting it. The counterexample was in hand and in my own text.

**What survives.** Proposition L itself — `lk(eta_1, eta_2) = 0` for any band sum
of one upper to one lower marked circle — stands, by bilinearity, subject to the
orientation and band-sum-homology bookkeeping Astra flags. It is a statement about
*ordinary* linking and nothing more. Everything I built on top of it is withdrawn.

## E18-2. Proposition N is overstated

**Claimed** (`results/opus_2026_09_18_2200_delta_r_nogo/`): "Miyazaki Theorem 5.5
cannot certify any `B_r` with `r != 0` non-homotopy-ribbon."

**Correct scope:** Miyazaki's **alternative 2** (the norm-free condition) is
excluded, because `Delta_r` *is* the norm `f_r f_{-r}`. That part stands.
**Alternative 1** (minimality) is **not** excluded. My dismissal of it —
"minimality is incompatible with `B_r` being slice" — is circular, as Astra says:
proving minimality is precisely one way the non-homotopy-ribbon property could be
established, and ordinary smooth sliceness does not place `U` below a knot in the
homotopy-ribbon order. A minimality proof for such a boundary knot, plus an
independently constructed disk, would be exactly a counterexample.

The blanket title of that note is withdrawn; the alternative-2 exclusion is kept.

## E18-3. Irreducibility, superseded by an actual proof

I verified `f_r` irreducible only for `|r| <= 6` and then used it in an
all-integer statement. Astra supplies a proof for **every** integer `r`: `f_r` is
monic with constant term 1, so a rational linear factor needs an integer root
`+-1`, excluded by `f_r(1) = 1` and `f_r(-1) = 13`; and by Gauss's lemma any
further factorisation is into monic integral quadratics, which the constant-term
and coefficient comparisons exclude. My bounded verification is superseded.

## E18-4. "A CE is exactly ..." — sufficient, not a characterisation

`PLAN_CE_2026_09_18.md` §0 asserted a CE **is** a concordance class with two
distinct `<=_h`-minimal fibered knots. Agol-Ren Cor 1.14(1) gives only the
contrapositive: two such knots **suffice** to refute slice-ribbon. A counterexample
need not be fibered, composite, or of that form at all. The same overreach applies
to the four-term cable relation, stated there as `<=>`.

## E18-5. Algebraic sliceness does not force `tau = 0`

I wrote "`tau` does not obstruct, as Cor 1.3's algebraic sliceness already
implies". The computation `tau(P) = 2 - 3 + 5 - 4 = 0` stands on its own; the
justification does not. Astra's control: the positive untwisted Whitehead double of
the positive trefoil has `Delta = 1`, hence is algebraically slice, and `tau = 1`
by Hedden's formula (*Knot Floer homology of Whitehead doubles*, Geom. Topol. 11
(2007) 2277-2338).

## E18-6. Citation error, verified and propagated

arXiv:1806.06225 is **Davis-Park-Ray**, *Linear independence of cables in the knot
concordance group*, Trans. AMS 374 (2021) 4449-4479. I attributed it to
Dai-Hom-Stoffregen-Truong. **Independently confirmed** from the arXiv metadata:
`citation_author` = Davis, Christopher W.; Park, JungHwan; Ray, Arunima.

The error did not originate with me: `research/03_candidate_families.md` line 148
carries the same misattribution and is where I took it from. **That line should be
corrected too** — flagged here rather than edited, since `research/03` is another
worker's file.

Astra is also right that a theorem about one specified family does not transfer to
every proposed Hom-Park example. My "filling the rest of those cells is predicted
to be worthless" is unsupported as stated; the families and parameters have to be
matched first.

## E18-7. The involutive computation is not uncomputed

`PLAN_CE_2026_09_18.md` P5 called involutive Floer on the Abe-Tagami lane "live
and uncomputed". **`research/11_involutive_local_equivalence.md` exists** — "An
exhaustive involutive local-equivalence audit for K1", placing `K_1` in the
involutive local class of the figure-eight, conditional on its stored
lifting/input assumptions. Confirmed present in the repository. Auditing those
assumptions is a different and much cheaper task than starting from HFK ranks,
which is what I proposed.

## E18-8. Hosokawa-Yanagawa: wrong gap, and a missed erratum

`results/opus_2026_09_19_0200_hosokawa_yanagawa/` originally located the 1965
proof's failure in the Appendix Lemma and reported that no published erratum was
found. **Both wrong.** Astra's `research/39` found Fox's report; verified here
from the primary source, **Fox, _Characterizations of slices and ribbons_, Osaka
J. Math. 10 (1973) 69-76**, p. 69 footnote:

> "The proof presented in [4] has an error in the second paragraph of p. 380.
> This fact was communicated to me by the authors, who cited diagram 2 to
> illustrate the difficulty."

Page 380 opens "[II] Triple points", so the error is in triple-point elimination,
in section 3, **before the appendix is ever invoked**. The synthesis I drew from
the misplacement - that the 1965 gap "is" the M1 unlink-derivative wall, and that
a CE must have an unavoidably linked derivative disk system - is **withdrawn**.

What survives: Lemma 2 really is the derivative-link picture in the 1965 source,
and the caution that the paper's true corollary (Fox-Milnor via Terasaka) came out
of a flawed proof.

**This is the third instance of one failure mode tonight**, with E18-1 and E18-2:
a bounded derivation generalised into a universal statement without checking it
against something checkable. In all three cases the checkable thing existed and I
did not look.

---

## What still stands from the three commits

* **Theorem F** and **Corollary M** (`opus_2026_09_18_0005`) — untouched by this
  audit.
* **Proposition L**, in its ordinary-linking form only (E18-1).
* The **alternative-2 exclusion** for `Delta_r` (E18-2).
* The independent reproduction of Astra's `Delta_r` identities, the `det = 169`
  and `f_r(-1) = 13` facts, and the coincidence of the dual-path polynomial with
  `Delta_1`.
* The **census evidence recovery and reconciliation** (`opus_2026_09_18_2100`),
  including the measured-as-nil bin-boundary repair.
* The **orientation bug fix** (`85b05cb`): `isometry_signature` defaults to the
  unoriented invariant and was silently accepting mirror pairs.

## Lesson

Two of the three withdrawn claims share one failure mode: I generalised a result
derived under specific hypotheses (particular over/under bits; a particular
Miyazaki alternative) into a universal statement, without checking the
generalisation against data I had already read. The campaign's standing rule
against turning a bounded search into a theorem applies just as much to turning a
bounded *derivation* into one.
