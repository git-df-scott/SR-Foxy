# Component ancestry and the remaining linking problem

13 September 2026, extra afternoon session. **No counterexample found.**

The exact goal remains a smooth concordance from the stored Abe–Tagami K0
to K1 in standard S3 × I. Together with the separately audited nonribbonness
of K0 # -K1, that would give the desired counterexample. Neither an invariant
match nor a nonsplit link with the desired components supplies this concordance.
The common ribbon upper construction is sufficient; we have not proved it
necessary for an arbitrary concordance.

## A useful elementary deduction: follow the descendants

Assume that a reverse movie uses only oriented splitting saddles, isotopies,
and deaths of split unknots. There are no later fusion saddles or births.
Suppose an intermediate level has two components A and B and the completed
movie ends at the single knot K.

Every subsequent split replaces one circle by two descendants. The ancestry
graph is a forest: distinct components never merge. Exactly one of A and B
has the surviving K among its descendants. Call that component A.

The surface traced by A is connected and planar. Starting from its cylinder,
each split adds a boundary circle and reduces Euler characteristic by one;
each terminal death caps a boundary circle and increases it by one. After
capping all terminal descendants except K, there are precisely two boundary
circles and Euler characteristic zero. Thus this surface is an annulus.
The analogous capped surface for B has one boundary circle and Euler
characteristic one, so it is a disk. Embeddedness is inherited from the movie.

Reverse the height on the annulus: deaths become births and splitting
saddles become fusion saddles, with no maxima. This is a ribbon concordance
K → A. Reversing the height on the capped surface for B produces only births
and saddles, hence a ribbon disk with a handle presentation of disks joined
by bands. Forgetting the other
surface does not introduce intersections into either surface.

Consequently, **up to exchanging A and B**, A must be ribbon-concordant above
K and B must be ribbon. This is an elementary deduction under the stated
movie restrictions, not a claimed new theorem about all concordances.
Puncturing a birth disk in the ribbon presentation of B gives U → B.
The unknot and K must therefore satisfy their respective graded homology
injection inequalities into B and A.

The determinant products det(A) det(K) and det(B) must be squares. Indeed,
A # -K and B are slice, so evaluate the Fox–Milnor factorization at -1.
We also use equality of tau on concordant knots. These are only necessary
conditions. With just one splitting saddle left, one component is untouched:
either A already is K or B already is U. Jones equality can test this
necessary condition but cannot recognize either knot.

**Scope matters.** Do not demand that A already be K when multiple splits
remain. Do not use this ancestry rule for a movie that later merges A and B.
Do not infer a genus inequality for a band sum of arbitrarily linked
components from a theorem about a band sum of a split link. A saved example,
first band `0b3f5f0e_3_0`, has a genus-four component after splitting the
genus-three J25533; the other component simplifies individually to an unknot.
The required split death is not supplied by that componentwise simplification.

## Computed effect on the saved two-stage search

The input is the 61 retained first-stage links in
`results/two_fission_nonfibered_25533.json`. No first-stage link was replaced
or silently removed from that historical file.

| Necessary tests toward K1 | First-stage links remaining |
|---|---:|
| Previous linking/Alexander-rank screen | 61 |
| Component determinants, tau and full graded HFK | 15 |
| Full graded F2 Khovanov injection for the distinguished component | 2 |

All component HFK computations finished. There were 43 distinct component
diagrams, and eight distinct distinguished components among the 15 survivors.
The Kh pass reused three previously checked diagram-identical calculations
and computed five new ones. All eight Euler characteristics match independent
Regina Jones calculations. Six of the eight component diagrams fail the K1
injection. The two retained first bands are:

    6267660c_0_0
    2b2a271f_1_0

Thus 59 of these **specified 61 first-stage links** are excluded from all
continuations in the restricted movie class, even if more fissions are added.
This does not exclude any untested first band, or a general concordance.

For calibration, the determinant/HFK screen retains 29 first-stage links
toward the known source K0. It does not reject the entire control direction.

The subsequent guided second-saddle search sampled 50,887 bands across the
two retained stages. Of these, 39,176 were fissions with all pairwise linking
numbers normalized to zero; 5,920 fused components and were outside the
chosen movie class, and 5,791 failed the linking correction. None of the
39,176 had component Jones polynomials K1, U, U. Each stage had a 90-second
budget, with maximum band length 14 and recorded seeds. This is a bounded
negative search, not an obstruction to all second saddles.

## Remove the twist parameter before searching geometry

For a fission band, its two long boundary edges lie on different resulting
components. A full twist introduces only mixed crossings between these
components. Removing either component removes those crossings, so the two
individual knot types are unchanged. With coherently transported orientations,
the full twist changes their linking number by one, with sign fixed by the
twisting convention. There is exactly one full-twist correction to linking zero.

The first implementation tested signed differences between independently
rebuilt diagrams and failed. The preserved regression is band
`293d3c3a394c1e1d42_56_0` on target 23841: the library reports linking -2 at
twist zero and +1 at twist two. Rebuilding can reverse a component orientation.
Subtracting these independently oriented numbers is invalid.

The repaired implementation tries both twists t ± 2|lk| and verifies which
has linking zero. It checks planarity, component count and component Jones
preservation. This is an orientation-independent implementation of the local
geometric argument. A component Jones check alone is not a proof of knot
identity; the preservation argument comes from the mixed-crossing description.

For three-component links, only the two descendants of the split component
have their mutual linking changed by twisting. The second-stage search tests
the correction and explicitly verifies the entire linking matrix is zero;
it does not assume the other two entries can be corrected by twisting.

## Correct component knots are being reached, but are not separated

A component-guided one-fission experiment tested 71,841 bands on the two
K0-built surviving upper targets and 125,000 on five K1-built upper targets.
The former produced no K1/unknot component Jones match. The latter produced
239 retained link diagrams with K0/unknot component Jones matches; all 239
also passed the K0 component HFK test. Every one had whole-link Jones
polynomial different from its split product, so each particular link is
nonsplit. Counts refer to retained diagrams, not distinct isotopy classes.

Normalizing twists and flipping up to two over/under choices on the saved
band cores then tested 6,623 normalized bands. It retained 1,092 link diagrams
with the required component Jones polynomials and linking zero. All 1,092
again fail the split-product Jones equality. In 156 cases the individual
component diagrams actually simplify to a diagram-identical K0 and an unknot
(up to orientation reversal, without identifying mirrors). Thus component
identification alone is demonstrably not the missing step in those cases.

An explicit 31-crossing example on target 23841 is the band
`080f2613_2_-2`. Both component diagrams are recognized and linking is zero,
but its whole-link polynomial is not the split product. Its complete PD and
band replay are in `results/normalized_component_neighborhoods.json`.
It is an example of a failed proposed endpoint, not a Slice–Ribbon counterexample.

The negative control is the Whitehead link with K0 connected-summed into
one component. It has exactly the right component knots and linking zero,
yet fails the split-product equality. The positive control is split K0 ∪ U.
This tests the false implication we most need to avoid. Polynomial coefficient
distance is stored only as a sorting heuristic, with no claim that smaller
values mean fewer geometric moves or proximity to a concordance.

## Next experiment and limitations

**Proposed next construction:** allow band attachment arcs and dual-path
homotopy classes to change. Use an explicit split K0 ∪ U as the reverse-side
boundary condition while preserving the known K1 → J birth-and-band movie.
Seek a common upper diagram by simultaneous local moves on both presentations,
recording every isotopy and saddle. Test the complete HFK/Kh conditions before
expanding a new upper knot. A successful endpoint needs an explicit splitting
sphere or a checked isotopy to a split link, then orientation and movie audits.

This proposal has not been implemented. It targets what fixed-core twist and
crossing-choice neighborhoods cannot guarantee: a change in how the band
attaches and how it runs through the link exterior. The current counts do
not prove those neighborhoods are all exhausted, nor that such a construction
exists. An independent audit should first try to break the ancestry argument
and the twist normalization. Claude's prepared audit prompt has not been sent:
Computer Use reported that the Mac was locked; the existing setup was unchanged.

## Primary-source ledger

Sources checked on 13 September 2026. The local ancestry and twist arguments
above are derivations; the following non-elementary inputs are source-backed.

| Claim used | Primary source | Status / precise location |
|---|---|---|
| Slice Alexander polynomial factors as a norm; evaluating at -1 gives a square determinant | Ralph H. Fox and John W. Milnor, *Singularities of 2-spheres in 4-space and cobordism of knots*, Osaka Journal of Mathematics 3(2), 257–267 (1966), [DOI 10.18910/7307](https://doi.org/10.18910/7307) | Original paper, Theorem 2, p. 262; checked in the university-hosted PDF |
| A ribbon concordance gives a graded HFK injection | Ian Zemke, *Knot Floer homology obstructs ribbon concordance*, Annals of Mathematics 190(3), 931–947 (2019), [DOI 10.4007/annals.2019.190.3.5](https://doi.org/10.4007/annals.2019.190.3.5), [arXiv 1902.04050](https://arxiv.org/abs/1902.04050) | Published theorem; Theorem 1.1 and the grading-preserving map in the introduction |
| A ribbon concordance gives a split, bigrading-preserving Kh injection | Adam Simon Levine and Ian Zemke, *Khovanov homology and ribbon concordances*, Bulletin of the London Mathematical Society 51 (2019), 1099–1103, [DOI 10.1112/blms.12303](https://doi.org/10.1112/blms.12303) | Theorem 1; field F2 used here; source checked in the preceding gate audit |

Run `scripts/check_component_session.py` for raw band replays, independent
Seifert/Jones/HFK determinant comparisons, Kh log/Euler checks, and the
orientation regression. Its result records exact counts and input hashes.
No calculation in this session supplies the missing smooth concordance.
