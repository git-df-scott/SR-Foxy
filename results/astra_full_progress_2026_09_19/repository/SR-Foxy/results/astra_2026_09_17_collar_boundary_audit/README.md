# Astra: collar obstruction and the actual crossed-surgery boundary

**No Slice–Ribbon counterexample. Sliceness and nonribbonness of the new boundary are UNKNOWN.**

Question: do the two crossed axes from the archived pass09 agree in the proposed disk group under changes of lower-factor identification, and does the first surgery produce the intended Abe–Tagami difference knot?

Success would require an actual marked disk-exterior map, an embedded modifying annulus with the correct framing, standard ambient four-ball, and a proven nonribbon boundary. This pass proves an algebraic obstruction and computes the boundary of a specific three-dimensional surgery. It does not supply those geometric certificates.

Scientific inputs were read directly from GitHub, pinned to main commit `07c20b0fd7f40aa3dd330d66ba1107a0af446d55`. The two input blob hashes appear in `CERTIFICATE.json`. The subsequent Opus commit `71200112d0f4e881896f1f5b5f01f4dc84809192` was read before publication; see `OPUS_AUDIT.md`.

## 1. Exact obstruction for every nonzero integer partial conjugation

Let q0 be the saved pass09 candidate collar map. Define q_n to fix the upper factor and conjugate every lower-factor image by mu^n, where mu is the common seam meridian. Zero-based lower boundary arcs are [4,9,10,11,12,13,14,15,16,17], and the shared seam arcs are 4 and 14. All boundary relations hold symbolically in n.

**Theorem for this algebraic family.** For every integer n != 0, the images of the two crossed axes under q_n are not conjugate, even after inverting either axis. The n=0 map is the favorable equality case recorded by pass09. This theorem does not identify which q_n, if any, is the actual map induced by the intended marked disk.

Proof: use the exact representation into SL(2,F), where
F = Q[z]/(R), and
R = z^6 + 3z^5 + 5z^4 + 4z^3 + 2z^2 + z + 1.
The starting source generators are x1=[[1,1],[0,1]] and x2=[[1,0],[z,1]]. The saved propagation determines all nine generators; all nine source relators and all eighteen boundary relators are checked. Reduction mod 2 has no monic divisor of degree 1, 2, or 3 (all fourteen tested), hence R is irreducible.

The seam is x3=[[1-z,1],[-z^2,1+z]]. Writing N=x3-I gives N^2=0 and mu^n=I+nN for every integer n, including negative n.

The difference of the two axis traces is n A(z)+n^2 B(z), with
A=-10-8z-18z^2-36z^3-34z^4-12z^5,
B=-2-2z^2-4z^3-2z^4.
Its degree in z is below 6 and its z^5 coefficient is -12n. Thus it is nonzero in F whenever n != 0. Conjugate SL(2) matrices have equal traces, and inversion preserves trace. This proves the obstruction without assuming the representation is faithful.

Python rational-polynomial arithmetic and an independently implemented JavaScript BigInt polynomial checker agree. The latter rejects mutated axis, matrix, and trace inputs. This is an all-integer proof, not a bounded search.

An adjacent-region diagnostic explains why the marking matters. The saved base sector (0,2) is region 0; sector (0,1) is region 6. Region 6 has word [6,-5,8,5,-6], literally the saved seam-meridian word. Replacing Dehn words D_f by D_f D_b^-1 conjugates the lower images by D_b while leaving the upper factor fixed. Thus this adjacent choice gives q1 and fails. It is not a simultaneous global conjugation. An actual geometric collar is needed to select the correct relative marking.

## 2. The first crossed surgery has the wrong target polynomial

Using the exact archived bands a40a423e_0_0 and d0826c36_0_0 gives the 62-crossing link (R,eta1,eta2). Fill eta1 with slope (1,1) and eta2 with (-1,1), in the preferred meridian-longitude bases, leaving R unfilled. Here the surgery parameter r is independent of the collar parameter n.

SnapPy 3.3.2 recovered a 38-crossing knot diagram using seed 1729, with its input and answer checks enabled. The complete PD, sparse Seifert matrix, and HFK ranks are in `BOUNDARY.json`. Independently, Fox calculus on the original 62-generator surgery presentation gives

Delta_new = t^8-6t^7+18t^6-36t^5+47t^4-36t^3+18t^2-6t+1.

This agrees with det(V-t V^T), after removing the unit t^51, and the HFK Euler characteristic. The r=0 Fox control is the original square polynomial.

Every intended D_nm in the repo has
Delta_old=(t^4-3t^3+5t^2-3t+1)^2.
But Delta_new-Delta_old=-t^2(t^2-1)^2 != 0.
Consequently this specific first crossed surgery is not D_01 or another knot in that common-polynomial family. Its nonribbonness cannot be inherited from the existing Abe–Tagami target argument.

The new polynomial does pass the Fox–Milnor necessary condition:
Delta_new=f(t)t^4 f(t^-1), f=t^4-2t^3+5t^2-4t+1.
Its determinant is 169. Computed HFK has genus 4, fibered flag true, tau=epsilon=nu=0, and total rank 409. None proves sliceness. Numerical volume 28.01523402725465 is not certified hyperbolicity and is not used as a proof of primality.

## 3. Reproduce and scope

From this directory, with assertions enabled:

```sh
python3 check_symbolic.py
node check_symbolic_independent.mjs
python3 check_surgery_alexander.py
python3 check_boundary.py
python3 probe_boundary.py
python3 inspect_boundary.py
```

The symbolic collar checker uses only the Python standard library. Boundary calculations used SymPy 1.14.0 and SnapPy 3.3.2 (Python 3.14); JavaScript verification used the tool runtime's BigInt implementation. Scripts read existing repository inputs and print to stdout. The producer's diagram simplification may vary by runtime; the saved PD and exact invariant checks are the reproducible target. Conversion timeouts report UNKNOWN.

`VERIFICATION.json` records checks and failed exploratory attempts. Algebraic and polynomial conclusions are exact for the encoded inputs. The identification of these calculations with an intended four-dimensional modification remains unproved.

The most valuable next work is to derive the marked collar map from explicit geometry and either alter the bands to recover the intended boundary polynomial or develop a separate nonribbon obstruction for the new boundary. Repeating a favorable finite coloring or treating a square determinant as sliceness will not close either gap.
