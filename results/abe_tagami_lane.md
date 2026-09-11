# The Abe-Tagami lane is now executable (2026-09-11)

## Knots built and independently verified

The family K_n = A^n(6_3) has no machine-readable diagram anywhere in the
literature; both e-print sources and the Dunfield-Gong data contain none. It was
reconstructed here from the paper's figures: the annulus presentation of 6_3 is
four parallel strands on the annulus with a 4-braid full twist on the right wall,
and the band b routed with one self-crossing and one ribbon intersection. Of the
four possible sign conventions only one yields 6_3 (the others give 6_2, 8_20,
9_42), which pins the convention: lk(c'_1,c'_2) = +1, so the n-fold annulus twist
is the Dehn filling c'_1 -> (n+1,n), c'_2 -> (n-1,n).

Independently re-verified in this session from the committed PD codes alone:

| knot | crossings | genus | fibered | vol(exterior) | 0-surgery isometric to 6_3(0) |
|---|---|---|---|---|---|
| K_0 = K_{-1} = 6_3 | 6 | 2 | yes | 5.693021091 | yes |
| K_1 | 19 | 2 | yes | 9.120006501 | **yes** |
| K_2 | 41 | 2 | yes | 11.241489252 | **yes** |
| K_3 | 71 | 2 | yes | 12.520472062 | yes |

Volumes pair as K_n <-> K_{-n-1} exactly as Abe-Tagami's d_3 computation requires,
and the K_n are pairwise non-isometric. The connected sums D_{0,1} (25 crossings),
D_{0,2} (47) and D_{1,2} (60) are built, each with Alexander polynomial Delta^2,
fibered, genus 4. These are the knots Miyazaki's theorem forbids from being ribbon.

## No cheap kill: the standard battery cannot close this lane

| knot | tau | epsilon | nu | signature | HFK total rank | H_1(Sigma_2) |
|---|---|---|---|---|---|---|
| K_0 | 0 | 0 | 0 | 0 | 13 | Z/13 |
| K_1 | 0 | 0 | 0 | 0 | 13 | Z/13 |
| K_2 | 0 | 0 | 0 | 0 | 13 | Z/13 |
| K_3 | 0 | 0 | 0 | 0 | 13 | Z/13 |

Every concordance invariant available here agrees across the family, so **no pair
is killed**. (The bigraded HFK rank profiles do differ, which re-confirms the knots
are distinct, but HFK is not a concordance invariant so this obstructs nothing.)
This is exactly the expected behaviour: the K_n share a 0-surgery, which forces
agreement of most classical and many modern invariants, and is why the lane has
stayed open since 2015.

## The one proof-grade search, now running

`scripts/concordance_search.py`. The logic:

> A ribbon concordance built from one birth and one saddle is an annulus in
> S^3 x I (chi = 0 + 1 - 1 = 0), hence a genuine concordance. Concretely: form
> K u U with U a split unknot, add one band, and keep any result with a single
> component. Such a J satisfies [K] = [J] in the smooth concordance group.

If one knot J is reachable from both K_n and K_m then [K_n] = [J] = [K_m], so
D_{n,m} = K_n # (-K_m) is smoothly slice; Miyazaki (Trans. AMS 341 (1994) Thm 5.5
via Abe-Tagami Cor. 4.3) proves D_{n,m} is not ribbon whenever n != m and
n + m != -1. **A hit is a counterexample to the Slice-Ribbon Conjecture.** This is
the only search in the campaign whose success would be a proof rather than
evidence; failure remains a coverage statement over the parameter box.

Smoke test (1 diagram, band length 4, 1 twist) returned a single successor per
knot and no common one - the band is too short to travel away from the birth site,
so it mostly undoes it. A wider run (6 diagrams, band length 9, 2 twists, over
K_0, K_1, K_2) is running.

Known context: Agol-Ren's Question 1.15 asks whether concordant fibered knots must
admit a common fibered upper bound, so a positive answer here is not expected to be
easy. The search is cheap and its payoff is a proof, which is why it runs anyway.
