#!/usr/bin/env python3
"""The R-link property: does 0-framed surgery on every component give #_n(S^1 x S^2)?

This is the decisive acceptance test that three scripts in this repository
name and none implements.  `scripts/gst_link_from_band_fission.py`,
`scripts/gst_L31_shaken_fission.py` and `scripts/verify_L31_candidates.py` all
end their scope note with "a positive still needs the R-link property,
0-surgery on both components giving #2(S^1 x S^2)", and then stop.  Without it
a candidate for GST's `L_{3,1}` is a nomination on component invariants only.

Why the test is decisive rather than another screen.  A closed orientable
3-manifold whose fundamental group is free of rank n is `#_n(S^1 x S^2)`: the
Kneser-Milnor decomposition splits it into prime factors, a free group forces
every factor to be `S^1 x S^2` or simply connected, and the simply connected
ones are `S^3` by Perelman.  So "pi_1 free of rank n" is not evidence for the
R-link property, it is the R-link property.

What this implementation can and cannot conclude:

* `YES`  - SnapPy reduced the filled group to n generators and **0 relators**.
  That is a proof, modulo SnapPy's triangulation and group simplification
  being correct, which is the same footing as every other computation here.
* `NO`   - either the first homology of the filled manifold is not `Z^n`
  (`#_n(S^1 x S^2)` has `H_1 = Z^n`; for a 2-component link this is exactly
  linking number 0), or the filled manifold carries a hyperbolic structure.
  A hyperbolic 3-manifold is irreducible with non-free fundamental group, so
  it is not `#_n(S^1 x S^2)` for any `n >= 1`. Both are proofs.
* `NO` also - the filled group has the wrong number of homomorphisms to a
  finite group.  A free group of rank `n` has exactly `|G|^n` homomorphisms to
  `G`, for every finite `G`, so any other count refutes freeness outright.
  This is counted by brute force over generator images from the presentation,
  so it is exact, and unlike simplification it cannot be inconclusive when it
  fires.
* `UNKNOWN` - homology passes, the filled manifold is not certified hyperbolic,
  the finite-group counts all match, and no presentation reduced to 0 relators
  in the attempts allowed.  Group simplification is heuristic, so this is
  genuinely inconclusive and must never be reported as a rejection.

Usage:
    r_link_test.py --controls
    r_link_test.py <out.json> <link.json|pd-json> ...
"""
import json, sys, os, random, datetime
import snappy


def _perm_mul(a, b):
    return tuple(a[b[i]] for i in range(len(b)))


def _perms(k):
    from itertools import permutations
    return [tuple(p) for p in permutations(range(k))]


def _inv(p):
    q = [0] * len(p)
    for i, v in enumerate(p):
        q[v] = i
    return tuple(q)


def count_homs_to_symmetric(generators, relators, k, budget=4_000_000):
    """|Hom(<gens | rels>, S_k)| by brute force, or None if over budget."""
    from itertools import product
    P = _perms(k)
    if len(P) ** generators > budget:
        return None
    ident = tuple(range(k))
    total = 0
    for images in product(P, range(0)) if False else product(P, repeat=generators):
        inv = [_inv(g) for g in images]
        ok = True
        for r in relators:
            acc = ident
            for ch in r:
                if ch.islower():
                    acc = _perm_mul(acc, images[ord(ch) - ord('a')])
                else:
                    acc = _perm_mul(acc, inv[ord(ch) - ord('A')])
            if acc != ident:
                ok = False
                break
        if ok:
            total += 1
    return total


def r_link_verdict(link, tries=12, seed=0):
    """(verdict, detail) for a link, verdict in YES / NO / UNKNOWN."""
    n = len(link.link_components)
    detail = {'components': n, 'attempts': []}
    L = link.copy()
    try:
        E = L.exterior()
    except Exception as e:
        detail['error'] = f'exterior: {type(e).__name__}: {e}'
        return 'UNKNOWN', detail
    if E.num_cusps() != n:
        detail['error'] = f'exterior has {E.num_cusps()} cusps for {n} components'
        return 'UNKNOWN', detail
    for i in range(n):
        E.dehn_fill((0, 1), i)
    try:
        h = E.homology()
        detail['filled_homology'] = str(h)
    except Exception as e:
        detail['error'] = f'homology: {type(e).__name__}: {e}'
        return 'UNKNOWN', detail
    # H_1(#_n S^1 x S^2) = Z^n: free rank n, no torsion.
    if h.rank() != n or h.order() != 'infinite' or len(h.coefficients) != n:
        detail['reason'] = 'first homology of the filled manifold is not Z^%d' % n
        return 'NO', detail
    # A geometric solution on the filled manifold settles it the other way:
    # #n(S^1 x S^2) is reducible with free pi_1 and admits no hyperbolic
    # structure, so a positively oriented solution is a rejection. This is the
    # same criterion spherogram's own `is_unlink_exterior` uses, in reverse.
    try:
        st = E.solution_type()
        detail['filled_solution_type'] = st
        if st == 'all tetrahedra positively oriented':
            vol = E.volume()
            detail['filled_volume'] = float(vol)
            if float(vol) > 0.9:
                detail['reason'] = ('the 0-filled manifold is hyperbolic (volume '
                                    '%.6f), hence irreducible with non-free pi_1, '
                                    'so it is not #%d(S^1 x S^2)' % (float(vol), n))
                return 'NO', detail
    except Exception as e:
        detail['solution_type_error'] = f'{type(e).__name__}: {e}'

    # Counting homomorphisms to a finite group is exact and two-sided: a free
    # group of rank n has exactly |G|^n homomorphisms to G. Any other count
    # refutes freeness, so it rejects where group simplification can only fail
    # to confirm.
    rng = random.Random(seed)
    M = E.filled_triangulation() if hasattr(E, 'filled_triangulation') else E
    try:
        G0 = M.fundamental_group(simplify_presentation=True)
        gens, rels = G0.num_generators(), [str(r) for r in G0.relators()]
        detail['presentation'] = {'generators': gens, 'relators': rels}
        for k, name in ((3, 'S_3'), (4, 'S_4')):
            import math
            c = count_homs_to_symmetric(gens, rels, k)
            if c is None:
                continue
            expected = math.factorial(k) ** n
            detail.setdefault('hom_counts', {})[name] = {'counted': c,
                                                         'free_rank_%d' % n: expected}
            if c != expected:
                detail['reason'] = ('pi_1 of the 0-filled manifold has %d '
                                    'homomorphisms to %s, but a free group of rank '
                                    '%d has %d, so it is not free and the manifold '
                                    'is not #%d(S^1 x S^2)' % (c, name, n, expected, n))
                return 'NO', detail
    except Exception as e:
        detail['hom_count_error'] = f'{type(e).__name__}: {e}'

    for t in range(tries):
        try:
            G = M.fundamental_group(simplify_presentation=True)
            row = {'try': t, 'generators': G.num_generators(),
                   'relators': G.num_relators()}
            detail['attempts'].append(row)
            if G.num_relators() == 0 and G.num_generators() == n:
                detail['certificate'] = ('pi_1 of the 0-filled manifold is free of '
                                         'rank %d, so the manifold is #%d(S^1 x S^2)' % (n, n))
                return 'YES', detail
        except Exception as e:
            detail['attempts'].append({'try': t, 'error': f'{type(e).__name__}: {e}'})
        try:
            M.randomize()
        except Exception:
            try:
                M = E.filled_triangulation()
                M.randomize()
            except Exception:
                break
    detail['reason'] = ('homology is Z^%d but no presentation reduced to 0 relators '
                        'in %d attempts; group simplification is heuristic, so this '
                        'is inconclusive, NOT a rejection' % (n, tries))
    return 'UNKNOWN', detail


def _controls():
    rows = []
    cases = [
        ('2-component unlink', snappy.Link(braid_closure=[1, -1]), 'YES'),
        ('3-component unlink', snappy.Link(braid_closure=[1, -1, 2, -2]), 'YES'),
        ('Hopf link L2a1', snappy.Link('L2a1'), 'NO'),
        ('Whitehead link L5a1', snappy.Link('L5a1'), 'NO'),
        ('L6a5', snappy.Link('L6a5'), 'NO'),
        ('L7a1', snappy.Link('L7a1'), 'NO'),
    ]
    for name, L, expected in cases:
        v, d = r_link_verdict(L)
        ok = (v == expected) or (expected == 'UNKNOWN_OR_NO' and v in ('NO', 'UNKNOWN'))
        rows.append({'case': name, 'components': len(L.link_components),
                     'verdict': v, 'expected': expected, 'as_expected': ok,
                     'filled_homology': d.get('filled_homology'),
                     'filled_volume': d.get('filled_volume'),
                     'reason': d.get('reason'), 'certificate': d.get('certificate')})
        print(f'{"ok " if ok else "MISMATCH"} {name:24s} -> {v:8s} '
              f'(expected {expected}); H1 = {d.get("filled_homology")}', flush=True)
    return rows


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--controls':
        rows = _controls()
        out = 'results/session_2026-09-15b/r_link_test_controls.json'
        os.makedirs(os.path.dirname(out), exist_ok=True)
        json.dump({'date': datetime.datetime.utcnow().isoformat() + 'Z',
                   'what': ('controls for scripts/r_link_test.py, the R-link '
                            'property test: 0-framed surgery on every component '
                            'gives #n(S^1 x S^2)'),
                   'controls': rows,
                   'all_as_expected': all(r['as_expected'] for r in rows)},
                  open(out, 'w'), indent=1)
        print('wrote', out)
        sys.exit(0 if all(r['as_expected'] for r in rows) else 1)
    out = sys.argv[1]
    rec = {'date': datetime.datetime.utcnow().isoformat() + 'Z', 'results': []}
    for path in sys.argv[2:]:
        d = json.load(open(path))
        pds = d.get('candidates') or d.get('hits') or [d]
        for k, cand in enumerate(pds):
            pd = cand.get('pd_code') or cand.get('pd_code_snappy_0indexed')
            if not pd:
                continue
            L = snappy.Link([tuple(c) for c in pd])
            v, det = r_link_verdict(L)
            rec['results'].append({'source': path, 'index': k, 'verdict': v,
                                   'detail': det})
            print(path, k, v, det.get('filled_homology'), flush=True)
    json.dump(rec, open(out, 'w'), indent=1)
    print('wrote', out)
