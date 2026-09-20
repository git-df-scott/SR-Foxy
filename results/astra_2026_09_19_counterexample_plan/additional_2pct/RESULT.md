# Additional allowance: chats, GST bands, and the 11-fold cover

19 September 2026. **No counterexample. New integral GST information obtained.** Shared weekly usage baseline was 4%, with at most two additional percentage points authorized. This is a continuation of the earlier plan, not a restart of a paused remote search.

## Strongest new result

For the literal saved GST48 knot diagram,

**H₁(Σ₁₁(K); Z) = Z/1849 ⊕ Z/1849**, where 1849=43².

The earlier GST package knew only the order 43⁴ and explicitly left the integral decomposition uncomputed. The computation here fills that gap. It does not identify the literal PD with the primary GST figure independently and does not obstruct ribbonness.

Evidence:

1. Recovered the 74×74 Seifert matrix from remote commit `841d445` and regenerated it from the stored PD with Spherogram. The matrices agree exactly.
2. Used G=(Vᵀ−V)⁻¹Vᵀ and R=G¹¹−(G−I)¹¹, an integral presentation of cyclic branched-cover homology. Verified that Vᵀ−V is unimodular. The formula is documented in [KnotInfo: Torsion Numbers](https://knotinfo.org/descriptions/torsion_numbers.html), a primary database-method source accessed 19 September 2026. Its figure-eight examples for covers 2 through 9 all passed the implementation.
3. A modular Smith calculation over Z/43⁵ gives valuations 0 seventy-two times,2,2. The independently computed Alexander resultant supplies the exact order 43⁴, ruling out additional prime factors or higher valuations.
4. Regina's separate **exact integer** Smith algorithm gives diagonal 1 seventy-two times,1849,1849. This agrees with the modular algorithm. The initial SymPy exact Smith attempt was too slow and was terminated; no negative mathematical inference was drawn from that.
5. The induced deck action on H/43H is represented, in the saved quotient basis, by [[39,40],[11,8]] over F₄₃. Its characteristic polynomial is t²−4t+1, irreducible over F₄₃, and its order is 11. The calculation checks that the quotient map intertwines G and its induced 2×2 action before forming the deck action. Reversing the deck generator preserves this reciprocal polynomial.

Files: `GST_COVER11_PADIC.json`, `GST_COVER11_REGINA_CHECK.json`, `GST_COVER11_DECK.json`; producers/checkers `gst_cover11_padic.py`, `verify_cover11_regina.py`, `gst_cover11_deck.py`. Dependencies and runtime are in the parent directory. Algorithms are exact but software-trusted; this is not formal proof-assistant verification.

## A useful algebraic consequence, with proof

Put H=(Z/43²)². There is **exactly one deck-invariant subgroup of order 43²**, namely M=43H. Consequently it is the only possible deck-invariant metabolizer for the nonsingular linking pairing on this cover.

Every abelian group of order 43² is either cyclic or killed by 43. In the latter case a subgroup of H lies in H[43]=43H, and equal cardinalities force equality. If a subgroup of order 43² is cyclic, its image in H/43H is a nonzero one-dimensional subspace. Deck invariance of the subgroup would make that line invariant. The computed irreducibility of t²−4t+1 forbids such a line. Thus only 43H remains.

It is isotropic for **any** linking pairing on H: bilinearity gives λ(43x,43y)=43²λ(x,y)=0 because H has exponent 43². Its order is the square root of |H|, so nonsingularity makes it self-annihilating. This is an algebraic statement about the boundary homology and action; it does not construct an embedded disk or classify ribbon disks.

This improves the plan: do not spend the next session enumerating multiple deck-invariant metabolizers in this cover. There is only one. The unresolved work concerns the **integral Alexander module/peripheral realization and actual disk exterior**, or a different genuinely ribbon-specific obstruction. Unusual 43-torsion is not itself a ribbon obstruction. The two rational Alexander-module metabolizers from the earlier report should not be confused with multiple possible invariant subgroups of this finite cover.

## What the extra chat review changed

Read the older pages of **Slice Knot Identification**, the recent construction proposals in **Slice Ribbon Prompt Request**, and the latest update in **Find Counterexample in SR Foxy**. Relevant responses and pagination coverage are preserved in `RESEARCH_CHAT_EXCERPTS.json`. The similarly named **Choose Counterexample Strategy** concerned other conjectures and supplied no SR-Foxy construction; it was not adopted as an instruction for this task.

The history reinforces two different routes:

- **Constructive knot route:** produce a smooth concordance between the exactly checked nonisotopic fibered pair, or a disk for D01 after a justified slice stabilization. The missing object is an actual embedded surface with controlled boundary, not a new invariant match. The marked mixed-transfer and mutation-tangle proposals are construction targets, not completed movies. For mutation, an explicit relative concordance to a symmetric tangle would be a mechanism, but no qualifying pair/movie was recovered.
- **GST route:** finish the actual link diagram and in-family Eisermann controls; then test L₃,₁. A successful link obstruction still needs a separate argument to yield a knot counterexample. Existing small-link census results exclude the tested Eisermann-violating candidates after sliceness screens; they do not prove that every small slice link is ribbon.

The latest GPT archive report says 4,602 additional nodes were recovered beyond the intact 21,067-node checkpoint, totaling 25,669 readable nodes. Those claims do not extend the first-hour endpoint exclusion automatically. Its full new ZIP was not present in the inspected Downloads set; the locally available search-evidence ZIP has 55 files and the earlier audit. The reported 192-dart GST bridge and original edge-preserving producer were not recovered here. Preserve those as retrieval gaps, not claims to have replayed them.

## Testing the parallel-edge idea on GST

Inspected installed Spherogram 2.4.1 `simple_bands`: it takes the first dual edge between each face pair. A prototype retains the specified attaching edges and enumerates internal dual-edge choices while retaining the original augmented-simple-face-path and band-minimality restrictions.

For the literal GST48 diagram, its generated descriptor sets exactly match the original sets in BOTH audited boxes:

| Maximum length / twists | Original distinct descriptors | Prototype distinct descriptors | Extra |
|---|---:|---:|---:|
| 3 / 1 | 1,698 | 1,698 | 0 |
| 4 / 2 | 15,794 | 15,794 | 0 |

This is a scoped negative experiment: that implementation change supplies no additional GST descriptors in these boxes. It is not an exhaustive geometric band classification or a denial of the D01 omission.

The stronger D01 regression exposed a limitation of the prototype: its fixed attachment ordering generated 8,370 descriptors versus the original 7,228, but omitted 74 original literal descriptors and added 1,216. This failure is saved in `D01_EDGE_CONTROL_INITIAL_FAILED.json`; **the prototype is not a validated drop-in replacement**. The four simpler control knots did not exercise this defect. Recovering the original chat's corrected producer, or explicitly handling both band directions while keeping every original descriptor, is required before using it for a production D01 search. Raw descriptor differences need not be new band isotopy classes.

## Immediate continuation

The concrete next GST experiment remains the certified L₁,₁/L₂,₁/L₃,₁ diagram-and-Eisermann sequence. The finite-cover subtask proposed in the earlier plan is now substantially completed, with a unique invariant metabolizer established. For a knot counterexample directly, the strongest construction target remains a complete smooth annulus/disk for the certified nonribbon difference knot. No recovered chat contains that missing surface or a global GST nonribbon proof.

New artifacts are local and additive. No remote search was restarted and no new external message was sent. The 4 PM continuation remains scheduled.
