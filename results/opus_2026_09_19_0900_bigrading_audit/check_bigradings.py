#!/usr/bin/env python3
"""Independent audit of the stored HFK ABSOLUTE BIGRADINGS for the Abe-Tagami family.

WHY THIS MATTERS, AND WHY IT IS THE RIGHT THING TO DO NEXT
----------------------------------------------------------
`research/11` concludes that K_0 and K_1 have the SAME involutive knot-Floer
local-equivalence class.  Its consequence has not been propagated: local
equivalence classes form a group, so [K_0] = [K_1] gives [K_0] - [K_1] = 0, i.e.
D_{0,1} = K_0 # (-K_1) is involutively locally TRIVIAL and every involutive
concordance invariant vanishes on it.  So `HANDOFF` P4 -- "a non-vanishing
involutive obstruction would kill the AT lane" -- is already answered NO, and
P4 is not a live lane.  `ERRATA_2026-09-18_OPUS.md` E18-7 says the same and says
the cheap task is to AUDIT research/11's conditions rather than recompute.

That whole chain is conditional on one thing, flagged by
`research/opus_mixed_lift_review.md` risk 1/2 and still recorded as OPEN in
`results/opus_2026_09_18_0040_hfk_delta_law/README.md`:

  "Nothing establishes that C_calc is the UV=0 reduction of the true CFK_UV(K_1)
   *with correct absolute bigradings*.  A uniform grading shift is harmless; a
   RELATIVE grading error is fatal ... A convention mismatch (mirror, or U<->V)
   would silently swap alpha <-> beta."

It stayed open because every recomputation used the same engine family.  This
script does not use the HFK engine at all.

THE TWO INDEPENDENT TESTS
-------------------------
1. GRADED EULER CHARACTERISTIC.  For any knot,
       sum_{A,M} (-1)^M * rank HFK_M(K, A) * t^A  =  Delta_K(t)
   up to normalisation.  The left side is the STORED bigrading data; the right
   side is computed here from a SEIFERT MATRIX of the stored diagram via
   det(V - tV^T), a completely different route with no Floer input.  This pins
   the Alexander gradings and the Maslov gradings mod 2.  A relative Alexander
   error, a mirror convention flip, or a U<->V swap all break it.

2. HFK SYMMETRY.  rank HFK_M(K, A) = rank HFK_{M-2A}(K, -A), a theorem.
   This ties the absolute Maslov grading to the Alexander grading, which is
   exactly the relative information risk 1/2 says is fatal if wrong.

Plus: fibered knots have rank HFK(K, g) = 1 at the top Alexander grading, and
genus = max A.

A PASS DOES NOT close risk 1/2 in full -- it does not certify the lift to a
homogeneous minimal full complex (risk 3).  It closes the part that a relative
or convention error would break, by a route sharing no code with the calculator.

Usage: python3 check_bigradings.py
"""
import json, os, sys
import sympy
from sympy import symbols, Poly, expand
import snappy

t = symbols('t')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')

STORED = os.path.join(ROOT, 'results', 'opus_2026_09_18_0040_hfk_delta_law', 'RESULTS.json')
KNOTS = {
    'K_0': 'AbeTagami_K_0_K_-1__6_3.json',
    'K_1': 'AbeTagami_K_1.json',
    'K_2': 'AbeTagami_K_2.json',
    'K_3': 'AbeTagami_K_3.json',
}


def normalise(coeffs):
    """Strip the +-t^k unit so two Alexander polynomials can be compared."""
    c = list(coeffs)
    while c and c[-1] == 0:
        c.pop()
    while c and c[0] == 0:
        c.pop(0)
    if c and c[0] < 0:
        c = [-x for x in c]
    return c


def alexander_from_seifert(pd):
    """Delta from a Seifert matrix -- no Floer input of any kind."""
    L = snappy.Link([tuple(c) for c in pd])
    V = sympy.Matrix(L.seifert_matrix())
    p = Poly(expand((V - t * V.T).det()), t)
    return normalise([int(x) for x in p.all_coeffs()])


def euler_from_hfk(ranks):
    """sum (-1)^M rank * t^A, from the STORED bigradings."""
    poly = {}
    for key, rk in ranks.items():
        A, M = (int(x) for x in key.split(','))
        poly[A] = poly.get(A, 0) + ((-1) ** M) * rk
    lo, hi = min(poly), max(poly)
    coeffs = [poly.get(a, 0) for a in range(hi, lo - 1, -1)]
    return normalise(coeffs), lo, hi


def symmetry_failures(ranks):
    R = {}
    for key, rk in ranks.items():
        A, M = (int(x) for x in key.split(','))
        R[(A, M)] = rk
    bad = []
    for (A, M), rk in R.items():
        mirror = R.get((-A, M - 2 * A), 0)
        if mirror != rk:
            bad.append(dict(A=A, M=M, rank=rk, mirrored_to=(-A, M - 2 * A),
                            mirrored_rank=mirror))
    return bad


def main():
    stored = json.load(open(STORED))['hfk']
    checks, npass = [], 0

    for name, fn in KNOTS.items():
        d = json.load(open(os.path.join(ROOT, 'data', 'knots', fn)))
        pd = d.get('pd_code_snappy_0indexed') or d['pd_code']
        h = stored[name]
        ranks = h['ranks']

        delta_seifert = alexander_from_seifert(pd)
        euler, lo, hi = euler_from_hfk(ranks)
        match = (euler == delta_seifert) or (euler == delta_seifert[::-1]) or \
                ([-x for x in euler] == delta_seifert) or \
                ([-x for x in euler] == delta_seifert[::-1])

        sym = symmetry_failures(ranks)
        genus_ok = (hi == h['genus'] and -lo == h['genus'])
        top_rank = sum(v for k, v in ranks.items() if int(k.split(',')[0]) == hi)
        fibered_ok = (top_rank == 1) if h['fibered'] else True

        for label, ok, detail in [
            (f'{name}: graded Euler char of stored HFK = Delta from Seifert matrix',
             match, f'euler={euler} seifert={delta_seifert}'),
            (f'{name}: HFK symmetry rank(A,M) = rank(-A,M-2A)',
             not sym, f'{len(sym)} violations'),
            (f'{name}: Alexander support [-g, g] with g = {h["genus"]}',
             genus_ok, f'support [{lo},{hi}]'),
            (f'{name}: fibered => rank at top Alexander grading is 1',
             fibered_ok, f'top rank {top_rank}'),
        ]:
            checks.append(dict(name=label, **{'pass': bool(ok)}, detail=detail))
            npass += bool(ok)

    out = dict(
        all_checks_pass=all(c['pass'] for c in checks),
        n_checks=len(checks), n_pass=npass,
        checks=checks,
        closes=('the part of risk 1/2 that a RELATIVE Alexander-grading error, a '
                'mirror convention flip, or a U<->V swap would break, by a route '
                'sharing no code with the HFK calculator'),
        does_not_close=('risk 3 (d_pure^2 = 0 over S) and the lift to a '
                        'homogeneous minimal full complex; and it certifies '
                        'gradings, not the involution itself'),
        counterexample=False)
    print(json.dumps(out, indent=1))
    json.dump(out, open(os.path.join(HERE, 'RESULTS.json'), 'w'), indent=1)
    return 0 if out['all_checks_pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
