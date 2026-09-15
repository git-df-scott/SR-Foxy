# Band count is not forced by genus

15 September 2026. **No counterexample found.** This note tests a claim that
`research/05_adversarial_memo.md` §3.6 raises and explicitly labels
`UNVERIFIED`, and reports evidence against it.

## The claim under test

§3.6 asks how many band moves a ribbon disk might need, and reasons:

> A ribbon disk for a genus-$g$ knot corresponds to an unlink derivative on a
> genus-$g$ Seifert surface (Miller–Zupan Prop. 1.1), so the natural band count
> for $K_G$ is **5** — one past DG's search ceiling of 4. [...] If the relevant
> unlink derivative lives on the genus-5 fiber surface, a fusion-number-5 ribbon
> disk is exactly the object a $\le 4$-band search structurally cannot find.

The memo flags this as a heuristic and not a theorem. It matters a great deal
here, because if band count were forced upward by genus, **every Teichner run in
this repository would be searching a box that is empty in advance**: the sweep
runs at `max_bands = 2` against sums of genus 5 to 7.

| sum | genus |
|---|---|
| `D_{0,1}` alone | 4 (fibered, tau 0) |
| `D_{0,1} # 6_1`, `# 9_46`, `# 10_3` | 5 |
| `D_{0,1} # 8_8`, `# 9_41` | 6 |
| `D_{0,1} # 10_22`, `# 10_87` | 7 |

## The test

Take known ribbon knots of known genus and find the smallest band budget at
which `spherogram`'s search actually reaches the unknot.

| knot | Seifert genus | unknot reached at |
|---|---|---|
| `6_1` | 1 | 1 band |
| `9_46` | 1 | 1 band |
| `10_3` | 1 | 1 band |
| **`8_8`** | **2** | **1 band** |
| **`9_41`** | **2** | **1 band** |

Negative controls, which must never reach the unknot and do not:
`3_1`, `4_1`, `5_2` — none reaches the unknot at 1 or 2 bands.

The `8_8` certificate at one band is explicit:
`[[(4,15,5,0),(0,5,1,6),(10,2,11,1),(2,12,3,11),(6,3,7,4),(14,8,15,7),(8,14,9,13),(12,10,13,9)], '0805_0_1', 'unknot']`.

## Reading

**Genus does not bound fusion number from below.** `8_8` and `9_41` have genus 2
and fusion number 1. The direction that is actually proved runs the other way
and is already in this repository: `research/06` §Lemma 1.2 records Miller–Zupan
as giving fusion number $\le 2g-1$, an **upper** bound. Nothing forces a
genus-$g$ knot to need many bands.

So the §3.6 worry, in the form that would have invalidated this campaign's
Teichner sweep, does not hold. A low-band search on a high-genus knot is not
structurally doomed.

## What this does NOT establish

It does not show the 2-band searches are adequate. It removes one specific
argument that they are inadequate, and nothing more. A ribbon disk for
`D_{0,1} # J` may still need more than two bands for reasons unrelated to genus;
Dunfield–Gong found 75 disks needing four. The distribution in their Table 7 is
over disks a $\le 4$-band search *found*, and §3.2 of the adversarial memo is
right that this is selection-biased.

The practical consequence is narrow and worth stating exactly: the three dials
`UNFINISHED.md` §6 identifies as untouched — `paths='simple'`, `max_twists`,
diagram choice — all widen the band **set** at a fixed band **count**. Had band
count been forced up by genus, spending compute on those dials would have been
searching harder in a place where the answer could not be. That objection is now
answered, so the dial choice stands.

## Provenance

SageMath with SnapPy 3.3.2 (`spherogram.links.bands.search`), installed in this
container for the first time; `Link.signature()` and `ribbon_concordant_links`
both raise `SageNotAvailable` in bare CPython, exactly as `TOOLING.md` records.
Genus and fiberedness from `knot_floer_homology()`.

One methodological note, since it nearly produced a false entry here: the first
version of this test passed `certificates=True`, which is not the keyword (it is
`certify`), inside a `try/except` that swallowed the `TypeError`. Every knot came
back "no certificate found", including `6_1`. A search harness that reports a
failure it did not run is the same hazard as the `simplify('global')` bug in
`research/19` §8. The controls above exist so that cannot pass silently again.
