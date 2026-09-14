# Current handoff — 13 September 2026, evening

**No counterexample found.** Read `research/19_link_concordance_completion_gate.md`, `results/evening_session_validation.json`, and `results/teichner_frontier_validation.json`. Work remains on main. Research note number 18 is reserved by Claude PR #3; no branch was created, removed or merged here.

**Construction priority:** Teichner certificates for D01 # J with J ribbon.
No sum certificate has been found. New partners 9_41 and 9_46 have separately
replayed ribbon certificates. Mixed-attachment and third-band searches save
full paths. Native Sage/Singular Fox-Milnor minors segfaulted; preserve the
logs and use the local conservative replacement, not an environment change.

**Current frontier (supersedes intermediate 350-path count):** A Miyazaki
component gate rejects 74 of 587 initial saved links, or 237 with inherited
prefix exclusions. Later component slice checks reject 803 of 805 remaining
and deeper paths by nonsquare component determinants. All 392 distinct
determinants agree independently with Regina Jones. Two first-stage paths
remain, both under 9_46: `78685a_1_-2`, `00676e_0_-2`. Continuing them across
the selected full shortest-band box tests 24,359 moves and saves **96 unknown
paths**, no ribbon certificate. Start with
`results/teichner_D01_J946_component_filtered_continuation.json` and its
validation; this is the constructive frontier, not the earlier unfiltered list.

**Missing partner orientation:** The second surviving knot component is
matched to the unoriented factors of D01 # mirror(6_1) after seeded
simplification. The signatures allow reversing factor orientations; a full
oriented connected-sum identification is not certified. The first has recognized
K0 and mirror(6_1), with its 19-crossing factor still unknown. The old 4.2-hour
run used 6_1, not its mirror. Both 6_1 and D01 are chiral by Jones, so do not
drop mirrored partners merely by assuming the target is amphichiral.
The 96 latest paths still require tau/Fox-Milnor and ribbon-specific screening;
passing their current determinant filter proves no sliceness.

**Validation:** 587 initial raw moves, 455 third-band moves, and 96 final
continuation moves are separately checked. 84 factor records support the
Miyazaki gate; all factor calculations finish, and Seifert evaluations agree
with HFK Alexander data. A component that cannot be ribbon blocks every
pure-fission ribbon-disk continuation of that prefix. This is not an
obstruction to an arbitrary smooth slice disk for D01.

**Link concordance gate:** All 1,092 normalized matches from research/17
have generic multivariable Alexander H1 rank zero; all are independently
checked using triangulation-derived groups and exact integer minors.
A split knot/unknot pair has rank one and link concordance preserves it.
The connected planar prefix completion lemma is proved in research/19;
it rules out arbitrary annular completions of a fixed prefix, not all
possible endpoint concordances. The proposed independent Claude review
was not confirmed delivered through the app. The 61 older first links
have 32 additional colored-rank exclusions; the two Kh survivors remain.
Never treat a deficient finite specialization as generic rank.

**Other completed checks:** New embedded band cores may return to a face
but cannot cross an original edge twice; face chords must not interleave.
35,930 samples yield 35,521 rank exclusions and 409 unknown retained
links, all replayed. No opposite-source Jones match and no known-source
return in this restricted sample. Preserve that missing positive control.
Rational odd Kh (Migdail–Wehrli 2607.04018v1 Thm 8, preprint) passes
J25533/J25541 and C2/C4. KnotJob returns reduced odd Kh; reconstruct
unreduced by quantum shifts +1 and -1. Do not use arbitrary odd primes
with that theorem. Eight Euler checks and the K1 mirror check pass.

**Coordination:** Scott pasted Claude's report. PR #3 at 579abda was
inspected read-only; its RBG survivor counts are not independently rerun.
Preserve `claude/counterexample-search-ungpe2` and its jobs. The existing
Claude configuration was unchanged. Computer Use inserted a coordination
prompt but did not confirm submission; do not claim a reply was received.

**Budget:** this is the authorized 17:30 MDT session, fresh shared-meter
baseline 38%, target 47%, hard ceiling 48%, stop by 22:30. The local
`work/slice_ribbon_budget.json` outside the repository records final
accounting. Pause the one-session heartbeat when checkpointed. Unused
allowance does not roll over, and the end of a window authorizes no new work.

---

## Historical checkpoints — priorities and schedules below are superseded

# Current handoff — 13 September 2026, extra afternoon session

**No counterexample found.** Read `research/17_fission_ancestry_and_linking.md`
and `results/component_session_validation.json` first. Work remains on `main`.

The key new deduction is component ancestry in a reverse movie with only
fissions, isotopies and split unknot deaths: one intermediate component must
be ribbon-concordant above K1 and every other component must be ribbon.
The proof and exact restrictions are written in research/17. It is NOT a
condition for movies with later fusion saddles or births. Do not demand that
the distinguished component already equal K1 before its last fission.

Applied to the 61 saved intermediates of J25533, determinant/HFK tests retain
15, and full graded F2 Kh retains only two first bands:
`6267660c_0_0` and `2b2a271f_1_0`. All eight relevant component Kh computations
finish (three reused by exact diagram signature), with checked Euler polynomials.
The 59 exclusions apply to every pure-fission completion of those particular
intermediates. A second-saddle search on the two survivors tested 39,176
zero-linking fissions without a K1/U/U component Jones match.

`results/component_guided_K1_to_K0.json` contains 239 retained component
Jones/HFK matches on five K1-built upper knots, all nonsplit by whole-link
Jones. `results/normalized_component_neighborhoods.json` removes the twist
parameter and varies up to two crossing choices: 6,623 normalized bands,
1,092 retained matches, all zero-linking and provably nonsplit. Of these,
156 have explicitly matching K0 and unknot component diagrams. Counts are
diagrams, not isotopy classes. K0-built survivors produced no K1 component match.

A full twist preserves the component knot types of a fission while changing
coherently oriented linking by one. The library may reverse orientations on
rebuilding: the original signed-slope pilot failed. The preserved regression
is in `results/fission_twist_orientation_regression.json`. The correction
tries both signs and directly verifies linking zero. Never silently ignore
the failed pilot, equate polynomial equality with splitness, or treat a
polynomial coefficient score as a geometric distance.

**Next construction:** change band attachments and paths, with explicit split
K0/U as a boundary condition, while tracking the known K1 birth-and-band
presentation. Explore simultaneous moves of the two presentations, not only
more twists on the same core. This proposed construction is not implemented
and is not guaranteed. Continue to screen new common upper knots by HFK/Kh.

The next session is **17:30 MDT today**, replacing 17:50, with a fresh shared
usage baseline, at most ten additional percentage points, a buffer, and a
22:30 stop. No unused allowance rolls over. Read the local budget ledger and
latest user instructions before starting. Claude's audit prompt is saved in
the local outputs directory, but was NOT sent: Computer Use found the Mac
locked. Existing Claude setup and remote branches were left unchanged.

---

## Historical earlier afternoon checkpoint — superseded priorities and schedule

# Handoff — 13 September 2026, afternoon

**No counterexample found.** Start with
`research/16_nonfibered_khovanov_gate.md` and
`results/nonfibered_session_validation.json`.

New computational obstruction: graded unreduced Khovanov homology over F2
excludes 46 of the 48 nonfibered targets in the 60-entry K0 wider pool.
The other 12 entries are fibered, not nonfibered. Only indices **25533 and
25541** survive. Both also pass Q and F3; the full sl3 target calculations
remain inconclusive after 60-second timeouts. All completed Kh Euler
characteristics agree with independently computed Regina Jones polynomials.

The known K0 -> J movies pass their Kh positive controls. K0's F2 Kh ranks
are bounded by K1's in every bigrading, so K1-built genuine ribbon upper
knots automatically pass this particular Kh test for both sources. The
existing K1 threaded archive has 1,111 nonfibered HFK-envelope survivors.
Five 25-crossing candidates were selected in `results/K1_nonfibered_shortlist.json`.

Focused one-fission searches tested 119,242 bands on the two K0 survivors
and 128,369 on those five K1 targets. Known-source diagram controls return;
no opposite-source HFK match was found. A two-fission pilot on 25533 also
returns only K0. These are incomplete geometric searches, not concordance
obstructions. Broad searches were stopped after the Kh filter; their partial
checkpoints and failed pilot are preserved.

The Alexander-rank helper now accounts for wholly overpassing components,
which `_pieces()` omitted. The real missing-generator regression and a
rejected, nonplanar hand-built test fixture are recorded. The latter was
replaced by a planar control. Do not treat failed checks as discarded data.

**Next:** use the combined HFK/Kh gate before searching a target; do not
resume the 46 excluded targets or fibered J149 by default. Develop a
component-guided two-stage search: distinguish wrong component knots from
correct components that remain linked, and preserve those near-matches.
Explore alternative diagrams and longer edge paths before increasing the
same shortest-first caps. Prove every geometric implication before claiming
an annulus in S3 x I or a disk in standard B4.

Session accounting is in the local `work/slice_ribbon_budget.json`, outside
this repository. The separate **17:50 MDT** wakeup remains scheduled with a
fresh shared-usage baseline and a maximum of ten additional percentage
points. Unused first-session allowance does not roll over. The old budgets
and priorities below are historical. Work in this session stays on `main`;
no branch was created or deleted.

---

## Historical morning checkpoint — superseded priorities and budget

# Current handoff — 13 September 2026

**No counterexample found.** Read `research/15_infection_target_compatibility.md`
first: zero-winding infection cannot preserve the fibered target if an infection
torus remains incompressible; adding meridians changes its Alexander polynomial
for nontrivial fibered companions. Keep infection and annulus twisting distinct.
The preceding exact audit is `research/14_marked_annulus_audit.md`. These supersede the priorities in the
historical handoff below. This session's changes remain on `main`; no branch
was created. The final remote check found `claude/pensive-hopper-3rh6p4`
with eight unmerged commits through f15e803, including a terminated J149
search and separate graph-reconstruction work. That concurrent work was
preserved, not merged or deleted. Do not assume the remote has only one branch.

New exact result: the fixed surgery circles have images of trace 1 and 4 in
SL(2,F5), with orders 6 and 3. They cannot cobound even a mapped annulus in
the standard product-disk exterior. Four triangulation seeds, geometric and
simplified relators, peripheral conjugators, and a standalone checker are
saved in `results/annulus_group*` and the corresponding scripts.

The fixed two-handle trace exterior has full group Z: its compact presentation
reduces after killing a generator commutator. Its equivariant intersection
determinant is Delta(t)^2 up to a Laurent unit, by the written duality proof.
It cannot lose a disjoint S2xS2 summand while preserving the annulus and become
a standard-product concordance. This does not obstruct the endpoints from
being concordant by a different annulus. See the n=-1 endpoint control.

**Next constructive task:** specify mixed band sums of the four circles in
`data/knots/AbeTagami_marked_product_scaffold.json`. Seek actual based words
uv and vu, then identify the surgery link/framing and boundary knot before
attempting an embedded standard annulus. This is a proposed construction;
the saved five-component link is only an input scaffold. Nonribbonness must
remain independently certified for any resulting knot.

J149 is downgraded: the Agol–Ren claim after Question 1.15 concerns the genus
of the inputs, so a genus-four target does not escape it. Treat the preprint
claim as a priority warning until its argument is reconstructed, not as a
new certified discard. Do not resume broad J149 searches by default.

Today's allowance: seven additional shared weekly percentage points, baseline
26% at 09:49 Edmonton, ceiling about 33% with a buffer. This is a manual cap
for the authorized session, not seven points automatically every five hours.
The old reminder was updated to a one-time 13:33 MDT wakeup today, authorized
to resume only within the unused morning allowance after checking fresh usage
and the latest user messages. The extra light pass has baseline 28%, ceiling
30% with a buffer, within the morning allowance. No new allowance is granted
by the reminder or by the end of a five-hour window.

## Historical handoff — 12 September (priority recommendations superseded)

**No counterexample found.** Read `RESUMED_2026-09-12.md` and research notes
10–13 before planning more work. The target is D01=K0#(-K1). Its audited
nonribbonness remains applicable; its smooth sliceness in standard B4 is
unproved. The missing object is a smooth concordance K0→K1.

User authorization: push this repository, keep `main` as the sole branch,
and use Opus for critiques. Working clone:
`/Users/scottg/Documents/Codex/2026-09-12/hey/work/SR-Foxy`.
Do not switch to the stale saved checkout or overwrite its user changes.
Python from this clone: `../knot-venv/bin/python`.

The resumed session started at 14% on the shared weekly meter, with at most
13 additional percentage points authorized (cap 27%, planned wrap by 26%).
The user's mistaken 15% message was subsequently corrected with an instruction
to keep working. This is a cap for this resumed session, not authorization for
another automatic session. Automation `resume-slice-ribbon-research-at-4-30`
was PAUSED during the resumed session. Do not schedule another budget or
restart from the earlier 4:30 instructions. Check fresh usage and current
user authorization before any further session.

## Main new results

* New coupled-birth movies: both unknots exist before either fusion. Return
  loops and longer paths now reach an exactly verified nonsplit intermediate
  (K0 double-return first saddle 20). Its Jones value at q=2 mod101 is 29,
  versus 88 for a split product. The endpoint family is still incomplete.
* 32,768 main moves replayed, 2,518 HFK attempts, 2,436 completed, 82 unknown,
  228 common-rank passes. Combined indices have 267 and 1,962 records and no
  diagram/numerical/factor matches. Do not treat these as global knot counts.
* Concrete new target J149: K0 batch1 move 10187, first saddle 319, 26 crossings,
  fibered genus four, rank149, determinant117, torsion order1. It passes both
  sources' rank, quotient-chain-map and retraction filters. ONLY the K0 movie
  exists. Bounded one-fission/death search tried 7,130 bands without a K1 hit.
* Sharper necessary bounds: genus-two common successor rank≥29 and nonfibered;
  fibered common successor genus≥4. See note10 for qualifications.
* All 256 full mixed differentials are basis-conjugate. An independent checker
  verifies all 4,096 involutive local-projection cases. Conditional on the
  stored Floer inputs/lifting, both sources have the figure-eight involutive
  local-equivalence class. Repeating invariants factoring through that class
  cannot distinguish them. Branched-cover and satellite data are not covered.
* The (2,13) linking/character basis gap is resolved. Fox→Dehn→Goeritz gives
  B=[[9,2],[2,2]]; the two isotropic lines (1,3),(1,8) both have the explicit
  norm square in note13. A second shading and a ribbon control agree. This
  specific refinement does not obstruct D01.
* The torsion script's largest-entry shortcut was wrong. Exact Smith form plus
  independent binary ranks now gives K0=K1=J149=KG=KB=1 and GST=2. A finite
  fusion lower bound is not a global nonribbon obstruction.
* Isolated KnotJob results and failures are recorded; do not repeat jobs
  already finished or call timeouts zero. The session report gives the scope.
* Higher-cover HKL manifests preserve exact methods and timeouts. Advanced
  (4,3),(4,13),(8,3),(8,13), and direct (4,3),(8,3), all return no obstruction.

## Most valuable next work

Extend the new two-fission reverse search from J149, or search for a matching
K1 successor using longer/returning band paths. The 180-second reverse pilot
generated 2,207 first and 311,098 second candidates, retained 157 intermediate
diagrams after linking/Alexander filtering, and recovered only K0. See
`results/two_fission_J149.json`; almost all second stages hit their 2,000-band
cap. The Alexander filter has positive and negative controls. Do not require
intermediate vertices to satisfy final-target HFK bounds. The saved K0 movie
is a positive control for reversing both saddles. A local inverse of its last
saddle can be recovered by trying the four strand indices on each of the two
band-end crossings; crossing rotations matter. The new bounded two-fission search recovers K0 through a different saved
control (`0b06_0_0`, `1918_0_-1`), but does not provide a K1 movie or a geometric
certificate.

Every positive endpoint meeting still requires oriented peripheral knot
identification, orientation checks, and a replayable annulus movie. A numerical
isometry signature or algebraic chain map is only a nomination. For KG/GST,
sliceness and global nonribbonness are separate obligations. The explicit
Hom–Park input is already obstructed from sliceness and should not be reopened.

Before new edits, inspect status and fetch/check origin/main. Preserve all
raw archives and hash-referenced source complexes, especially the large
`results/chain_map_filter_wider.json`. No need to redo completed checks unless
inputs or implementation change.
