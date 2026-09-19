# GST48: exact algebra, Floer computation, and certified band-prefix analysis

**Date:** 19 September 2026. **Slice–Ribbon counterexample: not established.**

This is a completed computational research block, not a proof of non-ribbonness. It produces a specific working diagram, independently checked Alexander data, a genus/non-fiberedness computation, exact obstructions to completing particular first bands, and replayable movies showing why every remaining prefix in the larger finite search returns to the original problem. “New” below means obtained in this session; no claim of first discovery in the literature is made.

## 1. Input, identification, and repository provenance

The input in `gst48.json` is exactly the 48-crossing `GST_START_PD` published by Epoch AI in *The Slice–Ribbon Conjecture and the GST Knot* [1]. The publisher identifies this diagram as a GST knot. Its PD was recovered directly, not reconstructed by guessing a knot from its polynomial or an image. The data have 96 edge labels, each occurring twice, 50 complementary faces, and one link component. The rotation-system Euler characteristic is 2.

There is an important provenance distinction. Gompf–Scharlemann–Thompson prove standard-four-ball sliceness for their construction and obtain slice knots by band-summing their slice links [2, §8]. This session **does not independently replay a Kirby/isotopy bridge from the published 48-crossing PD to their original Figure 2**. The identification remains source-attributed. All computations and finite-prefix conclusions apply unconditionally to the literal PD in this package.

The inspected repository files were `GST_AUDIT.md` and `ASTRA_BRIEF_2026_09_19.md` on `git-df-scott/SR-Foxy`. The latter explicitly listed GST as a target for which the campaign did not hold a working diagram. The latest repository head observed was `e5491286f233d4edcf6603ecba44cf24fbab2341`. Nothing in this package has been pushed to the repository.

The topology environment was recovered from the repository's already-existing successful workflow run 35417723921, artifact 10576048198. This session downloaded and installed that artifact; it did not create the workflow. Its SHA256 is recorded in `STATUS.json`. The 131 MB wheelhouse is deliberately not redistributed here.

## 2. A concrete obstruction to the direct fibered-knot route

The knot Floer calculation gives

\[
 g(K)=10,\qquad \operatorname{rank}_{\mathbb F_2}\widehat{HFK}(K)=189,
 \qquad \tau(K)=\nu(K)=\epsilon(K)=0.
\]

In maximal Alexander grading,

\[
 \widehat{HFK}(K,A=10)
 =\mathbb F_2{}_{M=13}\oplus\mathbb F_2{}_{M=14}.
\]

There is no support above Alexander grading 10. The genus-detection theorem and the rank-one characterization of fibered knots therefore interpret this computation as **genus 10 and non-fiberedness** [3,4]. In particular, a direct non-ribbon argument requiring this knot itself to be fibered cannot be applied. This does not rule out arguments using some other fibered knot, a satellite companion, or additional structure.

Checks saved in `topology_verification.json`:

* The complete bigraded ranks agree over both F2 and F3 and after deterministic random relabeling and crossing reordering.
* The mirror computation obeys `(A,M) -> (-A,-M)` and the original obeys conjugation symmetry.
* The graded Euler characteristic equals the independently computed, symmetrically normalized Alexander polynomial.
* The saved 189-generator reduced `UV=0` complex has differential squared zero. Its vertical and horizontal differentials each have rank 94, so each resulting homology has dimension one.

The calculator's installed test suite also passed: 40 module tests and one regression test. These are substantive consistency checks, not a formal verification of the Floer calculator or an independent second implementation of Floer homology. The full ranks and complex are saved, rather than only the software's `fibered=False` flag.

## 3. Exact Alexander data and two rational metabolizers

Put

\[
 f(t)=t^8-2t^7+t^6+t^5-2t^4+t^3-1,
\]
\[
 g(t)=t^8-t^5+2t^4-t^3-t^2+2t-1=-t^8 f(t^{-1}).
\]

The symmetric normalization is

\[
 \Delta_K(t)=f(t)f(t^{-1}),
 \qquad D(t):=t^8\Delta_K(t)=-f(t)g(t).
\]

Equivalently,

\[
\begin{aligned}
D(t)={}&-t^{16}+2t^{15}-t^{14}-2t^{12}+5t^{11}-2t^{10}
-7t^9+13t^8\\
&-7t^7-2t^6+5t^5-2t^4-t^2+2t-1.
\end{aligned}
\]

Thus the determinant is one, while the Alexander breadth is 16. Its breadth is strictly smaller than twice the computed genus: `16 < 20`. The polynomial does not detect the two extra genus units.

The polynomial was calculated from a 48-generator Wirtinger/Fox presentation. Independently, Spherogram constructed a 74-by-74 Seifert matrix; `det(V-V^T)=1`, and the normalized `det(tV-V^T)` is the same D. That particular matrix represents a nonminimal genus-37 surface; it must not be mistaken for the knot's minimal genus. The original diagram's canonical Seifert surface has genus 19.

Both f and g are irreducible modulo 2, and hence over Q. They are distinct. Let `R=Q[t,t^-1]` and let M be the rational Alexander module. Its square-free order fg gives

\[
 M\cong R/(fg)\cong R/(f)\oplus R/(g).
\]

This yields a useful exact reduction: **the nonsingular rational Blanchfield pairing has exactly two metabolizers**, the two primary summands.

Here is the argument, not merely a software assertion. Each summand is a simple R-module, and the two summands are nonisomorphic; hence the only R-submodules are zero, either summand, and M. On the f-primary summand, sesquilinearity makes a self-pairing annihilated by both f and its reciprocal. Those annihilators are coprime over R, so the self-pairing vanishes. The same holds for the g-primary summand. Nonsingularity then makes each of these half-size summands its own orthogonal complement. Neither zero nor all of M is a metabolizer.

This is a reduction of **rational algebraic kernels**, not a classification of embedded derivatives, ribbon disks, or slice disks. In particular, “two metabolizers” must not be rewritten as “two disks left to test.”

### The integral exceptional prime

Exact additional calculations give

\[
 \operatorname{Res}(f,g)=43^2,
 \qquad \gcd(f,g)\pmod {43}=t^2-4t+1.
\]

The latter polynomial is irreducible over F43. The integer Smith diagonal of the Sylvester matrix is fourteen 1s followed by 43,43. Explicit polynomials A,B in `algebra_certificates.json` satisfy `Af+Bg=43`, demonstrating that the rational splitting separates after inverting 43.

Over `F43[z]/(z^2-4z+1)`, z has multiplicative order 11 and the reduced 47-by-47 Fox matrix has nullity one. Also `|Res(D,t^11-1)|=43^4=3,418,801`, giving the order of first homology of the 11-fold cyclic branched cover. We have not computed its complete integral Smith decomposition here.

None of these arithmetic facts is itself a non-ribbon obstruction. In particular, the existing sliceness construction prevents selling an ordinary sliceness obstruction as the missing ribbon obstruction.

## 4. A finite-prefix theorem, not a failed random walk

An oriented first saddle in a ribbon-disk movie splits the boundary knot into two components. The part of the ribbon disk remaining after this cut would provide disjoint disks for the resulting link. Consequently, **a proved nonslice output link excludes that particular first-band prefix, regardless of how many later ribbon moves are allowed**.

The relevant obstruction is Alexander rank. Cha–Friedl's Theorem 1.1, with the trivial one-dimensional representation, says that a slice m-component link has Alexander rank m-1 for every admissible free-abelian meridional coefficient system [5]. For two components the required rank is one. We use both the total-meridian cyclic system and the full two-variable abelianization.

For a Fox matrix with q columns, the twisted first-homology rank is `q-1-rank(Fox)` over the fraction field: the degree-one boundary has rank one. A nonzero `(q-1)`-minor therefore proves rank zero and excludes sliceness. A nonzero integer evaluation, or a nonzero evaluation modulo a prime, proves that the corresponding polynomial is not identically zero. Evaluating at 2 is used only to certify polynomial nonvanishing; 2 is not being treated as a unit-circle signature parameter.

### Exact single-face enumeration

A direct rotation-system enumeration produces 164 distinct-edge, orientable, untwisted bands contained in one face of the fixed input diagram. For each of the 164 resulting links, an explicit 47-by-47 Fox minor is nonzero at t=2. Every integer determinant was checked by two algorithms: a separate fraction-free Bareiss implementation and SymPy.

The two most deceptive outputs have linking number zero and component determinants 1 and 9. Their components also pass the Alexander norm check. Nonetheless, their link minors at t=2 are 525,533,184 and -1,051,066,368, respectively, so these links are not slice.

Spherogram independently produces 164 bands at `(max_band_len=2,max_twists=0)`. The exact Regina diagram-signature multisets of the outputs agree with the independent enumeration. No numerical volume comparison is used for this check.

### One crossed arc and one half-twist

The next generator setting `(max_band_len=3,max_twists=1)` produces 1,698 distinct compressed band specifications. Of these, 1,483 fail linking number and 212 have a nonzero single-variable minor. All three remaining outputs fail with separate meridian variables.

For the particularly deceptive band `7f42_0_1`, the 48-by-48 minor at `(x,y)=(2,3)` is exactly

\[
153,714,723,840\ne 0.
\]

The unequal-weight cyclic specialization `(x,y)=(t,t^2)` also detects it: at t=2 the same-sized minor is 26,510,522,056,704. This explains why testing only the equal-meridian specialization can leave false survivors. The other two exceptional bands have component determinant 73 and are also independently excluded by the separate-variable rank test.

Thus **all 1,698 specified first bands have nonslice outputs**. This is not a claim about every geometric band with loosely comparable visual complexity.

## 5. The larger search: 50 apparent survivors are exact self-returns

At `(max_band_len=4,max_twists=2)`, allowing up to two interior arc encounters and two half-twists in the generator, the count is 15,794 distinct band specifications. The exact disposition is:

| Disposition | Count |
|---|---:|
| Excluded by nonzero linking number | 13,269 |
| Excluded by a single-variable Alexander minor | 2,463 |
| Excluded by a separate-variable Alexander minor | 12 |
| Explicitly return to the original knot plus a split unknot | 50 |
| Total | 15,794 |

The 50 survivors are not claimed to be 50 new knots, slice disks, or counterexample candidates. For every one, a recorded Reidemeister movie identifies the output as `K disjoint union U`, with K the original source knot and U a split unknot. Forty-one movies need two type-III moves, eight need three, and one needs four, interspersed with individually recorded type-I/type-II removals. The final nontrivial component has exactly the source's strict Regina diagram signature.

All 50 movies were replayed without search, including the individual intermediate diagrams. All 15,794 band records were replayed, as were the three smaller-search exceptional certificates. The code additionally checks every linking obstruction with the independent PD implementation, all 12 multivariable tail minors with exact integer determinants, and 23 single-variable larger-search minors with independent integer determinants as spot checks. The remaining larger-search nonzero modular minors are individually replayed by the modular checker.

A subtle but essential limitation: a self-return prefix is **not** proved impossible in a ribbon disk. Later bands could use the extra unknot. The result says the bounded search supplies no simpler nontrivial target, not that these 50 prefixes may be discarded from every possible ribbon movie.

Raw files named `survivors` or containing `inconclusive_specializations_zero` are intermediate stages. `STATUS.json`, the multivariable certificates, and the replayed self-return movies are the final disposition.

## 6. What the 2026 handleslide paper does and does not settle

Diao–Pan–Yan's 2026 preprint reports stable handleslide equivalences for bounded GST parameters and stable triviality for the `L(3,2;4/d)` family [6]. The usual n=3 GST parameter corresponds instead to slope 6/7. A stable equivalence to another parameterized link is not, by itself, an unlink certificate for this target.

There is also a distinction worth preserving: stabilization by split zero-framed unknots is not addition of a canceling Hopf pair. Genuine split-unknot stable triviality can imply ribbonness; the Hopf-pair weak stabilization used in the original construction is different. No argument in this package conflates them or uses Andrews–Curtis nontriviality as a proved converse ribbon obstruction.

## 7. The missing implication

The current gap is precise. No theorem has been proved here that forces every ribbon disk to begin with one of the excluded bands, or that eliminates all continuations through a self-return prefix. Nor has either rational Blanchfield metabolizer been shown unrealizable by a ribbon disk. Those are diagram-independent requirements; increasing a finite search count does not establish them.

The next focused target is the canonical GST disk's integral Alexander kernel and its peripheral realization: use the two rational primary possibilities and the computed prime-43 interaction as constraints, while seeking a property required of a ribbon realization but not of an arbitrary slice realization. This is a proposed research direction, not an obstruction already obtained.

## 8. Reproduction and scope of the package

Tested environment: Python 3.13.5; SymPy 1.14.0; Spherogram 2.4.1; SnapPy 3.3.2; Regina wheel 7.4.1; knot_floer_homology 1.2.2. Exact versions are pinned in `requirements.txt`. See `README.md` for replay commands and `STATUS.json` for the machine-readable result.

Every claimed positive certificate has an input and replay path. This remains ordinary checked research software, not a proof-assistant formalization. The code does not claim a global non-ribbon result or a ribbon disk for GST48. The files are prepared for insertion into `research/gst_2026_09_19_exact/`; they have not been committed or pushed.

## References

[1] Epoch AI, *The Slice–Ribbon Conjecture and the GST Knot*, public starting PD and certificate specification, retrieved 19 September 2026. https://epoch.ai/frontiermath/open-problems/slice-ribbon . Source attribution retained for the input data; the page states CC BY availability.

[2] R. E. Gompf, M. Scharlemann, A. Thompson, *Fibered knots and potential counterexamples to the Property 2R and Slice-Ribbon Conjectures*, Geometry & Topology 14 (2010), 2305–2347. https://arxiv.org/abs/1103.1601 . In particular §8.

[3] P. Ozsváth, Z. Szabó, *Holomorphic disks and genus bounds*, Geometry & Topology 8 (2004), 311–334. https://arxiv.org/abs/math/0311496 .

[4] Y. Ni, *Knot Floer homology detects fibred knots*. https://arxiv.org/abs/math/0607156 . The non-fibered implication used here is that a fibered knot has rank-one top knot Floer homology.

[5] J. C. Cha, S. Friedl, *Twisted torsion invariants and link concordance*. https://arxiv.org/abs/1001.0926 . Theorem 1.1, with trivial representation. For ordinary signature/nullity concordance see also M. Nagel, M. Powell, https://arxiv.org/abs/1608.02037 .

[6] Diao, Pan, Yan, *Some experimental results on stable equivalence of GST Links for the Generalized Property R Conjecture*, 2026 preprint, version 1. https://arxiv.org/abs/2604.17737 .

[7] knot_floer_homology implementation, based on Zoltán Szabó's calculator, https://github.com/3-manifolds/knot_floer_homology ; Spherogram, https://github.com/3-manifolds/Spherogram ; Regina, https://regina-normal.github.io/ . Version-specific installed code was inspected for band, Floer-complex, and signature conventions.
