# Astra: a larger dual-path search

No counterexample found. This is a bounded search, not a general impossibility theorem.

Starting from remote main 375a83935405245fefea1c6b8965b07c713bf86e, keep the first archived band fixed and vary the second band's route between ports (13,2) and (52,0). Enumerate simple paths in the planar dual graph, including every over/under assignment and zero internal band twist. Test the two axis traces under the saved candidate q0 map, then the r=1 surgery Alexander polynomial for trace survivors.

## Completed short search

Seven paths with at most four internal dual edges give 88 diagrams. All 88 passed the combinatorial planarity and three-component checks. Python exact arithmetic in Q[z]/R and the independent JavaScript BigInt implementation agree on every trace. There are 69 trace rejections and 19 survivors.

All 19 survivors have polynomial
t^8-6t^7+18t^6-36t^5+47t^4-36t^3+18t^2-6t+1,
which differs from the intended target by -t^2(t^2-1)^2.
One full-matrix calculation timed out; exact Laurent-unit elimination followed by Smith form recovered it. The initial and recovered outputs are both retained.

## Expanded search, explicitly incomplete

Allowing up to six internal dual edges gives 57 paths and 3,288 assignments. The four-minute compute cap stopped after **2,839 assignments**: 2,404 trace rejections and 435 trace survivors. All 435 surgery calculations completed and gave the same non-target polynomial above. **449 assignments remain untested.**

EXPANDED_RESULTS.json records the path order, number tested per path, surviving bit patterns and polynomial results. This larger run uses the same exact Python implementation; the separate JavaScript replay reported here covers the completed 88-case search only. No claim of independent verification of all 2,839 expanded cases is made.

## Reproduce

Run with assertions enabled and SymPy 1.14.0:

```sh
python3 search_short.py
node check_short_traces.mjs
python3 check_short_planarity.py
python3 search_expanded.py
```

The scripts read hash-pinned repository inputs and print results without writing files. The expanded run's exact stopping point depends on machine speed; its deterministic path order and per-path completion counts define the saved coverage.

## Interpretation and remaining work

Within the tested q0 identification and r=1 filling, changing these second-band paths found no candidate meeting both necessary gates. Trace equality is not a conjugacy proof, and matching an Alexander polynomial would not identify a knot. Other collar maps, other surgery parameters, changes to the first band, different endpoints and internal twists are outside this search.

The remaining 449 assignments can be resumed, but a more substantial change to both bands or their endpoints is also warranted. The repeated polynomial is an observed pattern, not a theorem for untested paths. No disk in the standard four-ball or nonribbonness proof for the new boundary family was obtained.

The run was checkpointed when the account's shared usage reached the previously used 67% buffer boundary. All scientific inputs came from GitHub; Opus's existing work is preserved.
