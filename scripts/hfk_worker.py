#!/usr/bin/env python3
"""One isolated HFK calculation; callers impose a hard process timeout."""
import json
import sys
import knot_floer_homology


def validate_hfk(h):
    """Reject internally inconsistent library output before any obstruction."""
    ranks = h['ranks']
    if sum(ranks.values()) != h['total_rank']:
        raise ValueError('HFK total rank disagrees with graded ranks')
    if any(n <= 0 or int(n) != n for n in ranks.values()):
        raise ValueError('HFK has invalid graded dimensions')
    if sum(n * (-1 if m % 2 else 1) for (a, m), n in ranks.items()) != 1:
        raise ValueError('HFK Euler polynomial is not normalized at 1')
    if ranks != {(-a, m-2*a): n for (a, m), n in ranks.items()}:
        raise ValueError('HFK grading symmetry failed')
    return h


if __name__=='__main__':
    # The direct PD API avoids importing the full topology stack per case.
    h=validate_hfk(knot_floer_homology.pd_to_hfk(json.load(sys.stdin)))
    print(json.dumps({'ranks':[[a,m,n] for (a,m),n in sorted(h['ranks'].items())],
                      'total_rank':h['total_rank'],'fibered':h['fibered'],
                      'seifert_genus':h['seifert_genus'],'tau':h['tau']}))
