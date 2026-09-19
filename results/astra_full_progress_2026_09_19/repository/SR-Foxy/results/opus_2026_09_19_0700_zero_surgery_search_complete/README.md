# The 0-surgery census search is COMPLETE, and it is empty

19 September 2026, Opus. **CE: NO.**
**Smooth concordance: UNKNOWN. Slice-Ribbon CE: NO.**

`scripts/zero_surgery_isosig_merge.py` over `raw/`, SnapPy 3.3.2.

---

## 1. The result

**3486 / 3486 signed knots. 3477 decided. 9 UNKNOWN. ZERO isometric groups.**

The population: prime fibered knots of at most 14 crossings with irreducible
Alexander polynomial, restricted to the **1589 groups whose 0-surgeries have
equal volume** inside a shared `Delta` (2352 pairs), a filter robust from `1e-6`
to `1e-10`. Each knot's 0-surgery was given its **oriented** isometry signature
(`ignore_orientation=False`, canonical retriangulation), and the signatures were
grouped across the whole population.

No two of them have isometric 0-surgeries.

## 2. What this is, stated precisely

**FAILED TO FIND, WITHIN STATED BOUNDS.** It is *not* a theorem. Specifically:

* **9 knots are UNKNOWN**, not excluded — `RuntimeError` from the SnapPea
  kernel. Nine undecided knots cannot be reported as nine exclusions. This
  campaign published exactly that error once already and retracted it in
  `5a4b38a`.
* The scope is **at most 14 crossings, hyperbolic, census-listed**. Abe-Tagami's
  own `K_1` is **in no census** — it is a 19-crossing knot rebuilt from a paper
  figure. The one configuration we *know* exists would not have been found by
  this search. That is the sharpest available statement of the search's reach.
* `isometry_signature(verified=True)` needs Sage, absent here, so the canonical
  retriangulations are numerical. High confidence, not proof.
* A shared 0-surgery would not have implied concordance anyway (Yasui disproved
  Akbulut-Kirby). A hit would have been a *candidate*, not a counterexample.

## 3. Why it came out empty — the diagnosis, not an excuse

`c1d0c46` established what the volume filter actually selects: **mutant pairs.**
1472 of the 1589 groups share identical bigraded HFK, volume agreeing to
`1e-10`, and Alexander polynomial — the signature of Conway mutation, which
preserves all three (Ruberman for volume). Mutation does **not** generally
preserve the 0-surgery, so a filter that selects mutants is not a filter that
selects 0-surgery-equal pairs.

The search was therefore looking in a population assembled by the wrong
mechanism. The empty result is evidence about the filter, and only weak evidence
about the census.

## 4. What survives as a lead

The ~1472 mutant pairs remain, and they are pairs of **distinct prime fibered
knots with irreducible `Delta`** — exactly the population for which any
concordance refutes slice-ribbon (via Miyazaki, or independently via
`../opus_2026_09_19_0600_fibered_irreducible_minimal/`). **"Is a knot concordant
to its positive mutant?" is a recognised open question.** Nothing here decides
it, and no tool in this container can.

## 5. The three shard bugs, and why the data is still good

The sharded producer's end-of-run self-report was wrong three ways: all shards
wrote one `OUT` path; each grouped over the `done` it loaded at startup; and
because knots are distributed by index mod 4, **two members of a group land in
different shards, so a genuine hit could be missed by every shard's own
report**. The per-record JSONL checkpoints are unaffected, and the merge script
(`cb1b420`) is the only correct readout. The zero above is the merged one.

## Raw data

`raw/zero_surgery_isosig_all_shards.jsonl.gz` — all 3486 records, one JSON
object per knot, with `SHA256SUMS`. The container's `/tmp` is reclaimed on
restart; this is the durable copy.

```
python3 ../../scripts/zero_surgery_isosig_merge.py
```
