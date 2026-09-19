# Pass 01 — direct four-parallel gate for KDG

17 September 2026 UTC. **NO COUNTEREXAMPLE. No four-parallel calculation has been run in this environment.**

The low-wrapping audit leaves degree four as the first unexcluded annular support. There is no need to invent a Bing pattern before testing whether degree four contains any information at all: use the canonical four-parallel pattern

`P = z^4`.

## Why this is an admissible ribbon pattern

`P(U)` is the four-component unlink under the standard untwisted embedding of the solid torus, so `P` is a ribbon pattern in Eisermann Definition 6.12. Its geometric wrapping number is four and its annular Kauffman bracket is exactly `z^4`; in the notation of the prior gate, the leading coefficient is

`a(A)=1`, hence `a(alpha)=1`.

For a ribbon companion, Eisermann Corollary 6.15 independently states that every zero-framed cable is a ribbon link. Thus `6_1^4` is a positive theorem-level control.

## Exact target condition

Let `B4(K)` denote the unnormalized bracket of the zero-framed four-parallel, with

`delta = q + q^-1 = q^-1(q^2+1)`

in the `q` convention used by `scripts/jones_root_jet.py`.

For a four-component ribbon link, Theorem 1 requires normalized Jones nullity three. Since the bracket carries one additional `delta` factor, the direct necessary condition is

`B4(KDG)` divisible by `delta^4` **in characteristic zero**.

If this exact divisibility fails at any lower order, `KDG^4` is not ribbon. Because the four-parallel pattern is ribbon-preserving, ribbonness of KDG would imply ribbonness of `KDG^4`; therefore such a failure would give a global nonribbon obstruction to the already-slice KDG and would trigger counterexample verification.

If exact divisibility holds, define

`e4(KDG) = [B4(KDG)/delta^4]_(q=i)`

with the same writhe normalization as the saved root-jet code. Eisermann Theorem 2 then requires

`e4(KDG) == 25^4 == 1 (mod 32)`.

So this one object simultaneously tests the missing four-parallel nullity and the mod-32 determinant congruence.

## Minimal root jet

Write `h=q^2+1`, so `delta=q^-1 h`. To decide exact divisibility by `delta^4`, an exact remainder modulo `h^4` suffices. To recover the quotient at `q=i`, one further order is necessary: compute the bracket in

`Z[q,q^-1]/(h^5)`.

No full Jones polynomial is required. Conveniently, `scripts/jones_root_jet.py` already sets `Jet.order=m+1`; for `m=4` components this is exactly order five. Its quotient routine divides by `h^4` and converts back to the `delta` quotient.

A modular run over `Z/32` is useful only as a cheap hit detector:

- a nonzero lower remainder modulo 32 certifies that the exact lower remainder is nonzero, hence exact divisibility fails;
- a zero lower remainder modulo 32 does **not** prove exact divisibility, because the exact remainder could be a nonzero multiple of 32;
- a quotient mismatch modulo 32 is only a candidate determinant obstruction until exact divisibility has been established.

An exact-integer rerun is mandatory before calling a target hit mathematical.

## Prepared input construction

The stored KDG card `data/knots/18nh00000601.json` contains a seven-strand braid word of length 34 and writhe zero. `scripts/cable.py` already implements the Seifert-framed `p`-cable by replacing every braid generator with a `p x p` block and adding the framing correction `q-p*w`. For `p=4`, `q=0`, and `w=0`, there is no extra twist correction. The raw cabled braid therefore has `34*16=544` crossings before simplification. This is a construction count, not the final diagram crossing number or a runtime estimate.

`run_kdg_4parallel_gate.py` in this checkpoint prepares the exact PD input, verifies four components, planarity, and zero pairwise linking, and then calls the existing root-jet engine with bounded resources. It has not been executed here because SnapPy/Spherogram are not installed in this automation container.

## Controls and stop rules

1. Build `6_1^4` through the identical cable path. Its modular necessary conditions must pass before interpreting KDG.
2. Save the exact PD and linking matrix before the Jones calculation.
3. Run one target calculation at a time. A timeout or resource kill is UNKNOWN.
4. A modular KDG hit is only a nomination. Rerun exact integer arithmetic and independently verify the cable framing and knot source before invoking the counterexample implication.
5. An exact KDG hit immediately stops pattern exploration. Audit Oliveira-Smith's standard-`B^4` sliceness theorem and the ribbon-pattern implication independently.
6. If the exact KDG four-parallel passes, the result excludes only this direct pattern. Do not infer that all degree-four patterns pass; a two-component degree-four pattern can probe a different linear functional of `B4`.

## New progress supplied by this pass

The first unexcluded degree-four pattern is now explicit and theorem-certified: **the four-parallel itself**, with maximal coefficient `a(alpha)=1`. The next computation therefore has no pattern-construction ambiguity. The only substantial missing input is the four-parallel root jet.
