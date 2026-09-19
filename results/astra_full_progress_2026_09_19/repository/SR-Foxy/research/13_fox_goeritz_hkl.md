# Resolving the character/linking-form basis gap for D01

12 September 2026. **Result: no (2,13) HKL obstruction, even after imposing
actual isotropy.** This closes the specific ambiguity in the earlier direct
calculation, which left four of fourteen possible subgroups without computing
the linking form. It proves neither topological nor smooth sliceness.

## Exact question and conventions

D01 is the stored 25-crossing K0#(-K1). Its double branched cover has first
homology (Z/13)^2. To obstruct sliceness by this test, every invariant
metabolizer must admit an annihilating character whose reduced twisted
Alexander polynomial is not a norm. For a double cover, the deck action is
minus identity, so every line is invariant. Only the isotropic lines of the
nonsingular linking form are metabolizers.

The earlier SnapPy direct routine deliberately used a larger set of subgroups
of the correct size. The new implementation works directly from the PD diagram
and retains character coordinates throughout; it does not guess how a
separately computed linking matrix matches SnapPy's simplified generators.

## The explicit basis bridge

1. Construct Fox 13-colorings on Wirtinger arcs and fix the first arc to zero,
   removing constant colorings. The remaining vector space has dimension two.
2. Recover Dehn face colors by requiring the colors of faces on either side
   of an arc to sum to its Fox color. Fix one shaded face to zero and check
   every equation.
3. Restrict to unshaded face values and subtract the reference unshaded value.
   This gives a vector y in the kernel of the reduced Goeritz matrix G mod 13.
   The saved two vectors form the entire kernel.
4. With integral lifts, put v=Gy/13. For another kernel vector z, the inverse
   Goeritz linking form satisfies

   `lambda(v, Gz/13) = y^T G z / 13² mod Z`.

   Therefore the character pairing over F13 is `y^T G z /13 mod 13`.
   Changing an integral lift does not change this residue: Gy and Gz are
   divisible by 13. All divisions, ranks and the inverse-matrix identity are
   checked exactly. The relevant Smith factors are 13,13.

Fox/Dehn coloring and the Goeritz kernel are related by the explicit maps in
Traldi's paper; the relation to the branched-cover presentation is described
by Silver–Traldi–Williams. These are topological inputs to the computation,
not consequences of a successful matrix-rank check alone.

In the saved Fox basis the pairing matrix is

`B = [[9,2],[2,2]] over F13`.

For a projective character (1,a), its self-pairing is `9+4a+2a²`. Its only
zeros are a=3 and a=8; the remaining projective line (0,1) has value two.
A separate implementation constructs the other checkerboard matrix directly
from crossing corners and obtains **the same B in the fixed Fox coordinates**.
It recovers region colors by propagation instead of solving the first
implementation's linear system. Its initial expectation of an overall minus
sign was wrong; the failed assertion is preserved in the first checker log.
With the recorded crossing-sign convention, the pairings agree exactly.

## Twisted polynomials with tracked generators

For a Fox coloring x, use the metabelian matrices

`rho(g_i) = [[0, t*zeta^(-x_i)], [zeta^(x_i), 0]]`.

Each square is t times identity. The Fox relation makes every Wirtinger
relator evaluate to identity. Presentation simplification uses only explicit
Tietze generator eliminations. Every eliminated meridian is reconstructed
and checked against its original matrix, as are all original relators,
including the redundant one removed to obtain deficiency one.

The determinant calculation uses SnapPy's exact twisted-Alexander routine,
with its documented reduced convention (division by t-1). Norm checking is
up to Laurent units, as in the HKL theorem. Scaling a nonzero character
applies a cyclotomic Galois automorphism, so one representative of each of
the fourteen projective lines suffices for norm status.

Both isotropic lines give the same polynomial:

`Delta_chi(t) = (t-1)^2 * (t² + A t + 1)^2`,

where `A = zeta^11 + zeta^10 + zeta^3 + zeta^2 - 1` and zeta is a primitive
thirteenth root of unity. A is real under complex conjugation. If
`h(t)=(t-1)(t²+A t+1)`, then `bar(h)=-t^-3 h`, so

`Delta_chi = -t³ h bar(h)`.

This is an explicit norm certificate up to a Laurent unit. The second
implementation reconstructs the saved polynomial coefficients and verifies
this multiplication. Norms occur on exactly four projective lines, a=3,5,6,8;
the two nonisotropic survivors a=5,6 were unnecessary in the earlier test.
Both actual metabolizers survive, so removing them does not strengthen the
conclusion to nonsliceness.

## Controls and evidence

* The known ribbon knot 6_3#(-6_3) has two isotropic character lines; both
  yield independently multiplied norm certificates. Four of all fourteen
  lines pass, illustrating why nonisotropic failures cannot obstruct a
  slice knot.
* On 6_3 alone, the character form is [7] over F13 and its nonzero character
  has a nonnorm polynomial. Its homology has nonsquare order 13, so this
  one-dimensional case is a calibration, not a metabolizer search.
* Inputs, Fox and Goeritz bases, pairing matrices, all fourteen line values,
  exact cyclotomic coefficients, generator eliminations and norm certificates
  are stored in `results/fox_goeritz_D01_all.json` and
  `results/fox_goeritz_independent_check.json`.
* `scripts/hkl_fox_goeritz.py` generates the calculation;
  `scripts/verify_fox_goeritz.py` independently checks the opposite shading
  and explicit norms. The determinant algorithm is still a shared SnapPy
  dependency, not an independently implemented twisted-torsion engine.

## Primary sources checked 12 September 2026

* Lorenzo Traldi, *Link colorings and the Goeritz matrix*, Journal of Knot
  Theory and Its Ramifications 26(8) (2017), 1750045,
  DOI [10.1142/S0218216517500456](https://doi.org/10.1142/S0218216517500456),
  [arXiv:1701.04308v4](https://arxiv.org/html/1701.04308v4), Sections 2 and 4:
  explicit Fox/Dehn maps and Goeritz-kernel correspondence.
* Daniel S. Silver, Lorenzo Traldi and Susan G. Williams, *Goeritz and
  Seifert Matrices from Dehn Presentations*, Osaka Journal of Mathematics
  57 (2020), 663–677, [repository PDF](https://www.i-repository.net/contents/osakacu/sugaku/00306126-57-3-663.pdf);
  [2018 preprint](https://arxiv.org/pdf/1808.10296), Theorem 3.4 and its proof
  (Theorem 4.1 in the published version): region generators and the Goeritz
  presentation. The introduction identifies the double-cover linking form.
* Nathan M. Dunfield and Sherry Gong, *Ribbon concordances and slice
  obstructions: experiments and examples*, preprint, 26 December 2025,
  [arXiv:2512.21825](https://arxiv.org/pdf/2512.21825), Theorem 3.3, Sections
  3.4 and 3.20: metabolizer quantifiers, norm convention, and the deliberately
  larger candidate-subgroup set used without a linking-form calculation.

The next obstruction must use information beyond this double-cover test.
Higher cyclic covers remain separate questions. More double-cover (2,13)
reruns on the same input and characters cannot resolve its smooth sliceness.
