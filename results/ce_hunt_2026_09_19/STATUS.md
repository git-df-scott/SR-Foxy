# Walker status snapshot — 2026-09-19T02:55:30.428188Z

**Hits: 0. No counterexample.**

| log | weights | exhausted | hits | complete |
|---|---|---|---|---|
| `pass1_00` | `[1,17,1,1,3]` | 12 | 0 | running |
| `pass1_01` | `[1,17,1,1,3]` | 31 | 0 | yes |
| `pass1_02` | `[1,17,1,1,3]` | 29 | 0 | yes |
| `pass2_crossheavy_02` | `[2,12,6,6,3]` | 1 | 0 | running |
| `pass2_twistheavy_01` | `[3,10,2,2,9]` | 4 | 0 | running |
| `weights_startheavy_AT` | `[4,17,1,1,3]` | 9 | 0 | running |

**Totals: 86 targets exhausted, 0 hits.**

Pass 1 (GHMR default weights, 400 tries) is complete on shards 01 and 02 —
31/31 and 29/29, `Succeeded 0 times` on both. Shard 00 carries the ten
`D_{0,1} # J` targets at 31-35 crossings and is slower by design.

Pass 2 spreads across the walker's action-weight space rather than going deeper
at one setting, since GHMR tuned the default on synthetic `Sym`/`Unsym` knots
and these are composite genus-5+ targets.

An exhausted target means no bands within the try budget. Per README §13 that is
**weak** evidence about ribbonness and **none** about sliceness — GHMR's own
programs failed on `L_{1,1}` and `L_{2,1}`, both known ribbon. Only a hit counts,
and a hit needs `verify_ribbon_to_unknot` first.

Why this is a lottery rather than a construction:
`research/51_why_infection_cannot_make_a_wild_pair.md`.
