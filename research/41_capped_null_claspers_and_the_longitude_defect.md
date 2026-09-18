# Capped null claspers and a hidden longitude defect

18 September 2026. Constructive continuation of research/40.

## Exact question and success criterion

Can a geometric operation insert a commutator from the explicit correction
while retaining the original auxiliary unlink and its exact equivariant
linking matrix E=0? The objects are the fixed ribbon boundary R and the two
0110 auxiliary curves. The smallest tested factor is

    [x3^-1 x4, x1^-1 x3] = x3^-1 x4 x1^-1 x3 x4^-1 x1.

A successful local construction must record the embedded operation, its based
word effect, framings, and its effect on E. A group-word identity alone is
insufficient. Even a successful local construction would still require the
remaining factors, an embedded annulus in an identified disk exterior,
standardness of the four-dimensional modification, and a nonribbon certificate
for the actual resulting boundary. Its Alexander polynomial alone would not
identify that boundary with the Abe--Tagami connected sum.

## 1. Stronger preservation available from an actual null surgery

The abstract-form warning in research/40 remains correct, but there is a
stronger statement when an actual surgery and common exterior are specified.
Moussard's proof of Lemma 2.1 preserves ordinary linking of lifted external
curves by replacing the interior pieces of a bounding surface inside the
LP-replacement. Applying the argument to annihilator multiples and deck
translates preserves the **exact rational equivariant linking**, with fixed
lifts and push-offs. Thus an actual null LP-surgery away from the marked
curves need not leave an uncontrolled Laurent error. This is an inference
from the proof, not merely from the quotient-valued theorem statement.
Choose the external push-offs and lifted bounding chains in general position
against all relevant deck translates; the surgery identification must respect
the meridian orientation defining the deck variable.

Source: Delphine Moussard, *Rational Blanchfield forms, S-equivalence, and null
LP-surgeries*, Bull. Soc. Math. France 143 (2015), 403--431,
DOI [10.24033/bsmf.2693](https://doi.org/10.24033/bsmf.2693).
[Author preprint, Section 1.5 and Lemma 2.1 proof](https://arxiv.org/pdf/1207.1954),
checked 18 September 2026. Section 1.5 also records Borromean surgeries as
integral LP-surgeries.

### A conditional geometric criterion

Suppose an embedded, framed Y-clasper G has annular leaves and satisfies:

1. N(G) is disjoint from R, both auxiliary curves, and their chosen push-offs.
   It is a null LP-surgery handlebody relative to R. For the usual Y-neighborhood,
   this requires checking the leaf cores generate H1 and each has linking
   number zero with R.
2. A cap D3 completes the third leaf to a disk-leaf, with the matching framing.
   Its interior is disjoint from R, eta1, and the rest of G, and meets eta2 once.
   The cap-completed model describes the **same surgery** as the annular model.
3. Another cap D1 completes a leaf to a trivial disk-leaf for the eta-sublink:
   it is disjoint from eta1, eta2, and the rest of G. It may meet R. This
   completion again describes the same surgery. No mutual-disjointness of the
   two alternative caps is inferred or needed for the separate applications.

Then the move can be identified back into S3 with R fixed, the auxiliary pair
is still an unlink, and its exact matrix E is preserved under the transported
marking. In particular E=0 remains E=0.

**Proof of the implication.** Use D3 to obtain a tame identification h_R of
the surgered manifold with S3, supported away from R. Before applying h_R,
Moussard's common-exterior calculation gives E_G(eta_ext)=E_R(eta). Applying
the orientation-preserving diffeomorphism h_R and transporting lifts and
push-offs leaves those numbers unchanged. The fact that D3 crosses eta2
does not invalidate that invariance: the image is the modified curve.

Separately, use D1 after omitting R. The trivial disk-leaf gives an
identification h_eta under which the auxiliary sublink retains its unlink
type. The transition h_R h_eta^-1 is a diffeomorphism of S3, so it takes
disjoint spanning disks to disjoint spanning disks. The unlink conclusion
does not require this transition to fix R.

The clasper ingredients are Habiro's definition of surgery by replacing
disk-leaves with annular leaves, the cap-supported identification in
Proposition 2.2, and Propositions 3.3--3.4 on tameness and trivial disk-leaves.
Source: Kazuo Habiro, *Claspers and finite type invariants of links*, Geometry
& Topology 4 (2000), 1--83,
DOI [10.2140/gt.2000.4.1](https://doi.org/10.2140/gt.2000.4.1),
[published paper](https://msp.org/gt/2000/4-1/gt-v4-n1-p01-p.pdf),
checked 18 September 2026.

This criterion is **conditional**. We have not supplied a marked embedding G
and these caps for the displayed factor, nor verified that its transported
axis word changes by precisely that factor. In particular, the fact that a
leaf has zero linking with R does not supply a cap with the required
disjointness. The proposed leaf labels are u=x3^-1 x4 and v=x1^-1 x3, with
the third leaf a meridian of eta2. They satisfy the homological nullness
test, but that is only one hypothesis.

## 2. A concrete local implementation has a peripheral defect

We tested a different, fully specified local model: three parallel R strands
and one auxiliary strand h. Give the first three meridians weight t and h
weight 1. Pure braids move the fourth strand around the first three. After
calibrating the point-pushing convention and based meridians, the target word
is exactly the displayed commutator, under x3 -> a, x4 -> b, x1 -> c.

For that order an explicit 14-crossing braid is

    [-3,-2,1,1,-2,3,3,-2,-1,-1,2,2,2,-3].

Positive sigma_i acts on meridians by

    (X_i,X_(i+1)) -> (X_i X_(i+1) X_i^-1, X_i).

The script tracks a conjugating word w for the auxiliary meridian. With the
campaign's transport convention X_out=lambda^-1 X_in lambda, the longitude
is lambda=w^-1. Its exponent in h is zero. Deleting h from lambda and freely
reducing gives precisely

    a^-1 b c^-1 a b^-1 c.

The surprising part is the peripheral calculation. The specialized full
meridian Fox Jacobian is I_4, but the longitude Fox row is

    (0, 0, 0, 2-t-t^-1).

Testing all six orders of the three R strands gives the same nonzero
polynomial up to sign. Its ordinary specialization at t=1 is zero. Thus
ordinary linking and the meridian Jacobian would both miss the defect.

This is a **local Fox-longitude statement**. It is not an already-computed
E22 entry for a new full scaffold link. To use it as a global response change,
the local meridians, transported longitude, lifts, and framing must be matched
at a physical splice. Formally, once those identifications are fixed, the
identity meridian transfer leaves the exterior linear Fox relations unchanged,
while the added longitude row contributes this coefficient in the auxiliary
meridian direction. We have not constructed or certified that full splice.

The calculation does not contradict the capped-null-clasper criterion. We
have not shown this particular braid is the same marked surgery as a clasper
satisfying its cap hypotheses. The same free word can carry different
peripheral data. Consequently replacing a specified clasper by this convenient
point-pushing braid would require an additional equivalence proof.

The producer uses free-word Artin substitution. An independent checker uses
only Laurent first jets: F(ab)=F(a)+t^e(a)F(b) and
F(a^-1)=-t^-e(a)F(a). All six cases pass, together with inverse-generator and
braid-relation controls. A falsely zeroed longitude row is rejected. No knot
census, HFK computation, or unbounded group search is involved.

## 3. The saved collar also passes a necessary peripheral test

Starting at scaffold port (1,1), the meridian is boundary x5. Oriented
undercrossing traversal gives upper and lower transport words

    U=[4,-3,1,5,-1,-5,-4,9,-1],
    L=[14,-11,15,11,15,-11,-15,-13,17].

Their exponent sums are -1 and +1, so UL has total writhe zero and is the
preferred boundary longitude in these conventions. In the saved source
presentation, let u=q0(U), l=q0(L), and mu=q0(x5)=q0(x15). We certify

    u l=1,        [u,mu]=1.

Each identity reduces by just three recorded relator applications, with the
archived Tietze and derived-relator provenance replayed independently.
Therefore every saved partial-conjugation map satisfies

    q_n(lambda_R)=u mu^n l mu^-n=1,       for every integer n.

This is a genuine necessary-condition pass. It does not identify q_n with a
particular marked disk exterior. The independent checker also follows the
meridian through every crossing and rejects a corrupted crossing sign.

## 4. What to do next

The next object should be a **marked capped-clasper diagram**, beginning with
the small factor, with the two alternative caps and its based word effect
checked. If that succeeds, exact E-preservation can follow from the criterion
rather than a fresh large matrix computation. The whole correction would
still require ordered composition, and the disk and actual nonribbon boundary
remain separate obligations.

Subsequent update: research/42 develops a different, whole-surface realization
argument. It keeps this capped-clasper construction as an independent local
diagrammatic audit rather than the only remaining boundary-level route.

For comparison, Conway--Piccirillo--Powell's Lemmas 5.2--5.3 can adjust
off-diagonal and diagonal Laurent entries while preserving the relevant
lifted isotopy classes. Projecting those isotopies gives free homotopies, but
not an unlink guarantee. This alternative therefore does not remove the
simultaneous-realization problem. Source: *4-manifolds with boundary and
fundamental group Z*, Comment. Math. Helv. 100 (2025), 323--420,
DOI [10.4171/CMH/587](https://doi.org/10.4171/CMH/587),
[published paper, pp. 355--356](https://ems.press/content/serial-article-files/50353?nt=1),
checked 18 September 2026.

Artifacts and independently replayable certificates:
`results/night_2026_09_18_geometric_gate/`.
