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

## Result, stated with its limits

| | |
|---|---|
| links evaluated | **8** |
| Theorem 1 | **8 pass, 0 fail** |
| Theorem 2 | **8 pass, 0 fail** |
| of those, with **knotted** components | **2**, both at residue **9 mod 32** |
| at the GST residue 17 mod 32 | **0** |
| tool failures | **65** |

**This is not yet a validation and the script no longer claims it is.** Eight
links, of which six have unknot components so their Theorem-2 test is the
trivial `1 = 1`, is a small and easy sample. The verdict line was initially a
bare "no failures seen", which would have read as a clean bill of health; it now
requires at least 25 evaluated links including 5 with knotted components before
it will say "validated", and otherwise prints **INCONCLUSIVE**.

What *is* established: **no certified ribbon link violated either theorem**, and
the two non-trivial cases both landed on residue **9**, which is exactly
`L_{1,1}`'s predicted value in `research/53`'s table. That is mildly encouraging
about conventions and nothing more.

## The blocker, and it is a known one

65 of 73 inputs failed with `UnboundLocalError: cannot access local variable
'start'`, raised inside spherogram's Seifert-matrix path when a single component
is extracted with `Link.sublink([i])`. It is a library fault on particular
diagrams, not a property of the links.

Note the first version of this script hit the *other* known fault instead:
`sagefree_eisermann.component_determinants` reaches `Link.determinant()`, which
this repository already records as **Sage-only** — the same fault that once made
every fission script here vacuous. It was replaced with a Seifert-matrix
determinant per component; that is what now hits the `sublink` bug.

**Next step** is to compute the component determinants without `sublink` — the
components can be read off the PD code directly, or `det = |Delta(-1)|` taken
from the Burau route in `results/opus_2026_09_19_0900_bigrading_audit/`, which
passed 9/9 controls and does not touch spherogram's Seifert code. With that,
the sample should open up to thousands, including the knotted cases the GST test
actually depends on.
