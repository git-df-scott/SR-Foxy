# Exact KDG four-parallel gate — completed, no counterexample

17 September 2026 UTC. Inputs pinned to `b71a29f3193bd725d41274e52efd3c6bdaa52b04`.

**NO COUNTEREXAMPLE.** The zero-framed four-component parallel of the stored KDG diagram passes both tested Eisermann necessary conditions. This is a completed targeted calculation, not a ribbon certificate and not a theorem that all satellite tests are ineffective.

## Exact result

For the 288-crossing four-parallel, the normalized Jones nullity is exactly **3**, and the reduced Jones determinant is **106081**. In particular,

```
106081 - 25^4 = -284544 = -8892 * 32.
```

The four-parallel of the ribbon control 6_1 gives **19681**, with nullity 3, and `19681 - 9^4 = 410 * 32`. The previously published three-parallel ribbon control gives **1785**, reproduced by the new engine.

## Computation, conventions, and certificate

The prepared SnapPy runner could not execute because this Linux container has no SnapPy/Spherogram/Regina and direct DNS resolution failed. No Mac process was started. Instead, a new standalone C++ frontier contraction and Python planar-diagram cabler were implemented and actually run.

Let `x=A^2`, `h=x^2+1`, and `delta=-x-x^-1`. The engine computes the unnormalized bracket/Jones quantity (unknot value delta) in `Z[x]/(h^5)`. Each crossing contributes the two smoothings `(01)(23)` and `(03)(12)` with respective weights `x` and `1`, with the common factor `A^-1` restored at the end. Writhe normalization is also applied; the cabled target has writhe zero. With `q=-x^-1`, the variable q equals i when x=i, and delta is `q+q^-1`.

The exact target residue is

```
106081 * (x^2+1)^4
```

with coefficient array `[106081,0,424324,0,636486,0,424324,0,106081,0]`. Vanishing of the remainder modulo `h^4` is exact, not inferred from modular zeros. The nonzero coefficient gives unnormalized order four, hence normalized Jones nullity three. Dividing by delta^4 and evaluating at x=i gives 106081.

The successful exact run used Boost's checked, signed 128-bit integer backend. Overflow throws an exception and cannot silently produce a result; this run completed without overflow. The source also supports arbitrary-precision `cpp_int`. A first arbitrary-precision run was externally interrupted with no value and is retained as UNKNOWN. The successful run used the reversed crossing order, finished its contraction in 28.2346 seconds, and retained at most 197612 states. The independent mod-32 run used the original order and finished in 27.1651 seconds. Jobs had a 3 GiB address-space cap; the successful exact run had a 40-second subprocess limit.

## Controls and limits

`validation.json` records 27 passing checks: independent full state-sum polynomial comparisons on nine small diagrams/unlinks, twelve Reidemeister-I checks, three planar/component/framing checks, an intentionally nonribbon Hopf-link divisibility failure, exact recovery of the prior control-input blob hash, and agreement of the target's exact and modular computations with different crossing orders.

Each of the four target components reduces to the original source diagram under deletion of the other components. The planar rotation-system Euler check gives 2, and every pairwise linking number is zero. The grid replacement is the blackboard parallel of a zero-writhe knot diagram, hence the Seifert-framed parallel.

This is not proof-assistant verification, nor an independent full-polynomial calculation for the 288-crossing target. The KDG knot identity and its standard-B4 slice disk remain upstream source dependencies. No new slice disk, concordance, or global nonribbon proof was produced.

## Reproduce

Requirements: Python 3 with SymPy, C++17 compiler, and Boost headers. No SnapPy, Sage, network, or Mac access is required.

```
python3 reproduce.py NEW_OUTPUT_DIRECTORY
```

The output directory must not exist. One calculation runs at a time. Timeout, overflow, and error states remain UNKNOWN. `--controls-only` runs only the ribbon controls. The full original local audit bundle also contains the original scripts, raw inputs, exact/modular logs, and the interrupted attempt.

## Checkpoint / next action

The four-parallel target is now **completed**. Do not relaunch it as an unfinished task. The next mathematical action is to check how this exact fourth-parallel jet closes the previously proposed degree-four satellite transfer gate, rather than automatically building a more complicated degree-four pattern or starting a five-parallel computation. No universal degree-four transfer theorem is asserted here.

## Sources and reading scope

- Michael Eisermann, *The Jones polynomial of ribbon links*, Geometry & Topology 13 (2009), 623–660; Theorems 1–2 and Corollary 6.15. https://arxiv.org/abs/0802.2287 . The necessary-condition statement is the established campaign dependency; no new literature-wide claim is made.
- KDG exact input: `data/knots/18nh00000601.json` at the pinned commit. https://github.com/git-df-scott/SR-Foxy/blob/b71a29f3193bd725d41274e52efd3c6bdaa52b04/data/knots/18nh00000601.json
- Ribbon control input: `results/astra_2026_09_16_followup/root_jet_final/ribbon61_3parallel.input.json`, blob `00135706508cf045df4fb19f5a6f6186df156a9a`, reproduced byte-for-byte before component extraction.
- The pinned `scripts/cable.py`, `scripts/jones_root_jet.py`, `tests/test_jones_root_jet.py`, and pass01 runner were read. The whole repository was not audited.
- Spherogram `exhaust.py`, blob `84b604d416d7e69ca43e6ed41bd584af2352b850`, was consulted for an alternative consecutive-frontier ordering heuristic. That heuristic was not used for the successful target run. https://github.com/3-manifolds/Spherogram/blob/master/spherogram_src/links/exhaust.py
