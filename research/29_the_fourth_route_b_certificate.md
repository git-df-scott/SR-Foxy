# A fourth route-B certificate, absent from the ledger, that needs only one knot to be slice

16 September 2026. **No counterexample to the Slice-Ribbon Conjecture was found.**
One structural correction, and one pre-registered test whose result is a null.

---

## 1. `research/24` §4's uniqueness claim is false

`research/24` §1 argues that every route-B lane reduces to the same missing object:

> **So the single object that would unlock all of route B at once is a pair of
> distinct, concordant, fibered knots.**

Its table lists three certificates — Miyazaki fibered pairing, Miyazaki Example 2,
Hom–Park `γ_0`-sharp pairing — and each needs a concordance coincidence. §4 then
presents the `r = 0` RBG crossing and says:

> Note that it does **not** need two concordant fibered knots. **It is the only
> route on this board that escapes section 1.**

**It is not.** There is a fourth, and it was already on the board when
`research/24` was written.

`ERRATA_2026-09-11.md` E1, three days earlier, records the recovery of Turaev's
Theorem H and Theorem I from the primary text (Mat. Sb. 116(158):3 (1981), English
translation Math. USSR-Sb. 44:3 (1983), recovered from mathnet.ru; see
`research/08`). Its conclusion, verbatim:

> Turaev's **Theorem I** is a live and untested route-B *target*. It builds
> explicit genus-3 knots that are algebraically slice and, by H(ii) plus the
> π₁-surjectivity proof, provably **not homotopy-ribbon**. Theorem J says H gives
> no sliceness obstruction, so it does not rule out their being slice. **Any
> Theorem I knot that is smoothly slice is a counterexample.**

That is a route-B certificate: `ribbon ⇒ handle-ribbon ⇒ homotopy-ribbon`, so
*not* homotopy-ribbon is a *stronger* statement than not ribbon, and Theorem J
says it costs nothing on the sliceness side. And what it needs is **one knot to be
smoothly slice** — no concordance coincidence, no pair of fibered knots, nothing
from §1. It escapes the reduction exactly as the `r = 0` crossing does.

`research/24` never mentions Turaev — the string does not occur in the file. Nor
does `CANDIDATE_LEDGER.md`, which is where this repository decides what is on the
board. So a lane declared live on 11 September has been invisible since, while
five of its knots sat in `data/knots/`.

### It is also the cheaper of the two

| | `r = 0` RBG crossing (`research/24` §4) | Turaev Theorem I |
|---|---|---|
| escapes §1 | yes | **yes** |
| objects in hand | **none** — all ten stored MP exteriors are hyperbolic, so none can carry a Miyazaki certificate | **five**, `data/knots/Turaev_A_*.json` |
| generator available | **no** — needs `../mma.py`, `../mp_auto.py`, outside every clone this campaign has used | not needed |
| smallest object | n/a | **27 crossings** |

The `r = 0` crossing needs files that do not exist in any clone. The Turaev lane
needs nothing that is not already here.

---

## 2. Pre-registered test: `s` on the Turaev knots. Result: null.

Pre-registration at `results/PREREG_turaev_s_invariant_2026-09-16.md`, written
before the run. Every classical obstruction already vanishes on these knots
(algebraically slice, Fox–Milnor passes — `results/fox_milnor_audit_2026-09-16.json`)
and `τ = ε = 0`, so `s` is the next tool. At 27–39 crossings it is cheap; the
failures in `UNFINISHED.md` §3 were at 47.

**Controls, same build and same session** (source-built KnotJob under `javac 21`):
`s(+3_1) = +2`, `s(-3_1) = -2`, `s(4_1) = 0`, `s(6_1) = 0`. All four correct, so
the rows below are not void.

| knot | crossings | genus | `det` | `Δ` Fox–Milnor | `τ` | `ε` | `s` (char 0) | `s` (char 2) | wall |
|---|---|---|---|---|---|---|---|---|---|
| `Turaev_A_1_1_0_0` | 27 | 3 | 1 | norm | 0 | 0 | **0** | **0** | 11 s |
| `Turaev_A_1_3_0_0` | 37 | — | — | — | — | — | **0** | **0** | 20 s |
| `Turaev_A_2_1_0_0` | 39 | — | — | — | — | — | **0** | **0** | 47 s |
| `Turaev_A_3_1_0_0` | 51 | — | — | — | — | — | running | running | — |
| `Turaev_A_1_1_1_1` | 143 | — | — | — | — | — | not attempted | | |

**Per decision rule 2, fixed in advance: `s = 0` is no obstruction and no evidence
of sliceness.** These knots merely survive. Nothing here makes them "probably
slice", and the campaign does not get to book it as progress. The informative
outcome would have been `s ≠ 0`, which would have killed a knot outright; that did
not happen, and the null is reported at the same prominence a kill would get.

`Turaev_A_1_1_1_1` at 143 crossings is out of reach in this container and is not
attempted; it is **UNKNOWN**, not negative.

---

## 3. The gap that has to be closed before this lane is promoted

I did **not** audit the certificate itself today, and it is the whole lane:

> **Open:** do the five stored `A(p,q,r,s)` knots actually realise Turaev's
> Theorem I, with its hypotheses satisfied?

`research/08` recovers the construction from the primary text and tests the knots
against classical slice obstructions, but the step "these specific stored PD codes
are Theorem I knots, and Theorem H(ii) applies to them" is what makes them
non-ribbon, and it is exactly the kind of step that this repository got wrong once
already today — see `ERRATA_2026-09-16.md` E16-1, where a theorem was restated
without a hypothesis and cancelled three searches. **Until that is checked against
Turaev's hypotheses knot by knot, every Turaev row stays a candidate and no
non-ribbon certificate should be quoted from it.**

What the lane needs, in order:

1. Verify Theorem I's hypotheses on each stored `A(p,q,r,s)`, and record which
   theorem number supplies non-homotopy-ribbonness, in `SOURCES.md`, with the
   hypotheses written out — the treatment [S07] now gets.
2. Add the knots to `CANDIDATE_LEDGER.md` as Tier-B with the certificate named.
3. Then, and only then, spend compute on proving one of them slice. The Teichner
   route on `Turaev_A_1_1_0_0 # 6_1` is a 33-crossing sum — the same band as the
   completed `8_8` run at 7.96 h, so it is tractable on a machine that stays up,
   though not in this container (`UNFINISHED.md` §3).

The honest summary: this note does not bring a counterexample closer by any
computation. It puts a fourth certificate back on a board that had written it off
to three, corrects a uniqueness claim, and establishes that the cheapest objects
carrying it survive the one smooth obstruction this container can compute.
