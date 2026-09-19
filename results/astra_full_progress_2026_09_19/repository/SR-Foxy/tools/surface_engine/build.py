"""
build.py -- Turaev's surface A(p,q,r,s) as a disk with 6 flat bands, and
Milnor's ribbon-linking move (Turaev's Figure 4).

    import build, bands, milnor
    c = build.build(p, q, r, s)      # the surface, as a braid word on 12 strands
    L = bands.boundary_link(c)       # the boundary knot, a spherogram.Link
    L.simplify('global')
    pd = L.PD_code(KnotTheory=False)

    c.linking_matrix()               # the Seifert data actually realized
    milnor.mu(c, 1, 3, 5)['mu']      # == r
    milnor.mu(c, 2, 4, 6)['mu']      # == s

Self-test: `python3 build.py`.  See bands.py for the surface model, the braid
letter convention, and why clasps and travels are the only two moves needed.

WHAT IS BEING REALIZED
----------------------
Turaev, Math. USSR-Sb. 44:3 (1983) 335-361, Section 1.5 and p. 341-342: a
genus-3 surface A(p,q,r,s) in S^3 with, in the Figure-3 generators x_1..x_6,

         | 0   1    0   1   0   0 |
         | 0   0    p   0   0   0 |
    X =  | 0   p    0   q   0   1 |     l_2(x_1,x_3,x_5) = r
         | 1   0   q-1  0   p   0 |     l_2(x_2,x_4,x_6) = s
         | 0   0    0   p   0   0 |
         | 0   0    1   0  -1   0 |

alt(X) = X - X^T is the standard symplectic form pairing (1,2),(3,4),(5,6), so
the handles are {1,2}, {3,4}, {5,6} and the foot layout must interleave exactly
those pairs:

    FEET = [1, 2, 1, 2, 3, 4, 3, 4, 5, 6, 5, 6]

Every diagonal entry of X is 0, so no band carries a self-twist and all six
bands are flat.  The rest of X splits into two kinds of data, each realized by
clasps:

    within-handle   X_12+X_21 = 1       handle crossing + 1 clasp
                    X_34+X_43 = 2q-1    handle crossing + q clasps
                    X_56+X_65 = -1      handle crossing, no clasp
    cross-handle    lk(x_1,x_4) = 1     1 clasp
                    lk(x_2,x_3) = p     p clasps
                    lk(x_3,x_6) = 1     1 clasp
                    lk(x_4,x_5) = p     p clasps
                    every other lk = 0  no clasps

(The "handle crossing" is the single letter that un-interleaves a handle's two
feet so the band can be capped; it is forced by the layout, and by the
calibration in bands.py an 'L' handle crossing alone gives sum -1, each further
'L' clasp adding +2.)  Note lk(x_1,x_3) = lk(x_1,x_5) = lk(x_3,x_5) = 0 and the
same for (2,4,6): both triples are algebraically split, which is exactly what
makes their Milnor triple linking numbers well-defined integers.

THE FIGURE-4 MOVE (`fig4`)
--------------------------
Turaev p. 339: "the ribbon-linking operator illustrated in Figure 4 changes
l_2(x_i0, x_j0, x_k0) by 1 and leaves unchanged the numbers l_2(x_i,x_j,x_k)
for all other i<j<k (see [8])", [8] being Milnor.  Reading the picture (see
REPORT.md Section 3 for the crossing-by-crossing transcription and which
crossings were and were not resolved at 6000 dpi): the i0 band is band-summed
with the commutator of the meridians of the j0 and k0 bands, the Borromean
move.  Along the modified i0 arc the word in pi_1 of the complement of the
other two bands reads a b a^-1 b^-1.

Here that is built out of clasps and travels only.  A clasp IS a meridian (the
strand goes out past the other band and returns the far side), so

    travel to j0, clasp(+), travel to k0, clasp(+),
    travel back to j0, clasp(-), travel to k0, clasp(-), travel home

realizes w (a B a^-1 B^-1) w^-1 with B a conjugate of the k0 meridian: a
commutator of two meridians.  Every travel is undone crossing-for-crossing with
the opposite sign and every clasp is paired with its inverse, so no linking
number and no self-writhe changes -- X is untouched, which is the whole point.
Doing the two wraps in the other order gives the inverse commutator, hence the
opposite sign of the invariant; `sign` selects between them.

SIGN CONVENTION.  Turaev's own sign for the move is not determined by the
paper.  The sign in `build` is fixed so that the ARGUMENT EQUALS THE MEASURED
INVARIANT: build(p,q,r,s) satisfies milnor.mu(c,1,3,5)['mu'] == r and
milnor.mu(c,2,4,6)['mu'] == s, on the nose, for r,s of either sign and |r|,|s|
greater than 1 as well.  This is checked by the self-test.

COST.  Each fig4 call costs 26 core crossings in this layout (the i0 band has
to travel four strands to reach the far band, four times), which is what makes
the r,s != 0 diagrams ~300 crossings raw and ~130 simplified.  A nested foot
layout would cut this to about 18; see bands.py and REPORT.md Section 6.
"""
import bands

FEET = [1, 2, 1, 2, 3, 4, 3, 4, 5, 6, 5, 6]
# foot positions (1-indexed): band m start = FEET.index(m)+1, end = second occurrence
START = {m: FEET.index(m) + 1 for m in range(1, 7)}
END = {m: len(FEET) - FEET[::-1].index(m) for m in range(1, 7)}

FLIP = {'L': 'R', 'R': 'L'}


def fig4(c, i0, j0, k0, sign):
    """Milnor ribbon-linking (Turaev Fig. 4) on the triple (i0,j0,k0):
    band i0's core is band-summed with the commutator [m_{j0}, m_{k0}] of
    meridians.  sign=+1 gives [a,b], sign=-1 gives [b,a]=[a,b]^{-1}."""
    home = END[i0]                       # the downward strand of band i0
    pj = START[j0]                       # the strand of band j0 we wrap
    pk = START[k0]
    assert home < pj < pk
    aj, ak = pj - 1, pk - 1              # parking positions next to j0 / k0
    fa, fb = ('R', 'R') if sign > 0 else ('L', 'L')
    c.travel(home, aj)
    if sign > 0:
        seq = [(aj, fa), (ak, fb), (aj, FLIP[fa]), (ak, FLIP[fb])]
    else:
        seq = [(ak, fb), (aj, fa), (ak, FLIP[fb]), (aj, FLIP[fa])]
    cur = aj
    for (tgt, fl) in seq:
        if tgt > cur:
            c.travel(cur, tgt)
        elif tgt < cur:
            c.travel_back(tgt, cur)
        cur = tgt
        c.clasp(cur, fl)
    if cur > aj:
        c.travel_back(aj, cur)
    c.travel_back(home, aj)


def build(p, q, r=0, s=0):
    c = bands.Core(FEET)
    # ---- cross-handle clasps (linking numbers) -------------------------
    c.clasp_between(2, -1, 3, +1, 'R')            # lk(x2,x3) += 1, p times
    for _ in range(p - 1):
        c.clasp(END[2], 'R')
    c.clasp_between(4, -1, 5, +1, 'R')            # lk(x4,x5) += 1, p times
    for _ in range(p - 1):
        c.clasp(END[4], 'R')
    c.clasp_between(1, -1, 4, +1, 'R')            # lk(x1,x4) = 1
    c.clasp_between(3, -1, 6, +1, 'R')            # lk(x3,x6) = 1
    # ---- within-handle clasps ------------------------------------------
    c.clasp(START[1], 'L', 1)                     # handle 1: sum -1 -> +1
    c.clasp(START[3], 'L', q)                     # handle 2: sum -1 -> 2q-1
    #                                              handle 3: sum -1, no clasp
    # ---- Milnor moves ---------------------------------------------------
    # sign chosen so that the realized mu-bar(x1,x3,x5) = r and mu-bar(x2,x4,x6) = s
    for _ in range(abs(r)):
        fig4(c, 1, 3, 5, -1 if r > 0 else 1)
    for _ in range(abs(s)):
        fig4(c, 2, 4, 6, -1 if s > 0 else 1)
    # ---- handle crossings ------------------------------------------------
    for k in range(3):
        c.add(4 * k + 2, 'L')
    return c


def realized_V(c):
    """The Seifert matrix entries this core actually realizes."""
    L = c.linking_matrix()
    return L


# --------------------------------------------------------------- self-test
def _selftest():
    """Run with `python3 build.py`.  Checks that build() realizes X exactly and
    that the Figure-4 move installs r and s and changes nothing else."""
    import milnor
    ok = True
    for (p, q) in [(1, 1), (1, 3), (2, 1), (3, 1)]:
        want = {(1, 4): 1, (2, 3): p, (3, 6): 1, (4, 5): p,
                (1, 2): 1, (3, 4): 2 * q - 1, (5, 6): -1}
        base = None
        for (r, s) in [(0, 0), (1, 1), (1, -1), (-1, 1), (-1, -1), (2, 0), (0, 3)]:
            c = build(p, q, r, s)
            L = c.linking_matrix()
            got = {}
            for i in range(1, 7):
                for j in range(i, 7):
                    v = L[(i, j)]
                    v = v[1] if isinstance(v, tuple) else v
                    if v:
                        got[(i, j)] = v
            diag = [L[(i, i)] for i in range(1, 7)]
            good = (got == want) and (diag == [0] * 6)
            m135 = milnor.mu(c, 1, 3, 5)['mu']
            m246 = milnor.mu(c, 2, 4, 6)['mu']
            good &= (m135 == r and m246 == s)
            if base is None:
                base = got
            else:
                good &= (got == base)           # fig4 must not disturb X
            ok &= good
            print('p=%d q=%d r=%-2d s=%-2d : X realized %-5s  mu135=%-2d mu246=%-2d '
                  'writhes %s  %d core crossings  %s'
                  % (p, q, r, s, got == want, m135, m246,
                     'all 0' if diag == [0] * 6 else diag, len(c.word),
                     'OK' if good else 'FAIL'))
    print('\n%s' % ('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED'))
    return ok


if __name__ == '__main__':
    import sys
    sys.exit(0 if _selftest() else 1)
