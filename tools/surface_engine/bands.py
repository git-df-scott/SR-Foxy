"""
bands.py -- realize a Seifert matrix as an explicit disk-with-bands surface and
read off the PD code of its boundary knot.

This is general: nothing here is specific to Turaev's family.  Give it a foot
layout and a braid word and it returns a `spherogram.Link`.

Requires: spherogram (and snappy only if you later want exteriors).
Self-test: `python3 bands.py`.

THE SURFACE MODEL
-----------------
A disk D, drawn as a long horizontal rectangle, with 2g flat bands attached
along its top edge.  Each band meets the disk in exactly two feet, so a genus-g
surface has 2g bands and 4g feet.  For g = 3: 6 bands, 12 feet.  `feet` lists
the band index at each foot, left to right, so `len(feet) = 2 * #bands = n`;
each band index appears exactly twice, its first occurrence being the START
foot and its second the END foot.

Each band is the flat ("blackboard framed") neighbourhood of a core arc.  The
core of band m leaves its START foot going up, runs through a braid region on
`n` strands, and comes back down to its END foot; at the top the two strands of
each band are adjacent and joined by a cap.  Closing through the disk makes the
core a loop x_m, and these loops are the generators of pi_1 of the surface.
Orientation: x_m runs UP the start strand and DOWN the end strand.

WHY THE FOOT LAYOUT IS THE WHOLE OF alt(V)
------------------------------------------
x_i and x_j intersect on the surface iff their feet interleave (a < c < b < d).
So `feet` alone determines the intersection form alt(V) = V - V^T.  For the
standard Figure-3 surface with handles {1,2}, {3,4}, ... take

    feet = [1, 2, 1, 2, 3, 4, 3, 4, 5, 6, 5, 6]

which interleaves exactly the pairs (2k-1, 2k).  A *nested* layout such as
[5,6,3,4,1,2,1,2,3,4,5,6] gives the same alt(V) (cross-handle feet are then
nested rather than disjoint, which is equally non-interleaved) and puts the odd
bands closer together; it needs caps interleaved with braid letters, which
`boundary_link` does not currently support.

BRAID LETTERS, AND THE TWO MOVES THAT ARE ALL YOU NEED
-----------------------------------------------------
A braid letter is `(pos, flag)`, `pos` in 1..n-1, `flag` in {'L','R'}:

    'L' : the strand entering from the lower-LEFT passes OVER
    'R' : the strand entering from the lower-RIGHT passes OVER

With eps = +1 for an upward strand and -1 for a downward one, a crossing has

    sign = s0 * eps_left * eps_right,    s0('L') = +1,  s0('R') = -1.

Everything is built from two composites, and the point of both is that their
effect on the Seifert data is exactly one number and nothing else:

  * CLASP -- the same letter twice, `Core.clasp(pos, flag)`.  The permutation
    cancels, both crossings carry the same sign, so lk of the two bands changes
    by `s0 * eps * eps` and NOTHING else changes.  A clasp is also, read in
    pi_1 of the complement, a single meridian: the strand goes out past the
    other band and comes back the far side.

  * TRAVEL -- `Core.travel(a, b)` moves the strand at position a rightwards to
    b with 'L' letters, `Core.travel_back(a, b)` brings it home with 'R'
    letters.  The moved strand passes OVER on the way out and OVER on the way
    back, so each crossing is undone by an R2 partner of the opposite sign: no
    linking number and no self-writhe changes.  Travels are how a band reaches
    a non-adjacent band; they are free.

Self-twists (diagonal entries of V) would be self-crossings of a core loop.
Turaev's X has zero diagonal, so `build.py` never makes one; `linking_matrix()`
reports the self-writhes so you can check they are 0.

FROM THE SURFACE TO THE BOUNDARY KNOT
-------------------------------------
`boundary_link(core)` doubles everything: 2n strands, a core crossing becomes
the 2x2 block crossing (local braid word sigma_2 sigma_1 sigma_3 sigma_2, all
four elementary crossings carrying the same flag), a core cap becomes two
nested caps, and the boundary of the disk closes the bottom with the
non-crossing cup pattern (1,2n),(2,3),(4,5),...,(2n-2,2n-1).

The Morse diagram is assembled into `spherogram.Crossing` objects.  Slot
convention used: slots 0,1,2,3 run counter-clockwise and the under-strand is
0-2, which pins down the local geometry WITHOUT needing an orientation --
spherogram orients the components itself afterwards.  Arcs are tracked with a
union-find over crossing half-edges; every class must end up with exactly two
half-edges, which is asserted.

VERIFYING WHAT YOU BUILT
------------------------
`Core.linking_matrix()` replays the braid word and returns, from crossing signs
alone (no knot theory):

  * lk(x_i, x_j) for every pair whose feet do NOT interleave -- these are
    honest linking numbers and are the cross-handle entries of V;
  * ('sum', V_ij + V_ji) for every interleaved pair -- lk is undefined there,
    but the sum is what the diagram determines, and V_ij - V_ji = +-1 is forced
    by the layout, so the sum pins the handle block down;
  * the self-writhe of each core on the diagonal.

Calibration note (measured, `python3 bands.py`): a lone handle with one 'L'
letter has V_12 + V_21 = -1; each additional 'L' clasp on that handle adds +2.
"""
import spherogram
from spherogram.links.links import Crossing, Link


# ----------------------------------------------------------------- core tangle
class Core:
    def __init__(self, feet):
        self.feet = list(feet)                 # feet[i] = band at position i+1
        self.n = len(feet)
        seen = {}
        self.ident = []                        # (band, eps) per position, bottom
        for b in feet:
            if b in seen:
                self.ident.append((b, -1))     # end foot: strand runs downward
            else:
                seen[b] = 1
                self.ident.append((b, +1))     # start foot: upward
        self.state = list(self.ident)          # evolves as letters are appended
        self.word = []                         # list of (pos, flag)

    def add(self, pos, flag):
        assert 1 <= pos <= self.n - 1, pos
        self.word.append((pos, flag))
        s = self.state
        s[pos - 1], s[pos] = s[pos], s[pos - 1]

    def pos_of(self, band, eps):
        for i, v in enumerate(self.state):
            if v == (band, eps):
                return i + 1
        raise KeyError((band, eps))

    # ---- building blocks -------------------------------------------------
    def clasp(self, pos, flag, times=1):
        """`times` clasps at position pos (flag repeated 2*times)."""
        for _ in range(times):
            self.add(pos, flag)
            self.add(pos, flag)

    def travel(self, a, b):
        """Move the strand at position a to position b (b>=a), always passing
        OVER the strands it crosses.  Returns the list of positions used."""
        assert b >= a
        for m in range(a, b):
            self.add(m, 'L')
        return list(range(a, b))

    def travel_back(self, a, b):
        """Inverse of travel(a,b): move the strand at b back to a, again over."""
        for m in range(b - 1, a - 1, -1):
            self.add(m, 'R')

    def clasp_between(self, band_i, eps_i, band_j, eps_j, flag):
        """One clasp between the given strand of band_i and the given strand of
        band_j, with band_i's strand travelling (over everything) to reach it.
        Assumes pos_i < pos_j."""
        a = self.pos_of(band_i, eps_i)
        b = self.pos_of(band_j, eps_j)
        assert a < b, (a, b)
        self.travel(a, b - 1)
        self.clasp(b - 1, flag)
        self.travel_back(a, b - 1)

    # ---- verification ----------------------------------------------------
    def crossing_data(self):
        """Replay the word, returning for each letter (band_l,eps_l,band_r,eps_r,sign)."""
        st = list(self.ident)
        out = []
        for (pos, flag) in self.word:
            (bl, el), (br, er) = st[pos - 1], st[pos]
            s0 = 1 if flag == 'L' else -1
            out.append((bl, el, br, er, s0 * el * er))
            st[pos - 1], st[pos] = st[pos], st[pos - 1]
        return out

    def linking_matrix(self):
        """lk(x_i,x_j) from the braid crossings (valid for pairs whose feet are
        NOT interleaved), and self-writhe on the diagonal."""
        bands = sorted(set(self.feet))
        L = {(i, j): 0 for i in bands for j in bands}
        for (bl, el, br, er, sg) in self.crossing_data():
            L[(bl, br)] += sg
            if bl != br:
                L[(br, bl)] += sg
        # each unordered pair counted once per crossing above
        out = {}
        for i in bands:
            for j in bands:
                if i == j:
                    out[(i, j)] = L[(i, j)]          # self-writhe (should be 0)
                elif self.interleaved(i, j):
                    out[(i, j)] = ('sum', L[(i, j)])   # cores intersect: V_ij+V_ji
                else:
                    assert L[(i, j)] % 2 == 0, (i, j, L[(i, j)])
                    out[(i, j)] = L[(i, j)] // 2
        return out

    def interleaved(self, i, j):
        pi = [k for k, b in enumerate(self.feet) if b == i]
        pj = [k for k, b in enumerate(self.feet) if b == j]
        a, b = pi
        c, d = pj
        return (a < c < b < d) or (c < a < d < b)

    def top_caps(self):
        """Positions (1-indexed) at which to cap, bottom-up, given final state."""
        st = list(self.state)
        caps = []
        while st:
            for i in range(len(st) - 1):
                if st[i][0] == st[i + 1][0]:
                    caps.append(i + 1)
                    del st[i:i + 2]
                    break
            else:
                raise RuntimeError("bands not cappable: %s" % (st,))
        return caps


# ------------------------------------------------------- Morse -> spherogram
class Morse:
    """Builds a spherogram Link from a bottom-up Morse word."""
    def __init__(self):
        self.stack = []
        self.uf = {}
        self.halfedges = {}       # node -> (crossing, slot)
        self.crossings = []
        self._c = 0

    def _new(self):
        self._c += 1
        n = self._c
        self.uf[n] = n
        return n

    def find(self, x):
        while self.uf[x] != x:
            self.uf[x] = self.uf[self.uf[x]]
            x = self.uf[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.uf[ra] = rb

    def cup(self, i):
        """local minimum: two new strands at positions i, i+1 (1-indexed)."""
        a = self._new()
        self.stack[i - 1:i - 1] = [a, a]

    def cap(self, i):
        u = self.stack[i - 1]
        v = self.stack[i]
        self.union(u, v)
        del self.stack[i - 1:i + 1]

    def cross(self, i, flag):
        u, v = self.stack[i - 1], self.stack[i]
        c = Crossing('c%d' % len(self.crossings))
        self.crossings.append(c)
        nSW, nSE, nNE, nNW = self._new(), self._new(), self._new(), self._new()
        self.union(nSW, u)
        self.union(nSE, v)
        if flag == 'L':
            # SW->NE is OVER, so the under strand is SE->NW; slots CCW from SE
            order = [nSE, nNE, nNW, nSW]
        else:
            # SE->NW is OVER, under strand is SW->NE; slots CCW from SW
            order = [nSW, nSE, nNE, nNW]
        for s, node in enumerate(order):
            self.halfedges[node] = (c, s)
        self.stack[i - 1] = nNW
        self.stack[i] = nNE

    def link(self):
        assert not self.stack, "diagram not closed"
        classes = {}
        for node, cs in list(self.halfedges.items()):
            classes.setdefault(self.find(node), []).append(cs)
        for cls, lst in classes.items():
            assert len(lst) == 2, (cls, lst)
            (c1, s1), (c2, s2) = lst
            c1[s1] = c2[s2]
        return Link(self.crossings, check_planarity=False)


# ------------------------------------------------------------ doubling
def boundary_link(core):
    """Return the spherogram Link which is the boundary of the disk-with-bands."""
    n = core.n
    M = Morse()
    # bottom: cups (1,24),(2,3),(4,5),...,(2n-2,2n-1)
    M.cup(1)
    for k in range(1, n):
        M.cup(2 * k)
    assert len(M.stack) == 2 * n
    # braid, doubled
    for (pos, flag) in core.word:
        m = pos
        # blocks A at (2m-1,2m), B at (2m+1,2m+2); word sigma_2 sigma_1 sigma_3 sigma_2
        for off in (2, 1, 3, 2):
            M.cross(2 * m - 2 + off, flag)
    # top caps, doubled: core cap at position i -> cap(2i), cap(2i-1)
    for i in core.top_caps():
        M.cap(2 * i)
        M.cap(2 * i - 1)
    return M.link()


# --------------------------------------------------------------- self-test
def _selftest():
    """Calibration + sanity checks.  Run with `python3 bands.py`.

    A lone genus-1 handle (feet 1,2,1,2 with the single crossing that
    un-interleaves them) bounds an unknot whatever the flag, because both
    [[0,1],[0,0]] and [[0,0],[-1,0]] have det(V - tV^T) = t.  Adding clasps
    moves V_12 + V_21 in steps of 2 and the boundary becomes a genuine knot,
    which is what calibrates the sign conventions.
    """
    ok = True

    def alex(c):
        L = boundary_link(c)
        L.simplify('global')
        return str(L.alexander_polynomial()) if L.crossings else '1'

    # 1. lone handle -> unknot, for both flags
    for flag in ('L', 'R'):
        c = Core([1, 2, 1, 2]); c.add(2, flag)
        got = alex(c)
        good = got in ('1', 't')
        ok &= good
        print('handle flag=%s : V_12+V_21 = %-3s  Alexander %-8s  %s'
              % (flag, c.linking_matrix()[(1, 2)][1], got, 'OK' if good else 'FAIL'))

    # 2. handle + n clasps: V_12+V_21 = -1 + 2n, and n = 2 gives V = [[0,2],[1,0]],
    #    Alexander 2t^2 - 5t + 2, i.e. the knot 6_1 (determinant 9).
    for n, want_sum in ((1, 1), (2, 3)):
        c = Core([1, 2, 1, 2]); c.clasp(1, 'L', n); c.add(2, 'L')
        s = c.linking_matrix()[(1, 2)][1]
        got = alex(c)
        good = (s == want_sum) and (n == 1 or '2*t^2 - 5*t + 2' in got.replace('  ', ' '))
        ok &= good
        print('handle + %d L-clasp(s): V_12+V_21 = %-3s Alexander %-20s %s'
              % (n, s, got, 'OK' if good else 'FAIL'))

    # 3. a clasp between two bands in different handles is an honest linking number
    c = Core([1, 2, 1, 2, 3, 4, 3, 4])
    c.clasp_between(2, -1, 3, +1, 'R')
    L = c.linking_matrix()
    good = (L[(2, 3)] == 1 and L[(1, 3)] == 0 and L[(1, 1)] == 0)
    ok &= good
    print('cross-handle clasp: lk(2,3) = %s, lk(1,3) = %s, writhe(1) = %s  %s'
          % (L[(2, 3)], L[(1, 3)], L[(1, 1)], 'OK' if good else 'FAIL'))

    # 4. travels are free: they change no linking number and no self-writhe
    c = Core([1, 2, 1, 2, 3, 4, 3, 4])
    before = c.linking_matrix()
    c.travel(3, 6); c.travel_back(3, 6)
    good = (c.linking_matrix() == before)
    ok &= good
    print('travel out and back changes nothing: %s' % ('OK' if good else 'FAIL'))

    print('\n%s' % ('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED'))
    return ok


if __name__ == '__main__':
    import sys
    sys.exit(0 if _selftest() else 1)
