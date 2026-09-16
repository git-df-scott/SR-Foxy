# Pre-registration: `s` on the Turaev Theorem I knots

Written **before** the run. Decision rules fixed and not to be retuned.

## Why these knots

`ERRATA_2026-09-11.md` E1 upgraded Turaev's Theorem I from closed to **live**:
Theorem H(ii) obstructs *homotopy*-ribbonness (it is proved via π₁-surjectivity),
and Theorem J says H gives **no** sliceness obstruction. So a Theorem I knot is
algebraically slice, **provably not homotopy-ribbon** — hence not handle-ribbon and
not ribbon — and its smooth sliceness is open. **Any Theorem I knot that is
smoothly slice is a counterexample to Slice-Ribbon outright.**

`research/24` §1 lists three route-B certificates and does not include this one.
It is a fourth, and unlike the other three it does **not** require a concordance
coincidence between distinct fibered knots: it needs one knot to be slice.

Measured today (`results/fox_milnor_audit_2026-09-16.json`), `Turaev_A_1_1_0_0`:
27 crossings, genus 3, non-fibered, `τ = 0`, `ε = 0`, `det = 1`,
`Δ = t^6 - 3t^5 - t^4 + 7t^3 - t^2 - 3t + 1`, Fox–Milnor **passes**. So every
classical obstruction vanishes and `τ`/`ε` give nothing. `s` is the next tool, and
at 27 crossings it is cheap — the failures in `UNFINISHED.md` §3 were at 47.

## The test

`s(K)` via the source-built KnotJob (`javac 21`; the distributed jar needs Java 23).
Flags `-s0 -s2`, `-Xmx6g`. Targets: all five stored `Turaev_A_*` knots.

## Controls, not optional

The same build, same session, same flags: `s(+3_1) = +2`, `s(-3_1) = -2`,
`s(4_1) = 0`, `s(6_1) = 0`. **If any control misses, every Turaev row is void**
and is reported as void, not as a negative.

## Decision rules, fixed in advance

1. `s(K) ≠ 0` ⟹ `K` is **not smoothly slice** (Rasmussen: `|s| ≤ 2g_4`). That
   **kills** that knot as a counterexample candidate. A real, reportable negative.
2. `s(K) = 0` is **no obstruction and no evidence of sliceness.** The knot merely
   survives. It does **not** become "probably slice", and the campaign does not get
   to call it progress.
3. A run that does not print a value is a resource failure, reported as such.
4. Whatever happens, this says nothing about the non-homotopy-ribbon certificate,
   which is a separate claim from `ERRATA` E1 that this run does not audit. Before
   any Turaev knot is promoted in `CANDIDATE_LEDGER.md`, that certificate must be
   checked against Turaev's Theorem I hypotheses **on these specific stored knots**
   — `research/08` recovers the construction but I have not verified today that the
   stored `A(p,q,r,s)` realise it.

## Prior, stated in advance

`s = 0` on all five is the likely outcome: these are algebraically slice knots with
`τ = ε = 0`, and `s` agrees with `2τ` on most small knots. A nonzero `s` would be
the informative surprise.
