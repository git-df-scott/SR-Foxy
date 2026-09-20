# Eisermann's Theorem 2 is a single bit in the regime `L_{3,1}` lives in

19 September 2026, Opus. **CE: NO.** One refuted hypothesis, one structural
finding, and a sharpened form of the pre-registered `L_{3,1}` test.

---

## 1. The hypothesis I was testing, and its refutation

`research/31` shows Theorem 2 has teeth at `lk = 0` (22 of 41 testable links
violate) and concludes the `L_{3,1}` test can fire. I suspected that conclusion
sat in the wrong regime, for the same reason `research/31` itself caught
`research/22` on: **Fox-Milnor forces a ribbon knot's determinant to be a
perfect square**, `det = f(-1)^2`. So a link whose component determinants
multiply to a non-square cannot be ribbon for a reason having nothing to do
with how its components are linked — some component is not even a ribbon knot.
`L_{3,1}` has components `Q` and `V_3` with `det = 9` each, both squares.

If every violation had a non-square product, the teeth would be an artifact and
the whole lane would be dead.

**Refuted.** Over 439 testable links (2 components, `lk = 0`, `null V = 1`,
tabulated hyperbolic links), **61 violations have a square product**, and
**55 have every component determinant individually a square** — including
`det` profiles `[1,9]` and `[1,25]`, the shape of `L_{3,1}`'s `[9,9]`. Examples:
`L14n9390`, `L14n9446` (`dets [1,9]`, `det V = 25 mod 32`, predicted 9);
`L14n10461`, `L14n11214` (`dets [1,25]`, `det V = 9`, predicted 25).

`research/31`'s conclusion stands, now on a population ten times larger and in
the right regime. The lane survives.

## 2. What the refutation exposed

Restrict to the 189 links where **every** component determinant is a perfect
square — i.e. every component passes Fox-Milnor and could be a ribbon knot,
which is the regime `L_{3,1}` is in. Then:

| `(det V - prod det K_i) mod 32` | count |
|---|---|
| **0** | 134 |
| **16** | 55 |
| anything else | **0** |

Equivalently: **`det V = prod det(K_i) (mod 16)` on all 189**, and modulo 32 the
only freedom is a single bit.

The contrast is sharp. On the 250 links with a non-square component determinant
the difference takes the values `0, 2, 10, 16, 18, 26`, and the mod-16 statement
fails.

**Status: numerically supported, not proved.** n = 189, exact integer
arithmetic (no floating point enters `det V`), over SnapPy's tabulated
hyperbolic 2-cusped links, `lk = 0`, `null V = 1`. It is a conjecture about that
population, not a theorem, and I have no proof of the mod-16 half.

## 3. The consequence: the `L_{3,1}` test is one bit, and it self-checks

`research/22` §3.3 pre-registers:

> if `L_{3,1}` is ribbon then `det V(L_{3,1}) = 81 = 17 (mod 32)`; a different
> residue makes it slice and not ribbon.

"A different residue" is too loose. If §2 holds, the components of `L_{3,1}`
having square determinants forces `det V` into exactly two classes:

| `det V(L_{3,1}) mod 32` | meaning |
|---|---|
| **17** | consistent with ribbon; Theorem 2 does not fire |
| **1** | `= 17 + 16`. **Theorem 2 fires: `L_{3,1}` is slice and not ribbon** |
| anything else | **a discrepancy to investigate** — see the caveat below |

That third row is the point. The pre-registration as written treats every
non-17 residue as a counterexample, so a mistraced diagram returning, say, 13
would read as the headline result. Under §2 a residue of 13 is far more likely a
construction or tool error than a counterexample.

**But §2 is an empirical rule over 189 examples, not a theorem, and it must be
falsified rather than assumed.** An unexpected residue is a *discrepancy to
investigate*, not automatically a bug: it could equally be a counterexample to
§2's mod-16 rule, which would itself be worth knowing. Treating row three as
"bug" by reflex would convert this note from a control into a way of discarding
inconvenient data, which is the failure mode this repository exists to avoid.

A second limit: square determinant is only **one necessary consequence** of
Fox-Milnor, not the full factorisation condition `Delta(t) = f(t) f(1/t)`. The
189-link population was selected by the square test alone, so it contains links
whose components fail Fox-Milnor in ways the selection did not see.

It also prices the lane honestly: accidental agreement is a coin flip, not
1-in-32. Among the 189, 134/189 = 71% satisfy the congruence anyway. So a
returned 17 is weak evidence of ribbonness, while a returned 1 is the
counterexample.

## 4. Controls

`L_{0,1}` (built in `results/opus_2026_09_19_session_L11_built`, and
**retracted there as a claimed `L_{1,1}`** -- it is `L10n36`, certified ribbon)
is a known-ribbon member of this family: `dets [9,1]`, `det V = -23 = 9
(mod 32)`, difference 0. It sits in the `0` row, as a ribbon link must.

The five-hour GST campaign's reconstructions are also all consistent with §2:
`n=1` `det V = 73 = 9 (mod 32)` against product 9; `n=2` `det V = -143 = 17`
against 17; `n=3` `det V = 241 = 17` against 17. Difference 0 in every case.

The whole `RibbonLinks` census (12,184 links, all ribbon) has difference 0 by
construction of the test, and separately shows every component determinant there
is an odd perfect square — 1, 9, 25, 49, 81, ..., 961 — which is Fox-Milnor
visible in the data.

## 5. A correction worth recording

Eisermann's identity is **only ever a congruence**. Of the 12,184 certified
ribbon links, exact equality `det V = prod det(K_i)` holds for **176**, i.e.
1.4%; every one of the 12,008 differences is divisible by 32. Primary source
re-read to settle it (arXiv:0802.2287 abstract): "every ribbon link `L`
satisfies `det V(L) = det(K_1)...det(K_n)` modulo 32".

This matters because a reader who remembers the theorem as an exact equality —
as I initially did — will reject a correct construction. `L_{1,1}` returns
`det V = -23` against a product of 9, which looks like a failure and is not.

## 6. Reproduce

```
python teeth2.py     # writes teeth_rows.json, the 439-link population
```
in `results/opus_2026_09_19_session_L11_built/`. Needs snappy + spherogram, no Sage.
