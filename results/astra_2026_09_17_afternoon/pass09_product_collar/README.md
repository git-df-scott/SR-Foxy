# Explicit collar-map candidate: a full-group equality

17 September 2026. **CE: NO. No new disk or embedded annulus.**

Input main: `f7ba2516304c0553a3180570abb6e257f4a68094`. Work concerns the actual crossed bands `a40a423e_0_0` and `d0826c36_0_0` from pass08, not abstract uv/vu words.

## New result

An explicit Dehn-region candidate for the missing above/below collar map is now specified. Under this map, the actual two band-summed axes are EQUAL in the full source knot-group presentation, not merely conjugate in SL(2,F5).

The map uses the base region at source sector `(0,2)` (between ports 2 and 3). Source meridians and region words obey `D_L=x^(-1) D_R`; the proposed lower meridian is `y=D_L^(-1) D_R`. The scaffold's rebuilt connecting edges are `(0,2)--(27,3)` and `(1,1)--(28,2)`. The source-to-mirror crossing correspondence and odd port rotations are saved, and all 108 port-adjacency checks pass.

The source's nine Wirtinger generators reduce by six explicit generator eliminations to generators 5,6,8. The actual axis image words, of lengths 70 and 48, reduce to the same 20-letter word. A six-step relator-replacement certificate reduces their difference to the empty word. This is a finite positive proof, not a claim that a word-rewriting procedure is complete.

The full diagram/word-map producer passed 370 exact checks, including region equations, arc consistency, all doubled-knot relations under the map and the axis equality. The successful bounded run took approximately 0.66 seconds, with a 15-second subprocess cap and 1 GiB address-space limit. An earlier shell invocation timed out before producing a result and remains UNKNOWN.

## Essential limitation — do not suppress it

The map is algebraically certified but has NOT been geometrically identified with the intended product-disk boundary parametrization. The opposite incident seam region produces different finite-group outcomes. Selecting the favorable sector alone is not a geometric proof, and this checkpoint does NOT announce that pass08's physical branch choice has been resolved.

The next task is to realize this exact saved map by an explicitly parametrized product collar (or specified twist-product collar), carrying the four original marked circles AND the two actual bands. If that identification succeeds, the full-group conjugacy gate passes. A framed nonseparating compression disk or a separately embedded annulus is still missing, as are the surgery, standardness and final-knot certificates. Equality of group elements does not supply any of these objects.

## Reproduce the published certificate

    python3 check_saved_proof.py certificate.json

The standalone checker verifies the generator eliminations and additional relator derivations, then replays both axis reductions and their difference without the diagram code or the producer's word-search algorithm. It rejects three deliberate mutations. `certificate.json` also records all source relators, region words, 18 boundary-arc images and proof traces.

This repository checkpoint publishes the algebra certificate and independent replay checker. The complete diagram producer, exact archival dependency, execution record and detailed report were saved separately in the accompanying user-download package `SR_Foxy_pass09_product_collar_2026_09_17.zip`; those additional files are not represented as present in this commit.

No Mac/Opus process, settled invariant calculation, existing research file, or branch was changed by the computation. Only selected source files were read, not the entire repository. The diagram primitives came from the supplied pass08 archive (longer script blob `8aeb62801a9880d040d62fcb9d12fec1cf12bee6`); its geometric inputs and relevant algorithms were checked against main's shorter checker (blob `90a76705b687561bebadca60750742e0f47a560d`). These distinct source files are not claimed byte-identical.

## Sources and scope

- Silver and Williams, *Group Presentations for Links in Thickened Surfaces*, arXiv:2005.01576v1, Sections 2-3, Proposition 3.1 and Example 4.6: Dehn/Wirtinger conversion and above/below presentations. Parsed text read; PDF screenshot attempts failed, so no figure inspection is claimed. https://arxiv.org/pdf/2005.01576
- Meier and Zupan, *Knots bounding nonisotopic ribbon disks*, Journal of Topology 18(4), e70047 (2025), Section 2.1: product and twist-product disk models. This does NOT certify our collar match. https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/topo.70047
- Spherogram `links_base.py`, `mirror`, inspected blob `ef6d64c2f86b0ac7251aac44614bf8e5b300d4f4`: the source port is shifted by the source crossing sign before rebuilding. https://github.com/3-manifolds/Spherogram/blob/master/spherogram_src/links/links_base.py
