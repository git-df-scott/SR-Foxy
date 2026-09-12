# Current handoff — resumed work completed 12 September 2026

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
