#!/usr/bin/env python3
"""Verify four fixed cyclic-cover homology separations; standard library only.

This reconstructs a Wirtinger presentation from the supplied PD, lifts its
presentation complex to the specified cyclic cover, contracts a spanning
tree, and computes H1 over F_p by exact row reduction. It does NOT certify
sliceness, nonribbonness, or every computation in the larger checkpoint audit.
"""
from collections import defaultdict
from pathlib import Path
import argparse, copy, json

def need(condition, message):
    if not condition:
        raise ValueError(message)

def first_betti(pd, degree=4, prime=5):
    need(degree >= 1 and prime == 5, 'This checker is calibrated for F_5')
    occurrences = defaultdict(list)
    for crossing, row in enumerate(pd):
        need(len(row) == 4, 'Crossing must have four ports')
        for port, label in enumerate(row):
            occurrences[label].append((crossing, port))
    need(bool(pd) and all(len(x) == 2 for x in occurrences.values()),
         'Every PD edge must occur exactly twice')
    edges = {}
    for a, b in occurrences.values():
        edges[a], edges[b] = b, a
    arcs = {}
    generators = 0
    for start in sorted(edges):
        if start in arcs:
            continue
        generators += 1
        stack = [start]
        while stack:
            x = stack.pop()
            if x in arcs:
                continue
            arcs[x] = generators
            stack.append(edges[x])
            c, p = x
            if p % 2:
                stack.append((c, (p + 2) % 4))
    incoming = set()
    start = min(edges)
    x = start
    while x not in incoming:
        incoming.add(x)
        c, p = x
        x = edges[c, (p + 2) % 4]
    need(x == start and len(incoming) == 2 * len(pd), 'Expected one knot')
    relators = []
    for c in range(len(pd)):
        inc = {p for p in range(4) if (c, p) in incoming}
        need(inc in ({0, 1}, {0, 3}, {1, 2}, {2, 3}), 'Invalid orientation')
        u = 0 if (c, 0) in incoming else 2
        o = 1 if (c, 1) in incoming else 3
        sign = 1 if (u - o) % 4 == 1 else -1
        over = arcs[c, 1]
        relators.append([-sign * over, arcs[c, u], sign * over,
                         -arcs[c, (u + 2) % 4]])
    # The reference meridian's first degree-1 lifted edges form a tree.
    columns = [(s, g) for s in range(degree) for g in range(generators)
               if g != 0 or s == degree - 1]
    index = {edge: i for i, edge in enumerate(columns)}
    matrix = []
    for s in range(degree):
        for word in relators:
            level = s
            row = [0] * len(columns)
            for letter in word:
                if letter < 0:
                    level = (level - 1) % degree
                edge = (level, abs(letter) - 1)
                if edge in index:
                    row[index[edge]] += 1 if letter > 0 else -1
                if letter > 0:
                    level = (level + 1) % degree
            need(level == s, 'Lifted relation is not closed')
            matrix.append([v % prime for v in row])
    rank = 0
    for column in range(len(columns)):
        pivot = next((i for i in range(rank, len(matrix))
                      if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, prime)
        matrix[rank] = [(v * inverse) % prime for v in matrix[rank]]
        for i in range(rank + 1, len(matrix)):
            multiple = matrix[i][column]
            if multiple:
                matrix[i] = [(a - multiple * b) % prime
                             for a, b in zip(matrix[i], matrix[rank])]
        rank += 1
        if rank == len(matrix):
            break
    return len(columns) - rank

def verify(data):
    results = {}
    for witness in data['witnesses']:
        actual = first_betti(witness['pd'], witness['degree'], witness['prime'])
        need(actual == witness['expected_first_betti'], 'Betti number mismatch')
        results[witness['node']] = actual
    for left, right in data['pairs']:
        need(results[left] != results[right], 'Pair not separated')
    return results

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='?', type=Path,
                        default=Path(__file__).with_name('CYCLIC4_WITNESSES.json'))
    args = parser.parse_args()
    data = json.loads(args.input.read_text())
    results = verify(data)
    rejected = 0
    for index in range(len(data['witnesses'])):
        for mode in ('edge', 'expected_rank'):
            bad = copy.deepcopy(data)
            if mode == 'edge':
                bad['witnesses'][index]['pd'][0][0] = 999999
            else:
                bad['witnesses'][index]['expected_first_betti'] += 1
            try:
                verify(bad)
            except ValueError:
                rejected += 1
            else:
                raise ValueError('Corrupt witness accepted')
    print(json.dumps({'status': 'PASS', 'mod5_betti': results,
                      'corrupt_witnesses_rejected': rejected,
                      'counterexample_established': False}, indent=2))

if __name__ == '__main__':
    main()
