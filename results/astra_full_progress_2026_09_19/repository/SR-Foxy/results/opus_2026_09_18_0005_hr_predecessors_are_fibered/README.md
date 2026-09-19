# Every `<=_h`-predecessor of a fibered knot is fibered, so `K_0` and `K_1` are
# `<=_h`-minimal outright

18 September 2026, Opus session. **NO COUNTEREXAMPLE.**
**Smooth concordance `K_0 ~ K_1`: UNKNOWN. Slice-Ribbon CE: NO.**

This pass closes the gap that the previous pass
(`results/opus_2026_09_17_2355_agol_ren_q115_reduction/`, Section 3) flagged as
UNKNOWN, and that `results/chat_archive_2026_09_17/CORRECTION_REGISTER.md`
item 18 independently flagged as unverified.

`check_minimality_closed.py` -> `RESULTS.json`: 13/13, sympy 1.14.0.

---

## 1. The gap, restated

Both routes from "`K_0 ~ K_1`" to "Slice-Ribbon is false" consume the hypothesis
that `K_0 = 6_3` and `K_1 = A_1(6_3)` are **minimal with respect to `<=_h`**.
What this repository had proved was strictly weaker:

> **Fibered-minimality (previous pass).** If `J` is a *fibered* knot with
> `J <=_h K_i`, then `J = K_i`.

The proof went through Casson-Gordon (Agol-Ren Theorem 1.7), which is stated for
`J, K` both fibered, and then through the compression genus lemma, which reads
`chi(F) = 1 - 2g` off a fiber surface. Both steps need `J` fibered. A
non-fibered predecessor was therefore not excluded, and the one surviving shape
was sharp: Friedl-Powell forces `Delta_J | Delta` with `Delta` irreducible of
degree 4, and the genus lemma was unavailable, so a predecessor with
`Delta_J = 1` was not ruled out by anything in the repository.

Route 1 (Miyazaki / Agol-Ren Corollary 1.14(1)) was unaffected, because
Agol-Ren Theorem 1.13 quantifies only over prime **fibered** knots. Route 2 (the
characteristic-submanifold remark) was left conditional.

## 2. The gap is empty

> **Theorem F.** Let `J, K` be knots with `J <=_h K`, i.e. there is a strongly
> homotopy-ribbon concordance from `J` to `K` in some homotopy `I x S^3`. If `K`
> is fibered and nontrivial, then `J` is fibered.

*Proof.* Let `C` be the concordance in the homotopy `I x S^3` called `Z`, and
put `W = Z \ N(C)`, `Y_- = E_J`, `Y_+ = E_K`, the two knot exteriors.

1. **`W` is a homology cobordism from `Y_-` to `Y_+`.** `Z` is a homotopy
   `I x S^3`, hence a homology `I x S^3`. Mayer-Vietoris for
   `Z = W u N(C)` with `W n N(C) = dN(C) ~ T^2` and `N(C) ~ S^1` gives
   `H_1(W;Q) = Q`, and the remaining degrees likewise; this is the standard fact
   that a concordance exterior is a homology cobordism between the knot
   exteriors, and it uses only `H_*(Z) = H_*(S^3)`, not standardness of `Z`.
2. **`W` is ribbon.** Agol-Ren's definition of strongly homotopy-ribbon is, in
   their words, that the complement "admits a relative handle decomposition with
   only 1- and 2-handles" - relative to the `E_J` end. That is verbatim Sun's
   ribbon condition.
3. **Both ends have toroidal boundary**, which Sun's Theorem 1.1 allows.
4. Let `phi_+` generate `H^1(E_K;Z) = Z`, sending the meridian to 1. `K`
   fibered and nontrivial means `phi_+` is a fibered class. Under the natural
   identification `H^1(Y_+;Q) = H^1(W;Q) = H^1(Y_-;Q)` supplied by the homology
   cobordism, `phi_+` corresponds to the generator `phi_-` of `H^1(E_J;Q)`,
   because meridian pairs with meridian (Sun's Corollary 1.2 makes exactly this
   identification).
5. Sun, arXiv:2604.20785, **Theorem 1.1**: `phi_+` fibered implies `phi_-`
   fibered. So `E_J` fibers over `S^1` with fiber dual to the meridian class,
   i.e. `J` is a fibered knot. []

**What makes this work for `<=_h` and not just for `<=`.** The knot statement
for genuine ribbon concordance is classical (Silver 1992, Kochloukova 2006, as
Sun attributes it). The new content is that Sun's Lemma 3.1 - the
Gerstenhaber-Rothaus extension of a representation into a compact connected Lie
group, which is Gordon's own tool - needs *only* the handle structure
`W = Y_- x I u 1-handles u 2-handles` together with the homology isomorphism. It
never asks for a band presentation, for the concordance to have no local maxima,
or for the ambient to be the standard `I x S^3`. Those are precisely the three
things `<=_h` gives up relative to `<=`.

## 3. Consequence: minimality, unconditionally

> **Corollary M.** `K_0 = 6_3` and `K_1 = A_1(6_3)` are minimal with respect to
> `<=_h`, with no fiberedness restriction on the predecessor.

*Proof.* Let `J <=_h K_i`. Both `K_i` are fibered (G1b/G8 of the previous pass)
and nontrivial, so `J` is fibered by Theorem F. Now the previously certified
argument applies in full, and the case list is finite and complete:

* Casson-Gordon plus the compression genus lemma give `g(J) < g(K_i) = 2`
  unless the compression is trivial, so `g(J) <= 1`.
* The fibered knots of genus `<= 1` are exactly `U`, the two trefoils, and
  `4_1` (genus-one fibered knots have once-punctured-torus fiber; classical).
* `g(J) = 0`: `J = U` means `K_i` is strongly homotopy-ribbon, hence slice,
  hence `det(K_i)` is a perfect square. It is 13 (C1), not a square (C2).
* `g(J) = 1`: Friedl-Powell forces `Delta_J | Delta = t^4-3t^3+5t^2-3t+1`, which
  is irreducible (C3). Neither `t^2-t+1` nor `t^2-3t+1` divides it (C4). []

The `Delta_J = 1` worry is subsumed twice over: a fibered knot has monic
Alexander polynomial of degree exactly `2g`, so `Delta_J = 1` forces `g(J) = 0`
and `J = U`, already excluded.

## 4. What this changes

* **Route 2 is no longer conditional on the minimality hypothesis.** It remains
  conditional on Agol-Ren's unnumbered genus-`<=3` remark itself, which is still
  printed without proof. That caveat stands unchanged and must keep being
  reported.
* **Route 1 is unchanged** - it never needed this - but the two routes now rest
  on the *same*, now-complete, minimality statement rather than on two different
  strengths of it.
* **A general simplification for the whole `<=_h` lane in this repository.**
  Theorem F says the predecessor set of any fibered knot consists of fibered
  knots. So Agol-Ren Corollary 1.11's enumeration algorithm, and the entire
  Casson-Gordon compression picture, see *every* predecessor - none are hiding
  in the non-fibered world. Wherever this repository has reasoned about
  `<=_h`-predecessors under an unstated fiberedness assumption, that assumption
  is now discharged rather than merely plausible.
* `CORRECTION_REGISTER.md` item 18 asked for the source hypotheses of the
  minimality step to be checked independently. They have now been checked, one
  of them was genuinely insufficient, and the deficiency is repaired rather than
  argued away.

## 5. Honest limits

* Sun arXiv:2604.20785 is an **unrefereed preprint** (v2, 6 May 2026). Theorem F
  is only as good as it is. It is, however, a short note whose proof I have read
  in full and whose ingredients (Friedl-Kim, Friedl-Vidussi, Gerstenhaber-
  Rothaus, Gordon) are all long-established.
* Theorem F is an **application** of Sun's Theorem 1.1, not an extension of it.
  The only work done here is checking that `<=_h` satisfies its hypotheses -
  the direction conventions, the homology-cobordism property in a homotopy
  `I x S^3`, and the meridian-to-meridian identification of the fibered class.
  Sun states the link-level ribbon-concordance corollary but does not state the
  `<=_h` knot corollary, so this specific consequence is not in his paper.
* **This does not advance the concordance question itself.** `K_0 ~ K_1` remains
  UNKNOWN. What improved is the certainty of the implication chain that a
  concordance would feed into.

## 6. Status ledger

| claim | status |
|---|---|
| `K_0 ~ K_1` | **UNKNOWN** |
| Slice-Ribbon counterexample | **NO** |
| Theorem F: `J <=_h K`, `K` fibered nontrivial `=>` `J` fibered | **PROVED**, modulo Sun Thm 1.1 (unrefereed) |
| Corollary M: `K_0, K_1` are `<=_h`-minimal, unrestricted | **PROVED** |
| previous pass's non-fibered `Delta = 1` gap | **CLOSED** (was UNKNOWN) |
| Route 1 (Miyazaki / Agol-Ren Cor 1.14(1)) | **PROVED**, modulo the cited theorem |
| Route 2 (Question 1.15 + genus-3 remark) | still modulo the **unproved remark** - corroborating only |
| 13 arithmetic/case gates | **COMPUTATIONALLY VERIFIED**, 13/13 |

## Reproduce

```
python3 check_minimality_closed.py       # prints RESULTS.json content, exit 0
```

Standard library plus sympy; reads `data/knots/AbeTagami_L_63_c1_c2.json`. No
network. Every external theorem it relies on is listed in `RESULTS.json` under
`external_inputs_not_verified_here` and quoted verbatim in `SOURCES.md`.
