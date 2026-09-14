# Slice–Ribbon counterexample research

**No counterexample found.** Start with the [evening construction and obstruction audit](research/19_link_concordance_completion_gate.md) and [current handoff](HANDOFF.md).

The direct construction target is a verified ribbon certificate for **D01 # J**, with a separately verified ribbon partner J. That proves D01 slice; its existing nonribbonness argument would then give a counterexample. New partners 9_41 and 9_46 were tested with full saved move sequences. Component obstructions reduce the intermediate searches to two paths; one matches the unoriented factors of **D01 # mirror(6_1)**, exposing a missing partner orientation in the old search. Their bounded continuation saves **96 unknown paths**, with no ribbon certificate. See the audit for exact coverage and failures.

All 1,092 earlier component matches have independently checked Alexander-module rank zero, obstructing link concordance to a split knot/unknot pair. The new completion lemma explains why this prevents annular completion of a fixed connected planar prefix. A separate audit excludes 32 of 61 older first-stage links by this test. It does not obstruct every possible concordance of K0 and K1.

The graded even Khovanov test still excludes 46 of 48 nonfibered K0 upper targets. J25533 and J25541 survive even and newly applied rational odd Kh tests. Eight odd Kh inputs pass independent Jones/Euler checks; a mirror control passes. Bounded face-return band searches found no opposite-source match.

The stored Abe–Tagami difference has a nonribbonness argument; its smooth sliceness remains unknown. The [marked-annulus audit](research/14_marked_annulus_audit.md) and [infection compatibility audit](research/15_infection_target_compatibility.md) record obstructions to specific earlier constructions. They are not global sliceness obstructions. The explicit Hom–Park member is already obstructed from sliceness.

See [reproduction instructions](REPRODUCE_2026-09-12.md), [exact Floer-filter diagram](figures/common-successor-filter.png), and [an actual search move](figures/fusion-example.png). All development stays on `main`.

New: [minimum-genus target bounds](research/10_low_genus_targets.md), [involutive algebra audit](research/11_involutive_local_equivalence.md), [coupled movies and corrected torsion](research/12_coupled_movie_audit.md), and [explicit linking/character audit](research/13_fox_goeritz_hkl.md).
