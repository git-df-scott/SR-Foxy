# The two-lattice lemma for derivatives on the fiber of K_G (2026-09-11)

> **2026-09-12 computation:** The stored matrix is singular 28×28, not the fiber matrix. The [exact audit](../results/seifert_model_exact_audit.json) now supplies an integral S-reduction to 10×10 and both saturated isotropic lattices. This is an algebraic model; no embedded fiber identification has been supplied. The finite homology alternatives do not classify geometric derivatives or stabilized surfaces.

Status: proof written here, not yet refereed. Builds on `06_theory_derivatives_on_fiber.md`, Theorem 3.1 (monodromy-invariant Lagrangians are Seifert-form metabolizers) and its notation: K fibered of genus g with fiber F, Seifert form v(x,y) = lk(x, y⁺) with unimodular matrix V, monodromy φ = φ_* on H₁(F) satisfying Vᵀφ = V, so v(x,y) = v(φy, x) for all x, y (identity (∗∗) there).

## Lemma A (converse of Theorem 3.1). For a fibered knot, every metabolizer of the Seifert form is monodromy-invariant.

Proof. Let M ⊂ H₁(F;Q) be a metabolizer: rank g and v|_{M×M} = 0. Put M^⊥ = {z : v(z, x) = 0 for all x ∈ M}. Since V is unimodular, dim M^⊥ = 2g − g = g, and M ⊂ M^⊥ because v vanishes on M. Hence M^⊥ = M. For x, y ∈ M, identity (∗∗) gives v(φy, x) = v(x, y) = 0, so φy ∈ M^⊥ = M. Thus φM ⊂ M, and φ is invertible, so φM = M. ∎

Together with Theorem 3.1 (which needs Δ_K(1) = ±1, true for every knot): **for a fibered knot, {metabolizers of V} = {φ-invariant Lagrangians of the intersection form}.** In particular the derivative classes of any derivative on the fiber span a φ-invariant sublattice.

## Lemma B. If Δ_K = f·f* with f irreducible over Q and f ≠ ±f* (f*(t) = t^{deg f} f(1/t)), then H₁(F;Q) has exactly two φ-invariant g-dimensional subspaces, N₁ = ker f(φ) and N₂ = ker f*(φ), and every metabolizer of V is one of N₁ ∩ H₁(F;Z) or N₂ ∩ H₁(F;Z).

Proof. The characteristic polynomial of φ is Δ_K (see the check under (∗) in the theory notes). With f, f* coprime and each irreducible, H₁(F;Q) = N₁ ⊕ N₂ as Q[φ]-modules, each summand a simple module of dimension deg f = g. A φ-invariant subspace is a direct sum of submodules of the simple summands, i.e. one of 0, N₁, N₂, N₁ ⊕ N₂; the g-dimensional ones are N₁ and N₂. Lemma A places every metabolizer among them. Derivative classes form part of a basis of H₁(F;Z) (F − L connected planar), so the lattice they span is saturated, hence equals N_i ∩ H₁(F;Z). ∎

## Application to K_G = 18nh00000601

- Δ = t¹⁰ − 2t⁹ + t⁸ − t⁷ + 4t⁶ − 7t⁵ + 4t⁴ − t³ + t² − 2t + 1 = f(t)·f*(t) with f = t⁵ − t² + 2t − 1, irreducible over Q (checked with sympy), and f* = t⁵ − 2t⁴ + t³ − 1 ≠ ±f. Genus 5 = deg f. (Computed 2026-09-11 from the Seifert matrix; `data/knots/18nh00000601_seifert.json`.)
- Therefore: **every derivative of K_G on its fiber, unlink or R-link, has homology span equal to one of two explicit rank-5 lattices M₁, M₂.** Whether both are actually metabolizers is decided by evaluating V on N_i; at least one is, since K_G is algebraically slice and the metabolizer of a genus-5 unlink derivative would be one of them. (The Oliveira-Smith disk supplies an R-link derivative, so at least one N_i carries a derivative.)
- The remaining freedom is geometric, not homological: cut systems L ⊂ F with span[L] = M_i, modulo isotopy, form an infinite set acted on by the stabilizer of M_i in the mapping class group. The ribbon question for a genus-5 ribbon disk of K_G (Theorem 1.4 of the theory notes, modulo its flagged Cochran–Davis genus count) is exactly: does some cut system with span M₁ or M₂ have free link group?

## What this buys

1. A fast, exact linear-algebra filter for any enumeration of cut systems on F: reject unless span[L] ∈ {M₁, M₂}. This is the "φ-invariance filter" of the theory notes' §P4.2 step 3, sharpened to two explicit targets.
2. A structural reason the Seifert form cannot separate ribbon from handle-ribbon here: both notions live on the same two lattices.
3. Needs F and φ explicitly to be applied (TOOLING.md item 6). Without the fiber, the lemma is a statement about an abstract lattice.

## Caveats

- Lemma B needs f ≠ ±f*. For K_G, f* is not ±f (coefficient lists differ), so the hypothesis holds.
- Both lemmas are about the fiber only. Derivatives on stabilized Seifert surfaces (higher-band ribbon disks) are not constrained by them; that is the stabilization barrier already recorded in the theory notes.
