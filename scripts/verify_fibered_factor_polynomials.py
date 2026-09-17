#!/usr/bin/env python3
"""Independent exact Seifert checks of HFK-derived Alexander polynomials.

N+1 integer evaluations prove equality of degree-at-most-N polynomials.
This does not independently verify the HFK fiberedness computation.
"""
import hashlib
import json
from pathlib import Path
import sys
import snappy
import sympy
from sagefree_slice_filter import _seifert_rows


def run(source, output):
    source, output = Path(source), Path(output)
    if output.exists():
        raise FileExistsError(output)
    data = json.loads(source.read_text())
    t = sympy.Symbol('t')
    rec = {'input_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
           'complete': False, 'checks': [], 'scope': __doc__.strip()}
    for key, row in data['factors'].items():
        if not row['eligible']:
            continue
        # Reconstruct the polynomial from integer HFK ranks, not executable text.
        coeff = {}
        for a, m, n in row['HFK']['ranks']:
            coeff[a] = coeff.get(a, 0) + n * (-1 if m % 2 else 1)
        coeff = {a: n for a, n in coeff.items() if n}
        low = min(coeff)
        poly = sympy.Poly(sum(n*t**(a-low) for a, n in coeff.items()), t)
        if poly.eval(1) == -1:
            poly = -poly
        V = sympy.Matrix(_seifert_rows(snappy.Link(row['pd'])))
        N = V.rows
        assert N % 2 == 0 and N >= poly.degree() and (N-poly.degree()) % 2 == 0
        shifted = sympy.Poly(t**((N-poly.degree())//2)*poly.as_expr(), t)
        evaluations = []
        for value in range(N+1):
            actual = int((V-value*V.T).det(method='domain-ge'))
            assert actual == shifted.eval(value), (key, value, actual, shifted.eval(value))
            evaluations.append([value, actual])
        rec['checks'].append({'factor': key, 'matrix_size': N, 'evaluations': evaluations,
                              'exact_polynomial_identity': True})
        output.write_text(json.dumps(rec, separators=(',', ':'))+'\n')
    rec['complete'] = True
    output.write_text(json.dumps(rec, separators=(',', ':'))+'\n')
    print('Exact Seifert identities checked:', len(rec['checks']), flush=True)


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2])
