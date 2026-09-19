# The Dunfield-Gong dataset is finally in the container, and it closes the 0-friend lane by a theorem

19 September 2026, Opus. **CE: NO. Smooth concordance `K_0 ~ K_1`: UNKNOWN.
Slice-Ribbon CE: NO.**

Checker: `results/opus_2026_09_19_0800_dg_zero_friends/check_dg_zero_friends.py`
-> `RESULTS.json`, controls pass. Data extract: `data/dg_unresolved_le15.csv`.

Nothing here is a counterexample and nothing here obstructs one. One named open
ledger item is closed, one stale citation is corrected, and one new primary
source is checked and found vacuous for our purposes.

---

## 1. The dataset is here, md5-verified, for the first time

`research/04` §1(b) records the Dunfield-Gong archive as a thing we know about
and have not pulled — *"(Ranged access to the Dataverse download endpoint
returned 404 for me — expect to pull the whole GB.)"*

Pulled. `doi:10.7910/DVN/YBDTBT` -> `plausibly_slice_V1.zip`,
**1,022,355,830 bytes, md5 `7f6dc1df595ba1b4dbb1a9b338798b0b`** — byte count and
hash both match the figures `research/04` recorded from the Dataverse metadata,
so the file is the one that paper describes. It is **not** committed here (1 GB);
what is committed is the extract in §4 and the checker in §2.

What it contains that this campaign has wanted:

| file | what |
|---|---|
| `data/zero_friends.csv` | 78,507 0-friends of PS19 knots (the ZF collection, §5.3) |
| `data/more_zero_friends.csv` | 79,667 more, diagrams <= 90 crossings |
| `data/plausibly_unknown.csv` | **11,679 knots of unresolved slice status, with PD codes, `fibered`, `genus3`, `alex`, `tau/nu/epsilon`, `s_*`, HKL columns** |
| `knots_mentioned_PD_codes.csv` | PD codes for the 285 knots DG name in the paper |
| `code/find_0_friends.py`, `code/rbg.py` | DG's own 0-friend generator and RBG machinery |

## 2. The 0-friend lane is closed, and not by a failed search

`HANDOFF_2026_09_18_OPUS.md` P2 and `research/24` line 185 both name *mine
Dunfield-Gong's 0-friend pairs* as the way to extend the wild-Miyazaki-pair hunt
past this repository's own `<= 14` crossing census — which came back empty
(`results/opus_2026_09_19_0700_zero_surgery_search_complete/`).

It cannot work, for a reason that is a theorem rather than a bound.

> **Proposition R.** No 0-friend pair drawn from a *plausibly slice* census can
> be a wild Miyazaki pair — two distinct fibered knots sharing one irreducible
> Alexander polynomial — at any crossing number.
>
> *Proof.* DG §1.8 defines PS19 by `sigma(K) = 0` **and Fox-Milnor**:
> `Delta_K(t) = f(t) f(t^-1)` up to a unit of `Z[t^+-1]`. Normalise `f` to a
> polynomial of degree `d` with `f(0) != 0`; then `Delta = f(t) f*(t)` with
> `f*(t) = t^d f(1/t)`, both factors of degree `d`. If `Delta` is irreducible in
> `Q[t]` one factor is a unit, so `d = 0` and `Delta` is constant; `Delta(1) = +-1`
> forces `Delta = 1`. A fibered knot has `deg Delta = 2g`, so `Delta = 1` forces
> `g = 0`, the unknot. A 0-friend shares its 0-surgery and hence its Alexander
> polynomial with its base knot, so this applies to both members of the pair. []

**The data agrees, and is the control that the proposition is not mis-stated.**
Over all **158,174** rows of `zero_friends.csv` + `more_zero_friends.csv`:

| | |
|---|---|
| `Delta` trivial | 8,393 |
| `Delta` nontrivial, not monic | 67,380 |
| `Delta` nontrivial, monic | 82,401 |
| of those, **irreducible over Q** | **0** |

Controls pass in the same run, including two that must fire *positive*
(`Delta(3_1) = t^2-t+1` and `Delta(6_3) = t^4-3t^3+5t^2-3t+1`, both monic
irreducible) and two that must fire *negative* (the `6_1` non-monic norm and the
square knot's monic norm). Per this repository's standing trap — *always run a
control that asks whether the tool works at all before believing an all-negative
sweep* — an all-zero column from a filter that cannot detect a positive would
have decided nothing.

Independent consistency check on the same dataset: of the **25 fibered** knots in
`plausibly_unknown.csv`, every one has `deg Delta = 2 * genus3` (so the `fibered`
column is internally consistent) and **none** has irreducible `Delta`.

### 2.1 The general moral, which is worth more than the null

The population a wild Miyazaki pair lives in is **disjoint from every
plausibly-slice census, by Fox-Milnor.** `J` and `J'` are *not* slice and must not
be — only the difference `J # (-J')` is. So any dataset built by filtering for
sliceability is structurally the wrong place to look, however large it is. This
repository's own census sweep used the right population (all 59,937 hyperbolic
knots `<= 14` crossings, then fibered + irreducible `Delta`); it was the
*extension* that was aimed wrong.

**The redirect is concrete and the tool now exists locally.** DG's
`code/find_0_friends.py` implements the [DOR §9.3] geodesic-drilling generator,
which applies to *any* hyperbolic knot — it is only DG's *input* that was
Fox-Milnor filtered, not their method. Running it on the 16,970 fibered knots
with irreducible `Delta` from `miyazaki_pair_sweep` is the version of P2 that is
not closed by Proposition R. Nobody has run it.

## 3. A stale citation: "21 prime knots with up to 14 crossings" is now 16, and they are named

`ASTRA_BRIEF_2026_09_19.md` §1 lists, from GHMR, *"21 prime knots with up to 14
crossings, ribbon status unknown"*, and this repository has never held them.

GHMR §3 attributes that figure to the **earlier** Dunfield-Gong classification.
The December 2025 paper supersedes it: `plausibly_unknown.csv` restricted to
`num_cross <= 14` has **exactly 16 rows**. All 16 appear in DG Table 1.

```
K13n65  K13n3871  K13n3872  K13n3897  K13n3936  K13n4582
K14n3713  K14n4425  K14n4621  K14n5486  K14n9023  K14n10011
K14n11063  K14n18909  K14n18911  K14n21673
```

* **None is fibered.** So — exactly as `results/opus_2026_09_19_0100_mp_rbg_lane`
  found for the ten MP survivors — Miyazaki Thm 5.5 and Hom-Park Thm 1.1 both
  quantify over fibered knots and **neither reaches any of them**. That is now
  two independent open-problem shortlists on which our only two non-ribbon
  certificates are vacuous for the same reason. It is the sharpest statement of
  the KDG-side wall we have: the field's own candidate lists are built from the
  population our certificates cannot see.
* 14 of the 16 have `Delta = 1`, hence are topologically slice (Freedman) and
  topologically homotopy-ribbon ([FQ] Thm 11.7B, per DG §1.17).
* `K14n3713` and `K14n4621` have `Delta = (t^2-t+1)^2` and are the only two whose
  *topological* slice status is also unresolved.
* `tau = nu = epsilon = 0` and `s_0 = s_2 = s_3 = 0` on all 16, already computed
  by DG. We do not need to recompute them.

## 4. What is committed: `data/dg_unresolved_le15.csv`

The 59 knots of `<= 15` crossings whose smooth slice status DG could not resolve,
with `alex`, `genus3`, `fibered`, `det`, `volume`, `tau/nu/epsilon`, `s_0/s_2/s_3`,
the HKL ribbon-obstruction column, and **PD codes**.

**Verified on load, not assumed:** all 59 PD codes build in `spherogram`, all are
1-component, all have the stored crossing number, and **58 of 59 reproduce the
stored hyperbolic volume to `1e-6`**. The single exception is `K15n115646`, which
DG Table 4 lists as non-hyperbolic (a satellite, `Trefoil[3/2]`); its stored
volume is the sentinel `-1.0` and SnapPy's 3.6639 is a degenerate solution for a
non-hyperbolic exterior. Expected, not a defect in the extract.

## 5. One new primary source, and it is vacuous for us

**Hom-Park, _Ribbon concordance and cabling_, arXiv:2608.06625 (6 Aug 2026)** is
carried in `research/01` as **S10, PARTIALLY VERIFIED (abstract/metadata)** and
appears in `research/02`'s and `research/03`'s 2026 lists without a vacuity
ruling. Read in full text today; the ruling is negative, twice over.

* **Definition (§2, verbatim):** `hmin(K) := min{ht(gamma_i) | i > 0}`, the
  minimum height of a *homologically inessential* component of the immersed-curve
  collection `gamma(K)`, *"with the convention that `hmin(K) = 0` if
  `gamma(K) = gamma_0(K)`."*
* **Proposition 2.3 (verbatim):** *"If `J <= K` and `hmin(J) != 0`, then
  `hmin(J) >= hmin(K)`."*

`K` is ribbon iff `U <= K`, and `gamma(U) = gamma_0(U)` has no inessential
component, so `hmin(U) = 0` and **Proposition 2.3's hypothesis fails at the
unknot**. Vacuous as a ribbon obstruction.

Their **Lemma 2.4** (`J <= K => h_0(J) = h_0(K)`) *is* non-vacuous at `J = U`,
giving `h_0(K) = 0` for every ribbon `K` — but they derive it from `gamma_0`
being *"invariant under ordinary concordance [HW23, Prop 2]"*, so it holds for
every **slice** knot and dies at slice level.

So S10 joins the pattern `research/02` §0 documents: every ribbon-concordance
obstruction either degenerates from the unknot or is already known at
slice/handle-ribbon level. **Theorem 1.6** (a nontrivial fibered knot with
`hmin != 2` is prime) is a genuinely new computable criterion, but it is a
primality statement, not a vanishing obstruction, and our `Lemma P` already gives
primality for the population we care about by a cheaper route.

## 6. What did not change

`D_{0,1}` still needs a slice disk nobody knows how to build; `18nh00000601`
still needs a ribbon-only obstruction the field does not have. Proposition R
removes a route that looked open; §3 replaces a stale target list with a correct
and smaller one; §5 closes a source that was still marked partially verified.
None of it is a counterexample.
