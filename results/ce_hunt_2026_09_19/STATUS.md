# Walker status snapshot — 2026-09-19T02:45:34.920006Z

**Hits: 0. No counterexample.**

| log | targets exhausted | hits |
|---|---|---|
| `pass1_00.log` | 2 | 0 |
| `pass1_01.log` | 8 | 0 |
| `pass1_02.log` | 6 | 0 |
| `weights_startheavy_AT.log` | 1 | 0 |
Totals: **17 exhausted at 400 tries, 0 hits**, of 90 targets (100 target-runs
counting the weight-varied AT pass separately).

A target recorded as exhausted means the walker did not find bands within its
try budget. Per section 13 of the README that is **weak** evidence of
non-ribbonness and **no** evidence about sliceness: GHMR's own programs failed
on `L_{1,1}` and `L_{2,1}`, both known ribbon. Only a hit counts, and a hit
needs `verify_ribbon_to_unknot` before it is a result.
