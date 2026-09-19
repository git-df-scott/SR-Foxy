# Exact endpoint audit of the first two live search checkpoints

19 September 2026. **No Slice-Ribbon counterexample established.** This is an additive, read-only audit of the running search's evidence. Neither its workflow nor its scientific inputs were edited or restarted. No historical novelty is claimed.

## Scope and recorded runtime

Run: `35455048082`, launched at commit `042a7dfc6fe61967902e1c4f7174af5f6342862c`.

The inspected artifacts are:

- Checkpoint 1, artifact `10587559866`, SHA256 `ed95f67285a105410eaefd8e0354b1343af90831969a69e802efa5b50dab334c`.
- Checkpoint 2, artifact `10589240719`, SHA256 `41b015d6114e936a4514573042377e01a3aefa74caa4a89b7479ffd7ed26d0cc`.

The second checkpoint closes at **17:29:36 UTC**. It records two completed common-upper segments, with **3600.021043032 seconds search wall time** and **3579.326956595 seconds CPU time**. This is one recorded hour, NOT seven hours. Queueing, setup, smoke tests, local audit computations, and the unfinished remainder of the run are not included.

Aggregate attempt counters: **167,163 attempts**, comprising **21,063 new endpoint nodes**, **145,976 duplicate endpoint records**, and **124 attempts without a sampled band**. There are **21,067 stored nodes including four roots**. These are diagrams/search states, not a claimed number of distinct knots. No UNKNOWN_ERROR, UNKNOWN_TIMEOUT or nomination occurs in these two completed search segments.

These two segments sampled augmented dual-face paths crossing at most two and three edges respectively, with absolute half-twist bounds four and six, at most two birth/fusion stages, crossing cap 72, and at most 48 reduction RIII trials. The full workflow has later bounds, but they are not covered by this checkpoint audit. Sampling is not exhaustive enumeration of these bounds.

## The new finite result

**For each of the two target families, every left endpoint stored in checkpoint 2 is different from every right endpoint stored there.** This conclusion is stronger than the search runner's failure to match diagram signatures: the audit compared knot invariants that do not depend on the drawing.

The chain of exact tests was:

1. Calculate the full Jones polynomial of all **21,067 stored diagrams** with Regina. The Abe-Tagami sides have **zero shared Jones classes**. The smaller K7a2/K10n4 sides have **four** shared Jones classes.
2. Calculate HOMFLY-PT for all **315 diagrams** in those four classes. One whole class separates; three remain.
3. Calculate cyclic-cover integral H1 directly from the PD for the remaining **184 diagrams**, at degrees two, three and four. Cross-check degree four using SnapPy's cyclic covers. This removes further potential matches but leaves **141 diagrams** participating in unresolved cross-side classes.
4. Enumerate all connected degree-four covers of those 141 knot exteriors and compare the multisets of their integral first homology groups. The independent enumeration options `low_index` and `snappea` agree at every node. **No opposite-side homology spectrum matches remain.** All 141 computations completed; none remains UNKNOWN.

Different spectra obstruct even unoriented homeomorphism of the knot exteriors. Numerical volumes were used only in an exploratory probe and are not evidence for the final exclusions. The two cover enumerators share SnapPy's triangulation and integral homology implementation; that implementation is trusted, not formally verified here.

This is a finite exclusion of the SAVED endpoints. It does not obstruct concordance of the original pair, exclude future endpoints, prove a whole parameter box empty, or replace the missing slice disk.

## Independently checked small witnesses

The first checkpoint contained two particularly deceptive classes: opposite sides shared Jones, HOMFLY-PT, and the full computed bigraded knot Floer homology. All **42 diagrams** in those two classes were checked with the HFK implementation. Their fourfold cyclic-cover homology nevertheless separates the sides.

For representative nodes, with `0` denoting a free Z summand:

| Node | H1 of fourfold cyclic cover | dim H1 over F5 |
|---|---|---:|
| 510 | Z/75 + Z/1425 + Z | 3 |
| 2482 | Z/5 + Z/5 + Z/15 + Z/285 + Z | 5 |
| 3761 | Z/5 + Z/5 + Z/5 + Z/855 + Z | 5 |
| 1808 | Z/25 + Z/4275 + Z | 3 |

Thus nodes 510/2482 and 3761/1808 cannot represent the same knot, despite the weaker equalities.

`CYCLIC4_WITNESSES.json` preserves their exact PD inputs. `verify_cyclic4.py` needs only Python's standard library. It independently reconstructs the Wirtinger presentation and the cyclic-cover relation matrix, then verifies the differing mod-5 Betti numbers. It rejects eight deliberately corrupted witnesses. It verifies these four fixed separations, NOT the entire 21,067-diagram audit.

The complete downloadable evidence also contains integral Smith decomposition certificates for these four matrices. A separate standard-library checker verifies U*M*V=D, det(U)=det(V)=+/-1, and the mod-5 ranks; twenty corrupted matrix/input certificates are rejected. The independent PD-derived cyclic calculation was calibrated against twelve knot/degree controls, and agreed with SnapPy on all 42 first-checkpoint and all 184 second-checkpoint collision diagrams at degree four.

### Why the elementary calculation computes the claimed group

A Wirtinger presentation complex has the knot group and one vertex. Send every oriented meridian to 1 in Z/k. Lift each generator edge and relator to the k-sheeted cover. Contract the first k-1 lifted edges of one meridian; they form a spanning tree. Signed edge counts of the lifted relators, after deleting the tree-edge columns, present H1. Smith form computes integral H1; row reduction modulo five computes H1 over F5. Higher cells do not change H1. The connected cyclic cover is preserved by a knot equivalence, including reversal of the meridian, so unequal Betti numbers are valid separations.

## Ledger and movie checks

Both downloaded archive digests match GitHub's advertised hashes. Both SQLite integrity checks pass. The entire 10,309-node prefix of checkpoint 1 is byte-identical within checkpoint 2. Source hashes match the saved preflight controls. Every parent/depth/death ledger in both databases was checked, and **200 deterministically selected complete movie chains per checkpoint** were replayed successfully through the deployed native runner.

That replay shares Spherogram with the producer. It is not an independent verification of every saddle or every isotopy. No nomination has been promoted into a counterexample.

The pinned installed package versions were SnapPy 3.3.2, Spherogram 2.4.1, Regina 7.4.1, SymPy 1.14.0 and NetworkX 3.6.1. Regina's internal `versionString()` reports 7.4; the wheel/distribution version is 7.4.1.

Local execution notes: direct package installation was unavailable, so the existing authorized wheelhouse artifact was used offline. A coefficient-to-int adapter and a missing SnapPy import were corrected before accepting results. The local 60-second execution wrapper interrupted the full-cover postprocessor twice; its saved records were resumed and all 141 nodes completed. Its last-invocation timer is not total audit runtime. None of this restarted the GitHub search.

## Reproduction and publication limits

Run the independent fixed-witness check from the repository root:

```sh
python results/astra_2026_09_19_live_checkpoint_audit/verify_cyclic4.py
```

The accompanying downloadable ZIP preserves both original checkpoint ZIPs, complete per-node polynomial/cover results, integer certificates, checker source, ledger audit, and reproduction instructions. This directory publishes the report and compact independently replayable witnesses; it does not contain the two large checkpoint databases. No existing scientific report was overwritten. The original seven-hour workflow and its result watch remain separate from this finite audit.
