# New weapons, 2023–August 2026

Each entry follows: paper → exact result → detected structure → slice/ribbon separation → application status → work required.

## Miller–Zupan (2023): handle-ribbon characterizations [S02]

**Paper →** “Equivalent characterizations of handle-ribbon knots.”
**Exact result →** Proposition 1.1 (ribbon iff unlink derivative); Theorem 1.3 (handle-ribbon iff R-link derivative); Theorem 1.4 (fibered homotopy-ribbon iff monodromy extends over a handlebody).
**Detects →** The precise boundary between ribbon, handle-ribbon and homotopy-ribbon.
**Can distinguish ribbon from slice? →** Yes in principle: exclude all unlink derivatives while a slice disk is independently known. The handle-ribbon criterion alone cannot.
**Applied? →** Oliveira-Smith applies the R-link/handle-ribbon side to `DG` [S01]. No exhaustive unlink-derivative exclusion is known. GST’s handle diagrams fit the same side [S05].
**Required →** A completeness theorem for candidate Seifert surfaces/derivatives, followed by exact unlink recognition.

## Miller–Zupan (2025): non-isotopic ribbon disks [S15]

**Exact result →** Infinite families of fibered homotopy-ribbon disks for generalized square knots; a specified (q=2) family consists of ribbon disks.
**Detects →** Disk nonuniqueness and fibered disk structure.
**Slice/ribbon separation? →** No counterexample; it enlarges the known ribbon side.
**Applied? →** Not to `DG` or GST.
**Required →** The still-open theorem “every ribbon disk of a fibered knot is fibered” would convert monodromy classification into a ribbon classification.

## Hom–Park (2025/26): γ₀-sharp immersed-curve obstruction [S08]

**Exact result →** Theorem 1.1 classifies when connected sums of γ₀-sharp fibered knots can be ribbon; Corollary 1.3 gives explicit algebraically slice non-ribbon sums.
**Detects →** Oriented pairing data in immersed-curve knot Floer invariants invisible to the ordinary Alexander factorization.
**Slice/ribbon separation? →** It proves non-ribbonness, but the displayed examples are not proved smoothly slice.
**Applied? →** Not to `DG`, GST or Abe–Tagami in the inspected paper.
**Required →** Verify γ₀-sharpness for the chosen summands and independently construct a smooth slice disk. Without the latter it remains Tier B.

## Dunfield–Gong (2025): certified census and ribbon search [S03]

**Exact result →** Theorem 1.1 and Section 2.7 provide a certificate-oriented census through 19 crossings; `18nh00000601` is the sole survivor of the strengthened ribbon search among 554 suspicious knots.
**Detects →** Concrete ribbon bands, branched-cover sliceness obstructions, twisted Alexander obstructions, and stabilization patterns.
**Slice/ribbon separation? →** No. Algorithm failure is not an obstruction.
**Applied? →** Directly to `DG`; later [S01] proves its smooth sliceness.
**Required →** A complete ribbon certificate search or an independent ribbon-only obstruction.

## Oliveira-Smith (March 2026): standardization and handle-ribbon disk [S01]

**Exact result →** Theorem 1.1 standardizes the DG sphere; Corollary 1.1.1 proves `DG` smoothly slice in standard (B^4); Theorem 1.2 proves it fibered handle-ribbon.
**Detects →** Explicit trace embeddings, R-link derivatives and handle structures.
**Slice/ribbon separation? →** It creates the strongest certified candidate but does not prove non-ribbonness.
**Applied? →** This is the application.
**Required →** Distinguish its R-link derivative from every possible unlink derivative.

## Fibered monodromy compression algorithm (2026) [S09]

**Exact result →** Theorems 1.7 and 1.9 characterize strong homotopy-ribbon concordance by monodromy compression and enumerate minimal compressions; Corollary 1.11 gives finiteness of predecessors.
**Detects →** Compression order, extendible monodromy and simplicial-volume monotonicity.
**Slice/ribbon separation? →** Not by itself. It classifies strong homotopy-ribbon data, which `DG` already has.
**Applied? →** No candidate-specific computation found.
**Required →** Couple the finite compression list to a theorem that every ribbon disk of the target is fibered, then test which compressions arise from unlink derivatives.

## Minimum-height ribbon concordance (August 2026) [S10]

**Exact result →** A minimum-height invariant from immersed curves and cabling formulas obstruct specified ribbon concordances.
**Detects →** Directional complexity lost by ordinary concordance invariants.
**Slice/ribbon separation? →** Potentially for a knot forced into the paper’s ribbon-concordance/cable setup; not a general slice/ribbon theorem.
**Applied? →** No ledger application found.
**Required →** Identify a candidate as a covered cable or prove an uncabled extension of the theorem.

## Singular instanton ribbon concordance (July 2026) [S11]

**Exact result →** Equivariant singular-instanton invariants with a Chern–Simons filtration constrain same-sign twists and ribbon concordances.
**Detects →** Filtered gauge-theoretic directionality.
**Slice/ribbon separation? →** Not generally; it must match the specific concordance/twist hypotheses.
**Applied? →** None found for the ledger.
**Required →** Produce an admissible presentation of the target and compute the filtered invariants exactly.

## Real/equivariant link Floer (April 2026) [S12]

**Exact result →** Constructs real link Floer homology for specified involutive link structures.
**Detects →** Equivariant data of periodic/real links.
**Slice/ribbon separation? →** `UNKNOWN`; no general ribbon necessity applicable to the ledger was verified.
**Applied? →** No.
**Required →** First certify a compatible symmetry on the candidate and then prove a ribbon-disk equivariance theorem; ordinary ribbon disks need not respect the symmetry.

## Dihedral quotient extension (April 2026) [S13]

**Exact result →** Theorem 1.1 gives a congruence criterion for quotient extension; Theorem 7.1 gives the associated homotopy-ribbon Ξ bound.
**Detects →** Extension of dihedral colorings over surface exteriors.
**Slice/ribbon separation? →** It separates homotopy-ribbon from weaker surface bounding, not ribbon from handle-ribbon.
**Applied? →** No GST computation found.
**Required →** Use only on a candidate whose homotopy-ribbon status is open. It is a dead end for `DG`/GST.

## Stable GST equivalences (April 2026) [S14]

**Exact result →** Theorem 1.1 proves stated finite ranges of stable handleslide equivalence among GST-related links.
**Detects →** Stable Generalized Property R behavior.
**Slice/ribbon separation? →** No. Stabilization does not imply a ribbon disk for the unstabilized band-sum knot.
**Applied? →** Directly to GST families, but not as a ribbon resolution.
**Required →** A theorem transporting stable handleslides to an unlink derivative for the exact band sum without introducing forbidden maxima.

## Bottom line

The genuinely new capability is not “a stronger sliceness invariant.” It is the combination of (i) a certified standard-(B^4) slice/handle-ribbon target [S01], (ii) the unlink-versus-R-link derivative characterization [S02], and (iii) finite monodromy-compression enumeration [S09]. The missing bridge is a completeness theorem from arbitrary ribbon disks to the finite fibered/derivative data.
