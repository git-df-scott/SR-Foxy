# Exact identification and primary annulus work

18 September 2026. Written handoff; no external message sent.

**No Slice--Ribbon counterexample has been established.** The new work makes
two computational checks exact and develops a boundary modification mechanism
for the first annulus obstruction. It does not produce the required embedded
annulus or identify its resulting surgery boundary with a certified nonribbon
knot.

## Read first

1. `research/44_positive_combinatorial_K1_identification.md` and
   `results/night_2026_09_18_positive_identification/`: stored K1 matches the
   specified filling of stored L by a positive oriented simplicial map.
   Independent integer-only replay checks 48 faces for K1 and 24 for K0;
   four corrupt maps are rejected. Kernel filling/retriangulation is trusted;
   numerical hyperbolic canonicity is unnecessary for this positive result.
   The paper figure-to-L correspondence remains unverified.
2. `results/night_2026_09_18_jones/`: full exact Jones polynomials for the
   stored K0 and K1, without Sage. Their exponent ranges are [-3,3] and
   [-9,5]. Distinctness, including K0 versus mirror(K1), therefore does not
   need unequal numerical isometry signatures. The bounded 19-crossing
   state sum took about one second, retaining only a small integer histogram.
3. `research/46_paired_clasps_and_the_primary_annulus_obstruction.md`:
   opposite clasps on words g,h with equal meridional exponent cancel their
   exact cyclic linking changes but alter the full-group annulus sum by
   [q(g)]-[q(h)]. The hypotheses include a specified geometric surjective q,
   fixed annulus markings, and transported standard bands.
4. `research/47_cyclic_annulus_gate_from_exact_boundary_linking.md`:
   the independently audited chain argument supplying cyclic vanishing from exact E=0 in
   a genuine slice-disk exterior. Read the proof and its geometric hypotheses;
   none is replaced by a saved group homomorphism.
5. `research/45_mutation_lead_source_audit.md`: the universal positive-mutant
   concordance assertion is false (Kirk--Livingston), and full bigraded HFK
   is not generally mutation invariant. The reported candidate groups have
   not been certified as positive mutant pairs.

## Highest-value geometric tasks

- Identify the saved q0 with inclusion into an explicit marked product-disk
  exterior. Retain the exact seam bridge and whiskers: changing the bridge
  conjugates only one factor and can replace q0 by q_n.
- Construct an immersed annulus movie for the repaired axes and record all
  signed full-group double-point labels and relative normal framing. Then
  realize one paired-clasp correction in the marked diagram and inspect its
  Whitney disks. A group identity alone does not record this movie.
- Track the actual surgery boundary after every permitted axis modification.
  The earlier nonribbon certificate for an Abe--Tagami knot does not transfer
  merely because the axis words and E remain unchanged.

Two further audit points: H2 of a slice-disk exterior is zero, so it cannot
contain an algebraically dual sphere with intersection 1 against the annulus.
Also, unequal unverified canonical signatures remain numerical exclusions;
the positive simplicial-map argument does not validate negative shard results.

The product-collar groupoid formulas remain suggestive: if P_f is a bridge
through face f, upper meridians have form P_R P_L^-1 while lower meridians
have form P_L^-1 P_R. Identifying a base bridge produces the saved conjugation
formulas. This is not yet the required marked global flattening certificate.
