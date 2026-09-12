# Two new results (2026-09-11, session 2 continued)

## A. The Floer torsion order gives no lower bound on the fusion number of K_G

**Setup.** Juhasz-Miller-Zemke (arXiv:1904.02735) prove that for a ribbon knot J,
the fusion number satisfies F(J) >= Ord_U(J), the maximal U-torsion order of
HFK^-(J). A large torsion order would prove that any ribbon disk for a knot needs
many bands, explaining Dunfield-Gong's <=4-band search failure and telling us how
deep to search. This computation had never been run on K_G.

**Computation.** SnapPy returns CFK_{UV=0} for K_G with 25 generators and 28
arrows. Using Zemke's gradings (gr_U = M, gr_V = M - 2A; U has bidegree (-2,0),
V has (0,-2); the differential drops both by 1), an arrow a -> b carries U^i V^j
with

    i = (M_b - M_a + 1)/2,    j = i + (A_a - A_b),    and  i = 0 or j = 0.

Running this on K_G: **every generator satisfies M = A** (the complex is delta-thin),
and the exponents are U_exponents = [1], V_exponents = [1]: 14 U-arrows and 14
V-arrows, all of exponent exactly 1.

**Consequence (rigorous, no Smith normal form needed).** Setting V = 0 leaves a
complex over F_2[U] whose differential matrix D has every nonzero entry equal to U.
So D = U*B with B a matrix over F_2. Smith normal form commutes with the scalar:
SNF(U*B) = U*SNF(B) = diag(U,...,U,0,...,0). Every elementary divisor is U^1, so
all torsion in HFK^-(K_G) is U^1-torsion and

    Ord_U(K_G) = 1,  hence the JMZ bound gives only F(K_G) >= 1.

(This is the expected behaviour of a delta-thin knot; the point is that K_G *is*
thin, which had not been recorded.)

**Why this matters, and it cuts against us.** The adversarial memo's strongest
steelman for "K_G is ribbon but nobody found the disk" was that a genus-5 knot
plausibly needs a 5-band disk, one past DG's search ceiling of 4. Heegaard Floer
homology supplies **no support** for that: there is no obstruction to K_G having a
ribbon disk with very few bands. So DG's failure at <=4 bands, and our own failure
across 61 shaken diagrams at 2 and 3 bands, is somewhat *more* meaningful than the
memo credited - though still only a coverage statement, since no upper bound on
fusion number exists either.

**Calibration.** K_B, the ribbon 0-friend, has exponents [1,5], but its ribbon
certificate is a single band to the unlink, so F(K_B) = 1 and JMZ gives
Ord_U(K_B) <= 1. The raw maximum exponent is therefore *not* the torsion order in
general - only the all-exponents-1 case above licenses the conclusion. The GST
Figure 2 knot has U-exponents [1,2,3,4,6] and is not thin; its torsion order needs
a genuine Smith normal form over F_2[U] and is left open here.

Script: `scripts/torsion_order.py`.

## B. GHMR's three r = 0 RBG pairs are only two distinct pairs, and one is already inside the Dunfield-Gong census

Gukov-Halverson-Manolescu-Ruehle section 6 flag three r = 0 pairs as potential
slice-ribbon counterexamples:

    K_{B/G}(0,0,0,1,2,-1),   K_{B/G}(0,0,0,-1,2,1),   K_{B/G}(0,0,-2,0,0,1).

**Finding 1 (duplicate).** The first and third are the **same pair**. After
simplification both sides have identical isometry signatures:

| knot | isometry signature (truncated) |
|---|---|
| K_B(0,0,0,1,2,-1)  | `rvLLvvALQQQQceghmqjmolopnpopnqqsmgcmwvxc` |
| K_B(0,0,-2,0,0,1)  | `rvLLvvALQQQQceghmqjmolopnpopnqqsmgcmwvxc` |
| K_G(0,0,0,1,2,-1)  | `pvLLLvMQMQQegghjklmnjmnlooogmmwfgooengtr` |
| K_G(0,0,-2,0,0,1)  | `pvLLLvMQMQQegghjklmnjmnlooogmmwfgooengtr` |

`is_isometric_to` returns True for both matched pairs. So lane 2 contains **four
distinct knots, not six**.

**Finding 2 (already censused).** That pair simplifies to **19 crossings, prime,
hyperbolic** (volumes 13.824520 and 13.990717). Dunfield-Gong's census covers
*all* prime knots with at most 19 crossings and searched them for ribbon disks to
4 bands using roughly 100 CPU-years. Any band search we run on these two knots is
therefore strictly weaker than one already performed. Conversely this makes them
*better* candidates than recorded: they have survived a far more thorough search
than anything in this campaign.

**Finding 3 (where the compute should go).** The other pair, K_B(0,0,0,-1,2,1) at
27 crossings and K_G(0,0,0,-1,2,1) at 24 crossings, both prime and hyperbolic,
lies **outside** DG's <=19-crossing census and has never been subjected to the DG
band search. The ribbon-search queue was redirected onto it.

All four r = 0 knots have Alexander polynomial 1, hence are topologically slice by
Freedman, with tau = epsilon = nu = signature = 0 and genus 2. Within each pair the
two knots have diffeomorphic traces, so identical smooth slice status in the
standard B^4: a ribbon disk for either certifies the other slice with no inherited
ribbon disk.
