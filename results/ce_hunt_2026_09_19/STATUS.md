# Walker status snapshot — 2026-09-19T02:52:11.239803Z

**Hits: 0. No counterexample.**

| log | targets exhausted | hits |
|---|---|---|
| `pass1_00.log` | 7 | 0 |
| `pass1_01.log` | 30 | 0 |
| `pass1_02.log` | 25 | 0 |
| `weights_startheavy_AT.log` | 6 | 0 |

Totals: **68 exhausted at 400 tries, 0 hits**, over 90 distinct targets plus a
weight-varied re-run of the ten AT targets.

An exhausted target means the walker found no bands within its try budget. Per
README section 13 that is **weak** evidence of non-ribbonness and **no** evidence
about sliceness: GHMR's own programs failed on `L_{1,1}` and `L_{2,1}`, both known
ribbon. Only a hit counts, and a hit needs `verify_ribbon_to_unknot` first.

See `research/51_why_infection_cannot_make_a_wild_pair.md` for why the search is
a lottery rather than a construction, and for the retraction of the
`deg Delta = 2g` fiberedness inference in README section 12.
