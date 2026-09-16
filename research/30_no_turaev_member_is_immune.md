# No Turaev Theorem I member is immune to the obstruction that killed the first one

16 September 2026. **No counterexample to the Slice-Ribbon Conjecture was found.**
This note proves a small theorem that closes the natural next move in the Turaev
lane. It is a **negative result**, and it is proved rather than searched.

## The situation it answers

`results/turaev_family_status.md` records that `A(1,1,1,1)` — the only realised
member of Turaev's Theorem I family — was killed on 12 September by
`slice_obstruction_HKL` returning **`(3, 13)`**: a character of order 13 on the
**3-fold** branched cover, proving the knot is not topologically slice.

That same file had predicted immunity for the `q = 1` subfamily, on the grounds
that `det = (2q-1)^2 = 1` makes `H_1(Σ_2)` trivial and the `Σ_2` Casson–Gordon
test vacuous. It then recorded its own correction: the argument "rules out only
the `Σ_2` flavour of the test. HKL fired here at `p = 3`, i.e. on the **3-fold**
branched cover."

So the obvious next move is: **find a member for which the higher covers are
trivial too, and build that one.** The family is infinite — `p = 1` or prime,
`q ≥ 1` (with `q ≠ 2` if `p = 2`), `r, s` both nonzero — and only one member has
ever been built. This note shows that move cannot work.

## The arithmetic

For the Turaev family, `Δ_K(t) = t^3 ρ(t) ρ(1/t)` with

```
ρ(t) = p t^3 - (p+q) t^2 - (p-q+1) t + p
```

and `|H_1(Σ_n(K))| = ∏_{j=1}^{n-1} |Δ(ζ_n^j)|`. Since `ρ` has real coefficients,
`ρ(1/ζ) = conj(ρ(ζ))` on the unit circle, so `|Δ(ζ_n^j)| = |ρ(ζ_n^j)|^2` and

```
|H_1(Σ_n)| = R_n^2,     R_n = |∏_{j=1}^{n-1} ρ(ζ_n^j)| = |Res(ρ, 1 + t + ⋯ + t^{n-1})|.
```

Every branched cover of every member has square homology, and `R_n` is what
decides whether characters exist at all. **`R_n` depends only on `(p,q)`** — `r`
and `s` are `l_2` data and never enter the Seifert matrix — so this is a property
of a whole `(r,s)`-family at once.

## The theorem

> **`R_3 = 1` is impossible. `|H_1(Σ_3)| ≥ 169` for every Theorem I member.**

*Proof.* Let `ω` be a primitive cube root of unity, so `ω^3 = 1` and
`1 + ω + ω^2 = 0`, hence `ω^2 = -1-ω`. Then

```
ρ(ω) = p - (p+q)ω^2 - (p-q+1)ω + p
     = 2p + (p+q)(1+ω) - (p-q+1)ω
     = (3p+q) + (2q-1)ω
     = A + Bω,      A = 3p+q,  B = 2q-1.
```

Therefore `R_3 = ρ(ω)ρ(ω̄) = A^2 - AB + B^2`, which is exactly the **Eisenstein
norm form** `N(A + Bω)`. Expanded,

```
R_3(p,q) = 9p^2 + 3p + 3q^2 - 3q + 1.
```

The norm form `x^2 - xy + y^2` represents 1 only at the six units,
`(x,y) ∈ {(1,0),(0,1),(1,1)}` up to sign — verified by exhaustive check in the
script. An admissible member has `p ≥ 1` and `q ≥ 1`, so `A = 3p+q ≥ 4`, and no
unit has `|x| ≥ 4`. Hence `R_3 ≠ 1`, and in fact `R_3 ≥ 13` with the minimum at
`(p,q) = (1,1)`. ∎

**Verification.** The closed form was checked against the resultant
`|Res(ρ, 1+t+t^2)|` for `p ∈ {1,2,3,5,7,11,13}` and `q ∈ {1,…,11}`: **zero
mismatches**. Two further controls pass: `R_2 = |2q-1|` across the grid, which
reproduces the stored determinants `(2q-1)^2`, and **`R_3(1,1) = 13` exactly** —
the `13` in the `HKL_agent (3,13)` that killed `A(1,1,1,1)`. Reproducing the kill
from independent arithmetic is what makes the rest of the table trustworthy.
`scripts/turaev_hkl_vacuity_search.py`.

## What it means, stated carefully

**Every** member of Turaev's Theorem I family has a 3-fold branched cover with
nontrivial homology, of order at least 169. So Casson–Gordon and HKL **always
have characters to test** — there is no member anywhere in the family for which
the machinery is structurally unable to fire, at any `(p,q)`, for any `(r,s)`.

Two things this does **not** say:

* It does **not** prove every member is non-slice. Having characters is not the
  same as an obstruction firing. HKL could return `None` on some member.
* It does **not** retract the certificate. Theorem I members with `r,s ≠ 0` really
  are algebraically slice and really are not homotopy-ribbon; if one were smoothly
  slice it would still be a counterexample.

What it removes is the *reason to expect* one to survive. The campaign built the
member with the **smallest possible** `H_1(Σ_3)` in the entire family — `R_3 = 13`
at `(p,q) = (1,1)`, the literal minimum of the Eisenstein form over the admissible
range — and HKL killed it at exactly that prime. Every other member has strictly
more homology on the 3-fold cover, hence strictly more characters, hence strictly
more chances for the obstruction to fire.

A wider sweep is in the table: `R_5`, `R_7`, `R_11`, `R_13` are large and growing
for every `(p,q)` tested, and **no member has all of `Σ_2, Σ_3, Σ_5, Σ_7, Σ_11,
Σ_13` trivial**. Only `q = 1` buys `Σ_2`, which is the observation that already
proved insufficient.

## Consequence for the campaign

Building `A(1,3,1,1)` or `A(2,1,1,1)` — `results/turaev_family_status.md`'s
suggested next members — is a **worse** bet than the one already tried, not a
better one: `R_3` is 31 and 43 respectively against 13. The honest ranking of the
Turaev lane drops accordingly. It should not be the next place compute goes, and
`research/29`'s framing of it as the promising fourth lane is weakened further by
this note than by the `A(1,1,1,1)` kill alone.

If anyone does return to it, the thing to look for is not a smaller cover but a
member on which HKL happens to return `None` despite having characters — which is
a search over built knots, needs Sage, and has no structural argument behind it.
