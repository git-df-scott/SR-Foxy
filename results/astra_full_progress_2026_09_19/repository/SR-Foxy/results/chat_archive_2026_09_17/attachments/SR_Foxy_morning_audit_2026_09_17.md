# SR-Foxy morning audit — 2026-09-17

**CE: NO.**

## Scope
Small audit of new Opus commits after Astra main head
`f7ba2516304c0553a3180570abb6e257f4a68094`.

Audited Opus commits:
- `ac5a2b839597b7e885b88325a41c54f0a402b9c2` — lifted surgery description.
- `3c73dd6552ef7d1d9e6ee375f925650069bfa1ed` — Sigma_2 geometry probe.

No broad search or new invariant computation was run.

## Verdict on the lifted-surgery result

**PARTIALLY VERIFIED, with one orientation-critical gap and one labeling gap.**

The code/artifact does support the following **unoriented/existential** statement:

> On the saved 34-tetrahedron representative of the 4-free-cusp cover, there are
> explicit slope vectors in the searched box whose fillings are certified by
> SnapPy `is_isometric_to` to be isometric to the independently constructed
> Sigma_2(K_1).

SnapPy documents that a `True` answer from `is_isometric_to` is rigorous.

However, the present script uses only
`bool(cand.is_isometric_to(target_mfd))`.
It does **not** request the isometries, record whether the successful isometry
preserves orientation, or transport any oriented peripheral data.

Therefore the artifact is **not yet a complete input for an orientation-sensitive
d-invariant calculation**. Before using it that way, record at least one successful
isometry with its orientation behavior (or compute an oriented isometry signature /
equivalent certified orientation check) and select a concrete slope vector.

## Cusp-pairing gap

The script records the four free cusp indices but not which two are the two lifts
of `c'_1` and which two are the lifts of `c'_2`.

Thus the sentence that the 59 hits reproduce the expected doubled-lift structure
because two cusps receive one slope and two receive the other is not, by itself,
a verification that the equal-slope pairs are the **geometrically corresponding
lift pairs**. A 2+2 numerical pattern does not identify the deck-transformation
pairing.

This does **not** invalidate the existential surgery description: any confirmed
slope vector on the saved 4-cusped link exterior that fills to the target is still
a surgery description of that unoriented target. It does matter if the argument
claims these are the actual lifted downstairs annulus-twist slopes.

## Additional reliability note

Exceptions while computing `M.homology()` are currently silently skipped rather
than recorded as `UNKNOWN`. This cannot create a false positive hit, but it means
the search accounting is not exhaustive as written.

## Geometry probe

Commit `3c73dd...` explicitly labels Sigma_2(K_1) only
`hyperbolic_numerically`, not verified hyperbolic, and records K_2 as NOT ATTEMPTED
after timeout. That scope is appropriate. Its matching numerical volume is a
cross-check, not a proof of the missing orientation data above.

## Exact remaining step

For the surgery/d-invariant lane, before computing any d-invariants:

1. choose one saved successful slope vector;
2. recover/record the cusp pairing induced by the covering map;
3. obtain the successful isometry with orientation information and certify the
   oriented identification with Sigma_2(K_1).

Separately, D01 still lacks a smooth disk/concordance in standard B^4 / S^3 x I,
and KDG still lacks a global nonribbon proof.

## Next action
Have Opus/Codex add an **orientation-and-cusp-pairing certificate** for one of
the 59 successful fillings. Do not start the intersection-form or d-invariant
calculation until that certificate exists.
