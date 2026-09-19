# Corollary Q: fibered + irreducible `Delta` ⟹ `<=_h`-minimal

19 September 2026, Opus. **CE: NO.**
**Smooth concordance: UNKNOWN. Slice-Ribbon CE: NO.**

`check_corollary_q.py` -> `RESULTS.json`, **26/26**, SnapPy 3.3.2, sympy 1.14.0.

---

## 1. Statement

> **Corollary Q.** Let `K` be a nontrivial fibered knot whose Alexander
> polynomial is irreducible over `Z`. Then `K` is minimal for `<=_h`.

*Proof.* Let `J <=_h K`, `J != K`.
`K` is fibered and nontrivial, so `J` is fibered (**Theorem F**). Casson-Gordon
(**Agol-Ren Thm 1.7**) and the compression genus lemma — both available now that
`J` and `K` are *both* fibered — give `g(J) < g(K)`. **Friedl-Powell** gives
`Delta_J | Delta_K`; irreducibility leaves `Delta_J in {1, Delta_K}`. A fibered
knot has monic `Delta` of degree exactly `2g`, so
`deg Delta_J = 2g(J) < 2g(K) = deg Delta_K` excludes `Delta_J = Delta_K`. Hence
`Delta_J = 1`, hence `g(J) = 0`, hence `J = U`. But `U <=_h K` says `K` is
strongly homotopy-ribbon, hence slice, and an irreducible `Delta_K` of degree
`>= 2` is never a Fox-Milnor norm `f(t)f(1/t)`. Contradiction. []

## 2. What is new here, honestly

**Not a new target.** `scripts/zero_surgery_pair_search.py` already operates on
exactly this population, justified by **Miyazaki Thm 5.5**: two distinct prime
fibered knots with irreducible `Delta` have a connected sum that is never
homotopy-ribbon, so a concordance between them refutes slice-ribbon.

What Corollary Q adds is a **second route to the same premise that does not pass
through Miyazaki's alternatives at all.** That matters because
`ERRATA_2026-09-18_OPUS.md` E18-2 records this campaign misreading which of
Miyazaki's two alternatives it was entitled to. Two routes with *disjoint* weak
points is the point — Corollary Q is not stronger, it is differently
conditioned.

It also sharpens the criterion already in `PLAN_CE_2026_09_18.md` §0 ("`Delta_J`
irreducible of degree `2g(J)` and `J` not slice ⟹ minimal"): **for a fibered
knot both side conditions are automatic.** Degree `2g` is forced by fiberedness;
not-slice is forced by Fox-Milnor. Only irreducibility has to be checked.

And it generalises **Corollary M**, whose stored proof needed genus 2 to get a
finite classified predecessor list, `det = 13` not a square, and two specific
quadratic divisors. Routing through fiberedness twice replaces the case list.

## 3. Verified vs. assumed

**Checked here (26/26):** `deg Delta = 2g` and monicity on `K_0..K_3`;
irreducibility over `Z`; and an **exhaustive** search for a Fox-Milnor factor
`f` with `deg f <= 3`, `|coeff| <= 8`, finding none. The degree argument alone
suffices; searching anyway is the cheap independent confirmation that the errata
says was skipped three times when it existed.

**NOT verified here:** Theorem F (this repo, resting on **Sun arXiv:2604.20785
Thm 1.1 — UNREFEREED**, read in full), Agol-Ren Thm 1.7, the compression genus
lemma, Friedl-Powell, Agol-Ren Cor 1.14(1), Fox-Milnor.

## 4. What it does not do

It supplies **no concordance and no slice disk.** It says the census population
is one where *any* concordance between two distinct members is a counterexample
— which was already the operating premise. The missing half of every lane is
unchanged.

## Reproduce

```
python3 check_corollary_q.py     # exit 0, 26/26
```
