# Pass 03 — a proposed general transfer argument, not a counterexample

17 September 2026 UTC. Read against SR-Foxy main at `0eb81a1a15147b2059b9028d0bbc0f4173f0ad33`.

**CE: NO. No new disk, concordance, or global nonribbon certificate.**

## Strongest new result and its review status

A complete proposed proof in `PROPOSED_TRANSFER_THEOREM.md` would show that EVERY ribbon-pattern satellite of a smoothly slice companion passes Eisermann's full-nullity and mod-32 determinant-product tests, without a wrapping bound. The argument is independently UNREVIEWED, not a published theorem or a claim of novelty. The infinite conclusion comes from the written proof, not finite pattern/cable examples.

The key new ingredients are a coefficientwise Chebyshev connected-sum filtration, all-degree 2-integrality of the leading laws, and a Vandermonde argument using connected sums of the ribbon knot 6_1 to force integral pattern-coefficient divisibility. Casson's stable-ribbon observation then transfers the conditions from ribbon knots to smooth slice knots. Imported results and exact source locations are separated from these deductions.

If the proof survives an independent audit, another five-parallel or high-wrapping ribbon-pattern computation on KDG cannot find a counterexample using these TWO tests. This says nothing about arbitrary slice links, higher Jones coefficients, other invariants, or all satellite constructions. It certainly does not prove KDG ribbon.

## What actually ran

The standard-library checker passed **4,832 exact finite algebra checks through parallel degree 20**, including 22 negative checks. A second implementation path constructed the two- and three-parallels of 6_1#6_1 and evaluated them with the existing pass02 diagram engine:

| new control | crossings | exact reduced value | predicted value |
|---|---:|---:|---:|
| (6_1#6_1) two-parallel | 80 | 97 | 97 |
| (6_1#6_1) three-parallel | 180 | 32049 | 32049 |

The written low-degree laws explain the values: e2(K#J)=e2(K)+e2(J)-1; e3(K#J)=d(K)e3(J)+e3(K)d(J)-d(K)d(J). Exact divisibility was checked, not inferred from a modular zero. The direct diagram computation is independent of the colored-sum algebra, but reuses pass02's cabler and frontier engine rather than an independent topology library.

A four-parallel connected-sum control failed with `std::bad_alloc` under a 2 GiB address-space cap and produced no value. Its predicted 53185 is NOT a computed knot invariant. The failed attempt, input, and log are saved. It was not rerun. No KDG target calculation was repeated and no fifth-parallel was attempted.

## Reproduce

From a repository containing the proposed additions:

```
D=results/astra_2026_09_17_overnight/pass03_0431_general_transfer
python3 "$D/check_general_transfer.py" --output /tmp/FRESH_ALGEBRA.json --degree 20
python3 "$D/check_connected_sum_controls.py" \
  results/astra_2026_09_17_overnight/pass02_0410_four_parallel \
  /tmp/FRESH_DIRECT_CONTROLS --maximum 3
```

The first command uses standard-library Python only. The second needs SymPy, g++, Boost headers, and the already published pass02 sources. Output paths must not exist. The audit ZIP includes those unchanged pass02 dependencies for offline reproduction; they are NOT repeated as proposed repository additions. All runs are serial, exact, bounded, and executed in this Linux container, not on the Mac.

## Publishing state

These files were prepared for the new directory named above, but **were not pushed in this response**. The current GitHub connector provided 48 read/search tools and no create-file/tree/commit/ref-update action. Plugin discovery confirmed GitHub is already installed; no new service was connected, no credential was reused, and the container has no authenticated GitHub CLI. Earlier successful pushes are not evidence that a write operation is available now.

`SR_Foxy_pass03_additions.patch` is an additions-only patch. A worker with the existing authorized repository can inspect `git status`, then use `git apply --check` before applying it on its CURRENT branch. No reset, branch creation, overwrite, force-push, or change to existing research files is part of this patch. A commit ID for these new files does not yet exist remotely.

## Exact remaining gap / next action

For the research result: independently audit the proposed all-degree proof, especially the odd-color filtration, 2-integrality, and the characteristic-zero-to-integral pattern step. If a gap is found, record its exact location and retain only the verified scoped consequences. This audit should be bounded and should not interrupt a real geometric construction by Opus.

For the counterexample: D01 still needs a smooth concordance K0 -> K1 in standard S3 x I (or an equivalent standard-B4 slice disk); KDG still needs global nonribbonness. A failure or closure of this Jones test family supplies neither. The single immediate action is the proof audit in `OPUS_REVIEW.md`, then a reasoned pivot back to a missing geometric certificate or a genuinely different ribbon-specific obstruction.
