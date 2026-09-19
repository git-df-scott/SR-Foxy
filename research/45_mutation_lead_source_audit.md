# Mutation is a candidate relation, not a concordance construction

18 September 2026. Primary-source audit of the incoming Opus lead.

The reported 1472 groups are **candidate groups**, not certified mutant pairs.
This pass did not recompute that count. Equal volume, Alexander polynomial,
and HFK do not exhibit a mutation sphere, its tangle involution, or the
orientation compatibility required for positive mutation.

Two distinctions change how to use this population:

1. Full bigraded knot Floer homology is not generally mutation invariant.
   Peter Lambert-Cole explicitly discusses mutants distinguished by it, then
   constructs twist families where the bigraded groups eventually agree:
   *Twisting, mutation and knot Floer homology*, Quantum Topology 9 (2018),
   749--774, DOI [10.4171/QT/119](https://doi.org/10.4171/QT/119),
   [Theorems 1.1--1.2 and introduction](https://ems.press/content/serial-article-files/36858).
   Claudius Zibrowius's later theorem concerns the **relatively delta-graded**
   hat theory: *On symmetries of peculiar modules, or delta-graded link Floer
   homology is mutation invariant*, JEMS 25 (2023), 2949--3006,
   DOI [10.4171/JEMS/1201](https://ems.press/journals/jems/articles/6800417).
   These gradings must not be conflated.
2. The universal assertion that a knot is concordant to its positive mutant
   is already false. Paul Kirk and Charles Livingston distinguish the positive
   mutant pretzels P(-3,5,7,2) and P(5,-3,7,2) up to concordance:
   *Twisted knot polynomials: inversion, mutation and concordance*, Topology
   38 (1999), 663--671, DOI
   [10.1016/S0040-9383(98)00040-8](https://doi.org/10.1016/S0040-9383(98)00040-8),
   [primary paper](https://www.maths.ed.ac.uk/~v1ranick/papers/kirkliv2.pdf).
   Their later *Concordance and Mutation*, Geometry & Topology 5 (2001),
   831--883, DOI [10.2140/gt.2001.5.831](https://doi.org/10.2140/gt.2001.5.831),
   gives infinite families. A particular census pair can of course remain open.

All sources checked 18 September 2026, with a separate Luna literature audit.
The negative examples do not exclude concordance for every positive-mutant
pair, and do not establish a result for any of the proposed census pairs.

## A useful narrowed task

Select one actual pair and exhibit its Conway sphere as four marked endpoints
in a diagram. Check the tangle rotation and orientations explicitly. Then ask
for a concordance of that tangle, relative to those endpoints, to a tangle
invariant under the rotation. Such a concordance, together with its rotated
copy, would induce a concordance of the closed mutants. The nontrivial task is
constructing this relative concordance; invariant matching does not supply it.

A symmetry extending as an isotopy of the tangle only proves the mutant is
isotopic to the original, which cannot supply two distinct knots for the
desired counterexample. Any proposed construction must therefore retain a
separate certificate of distinctness. No qualifying concordance was found in
this bounded source pass.

This makes the mutation population a useful source of explicit geometric
problems, but not a replacement for the missing annulus construction. The
positive combinatorial K1 audit in research/44 makes immediate progress without
depending on that population or on the running shards.
