# Bigraded HFK of the whole Abe-Tagami family, a delta law matching Oba's `d_3`,
# and two flagged risks discharged

18 September 2026, Opus session. **NO COUNTEREXAMPLE.**
**Smooth concordance `K_0 ~ K_1`: UNKNOWN. Slice-Ribbon CE: NO.**

`check_hfk_delta_law.py` -> `RESULTS.json`: **37/37**, spherogram 2.4.1, Szabo's
HFK calculator as bundled with SnapPy 3.3.2. Everything is recomputed from the
committed PD codes in `data/knots/`; nothing is transcribed.

`data/knots/AbeTagami_K_n_NOTES.json` recorded that no HFK data for the family
had been obtained, and the chat archive's correction register says "Invalid HFK
results remain unknown". This pass supplies the full bigraded table.

---

## 1. What is forced, and what is not

Lemma B of `research/33` proves that every invariant factoring through the
S-equivalence class of the Seifert matrix is *forced* to agree across the family.
The computation confirms that, and then shows exactly where the family does
separate.

| | `K_0` | `K_1` | `K_2` | `K_3` |
|---|---|---|---|---|
| total rank of `HFK-hat` | 13 | 13 | 13 | 13 |
| Seifert genus | 2 | 2 | 2 | 2 |
| fibered | yes | yes | yes | yes |
| `tau`, `nu`, `epsilon` | 0, 0, 0 | 0, 0, 0 | 0, 0, 0 | 0, 0, 0 |
| `delta = M - A` levels | `{0: 13}` | `{-2: 8, 0: 5}` | `{-6: 8, 0: 5}` | `{-12: 8, 0: 5}` |
| thin | **yes** | no | no | no |

Total rank 13 is the determinant, as it must be. The concordance package is
uniformly zero, as the repository already knew. The **`delta`-grading is the
thing that moves**, and it moves in a completely regular way.

## 2. The delta law

> **Observation D.** For `n = 0, 1, 2, 3` the `delta`-levels of `HFK-hat(K_n)`
> are `{0, -n(n+1)}`, with 5 generators on `delta = 0` and 8 on the lower level
> (13 = 5 + 8 for every `n`; for `n = 0` the two levels coincide and the knot is
> thin).

Two things make this worth recording rather than filing as a curiosity.

**It reproduces Oba's contact invariant.** `AbeTagami_K_n_NOTES.json` records
Abe-Tagami Remark B: `d_3(xi_n) = -n^2 - n + 3/2`. The `n`-dependence
`-n^2 - n = -n(n+1)` is exactly the lowest `delta`-level found here, computed by
a completely different route (Szabo's HFK calculator on a PD code recovered from
a Dehn filling, versus Oba's contact-geometric computation).

**It carries the right symmetry.** `-n(n+1)` is invariant under `n -> -1-n`, and
that involution is precisely the one behind `K_n = K_m` iff `n = m` or
`n + m = -1` - hence `K_{-1} = K_0 = 6_3` and `K_{-2} = K_1`. The check verifies
the invariance for `n` in `[-6, 6]`.

**What it does not do.** `delta` is not a concordance invariant, so Observation D
obstructs nothing. It distinguishes the `K_n` as *knots*, which was already known
from volume and from `d_3`. Do not report it as a concordance separation.

## 3. Two flagged risks, discharged

`research/opus_mixed_lift_review.md` is an external critique of the argument that
`K_1` is locally equivalent to the unknot in `CFK_UV` - the result that makes
"every ordinary Floer concordance invariant vanishes" true, and hence makes
`D_{0,1}` a live slice candidate at all. The critique lists five ways the
argument could fail. Two of them are checkable algebraic facts that the original
pass *asserted from its own calculator output*:

> **risk 4.** "`delta` in `{0,-2}` for all 13. This is what makes mixed arrows
> non-composable and `d^2 = 0` linear in the 18 unknowns. A single generator at
> `delta = -1` or `-4` breaks both the '18 slots' enumeration and the linearity,
> and `18 - 10 = 8` would no longer be the right dimension count."
>
> **risk 5.** "The count 18 itself is a derived fact from the `(A,M)` table,
> recomputable by hand."

Both now check out, recomputed here from the committed PD code:

* **risk 4 discharged.** The 13 generators sit at
  `(-2,-4), (-1,-3)x2, (-1,-1), (0,-2)x2, (0,0)x3, (1,-1)x2, (1,1), (2,0)`.
  Every one has `delta` equal to `0` (five of them) or `-2` (eight). No generator
  at `-1` or `-4`. Checks 3a, 3b.
* **risk 5 discharged, count exactly 18.** With `deg d = (0,-1)`,
  `deg U = (-1,-2)`, `deg V = (1,0)`, an entry `x -> U^a V^b y` forces
  `delta(y) = delta(x) - 1 + a + b`, so a jump of `+2` forces `a + b = 3`, and
  mixed (`a, b >= 1`) leaves only `U^2 V` and `U V^2`. Enumerating admissible
  `(x, y)` pairs gives **18**, matching the asserted count. Check 3c.
* The three bidegrees the stated chain retraction needs - two generators at
  `(0,0)`, one at `(-2,-4)`, one at `(2,0)` - all exist, with rank 3 available at
  `(0,0)`. Check 3d.

**What is still NOT discharged, and this matters.** The critique's risks 1 and 2
are that nothing establishes the calculator's absolute bigradings to be those of
the true `CFK_UV(K_1)`, and that the "independent" Python enumerator consumed the
same generator table. This pass uses **the same HFK engine family**, so it is a
re-derivation from the PD code, not an independent check of the engine's
grading conventions. Risk 3 (`d_pure^2 = 0` over `S`, not merely over `R`) is
untouched. Those three remain open exactly as stated.

## 4. The connected sums, and a live obstruction

| | `D_{0,1}` | `D_{0,2}` | `D_{1,2}` |
|---|---|---|---|
| total rank | 169 = 13^2 | 169 | 169 |
| fibered genus | 4 | 4 | 4 |
| `tau`, `nu`, `epsilon` | 0, 0, 0 | 0, 0, 0 | 0, 0, 0 |
| `delta` levels | `{0: 65, 2: 104}` | `{0: 65, 6: 104}` | `{-2: 40, 0: 25, 4: 64, 6: 40}` |
| thin | no | no | no |

`D_{0,1}` is **not thin**. That is worth stating plainly, because for a thin knot
with `tau = 0` the involutive invariants are pinned by the thin classification
and there would be nothing to compute. There is something to compute here. So:

> **The involutive route is live, not vacuous.** The vanishing recorded in this
> repository is for invariants factoring through the *ordinary* local
> equivalence class. `iota_K`, `d-bar`/`d-underline`, and the involutive local
> equivalence class of `D_{0,1}` are neither computed nor excluded, and the
> non-thinness means no shortcut kills them.

This is a target, not a result. It is also out of reach in this container: the
bundled HFK calculator returns bigraded *ranks* only, not `CFK^infinity` with its
differentials, and there is no Sage, flipper, curver or twister here. Computing
`iota_{D_{0,1}}` needs machinery this environment does not have.

## 5. Status ledger

| claim | status |
|---|---|
| `K_0 ~ K_1` | **UNKNOWN** |
| Slice-Ribbon counterexample | **NO** |
| bigraded `HFK-hat` of `K_0..K_3`, `D_{0,1}`, `D_{0,2}`, `D_{1,2}` | **COMPUTATIONALLY VERIFIED**, 37/37 |
| Observation D: `delta`-levels of `K_n` are `{0, -n(n+1)}` | **VERIFIED for n = 0,1,2,3**; not a proof for all `n` |
| `delta` law matches the `n`-dependence of Oba's `d_3(xi_n)` | **OBSERVED**, two independent routes agree |
| risk 4 (`delta in {0,-2}`) of the local-equivalence argument | **DISCHARGED** |
| risk 5 (18 mixed slots) | **DISCHARGED** |
| risks 1, 2 (calculator absolute bigradings) | **STILL OPEN** - same engine family used here |
| risk 3 (`d_pure^2 = 0` over `S`) | **STILL OPEN** |
| involutive invariants of `D_{0,1}` | **NOT COMPUTED**, and non-thinness keeps them live |

## Reproduce

```
python3 check_hfk_delta_law.py     # ~2 min, exit 0
```

Needs `spherogram` (SnapPy). Reads seven PD codes from `data/knots/`. No network.
