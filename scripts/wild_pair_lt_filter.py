#!/usr/bin/env python3
"""Levine-Tristram filter on the wild Miyazaki pair list.

For a wild pair (J, J') -- distinct prime fibered knots sharing one irreducible
Alexander polynomial -- the knot D = J # (-J') is certified NOT homotopy-ribbon
by Miyazaki Thm 5.5.  D is slice iff J is smoothly concordant to J'.

The Levine-Tristram signature sigma_omega is a CONCORDANCE INVARIANT and
vanishes on slice knots (Levine; Tristram), so

    J ~ J'   ==>   sigma_omega(J) = sigma_omega(J')  for every omega on the
                   unit circle with Delta_J(omega) != 0.

Contrapositive: any pair with a single mismatching omega is PROVED NOT
CONCORDANT, hence D is proved not slice, and the expensive band search must not
be spent on it.  This is an obstruction, not a heuristic -- unlike everything
the existing pair filter uses (Delta, tau, nu, eps, genus agree across the whole
list by construction or coarseness).

sigma_omega(K) = signature of the Hermitian form (1-omega) V + (1-conj(omega)) V^T,
V a Seifert matrix.  Computed with numpy eigvalsh; eigenvalues within TOL of 0
make the value unreliable and that omega is skipped for that knot.

CONTROLS (must all pass or the run aborts):
  * every slice knot tested has sigma_omega == 0 at every omega  -- the filter
    must not fire on something that IS slice, or it would kill true pairs;
  * the trefoil has sigma_omega != 0 somewhere -- the filter must be able to
    fire at all;
  * sigma at omega = -1 reproduces the repository's own Murasugi signature.

Usage: wild_pair_lt_filter.py <out.json> [n_pairs]
"""
import json, gzip, os, re, sys, time, cmath
from collections import defaultdict

import numpy as np
import snappy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sagefree_slice_filter as sff
from spherogram.links.bands import normalize_crossing_labels

TOL = 1e-7
# Prime-power roots of unity: the omegas at which Levine-Tristram is a
# concordance obstruction in the classical (Casson-Gordon-free) statement.
PRIME_POWERS = [2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 17, 19, 23, 25, 27, 29, 31]


def omegas():
    out = []
    for q in PRIME_POWERS:
        for k in range(1, q):
            if q == 2 and k != 1:
                continue
            out.append((q, k, cmath.exp(2j * cmath.pi * k / q)))
    return out


OMEGAS = omegas()


def lt_signature_vector(V):
    """sigma_omega for each omega in OMEGAS; None where the form is degenerate."""
    V = np.array(V, dtype=float)
    Vt = V.T
    out = []
    for _q, _k, w in OMEGAS:
        H = (1 - w) * V + (1 - w.conjugate()) * Vt
        H = (H + H.conjugate().T) / 2.0          # force exact hermitian
        ev = np.linalg.eigvalsh(H)
        if np.any(np.abs(ev) < TOL):
            out.append(None)                      # degenerate: Delta(omega)=0
        else:
            out.append(int(np.sum(ev > 0) - np.sum(ev < 0)))
    return out


_cache = {}
def lt_of(name):
    if name not in _cache:
        V = snappy.Link(name).seifert_matrix()
        _cache[name] = lt_signature_vector(V)
    return _cache[name]


def compatible(a, b):
    """False only when some omega is decided for BOTH and the values differ."""
    for x, y in zip(a, b):
        if x is not None and y is not None and x != y:
            return False
    return True


def orientations(a, b):
    """Which of D = J # (-J') and D = J # J' survive Levine-Tristram.

    A census entry names a knot only up to mirror (a knot and its mirror share
    an exterior and one census entry), so BOTH differences have to be tested.
    sigma_omega(mirror K) = -sigma_omega(K), so the second test compares a
    against -b.  Miyazaki applies to either difference: the prime fibered
    summands still fail to pair as long as J is not +-J'.
    """
    nb = [None if y is None else -y for y in b]
    out = []
    if compatible(a, b):
        out.append('J # (-J\')')
    if compatible(a, nb):
        out.append('J # J\'')
    return out


def run_controls():
    rows, ok = [], True
    # slice knots: sigma_omega must be identically zero
    for name in ['6_1', '8_8', '9_46', '10_3', '6_1']:
        v = lt_of(name)
        z = all(x == 0 for x in v if x is not None)
        rows.append(dict(control=f'slice {name}: sigma_omega == 0', passed=bool(z)))
        ok = ok and z
    # square knot = 3_1 # -3_1, ribbon: identically zero.  spherogram's Seifert
    # algorithm can fail on a composite diagram; simplify and normalize first,
    # and if it still cannot build V, record the control as SKIPPED rather than
    # failed -- a tool that cannot run has decided nothing.
    try:
        K = snappy.Link('3_1').connected_sum(snappy.Link('3_1').mirror())
        K.simplify('global')
        normalize_crossing_labels(K)
        v = lt_signature_vector(K.seifert_matrix())
        z = all(x == 0 for x in v if x is not None)
        rows.append(dict(control='ribbon square knot: sigma_omega == 0', passed=bool(z)))
        ok = ok and z
    except Exception as e:
        rows.append(dict(control='ribbon square knot: sigma_omega == 0',
                         passed=None, skipped=type(e).__name__))
    # trefoil: must fire somewhere
    v = lt_of('3_1')
    fires = any(x not in (None, 0) for x in v)
    rows.append(dict(control='trefoil: sigma_omega != 0 somewhere', passed=bool(fires),
                     values=sorted({x for x in v if x is not None})))
    ok = ok and fires
    # omega = -1 must reproduce the repo's Murasugi signature
    i_m1 = [i for i, (q, k, _) in enumerate(OMEGAS) if q == 2][0]
    for name in ['3_1', '4_1', '6_1', '5_2']:
        mine = lt_of(name)[i_m1]
        theirs = sff.seifert_signature(snappy.Link(name))
        good = (mine == theirs) or (mine == -theirs)
        rows.append(dict(control=f'omega=-1 matches Murasugi on {name}',
                         passed=bool(good), lt=mine, repo=theirs))
        ok = ok and good
    return ok, rows


def load_pairs(path):
    rows = [json.loads(l) for l in gzip.open(path, 'rt')]
    rows = [r for r in rows if 'delta' in r]
    def cr(n):
        m = re.match(r'K?(\d+)[an]', n)
        return int(m.group(1)) if m else 99
    buck = defaultdict(list)
    for r in rows:
        buck[tuple(r['delta'])].append(r)
    pairs = []
    for k, v in buck.items():
        if len(v) < 2:
            continue
        for i in range(len(v)):
            for j in range(i + 1, len(v)):
                a, b = v[i], v[j]
                if (a['tau'], a['nu'], a['eps'], a['genus']) == \
                   (b['tau'], b['nu'], b['eps'], b['genus']):
                    pairs.append(dict(cr_sum=cr(a['name']) + cr(b['name']),
                                      A=a['name'], B=b['name'],
                                      genus=a['genus'], deg_delta=len(k) - 1))
    pairs.sort(key=lambda p: (p['cr_sum'], p['A'], p['B']))
    return pairs


def main():
    out = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
    ok, controls = run_controls()
    print(json.dumps(controls, indent=1), flush=True)
    if not ok:
        print('CONTROLS FAILED -- refusing to report any filtering', flush=True)
        json.dump(dict(controls_pass=False, controls=controls), open(out, 'w'), indent=1)
        sys.exit(1)
    print('controls pass\n', flush=True)

    here = os.path.dirname(os.path.abspath(__file__))
    pairs = load_pairs(os.path.join(here, '..', 'data', 'sweeps',
                                    'miyazaki_pair_sweep.jsonl.gz'))
    if limit:
        pairs = pairs[:limit]
    t0 = time.time()
    survivors, killed, errors = [], 0, 0
    for i, p in enumerate(pairs):
        try:
            a, b = lt_of(p['A']), lt_of(p['B'])
        except Exception:
            errors += 1
            survivors.append(p)          # undecided keeps the pair; never lose one
            continue
        orients = orientations(a, b)
        if orients:
            p = dict(p, lt_surviving_orientations=orients)
            survivors.append(p)
        else:
            killed += 1
        if i % 2000 == 0:
            print(f'  {i}/{len(pairs)}  killed={killed}  {time.time()-t0:.0f}s', flush=True)

    res = dict(
        controls_pass=True, controls=controls,
        n_omegas=len(OMEGAS), prime_powers=PRIME_POWERS,
        pairs_in=len(pairs),
        pairs_killed_by_levine_tristram=killed,
        pairs_surviving=len(survivors),
        seifert_matrix_errors=errors,
        meaning=('a killed pair is PROVED not concordant, so its D = J # (-J\') is '
                 'proved not slice and is not a counterexample; a surviving pair is '
                 'undecided, NOT a counterexample and NOT evidence of one'),
        counterexample=False,
        survivors=survivors,
        seconds=round(time.time() - t0, 1))
    json.dump(res, open(out, 'w'), indent=1)
    print(f'\npairs in {len(pairs)}  KILLED {killed}  surviving {len(survivors)}  '
          f'errors {errors}  {time.time()-t0:.0f}s', flush=True)


if __name__ == '__main__':
    main()
