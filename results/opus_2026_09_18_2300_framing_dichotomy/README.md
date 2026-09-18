# The framing dichotomy: why no mixed-band design can produce `D_{0,1}`

> **Audit correction, 18 September 2026:** the universal corollary below is unsupported. The existing 0110 band choice has the same zero linking but the target polynomial at r=1, independently reproduced in [the new audit](../../research/36_audit_of_framing_and_miyazaki_closures.md). It still fails its own group gate; it is not a counterexample. The old raw RESULTS.json records arithmetic and does not certify the claimed universal theorem.


18 September 2026, Opus night session. **CE: NO.**
**Smooth concordance `K_0 ~ K_1`: UNKNOWN. Slice-Ribbon CE: NO.**

The handoff's selected experiment is a joint redesign of the two mixed bands, and
it requires writing down the proposed local cancellation *before* enumerating.
Doing that turns up a reason no enumeration in this family can succeed.

`check_framing_dichotomy.py` -> `RESULTS.json`, 12/12, sympy 1.14.0, no network.

---

## 1. The obstruction

The marked double's linking matrix is committed in
`data/knots/AbeTagami_marked_product_scaffold.json`:

|  | `R` | `c1_upper` | `c2_upper` | `c1_lower` | `c2_lower` |
|---|---|---|---|---|---|
| `R` | 0 | 0 | 0 | 0 | 0 |
| `c1_upper` | 0 | 0 | **+1** | 0 | 0 |
| `c2_upper` | 0 | +1 | 0 | 0 | 0 |
| `c1_lower` | 0 | 0 | 0 | 0 | **-1** |
| `c2_lower` | 0 | 0 | 0 | -1 | 0 |

The lower copy is **mirrored** — that is what makes the double a product disk for
`K_0 # (-K_0)` — so its linking is `-1` where the upper's is `+1`, and every
upper-lower cross term vanishes.

> **Proposition L.** Let `eta_1` and `eta_2` be obtained by band-summing one
> upper marked circle to one lower marked circle, in either pairing. Then
> `lk(eta_1, eta_2) = 0`.

*Proof.* Linking number is bilinear on homology classes, and a band sum adds
them: if `eta_1` is a band sum of `a` and `b`, both disjoint from `eta_2`, then
`[eta_1] = [a] + [b]` in `H_1(S^3 - eta_2)`, so
`lk(eta_1, eta_2) = lk(a, eta_2) + lk(b, eta_2)`. Crossed:
`1 + 0 + 0 + (-1) = 0`. Uncrossed: `1 + 0 + 0 + (-1) = 0`. []

**Nothing in the band design can change this.** Band paths, endpoints, over/under
choices and internal twists all leave homology classes alone. This is why Astra's
16 over/under choices, 88 short dual paths and 2839 expanded assignments *all*
reported zero pairwise linking — it was forced, not observed.

## 2. Why that kills the target

An annulus `A` with `dA = eta_1 u eta_2` induces the framing `lk(eta_1, eta_2)` on
its boundary. Framing `0` means the annulus twist is `+1/r` and `-1/r` surgery,
i.e. slopes `(1,r)` and `(-1,r)`. That is exactly the convention in Astra's
`check_all_surgeries.py`, whose two extra Fox rows are `r*longitude +- 1*meridian`.

Abe-Tagami's annulus `A~` has `lk(c'_1, c'_2) = +1`, so its `n`-fold twist is
`1 + 1/n` and `1 - 1/n`, slopes `(n+1, n)` and `(n-1, n)` — the committed
construction card, `(2,1)` and `(0,1)` at `n = 1`.

**The mixed-band construction implements the wrong twist.** Astra's

```
Delta_r = Delta^2 - r^2 t^2 (t^2-1)^2 = Delta^2 - r^2 (t^3 - t)^2
```

is the polynomial signature of that framing mismatch, and it equals the target
`Delta^2` **only at `r = 0`** — the meridional filling, i.e. no twist at all,
whose boundary is `K_0 # (-K_0)`, which is ribbon.

> **Corollary.** No mixed-band design whatsoever — any paths, endpoints,
> over/unders or twists — produces `D_{0,1}`. At the twist parameter the target
> needs, the polynomial is wrong; at the parameter giving the right polynomial,
> there is no twist.

This explains, rather than merely reproducing, Astra's "all-parameter target
incompatibility". Their proof covers their family by a 55-pivot Fox reduction;
Proposition L says why, and extends it to every band design in the mixed
configuration.

## 3. The dichotomy

| axes | framing | status |
|---|---|---|
| **same half** (`c1_lower`-`c2_lower`, or upper) | `-1` / `+1` — **correct** | obstructed: the `SL(2,F_5)` certificate shows the axes are non-conjugate even up to inversion |
| **mixed** (one upper, one lower) | `0` — **wrong** | escapes the conjugacy gate, but the boundary polynomial cannot be the target |

The mixed pairing was introduced precisely to escape the fixed-axis conjugacy
obstruction. It does escape it, and pays for it with the framing. Each side of the
lane fails for the opposite reason, which is a complete account of why this
program has not closed.

## 4. What a redesign would have to do

Proposition L assumes only that the axes are **band sums of the four marked
circles**. So the escape routes are:

1. **Axes outside that span.** Curves not homologous to sums of the marked
   circles — for instance curves linking `R`, or curves crossing the seam. Every
   axis tested so far lies in the span, so this is untested rather than excluded.
   This is the one live direction.
2. **A non-mirrored double.** The mirror is what makes the boundary
   `K_0 # (-K_0)`; removing it changes the disk and the target, so this is not a
   repair of the present construction.
3. **Accept framing `0` and certify `B_r` non-ribbon by other means.** Excluded
   for Miyazaki by `results/opus_2026_09_18_2200_delta_r_nogo/` (Proposition N):
   `Delta_r` is a norm `f_r f_r^*` whose factors are swapped by the reciprocal
   involution, so it can never present the two-symmetric-summand shape Miyazaki
   requires. No other applicable non-ribbon theorem is known to this campaign.

**Recommendation.** Do not enumerate further mixed-band designs. Direction 1 is
the only one of the three that is open, and it changes the axes rather than the
bands, so it is a different experiment from the one the handoff selected.

## 5. Limits

* Proposition L is about **linking numbers**, hence necessary conditions. It
  constructs nothing and obstructs no disk.
* It says nothing about axes that are not band sums of the four marked circles.
* No knot is identified here; `B_r` remains unidentified, as Astra also records.
* The `SL(2,F_5)` fixed-axis obstruction is quoted from the existing certificate,
  not re-derived from the PD.

## Reproduce

```
python3 check_framing_dichotomy.py     # exit 0
```
