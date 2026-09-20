# Checkpoint4 — new coloured-Jones lead and source-band test

2026-09-20 UTC. No counterexample. Shared weekly usage12% at start,13% at milestone. Total allowance14 points from baseline7; stop at20%, deadline04:41:43UTC unchanged. Remote2a07128 and local3e4461e unchanged; concurrent changes preserved. No remote searches restarted.

## Completed new calculation: Suzuki first reduced colour

Primary source: Sakie Suzuki, *On the universal sl2 invariant of ribbon bottom tangles*, Algebraic & Geometric Topology10(2010),1027–1061, DOI10.2140/agt.2010.10.1027, https://msp.org/agt/2010/10-2/agt-v10-n2-p18-p.pdf. Theorem1.5 imposes an ideal-membership condition on Habiro-reduced coloured Jones invariants of zero-framed ribbon links. Theorem1.4 is the weaker algebraically split baseline. This supplies a concrete next obstruction beyond the already-tested Jones nullity and modulo32 conditions. A targeted search found no earlier Suzuki implementation in checked local research/scripts; this is not a claim that no historical chat ever mentioned it.

Our calculation uses v for the repository Jones variable and q=v^2 for Suzuki's variable. Put delta=v+v^-1. The reduced colour P'_1=v(V2-delta)/(q-1). Quantum traces are multilinear, so for an n-component zero-linking link:

J(L;P'_1,...,P'_1) = [v/(q-1)]^n sum_{S subset components} (-delta)^(n-|S|) J(L_S),

where J(empty)=1 and J(nonempty sublink)=delta times its normalized Jones polynomial. Pairwise linking zero removes the mixed-writhe framing discrepancy; changing mirror convention preserves the divisibility ideals. Components deleted by the trivial representation disappear. The saved code explicitly tracks the number of components when simplification removes crossing-free unknots.

For all colours1, Habiro's required factor is H=(q^3-1)(q^2-1)/(q-1), and Suzuki's is H*(q-1)^(n-1), since I1=(q-1). We check exact Laurent integrality in Z[q,q^-1], including integer coefficients and even v-exponents, not just numerical values.

| input | Habiro baseline | Suzuki ribbon condition |
|---|---|---|
| ribbon control L10n36 | pass | pass |
| Whitehead L5a1 | pass | fails |
| Borromean L6a4 | pass | fails |
| provisional GST n1,k1 | pass | pass |
| provisional GST n2,k1 | pass | pass |
| provisional GST n3,k1 | pass | pass |

Code `suzuki_first_colour.py`; exact sublink polynomials, factorizations and outputs `SUZUKI_FIRST_COLOUR.json`. GST inputs reuse the independently verified full polynomials from checkpoint2. These passes establish only absence of this obstruction. The Borromean result agrees with Suzuki's explicit example, and the ribbon control passes. An initial implementation exception occurred because crossing-free sublink bookkeeping returned zero unlinked components; saved in `suzuki_first_colour_initial_failure.log`. The corrected implementation uses the known subset size, and all baseline/control assertions pass.

**Next new algebraic experiment:** derive and independently calibrate the mixed reduced colours (P'_2,P'_1). P'_2 = v^2/[(q-1)(q^2-1)] * (V2-(v+v^-1))*(V2-(v^3+v^-3)). Expand by multilinearity: this needs an exact zero-framed two-parallel of only one component, plus ordinary link/sublink polynomials. The V2^2 term denotes that cable, not a connected sum. Framing correction and disconnected components must be verified on unlink, split knots and known ribbon controls. Apply first to the smallest source n1 before expensive n3. Use bounded computations and preserve inconclusive failures. For a knot alone Theorem1.5 supplies no extra I-factor; to infer knot nonribbonness from a satellite-link failure, first prove that the chosen pattern preserves ribbonness. Do not treat a GST link obstruction as a knot obstruction.

## Completed source-side band screen

`probe_preblow_fusion_one_edge.py` enumerates182 bands joining the two black components of the n3,k1 pre-surgery diagram, with exactly one crossed diagram edge, both over/under choices, and twists-2..2 subject to orientability. All182 constructed successfully. Red components are tracked by original crossing-label occurrence multisets, ignoring added labels. Their +1,-1 surgeries then give the candidate knot exteriors.

No numerical volume match to the stored Figure2 target occurred; closest difference0.494507128965285. This is a numerical screen, not interval-certified exclusion. `preblow_fusion_one_edge/INPUT.json`, `ROWS.jsonl`, `RESULT.json` preserve all exact descriptors and PDs. Together with checkpoint3 this covers27 same-face and182 one-edge cases, not all bands. Do not expand blindly: the preferred next geometric step is transport of the literal red dotted arc in source Figure1 through the published isotopies/blow-downs. Its endpoint placement in the n-strand spiral matters; this was exactly where the old L11 transcription failed.

## Virtual-cover literature audit: specific limitation found

Micah Chrisman and Aaron Kaestner, *Virtual Covers of Links II*, arXiv:1512.02667v2 (2016-08-28), https://arxiv.org/abs/1512.02667, PDF https://arxiv.org/pdf/1512.02667. Section3 explicitly returns to the GST square-knot links: their second component lies as a simple closed curve on a fiber, producing the trivial associated virtual knot. Thus that virtual-knot obstruction does not detect these examples. The paper asks for ribbon presentations using a fixed displayed square-knot disk, or an obstruction to those particular presentations. Such an obstruction would not rule out all ribbon disks. Do not repackage pure-ribbon, complement-restricted, semi-fibered, or fixed-disk obstructions as global nonribbonness.

Eisermann Proposition6.13 was rechecked directly at https://pnp.mathematik.uni-stuttgart.de/igt/eiserm/publications/ribbonlinks.pdf: ribbon patterns preserve ribbonness of a ribbon companion. This keeps the satellite transfer route viable, but supplies no failing invariant here. New targeted searches for a general modulo16/Sato–Levine explanation located no checked theorem settling our empirical relation; it remains conjectural.

## Priority for the next paced session

1. Implement and calibrate Suzuki mixed reduced colours (2,1), with exact zero-framed single-component cabling and modest resource bounds.
2. Alternatively recover the literal GST dotted band through source diagrams; the short source-band box has now been screened.
3. Retain all unresolved global proof obligations: source identity, standard-B4 disks for the actual identified object, and independent global nonribbonness. No finite negative box closes a lane.

No long computation remains running. Pause automation only at the campaign deadline, displayed20%, monitoring failure, or explicit user instruction. This checkpoint does not renew the allowance.
