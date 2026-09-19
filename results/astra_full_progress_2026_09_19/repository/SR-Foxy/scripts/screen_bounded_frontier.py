#!/usr/bin/env python3
"""Replay saved bands and apply exact necessary Alexander-rank obstructions.

For an m-component slice link, the generic Alexander-module rank is m-1.
A specialization has rank at most the generic Fox rank; thus specialized
H1 dimension below m-1 proves an obstruction. Other cases remain UNKNOWN.
Source: Cochran--Harvey, Homology and derived series of groups, GT9 (2005),
Cor.3.3 and the paragraph following its proof, pp.2169-2170.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import snappy
import sympy
from spherogram.links.bands.core import add_one_band
from colored_link_rank import check, fox_matrix, ribbon_control
from bounded_ribbon_search import digest, save


def verify_minor(link, certificate):
    rows, colors = fox_matrix(link, certificate['component_values'], certificate['prime'])
    minor = sympy.Matrix([[rows[i][j] for j in certificate['minor_columns']]
                         for i in certificate['minor_rows']])
    assert int(minor.det(method='domain-ge')) % certificate['prime'] == certificate['minor_determinant_mod_prime']


def controls():
    knot = snappy.Link('6_3').PD_code()
    n = 2 * len(knot)
    split = snappy.Link(knot + [(n, n+1, n+1, n)])
    whitehead = snappy.Link('L5a1')
    ribbon, provenance = ribbon_control()
    output = {}
    for label, link, expected in [('split_knot_unknot', split, 1),
                                   ('whitehead', whitehead, 0),
                                   ('nonsplit_ribbon_concordance', ribbon, 1)]:
        c = check(link, [2, 3], 101)
        assert c['specialized_H1_dimension'] == expected
        verify_minor(link, c)
        output[label] = c
    output['nonsplit_control_provenance'] = provenance
    return output


def run(directory, output):
    output = Path(output)
    if output.exists():
        raise FileExistsError(output)
    rec = {'controls': controls(), 'source': 'https://math.rice.edu/~shelly/publications/Stallings.pdf',
           'inputs': {}, 'rows': [], 'counts': Counter(), 'complete': False,
           'scope': 'Obstructions only to ribbon completion of these fixed fission prefixes. '
                    'No conclusion about D01 sliceness or unsearched movies.'}
    cache = {}
    for path in sorted(Path(directory).glob('job-*-attempt-*.json')):
        data = json.loads(path.read_text())
        rec['inputs'][str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
        parent = snappy.Link(data['prefix'][-1])
        for index, row in enumerate(data['frontier']):
            raw = add_one_band(parent, row['band'])
            assert raw.PD_code() == [tuple(c) for c in row['raw_pd']]
            assert len(raw.link_components) == row['raw_components']
            rec['counts']['raw_band_replays'] += 1
            pd = row['endpoint_pd']
            key = digest(pd)
            if key not in cache:
                link = snappy.Link(pd)
                m = len(link.link_components)
                checks, error = [], None
                if m > 1:
                    try:
                        for values, prime in [([2]*m, 101), (list(range(2, 2+m)), 103)]:
                            c = check(link, values, prime)
                            checks.append(c)
                            if c['specialized_H1_dimension'] < m-1:
                                verify_minor(link, c)
                                break
                    except Exception as e:
                        error = repr(e)
                cache[key] = {'components': m, 'checks': checks, 'error_unknown': error,
                              'obstructed': error is None and any(c['specialized_H1_dimension'] < m-1 for c in checks)}
            test = cache[key]
            rec['rows'].append({'source': str(path), 'index': index, 'label': data['label'],
                                'endpoint_sha256': key, **test})
            rec['counts']['obstructed' if test['obstructed'] else 'retained_unknown'] += 1
        save(output, rec)
    rec['complete'] = True
    rec['counts']['unique_endpoint_diagrams'] = len(cache)
    save(output, rec)
    print(json.dumps(rec['counts']), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory')
    parser.add_argument('output')
    args = parser.parse_args()
    run(args.directory, args.output)
