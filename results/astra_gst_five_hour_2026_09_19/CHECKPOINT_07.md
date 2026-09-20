# Checkpoint7 — exact(2,2) tests and a concrete(3,3) local criterion

2026-09-20 02:25UTC. No counterexample. Usage15% at start,16% at finish; original baseline7%, amended14additionalpoints, stopwithbuffer20%, deadline04:41:43UTC. All local jobs completed. Local3e4461e and remote2a07128 unchanged; our earlier research02citationcorrection remains the only tracked edit. No paused remote search restarted.

## Exact(2,2) test completed for n1 and n2

Write delta=v+v^-1, epsilon=v^3+v^-3, a=delta+epsilon, b=delta*epsilon, q=v^2. Expanding the two reduced-colour numerators gives

N22 = J(AABB) - a[J(AAB)+J(ABB)] + b[J(AA)+J(BB)] + a^2 J(AB) - ab[J(A)+J(B)] + b^2.

The reduced invariant is v^4*N22/[(q-1)^2(q^2-1)^2]. Habiro guarantees divisibility byH2; Suzuki addsI2=(q-1)^2. The denominator has order4 atq=1, H2 order2, and I2 order2. Therefore the extra ideal condition is exactly N22 having order>=8 atv=1, using the same integral factor-theorem argument as checkpoint6. No full four-component polynomial is needed.

`suzuki_double_colour.py` cables both braid components with explicit separate self-writhe corrections. All resulting four-component links have linking matrix zero. It reuses the saved smaller exact traces and computes only the new four-parallel trace in Z[x]/x^8, v=1+x. Seeded four-round all-starts Morse layouts, saved events and20000-state cap are retained. Small new cable traces are independently checked using full Regina polynomials.

| input | simplified cable crossings | coefficients of N22 throughdegree7 | result |
|---|---:|---|---|
| split trefoil–unknot |18|all0|pass|
| ribbonL10n36 |40|all0|pass|
| L10n57 |45|[0,0,0,0,0,0,245760,0]|obstructed|
| L14n38935 |68|[0,0,0,0,0,0,245760,-1597440]|obstructed|
| provisionalGSTn1 |72|all0|pass|
| provisionalGSTn2 |152|all0|pass|

Every Habiro baseline check passes. The two nonribbon controls were already known nonslice; neither is a new counterexample. GSTn2 completed within its45second bound (about15.5seconds including setup). Exact inputs, braids, framings, polynomial/Taylor data and results are under `suzuki_double/`; batch statuses in `SUZUKI_DOUBLE_BATCH_STATUS.json`. GSTn3(2,2) has NOT been calculated: its smaller traces need order8 data and the new four-parallel may be substantially wider. Do not mark that case closed.

## Design of the first additional q=-1 condition

`derive_suzuki_33.py` symbolically verifies the coefficients and cyclotomic orders; `SUZUKI_33_DESIGN.json` contains all16 terms and the precision each needs.

Let p3(X)=product_{j=0}^2 [X-(v^(2j+1)+v^(-2j-1))] = sum_{a=0}^3 c_a(v)X^a. Define N33=sum_{a,b=0}^3 c_a c_b J(A^a B^b), where powers mean zero-framed parallel components, power0 means deletion and J(empty)=1. The reduced invariant is v^6*N33/({3}_q!)^2.

At q=-1, equivalently Phi2(q)=v^2+1=0, the denominator has order2, Habiro's H3={7}{6}{5}{4}/{1} has order2, and Suzuki's I3=(q-1)^3(q+1) adds one. Therefore the local ribbon condition is **N33 divisible by(v^2+1)^5**. This tests only the q=-1 part of the full ideal condition; the q=1 part remains separate.

Each c_a has(v^2+1)-order3-a. Hence terms with a+b<=1 disappear at this precision; other terms need only the precision listed in the saved JSON. No extra Jones-nullity theorem for slice cables has been assumed. A modular implementation can use v=10+x in F101[x]/x^5, since10^2=-1 mod101. A nonzero remainder obstructs integral divisibility; zero modulo101 is inconclusive. The numerator has even v-parity, so the two roots are related by v->-v, but test both during calibration if helpful.

Next implementation should support variable component multiplicities0..3 in a braid, with separate zero-framing corrections. For a p-strand selected bundle, compensate its original braid self-writhe w by the braid cycle(sigma1...sigma_{p-1}) repeated-p*w times with the corresponding sign. This is a proposed extension to calibrate, not implemented/verified here. Compare knot-only outputs to existing cable_braid, check all pairwise linking numbers, and test boundary/ribbon controls before GST. Keep the state cap and save exact inputs; do not launch a blind six-parallel full polynomial.

## Milnor-source audit and its limit

Jean-Baptiste Meilhan and Sakie Suzuki, *The universal sl2 invariant and Milnor invariants*, arXiv1405.3062v2 (2016-10-06), https://arxiv.org/pdf/1405.3062. Theorem5.2 relates a projected universal invariant J^t to Milnor data; Corollary5.4 gives the projected concordance statement. Corollary7.6 bounds PBW degree by h-order for string links with vanishing Milnor invariants. The source PDF, hash and precise scope are saved in `sources/CHECKPOINT_07_SOURCE.json`.

We have NOT shown that our closed-link reduced-colour Taylor functional factors through the stated projection, nor handled all basing/closure choices needed to apply it. Thus these results do not yet justify declaring the q=1 tests automatic for all slice links. The stronger general divisibility statement remains a conjectural extension in the cited discussion. This is a promising redundancy audit, not a lane closure.

Suzuki's verified ribbon/boundary ideal theorem and principal generators remain as recorded in checkpoint6 (arXiv1111.6408, Theorems2.2/3.1). Boundary-link controls necessarily pass these conditions even without ribbon companions. This does not establish GST as a boundary link or close general ribbon-preserving satellite patterns.

## Remaining priorities

Calibrate the bounded(3,3),q=-1 computation on small controls, then estimate GST resource needs. Alternatively finish n3(2,2) through order8 with the existing optimized layouts, or return to literal GST dotted-band transport. Success still requires a smooth disk in standardB4 and global nonribbonness for the same precisely identified knot. No such proof has been found.
