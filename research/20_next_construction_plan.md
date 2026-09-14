# Construction plan after the Opus audit

14 September 2026 UTC / late 13 September MDT. **No counterexample found.**
Scott requested planning, no interruption of Opus, and no overnight Codex
session. There is no evidence supporting his conditional >60% confidence
threshold for extra overnight work. Stop after this checkpoint; resume only
when authorized. No Claude prompt was sent and no cloud job was changed.

## Exact success criterion

Find a knot smoothly slice in standard B^4 and prove it is not ribbon.
The primary target remains D01 = K0 # (-K1). The repository's Abe–Tagami /
Miyazaki nonribbonness audit supplies the second half, subject to the recorded
knot-identification and hypothesis checks. The missing half is a slice disk.
The actionable Teichner route is to supply ribbon certificates for both J
and D01 # J. Merely increasing the number of surviving intermediate links
does not satisfy either certificate requirement.

## What this pass actually checked

Opus PR #3 was read at pinned commit
`345f73ef5aebd1e9c833f177217f2c1b72f08120`; it was not merged. Its 71-path
K_G result is archived verbatim in
`results/opus_snapshots/KG_frontier_345f73e.json`. Each entry stores the
five-item sequence [PD, band, PD, band, PD], rather than a single triple.
This pass checked endpoint components; it did not independently replay all
142 band transitions and intervening diagram identifications.

The component screen gives:

| Input | Paths | Newly excluded | Unresolved |
|---|---:|---:|---:|
| Our D01 # 9_46 continuation | 96 | 1 | 95 |
| Opus K_G two-band frontier | 71 | 1 | 70 |

Indices are zero-based. D01 path 49 contains a knot whose Alexander
polynomial has an irreducible self-reciprocal degree-six factor with odd
multiplicity, violating Fox–Milnor. K_G path 2 contains a knot with computed
tau = -1, incompatible with sliceness. Both exclusions concern continuation
of these fixed pure-fission prefixes; neither excludes the original target.

Checks: 156 distinct component diagram signatures were examined. Determinants
were compared using Seifert matrices and Regina Jones polynomials. For the
two exclusions, the entire Alexander polynomial was independently verified:
for a Seifert matrix of size N, det(tV-V^T) and the shifted HFK Euler polynomial
agreed at N+1 distinct integers, proving polynomial equality by their degree
bounds. Mirror HFK reverses tau and both gradings for the K_G exclusion; this
is a consistency check using the same HFK library, not an independent tau
implementation. Results are computational evidence, not a formally verified
topological proof.

One HFK computation failed its Euler consistency check. It occurs in D01
path 73. A retry again returned an invalid knot Euler polynomial; its values
at 1 and -1 were 2 and 3042 rather than a unit and absolute determinant 1521.
That path remains UNKNOWN, including its reported tau. The failed output is
preserved in `results/september14_HFK_inconsistency.json`.

Among the 95 unresolved D01 endpoints, 12 are single-component knots,
28 have two components, and 55 have three. Eighty-two paths have exactly one
component not simplified to an unknot. All 70 unresolved K_G endpoints have
one such component and two unknot components. **Those unknot components have
not been shown split.** Component simplicity does not establish a link disk.

## Corrections to carry forward

1. Opus's retracted unknot-deletion error is real. His corrected 32 rank-zero /
   29 passing first-stage counts agree with ours. Our independent group
   checker restores detached unknots explicitly before forming an exterior.
   Our earlier copy-bookkeeping regression remains relevant.
2. The rank-invariance source is already in research/19: Tim Cochran and
   Shelly Harvey, *Homology and derived series of groups*, Geometry & Topology
   9 (2005), 2159–2191, published 22 November 2005, Corollary 3.3 and the
   following paragraph on pp. 2169–2170.
   https://math.rice.edu/~shelly/publications/Stallings.pdf
   Checked again 14 September 2026 UTC. It explicitly supports concordance
   invariance of Alexander-module rank. The geometric completion lemma still
   requires an actual connected annulus and a fixed connected prefix.
3. Opus's proposed Whitehead terminology correction is itself unsupported.
   For SnapPy's `Manifold('L5a1')`, the meridians abelianize as ab and ab^2.
   The reported polynomial factors as (ab-1)(ab^2-1). With x=ab, y=ab^2 it is
   (x-1)(y-1), and satisfies the expected Torres specialization. Setting b=1
   in the original basis was not setting a component meridian variable to 1.
   The change of basis is unimodular and checked exactly. Rank conclusions
   are unchanged. Official API documentation calls the output the
   multivariable Alexander polynomial; local source uses a free abelian basis.
   https://snappy.computop.org/manifold.html#snappy.Manifold.alexander_polynomial
4. The Teichner start record is not a resumable checkpoint. At the pinned
   commit, before the long call it saves a partner verification Boolean but
   not that partner's actual certificate, the exact sum PD, or an unfinished
   frontier. Those arrive only after the call returns. K_G writes after each
   completed diagram. Both improve recovery, but do not recover work inside
   an interrupted diagram. Do not interrupt running jobs to fix this.

## Tomorrow's experiment, in priority order

**First: use anything Opus actually finishes.** If a sum certificate appears,
replay both required ribbon certificates and check every transition, including
ambient orientation, meridians, and capped components. The library's generic
`are_same_link` explicitly allows mirror equivalence; that alone cannot
justify gluing oriented intermediate movies. A positive needs actual
orientation-compatible identifications. If only frontiers appear, archive
them and apply the existing component gates before allocating continuation
time. Do not duplicate the 8_8, 10_3, or 10_22 searches already running.

**Second: exploit the specific mirror-partner lead.** Our 9_46 first band
`00676e_0_-2` has a knot component with recognized unoriented factors
K0, mirror(K1), and mirror(6_1). The previous long 6_1 search does not cover
this partner automatically. Verify the oriented factor identification and
the whole endpoint link. If the extra unknot is split, replay its cap; if it
is not, retain its placement and seek a band that separates it. In parallel
within a future authorized local compute box, search D01 # mirror(6_1)
directly, after replaying the reflected partner certificate. Prioritize bands
interacting with the K0/K1 factors. The working hypothesis is that the
stabilizing partner permits a cancellation involving these factors; it is
not a theorem and it may be false.

**Third: search for a meeting with known ribbon links.** Start from the 95
unresolved saved D01 endpoints, giving the 12 single-component endpoints an
initial short box. Index a bounded collection of explicitly certified ribbon
endpoints and compare full links with preserved peripheral and orientation
data. Invariant agreement only nominates a comparison. A verified match
provides a concrete continuation of the existing movie. Keep the current
library's ribbon-link lookup, but extend the *verified target collection*
when it adds missing cases rather than only increasing band depth. This is
a search heuristic, not a completeness claim.

**Measure new states and interactions, not just moves.** If a first-stage
band merely returns D01 with a different visibly ribbon partner, record it
as a possible partner transformation. Require a full ribbon movie before
using that transformation as an implication. Matching connected-sum factors
or deleting an unknotted but linked component does not certify it. Keep
such returns in the archive; lower their priority rather than falsely
excluding them. A box that produces only already-identified states should
trigger a change of diagram or band family, not an automatic runtime increase.

**Keep K_G as a secondary construction lane.** Seventy paths survive the
new component screen. A ribbon disk on one side of the verified r=0 trace
pair can establish sliceness on the other side, but we would still need an
independent nonribbonness obstruction there. Therefore that hit alone is not
yet a counterexample. D01 remains the more direct proof target because its
nonribbonness argument is already available.

Before any new long local run, save exact input PDs, seeds, partner
certificates, pending parent states, band positions and completed prefixes
atomically. A small interrupted/restarted positive control must reproduce its
certificate. Keep this preparation bounded; most of the next authorized
effort should go to constructing the missing disk.

## Limits and stop conditions

No probability of success is justified by these counts. No global
nonexistence follows from a finite search. This pass found two unusable
prefixes and repaired interpretation of the evidence; it did not find a new
slice disk. Do not discard UNKNOWN path 73. Do not treat mirror-insensitive
or componentwise identifications as whole-link movie certificates. No
overnight Codex work or automatic restart is authorized by this checkpoint.

The highest-value next attempt is the oriented, full-link analysis of the
mirror(6_1) stabilization, followed by a bounded disk-completion search that
preserves that geometry.

Reproduce this pass from repository root:

```
../knot-venv/bin/python scripts/audit_september14_frontiers.py results/opus_snapshots/KG_frontier_345f73e.json
../knot-venv/bin/python scripts/check_september14_frontier_obstructions.py
```

The first script refuses to overwrite its result; replay in a separate copy
or preserve the existing output first. Input hashes identify the original
pinned source independently of its local path.
