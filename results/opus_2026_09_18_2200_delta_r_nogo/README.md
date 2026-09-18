# The `Delta_r` family cannot carry a Miyazaki non-ribbon certificate

18 September 2026, Opus night session. **CE: NO.**
**Smooth concordance `K_0 ~ K_1`: UNKNOWN. Slice-Ribbon CE: NO.**

Astra's two 18 September passes both close with the same suggestion: pursue "a
geometric slice certificate plus an independent nonribbon obstruction for the new
`Delta_r` family". This note verifies their algebra independently and then shows
the second half of that suggestion is unreachable by the only non-ribbon theorem
this campaign has.

`check_delta_r_nogo.py` -> `RESULTS.json`. sympy 1.14.0, no network.

---

## 1. Astra's algebra, independently reproduced

From `results/astra_2026_09_18_local_band_no_go/` and
`results/astra_2026_09_18_dual_path_frontier/`, recomputed here from scratch:

| claim | status |
|---|---|
| `Delta_r = Delta^2 - r^2 t^2 (t^2-1)^2` equals `f_r(t) t^4 f_r(1/t)`, `f_r = Delta + r(t^3-t)` | **VERIFIED** identically in `Z[r,t]` |
| the dual-path survivors' polynomial equals `Delta_1` | **VERIFIED** exactly |
| `det = |Delta_r(-1)| = 169` for every `r` | **VERIFIED**; `f_r(-1) = 13` for every `r` |
| `f_r` irreducible over `Q` | **VERIFIED** for `r` in `[-6, 6]` |
| `Delta_r` symmetric | **VERIFIED** |

So two independent searches - 16 over/under choices on fixed paths, and 88 + 2839
dual-path assignments - converge on the same boundary family. That is the
construction's actual output, not a near miss.

## 2. The structural obstruction

> **Proposition N.** Let `B_r` be a knot with `Delta_{B_r} = Delta_r`, `r != 0`.
> Then Miyazaki's Theorem 5.5 cannot certify `B_r` non-homotopy-ribbon.

*Proof.* Write `*` for the degree-4 reciprocal `p -> t^4 p(1/t)`, the involution
under which "symmetric" means fixed. Then `Delta^* = Delta` and `(t^3-t)^* =
-(t^3-t)`, so `f_r^* = Delta - r(t^3-t)` and `f_r` is **not** fixed for `r != 0`; `f_r` and `f_r^*`
are therefore non-associate, and both are irreducible (verified for
`r` in `[-6,6]`; irreducibility of `f_r^*` follows from that of `f_r`). So the
irreducible factorisation of `Delta_r` is exactly `f_r * f_r^*`.

A connected sum `J # J'` has `Delta = Delta_J * Delta_{J'}` with **each factor
symmetric**. A symmetric divisor of `Delta_r` must be the product of a
reciprocal-**closed** subset of `{f_r, f_r^*}`, i.e. of `{}` or of the whole set.
Hence `Delta_J = 1` or `Delta_J = Delta_r`. A fibered knot with trivial Alexander
polynomial is the unknot, so `B_r` has **at most one** nontrivial fibered prime
summand: `n = 1` in Theorem 5.5.

With `n = 1` the index set `{1}` admits no pairing, so the theorem's conclusion is
unsatisfiable and it *would* return non-homotopy-ribbon - but only if that summand
satisfies one of its two alternatives.

* **Alternative 2** ("there is no `f` in `Z[t] \ {+-t^k}` with `f(t)f(t^{-1}) |
  Delta`") **fails by construction**: `Delta_r` *is* the norm `f_r f_r^*`, and
  `f_r` is not a unit.
* **Alternative 1** (minimality with respect to `>=` among fibered knots in
  homology spheres) is incompatible with the goal. If `B_r` is slice via a
  homotopy-ribbon disk then `U <=_h B_r`, which is exactly a failure of
  minimality; and if `B_r` is slice via a disk that is *not* homotopy-ribbon,
  that is the counterexample itself and needs no Miyazaki certificate.

Neither alternative is available, so Theorem 5.5 does not apply. []

## 3. Why this is structural, not an accident of these bands

Fox-Milnor and Miyazaki's second alternative are in **direct tension**:

* Fox-Milnor: `K` slice `=>` `Delta_K = f(t) f(t^{-1})`.
* Miyazaki alt. 2: no such `f` exists.

A knot satisfying alternative 2 with `Delta != 1` is therefore **not slice**, and
its non-ribbon certificate is vacuous for a counterexample hunt. Being a norm is
simultaneously what permits sliceness and what destroys this certificate.

This is exactly why the campaign's target is a **connected sum of at least two**
prime fibered summands. `D_{0,1} = K_0 # (-K_1)` has `Delta = Delta^2`, a norm at
the level of the sum, while each *summand* separately carries the irreducible
`Delta` and so satisfies alternative 2. The alternatives are tested on the
summands; Fox-Milnor is tested on the sum. That separation is the whole mechanism.

**Consequence for the band redesign.** Drifting off `Delta^2` is not a near miss
to be repaired by a better path - it loses the only non-ribbon certificate
available. `Delta_r` for `r != 0` is a norm whose two irreducible factors are
swapped by the reciprocal involution, so it can never be split into two
**symmetric** pieces, and therefore can never present the two-summand shape that
Miyazaki needs.

> **Hard gate for any redesigned band pair.** The surgery Alexander polynomial
> must be `Delta^2` exactly, i.e. `r = 0` in the family above. A design producing
> any `Delta_r` with `r != 0` is not a partial success and must not be reported as
> trace-survivor progress.

This does not exclude a non-ribbon certificate for `B_r` from some *other*
theorem, and none is claimed. It excludes Miyazaki, which is the only one this
campaign has been able to apply.

## 4. Limits

* This is a statement about Alexander polynomials, hence about **necessary**
  conditions. It proves nothing about whether any `B_r` is slice, and constructs
  no disk and no obstruction.
* Irreducibility of `f_r` is verified for `|r| <= 6`, not proved for all `r`. The
  symmetry argument itself needs only that `f_r` is not symmetric, which holds for
  all `r != 0` by the palindromic/anti-palindromic split.
* `B_r` is not identified as a knot anywhere. Astra's own report states the
  boundary identification timed out; matching a polynomial is not a knot.
* Miyazaki 5.5 is quoted from `ERRATA_2026-09-16.md`, which transcribes it from
  Abe-Tagami Appendix A. The quantifier correction recorded there (the alternative
  is required of **every** summand) is used as stated.

## Reproduce

```
python3 check_delta_r_nogo.py      # exit 0
```
