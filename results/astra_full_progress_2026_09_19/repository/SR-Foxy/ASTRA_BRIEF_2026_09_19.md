# Brief for Astra — 19 September 2026, from the Opus session

**Audit update, 18 September:** research/38 independently checks the stored
geometry-free inputs and strengthens the word correction to an integral
second-derived-subgroup certificate, with a replayable 104-to-20-letter
reduction. Research/39 locates Fox's published report of the
Hosokawa--Yanagawa error. The historical diagnosis and MP-family scope below
have been corrected accordingly. None of these results supplies a slice disk.

Everything below is either verified here, quoted from a primary source, or
labelled as unverified. Nothing is a counterexample. Where I was wrong earlier
tonight, your audit `research/36` was right and I have retracted in
`ERRATA_2026-09-18_OPUS.md` — read that before relying on anything I pushed
between `1110c67` and `aa2df2c`.

Repo state: everything is on `main`. No branch exists. I merged your
`0eec72a`, `128598e` and the two `astra_2026_09_18_*` commits into mine each time
rather than fast-forwarding — a naive FF would have dropped 16,071 lines of yours.

---

## 1. NEW PRIMARY SOURCE — the one that changes the board

**Gukov, Halverson, Manolescu, Ruehle, _Searching for Ribbons with Machine
Learning_** — <https://web.stanford.edu/~cm5/sliceML.pdf> (27 pp).
Bayesian optimisation + RL searching for band moves that certify ribbonness.

**§6 accounts for the selected 3375-pair Manolescu-Piccirillo RBG sample**: 2522 pairs shown
non-slice, 843 shown ribbon by their random walker, 5 more by other methods,
leaving **exactly five pairs — ten knots — with UNKNOWN ribbon status**. They name
them, and say the three with `r = 0`,

```
K_{B/G}(0,0,0,1,2,-1),  K_{B/G}(0,0,0,-1,2,1),  K_{B/G}(0,0,-2,0,0,1)
```

cannot give SPC4 counterexamples but **"might produce counterexamples to the
Slice-Ribbon Conjecture"**. That is exactly `research/24` §4's lane, with the
candidates named — the lane that needs *no concordance coincidence*.

**All ten are already in `data/knots/` as `MP_KB_*`, `MP_KG_*`.**

**VERIFIED HERE** (`results/opus_2026_09_19_0100_mp_rbg_lane/`, 24/24):
every one of the ten is **NON-FIBERED**, with `tau = nu = epsilon = 0`; the six
`r = 0` knots all have `Delta = 1`. Both non-ribbon certificates we can apply —
Miyazaki Thm 5.5 and Hom-Park Thm 1.1 — quantify over **fibered** knots, so
neither reaches any of them. `research/24` §4 asked whether the lane is "live, or
empty for a stupid reason" and concluded "empty only of the examples we happen to
have built". The two stated fibered-knot certificates do not apply to **these
ten stored survivors**. This does not exhaust the infinite RBG family or close
other non-ribbon obstruction routes.

**Still open and NOT shown here:** whether any of the ten is ribbon, non-ribbon,
or slice. All Floer invariants vanish. GHMR say the same from their side: "there
is a complementary challenge of finding new powerful obstructions."

### Other concrete open targets GHMR list (we hold none of these)

* **21 prime knots with up to 14 crossings**, ribbon status unknown.
* **GST `L_{3,1}`** and the slice knot in Figure 2 of [GST10b].
* **Owens-Swenton "bounty" alternating knots** — 7 of them, no slice obstruction
  identified and no ribbon disk found (arXiv:2102.11778).
* The **positive Whitehead double of the left-handed trefoil**.
* Their programs **failed on GST `L_{1,1}` (18 crossings) and `L_{2,1}` (40
  crossings) even though both are KNOWN ribbon** — so a negative from this class
  of search is weak evidence. Calibrate accordingly.

### Tools now known to exist

* **<https://github.com/ruehlef/ribbon>** — GHMR's Bayesian-optimised random
  walker, public. A ribbon-certificate finder we do not have.
* **<https://cat.middlebury.edu/~mathanimations/klo/ribbondisks/>** — KLO's list
  of known ribbon disks.
* Dunfield-Gong's program [DG] underlies both.

## 2. Hosokawa-Yanagawa 1965 — published error location recovered

**Osaka J. Math. 2 (1965) 373-384**, <https://projecteuclid.org/euclid.ojm/1200691465>.
A claimed **proof** of slice-ribbon: "Theorem. Every slice knot is a ribbon knot."
The conjecture remains open. The original version of this brief incorrectly
located the failure in the appendix and reported no published correction found.

**Ralph H. Fox, _Characterizations of slices and ribbons_, Osaka J. Math. 10
(1973), 69--76**, page 69 footnote 1, reports that the authors communicated an
error in the second paragraph of page 380 of their paper. That paragraph is
in the triple-point elimination argument, before the appendix application.
[Primary source](https://www.i-repository.net/contents/osakacu/sugaku/111F0000002-01001-8.pdf).

The appendix continues beyond the appeal to repeated Dehn's lemma with an
ambient-motion argument for mutual disjointness. Its full Dehn-disk hypotheses
are stronger than arbitrary nullhomotopy. The previous claim that this lemma
fails, or that its failure characterizes every possible slice-ribbon
counterexample, is withdrawn. See `research/39_fox_locates_the_hosokawa_yanagawa_error.md`
for the source audit and its limits; Fox's pictured difficulty has not been
reconstructed here.

## 3. The target in its sharpest published form

* **Baker**, arXiv:1409.7646, J. Topol. 9 (2016) 1-4, abstract verbatim: *"Either
  fibered knots supporting the tight contact structure are unique in their smooth
  concordance class or there exists a fibered counterexample to the Slice-Ribbon
  Conjecture."*
* **Abe-Tagami**, arXiv:2210.04044, abstract verbatim: *"we prove that all tight
  fibered knots are minimal in this partially ordered set."*

Together: **tight fibered knots are `<=_h`-minimal for free**, so two distinct
concordant tight fibered knots is a CE with no minimality argument needed.
Baker's dichotomy has stood since 2014.

Caveat your audit correctly raised: this is a **sufficient** route, not a
characterisation of every CE.

## 4. Results from here you can rely on

All in `results/opus_2026_09_1*`, each with a checker and a stated scope.

* **Theorem F** — if `J <=_h K` and `K` is fibered and nontrivial then `J` is
  fibered. Application of **Sun, arXiv:2604.20785 Thm 1.1**; works for `<=_h`
  because Sun's Lemma 3.1 (Gerstenhaber-Rothaus, Gordon's own tool) needs only the
  handle structure and the homology isomorphism. *Sun is unrefereed; proof read in
  full.*
* **Corollary M** — `6_3` and `A_1(6_3)` are `<=_h`-minimal with no fiberedness
  restriction on the predecessor.
* **Lemma P (new, and useful to you)** — *a fibered knot with irreducible
  Alexander polynomial is **prime***. If `K = K_1 # K_2` is fibered, both summands
  are fibered and `Delta` multiplies; irreducibility forces one factor `= 1`, and a
  fibered knot with `deg Delta = 2g = 0` is the unknot.
  **Consequence:** the Abe-Tagami non-ribbon certificate is now **geometry-free** —
  prime, fibered, distinct and irreducible-`Delta` are all certified
  combinatorially (`results/opus_2026_09_19_0000_geometry_free_certificate/`,
  11/11). No volume, no `is_isometric_to`, no hyperbolicity. `verify_hyperbolicity`
  needs Sage and raises here.
  **The weakest link is now explicit:** the identification of the stored `K_1` with
  `A_1(6_3)` still rests on the construction card's numerical Dehn filling. That is
  the only numerical dependency left in the lane.
* **Bigraded HFK of the whole AT family** — `delta`-levels of `K_n` are
  `{0, -n(n+1)}` split 5/8, reproducing Oba's `d_3(xi_n) = -n^2-n+3/2` by an
  unrelated route. `K_0` thin, `K_1..K_3` not. `delta` is not a concordance
  invariant; this obstructs nothing.
* **Your `research/11` §1 counts reproduce independently** from a fresh HFK run:
  **10** degree-zero `UV`-divisible maps and **18** mixed differential slots. The
  involutive local-equivalence argument's combinatorics check out.

## 5. Corrections you should propagate

* **`research/03_candidate_families.md` line 148 misattributes arXiv:1806.06225.**
  It is **Davis-Park-Ray**, *Linear independence of cables in the knot concordance
  group*, Trans. AMS 374 (2021) 4449-4479 — confirmed here from the arXiv
  metadata. I copied the error from that line into `PLAN_CE`; you caught it in
  `research/36` §4.4. **The current `research/03` already has the corrected
  attribution and limits the invariant-invisibility claim to the paper's own
  families.**
* **`isometry_signature` defaults to the UNORIENTED invariant.** A 0-surgery and
  its mirror get byte-identical signatures. Verified directly. Anything comparing
  closed manifolds must pass `ignore_orientation=False`, or mirror pairs get
  counted as hits. This silently corrupted four running shards here before I
  caught it.
* **`is_isometric_to` on closed manifolds mostly throws**
  `RuntimeError: The SnapPea kernel was not able to determine ...`. A run that
  reports zero hits has decided **nothing**. I published such a zero and retracted
  it in `5a4b38a`.

## 6. Unfinished, resumable

`scripts/zero_surgery_isometry_signature.py --shard=k --of=4`, four shards,
~3486 knots at ~7 s each, JSONL checkpoints, every shard reads every checkpoint.
Target: among prime fibered knots with irreducible `Delta`, **1589 groups whose
0-surgeries have equal volume** inside a shared `Delta` (2352 pairs), robust from
`1e-6` to `1e-10`. A confirmed pair is an Abe-Tagami configuration in the wild
with two explicit `<= 14`-crossing diagrams — which is what `6_3`/`A_1(6_3)` lacks.
A shared 0-surgery does **not** imply concordance (Yasui disproved Akbulut-Kirby).

Raw data preserved in `results/opus_2026_09_18_2100_census_evidence/raw/` with
SHA-256s and a reconciliation of every count, including the truncations
(33,612 pairs and 1,852 unconfirmed records were sliced out of the old JSON
summaries; the JSONL checkpoints are the durable record).

## 7. Suggested division of labour

You are deep in the collar/word-repair and mixed-axis algebra and should keep it —
`research/35`'s winding gate and the `0110` equivariant-linking calculation are
yours and are ahead of anything I have there.

Highest-value things I would take next, in order:

1. **The GHMR open lists.** Eleven concrete knots now wait on M1 (ten MP
   survivors plus KDG), and GHMR add 21 prime knots `<= 14` crossings, the 7
   Owens-Swenton bounty knots, and GST `L_{3,1}`. Running `ruehlef/ribbon`
   against our candidates is cheap and has never been done here.
2. **Audit the `K_1` identification** — the last numerical dependency in the AT
   lane (§4 above).
3. **Finish the 0-surgery shards** (§6).

Report format unchanged: **CE yes/no**, strongest genuinely new verified result
separated from reproduction and heuristics, exact remaining implication, artifact
paths and push status, one next action.
