# Eisermann's Theorem 2 has teeth at linking number 0 — so the `L_{3,1}` test can fire

16 September 2026. **No counterexample to the Slice-Ribbon Conjecture was found.**
One gating question answered in the affirmative, and one route exhausted.

---

## 1. The gap in the existing rationale

`research/22` §3.3 pre-registers the whole `L_{3,1}` test as a single congruence,
because Theorem 1 is automatic on 2-component slice links (§3.1):

> if `L_{3,1}` is ribbon then `det V(L_{3,1}) ≡ det(Q)·det(V_3) = 81 ≡ 17 (mod 32)`.

Everything therefore rests on Theorem 2 being a **sharp** constraint rather than a
formality. `results/eisermann_ribbon_link_gate.json` argues exactly that:

> "Of 75 tabulated 2-component links only `L9n18` and `L9n19` have `null V = 1`,
> and both VIOLATE Theorem 2 … Neither is slice: linking number 4, signature −6
> and −4. So Theorem 2 is a sharp constraint, not a formality."

**Both of those links have linking number 4. GST's `L_{3,1}` is algebraically
unlinked — linking number 0.** So the teeth were demonstrated in one regime and
the test is to be run in another. `scripts/eisermann_lk0_vacuity.py` makes the gap
concrete: among the small census, **not one `lk = 0` link is even testable**. Every
one has `null V = 0`, so it fails Theorem 1, `det V = [V(L)/V(O^n)](q=i)` is
infinite, and Theorem 2 says nothing. Zero evidence either way, in the regime that
matters.

This also mattered in the other direction. `research/28` found the 0-framed
2-cable route vacuous on seven knots — and every one of those had `lk = 0`. If the
congruence were automatic at `lk = 0`, that would have explained `research/28`
*and* killed the `L_{3,1}` test in one stroke, making the reconstruction pointless.

## 2. The sweep

`scripts/eisermann_lk0_census_sweep.py`, over the tabulated links to 12 crossings.
Controls first: `null V(O^n) = n−1` with `det V = 1` for `n = 2, 3`; and `L9n18`,
`L9n19` reproduce at `det V = 9` and `−7 ≡ 25 (mod 32)`, matching the values the
gate file records.

| | |
|---|---|
| links scanned | 5700 |
| 2-component | 3732 |
| with `lk = 0` | 1152 |
| **testable** (`lk = 0` **and** `null V = 1`) | **41** |
| of those, **violating Theorem 2** | **22** |
| of those, satisfying it | 19 |

**Theorem 2 has teeth at `lk = 0`.** 22 of 41 testable links violate the
congruence, so it is neither vacuous nor automatic in the regime `L_{3,1}` lives
in. The pre-registered `L_{3,1}` test can fire, and the reconstruction in
`research/27` is worth doing. That was the gating question and it is now settled.

A methodological note: the first version of the sweep reported "no `lk = 0` link
violated the congruence" when in truth **no `lk = 0` link had been tested at all** —
every one was `n/a`. A vacuous pass read as a clean pass. The script now
distinguishes *tested and held* from *not testable* and prints the counts, because
that distinction is the entire content of §1.

## 3. The census route is exhausted: none of the violators is slice

A violator is a link **proved not ribbon** by Eisermann. If one were also slice it
would be slice-and-not-ribbon — the first such object of any kind, which is exactly
the prize `research/22` §3.3 describes. So each was screened.

Of the 22 violators, **seven have both components unknotted** — `L10n56`, `L10n57`,
`L12n1109`, `L12n1272`, `L12n1273`, `L12n1299`, `L12n1300` — so their components are
slice and the usual component-level obstructions are silent. The other 15 have a
component of determinant 3, 5 or 27, which is not a square, so that component is not
slice and neither is the link.

The seven were put through the repository's own Sato–Levine screen
(`scripts/slice_screen_links.py`, `triple_linking.conway_coefficients`): every
sublink of a slice link is slice, and a `lk = 0` 2-component slice link has
`β = μ̄(1122) = [z^3]∇_L = 0`. Control: the Whitehead link returns `β = −1`,
nonzero as required.

| link | Conway coefficients | `β` | verdict |
|---|---|---|---|
| `L10n56` | `[0,0,0,4,0,1]` | **4** | not slice |
| `L10n57` | `[0,0,0,4,0,1]` | **4** | not slice |
| `L12n1109` | `[0,0,0,−4,0,−5,0,−1]` | **−4** | not slice |
| `L12n1272` | `[0,0,0,−4,0,−1]` | **−4** | not slice |
| `L12n1273` | `[0,0,0,−4,0,−1]` | **−4** | not slice |
| `L12n1299` | `[0,0,0,−4,0,−5,0,−1]` | **−4** | not slice |
| `L12n1300` | `[0,0,0,−4,0,−5,0,−1]` | **−4** | not slice |

**Zero survivors.** Every Theorem-2 violator with slice components in the tables to
12 crossings has nonzero Sato–Levine invariant and is therefore not slice.

That is a real negative and it has a clear consequence: **the counterexample is not
sitting in the link tables.** Being non-ribbon is common among tabulated links;
being non-ribbon *and slice* is not, and the census does not contain it to 12
crossings. It has to be **constructed** — which is precisely what `L_{3,1}` is, and
why GST built it rather than looking one up.

## 4. Where this leaves the lane

* The `L_{3,1}` test is **worth running**: Theorem 2 is sharp at `lk = 0`.
* The blocker is unchanged and is construction, not computation — trace
  `L_{3,1}` from the figures now archived in `figures/gst_source/` and pass all
  three identity checks (components `Q` and `V_3`; linking number 0; the band sum
  along GST's band reproducing `B_{3,1}`) before computing anything.
* A cheap extension worth doing first: this sweep stopped at 12 crossings. Running
  it to 14 costs little and would either turn up a survivor — a genuine
  candidate — or strengthen §3 considerably. It should be run before the tracing,
  because a survivor would be a far cheaper target than `L_{3,1}`.
* `research/22` §3.4(2)'s `n ≥ 3` route remains open and untouched; `research/28`
  §3.1 already showed split unknots cannot reach it.
