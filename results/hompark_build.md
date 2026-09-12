# Building the Hom-Park knot, and a construction error caught by its own check
2026-09-12

## The object

Hom-Park (arXiv:2507.20455) Corollary 1.3 gives explicit knots that are
**algebraically slice and provably not ribbon**:

    P(K,J,p,q1,q2) = K_{p,q1} # -K_{p,q2} # J_{p,q2} # -J_{p,q1}

smallest named instance K = T(2,3), J = T(2,5), p = 2, q1 = 1, q2 = 3. This campaign
has carried that lane since Session 0 without ever building the knot.

## The error, and how it surfaced

The first build used `snappy.Link('3_1')` and `snappy.Link('5_1')` as T(2,3) and
T(2,5). Every cabled piece came back with **epsilon = -1** and negative tau. Those
census entries are the **left-handed** trefoil and (2,5) torus knot, so the
construction had cabled the mirrors. Cabling a mirror is not the mirror of a cable:
mirror(K)_{p,q} = mirror(K_{p,-q}), so the result was neither Hom-Park's knot nor its
mirror, but a different four-term cable sum. The global tau still summed to zero,
which is exactly why a weaker check would have passed it through.

Fixed by building the torus knots as explicit braids, the closure of sigma_1^n on two
strands, which is right-handed for n > 0 and leaves no ambiguity. Verified:
T(2,3) has tau = 1, epsilon = +1; T(2,5) has tau = 2, epsilon = +1.

## Verification of the corrected build

Against the Hedden-Hom cabling formula tau(K_{p,q}) = p*tau(K) + (p-1)(q-1)/2, valid
when epsilon(K) = +1:

| piece | crossings | genus | tau | predicted | |
|---|---|---|---|---|---|
| K_{2,1} | 17 | 2 | 2 | 2 | OK |
| K_{2,3} | 15 | 3 | 3 | 3 | OK |
| J_{2,3} | 27 | 5 | 5 | 5 | OK |
| J_{2,1} | 29 | 4 | 4 | 4 | OK |

**Every piece matches on the nose.** The connected sum P has **88 crossings**,
signature 0, and

    tau(P) = 2 - 3 + 5 - 4 = 0,

so tau gives no obstruction, exactly as Hom-Park's design requires: they chose the
parameters to make P algebraically slice.

Saved as `data/knots/HomPark_P_corrected.json`. The earlier mirrored build is kept as
`data/knots/HomPark_P.json`, labelled, rather than deleted.

## Why it is worth having

P is a **second route-B object with a proved non-ribbon certificate and open
sliceness**, reached through entirely different machinery from the Miyazaki sums: the
certificate comes from Hom-Park's gamma_0-sharp pairing theorem rather than
Miyazaki's fibered pairing. If it survives Casson-Gordon it joins the Abe-Tagami sums
on the live board, and the two lanes fail independently, which is worth more than two
correlated candidates.

Casson-Gordon is running on the corrected knot.

## Tooling note

`scripts/cable.py` implements Seifert-framed cabling: the blackboard p-parallel of a
braid closure has framing equal to the writhe, so the cable needs q - p*w corrective
half twists. Calibrated by reproducing genus = p * genus on 3_1, 4_1 and 10_17, by
independently rebuilding (10_17)_{2,1} at 41 crossings to match the earlier
construction, and now by matching the Hedden-Hom tau formula on four cables of torus
knots.
