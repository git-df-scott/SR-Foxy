# Infection does not automatically preserve our target

13 September 2026. **No counterexample found.** This corrects the earlier light-literature suggestion to use a joint unlink movie followed by infection without first checking the resulting boundary type.

## Question and success criterion

Can mixed axes in the product-disk scaffold yield the fixed, independently nonribbon fibered target D = K1 # (-K0) by Cochran–Davis infection? A successful counterexample still requires a smooth disk in standard B4 and global nonribbonness of its boundary. An annulus certificate alone does not identify that boundary.

## Established source facts

Hirasawa, Murasugi and Silver, *When does a satellite knot fiber?*, arXiv:0705.0012v1, submitted 30 April 2007, Theorem 2.1 and its proof: a fibered satellite has nonzero winding; its companion and its pattern **in the solid torus** must be fibered. Fiberedness of the pattern knot in S3 alone is insufficient. [Primary paper](https://arxiv.org/pdf/0705.0012).

Cochran and Davis, *Counterexamples to Kauffman's Conjectures on Slice Knots*, arXiv:1303.4418, 2013, Proposition 2.2: infection multiplies the Alexander polynomial by Delta_J(t^w), where w is axis linking number. Theorem 3.1 gives smooth sliceness in standard B4 from the specified slice disk and disjoint embedded annulus with unlink boundary, using companions J and -J. These statements do not assert that an arbitrary resulting knot is nonribbon. [Primary paper](https://arxiv.org/html/1303.4418). Sources checked 13 September 2026.

## Deductions for our proposal

Every marked auxiliary circle links R zero times. An oriented band sum in the complement represents the sum of the two homology classes: the band gives a pair of pants in that complement. Therefore **every band routing using the proposed summands still gives winding zero**. Changing a band's path cannot repair this.

If a zero-winding infection torus is incompressible in the final exterior, its Z^2 fundamental group injects into the knot group and lies in the kernel of abelianization. For a fibered knot that kernel is a free group, which contains no Z^2. Thus this infection output is not fibered and cannot be D. This is a conditional obstruction: incompressibility has not been checked for any constructed mixed axes, because no such axes have yet been constructed. Compressible tori and trivial companions are outside this argument. Annulus Dehn twisting is a different operation and is not excluded by it.

## Algebraic variation and its cost

In the saved compact presentation, the abelianization is a -> -3, b -> 2; the meridian mu = bba has value one, while u and v have value zero. Proposed words

    eta1 = u v mu,    eta2 = v mu u
    u^(-1) eta1 u = eta2

are conjugate already in the free group and both have winding one. Adding meridian summands is therefore a possible *algebraic* redesign. It supplies neither actual disjoint unlink axes nor an embedded annulus, and does not establish a fibered pattern.

There is an unavoidable target cost for this redesign with a nontrivial fibered companion. The two infections multiply Delta_R by Delta_J(t)^2, up to Laurent units, since reflection/reversal preserves the Alexander polynomial up to units. But Delta_D = Delta_R = (t4 - 3t3 + 5t2 - 3t + 1)^2. A trefoil companion pair increases the polynomial span from 8 to 12. More generally a common nonzero winding w increases span by 2|w| span(Delta_J); a nontrivial fibered companion has positive span. This cannot give our fixed D.

`scripts/mixed_infection_design_gate.py` checks linking sums, the group abelianization, both conjugacy identities, and the trefoil polynomial calculation using exact integers. Its JSON explicitly lists the unverified geometric hypotheses. It does not computationally certify the source theorems or an actual infection diagram.

## Next falsification check

Keep the two projects distinct. For the fixed D, identify a concrete annulus-twist surgery link and its boundary before investing in a disk construction. For infection, first choose a new target and a nonribbon certificate that applies to its boundary type; if pursuing fibered output, construct and test a fibered solid-torus pattern. The winding-one words are only a starting constraint, not a candidate counterexample.
