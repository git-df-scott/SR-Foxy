# Additional three-point session: stopped at buffered usage limit

No Slice–Ribbon counterexample. Baseline weekly usage 24%; final displayed usage 26%; absolute allowance ceiling 27%. Stop is intentional to preserve a buffer. No new scheduled wakes authorized. Automation remains paused, as do GitHub run 35455048082 and other explicitly paused searches.

## Most useful surviving lead

D = K9n4 # (-K14n282), with census names and precise PD codes in `SURVIVOR_AUDIT.json` and `EXACT_K9n4_K14n282.json`.

Fresh calculations: both are fibered genus two (HFK over F2 and F3, same implementation), have tau=nu=epsilon=0, and have irreducible Alexander polynomial x^4-2x^3+x^2-2x+1. Regina Jones polynomials differ, proving the recorded knots distinct. These are the computed hypotheses for the Miyazaki/Abe–Tagami irreducible-fibered nonribbonness argument. Primary reference: Tetsuya Abe and Keiji Tagami, *Fibered knots with the same 0-surgery and the slice-ribbon conjecture*, Math. Res. Lett. 23 (2016), 303–323, DOI 10.4310/MRL.2016.v23.n2.a1, https://arxiv.org/abs/1502.01102. Corollary 4.3 is the intended theorem; the primary PDF was located but its exact wording was not re-opened before this usage stop. Keep that final source audit explicit.

The double-cover H1 groups are both Z/7. Reduced twisted polynomials are t^2+A(z)t+1 and t^2+B(z)t+1, with

A(z)=z^5+2z^4+2z^3+z^2+1,
B(z)=z^5-z^4-z^3+z^2.

Exact remainder checks modulo Phi_7 in this session gave A(z^a)=B(z^b) for (a,b)=(1,2),(2,3),(3,1), with a,b represented by 1,2,3 modulo independent signs. These checks were printed during the session; the exact polynomial inputs are saved. Their products are actual norms up to a Laurent unit. All other pairings have finite-field non-norm witnesses in `CERTIFICATE_K9n4_K14n282.json`.

IMPORTANT: this does not certify a metabolizer, vanish all Casson–Gordon invariants, or prove sliceness. The matching ratio is b/a=±2 modulo 7. Next determine whether that ratio is compatible with the linking forms IN THESE COCYCLE COORDINATES. Abstract matching linking forms or a fresh unrelated basis do not settle this. Do not spend more primes trying to disprove an exact polynomial equality.

Then audit further obstructions (full Casson–Gordon data, higher covers, Floer concordance invariants) before a disk search. A smooth concordance between the precisely recorded summands would produce a disk for D; none has been constructed. Standard B4 remains required.

## Completed eliminations

`SMALL_DIFFERENCE_PROOF.md` explains the all-character argument excluding K7a2#(-K10n4), K8a5#(-K12n13), and K11n91#(-K13n16), with exact coefficient files and elementary finite-field witness certificates. Review of the torsion normalization is still valuable; avoid presenting computer deductions as externally certified theorems.

Earlier campaign work remains in `../astra_seven_hour_2026_09_20`: same-sign trefoil cable differences excluded by the earlier argument; 10_17 cable screens inconclusive; GST needs source-certified knot construction and global knot nonribbonness. Do not reopen previously excluded candidates without identifying a specific flaw in the exclusion.

## Reproduction

Python: `/tmp/sr-foxy-20260919-leads-venv/bin/python` with SnapPy, Spherogram, Sympy, Regina and python-flint. Scripts: `audit_small_difference.py`, `elementary_norm_certificate.py`, `exact_pair.py`, `screen_next_pair.py`, `survivor_audit.py`. Exact scripts depend on the prior session's `metabelian_probe.py`; retain that directory. Default exact/screen scripts address q=29; explicit CLI filenames address the q=7 and q=31 pairs. No computations are left running. No push or remote search was started.
