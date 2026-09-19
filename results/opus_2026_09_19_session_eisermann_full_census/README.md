# Eisermann validation completed on the whole RibbonLinks census

**19 September 2026. CE: NO.** Step 0 of `research/53`'s calibration ladder,
which `HANDOFF_2026_09_19_OPUS_NIGHT.md` §3 recorded as "started and stuck"
(8 links evaluated, 65 of 73 inputs dead on `UnboundLocalError: 'start'`), is
finished.

| | |
|---|---|
| links evaluated | **12,184 / 12,184** (the entire SnapPy `RibbonLinks` census) |
| tool failures / skips | **0** |
| Theorem 1 violations | **0** |
| Theorem 2 violations | **0** |
| links with a **knotted** component | **8,546** |
| links at residue **17 mod 32** | **2,081** |
| crossing range | 6 – 38 |
| wall time | 172 s |

Every link in this census is a certified ribbon link, so every one of them
*must* satisfy Eisermann Theorem 2. All 12,184 do.

## What was actually blocking it

`Link.sublink([i])` dies inside spherogram's Seifert path. The handoff's
proposed fix — take component determinants without `sublink` — is implemented
in `compdet.py`: other components are spliced out directly on the crossing
graph, and `det(K) = |V_K(q=i)|` is then read off the repository's own
`sagefree_jones`, the same code path already validated on the Eisermann
controls.

## A wrong first run, and the control that caught it

The first version of that splice classified a crossing as a self-crossing only
when the component contributed **four** strand indices. A component running
through its own crossing contributes **two** (the reverse traversal is not
listed), so every crossing was spliced out and every component was returned as
an unknot. That run reported **424 "violations" in 700 certified ribbon links**.

It was caught by a control, not by inspection: `5_1`, a one-component knot that
requires no splicing at all, returned determinant 1 instead of 5. The control
set is in `validate_census.py`'s companion checks — trefoil 3, `4_1` 5, `5_1` 5,
square knot 9, and the same knots with a split unknot added.

**Had that run been believed, it would have produced 424 false counterexamples.**
That is the exact failure mode `research/53` §2 names as the worst available
outcome, reached here through a component-determinant bug rather than a mistrace.

## Why this matters for `L_{3,1}`

The standing objection to the `L_{3,1}` lane is that an isolated `det V` from a
hand-built diagram cannot be trusted. Two specific worries are now closed:

1. **Knotted components.** The earlier partial run had only 2 links with
   knotted components. Here 8,546 do, and the observed component determinants
   include **9 in 2,680 links** — exactly `det(Q) = det(V_3) = 9`.
2. **The disputed residue.** 2,081 links land at exactly **17 mod 32**, the
   residue `L_{3,1}` is tested against, and the pipeline returns it correctly
   on every one.

`det V mod 32` took only the values **1, 9, 17, 25** across all 12,184 links —
all `= 1 (mod 8)`, as Eisermann's corollary requires.

**This validates the tool, not the link.** It says nothing about whether
`L_{3,1}` is ribbon. The in-family rungs `L_{1,1}` (must give 9) and `L_{2,1}`
(must give 17) remain unattempted, because the link itself is still not built.

## Reproduce

```
python validate_census.py 12184        # writes census_validation.json
```
Needs snappy + spherogram; no Sage.
