# The `K_1` identification, upgraded off `is_isometric_to`

19 September 2026, Opus. **CE: NO.**
**Smooth concordance `K_0 ~ K_1`: UNKNOWN. Slice-Ribbon CE: NO.**

`check_k1_identification.py` -> `RESULTS.json`, **7/7**, SnapPy 3.3.2 /
spherogram 2.4.1. No network.

---

## 1. The dependency this closes

`results/opus_2026_09_19_0000_geometry_free_certificate/` made the Abe-Tagami
**non-ribbon** certificate combinatorial — prime, fibered, distinct and
irreducible `Delta`, all without geometry — and named the one thing left standing
on a numerical call:

> the stored `K_1` PD code is identified with `A_1(6_3)` only through the
> construction card's Dehn filling, checked with `is_isometric_to`.

That is the weakest call in the lane. `is_isometric_to` has failed this campaign
twice in one night: it throws on closed manifolds (`RuntimeError: the SnapPea
kernel was not able to determine ...`), and a possibly-numerical `False` was
nearly recorded as a certified exclusion.

## 2. What replaces it

The **oriented isometry signature**, computed from the **canonical
retriangulation**. Two points matter:

* it is *not* the `isoSig`-after-random-`simplify()` method retracted in
  `research/34` — that signature was canonical for a *triangulation*; this one
  depends only on the isometry type, so equal signature means isometric;
* `ignore_orientation=False` is **mandatory**. The default returns the
  **unoriented** invariant and gives a manifold and its mirror byte-identical
  signatures — the bug that silently corrupted four shards here earlier tonight.

## 3. Result, with the control first

| object | oriented isometry signature |
|---|---|
| stored `K_0` | `gLLPQccdefffhggaacv` |
| **L filled at `n=0`: `(1,0), (-1,0)`** | `gLLPQccdefffhggaacv` — **matches `K_0`** |
| stored `K_1` | `mvLLLPPQQcdjhkilikilklwrqunrlrkcawm` |
| **L filled at `n=1`: `(2,1), (0,1)`** | `mvLLLPPQQcdjhkilikilklwrqunrlrkcawm` — **matches `K_1`** |

**The `n = 0` control is the point of the exercise.** The zero-fold annulus twist
is the identity, so filling `L` at `(1,0), (-1,0)` must return `6_3`. It does.
Had that failed, the `n = 1` agreement would have meant nothing — which is
exactly the trap a bare `is_isometric_to` "true" walks into.

By Gordon-Luecke a knot in `S^3` is determined by its complement, so an oriented
isometry of exteriors identifies the knots.

## 4. Residual gap, recorded not hidden

`isometry_signature(verified=True)` **raises `SageNotAvailable`** in this
container, so the canonical retriangulation is found numerically. This is a
**high-confidence identification, not a proof**. Rerunning inside Sage with
`verified=True` would close it, and that is a five-minute job for anyone who has
Sage.

The upstream dependency also stands: the PD code of `L` itself is taken as
committed, and nothing here re-derives it from Abe-Tagami's figures.

## 5. Where the lane now stands

| half of the Abe-Tagami counterexample | status |
|---|---|
| `D_{0,1}` is **not ribbon** | certified combinatorially — no geometry anywhere |
| `K_1` really is `A_1(6_3)` | oriented canonical signature, control passes; numerical only in the sense of §4 |
| `D_{0,1}` is **slice** | **MISSING.** No construction. |

Nothing here bears on the missing half.

## Reproduce

```
python3 check_k1_identification.py    # exit 0
```
