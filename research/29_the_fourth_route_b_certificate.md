# A fourth route-B certificate, absent from the ledger, that needs only one knot to be slice

16 September 2026. **No counterexample to the Slice-Ribbon Conjecture was found.**

> ### CORRECTION, same day, before this note was ever acted on
>
> **Sections 2 and 3 as first written were wrong, and the error was mine.** I
> presented the Turaev lane as "live and untested with five knots at 27–51
> crossings" on the strength of `ERRATA_2026-09-11.md` E1, **without reading
> `results/turaev_family_status.md`**, whose UPDATE of 12 September already
> settled it. What that file records:
>
> * **Four of the five stored knots have `r = s = 0`.** Theorem I's three
>   conclusions are for `r≠0 and s≠0`, `r≠0 or s≠0`, and `r=0,s≠0` or `r≠0,s=0`.
>   `r = s = 0` falls into **none** of them, so those four carry **no non-ribbon
>   certificate at all** and are not route-B candidates. `research/08` §4 says so
>   explicitly: "r=0 or s=0 members are *not* candidates".
> * **`A(1,1,0,0)` is known RIBBON**, with a one-band Dunfield–Gong certificate
>   found in 1.3 seconds — which is the expected outcome and validates the surface
>   construction.
> * **`A(1,1,1,1)`, the only stored member Theorem I does obstruct, was killed on
>   12 September.** `slice_obstruction_HKL` returns `(3, 13)`; a non-None value
>   proves the knot is **not topologically slice**, hence not smoothly slice.
>   Verified independently from the stored PD, 25.3 s. It is not a counterexample.
>
> So the lane's only built candidate is **dead**, and my `s`-invariant runs in §2
> below were performed on knots that are **not candidates** — one of them already
> known ribbon. Those runs are correct as computations and worthless as evidence.
> The ledger entry I added has been corrected accordingly.
>
> **What survives** is the narrow structural point in §1, and only that: Turaev
> Theorem I is a route-B certificate that needs **one knot to be smoothly slice**,
> with no concordance coincidence, so `research/24` §4's "the only route on this
> board that escapes section 1" is wrong as written. That remains true of the
> *family*. It is much weaker than I made it sound, because the family's one
> realised member is dead and `research/24` was written two days **after** that
> kill — so omitting Turaev may have been a deliberate editorial call rather than
> an oversight, and I should not have assumed otherwise.

One structural point that survives, and one pre-registered test whose result turned
out to be worthless for the reason above.

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

## 2. The pre-registered `s` test, and why its result does not matter

Pre-registration at `results/PREREG_turaev_s_invariant_2026-09-16.md`, written
before the run. Controls on the source-built KnotJob, same session: `s(+3_1) = +2`,
`s(-3_1) = -2`, `s(4_1) = 0`, `s(6_1) = 0`. All four correct.

| knot | `(p,q,r,s)` | cr | `mu_135, mu_246` | Theorem I obstructs? | `s` char 0 / 2 | wall |
|---|---|---|---|---|---|---|
| `Turaev_A_1_1_0_0` | (1,1,0,0) | 27 | (0,0) | **no** — and it is **known ribbon** | 0 / 0 | 11 s |
| `Turaev_A_1_3_0_0` | (1,3,0,0) | 37 | (0,0) | **no** | 0 / 0 | 20 s |
| `Turaev_A_2_1_0_0` | (2,1,0,0) | 39 | (0,0) | **no** | 0 / 0 | 47 s |
| `Turaev_A_3_1_0_0` | (3,1,0,0) | 51 | (0,0) | **no** | UNKNOWN — container reclaimed | — |
| `Turaev_A_1_1_1_1` | (1,1,1,1) | 143 | (1,1) | **yes** | not attempted | — |

Every row I computed is a knot Theorem I does not obstruct, so `s = 0` there carries
no information about the lane whatsoever — and for `A(1,1,0,0)`, already certified
ribbon, `s = 0` was a foregone conclusion. **Three completed runs, zero evidential
value.** The 51-crossing row died to a container reclamation (`up 0 min`, no `exit=`
line, so not a Java OOM) and is UNKNOWN, not negative.

The one row that would have mattered, `A(1,1,1,1)`, is both out of reach here at 143
crossings and already dead by HKL.

**The methodological lesson, which is the only thing §2 earns:** I ran compute
before reading the file in `results/` that carried the answer. The parameters
`r, s` are in the filenames and in the JSON, and Theorem I's hypotheses were quoted
verbatim in `research/08` two screens above the verdict. Checking the certificate
applies to the object should precede measuring the object.

## 3. What the lane actually needs now

Not `s`, and not these five knots.

1. **The family is not exhausted.** Theorem I applies for every `p = 1` or prime,
   `q ≥ 1` (`q ≠ 2` if `p = 2`), and `r, s` both nonzero. Exactly **one** such knot
   has ever been built, `A(1,1,1,1)`, and HKL killed it. `results/turaev_family_status.md`
   names `(1,3,1,1)` and `(2,1,1,1)` as the next smallest. The construction pipeline
   exists — disk with six untwisted bands from `X`, then Milnor's ribbon-linking move
   to install `r, s`, validated by `mu_135`/`mu_246` coming out as intended.
2. **The expected outcome is another HKL kill.** `turaev_family_status.md` predicted
   it for `A(1,1,1,1)` and was right, and its own correction notes that the `q = 1`
   "immune subfamily" argument was wrong: HKL fired on the **3-fold** cover, not
   `Σ_2`, where `det = 1` makes the classical test vacuous. Anyone building
   `(1,3,1,1)` should expect the same and pre-register that expectation.
3. **HKL needs Sage**, which this container does not have
   (`Manifold.slice_obstruction_HKL` is `@sage_method`). So the decisive test for any
   newly built member cannot be run here even though the build might be.

So the fourth certificate is real as a certificate and nearly empty as a lane: one
member realised, one member dead, and the next members unbuilt and likely to die the
same way. That is a much more modest claim than the one this note opened with, and it
is the accurate one.
