# The common-upper-bound concordance search: why it does not run, and what it needs
2026-09-11

This was billed as the only search in the campaign whose success would be a proof.
It is now implemented, diagnosed, and **blocked on a missing piece of machinery**
that is precisely identified below. Two bugs were found and one is structural.

## The logic (unchanged, still correct)

A ribbon concordance built from one birth and one saddle is an annulus in S^3 x I
(chi = 0 + 1 - 1 = 0), hence a genuine concordance. So if a knot J satisfies
K_n <= J and K_m <= J in Gordon's ribbon-concordance order, then

        [K_n] = [J] = [K_m],

so D_{n,m} = K_n # (-K_m) is smoothly slice. Miyazaki (Trans. AMS 341 (1994)
Thm 5.5, via Abe-Tagami Cor. 4.3) proves D_{n,m} is not ribbon for n != m,
n + m != -1. A hit is a counterexample. A common *predecessor* works equally well,
since a concordance is a concordance in either direction.

## Bug 1: the band generator only splits

`spherogram.links.bands.banded_links` generates only bands that **raise** the
component count. This is by design: a ribbon-disk search drives a knot toward an
unlink, so every band splits. Measured on K_0 u U (a knot plus a split unknot,
2 components): all 156 generated bands gave **3 components**, never 1. A fusing
band, which the common-successor formulation needs, is never produced. The naive
implementation could not have found anything.

## The fix, and Bug 2 (structural)

Run the concordance backwards: apply one splitting band to K and keep results of
the form A u U with U a split unknot. Reversing, A -> A u U -> K is a birth plus a
saddle, so [A] = [K]. This *is* expressible with the DG generator.

Measured, band length <= 9, 2 twists:

| knot | bands generated | split off a trivial unknot |
|---|---|---|
| 6_3 = K_0 | 156 | **0** |
| 6_1 (ribbon, fusion number 1) | 138 | 0 of type (knot) u U; **12** give the 2-component unlink |
| 8_9 | 304 | 0 |
| 9_27 | 401 | 0 |

The bookkeeping is verified correct by 6_1: it is ribbon with fusion number 1, and
exactly 12 of its bands produce the 2-component unlink, i.e. zero remaining
components and two unlinked unknots. So the detector works; the event simply does
not occur. No band splits any of these knots into (nontrivial knot) u (split
unknot).

**Why, and this is the real content.** Such an A is an immediate predecessor of K
in the ribbon-concordance order. Agol (partial order), Baldwin-Sivek and Agol-Ren
prove a fibered knot has only **finitely many** ribbon-concordance predecessors,
and tight fibered knots are minimal. Every Abe-Tagami K_n is fibered. So this
family is expected to have essentially no nontrivial predecessors, and the
predecessor direction of the search is structurally doomed for exactly the knots
we care about.

## What the lane actually needs

**A fusing-band generator.** To search the successor direction one must enumerate
bands on K u U whose two feet lie on *different* components. That is a modest but
real piece of code: DG's `Band` class takes a path of crossing strands, so the work
is to generate paths from a face touching K to a face touching U and check
embeddedness, rather than reusing `min_len_bands`/`simple_bands`, which are written
for the splitting case.

Until that exists, the Abe-Tagami lane cannot be advanced computationally, and the
honest status is: the knots are built and verified, the logic is airtight, no cheap
concordance invariant kills any pair, and the search is blocked on machinery rather
than on compute.

Note also Agol-Ren's Question 1.15 (do concordant fibered knots admit a common
fibered upper bound?) is open, so even a working generator is not expected to
succeed quickly.

Script: `scripts/concordance_search.py`, which now writes incrementally so a killed
run keeps partial results.

## Operational note

All detached background searches (`nohup setsid`) were reclaimed by the container
between check-ins. The wide concordance run lost 24 minutes of completed work
because the original script wrote output only at the end. Every long-running script
in this repository should checkpoint after each diagram; `concordance_search.py`
and `band_search_shaken.py` now do.
