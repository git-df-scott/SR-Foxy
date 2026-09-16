#!/usr/bin/env python3
"""Which Turaev Theorem I members are STRUCTURALLY IMMUNE to Casson-Gordon / HKL?

Motivation.  `results/turaev_family_status.md` records that A(1,1,1,1), the only
realised Theorem I member, was killed by `slice_obstruction_HKL` returning
(3, 13): a character of order 13 on the 3-FOLD branched cover.  That file also
records a wrong prediction -- that the q=1 subfamily is immune because
det = (2q-1)^2 = 1 kills the Sigma_2 test -- and notes the lesson: immunity at
Sigma_2 says nothing about Sigma_n for n > 2.

This script does the calculation that would have caught it, over the whole grid.

The arithmetic.  For the Turaev family,
    Delta_K(t) = t^3 rho(t) rho(1/t),   rho(t) = p t^3 - (p+q) t^2 - (p-q+1) t + p
and |H_1(Sigma_n(K))| = prod_{j=1}^{n-1} |Delta(zeta_n^j)|.  On the unit circle
rho(1/zeta) = conj(rho(zeta)) since rho has real coefficients, so
    |Delta(zeta_n^j)| = |rho(zeta_n^j)|^2
and therefore
    |H_1(Sigma_n)| = R_n^2,   R_n = |prod_{j=1}^{n-1} rho(zeta_n^j)|
                                  = |Res(rho(t), 1 + t + ... + t^(n-1))|.
So the homology of every branched cover is a perfect square, and R_n is the
quantity that decides whether characters exist at all.

Casson-Gordon and HKL run over nontrivial characters on H_1(Sigma_n).  If
R_n = 1 then H_1(Sigma_n) is trivial, there are no characters, and the test is
VACUOUS at that n -- it cannot fire no matter how the knot is built, because it
depends only on (p,q).  R_n is independent of r and s, which are l_2 data and do
not appear in the Seifert matrix.

A member with R_n = 1 for every small n is the one to build next: it is immune to
the exact machinery that killed A(1,1,1,1).  That is NOT evidence it is slice.
It only means the standard killer has nothing to fire with, so the member would
have to be settled by something else.

Controls: R_2 must equal |2q-1| (so det = (2q-1)^2, matching the stored data), and
(p,q) = (1,1) must give R_3 = 13, reproducing the HKL_agent that killed A(1,1,1,1).
If either control misses, every row below is void.
"""
import sympy
from sympy import symbols, Poly, ZZ, resultant, primerange

t = symbols('t')

def rho(p, q):
    return Poly([p, -(p + q), -(p - q + 1), p], t, domain=ZZ)

def R(p, q, n):
    """|Res(rho, 1 + t + ... + t^(n-1))| = |prod_{j=1}^{n-1} rho(zeta_n^j)|."""
    cyc = Poly([1] * n, t, domain=ZZ)          # 1 + t + ... + t^(n-1)
    return abs(int(resultant(rho(p, q).as_expr(), cyc.as_expr(), t)))

COVERS = [2, 3, 5, 7, 11, 13]


def R3_closed(p, q):
    """Closed form for R_3, proved in research/30 and checked against R() below.

    omega^3 = 1 and 1 + omega + omega^2 = 0 give
        rho(omega) = 2p - (p+q)omega^2 - (p-q+1)omega = A + B*omega,
        A = 3p + q,   B = 2q - 1,
    so R_3 = |rho(omega)|^2 = A^2 - A*B + B^2 = 9p^2 + 3p + 3q^2 - 3q + 1.

    A^2 - A*B + B^2 is the Eisenstein norm form, which takes the value 1 only at
    (A,B) in {(1,0),(0,1),(1,1)} up to sign.  An admissible Theorem I member has
    p >= 1 and q >= 1, hence A = 3p+q >= 4, so **R_3 = 1 is impossible** and
    |H_1(Sigma_3)| = R_3^2 >= 169 for every member of the family.
    """
    return 9 * p * p + 3 * p + 3 * q * q - 3 * q + 1

def main():
    print(__doc__.split('Controls:')[0].strip()[:0] or '', end='')
    print('Turaev Theorem I: |H_1(Sigma_n)| = R_n^2.  R_n = 1 <=> that cover has')
    print('trivial homology <=> Casson-Gordon / HKL is VACUOUS at that n.')
    print()
    # ---- controls -------------------------------------------------------
    ok = True
    for q in range(1, 6):
        for p in [1, 2, 3, 5]:
            if p == 2 and q == 2:
                continue
            if R(p, q, 2) != abs(2 * q - 1):
                print('CONTROL FAILED: R_2(%d,%d) = %d, expected |2q-1| = %d'
                      % (p, q, R(p, q, 2), abs(2 * q - 1)))
                ok = False
    for pv in [1, 2, 3, 5, 7, 11, 13]:
        for qv in range(1, 12):
            if pv == 2 and qv == 2:
                continue
            if R(pv, qv, 3) != R3_closed(pv, qv):
                print('CONTROL FAILED: closed form for R_3 wrong at (%d,%d)' % (pv, qv))
                ok = False
    r3_11 = R(1, 1, 3)
    print('control  R_2 == |2q-1| and R_3 closed form over the grid :', ok)
    print('control  R_3(p=1,q=1) == 13          :', r3_11 == 13, '(got %d)' % r3_11,
          '  <- the HKL_agent (3,13) that killed A(1,1,1,1)')
    if not ok or r3_11 != 13:
        raise SystemExit('controls failed; table below would be void')
    print()
    # ---- the grid -------------------------------------------------------
    hdr = '%-4s %-4s' % ('p', 'q') + ''.join('%8s' % ('R_%d' % n) for n in COVERS) + '   vacuous at'
    print(hdr); print('-' * len(hdr))
    winners = []
    for p in [1] + list(primerange(2, 14)):
        for q in range(1, 9):
            if p == 2 and q == 2:
                continue
            rs = [R(p, q, n) for n in COVERS]
            vac = [n for n, v in zip(COVERS, rs) if v == 1]
            print('%-4d %-4d' % (p, q) + ''.join('%8d' % v for v in rs)
                  + '   ' + (','.join(map(str, vac)) if vac else '-'))
            if len(vac) == len(COVERS):
                winners.append((p, q))
    print()
    print('THEOREM (research/30).  R_3 = A^2 - AB + B^2 with A = 3p+q, B = 2q-1, the')
    print('Eisenstein norm form.  It equals 1 only at (A,B) = (1,0),(0,1),(1,1) up to')
    print('sign; an admissible member has A = 3p+q >= 4.  So R_3 = 1 is IMPOSSIBLE and')
    print('|H_1(Sigma_3)| = R_3^2 >= 169 for EVERY Theorem I member.  The 3-fold cover')
    print('always carries characters, so Casson-Gordon / HKL always has ammunition and')
    print('no member of the family is structurally immune.  The minimum, R_3 = 13, is')
    print('attained at (p,q) = (1,1) -- which is exactly the member that was built and')
    print('killed by HKL_agent (3,13).')
    print()
    if winners:
        print('MEMBERS WITH EVERY TESTED COVER TRIVIAL (Casson-Gordon/HKL has no character):')
        for p, q in winners:
            print('   (p,q) = (%d,%d)  -> build A(%d,%d,r,s) with r,s both nonzero' % (p, q, p, q))
    else:
        print('No member has all of', COVERS, 'trivial.')
    print()
    print('Reminder: R_n depends only on (p,q), never on r,s.  A row of 1s means the')
    print('standard killer is structurally unable to fire -- it is NOT evidence of')
    print('sliceness, and such a member still has to be built and tested by other means.')

if __name__ == '__main__':
    main()
