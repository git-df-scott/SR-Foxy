# Independent audit of the stored HFK absolute bigradings — IN PROGRESS

19 September 2026, Opus. **CE: NO.** This is an audit, not a search.

## Why this and not more searching

The band searches and the random walker are lotteries. `research/51` says why:
the lane needs a *construction*, and every construction that gives concordance
for free loses fiberedness. Feeding more compute to a lottery is activity, not
progress.

This is the decisive task instead, and `ERRATA_2026-09-18_OPUS.md` E18-7 already
named it as the cheap one.

## The consequence nobody propagated

`research/11` concludes `K_0` and `K_1` have the **same involutive knot-Floer
local-equivalence class**. Local equivalence classes form a **group**, so
`[K_0] = [K_1]` gives `[K_0] - [K_1] = 0`:

> `D_{0,1} = K_0 # (-K_1)` is involutively locally **trivial**, and every
> involutive concordance invariant vanishes on it.

So `HANDOFF_2026_09_18_OPUS.md` **P4** — *"Involutive Heegaard Floer on
`D_{0,1}`. Live and uncomputed ... A non-vanishing involutive obstruction would
kill the AT lane"* — is already answered **NO**. It is not a live lane. The plan
still lists it as one, and `PLAN_CE` P5 did too until E18-7.

## The one condition the chain rests on

`research/opus_mixed_lift_review.md` risk 1/2, still recorded **OPEN** in
`results/opus_2026_09_18_0040_hfk_delta_law/README.md`:

> "Nothing in the argument establishes that `C_calc` is the `UV=0` reduction of
> the true `CFK_UV(K_1)` **with correct absolute bigradings**. A uniform grading
> shift is harmless; a **relative** grading error is fatal, because it changes
> which pairs admit a mixed monomial. A convention mismatch (mirror, or
> `U <-> V`) would silently swap `alpha <-> beta`."

It stayed open for one reason: **every recomputation used the same engine
family**, so nothing was independent. `opus_2026_09_18_0040`'s own table records
risks 1 and 2 as "STILL OPEN - same engine family used here".

## What this audit does differently: no Floer code at all

1. **Graded Euler characteristic.**
   `sum_{A,M} (-1)^M rank HFK_M(K,A) t^A = Delta_K(t)`.
   The left side is the **stored bigradings**; the right side is computed here
   from a **Seifert matrix** of the stored diagram via `det(V - tV^T)` — a route
   sharing no code and no conventions with the HFK calculator. A relative
   Alexander-grading error, a mirror convention flip, or a `U <-> V` swap each
   break this equality.
2. **HFK symmetry**, `rank HFK_M(K,A) = rank HFK_{M-2A}(K,-A)`, a theorem. This
   ties the absolute Maslov grading to the Alexander grading — exactly the
   relative information risk 1/2 says is fatal if wrong.
3. Alexander support `[-g, g]`, and `rank HFK(K, g) = 1` for fibered `K`.

Run on `K_0`, `K_1`, `K_2`, `K_3`.

## What a pass would and would not mean

**Would:** close the part of risk 1/2 that a relative or convention error breaks,
by an independent route — and with it put `research/11`'s conclusion, and
therefore the closure of P4, on a footing that does not depend on the calculator.

**Would not:** close risk 3 (`d_pure^2 = 0` over `S`), certify the lift to a
homogeneous minimal full complex, or say anything about the involution itself.
It audits gradings.

**A failure would be the more valuable outcome**: it would collapse
`research/11`'s conclusion, reopen involutive Floer as a genuinely decisive test
on `D_{0,1}`, and cast doubt on the stored complexes that several later notes
build on.

Status: running. `check_bigradings.py` -> `RESULTS.json`. The Seifert matrix for
the 19-crossing `K_1` is the slow step.
