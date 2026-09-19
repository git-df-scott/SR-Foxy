# GST / Generalized Property R audit

## Exact certified objects

Gompf–Scharlemann–Thompson [S04, §8] construct two-component links (L_{n,k}). Their dual handle description identifies the relevant 4-manifold with the standard (B^4), so both components bound disjoint smooth disks. After fixing a band (b) joining the components, the band sum

\[
B_{n,k,b}=\operatorname{band}_b(L_{n,k})
\]

bounds the disk obtained by boundary-band-summing those disjoint disks. Thus the exact banded knot is smoothly slice in standard (B^4). This is a constructive proof, not an inference from algebraic sliceness.

Known ribbon cases recorded in [S04] are (n=0,1), (k=0), and ((n,k)=(2,1)). The first displayed unresolved test is the Figure 2 band sum associated to (L_{3,1}); this report denotes that exact pictured knot by (B_{3,1}). Crossing counts vary with diagram simplification and are not used as identifiers.

## Exact weaker status

[S04] observes that the displayed slice-link complement is a regular neighborhood of a wedge of two circles. [S05, §6] further identifies GST band sums, after a handle slide, as belt spheres of 2-handles in handle diagrams of (B^4) without 3-handles. Abe–Tange conjecture that every such belt sphere is ribbon [S05, Conj. 6.1]; a conjecture is not a status upgrade.

The handle presentation supplies strong/handle-ribbon-type structure and explains why homotopy-ribbon obstructions do not close the lane. It does **not** establish half-ribbonness: no theorem handle-ribbon ⇒ half-ribbon is invoked.

## Relation to Generalized Property R

If the relevant framed link handleslides to the unlink in the required way, the handle picture yields ribbon disks for associated band sums. The converse is not proved in [S04]: a ribbon disk for one band sum need not force the original two-component framed link to be handleslide trivial. Therefore:

- failure to prove Generalized Property R is not non-ribbonness;
- stable handleslide equivalence is not ordinary handleslide equivalence;
- adding canceling Hopf pairs/stabilization may alter the disk presentation and cannot be silently removed;
- [S14, Thm. 1.1] narrows finite stable-equivalence questions but does not settle ribbonness of (B_{3,1}).

## Diagrams and reproducibility

Best primary presentations:

1. [S04, Figure 2] for the fixed simplest band-sum knot (B_{3,1}).
2. [S04, Section 8] for (L_{n,k}), its dual handle description and slice disks.
3. [S05, Section 6] for the belt-sphere reformulation.
4. [S16] for explicit search encodings and the warning that algorithms fail on known ribbon GST examples.
5. [S14] for 2026 stable-handleslide experiments and exact finite parameter ranges.

## Obstructions actually tested

- Ribbon-band search has been tested on GST examples [S16]. It fails on both unresolved and known ribbon members, so the negative result is inconclusive.
- Stable handleslide computations have been carried out in finite ranges [S14]. They address stable Generalized Property R, not non-ribbonness.
- No primary candidate-specific computation was found for Turaev’s multiplace form [S20], Park–Powell derivative triple linking [S17], irregular dihedral covers [S13,S18], or a global unlink-derivative exclusion [S02].
- The irregular-dihedral/metabelian absence should not be romanticized: these obstruct homotopy-ribbon structure already supplied by the handle construction.

## Why no obstruction closes the candidate

Classical concordance invariants vanish because (B_{3,1}) is smoothly slice. Homotopy-ribbon invariants vanish or are inapposite because of the exhibited disk exterior. Ribbon searches lack completeness. Generalized Property R gives a sufficient handle simplification, not a known necessary one for ribbonness of a chosen band sum. The only exact ribbon characterization in hand is [S02, Prop. 1.1], but it quantifies over Seifert surfaces and unlink derivatives; no finite candidate-complete enumeration is known.

## The missing theorem

The strongest useful missing statement is:

> **GST ribbon-completeness theorem (not known).** For a fixed GST band-sum knot (B_{n,k,b}), every ribbon disk can be converted, without stabilization, into the disk induced by an ordinary handleslide trivialization of the associated framed GST link; equivalently, every unlink derivative from [S02, Prop. 1.1] can be normalized into the GST handle presentation.

With this theorem, an exact proof that the framed link is not handleslide trivial would prove (B_{n,k,b}) non-ribbon. Current stable equivalence results do not supply either half.

A less GST-specific missing theorem is:

> **Fibered ribbon-disk completeness (not known).** Every ribbon disk bounded by a fibered knot is fibered.

If (B_{3,1}) is verified fibered, [S09] could then reduce the disk search to finitely many monodromy compressions. Fiberedness of this exact band sum was not certified in the audited sources, so this route is presently better for `DG`.

## Adversarial lane analysis

**Strongest reason it might work.** The diagrams are explicit, smooth sliceness is constructive, and ribbonness is tied to a concrete 3-dimensional unlink-derivative condition.

**Strongest reason it probably fails.** The handle structure is already extraordinarily close to ribbon; Abe–Tange’s Conjecture 6.1 predicts every such belt sphere is ribbon. Search failure has near-zero force because known ribbon GST knots defeat the same algorithms.

**Exact missing lemma.** Prove GST ribbon-completeness above, or directly prove that (B_{3,1}) admits no unlink derivative on any Seifert surface.

**Finite verification route if supplied.** Enumerate the finite normalized handle moves/derivatives, verify each by Kirby calculus, and certify non-unlink status by exact π₁, Alexander module or normal-surface recognition.

**Kill condition.** One explicit ribbon band movie or unlink derivative for (B_{3,1}) kills that object. A proof of Abe–Tange Conjecture 6.1 closes the entire GST belt-sphere lane in favor of ribbonness.

## GST verdict

**LIVE but secondary to `DG`.** It is certified-slice and historically central, but `DG` is smaller, fibered, explicitly handle-ribbon in standard (B^4), and now connected to finite monodromy technology.
