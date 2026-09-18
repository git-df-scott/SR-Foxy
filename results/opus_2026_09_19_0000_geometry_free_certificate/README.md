# The Abe-Tagami non-ribbon certificate needs no geometry

19 September 2026, Opus. **CE: NO.**
**Smooth concordance `K_0 ~ K_1`: UNKNOWN. Slice-Ribbon CE: NO.**

An audit of the half of the counterexample the campaign actually *has*.

`check_geometry_free.py` -> `RESULTS.json`, **11/11**, spherogram 2.4.1,
sympy 1.14.0. No geometry, no network, no Sage.

---

## 1. What was resting on what

Miyazaki Thm 5.5 and Agol-Ren Thm 1.13 both quantify over **prime fibered**
knots, and the campaign's use of them also needs `K_0 != K_1` and an irreducible
Alexander polynomial. Until now three of those four facts rested on SnapPy's
**numerical** hyperbolic geometry:

* *prime* — inferred from "hyperbolic implies prime", with hyperbolicity taken
  from a floating-point volume;
* *distinct* — from a volume comparison and `is_isometric_to`;
* the identification of the stored `K_1` — likewise.

`verify_hyperbolicity()`, which would make hyperbolicity rigorous, **requires Sage
and raises `SageNotAvailable` in this container**. So the certificate's hypotheses
were not rigorously established.

They do not need to be.

## 2. Lemma P

> **Lemma P.** A fibered knot with irreducible Alexander polynomial is **prime**.

*Proof.* If `K = K_1 # K_2` is fibered then both summands are fibered, and
`Delta_K = Delta_{K_1} Delta_{K_2}`. Irreducibility forces some `Delta_{K_i} = 1`.
A fibered knot has `deg Delta = 2g`, so that summand has `g = 0` and is the
unknot. The decomposition is therefore trivial. []

No geometry, no hyperbolicity, no Sage.

## 3. The certificate, recertified combinatorially

| hypothesis | how it is certified now |
|---|---|
| `K_0`, `K_1` **fibered** | Ni's theorem (Ghiggini in genus 1): rank of `HFK-hat(K, g)` is **1**, checked directly rather than read off the calculator's summary flag |
| `deg Delta = 2g` | `4 = 2 x 2` for both |
| `Delta` **irreducible** | exact arithmetic on `t^4-3t^3+5t^2-3t+1` |
| **prime** | Lemma P, from the two above |
| `K_0 != K_1` | bigraded `HFK` groups differ: `delta`-levels `{0}` versus `{-2, 0}` |
| Miyazaki **alternative 2** | irreducible `Delta` admits no `f` with `f(t)f(1/t) | Delta` |

Every entry is combinatorial. The non-ribbon half of the Abe-Tagami lane no longer
depends on a volume, on `is_isometric_to`, or on hyperbolicity.

**Why this matters for a counterexample.** If a slice disk is ever produced, the
implication "slice + non-ribbon => slice-ribbon is false" now runs on exact
arithmetic end to end. The remaining external inputs are the cited theorems
themselves — Ni, Miyazaki 5.5, Agol-Ren 1.13 — not a floating-point computation.

## 4. What this does NOT do

* It says **nothing** about whether `D_{0,1}` is slice. Only the certificate's
  hypotheses are hardened; the missing disk is still missing.
* Ni's theorem and Miyazaki Thm 5.5 are **cited, not reproved**.
* The PD codes are taken from `data/knots/` as committed. This audit does not
  re-derive them from Abe-Tagami's figures, and the identification of the stored
  `K_1` with `A_1(6_3)` still rests on the construction card's numerical Dehn
  filling. **That identification remains the weakest link**, and it is now the
  only numerical dependency left in the lane.
* Hyperbolicity claims elsewhere in the repository remain numerical. They are
  simply not needed here.

## Reproduce

```
python3 check_geometry_free.py      # exit 0
```
