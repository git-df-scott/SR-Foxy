# Exact Jones distinction of the stored K0 and K1 diagrams

The stored six-crossing K0 PD and nineteen-crossing K1 PD have different Jones
polynomials. K0 also differs from the mirror of K1, and K1 differs from its own
mirror. These conclusions do not require Sage, numerical hyperbolic geometry,
or recognition of a canonical triangulation.

This identifies invariants of the **stored PD diagrams**. Their identification
with specific paper figures remains a separate input-provenance question.
Nothing here establishes sliceness or concordance.

## Exact method and conventions

For a cyclic Spherogram PD tuple `(a,b,c,d)`, opposite ports are the strands,
and ports 0 and 2 are undercrossing. The A-smoothing joins `(a,b),(c,d)` and the
B-smoothing joins `(a,d),(b,c)`. We use

```
delta = -A^2 - A^-2
<D> = sum_states A^(N-2*number_of_B_smoothings) delta^(number_of_circles-1)
F_D(A) = (-A^3)^(-writhe(D)) <D>
V_D(t) = F_D(A), with t = A^-4 and V_unknot = 1.
```

Thus this is the usual single-variable knot Jones convention, not Spherogram's
new default variable whose exponents are twice as large. A global choice of
the reciprocal variable would not affect any distinction claimed here.

The writhe calculation orients the actual strand graph, independently of arc
label numbering. A crossing is positive when the incoming ports are `(0,3)`
or `(2,1)`. This agrees with `Crossing.orient` and `Crossing.is_incoming` in
the official Spherogram source. All inputs are checked to have one component.

`state_histogram.c` enumerates every smoothing state with a disjoint-set data
structure on arc labels, counting the histogram `(number_of_B_smoothings,
number_of_circles)`. The histogram and all input PDs are retained in
`RESULTS.json`. Python expands the powers of delta and normalizes with exact
arbitrary-precision integers. The complete polynomials, rather than just their
evaluations, are saved.

The C helper rejects inputs above twenty crossings. Each invocation has a
15-second CPU cap and a 20-second wall cap. K1 has exactly 524,288 states; no
K2/K3 computation is attempted. Histogram counts are at most 2^20 and cannot
overflow their 64-bit unsigned storage. The helper's state memory is O(N).

## Results

In increasing powers of t:

```
V_K0 = -t^-3 + 2t^-2 - 2t^-1 + 3 - 2t + 2t^2 - t^3

V_K1 = -t^-9 + t^-8 - t^-7 + t^-6 + t^-4 - t^-3
       + 2t^-2 - 2t^-1 + 2 - 2t + t^2 - t^4 + t^5
```

Their supports already distinguish K0 from both K1 and its mirror.
As a compact exact modular witness, evaluating F(A) at A=2 modulo the prime
1,000,000,007 gives:

| Diagram | Evaluation |
| --- | ---: |
| K0 | 677486626 |
| K1 | 466405112 |
| mirror K1 | 946929546 |

Negative exponents are interpreted using the multiplicative inverse of 2.
Mirror inversion is `F_mirror(A)=F(A^-1)` or `V_mirror(t)=V(t^-1)`.

## Verification

The checks include:

- Crossingless unknot; positive and negative Reidemeister-I curls, including
  their bracket factors `-A^3` and `-A^-3` and their writhe signs.
- The negative trefoil `t^-1+t^-3-t^-4` and figure-eight
  `t^-2-t^-1+1-t+t^2`.
- An independent Python implementation using explicit half-edge graphs and
  depth-first searches instead of the C label-based disjoint-set method;
  compared on every control and the six-crossing K0.
- Explicit mirrored PDs for the small controls, obtained by cyclically
  rotating every crossing tuple one port.
- State counts, one-component checks, integer Jones exponents, `V(1)=1`,
  `V'(1)=0`, and determinant check `|V(-1)|=13` for both stored diagrams.

The knot-diagram input and output stages still trust the stated PD convention
and the C/Python/compiler runtime. This is an auditable exact computation, not
a formally verified implementation.

## Reproduce

From the repository root, with Python 3 and a C compiler:

```
python3 results/night_2026_09_18_jones/check_jones.py
```

`inputs.json` preserves the two PDs and hashes of their original JSON files.
`RESULTS.json` records source hashes, runtime/compiler versions, conventions,
controls, full state histograms, exact polynomials, and the run timestamp.

Official convention references checked during this calculation:

- [SnapPy/Spherogram link documentation](https://snappy.computop.org/spherogram.html).
- [Spherogram crossing orientation implementation](https://github.com/3-manifolds/Spherogram/blob/master/spherogram_src/links/links_base.py).
- [Spherogram Jones variable conventions](https://github.com/3-manifolds/Spherogram/blob/master/spherogram_src/links/invariants.py).
