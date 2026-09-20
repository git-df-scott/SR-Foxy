# Checkpoint5 — mixed reduced colours and a bounded Taylor test

2026-09-20 01:29UTC. **No counterexample.** Campaign active; weekly usage13% at start,14% at finish. Baseline7%, total14 additional points, buffered stop20%, deadline04:41:43UTC unchanged. Local3e4461e and remote2a07128 unchanged; concurrent files untouched. All local batch jobs completed; no remote jobs started.

Question: do the precisely encoded provisional GST links violate Suzuki's necessary ribbon-link condition in mixed reduced colours(2,1)? This can establish nonribbonness of a link if it fails. A knot conclusion additionally needs a valid ribbon-preserving transfer, and a Slice–Ribbon counterexample needs the standard-B4 slice construction for the same identified object. Source transcription remains qualified.

## Exact selective cabling and framing controls

`selective_cable.py` takes a braid closure and doubles one cycle of its permutation. At a crossing of bundles of sizes p and q it inserts the p*q braid crossings, preserving strand tracking. At one strand of the selected component it inserts -2w half twists, where w is that component's **actual braid self-writhe**. Using a separate non-braid input diagram's writhe would not be justified. The resulting three-component link has linking matrix zero for every tested algebraically split input.

Controls include the unlink, trefoil, and split trefoil–unknot with either component doubled. Expected component knot diagrams and zero framing are recovered. For3_1,4_1,6_1, the knot-only construction exactly agrees with the repository's separate cable_braid implementation when supplied the actual braid writhe. Deliberately adding a full twist produces nonzero mutual linking in all three cases. See `SELECTIVE_CABLE_CONTROLS.json`, `SELECTIVE_CABLE_FRAMING_AUDIT.json` and their scripts. Implementation agreement is a control, not an independent proof of the entire source-to-braid conversion.

The first mixed calculation stopped on a component marker mismatch because braid crossings have labels x0,x1,... rather than integer labels. It was fixed by normalizing crossing labels. This failure is saved in `suzuki_mixed_label_failure.log`. Cycle/component correspondence is checked through crossing-visit multisets; ambiguous markers are accepted only when there are no self crossings, so the subtracted individual components are both unknots. The doubled cycle itself remains specified by strand tracking.

## Derived mixed-colour formula

Use v for the repository variable, q=v^2 for Suzuki, delta=v+v^-1 and epsilon=v^3+v^-3. Put a=delta+epsilon, b=delta*epsilon. For L=A union B, let J be the unreduced, zero-framed quantum trace, and use AA to mean two zero-framed parallels of A. Then

J(L;P'_2,P'_1) = v^3/[(q-1)^2(q^2-1)] * N,

N = J(AAB) - delta J(AA) - a J(AB) + a delta J(A) + b J(B) - b delta.

This follows by multiplying the representation-ring polynomials P'_2=v^2(V2-delta)(V2-epsilon)/[(q-1)(q^2-1)] and P'_1=v(V2-delta)/(q-1). Cabling realizes V2 squared; it is not a connected sum. The empty-link trace is1. All ordinary Jones inputs are converted to unreduced traces, with crossing-free components tracked separately.

Habiro's baseline factor is H2=(q^5-1)(q^4-1)(q^3-1)/(q-1). Suzuki requires the additional I1=(q-1). The exact test checks membership of J/H2 and J/[H2(q-1)] in Z[q,q^-1], including coefficients and exponent parity, using full Regina polynomials. This is a different colour test, not a monotonically stronger replacement for the previous colour.

## Results and controls

`SUZUKI_MIXED_SUMMARY.json` and per-case `suzuki_mixed/*/RESULT.json` contain results; INPUT.json records braids, selected cycle, framings, and PDs; POLYNOMIALS.json records exact sublink/cable polynomials.

| input | doubled choices | Habiro baseline | ribbon condition |
|---|---|---|---|
| unlink | one | passes | passes, invariant0 |
| split trefoil–unknot | both | passes | passes, invariant0 |
| ribbonL10n36 | both | passes | passes |
| WhiteheadL5a1 | both | passes | passes, invariant0 |
| L10n57 | cycle0 | passes | passes |
| L10n57 | cycle1 | passes | **fails** |
| L14n38935 | both | passes | **fails** |
| provisionalGSTn1,k1 | both | passes | passes |
| provisionalGSTn2,k1 | both | passes | passes |
| provisionalGSTn3,k1 | both | full calculation timed out | unresolved |

The nonribbon controls are not newly discovered Slice–Ribbon examples; their classical nonsliceness was already known/tested. Whitehead passing here shows why testing one colour does not subsume all others. Every completed Habiro baseline passes, and the known ribbon control passes. Full n3 computations were bounded at45seconds each and saved partial results; no timeout is a mathematical negative.

## Less expensive n3 calculation

A necessary local consequence of the mixed-colour condition is that N vanishes to order at least6 at v=1: its prefactor denominator has order3, H2 order2, and the extra I1 order1. Thus the coefficient of (v-1)^5 supplies a potential obstruction after lower orders vanish.

`suzuki_taylor_jet.py` computes unreduced Jones in F101[x]/(x^6), v=1+x, using deterministic Morse layout selection and a20000-state cap. `check_suzuki_taylor.py` combines the result with the saved exact A,B,AB,AA polynomials. On L10n57 cycle1 the numerator coefficients are [0,0,0,0,0,99], detecting failure. On GSTn1 cycle0 they are allzero. Both truncated cable calculations agree with their independently computed full Regina polynomials.

For provisionalGSTn3 cycle1, the recovered124-crossing cable calculation took about12seconds, Morse width20, maximum16784 states. N's six coefficients are allzero modulo101: **no obstruction modulo101**, not exact divisibility. Cycle0 exceeded20000states and remains unresolved. Saved exact input PDs, logs and status files distinguish these cases. An initial missing AA record on an unknotted component was fixed by inserting its known two-component unlink trace delta squared; the missing-key exception was an implementation issue, not evidence.

## Next valuable work

1. Avoid repeating full n3 mixed-polynomial timeouts. For cycle0, improve the Morse ordering of the saved cable or derive a narrow tangle decomposition; retain bounded states/runtime. A zero modular Taylor coefficient cannot be promoted to exact ideal membership.
2. Consider colours(2,2), with a single new double-of-both-components trace J(AABB), reusing all smaller traces. Here I2=(q-1)^2 because its generators include(q-1)^2 and(q-1)(q^2-1). The polynomial test needs H2(q-1)^2; first calibrate on known ribbon and positive obstruction controls and estimate contraction width. Before expensive expansion, investigate whether its low-order part is already forced by classical sliceness constraints.
3. The geometric alternative remains literal GST dotted-band transport through source isotopies. The screened27 same-face and182 one-edge bands did not match numerically, and are not all bands. No global nonribbon proof has appeared.

Primary source rechecked September19MDT/September20UTC2026: Sakie Suzuki, *On the universal sl2 invariant of ribbon bottom tangles*, Algebraic & Geometric Topology10(2010),1027–1061, Theorems1.4–1.5; DOI10.2140/agt.2010.10.1027; https://msp.org/agt/2010/10-2/agt-v10-n2-p18-p.pdf. Original source PDF and hash were saved at checkpoint4. The formulas and bounded calculations above are our derivations/computations. Do not treat the paper's conjectural extension to slice tangles as a proved theorem.
