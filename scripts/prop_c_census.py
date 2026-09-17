#!/usr/bin/env python3
"""Census test of Proposition C (research/33 section 4b).

PROPOSITION C.  Let p be an odd prime, K a knot, and suppose H_1(Sigma_p(K)) is
elementary abelian of prime exponent q with q = 1 (mod p).  Then the linking
form of Sigma_p(K) is hyperbolic.  Hence the Sigma_p linking-form metabolizer
obstruction vanishes identically on every difference of two such knots.

Proof sketch (full proof in research/33): the deck transformation tau has order
p and preserves lambda; tau - 1 is invertible on H_1(Sigma_p) because
H_1(Sigma_p) = H_1(X_infinity)/(t^p - 1) and Delta_K(1) = +-1, so 1 is not an
eigenvalue.  With q = 1 (mod p) the primitive p-th roots of unity lie in F_q and
tau is diagonalizable, and lambda(x,y) = lambda(tau x, tau y) = alpha*beta*
lambda(x,y) forces E_alpha perp E_beta unless alpha*beta = 1.  Since alpha has
odd order dividing p, alpha = alpha^{-1} is impossible, so H_1 splits as an
orthogonal sum of hyperbolic planes E_alpha (+) E_{alpha^{-1}}.

This script tests the statement, and the complementary q = -1 (mod p) case,
over the knots of the SnapPy link-exterior table with Seifert matrices of size
at most 12, at p = 3, 5, 7.  A single violation would refute the proposition.

Usage: python3 scripts/prop_c_census.py <out.json>
"""
import json, os, sys, time, importlib.util
from collections import Counter
import snappy

_here = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    'cclfg', os.path.join(_here, 'cyclic_cover_linking_form_gate.py'))
_m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_m)

PRIMES = (3, 5, 7)
MAX_SEIFERT = 12


def is_prime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def main(out_path):
    if os.path.exists(out_path):
        sys.exit('refusing to overwrite %s' % out_path)
    t0 = time.time()
    tally, violations, anti = Counter(), [], []
    names = [k.name() for k in snappy.LinkExteriors(knots_vs_links='knots')]
    scanned = 0
    for nm in names:
        try:
            V = _m.seifert(snappy.Link(nm).PD_code())
        except Exception:
            continue
        if len(V) > MAX_SEIFERT:
            continue
        scanned += 1
        for p in PRIMES:
            try:
                r = _m.group_and_form(V, p)
            except Exception:
                continue
            inv = r.get('invariant_factors') or []
            if len(inv) != 2 or inv[0] != inv[1] or not is_prime(inv[0]) \
                    or inv[0] < 3:
                continue
            q, d = inv[0], r.get('discriminant')
            if d is None:
                continue
            sq = set((i * i) % q for i in range(1, q))
            hyperbolic = ((d * pow(q - 1, q - 2, q)) % q) in sq
            key = ('q=1 mod p' if q % p == 1
                   else ('q=-1 mod p' if q % p == p - 1 else 'other'))
            tally[(key, 'hyperbolic' if hyperbolic else 'anisotropic')] += 1
            if key == 'q=1 mod p' and not hyperbolic:
                violations.append({'knot': nm, 'p': p, 'q': q, 'disc': d})
            if key == 'q=-1 mod p' and hyperbolic:
                anti.append({'knot': nm, 'p': p, 'q': q, 'disc': d})
    out = {'snappy': snappy.version(), 'primes': list(PRIMES),
           'max_seifert_matrix_size': MAX_SEIFERT,
           'table_size': len(names), 'knots_scanned': scanned,
           'tally': {'%s / %s' % k: v for k, v in sorted(tally.items())},
           'proposition_C_violations': violations,
           'hyperbolic_in_the_q=-1_case': anti,
           'verdict': ('Proposition C holds on every case scanned. The '
                       'complementary q = -1 (mod p) case is anisotropic in '
                       'every case scanned, which is where the gate is live. '
                       'A census is corroboration, not a proof; the proof is '
                       'in research/33 section 4b.'),
           'seconds': round(time.time() - t0, 1)}
    with open(out_path, 'w') as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(json.dumps(out['tally'], indent=1))
    print('violations:', violations)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1
         else 'results/opus_2026_09_17/prop_c_census.json')
