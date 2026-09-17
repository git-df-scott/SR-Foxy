# Centered proof repair and a direct D01 test

17 September 2026 UTC. Scientific repository inputs pinned to `7a74678daccd9f3148b25a22a3f84a82eb1d374b`.

**NO COUNTEREXAMPLE. No new concordance or smooth disk.** This pass repaired a false displayed identity in the proposed all-degree transfer argument and performed targeted exact tests on the actual stored D01 diagram. Both tests pass. A passing necessary condition is not positive evidence sufficient to establish sliceness.

## Strongest new results

1. The draft's equation `L_n(r^n)=(-1)^((n-epsilon)/2)2^n n!` is false. It must read `L_n((r+1)^n)=...`. The n=1 and n=2 counterexamples are 1 versus 2 and -4 versus -8. `CENTERING_ERRATUM.md` gives the corrected all-degree argument; `CORRECTED_TRANSFER_THEOREM.md` integrates the repair without overwriting the original draft. The connected-sum leading formulas are unchanged. No further gap was found in this pass, but the corrected proof has not been externally reviewed or formalized.
2. The stored D01 zero-framed two-parallel has exact reduced Jones determinant -47 and normalized nullity 1. Its three-parallel has determinant -27911 and normalized nullity 2. These are new completed diagram evaluations in this pass, not solely algebraic predictions.
3. Direct D01 jets agree with the generic colored connected-sum formulas applied to K0 and the mirrored K1, to the full available order. This checks a separate algebraic route against the diagram calculation; it is not an independent topology-library certificate.

## Computed values

All displayed divisibility tests were in characteristic zero, using `Z[x]/((x^2+1)^5)`, where x=A^2 and delta=-x-x^-1. The computed nonzero quotient at x=i gives exact normalized nullity p-1 for each p-parallel. The component determinants and K0 two-parallel are controls already recorded in the project, not discoveries.

| Knot | p | Diagram crossings | Exact quotient | Residue modulo 32 | Contraction seconds |
|---|---:|---:|---:|---:|---:|
| K0 | 1 | 6 | 13 | 13 | 0.000078 |
| K0 | 2 | 24 | -23 | 9 | 0.000263 |
| K0 | 3 | 54 | -1067 | 21 | 0.002084 |
| K1 | 1 | 22 | 13 | 13 | 0.000145 |
| K1 | 2 | 88 | -23 | 9 | 0.008611 |
| K1 | 3 | 198 | -1067 | 21 | 4.4413 |
| D01 | 1 | 28 | 169 | 9 | 0.000244 |
| D01 | 2 | 112 | -47 | 17 | 0.020662 |
| D01 | 3 | 252 | -27911 | 25 | 20.7426 |

The K1 and D01 crossing counts include three Reidemeister-I curls to set blackboard writhe to zero before parallelization. They are not claims about minimal crossing number.

For D01 the two congruence differences are

```
-47 - 169^2 = -894 * 32
-27911 - 169^3 = -151710 * 32.
```

The summand values give the same results:

```
e2(D01) = -23 -23 -1 = -47
e3(D01) = (-1067)*13 + 13*(-1067) -13*13 = -27911.
```

Equality of these few values for K0 and K1 proves neither concordance nor equality of their full colored Jones invariants. No such stronger claim is made.

## Controls and independent arithmetic

`audit_centered_kernel.py`: 2792 passing exact checks through degree 20, using cleared integer denominators rather than the prior kernel-series implementation. Its finite tests supplement, not replace, the corrected all-degree proof.

`check_jet_composition.py`: three cleared composition identities verified modulo `(x^2+1)^5`, plus one deliberately false two-parallel perturbation rejected. It reflects the K1 jet by x -> x^-1 rather than assuming unmirrored full jets equal. Agreement is at the jet order, not full-polynomial equality.

`validate_target_geometry.py`: 29 checks. Each cable has a planar rotation system, the stated component count, zero total writhe and zero pairwise linking. Each component reduces under deletion of the others to the zero-writhe source diagram. Input and source-subset hashes match. A separate full 64-state sum for K0 matches the frontier jet. A tampered PD fails multiplicity validation.

The exact C++ engine and PD cabler are unchanged dependencies from pass02, identified by their Git blobs in `DEPENDENCIES.json`. Boost checked 128-bit arithmetic throws on overflow; all nine target/control runs completed without overflow. Jobs were serial with a 2 GiB address-space cap, 30-second subprocess cap and explicit CPU cap. Fifty deterministic diagram-order seeds were tested per job. The original stdout, stderr, diagrams, orders and result files are retained in the audit archive.

## Interpretation and next action

The corrected transfer argument supplies only these two numerical necessities for satellites of smooth slice knots. It does not provide a disk, settle Slice-Ribbon, or eliminate all quantum invariants. D01's missing step remains a smooth concordance K0 -> K1 in standard S3 x I, equivalently a smooth disk for the correctly identified difference in standard B4. KDG still lacks global nonribbonness.

Do not repeat D01 p=2 or p=3 as unfinished work. Do not automatically launch D01 p=4 or KDG p=5. The next constructive action is to audit one actual changed-axis or nonlocal concordance construction from the geometry lane, with explicit bands, framings, marked boundary and ambient-standardness proof. Algebraically conjugate words alone are not such a construction. If no such object has been saved, the next pass should construct one marked diagram rather than repeat the Turaev audit or another menu of invariants.

## Reproduction and saved evidence

Use Python 3, SymPy, a C++17 compiler, and Boost headers. No Sage, SnapPy, Spherogram, Regina, Mac access, credentials, or network is required.

```
python3 reproduce.py NEW_OUTPUT_DIRECTORY
```

This creates a fresh work directory, compiles the pinned portable engine, runs one calculation at a time, and writes explicit failures as unknown. It never overwrites the saved historical evidence. A full local audit archive also retains every original per-job input and log. The repository checkpoint contains the scripts, exact inputs, compact original results, proof correction and hashes; `RESULTS.json` can restore the original records needed by the composition checker without rerunning a target.

## Reading and proof dependencies

Read in this pass: the entire attached proposed proof; current main and overnight directory; the exact K0, K1 and D01 input cards; research/28's historical cable table and correction; the relevant source passages below. This is not an exhaustive repository, branch, or archive audit. No independent geometric extraction of the candidate knots or smooth disks was performed.

- Michael Eisermann, *The Jones polynomial of ribbon links*, Geometry & Topology 13 (2009), 623-660. Proposition 6.13, Corollary 6.15, Example 6.16, and section 7.1: ribbon-pattern preservation, parallel necessities, 6_1 controls and stable-ribbon discussion. https://arxiv.org/html/0802.2287
- Charles Livingston, *A survey of classical knot concordance*, Handbook of Knot Theory (2005), 319-347, arXiv:math/0307077. Section 2.1 after Definition 2.3: a smooth slice knot admits a ribbon stabilizer. The smooth-category statement was checked in the PDF. https://arxiv.org/pdf/math/0307077
- H. R. Morton and P. Strickland, *Jones polynomial invariants for knots and satellites*, Math. Proc. Cambridge Philos. Soc. 109 (1991), 83-103. Theorem 1.1 and Corollary 1.2, printed p.87; Theorem 2.1 and Corollaries 2.2-2.3, pp.92-93. Scalar connected-sum and tensor-product cabling identities; the actual pages were inspected. https://www.researchgate.net/profile/Hugh-Morton/publication/232015440_Jones_polynomial_invariants_for_knots_and_satellites/links/5ba287fd92851ca9ed15cead/Jones-polynomial-invariants-for-knots-and-satellites.pdf
- Megan du Preez, Bryan Silva, Eric Yu and Sherry Gong, *Connections between common slice obstructions and the Eisermann ribbon obstruction*, Texas A&M REU report (July 2025), Theorem 5.10, printed p.18. Its proof is marked WIP; that page was checked, and the claim is NOT an imported theorem here. https://artsci.tamu.edu/mathematics/_files/_docs/reu/results/2025/dupreez-silva-yu-report.pdf

The knot-to-PD identifications and the intended Abe-Tagami nonribbon hypotheses remain upstream dependencies. Neither numerical knots matching nor passing quantum tests resolves them. No Mac files or Opus processes were changed. No continuing compute process is left by this pass.
