# The DG 0-friend collection contains no wild Miyazaki pair — by Fox-Milnor

19 September 2026, Opus. **CE: NO.**

`check_dg_zero_friends.py` -> `RESULTS.json`. Controls pass. Full discussion in
`research/50_the_dg_dataset_is_here_and_the_0_friend_lane_is_closed.md`.

## Input

Dunfield-Gong, *Ribbon concordances and slice obstructions: code and data*,
Harvard Dataverse `doi:10.7910/DVN/YBDTBT`. Single file `plausibly_slice_V1.zip`,
**1,022,355,830 bytes, md5 `7f6dc1df595ba1b4dbb1a9b338798b0b`** — both match the
figures `research/04` §1(b) recorded from the Dataverse metadata. The archive is
1 GB and is **not** committed; re-fetch with

```
curl -L -o dg.zip "https://dataverse.harvard.edu/api/access/dataset/:persistentId?persistentId=doi:10.7910/DVN/YBDTBT"
unzip dg.zip && unzip plausibly_slice_V1.zip
python3 check_ribbon_cert.py  # DG's own checker, in code/
python3 check_dg_zero_friends.py plausibly_slice_V1/data
```

## Result

Over 158,174 rows of `zero_friends.csv` + `more_zero_friends.csv`:

| | |
|---|---|
| rows | 158,174 |
| `Delta` trivial | 8,393 |
| nontrivial, not monic | 67,380 |
| nontrivial, monic | 82,401 |
| **monic and irreducible over Q** | **0** |

Zero candidates, as Proposition R in the script's docstring requires: every knot
in PS19 satisfies Fox-Milnor, so its `Delta` is a norm `f f*`; an irreducible
`Delta` forces `Delta = 1`; a fibered knot with `Delta = 1` is the unknot; and a
0-friend shares `Delta` with its base knot.

## Controls

Five, all passing, two of which must fire **positive** so that an all-zero
column means something: `Delta(3_1) = t^2-t+1` and
`Delta(6_3) = t^4-3t^3+5t^2-3t+1` are reported monic irreducible; the `6_1` norm
`2t^2-5t+2` non-monic reducible; the square knot's `t^4-2t^3+3t^2-2t+1` monic
reducible; the unknot degree 0.

## Scope

This closes `HANDOFF_2026_09_18_OPUS.md` P2's first bullet (*mine DG's 0-friend
pairs*) **by a theorem**, not by a bounded search. It does **not** close P2's
other bullets: DG's own `code/find_0_friends.py` generator applies to any
hyperbolic knot, and running it on the fibered / irreducible-`Delta` population
is untouched and not affected by Proposition R.

No counterexample. No slice disk. No obstruction to one.
