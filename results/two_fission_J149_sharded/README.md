# Sharded reverse two-fission search from J149 — terminated, no hit

**No counterexample found. No K1 endpoint found.** This run was stopped by hand
before its 2400-second cap, so every `shard*.json` has `complete: false` and no
`stop` field. Treat these as partial coverage records, not completed runs.

Bounds: target `results/coupled_small_targets.json` (J149), four disjoint shards
(`--shards 4`), per-intermediate cap 2000, path length 8, twists 2, field F101 at t=2.

| shard | first bands | linking rej. | rank rej. | intermediates | second bands | endpoints | hits |
|---|---:|---:|---:|---:|---:|---:|---|
| shard0 | 7130 | 1322 | 343 | 105 | 208230 | 1 | [['K0']] |
| shard1 | 7130 | 1326 | 347 | 101 | 200223 | 1 | [['K0']] |
| shard2 | 7130 | 1327 | 321 | 127 | 252252 | 1 | [['K0']] |
| shard3 | 7130 | 1325 | 344 | 100 | 198225 | 1 | [['K0']] |
| **total** | **28520** | **5300** | **1355** | **433** | **858930** | **4** | — |

Every endpoint found was K0, the saved positive control, recovered once per
shard. That is the search recognising a movie already in the repository. It is
not a hit, and the run supplies no K1 movie and no geometric certificate.

## Why it was stopped

`research/11_involutive_local_equivalence.md` establishes that K0 and K1 share
an involutive knot-Floer local equivalence class, and `HANDOFF.md` draws the
consequence: no invariant factoring through that class distinguishes them. The
filters steering this search — HFK rank injection, the Zemke chain-retraction
condition, the quotient chain maps — all factor through that class. So the
search's guidance is blind to the distinction it is trying to resolve: it can
neither reject a wrong candidate for the right reason nor confirm a right one.
Enlarging the box does not repair that.

Separately, K0 and K1 are not related by bands. They are the (n+1,n) and
(n-1,n) fillings of the single 3-cusped exterior in
`data/knots/AbeTagami_L_63_c1_c2.json`. This search discards that structure and
shakes bands on the filled diagrams instead.

Not a proof that no common successor exists, and not evidence that one does.
