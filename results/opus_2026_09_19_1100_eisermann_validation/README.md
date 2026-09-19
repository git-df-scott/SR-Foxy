# Validating the Eisermann pipeline before it is pointed at `L_{3,1}`

19 September 2026, Opus. **CE: NO.** A validation, not a search — it cannot find
a counterexample, only prevent a fake one.

## Why

`research/53` sets out the GST link lane: if `det V(L_{3,1}) != 17 (mod 32)` then
`L_{3,1}` is slice and not ribbon, the first such object of any kind. The lane
has been blocked all campaign because an isolated computation on a hand-traced
diagram cannot be trusted — a tracing slip or a convention error yields a wrong
residue that **looks exactly like a counterexample**.

So before any GST object is built, the pipeline itself should be exercised
against ground truth. SnapPy ships `RibbonLinks`: **12,184 links each carrying a
ribbon certificate**. Every one must satisfy

* **Theorem 1** `null V(L) = n - 1`
* **Theorem 2** `det V(L) = det(K_1)...det(K_n)  (mod 32)`

A single violation would mean the implementation or the convention is wrong.

## Result

| | |
|---|---|
| certified ribbon links evaluated | **599** |
| **Theorem 1** `null V = n-1` | **599 pass, 0 fail** |
| **Theorem 2** `det V = prod det(K_i) (mod 32)` | **599 pass, 0 fail** |
| with **knotted** components (non-trivial Theorem 2) | **431**, all passing |
| **at the GST residue 17 mod 32** | **134**, all passing |
| tool failures | **0** |

Residue distribution of `prod det(K_i) mod 32`: `{1: 190, 9: 164, 17: 134, 25: 133}`.

**The pipeline returns the right answer on 134 certified ribbon links sitting at
exactly the residue `L_{3,1}` is tested against**, and on 431 with genuinely
knotted components where Theorem 2 is not the trivial `1 = 1`. That is the
calibration `research/53` asked for, and it is now in hand before any GST object
exists. A hand-traced `L_{3,1}` returning a residue other than 17 can no longer
be dismissed as a convention or normalisation artefact of this code.

It does not validate a *tracing* of Figure 1 — only the machinery that would be
applied to it. `research/53`'s in-family controls (`L_{1,1}` must give 9,
`L_{2,1}` must give 17) remain the next step and are still unattempted.

## The two faults fixed to get here

1. `sagefree_eisermann.component_determinants` reaches `Link.determinant()`,
   which this repository already records as **Sage-only** — the same fault that
   once made every fission script here vacuous. Replaced with a per-component
   Seifert determinant.
2. That then raised `UnboundLocalError: 'start'` inside spherogram on **65 of 73**
   inputs. Cause: components surviving as **0-crossing diagrams**. Such a
   component is an unknot with `det = 1`; the Seifert routine cannot take an
   empty diagram. One guard took the error count from 65 to **0**.

## Earlier, weaker run, kept for the record

Before those fixes: 8 links evaluated, 8/8 passing, but 6 of them with unknot
components so their Theorem-2 test was the trivial `1 = 1`, none at residue 17,
and 65 tool failures. The script's verdict line then read as a clean bill of
health on an easy sample, so it was changed to demand at least 25 evaluated
links including 5 with knotted components before saying "validated". That
threshold is what the 599-link run clears.
