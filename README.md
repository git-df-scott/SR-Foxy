# Slice–Ribbon counterexample research

**No counterexample found.** Start with the [current handoff](HANDOFF.md), which as of 14 September 2026 covers the whole board: every branch is folded into `main` and there are no unmerged branches. Then the [evening construction and obstruction audit](research/19_link_concordance_completion_gate.md).

Strategy, if you want the shape of the problem before the computations: [why every route-B construction is circular and where the Teichner lane runs out](research/24_why_route_b_is_circular.md), and [why route B can only succeed by refuting a stronger conjecture](research/22_where_a_counterexample_can_come_from.md).

The direct construction target is a verified ribbon certificate for **D01 # J**, with a separately verified ribbon partner J. That proves D01 slice; its existing nonribbonness argument would then give a counterexample. New partners 9_41 and 9_46 were tested with full saved move sequences. Component obstructions reduce the intermediate searches to two paths; one matches the unoriented factors of **D01 # mirror(6_1)**, exposing a missing partner orientation in the old search. Their bounded continuation saves **96 unknown paths**, with no ribbon certificate. See the audit for exact coverage and failures.

All 1,092 earlier component matches have independently checked Alexander-module rank zero, obstructing link concordance to a split knot/unknot pair. The new completion lemma explains why this prevents annular completion of a fixed connected planar prefix. A separate audit excludes 32 of 61 older first-stage links by this test. It does not obstruct every possible concordance of K0 and K1.

The graded even Khovanov test still excludes 46 of 48 nonfibered K0 upper targets. J25533 and J25541 survive even and newly applied rational odd Kh tests. Eight odd Kh inputs pass independent Jones/Euler checks; a mirror control passes. Bounded face-return band searches found no opposite-source match.

The stored Abe–Tagami difference has a nonribbonness argument; its smooth sliceness remains unknown. The [marked-annulus audit](research/14_marked_annulus_audit.md) and [infection compatibility audit](research/15_infection_target_compatibility.md) record obstructions to specific earlier constructions. They are not global sliceness obstructions. The explicit Hom–Park member is already obstructed from sliceness.

Branched double covers now separate the Abe-Tagami family: Sigma_2(K_0) = L(13,5) while Sigma_2(K_1) has non-cyclic pi_1. This is the first invariant here that tells K_0 and K_1 apart, and it is **not** a concordance obstruction. It does open a finite falsifiable [d-invariant gate](research/21_branched_double_covers.md), whose other half needs Heegaard Floer for a closed hyperbolic QHS^3 -- no tool in the recorded environment does this.

The Teichner lane is the only constructive one, and its cost roughly doubles per two crossings of the sum: 4.21 h at 31, 7.96 h at 33, over 12 h at 35. `D_{0,1} # 6_1` and `# 8_8` are complete with no certificate. `D_{0,1}` will not shrink below 25 crossings, so 31 is the hard floor. The lane runs out of tractable partners within a handful of runs.

The unmined r = 0 RBG pair K(0,0,0,-1,2,1) has now been searched to two bands at length 5: 333 and 304 survivors, no unknot. Its frontier **grows** with band count, unlike K_DG, which is why the lane has real input.

A published claim was **retracted**: `Link.simplify('global')` deletes split unknot components, which inverted a screen whose intended pass is "split knot plus unknot". Nothing is eliminated; see [the audit](research/23_prefix_annulus_lemma_audit.md).

See [reproduction instructions](REPRODUCE_2026-09-12.md), [exact Floer-filter diagram](figures/common-successor-filter.png), and [an actual search move](figures/fusion-example.png). All development stays on `main`.

`graph-reconstruction/` is a self-contained side project on the Kelly-Ulam conjecture, unrelated to slice-ribbon. No counterexample there either.

New: [minimum-genus target bounds](research/10_low_genus_targets.md), [involutive algebra audit](research/11_involutive_local_equivalence.md), [coupled movies and corrected torsion](research/12_coupled_movie_audit.md), and [explicit linking/character audit](research/13_fox_goeritz_hkl.md).
