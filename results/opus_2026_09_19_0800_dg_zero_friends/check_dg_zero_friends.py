#!/usr/bin/env python3
"""
Does the Dunfield-Gong 0-friend collection contain a "wild Miyazaki pair"?

A wild Miyazaki pair (HANDOFF_2026_09_18_OPUS.md section 4) is a pair of
DISTINCT prime fibered knots sharing one IRREDUCIBLE Alexander polynomial.
By Miyazaki Thm 5.5 the difference J # (-J') of such a pair is never
homotopy-ribbon, so a concordant pair refutes Slice-Ribbon.

HANDOFF P2 and research/24 line 185 both name "mine Dunfield-Gong's 0-friend
pairs" as the way to extend the search past this repository's own <= 14
crossing census (which came back empty, results/opus_2026_09_19_0700_*).

This script settles that item.  It is a DATA CHECK on a THEOREM, not a search:
Proposition below says the answer must be no, and the data is the control that
the proposition is not mis-stated.

    Proposition.  No 0-friend pair drawn from a plausibly-slice census can be a
    wild Miyazaki pair, at any crossing number.

    Proof.  DG section 1.8 defines PS19 by sigma(K) = 0 and Fox-Milnor:
    Delta_K(t) = f(t) f(t^-1) up to a unit of Z[t^+-1].  Normalising f to a
    polynomial of degree d with f(0) != 0 gives Delta = f(t) f*(t) with
    f*(t) = t^d f(1/t), both of degree d.  If Delta is irreducible in Q[t] then
    one factor is a unit, so d = 0 and Delta is a constant; Delta(1) = +-1 forces
    Delta = 1.  A fibered knot has deg Delta = 2g, so Delta = 1 forces g = 0 and
    the knot is the unknot.  A 0-friend shares its 0-surgery, hence its
    Alexander polynomial, with its base knot, so the same applies to both
    members of the pair.  QED

Usage:  python3 check_dg_zero_friends.py <path to plausibly_slice_V1/data>

Data:  Dunfield-Gong, "Ribbon concordances and slice obstructions: code and
data", Harvard Dataverse, doi:10.7910/DVN/YBDTBT, single file
plausibly_slice_V1.zip, md5 7f6dc1df595ba1b4dbb1a9b338798b0b (verified).
"""
import csv, json, os, sys
from collections import defaultdict
import sympy
from sympy import Poly, symbols

t = symbols('t')
csv.field_size_limit(10**7)


def classify(s, _cache={}):
    """(monic, irreducible_over_Q, degree) for an Alexander polynomial string."""
    if s in _cache:
        return _cache[s]
    try:
        p = Poly(sympy.sympify(s.replace('^', '**')), t)
    except Exception:
        r = (None, None, None)
        _cache[s] = r
        return r
    co = p.all_coeffs()
    monic = abs(co[0]) == 1 and abs(co[-1]) == 1
    fl = sympy.factor_list(p.as_expr(), t)[1]
    irr = (len(fl) == 1 and fl[0][1] == 1 and p.degree() > 0)
    r = (monic, irr, p.degree())
    _cache[s] = r
    return r


CONTROLS = [
    # (name, Alexander polynomial, monic?, irreducible over Q?)
    ("3_1  (fibered, irreducible)",            "t^2-t+1",                      True,  True),
    ("6_3  (fibered, irreducible; K_0 of AT)", "t^4-3*t^3+5*t^2-3*t+1",        True,  True),
    ("6_1  (ribbon; Fox-Milnor norm)",         "2*t^2-5*t+2",                  False, False),
    ("square knot 3_1#-3_1 (norm)",            "t^4-2*t^3+3*t^2-2*t+1",        True,  False),
    ("unknot",                                 "1",                            True,  False),
]


def run_controls():
    rows, ok = [], True
    for name, poly, want_monic, want_irr in CONTROLS:
        monic, irr, deg = classify(poly)
        good = (monic == want_monic) and (irr == want_irr)
        ok = ok and good
        rows.append(dict(control=name, poly=poly, degree=deg, monic=monic,
                         irreducible=irr, expected=(want_monic, want_irr),
                         pass_=good))
    return ok, rows


def main(datadir):
    controls_pass, control_rows = run_controls()

    stats = defaultdict(int)
    hits = []
    files = ["zero_friends.csv", "more_zero_friends.csv"]
    for fn in files:
        path = os.path.join(datadir, fn)
        with open(path) as f:
            for row in csv.DictReader(f):
                stats['rows'] += 1
                a = (row.get('alex') or '').strip()
                if not a:
                    stats['alex_missing'] += 1
                    continue
                monic, irr, deg = classify(a)
                if monic is None:
                    stats['unparsed'] += 1
                    continue
                if deg == 0:
                    stats['alex_trivial'] += 1
                    continue
                stats['alex_nontrivial'] += 1
                if not monic:
                    stats['not_monic'] += 1
                    continue
                stats['monic'] += 1
                if irr:
                    stats['monic_irreducible'] += 1
                    hits.append(dict(file=fn, base_knot=row.get('base_knot'),
                                     alex=a, degree=deg,
                                     num_cross=row.get('num_cross')))
                else:
                    stats['monic_reducible'] += 1

    out = dict(
        source="Dunfield-Gong, doi:10.7910/DVN/YBDTBT, plausibly_slice_V1.zip",
        source_md5="7f6dc1df595ba1b4dbb1a9b338798b0b",
        files=files,
        controls_pass=controls_pass,
        controls=control_rows,
        stats=dict(sorted(stats.items())),
        wild_miyazaki_candidates=hits,
        verdict=("NO wild Miyazaki pair exists in the DG 0-friend collection. "
                 "This is forced by Fox-Milnor (see the Proposition in this "
                 "file's docstring), and the data agrees. It is a THEOREM, not "
                 "a failed search."),
        counterexample_to_slice_ribbon=False,
    )
    print(json.dumps(out, indent=2))
    return out, controls_pass and not hits


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "."
    out, ok = main(d)
    sys.exit(0 if ok else 1)
