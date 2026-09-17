# Bounded continuation handoff; do not restart current geometry

NO COUNTEREXAMPLE. This pass is local, not pushed. Source main remained
7a74678daccd9f3148b25a22a3f84a82eb1d374b. An additions-only patch is supplied;
do not apply blindly over concurrent work. No new branch.

The original transfer proof's equation (2) is false: L_n(r^n) must be replaced
by L_n((r+1)^n). See MOMENT_CORRECTION.md for the all-degree repair and its
reflection-parity hypothesis. The actual coefficient polynomials in the kernel
argument have that parity, so the leading laws are unchanged by this repair.
The original 4832 checks had not tested that incorrectly printed identity.
The new checker rejects it explicitly. This is not an external peer review;
no further fatal gap was identified in the inspected steps. Do not continue
an endless audit loop without a concrete new mathematical objection.

New D01 gates: exact e2(K0)=e2(K1)=-23; exact e3(K0)=e3(K1)=-1067. Generic
connected-sum identities give e2(D01)=-47 and e3(D01)=-27911. The first was also
computed directly on D01's 112-crossing zero-framed two-parallel. Both modulo32
sliceness necessities pass, and no concordance evidence follows. The n=2,3
sliceness deduction in D01_JONES_GATE.md is standalone and does not require
the amended all-degree theorem. Do not repeat these computations.

The key verification dependency now improved is the marked-group extraction.
A new finder and a separate checker work directly on the original 27-crossing
marked PD, not on the saved a,b relator or SnapPy peripheral words. After
killing the two auxiliary meridians, all 27 Wirtinger relations are verified,
and the two longitude images have traces 1,4 in SL(2,F5). Their orders are 6,3.
Thus the fixed-axis obstruction is independently supported at the PD level.
Read DIRECT_PD_CERTIFICATE.md. The diagram-to-paper correspondence and any
four-dimensional application remain separate obligations.

Continue any substantive nonlocal construction already underway. Otherwise
supply ONE actual changed-axis surgery diagram, not only the words uv/vu:
record band paths, whiskers, component markings, surgery coefficients, and
boundary knot. A new diagram can be tested using the direct coloring method
before expensive annulus/ambient-standardness work. Trace agreement only
removes this particular necessary obstruction; it does not construct an
embedded annulus. The inherited-framing restriction remains conditional on
its stated handle classes and coefficients.

Preserve serial bounded jobs, exact inputs, UNKNOWN on failures, and the
standard-B4 requirement. A proposed counterexample immediately triggers an
independent boundary-knot, disk and nonribbon-proof audit. No current result
supplies either candidate's missing half.
