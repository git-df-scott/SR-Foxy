# Pass 03 — ribbon-obstruction source audit

17 September 2026 UTC. Base commit: `0eb81a1a15147b2059b9028d0bbc0f4173f0ad33`.

**NO COUNTEREXAMPLE.** This pass did not construct a disk or prove a knot non-ribbon. It closed two tempting KDG obstruction directions by reading their primary statements/proofs closely enough to determine the logical level at which they vanish.

## New result 1: Turaev Theorem H(ii) is not a usable ribbon-only obstruction against KDG

The repository had listed Turaev's 1983 Theorem H as an under-examined possibly ribbon-only lead because the primary text had not been obtained. The English primary text is now available and the proof resolves the question.

Theorem H(ii) says that for a ribbon knot, Turaev's degree-two nil-form `F_2(l_1(K),l_2(K))` is metabolic. But §7.4 proves this implication from Lemmas 7.2 and 7.3 together with only the existence of a smooth disk `D ⊂ B^4` for which

`pi_1(S^3 - K) -> pi_1(B^4 - D)`

is surjective. That is the modern homotopy-ribbon group condition. Therefore the same proof applies to any smooth disk satisfying this surjectivity condition; it does not require a band presentation after that hypothesis is supplied.

KDG is already certified handle-ribbon, hence homotopy-ribbon. Consequently its known disk lies on the side where Turaev H(ii) must vanish. Computing this nil-form cannot provide the missing global non-ribbon certificate for KDG. The same caution applies to other candidates only when the required pi_1-surjective disk is actually known.

This corrects the status in `research/02_ribbon_only_obstructions.md`, which had explicitly marked Theorem H as not obtained / possibly ribbon-only. Existing files were not edited in this pass; the correction is recorded here additively.

See `TURAEV_H_AUDIT.md` for the source-level argument and limitations.

## New result 2: Suzuki's ribbon colored-Jones ideal is automatic for plain zero-framed parallels

Suzuki Theorem 2.2 gives the same strengthened colored-Jones ideal containment for an `n`-component **ribbon or boundary link** with zero framing. A zero-framed `n`-parallel of any knot is a boundary link: choose a Seifert surface and take `n` pairwise disjoint normal translates; their boundary components are the zero-framed parallels.

Therefore every plain zero-framed parallel of KDG satisfies Suzuki Theorem 2.2 whether or not KDG is ribbon. The completed 2-, 3-, and 4-parallel work should not be followed by a colored-Jones-ideal computation on a 5-parallel or larger plain parallel. That route is structurally unable to distinguish ribbonness of the companion.

This does **not** close colored Jones on a non-boundary ribbon-preserving satellite pattern. It closes only the obvious continuation on plain parallels.

See `SUZUKI_PARALLEL_NOGO.md`.

## Strategic consequence

The four-parallel result already passed Eisermann; this pass shows that escalating the same parallel-cable idea to Suzuki's stronger colored-Jones divisibility is also a dead end. Turaev's old nil-form obstruction also dies at the homotopy-ribbon level for KDG.

The sharp known ribbon/handle-ribbon gap remains Miller–Zupan:

- ribbon iff some derivative on some Seifert surface is an unlink;
- handle-ribbon iff some derivative is an R-link.

For KDG, a genuine non-ribbon proof therefore still requires a tool that survives the known handle-ribbon disk, most concretely a global exclusion of unlink derivatives including after arbitrary Seifert-surface stabilization, or a genuinely new ribbon-only invariant. No finite reduction of that global problem was obtained here.

A secondary live route is a non-boundary multi-component ribbon pattern whose satellite operation preserves ribbonness for ribbon companions and for which Suzuki/Eisermann supplies a condition not already forced by sliceness or boundary-link structure. No such pattern was constructed in this pass.

## Sources

1. V. G. Turaev, *Multiplace generalizations of the Seifert form of a classical knot*, Math. USSR-Sb. 44(3) (1983), 335–361, Theorem H and §7.4. DOI 10.1070/SM1983v044n03ABEH000971. English primary text: https://www.mathnet.ru/eng/sm2474
2. Sakie Suzuki, *On the colored Jones polynomials of ribbon links, boundary links and Brunnian links*, arXiv:1111.6408, especially Theorem 2.2. https://arxiv.org/abs/1111.6408
3. Repository context: `research/02_ribbon_only_obstructions.md`; `CANDIDATE_LEDGER.md`; `results/astra_2026_09_17_overnight/pass02_0410_four_parallel/`.

## Exact next action

Do **not** start a fifth plain parallel. Either (A) derive a stable obstruction to the existence of an unlink derivative under arbitrary stabilization of KDG's Seifert surface, or (B) specify one explicit non-boundary ribbon-preserving multi-component pattern before spending further colored-Jones compute. For D01, continue to leave changed-axis/nonlocal concordance geometry to Opus unless it publishes a concrete object requiring audit.
