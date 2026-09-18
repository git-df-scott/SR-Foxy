# The Manolescu-Piccirillo RBG lane is empty for both available certificates

19 September 2026, Opus. **CE: NO.**
**Smooth concordance `K_0 ~ K_1`: UNKNOWN. Slice-Ribbon CE: NO.**

`check_mp_rbg.py` -> `RESULTS.json`, **24/24**, spherogram 2.4.1. No network.

---

## 1. The lane, and the question it left open

`research/24` §4 identifies the sharpest counterexample generator on the board:
an `r = 0` super-special RBG pair `(K_B, K_G)` has **diffeomorphic 0-traces**, so
a ribbon disk for one certifies the *other* slice, and if that other side carries
a non-ribbon certificate the pair is a counterexample —

> "with no concordance coincidence needed anywhere."

It then asks whether the lane is live or "empty for a stupid reason", observes
that the four `r = 0` knots then in `data/knots/` all have `Delta = 1` (so no
fibered knot among them but the unknot), and concludes:

> "So the lane is live, and **empty only of the examples we happen to have
> built**."

## 2. The new input

Gukov-Halverson-Manolescu-Ruehle, *Searching for Ribbons with Machine Learning*
(<https://web.stanford.edu/~cm5/sliceML.pdf>), §6, report the **exhaustion** of
Manolescu-Piccirillo's 3375-pair RBG family: 2522 pairs shown non-slice, 843
shown ribbon by their Bayesian-optimised random walker, 5 more resolved by other
methods — leaving exactly **five pairs, ten knots**, whose ribbon status is
unknown. They name them, and observe that the three with `r = 0`,

```
K_{B/G}(0,0,0,1,2,-1),   K_{B/G}(0,0,0,-1,2,1),   K_{B/G}(0,0,-2,0,0,1)
```

cannot give SPC4 counterexamples but **"might produce counterexamples to the
Slice-Ribbon Conjecture"** — `research/24`'s lane, with the candidates named.

All ten are already committed here as `data/knots/MP_KB_*`, `MP_KG_*`.

## 3. Result

| | |
|---|---|
| ten MP/RBG survivors present | yes |
| **fibered** | **none — all ten** |
| `tau = nu = epsilon` | `0` for all ten |
| `Delta = 1` | all six `r = 0` knots; the four `r != 0` knots have `Delta != 1` |

> **Both non-ribbon certificates this campaign can apply — Miyazaki Thm 5.5 and
> Hom-Park Thm 1.1 — quantify over FIBERED knots. Every surviving MP candidate is
> non-fibered. Neither can reach any of them.**

So `research/24` §4's lane is empty **across the whole Manolescu-Piccirillo
family**, not merely across the examples previously built — which is the stronger
statement its closing sentence left open. The `r = 0` candidates would collapse
twice over: `Delta = 1` means even a fibered one would be the unknot.

## 4. What this does NOT show

* It does **not** show any of the ten is ribbon, non-ribbon, or slice. `tau`,
  `nu` and `epsilon` all vanish, so no Floer obstruction to sliceness is found
  here either. **All ten remain open**, exactly as GHMR leave them.
* It considers only the two non-ribbon certificates this campaign can apply.
  Another theorem could still reach them — GHMR say the same: "there is a
  complementary challenge of finding new powerful obstructions."
* The PD codes are taken from `data/knots/` as committed and are not re-derived
  from Manolescu-Piccirillo's construction.

## 5. Where that leaves the board

The `r = 0` RBG generator was attractive precisely because it needs no
concordance coincidence — it manufactures a slice knot from a ribbon partner.
It is now closed for want of a certificate, not for want of slice knots. That
puts it in the same place as KDG: **the missing piece is M1, a ribbon-only
obstruction**, and the count of concrete knots waiting on M1 has just gone from
one to eleven.

## Reproduce

```
python3 check_mp_rbg.py     # exit 0
```
