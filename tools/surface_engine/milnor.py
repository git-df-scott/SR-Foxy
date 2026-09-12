"""
milnor.py -- the Milnor triple linking number mu-bar(i,j,k) of three band
cores, read straight off the braid word of a `bands.Core`.

    import build, milnor
    c = build.build(1, 1, 1, -1)
    milnor.mu(c, 1, 3, 5)        # {'mu': 1, ...}
    milnor.mu(c, 2, 4, 6)        # {'mu': -1, ...}

Self-test: `python3 milnor.py`.  No knot-theory library is needed -- this is
pure combinatorics on the word, which is why it is a genuinely independent
check on whether Figure-4's move did what it was supposed to do.

WHEN IS IT DEFINED
------------------
mu-bar(i,j,k) is an honest integer (no indeterminacy) exactly when the three
pairwise linking numbers vanish.  For Turaev's X that holds for (1,3,5) and for
(2,4,6): lk(x_1,x_3) = lk(x_1,x_5) = lk(x_3,x_5) = 0, likewise (2,4,6).  The
three cores are also genuinely disjoint curves, since bands in different
handles have non-interleaved feet, so their closing arcs inside the disk do not
meet.  `mu()` returns the two meridian exponent sums alongside the answer; if
either is non-zero the hypothesis has failed and the number is meaningless.

HOW IT IS COMPUTED
------------------
Milnor's definition, done directly:

 1. Walk the core loop x_i.  It is the UP strand (i, +1) traversed in
    increasing braid-letter order, then the DOWN strand (i, -1) traversed in
    DECREASING order (the loop goes up one strand, over the cap, and back down
    the other).  `longitude_word` does exactly this.

 2. At each letter, record a generator only when x_i passes UNDER a strand of
    x_j or x_k -- under-crossings are what contribute to the class of the arc
    in pi_1 of the complement of the other two bands; passing over contributes
    nothing.  For flag 'L' the left-incoming strand is over, so the right one
    is the under strand, and vice versa for 'R'.  The exponent is the sign of
    the crossing, s0 * eps_left * eps_right (see bands.py).  The result is a
    word in the free group F(a, b), a = meridian of x_j, b = meridian of x_k.

 3. `magnus_ab` takes the coefficient of AB in the Magnus expansion of that
    word (a -> 1 + A, a^-1 -> 1 - A + A^2 - ..., etc.).  Scanning left to
    right, each b^e picks up (running A-exponent-sum) * e.  For the commutator
    [a,b] = a b a^-1 b^-1 this gives 1, which is why the Figure-4 move
    registers as exactly +-1 per application.

The closing arcs inside the disk contribute nothing: they are disjoint from
everything, so the whole invariant lives in the braid word.
"""
import build


def longitude_word(c, i, others):
    """Word (list of (band, exponent)) read along the core loop of band i,
    recording only the crossings where x_i passes UNDER a strand of a band in
    `others`.  Exponent = sign of the crossing."""
    st = list(c.ident)
    events = []          # (letter_index, band_of_our_strand_eps, other_band, exp)
    per_letter = []
    for idx, (pos, flag) in enumerate(c.word):
        l, r = st[pos - 1], st[pos]
        s0 = 1 if flag == 'L' else -1
        sign = s0 * l[1] * r[1]
        # who is under?  'L' -> left is over -> right is under
        under = r if flag == 'L' else l
        over = l if flag == 'L' else r
        per_letter.append((l, r, under, over, sign))
        st[pos - 1], st[pos] = st[pos], st[pos - 1]

    word = []
    # up strand (i,+1): letters in increasing order
    for idx in range(len(per_letter)):
        l, r, under, over, sign = per_letter[idx]
        if under == (i, +1) and over[0] in others:
            word.append((over[0], sign))
    # down strand (i,-1): letters in decreasing order
    for idx in range(len(per_letter) - 1, -1, -1):
        l, r, under, over, sign = per_letter[idx]
        if under == (i, -1) and over[0] in others:
            word.append((over[0], sign))
    return word


def magnus_ab(word, j, k):
    """Coefficient of AB in the Magnus expansion of the word, where A is the
    meridian of band j and B that of band k.  Also returns exponent sums."""
    ea = eb = 0
    ab = 0
    for (band, e) in word:
        if band == j:
            # a^e : contributes A-degree e ; picks up nothing with previous B
            ea += e
        else:
            # b^e : coefficient of AB gains (current A exponent sum) * e
            ab += ea * e
            eb += e
    return ab, ea, eb


def mu(c, i, j, k):
    w = longitude_word(c, i, {j, k})
    ab, ea, eb = magnus_ab(w, j, k)
    return {'mu': ab, 'exp_sum_meridian_%d' % j: ea, 'exp_sum_meridian_%d' % k: eb,
            'word_length': len(w)}


# --------------------------------------------------------------- self-test
def _selftest():
    """Run with `python3 milnor.py`."""
    ok = True
    for (r, s) in [(0, 0), (1, 1), (1, -1), (-1, 1), (-1, -1), (2, 0), (0, 3), (2, 2)]:
        c = build.build(1, 1, r, s)
        a, b = mu(c, 1, 3, 5), mu(c, 2, 4, 6)
        good = (a['mu'] == r and b['mu'] == s
                and a['exp_sum_meridian_3'] == 0 and a['exp_sum_meridian_5'] == 0
                and b['exp_sum_meridian_4'] == 0 and b['exp_sum_meridian_6'] == 0)
        ok &= good
        print('r=%-2d s=%-2d : mu(1,3,5)=%-2d mu(2,4,6)=%-2d  '
              'meridian exponent sums all 0: %-5s  word lengths %d,%d  %s'
              % (r, s, a['mu'], b['mu'],
                 a['exp_sum_meridian_3'] == 0 and b['exp_sum_meridian_4'] == 0,
                 a['word_length'], b['word_length'], 'OK' if good else 'FAIL'))
    print('\n%s' % ('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED'))
    return ok


if __name__ == '__main__':
    import sys
    sys.exit(0 if _selftest() else 1)
