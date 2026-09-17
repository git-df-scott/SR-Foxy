# Explicit collar-map candidate and a full-group equality

17 September 2026. **CE: NO. No new slice disk or embedded annulus.**

This pass replaces the finite-quotient branch guesses for the exact crossed bands with a fully specified group-map candidate and an exact equality certificate. The new result is algebraic. Matching this map to the intended geometric product-disk boundary parametrization is still required; the choice must NOT be promoted merely because it gives a favorable answer.

## Exact input and what was done

Scientific input: SR-Foxy main `f7ba2516304c0553a3180570abb6e257f4a68094`. The marked 54-crossing scaffold and bands are exactly those in pass08:

```
a40a423e_0_0 : [(15,2),(16,2),(2,2),(41,0)], over/over, zero twist
d0826c36_0_0 : [(13,2),(27,0),(32,2),(52,0)], over/over, zero twist
```

The code reconstructs both bands and evaluates the resulting actual axes; it does not substitute abstract uv/vu words.

In the stored scaffold's rebuilt port labels, the connecting edges are `(0,2)--(27,3)` and `(1,1)--(28,2)`. These are not the pre-rebuild port numbers in the original construction script. Restoring the cut strand separately in each half gives a source diagram and its mirror. The crossing correspondence is recovered as `c -> c+27`, with the explicitly saved odd port rotations. All 108 port-adjacency tests pass.

Remove auxiliary meridians and use the source knot's nine-generator Wirtinger presentation. Associate a Dehn-region word D_f to each of the 29 regions. In our conventions, across an oriented source arc x with regions L and R:

    D_L = x^(-1) D_R, hence x = D_R D_L^(-1).

For the proposed upper-to-lower transition use

    y = D_L^(-1) D_R.

This is the candidate above/below meridian conversion. Fix the base region to the sector between ports 2 and 3 at source crossing 0, recorded as `base_sector=[0,2]`. This completely specifies the algebra; no arbitrary finite coloring remains in its definition.

## Strongest new verified result

The specified region map defines a homomorphism from the doubled boundary-knot presentation to the source presentation. Under it, the two actual band-summed axis words represent the SAME element of the full source group, not just conjugate elements of SL(2,F5).

The source presentation is reduced by six explicit, reversible generator eliminations to generators numbered 5,6,8. The two raw axis-image words have lengths 70 and 48. They reduce to the same 20-letter word:

```
[6,6,6,-5,8,5,-6,-5,6,-5,6,-5,-8,5,-6,5,-6,-8,5,-6]
```

Positive numbers are generators and negative numbers their inverses. A six-step relator-replacement certificate reduces eta1 * eta2^(-1) to the empty word. This is a positive proof by relator applications; it does not rely on assuming a rewriting system is complete.

`certificate.json` stores the source relators, every generator elimination, the explicitly derived additional relators and their proofs, region words, all 18 boundary-arc images, both axis words, and their reduction traces. `check_saved_proof.py` independently replays that certificate without importing the diagram code or searching for word reductions. It also rejects tampering with either axis data, the common word, or a source-generator image.

The full diagram reconstruction and word-map producer, supplied in the accompanying local audit package, passed 370 exact checks. These include the mirror correspondence, region equations, arc consistency, all doubled-knot relations under the map, the axis equality, and a meridian-perturbation negative control. The successful capped run took approximately 0.66 seconds; the independent certificate replay passed separately. These are checks of specified finite data, not 370 new knots.

## The important unclosed geometric step

An explicit homomorphism is NOT automatically the inclusion-induced map of the intended disk exterior. Dehn-region conversion is natural for the above/below presentations, but the actual collar identification between the displayed doubled boundary, the punctured-ball product, and the base paths still has to be matched.

A diagnostic using the other incident seam region gives different finite-group outcomes. It is therefore not legitimate to select this sector solely because it makes the axes equal. In particular, this note does NOT assert that the original pass08 six-branch problem has been geometrically settled, nor that the two sector choices represent the same marked product disk. Such an assertion needs the neck/collar isotopy with base paths tracked.

The precise next certificate is: realize the saved region map as the inclusion map for an explicitly parametrized product disk (or a specified twist-product disk) in the fixed marked boundary, transporting BOTH actual bands. This is now a concrete map to prove or falsify, rather than an unspecified branch choice. If realized, the full-group conjugacy gate passes. An embedded annulus or a framed nonseparating compression disk remains an additional smooth-geometric problem; group equality supplies neither. Surgery coefficients, standardness and the final knot identity remain separate.

## Scope, reproducibility, and failures

On the repository, replay the saved proof with:

    python3 check_saved_proof.py certificate.json

The local complete package additionally contains `diagram_core.py` and `verify_product_collar.py`. In that directory:

    python3 verify_product_collar.py --output FRESH_RESULTS.json
    python3 check_saved_proof.py FRESH_RESULTS.json

Python standard library only. Run one job at a time; the recorded successful producer run had a 15-second subprocess cap and 1 GiB address-space limit. One earlier shell invocation timed out before creating its result; it remains UNKNOWN, not a failed mathematical test. Subsequent completed runs are separately recorded. No Mac or Opus process was used or changed, and no new branch was created.

The diagram primitives were adapted from the user-supplied pass08 archive. Its script is a longer archival version, Git blob `8aeb62801a9880d040d62fcb9d12fec1cf12bee6`, not byte-identical to main's shorter script, blob `90a76705b687561bebadca60750742e0f47a560d`. The scaffold, band descriptors and relevant algorithms were checked against the retrieved main file; the two code versions are not represented as matching hashes. The complete package preserves the exact archival input and generated producer.

Read: current main, `build_marked_product_scaffold.py`, pass08's checker, Spherogram's actual mirror implementation, and the cited primary-source passages. This was not an exhaustive repository audit. No settled Jones, s, HKL, Floer, or broad band search was repeated.

## Primary sources and exact use

- D. S. Silver and S. G. Williams, *Group Presentations for Links in Thickened Surfaces*, arXiv:2005.01576v1 (May 2020), Sections 2-3, Proposition 3.1, and Example 4.6. These support the Dehn/Wirtinger conversion and distinction between above/below presentations. The parsed paper text was read; PDF screenshot attempts failed, so no figure inspection is claimed. https://arxiv.org/pdf/2005.01576
- J. Meier and A. Zupan, *Knots bounding nonisotopic ribbon disks*, Journal of Topology 18(4), e70047 (2025), Section 2.1: product disks `(B3,J^circ) x I` and twist-product disks. This supports the geometric model, NOT our unverified collar matching. https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/topo.70047
- Spherogram, `spherogram_src/links/links_base.py`, `mirror`, inspected blob `ef6d64c2f86b0ac7251aac44614bf8e5b300d4f4`: source port p is converted to p+crossing.sign modulo 4 before rebuilding. This explains why correspondence must be transported, not guessed from equal arc labels. https://github.com/3-manifolds/Spherogram/blob/master/spherogram_src/links/links_base.py
