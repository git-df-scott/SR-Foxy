# The tabulated link census contains no slice-not-ribbon link to 14 crossings

16 September 2026. **CE: NO.** A complete negative over a precisely specified
finite box, plus an audit of the machinery the Teichner lane now depends on.

---

## 1. Result

**Computationally exhaustive over a stated finite box.** For every tabulated
2-component link to 14 crossings:

| box | scanned | `lk = 0` | testable (`lk=0` ∧ `null V = 1`) | Theorem 2 violations | **candidates** |
|---|---|---|---|---|---|
| ≤ 12 crossings | 5,700 | 1,152 | 41 | 22 | **0** |
| 13–14 crossings | 114,874 | 19,603 | 398 | 220 | **0** |
| **total** | **120,574** | **20,755** | **439** | **242** | **0** |

A *violation* is a proof, via Eisermann Theorem 2, that the link is **not
ribbon**. 242 such links were found. Each was then screened for sliceness, and
**every single one failed**:

* a component with non-square determinant (so that component is not slice, so the
  link is not slice — every sublink of a slice link is slice); or
* Sato–Levine `β = μ̄(1122) = [z^3]∇_L ≠ 0`, which vanishes for slice links.

Among the 13–14 crossing violators the observed `β` values were `±4` (41 links)
and `±12` (5 links) — never 0.

**Conclusion, proved over this box: no tabulated 2-component link to 14 crossings
is both slice and non-ribbon.** Non-ribbonness is *common* in the tables; 242 of
439 testable links have it. Non-ribbon **and** slice does not occur.

That is why GST had to *construct* `L_{3,1}` rather than look one up, and it is
independent confirmation that the reconstruction in `research/27` is the right
target rather than a census search.

**Controls, mandatory and passing** (the sweep refuses to start otherwise):
unlinks give `null V(O^n) = n−1` with `det V = 1` for `n = 2, 3`; the Whitehead
link returns Sato–Levine `β = −1`; and `L9n18` reproduces `det V = 9`, matching
`results/eisermann_ribbon_link_gate.json`.

**What this is not.** It is not evidence that no such link exists. It is coverage
of the tabulated census to 14 crossings and nothing more. `research/22` §3.4(2)'s
`n ≥ 3` component route is untouched by it.

Scripts: `scripts/eisermann_lk0_census_sweep.py`, `scripts/eisermann_lk0_sweep_v2.py`.
Data: `results/eisermann_lk0_census_sweep.json`, `results/eisermann_lk0_sweep_13_14.json`.

---

## 2. Audit of the one-band coverage argument

The Teichner lane now runs as checkpointable one-band chunks, so the argument
licensing that has to be checked rather than assumed.

**The argument.** If `S = D_{0,1} # J` is ribbon by a movie inside the box (≤ 2
bands, each of length ≤ L with ≤ T twists), then reversing the movie writes `S` as
a fusion of an unlink, so **every intermediate link is itself a ribbon link**,
hence strongly slice. `sagefree_slice_filter` tests only *necessary* conditions
for strong sliceness and **keeps** anything it cannot decide (its own docstring
and self-test), so the first intermediate `L_1` survives the filter. Hence if the
one-band frontier of `S` has no surviving successor and no unknot endpoint, no
two-band movie exists in that box.

**Status: PROVED**, conditional on (a) the filter being necessary-only — asserted
by its docstring and checked by its self-test — and (b) the one-band enumeration
covering the same first-band set as the two-band search, which is tested below
rather than assumed.

**Empirical audit** (`scripts/teichner_frontier_resumable.py --audit`), all passing:

* *Positive control.* `6_1` is ribbon with a one-band disk; the one-band frontier
  finds the unknot endpoint. PASS.
* *Implication control.* `3_1`, `4_1`, `5_2`, `6_2`, `7_4` each have zero one-band
  survivors and no one-band hit, and the full **two-band** search also finds no
  certificate. 0 violations of the implication.

**One correction the audit forced, and it matters.** On all six ribbon knots
tested (`8_9`, `8_20`, `9_27`, `8_8`, `9_46`, `10_3`) the one-band frontier reports
`survivors = 0` **but** `unknot endpoint = True` — because `survivors` counts only
*non-unknot* endpoints. So "zero survivors" alone does **not** mean "no disk"; the
coverage rule must be **zero survivors AND no unknot endpoint**. The resumable
runner's `zero_survivor_diagrams` field applies exactly that conjunction. Reading
`survivors = 0` as coverage on its own would have silently inverted the test.

**Honest limitation.** The sharp control — a ribbon knot whose disk genuinely needs
*two* bands, where a real two-band certificate must leave a nonzero one-band trace
— is **unfulfilled**: every ribbon knot tried has a one-band disk, so the critical
case was never exercised. The argument stands on its proof, not on that control.

---

## 3. Checkpointing defect found and fixed

`scripts/teichner_one_band_frontier.py` builds its record fresh on every start and
never reads an existing output file, so a container reclamation **destroys every
completed row**. On a box that reclaims in ~2 h this makes long frontier runs
unresumable in practice.

`scripts/teichner_frontier_resumable.py` replaces it:

* **deterministic unit ids** `"<knot>|<J>|<diagram>|<box-hash>"`, so the same
  configuration always yields the same ids and no region is skipped or duplicated;
* **atomic completion records** — tmp file plus `os.replace` after every unit;
* **resume** — loads the existing checkpoint and skips completed ids;
* **retune protection** — refuses to resume a checkpoint whose box-hash differs,
  so a silently retuned search cannot be merged into an old one;
* **final coverage audit** listing, per partner, which diagrams are done and which
  are genuinely zero-survivor-and-no-hit.
