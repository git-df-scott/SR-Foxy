#!/usr/bin/env python3
"""Validate the bundled HFK calculator's bigradings against the alternating theorem.

research/opus_mixed_lift_review.md risk 1: "Nothing in the argument establishes
that C_calc is the UV=0 reduction of the true CFK_UV(K_1) *with correct absolute
bigradings*.  A uniform grading shift is harmless; a **relative** grading error is
fatal, because it changes which pairs admit a mixed monomial."

Ozsvath-Szabo: for an ALTERNATING knot, HFK-hat_m(K,s) has rank |a_s| (the
coefficient of the Alexander polynomial) and is supported in the single Maslov
grading m = s - sigma/2, with sigma the knot signature.  So every alternating
knot is a closed-form test of the engine's relative bigradings.

Neither `Link.signature()` nor `Link.alexander_polynomial()` is available outside
Sage, but `Link.seifert_matrix()` is, so both are derived here:
  Delta(t) = det(V - t V^T), normalised to Delta(1) = +1;
  sigma    = signature(V + V^T), by exact congruence diagonalisation over Q.

Both Maslov sign conventions are tested, because spherogram's seifert_matrix()
convention for its named knots need not agree with the standard knot signature.
A uniform winner validates the RELATIVE gradings, which is the fatal case; it
does not pin the global sign, which is a chirality convention.

Result recorded 18 September 2026: 196 alternating knots checked, all 196 match
m = s - sigma/2, 0 match the other convention, 0 match neither.
"""
import sys

import spherogram
import sympy as sp

t = sp.Symbol("t")


def signature(A):
    """Exact signature of a symmetric rational matrix by congruence diagonalisation."""
    A = sp.Matrix(A)
    n = A.rows
    pos = neg = 0
    while n > 0:
        idx = next((i for i in range(n) if A[i, i] != 0), None)
        if idx is None:
            pair = next(((i, j) for i in range(n) for j in range(i + 1, n)
                         if A[i, j] != 0), None)
            if pair is None:
                break                      # remaining block is zero: nullity
            i, j = pair
            A[i, :] = A[i, :] + A[j, :]
            A[:, i] = A[:, i] + A[:, j]    # congruence, creates a nonzero diagonal
            continue
        A.row_swap(0, idx)
        A.col_swap(0, idx)
        p = A[0, 0]
        if p > 0:
            pos += 1
        else:
            neg += 1
        for i in range(1, n):
            A[i, :] = A[i, :] - (A[i, 0] / p) * A[0, :]
        for j in range(1, n):
            A[:, j] = A[:, j] - (A[0, j] / p) * A[:, 0]
        A = A[1:, 1:]
        n -= 1
    return pos - neg


def alexander(V):
    V = sp.Matrix(V)
    c = sp.Poly(sp.expand((V - t * V.T).det()), t).all_coeffs()[::-1]
    while c and c[0] == 0:
        c = c[1:]
    if sum(c) < 0:
        c = [-x for x in c]
    return [int(x) for x in c]


def main():
    plus = minus = neither = skipped = 0
    bad = []
    for n in range(3, 11):
        for i in range(1, 200):
            try:
                L = spherogram.Link("%d_%d" % (n, i))
            except Exception:
                break
            try:
                if not L.is_alternating():
                    skipped += 1
                    continue
                V = L.seifert_matrix()
                c = alexander(V)
                if len(c) % 2 == 0:
                    skipped += 1
                    continue
                g = (len(c) - 1) // 2
                s = signature(sp.Matrix(V) + sp.Matrix(V).T)
                got = dict(L.knot_floer_homology()["ranks"])
            except Exception:
                skipped += 1
                continue
            pred_p = {(k - g, k - g + s // 2): abs(c[k])
                      for k in range(len(c)) if c[k]}
            pred_m = {(k - g, k - g - s // 2): abs(c[k])
                      for k in range(len(c)) if c[k]}
            if pred_m == got:
                minus += 1
            elif pred_p == got:
                plus += 1
            else:
                neither += 1
                if len(bad) < 5:
                    bad.append(("%d_%d" % (n, i), s, pred_p, got))
    print("alternating knots checked:", plus + minus + neither)
    print("  matches m = s - sigma/2 :", minus)
    print("  matches m = s + sigma/2 :", plus)
    print("  matches NEITHER         :", neither)
    print("  skipped                 :", skipped)
    for b in bad:
        print("   NEITHER:", b)
    # Validation succeeds iff one convention wins uniformly and nothing is unexplained.
    return 0 if neither == 0 and (plus == 0 or minus == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
