# Sources and files actually read this pass

## Files read, with the version read

On the working branch `claude/compassionate-carson-b6lxu8` at `c8ef36a`:

* `research/33_one_stabilization_and_the_forced_collapse.md` — §3 only (the
  hyperbolicity of `Σ₂(K_1)` and why it bounds no plumbing).
* `research/34_searchlight_and_the_general_stabilization.md` — §5, §5a (the
  lifted surgery description and the failed `L(13,5)` unwinding).
* `scripts/lifted_surgery_description.py` — construction and identification
  method.
* `results/opus_2026_09_17/lifted_surgery_description.json` — `M̃` 34
  tetrahedra, `H_1 = Z⁴`, 320 `L(13,5)` fillings, 59 `Σ₂(K_1)` fillings.
* `results/opus_2026_09_17/annulus_trace_stabilization.json` — `lk(K,c'_i) = 0`,
  framings 2 and 0, `Q_W = [[2,1],[1,0]]`.
* `scripts/build_marked_product_scaffold.py` — lines 15–50.

On `origin/main` at `f7ba2516304c0553a3180570abb6e257f4a68094`, read with
`git show` without touching the working tree:

* `results/astra_2026_09_17_overnight/pass08_0202_whisker_branch_gate/RESULTS.json`
  — 49 colourings, 36 witness/witness, 24 separated, 12 surviving, and its own
  interpretation that unbased end-circle data do not select the physical branch.

**Not re-audited:** the rest of the repository, including the other seven
overnight passes.

## Mathematical facts used

* **Poincaré–Lefschetz duality** and the long exact sequence of a pair, over `Q`.
  Standard; no citation status claimed beyond textbook.
* **Projection formula / naturality of cup products** for a proper degree-`d`
  map: `⟨p^*x, [M,∂M]⟩ = ⟨x, p_*[M,∂M]⟩`. Standard.
* **Donaldson's diagonalizability theorem** for closed smooth oriented negative
  definite 4-manifolds. Invoked by name only; its hypotheses are listed in
  `README.md` §3 and are **not** met here, because no explicit negative definite
  filling `X_1` of `−Y_1` exists.
* **Atiyah–Singer `G`-signature theorem**, in the double-branched-cover form
  `σ(W_2) = 2σ(W) − ½[F]²`. Used only as an independent cross-check, not as a
  load-bearing step; `SECONDARY, NOT VERIFIED FROM ORIGINAL` in this container.
* **Lens space amphichirality**: `L(p,q) ≅ −L(p,q)` iff `q² ≡ −1 (mod p)`.
  Verified arithmetically here (`5² ≡ 12 ≡ −1 mod 13`) and consistent with
  `research/21` §3.

## Reproduction

```sh
python3 results/opus_2026_09_17_1836_trace_cap_gate/check_trace_cap_gate.py
# exit 0; standard library only, no SnapPy, Regina, sympy or Sage
```
