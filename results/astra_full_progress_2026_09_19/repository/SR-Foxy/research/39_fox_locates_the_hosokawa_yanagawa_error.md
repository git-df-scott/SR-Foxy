# Fox explicitly located the Hosokawa--Yanagawa error

18 September 2026. **No counterexample.** This audits the concurrent upstream
commit `eff71b0`, received while integrating research/38.

## Published correction, not an inferred historical diagnosis

Ralph H. Fox, *Characterizations of slices and ribbons*, Osaka Journal of
Mathematics **10** (1973), 69--76, printed page 69, footnote 1, states:

> The proof presented in [4] has an error in the second paragraph of p. 380.

Fox then says the authors communicated the error to him, referring to his
diagram 2. Reference [4] is explicitly Hosokawa--Yanagawa, *Is every slice knot
a ribbon knot?*, Osaka J. Math. **2** (1965), 373--384.
[Publisher-text repository copy of Fox](https://www.i-repository.net/contents/osakacu/sugaku/111F0000002-01001-8.pdf).

Thus there is a published, author-acknowledged report locating the error.
This supersedes the upstream note's unsuccessful search for such a report.
Fox's footnote is not a standalone erratum by the original authors, and we
should describe it accurately as Fox's published report of their communication.

## The cited paragraph concerns triple-point elimination

The original paper's page 380 is Section 3, part II, on triple points. Its
second paragraph attempts a cut along an arc avoiding the specified preimage
lines to arrange a favorable local configuration; subsequent cuts are claimed
to remove triple points while retaining the permitted singularities and
boundary knot. This precedes the appendix application.
[Original paper, Osaka University repository](https://ir.library.osaka-u.ac.jp/repo/ouka/all/8798/ojm02_02_10.pdf),
DOI [10.18910/8798](https://doi.org/10.18910/8798).

The appendix on pages 383--384 does **not** end with repeated Dehn's lemma.
It continues with a ball around the first embedded disk, disjoint from the
other boundaries, and an ambient homeomorphism used to move the other disks
off it. It then repeats the process. Omitting that continuation removes the
very argument addressing mutual disjointness.

The elementary mechanism is sound under the full Dehn-disk boundary-collar
hypotheses: obtain embedded disks avoiding the other boundaries; shrink one
disk inside a small ball away from the other disks, then apply the inverse
ambient motion to the other disks while retaining the chosen disk. Their
boundaries remain fixed. Induct in the complement of disks already separated.
Arbitrary nullhomotopies do not supply these Dehn-disk hypotheses.

## Consequence for the research program

The upstream claim that the appendix is the historical failure point, or that
it is the only substantive missing step, is unsupported and should not guide
the search. The primary historical source points to an earlier triple-point
operation. A full reconstruction of Fox's pictured difficulty is not supplied
here; locating the documented error does not itself reconstruct that example.

For our own correction, neither rational nor integral Alexander vanishing
provides the special Dehn-disk or embedded-annulus hypotheses. The lesson is
to record exactly which singularities a proposed geometric move creates,
including its effect on boundary curves and other sheets. It is not a theorem
that a counterexample must arise from a universally linked derivative system.

Scope: source text, appendix continuation, and references checked. One PDF
screenshot request timed out; no reconstruction or visual verification of the
figures is claimed. The short independent reading is in
`results/night_2026_09_18_followup/history_review.md`.
