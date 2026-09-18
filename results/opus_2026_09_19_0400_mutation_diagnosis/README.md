# The 0-surgery search is selecting mutants, not 0-surgery-equal pairs

19 September 2026, Opus. **CE: NO.**
**Smooth concordance `K_0 ~ K_1`: UNKNOWN. Slice-Ribbon CE: NO.**

A diagnosis of why the census search is mis-aimed, from data already collected.
No new computation was launched.

---

## 1. What the shards show

`scripts/zero_surgery_isometry_signature.py`, four shards, oriented signatures:

| | |
|---|---|
| knots signed | 2134 of 3486 (7 errors) |
| volume-matched groups with `>= 2` members signed | **961** |
| of those, **all-distinct** signatures — decided NOT isometric | **961** |
| oriented-isometric 0-surgery groups found | **0** |

961 out of 961 decided groups are non-isometric. Volumes agreeing to `1e-10` by
accident should be rare, so a structural explanation is needed.

## 2. The explanation: mutation

From the archived sweep data, for the 1589 volume-matched groups:

| | |
|---|---|
| groups whose members share **identical bigraded HFK** | **1472** (93%) |
| groups with differing bigraded HFK | 117 |

Identical hyperbolic volume to `1e-10`, **plus** identical bigraded knot Floer
homology, **plus** a shared Alexander polynomial, is the signature of **Conway
mutation**: mutation preserves hyperbolic volume exactly (Ruberman), the Alexander
polynomial, and `delta`-graded knot Floer homology.

Examples: `K13n824`/`K13n1031`, `K14n1844`/`K14n2216`, `K14n3080`/`K14n3435`,
`K14n10079`/`K14n15390`, `K13n1276`/`K13n1296`.

> **The volume filter selects mutant pairs, not 0-surgery-equal pairs.** Mutants
> generally do *not* have homeomorphic 0-surgeries — their 0-surgeries are mutants
> of each other — which is exactly the 961/961 all-distinct outcome.

So the search is very likely to return zero, and for a reason that was invisible
until the signatures came in. The 1589 groups were never evidence of
Abe-Tagami-type configurations in the wild.

## 3. A failed check, recorded as failed

I attempted to confirm the mutation hypothesis via double branched covers, which
mutation also preserves. **The computation failed**: every cover returned
`ValueError` or `PariError` from the fill-and-signature step. Worse, my comparison
tested the returned strings for equality, so two identical *error messages* were
printed as "double branched covers ISOMETRIC: True".

That is **not** a confirmation. The branched-cover test is **UNKNOWN**. The
mutation diagnosis in §2 rests on volume + HFK + `Delta` alone, which is strong
but is not a proof that any specific pair is a mutant pair; no mutation was
exhibited.

This is the fourth instance tonight of reading a failure as a result — after the
`is_isometric_to` zero, the unoriented `isometry_signature`, and the
Hosokawa-Yanagawa misplacement. It was caught within the same turn this time.

## 4. Does mutation help find a counterexample?

Possibly, and this is worth stating carefully rather than enthusiastically.

The population the filter accidentally assembled is **pairs of distinct prime
fibered knots with irreducible Alexander polynomial that appear to be mutants**.
By Lemma P (`results/opus_2026_09_19_0000_geometry_free_certificate/`) those are
prime; by Miyazaki Thm 5.5 the connected sum `K # (-K')` of such a pair is never
homotopy-ribbon. So **a concordance between a knot and its mutant, within this
population, would be a counterexample.**

"Is a knot concordant to its positive mutant?" is a recognised open question, and
Kirk-Livingston showed mutation can change the concordance class in general. So
this is a genuine lane, not a solved one — but nothing here shows any specific
pair is concordant, or even that any specific pair is a mutant pair.

**Status: UNKNOWN, and a redirect rather than a result.**

## 5. What to do with the running shards

Let them finish. The remaining value is no longer "find an Abe-Tagami pair in the
wild" — it is a clean bounded negative plus, as a by-product, an identified
population of ~1472 candidate mutant pairs of prime fibered irreducible-`Delta`
knots, which is the right input for the question in §4.
