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

## Result: it survives Casson-Gordon

| character spec | result | time |
|---|---|---|
| [(3,[0,6])] | None | 0.2s |
| [(5,[0,8])] | None | 0.3s |
| [(7,[0,10])] | None | 0.8s |
| [(11,[0,12])] | **None** | 26.8s |

No obstruction fires. (The full [(10,[0,20]),(20,[0,10])] spec exceeded a 10-minute
budget at 88 crossings, so coverage stops at prime 11; that is a compute limit, not a
result.)

**So the Hom-Park knot joins the live board as a third route-B candidate:**

| | status |
|---|---|
| non-ribbon | **PROVED**, Hom-Park Cor. 1.3 |
| tau, signature | 0, 0 |
| Casson-Gordon | no obstruction up to prime 11 |
| smooth sliceness | **OPEN** |

Its value is independence. The Abe-Tagami sums get their non-ribbon certificate from
Miyazaki's fibered pairing theorem; this one gets it from Hom-Park's gamma_0-sharp
pairing theorem, via cables of torus knots rather than annulus twists. The two lanes
share no machinery, so they cannot die to the same cause.

What makes it slice, if it is: P is slice exactly when

    [K_{2,1}] - [K_{2,3}] + [J_{2,3}] - [J_{2,1}] = 0

in the smooth concordance group, i.e. when that four-term relation among cables of
T(2,3) and T(2,5) holds. Hom-Park's Corollary 1.2 states the dichotomy directly:
either distinct iterated cables of tight fibered knots are linearly independent in
concordance, or the Slice-Ribbon Conjecture is false. This knot is that dichotomy
made explicit at its smallest parameters.
