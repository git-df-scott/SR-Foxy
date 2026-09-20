# Exact audit of the Dunfield–Gong flagship

Cutoff: 2026-08-30. Verdict: **NO CE**. This file records exact inputs and closes
three misleading routes without treating a failed search as a theorem.

## 1. Exact knot input

The Dunfield–Gong data archive [S23] gives the following PD code for
`18nh_00000601`:

```text
[[12,2,13,1],[2,31,3,32],[32,3,33,4],[4,33,5,34],
 [34,5,35,6],[15,7,16,6],[7,15,8,14],[8,35,9,36],
 [26,9,27,10],[10,25,11,26],[18,11,19,12],
 [13,16,14,17],[36,18,1,17],[19,25,20,24],
 [27,21,28,20],[21,29,22,28],[29,23,30,22],
 [23,31,24,30]]
```

The same row records

```text
Δ(t) = t^10-2*t^9+t^8-t^7+4*t^6-7*t^5+4*t^4-t^3+t^2-2*t+1
det(K) = 25
```

SnapPy 3.3.2 reproduces the paper's genus-five fibered knot Floer package:

```text
fibered = True; genus = 5; epsilon = nu = tau = 0; total rank = 25
HFK ranks = {(-5,-5):1, (-4,-4):2, (-3,-3):1, (-2,-2):1,
             (-1,-1):4, (0,0):7, (1,1):4, (2,2):1,
             (3,3):1, (4,4):2, (5,5):1}
```

## 2. The published band search is not an exclusion

[S03, §2.2] explicitly says that band arcs have infinitely many isotopy classes,
that twist choices are unbounded, and that no bound is known for the arc complexity
needed to encode a ribbon disk. Sections 2.3 and 2.8 describe the actual finite
heuristic: mostly simple paths of length at most six and searches requiring at most
four bands. The authors stopped after the four-band pass because it was expensive.

Therefore neither of the following is certified:

- `fusion number > 4`;
- `K` has no ribbon disk with at most four bands.

The computation only says that no disk was found in the searched diagrammatic
subspace. Any plan that begins with "the cases r <= 4 are excluded" has a false
premise.

## 3. What Oliveira–Smith actually constructs

[S01, Figure 9 and Theorem 1.2] constructs an explicit two-component R-link

```text
L = K_G ∪ U.
```

It comes from turning the known ribbon-disk exterior of the 31-crossing
zero-surgery friend upside down and pulling the extra component through the RBG
homeomorphism. Theorem 3.3 of Miller–Zupan then makes `L` stably equivalent to a
six-component link `K_G ∪ L+`, where the five-component `L+` is a Casson–Gordon
derivative. The paper does **not** draw or tabulate `L+`.

The standardization of the associated sphere slides a 2-handle over a dotted
1-handle, cancels one Hopf pair, and invokes Gabai's Property R theorem for the
remaining one-handle/one-two-handle pair. This proves the ambient sphere is
standard. It does not give an ordinary component-preserving handleslide of `L` to
an unlink, and it does not turn the unspecified R-link derivative `L+` into an
unlink derivative. The marked disk question is exactly why [S01, Questions 3.3 and
3.4] remain open.

## 4. Two obstruction routes are structurally neutralized

### Turaev's multiplace form

The full primary statement has now been recovered. Turaev [S20, Theorem H(ii)]
states that the relevant two-place form of a ribbon knot is metabolic. In the proof,
Lemma 7.2 gives the same conclusion for a smooth slice disk when the induced map on
the commutator-quotient group is surjective.

Miller–Zupan [S02] show that a handle-ribbon disk has a disk-exterior handle
decomposition whose upside-down form makes

```text
π₁(S³ - K) → π₁(B⁴ - D)
```

surjective. The induced commutator quotient is therefore also surjective. Since
Oliveira–Smith's disk is handle-ribbon in the standard `B^4`, Turaev's metabolic
condition is already forced for this disk. It cannot distinguish this candidate's
known handle-ribbon status from ribbonness.

### HKL/twisted-Alexander ribbon tests

[S03, Theorem 3.12] obstructs topological homotopy-ribbonness. Handle-ribbon implies
homotopy-ribbon, so that theorem cannot obstruct `K_G`. The empty `HKL_ribbon_obs`
field for `18nh_00000601` in [S23] is consistent with this logical implication; it
is not merely a missing computation.

## 5. Reproducible geometric fingerprint (numerical, not a proof)

Using the exact PD code above with SnapPy 3.3.2 gives:

```text
tetrahedra = 14
H1 = Z
volume = 11.934508149946334086071209092163058047125889932960031930366128122
isometry signature = ovLLLMPPPQcegfijkklkmnlnmngeexigvusqtexov
link symmetry group = Z/2
amphicheiral = True
invertible as a knot = False
extending cusp maps = [[1,0],[0,-1]] and [[1,0],[0,1]]
```

Twelve independent randomized triangulations returned the same signature and the
same link symmetry data. The standalone Python wheel cannot invoke Sage's rigorous
interval verifier, so this is a high-confidence computational fingerprint, **not**
a theorem-level symmetry certificate. A small ambient symmetry group also does not
enumerate derivative links on the fiber.

## 6. The certified-non-ribbon flank

[S03, Table 8 and Theorem 3.12] gives 24 knots that are not even topologically
homotopy-ribbon, while their smooth and topological sliceness remain unknown:

```text
17nh_0630889   18nh_09292518  18nh_13798702  18nh_25872205
19nh_000130563 19nh_000130564 19nh_001561948 19nh_001746199
19nh_001785287 19nh_015088058 19nh_020746102 19nh_026824671
19nh_032393076 19nh_035320248 19nh_035487682 19nh_055867647
19nh_068872115 19nh_083547570 19nh_109593374 19nh_144186247
19nh_144186248 19nh_146789683 19nh_150081216 19nh_169852405
```

All have Alexander polynomial
`t^4 - 2*t^3 + 3*t^2 - 2*t + 1 = (t^2 - t + 1)^2`.

A streaming audit of both zero-friend tables in [S23] found no occurrence in the
main `zero_friends.csv`. Exactly one of the 24 occurs in
`more_zero_friends.csv`: `19nh_001785287`. Its recorded 82-crossing zero-friend has
determinant 9 and the same Alexander polynomial, but its `slice` and `ribbon` fields
are both `0` (unknown). Thus this is the only Table 8 target with a recorded trace
partner in the extended search, but the partner does not yet certify sliceness.

## 7. Next exact strikes

1. Recover the five-component CG derivative `L+` by executing the constructive
   stable-equivalence proof on Oliveira–Smith's exact Figure 9 R-link. If `L+` is an
   unlink, this produces a ribbon disk and kills the flagship candidate.
2. Search for a *marked* handleslide sequence that preserves enough of the `K_G`
   cocore to yield an unlink derivative. Ordinary unmarked sphere
   standardization is insufficient.
3. For `19nh_001785287`, reconstruct the zero-surgery homeomorphism/RBG link to its
   recorded friend and attempt a standard `S^4` trace embedding. If successful,
   Theorem 3.12 already supplies non-ribbonness, so this route avoids a global
   ribbon-disk exclusion.
4. Do not spend further time applying any obstruction whose conclusion is only
   "not homotopy-ribbon" to `K_G`; its known disk already defeats the hypotheses.

## Storage discipline

The 1,022,355,830-byte [S23] archive was not downloaded. ZIP central-directory and
HTTP range requests recovered the exact small code/CSV members; the largest saved
range was 1.22 MB. The two 28–29 MB bzip2 tables were streamed through the matcher
without being stored.
