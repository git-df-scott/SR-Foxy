# The GST lane: the knot is dead for the usual reason, and the link test has a
# known-answer calibration nobody has used

19 September 2026, Opus. **CE: NO.** A thinking note with one small computation.

---

## 1. `B_{3,1}` cannot be reached, and it is the third shortlist killed the same way

GST Figure 2 is *"a slice knot that might not be ribbon"* — exactly the shape of a
counterexample. GST prove it slice; nobody can prove it non-ribbon.

The stored object (`data/knots/GST_knot.json`, from `regina.ExampleLink.gst()`,
48 crossings, reconciled in `research/27` §2) computes as:

| | |
|---|---|
| Seifert genus | 10 |
| **fibered** | **NO** (HFK) |
| `deg Delta` | 16 `< 2g = 20` |
| `tau = nu = eps` | 0 |
| `det` | 1 |

**Both non-ribbon certificates this repository can apply quantify over fibered
knots**, so neither Miyazaki Thm 5.5 nor Hom-Park Thm 1.1 reaches `B_{3,1}`.
Eisermann's Theorem 2 degenerates for a knot to `det ≡ 1 (mod 8)`, and `det = 1`
satisfies it. Nothing fires.

That is now the **third** independent field shortlist closed for the identical
reason, and the pattern deserves naming:

| shortlist | size | fibered? | source |
|---|---|---|---|
| Manolescu-Piccirillo RBG survivors | 10 | **none** | `results/opus_2026_09_19_0100_mp_rbg_lane` |
| Dunfield-Gong unresolved, `<= 14` crossings | 16 | **none** | `research/50` §3 |
| **GST `B_{3,1}`** | 1 | **no** | here |

The field's own candidate lists are built from the population our certificates
cannot see. That is the `KDG`-side wall stated as sharply as this campaign can
state it, and no amount of searching moves it.

## 2. So the only live GST route is the LINK, and it always was

`research/22` §3.3 pre-registers the whole test as one congruence. Eisermann's
Theorem 2 is **ribbon-only as proved** and, per `research/31`, has teeth at
linking number 0 — which is where `L_{3,1}` lives:

> if `L_{3,1}` is ribbon then `det V(L_{3,1}) ≡ det(Q) · det(V_3) (mod 32)`.

A different residue makes `L_{3,1}` **slice and not ribbon** — the first such
object of any kind.

The blocker has never moved: `L_{3,1}` is a picture, not a combinatorial
description. `research/27` made the figures readable; tracing ~36 crossings from
a raster was judged too risky because **a mistrace yields a false
counterexample, the worst available outcome**, and three attempts to recover the
link as a band fission of `B_{3,1}` were rejected.

## 3. The observation: `L_{2,1}` is a known-answer control at the *same* residue

`V_n = T_{n,n+1} # mirror(T_{n,n+1})` and `Q = 3_1 # (-3_1)`. Determinants are
multiplicative under connected sum, so (computed here, `det(3_1) = det(8_19) = 3`):

| link | `det(Q)` | `det(V_n)` | product | **predicted residue mod 32** | ribbon status |
|---|---|---|---|---|---|
| `L_{1,1}` (18 cr) | 9 | 1 (`V_1` unknot) | 9 | **9** | **known ribbon** [GST] |
| `L_{2,1}` (40 cr) | 9 | 9 (`T_{2,3} # -T_{2,3}`) | 81 | **17** | **known ribbon** [GST] |
| `L_{3,1}` | 9 | 9 (`T_{3,4} # -T_{3,4}`, `T_{3,4} = 8_19`) | 81 | **17** | **UNKNOWN** |

> **`L_{2,1}` is known ribbon and is tested against the identical residue,
> 17 mod 32, that `L_{3,1}` is tested against.**

That has not been written down here, and it changes the risk calculus that has
blocked this lane for the whole campaign. The standing objection is that an
isolated `det V(L_{3,1})` computed from a hand-traced diagram cannot be trusted:
a tracing slip, a mirror convention, or a normalisation of `V` at the wrong
fourth root of unity all produce a wrong residue that **looks exactly like a
counterexample**.

With `L_{2,1}` in hand that stops being true. It is the same construction, the
same components up to `n`, the same linking number, the same predicted residue —
and the answer is known in advance. A pipeline that returns **17 on `L_{2,1}`**
and something else on `L_{3,1}` has been calibrated on the exact quantity in
dispute. A pipeline that misses on `L_{2,1}` is broken, and says nothing about
`L_{3,1}`.

`L_{1,1}` at 18 crossings is the cheaper first rung, and its residue **9** is
distinct from 17, so it independently pins the normalisation rather than merely
agreeing by coincidence.

## 4. What to do with this

The task is no longer "trace `L_{3,1}` and hope". It is:

1. Build `L_{1,1}` (18 crossings — the smallest object in the family, and GHMR
   note their own programs failed to find its bands even though it **is**
   ribbon, so it is well documented).
2. Run the Eisermann pipeline. **It must return 9 mod 32.** If not, stop: the
   pipeline is wrong, not the mathematics.
3. Build `L_{2,1}` (40 crossings). **It must return 17 mod 32** — the disputed
   residue, on a known-ribbon object.
4. Only then trace `L_{3,1}`, with `research/22` §3.3's verification protocol
   (two components identified as `Q` and `V_3`, linking number 0, band sum
   reproducing `B_{3,1}`) still required on top.

Steps 1-3 are risk-free: every answer is known in advance, so they can only
expose a broken tool, never manufacture a false positive. **None of them has
been attempted.** That is the cheapest genuinely-unblocking work left on this
board, and unlike the band searches it is not a lottery — the objects are
specified, the answers are pre-registered, and a failure at any step is
informative.

*Caveat kept from `research/22`: a slice non-ribbon **link** does not literally
refute the Slice-Ribbon Conjecture, which is stated for knots. It would be the
first slice non-ribbon object of any kind, and it would make `B_{3,1}` the
immediate next target.*
