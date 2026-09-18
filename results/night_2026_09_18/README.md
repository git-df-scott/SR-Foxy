# September 18: exact mixed-surgery response and a winding repair gate

**CE: NO.** Main mathematical report:
[research/35](../../research/35_mixed_axes_response_and_winding_gate.md).
No disk in standard B4, embedded annulus, concordance, or new nonribbon knot
is claimed. The work is exact algebra for the existing marked diagrams, plus
primary-source and proof audits.

Start: clean `codex/reliable-counterexample-search`, HEAD b7ae727.
The user then explicitly requested existing main and authorized pushing.
Switched to existing main and fast-forwarded to 91732d4. Three concurrent upstream commits through aa2df2c were later read and
fast-forwarded without conflicts; their claims are audited in research/36.
No new branch,
reset, cleanup, force-push, or automatic non-fast-forward merge occurred.

## New results versus reproductions

New:
- Counterexample to the new universal framing-to-polynomial inference: the
  archived 0110 repair has zero linking, zero longitude response, and target
  polynomial at r=1. This is not a counterexample to slice-ribbon.
- An elementary proof that f_r is irreducible for all integers r, and an audit
  distinguishing Miyazaki's failed norm-free alternative from open minimality.
- Two-variable extension of the previously known opposite-twist formula: `d^2+xy*t^2*(t^2-1)^2`, proved by
  the full set of symbolic maximal minors for all integer parameters.
- Exact rational longitude response with zero diagonal and nonzero off-diagonal
  `t*(t^2-1)/d`; a precise explanation of the old one-parameter failure.
- Boundary Alexander coordinates of original and mixed axes, and the
  necessary dependence condition `k-l=2` for the defined winding model.
- Explicit Bezout certificate showing that this winding condition conflicts
  with the trace gate for every saved algebraic collar q_n. This is a word-level
  obstruction, not an identification of an actual collar or a global no-go.
- Correction of the blanket homological Norman-trick dismissal.

Reproduced/input dependencies:
- At surgery parameter 0 the polynomial is d^2; at 1 it is the previously
  saved non-target polynomial. The underlying PD, Fox extractor, source
  representation, and candidate collars were inherited.
- The old auxiliary unlink certificate was read; it was not independently
  re-extracted here. Nor was the PD independently matched to paper figures.
- Luna checked primary Park/Abe--Tange and tubing sources, and independently
  reviewed the abstract residue lemma. No agent ran a knot search.

## Reproduction

Python 3.14.6 and SymPy 1.14.0. Commands below print to stdout and do not
silently replace archived scientific outputs. Run from repository root.

```sh
python results/night_2026_09_18/surgery_response.py
python results/night_2026_09_18/response_matrix.py
python results/night_2026_09_18/axis_module.py
python results/night_2026_09_18/axis_segments.py
python results/night_2026_09_18/winding_trace.py
python results/night_2026_09_18/winding_collar.py
python3 results/night_2026_09_18/check_bezout.py
```

SymPy is required by the algebra producers; axis_segments and check_bezout
use only the standard library. Their deterministic source
inputs and output hashes are in MANIFEST.json. check_bezout uses only the
standard library and verifies an explicit identity, without a Groebner engine.
Producer scripts use 60 or 90 CPU-second limits; no large search was started.
Only one substantive computation ran at a time. RLIMIT_AS was not used because
macOS does not reliably implement it; matrices here have at most 64 rows.
No process is promised to survive the session. An isolated dependency venv
was installed at /tmp/sr-foxy-night-venv; it is disposable and not committed.

## Files and failures

The two upstream closure-check producers were corrected to report only the
arithmetic they actually check. The unconditional True asserting that
Miyazaki minimality is incompatible with the goal was removed. Corrected
outputs are framing_arithmetic_corrected.json and miyazaki_algebra_corrected.json;
the historical upstream RESULTS.json files were preserved unchanged.
repair_0110_response.py rechecks the zero response and the target Fox order
for the existing 0110 diagram. See research/36 for the exact refuted inference.


- surgery_response.jsonl: full reduced 7x6 matrix and all seven maximal minors.
- longitude_response.json: independently eliminated rational longitude matrix.
- axis_module_verified.jsonl: boundary-module proof output with relator checks.
- axis_module.jsonl: earlier output, agrees with the subsequently checked version.
- axis_segments.jsonl: each traversed half-edge, side label, and contributed word.
- winding_trace.json: word segments and exact q0 trace polynomial.
- winding_collar.json: all-q_n equations and explicit Bezout multipliers.
- bezout_check.json: independent rational identity check, two mutation rejections.
- literature.md, algebra_review.md, source_check.md: targeted Luna audits,
  reviewed and scoped by the main agent.
- response_exploratory.jsonl: **superseded exploratory output**. SymPy's gcd
  applied directly to Laurent rational expressions returned 1 despite the
  visible common numerator. That field and its `opposite: 1` are invalid and
  must not be used. The corrected script clears t-denominators first and
  verifies every minor is a Laurent unit times the displayed numerator.
- Initial winding_trace serialization failed because a SymPy Boolean was not
  JSON serializable. The computation completed but no JSON certificate was
  produced until conversion to Python bool. It was not a mathematical failure.
- System and bundled Python lacked SymPy. The isolated venv resolved this.
- A web PDF screenshot and an arXiv HTML version fetch failed; the primary
  source check used the published and author PDFs instead. No screenshot
  from the failed call is represented as inspected.

## Orientation and recovered-evidence scope

Read the supplied night-session handoff; local HANDOFF and Session September16
(the combined shell output was truncated, so no claim of full historical
coverage); current Opus handoff through its priority discussion; construction
card; research12,14,15; relevant sections of research33/34; current collar and
dual-path README/audit reports; passes05/06/07 and pass09; September16 summary,
followup summary, Claude review audit and selected raw response fields; and
the latest census-recovery README. The raw Claude response was not re-audited
in full. No full dataset re-audit is claimed. The local_band_no_go README and selected
SURGERY records were inspected late; its previously proved all-r formula was
initially rediscovered here and has been relabeled as reproduction. The 0110
polynomial was then independently rechecked. PLAN_CE and the two newer closure
notes/scripts were read after the concurrent fast-forward.

/tmp/claude-0 is absent on this Mac. The upstream 91732d4 recovery includes
hashed compressed raw data; we read its reconciliation report and preserved
those files without alteration. Its recorded process statuses are historical,
not a claim that the remote process is still running. AUDIT.md and the
preparation package's audit_regressions.py remain absent, so its stated 16
tests were **not** run. We did not recreate fake substitutes or repeat the
59,937-knot census. The known broken census scripts were not reused.

## Remaining implication and next action

A physical band design still needs its boundary classes, actual marked collar,
embedded compression/annulus, standard ambient B4, and target identity.
The new algebra tells us what a redesign must change; it does not provide it.
Derive the actual collar and a joint connector with the required module
collapse and a specified geometric cancellation, instead of enumerating longer
pure-meridian or second-band paths. A different construction is not excluded.
