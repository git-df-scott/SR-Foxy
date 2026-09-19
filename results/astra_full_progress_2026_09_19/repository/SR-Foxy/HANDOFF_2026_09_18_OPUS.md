# Handoff — SR-Foxy, 18 September 2026 (Opus session)

**NO COUNTEREXAMPLE. Smooth concordance `K_0 ~ K_1`: UNKNOWN. Slice-Ribbon CE: NO.**

Read this with `research/22_where_a_counterexample_can_come_from.md`,
`ERRATA_2026-09-16.md`, and `results/chat_archive_2026_09_17/CORRECTION_REGISTER.md`.
Everything below is either machine-checked in a named script or labelled with its
status. Nothing here is a counterexample and nothing here obstructs one.

---

## 1. The shape of the problem, stated once

A counterexample needs a knot that is **slice** and **not ribbon**. There are
exactly two ways to get one, and they have different missing halves.

| lane | has | needs | the wall |
|---|---|---|---|
| **KDG** `18nh00000601` | smoothly slice in standard `B^4` (Oliveira-Smith, arXiv:2603.23717), and handle-ribbon | a proof it is not ribbon | no ribbon-only obstruction exists in the literature |
| **AT** `D_{0,1} = 6_3 # (-A_1(6_3))` | a proof it is not even homotopy-ribbon (Miyazaki Thm 5.5) | a smooth slice disk, i.e. a concordance `K_0 ~ K_1` | no construction produces one; the only positive machine lands one `S^2xS^2` away |

**The asymmetry matters and is easy to miss.** KDG is handle-ribbon, so a
counterexample there refutes exactly `slice => ribbon`. `D_{0,1}` is not
homotopy-ribbon, so if it is slice it refutes `slice => homotopy-ribbon`, which is
**strictly stronger** and implies the other. `research/22` §2 says this; this
session verified its load-bearing hypothesis (§3 below). The AT lane is aiming
several rungs above the target. That does not make it wrong — it may be the only
constructive path — but the prior should reflect it.

---

## 2. What is now proved (new this session)

**Theorem F.** *If `J <=_h K` and `K` is fibered and nontrivial, then `J` is
fibered.*
Application of Sun, arXiv:2604.20785 Theorem 1.1 (fibered classes descend across
a ribbon homology cobordism). The work was checking `<=_h` meets its hypotheses:
the concordance exterior in a homotopy `I x S^3` is a homology cobordism between
the knot exteriors; Agol-Ren's definition of strongly homotopy-ribbon is verbatim
Sun's ribbon condition; direction conventions pinned by comparing his Cor 1.2
against Thm 1.1; the fibered class transports because meridian pairs with
meridian. It survives the jump from `<=` to `<=_h` because Sun's Lemma 3.1 — the
Gerstenhaber-Rothaus extension, Gordon's own tool — needs only the handle
structure plus the homology isomorphism, never a band presentation, an absence of
local maxima, or a standard ambient.
*Caveat: Sun's preprint is unrefereed. Its proof was read in full.*
`results/opus_2026_09_18_0005_hr_predecessors_are_fibered/` (13/13).

**Corollary M.** `K_0 = 6_3` and `K_1 = A_1(6_3)` are `<=_h`-minimal with **no**
fiberedness restriction on the predecessor. Predecessor list is finite and
complete — `U`, both trefoils, `4_1` — each excluded by `det = 13` not being a
square or by Friedl-Powell divisibility against an irreducible degree-4 `Delta`.
The `Delta = 1` worry is subsumed: a fibered knot with trivial Alexander
polynomial is the unknot. **This closed the gap that both the previous pass and
`CORRECTION_REGISTER` item 18 had flagged as unverified.**

**Second, independent route to the implication.** `K_0 ~ K_1 => slice-ribbon
false` now holds by two routes sharing no step: Miyazaki / Agol-Ren Cor 1.14(1),
and Agol-Ren Question 1.15 plus their unnumbered genus-`<=3` remark.
*The second is corroborating only — that remark is printed with no proof.*
`results/opus_2026_09_17_2355_agol_ren_q115_reduction/` (23/23).

**Miyazaki hypothesis check.** `MANIFEST.md` flagged `research/22` §2's argument
as "should be checked... not struck here". Checked: Miyazaki 5.5's second
alternative (no `f` with `f(t)f(1/t) | Delta`) holds because `Delta(6_3)` is
irreducible — a degree-1 `f` forces a degree-2 factor, a degree-`d` `f` with
`f f* | Delta` of degree `2d` forces `Delta = f f*`, a constant needs
`f^2 | content = 1`. So Miyazaki applies and `D_{0,1}` is not homotopy-ribbon.

**Alexander divisibility under `<=_h`** (earlier pass, on `main`): holds, and
Gilmer's stronger hypothesis was never needed — Friedl-Powell arXiv:1907.09031
Thm 1.1, whose authors state the injectivity hypothesis "is not needed anywhere
in our proof".

---

## 3. What is computed

**Bigraded HFK of the whole Abe-Tagami family** — `AbeTagami_K_n_NOTES.json`
recorded that none existed. `results/opus_2026_09_18_0040_hfk_delta_law/` (37/37).

* Total rank 13, fibered, genus 2, `tau = nu = epsilon = 0` for every `K_n`.
* `delta = M - A` levels are `{0, -n(n+1)}`, split 5 and 8. The lowest level
  reproduces the `n`-dependence of Oba's `d_3(xi_n) = -n^2-n+3/2` by a completely
  unrelated route, and carries the involution `n -> -1-n` behind
  `K_n = K_m iff n = m or n + m = -1`.
* `K_0` is thin; `K_1, K_2, K_3` are not. `D_{0,1}` is not thin, so **no thinness
  shortcut makes its involutive invariants vacuous**.
* `delta` is not a concordance invariant. This obstructs nothing.

**Two flagged risks discharged** (from `research/opus_mixed_lift_review.md`):
every generator of `CFK(K_1)` has `delta in {0,-2}` split 8/5 (risk 4), and the
admissible mixed `U^a V^b` slots number exactly **18** (risk 5).
*Risks 1-3 remain open: the same engine family was used, so absolute bigradings
are re-derived rather than independently checked.*

**HFK engine validated.** 196 alternating knots, 196/196 match the Ozsvath-Szabo
closed form `m = s - sigma/2`. `Link.signature()` and `alexander_polynomial()`
need Sage, which is absent, so `Delta` came from `det(V - tV^T)` and `sigma` from
exact congruence diagonalisation of `V + V^T`.
`scripts/hfk_engine_grading_validation.py`.

---

## 4. The new lane (this session) — wild Miyazaki pairs

**The criterion, freed from Abe-Tagami.** Miyazaki 5.5 never mentions `6_3`. Its
second alternative holds for any irreducible `Delta`. Therefore:

> For **any** two distinct prime fibered knots with irreducible Alexander
> polynomials, their connected sum is never homotopy-ribbon, hence never ribbon.
> So **any** concordant such pair refutes slice-ribbon.
>
> **Corollary.** If slice-ribbon holds, no two distinct prime fibered knots with
> irreducible Alexander polynomial are smoothly concordant.

Fox-Milnor pins the search: `Delta_J Delta_{J'} = f f*` with both irreducible
forces `f = Delta_J` and `Delta_{J'} = Delta_J* = Delta_J`. **A concordant pair
must share one irreducible Alexander polynomial.**

**Why the window is narrow for constructions** (not for invariants — see the trap
in §6): `K # R` for `R` ribbon is not prime; a satellite has
`Delta_P(t) Delta_K(t^w)`, generically reducible; a winding-number-zero satellite
fixes `Delta` and primality but its genus grows while `deg Delta` does not, so
`deg Delta < 2g` and it is not fibered. Every cheap construction breaks exactly
one of prime / fibered / irreducible. The annulus twist is a rare machine that
preserves all three.

**Census results** (all 59937 hyperbolic knots `<= 14` crossings):

| | |
|---|---|
| fibered with irreducible `Delta` | 16970 |
| `Delta` shared by more than one | 2925 |
| pairs also matching `tau, nu, epsilon` | 35612 |
| in shared-`Delta` buckets (0-surgery stage) | 14127 |
| usable geometric 0-surgery solutions | 14122 |
| **0-surgery volume-matched groups** | **1589** (2352 pairs) |

**The volume coincidences are real.** Tightening the grouping tolerance from
`1e-6` to `1e-10` splits essentially nothing (1589 -> 1588 at `1e-11`). A knot and
its mirror share an exterior and occupy one census entry, so group members are
genuinely different knots.

**Status: confirmation IN PROGRESS.** `scripts/zero_surgery_isometry_signature.py`
is running. See §5 for why the earlier attempts failed and why this one is sound.

---

## 5. The plan for a counterexample, in priority order

### P1. Finish the wild-pair confirmation (in flight, highest value per unit work)

`scripts/zero_surgery_isometry_signature.py` signs each 0-surgery in a
volume-matched group with `M.isometry_signature()` and groups by signature.
**Equal signature means isometric** — it is built on the *canonical*
retriangulation, so it is NOT the retracted `isoSig`-after-random-`simplify()`
method of `research/34`. Controls pass: reproducible on the same manifold,
separating on different ones. Cost ~6 s/knot, ~3300 knots; the run is resumable
via a JSONL checkpoint. Hits are re-run with `verified=True` and that status is
recorded.

For each confirmed pair `(J, J')`:

1. Miyazaki fires for free — irreducibility of `Delta` is already in the data, so
   `J # (-J')` is never homotopy-ribbon.
2. Do **not** cite agreeing classical invariants as support. Same 0-surgery means
   same S-equivalence class, so by Lemma B of `research/33` those agreements are
   theorems, not evidence.
3. The concordance still has to be **built**. Yasui disproved Akbulut-Kirby.
4. **The payoff over Abe-Tagami:** both knots are `<= 14` crossings with explicit
   diagrams, so the trace, the annulus, and any band movie are directly
   computable. `K_1` is in no census and had to be rebuilt from Figure
   `annulus-pre`; that is a large part of why the AT lane stalled.

If the run returns **no** isometric group, that is a bounded negative over `<= 14`
crossings — and an interesting one, since it would say the 0-surgery machine is
rarer than the invariant coincidences suggest.

### P2. Extend the wild-pair search beyond the census

The census is a small room. Extensions, in order of cost:

* Piccirillo-style **RBG links / dualizable patterns** generate 0-surgery-equal
  pairs by construction rather than by search — this is how trace-siblings are
  built, and it is the natural generator for this lane.
* **Annulus presentations** of census knots: enumerate annulus twists `A_n(J)` for
  `J` fibered with irreducible `Delta`, which preserves all three conditions by
  construction. Abe-Tagami is the `J = 6_3` case; nothing says it is the best one.
* Relax to knots of 15-16 crossings where HFK is still computable.

### P3. Agol-Ren Question 1.15 for the AT pair

A fibered `K` with `K_0 <=_h K` and `K_1 <=_h K` gives `K_0 ~ K ~ K_1` in a
homotopy `I x S^3`; standardising it is the Dunfield-Gong/Oliveira-Smith pattern.
By Casson-Gordon (Agol-Ren Thm 1.7, printed as `[CG83]`) plus Theorem F, this is
now a **pure mapping-class-group question on `Sigma_{2,1}`**: is there a surface
homeomorphism compressing to both

```
phi_0 = t_d^-1 t_b t_c^-1 t_a
phi_1 = t_{c'_1}^-1 t_{c'_2} phi_0
```

(Abe-Tagami Appendix B, in `AbeTagami_K_n_NOTES.json`)? They differ by exactly the
annulus-twist pair. This is the first formulation of the campaign's central
question with no 4-manifold in it. Implementing Casson-Long / Agol-Ren's
minimal-compression algorithm is the concrete task; **no flipper, curver, twister
or Sage exists in the cloud container**, so this needs tooling first.

Conversely, **proving** Q1.15 for hyperbolic genus-2 `<=_h`-minimal pairs kills
the AT lane outright — a valuable negative that would free the campaign.

### P4. Involutive Heegaard Floer on `D_{0,1}`

Live and uncomputed. Everything that vanishes does so through the *ordinary*
local equivalence class; `iota_K`, `d-bar`/`d-underline`, and the involutive local
class are untouched, and `D_{0,1}` is **not thin**, so no shortcut kills them.
Needs `CFK^infinity` with differentials — the bundled calculator returns bigraded
ranks only. **Tooling gap, not a mathematical one.** A non-vanishing involutive
obstruction would kill the AT lane; vanishing would be the strongest survival
evidence yet.

### P5. KDG — only if a ribbon-only obstruction appears

`research/02` leaves exactly one computable ribbon-only family, Eisermann's link
theorems, and `research/22` §3.1 shows them vacuous for 2-component slice links.
"No unlink derivative" is an infinite search with no bounding theorem
(`research/02`, `06`, `07`). The gap *is* Generalized Property R. **Do not spend a
session here without a new idea** — this is a field-level wall, not a search
problem.

---

## 6. Traps — read before running anything

**Never turn a tool failure into a result.** This session reported "0 isometric
0-surgery pairs" when every pair had thrown
`RuntimeError: The SnapPea kernel was not able to determine if the manifolds are
isometric`. Nothing had been decided. Retracted in `5a4b38a`. Same class as the
`isoSig` retraction in `research/34`. **Always run a control that asks whether the
tool works at all before believing an all-negative sweep.**

**A pattern that matches its own shell.** Three times this session:
`pkill -f <script>` killed its own parent (exit 144); `pgrep -f <script>` matched
the watcher whose command string contained the name, reporting a dead sweep as
alive; and again on a hung job. Use `ps aux | grep "[p]ython3"` and kill by PID.

**Background jobs die with the sandbox.** `nohup` does not survive between turns.
Use the harness's own background mechanism, and make long runs resumable via a
JSONL checkpoint.

**Do not rebuild the census inside a helper.** `snappy.HTLinkExteriors(cusps=1)`
inside a per-call function burned 238 minutes of CPU without finishing 100 of 2352
pairs. Cache it once.

**A long candidate list is not a result.** 35612 pairs passing `Delta/tau/nu/eps`
measures how coarse those invariants are, nothing more. I conflated the narrow
*construction* window with the *invariant* window and had to correct it.

**Sage is absent** in the cloud container, so `Link.signature()`,
`alexander_polynomial()`, `jones_polynomial()` all raise. Workarounds:
`seifert_matrix()` works; `Delta = det(V - tV^T)`; `sigma` by exact congruence
diagonalisation; `Delta` also from the graded Euler characteristic of HFK.
Chern-Simons is unavailable on the filled 0-surgeries, and `length_spectrum` needs
`ManifoldHP` (normal precision fails the Dirichlet construction).

**Available:** SnapPy 3.3.2, Regina, Spherogram 2.4.1, sympy 1.14.0, 16 GB RAM.
**Absent:** Sage, numpy, flipper, curver, twister.

---

## 7. Repository state

* `main` at `7120011` (Corollary M / Theorem F landed).
* Branch `claude/compassionate-carson-b6lxu8` carries everything after that.
  Scott deleted the remote branch twice and closed PR #11; a direct push to
  `main` was approved once and later blocked by the permission classifier, so
  **ask before assuming either route is open**.
* New scripts: `miyazaki_pair_sweep.py`, `zero_surgery_pair_search.py`,
  `zero_surgery_confirm.py`, `zero_surgery_hammer.py`,
  `zero_surgery_isometry_signature.py`, `hfk_engine_grading_validation.py`,
  `common_upper_bound_search.py` (superseded, stopped at 20000/59937 with its
  Zemke bigraded-domination filter admitting nothing).
* Intermediate data lives in `/tmp/claude-0/` and does **not** survive the
  container. `miyazaki_pair_sweep.jsonl` (16970 rows) and
  `zero_surgery_volumes.jsonl` (14122 rows) are the expensive ones —
  **copy them into the repo before the session ends** if they are still wanted.

---

## 8. Honest standing

No counterexample. The AT lane needs a construction nobody knows how to make; the
KDG lane needs an invariant the field does not have. What genuinely moved is that
the implication chain beneath a counterexample is now verified rather than
assumed, and that the search target has been widened from one pair of knots to a
characterised class — with 1589 volume-matched candidates awaiting confirmation.
