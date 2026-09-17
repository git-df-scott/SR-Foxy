#!/usr/bin/env python3
"""Conditional inherited-framing calculation; NOT a geometric surgery certificate.

The stored unframed scaffold does not specify the diagonal below. This script
assumes the mirrored n=1 two-handle traces described in FRAMING_ADDENDUM.md.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

Q = ((2,1,0,0),(1,0,0,0),(0,0,-2,-1),(0,0,-1,0))

def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)

def pairing(a, b):
    return sum(a[i]*Q[i][j]*b[j] for i in range(4) for j in range(4))

def gram(a, b):
    return [[pairing(a,a),pairing(a,b)], [pairing(b,a),pairing(b,b)]]

def invariants(g):
    determinant = g[0][0]*g[1][1] - g[0][1]*g[1][0]
    divisor = math.gcd(*(x for row in g for x in row))
    require(determinant != 0 and divisor > 0, 'singular matrix outside this test')
    return determinant, [divisor, abs(determinant)//divisor]

def run():
    # A same-side Hopf block is a homology-sphere control, not a B4 proof.
    e = [tuple(int(i==j) for i in range(4)) for j in range(4)]
    require(invariants(gram(e[0],e[1])) == (-1,[1,1]), 'Hopf-block control failed')
    # Changing the framings independently can pass the homology gate.
    require(invariants([[1,0],[0,-1]]) == (-1,[1,1]), 'independent-framing control failed')
    cases = []
    for s1,s2,s3,s4 in itertools.product((-1,1),repeat=4):
        a,b = (s1,0,0,s4), (0,s2,s3,0)
        g = gram(a,b)
        d,snf = invariants(g)
        ell = s1*s2-s4*s3
        require(g == [[2,ell],[ell,-2]], 'signed closed formula failed')
        require(d in (-4,-8) and snf in ([2,2],[2,4]), 'unexpected signed homology')
        cases.append({'signs':[s1,s2,s3,s4],'matrix':g,'determinant':d,'smith_diagonal':snf})
    # Verify the mod-2 necessary condition on the exact residue classes.
    # The all-integer extension is the bilinearity proof in the addendum.
    a,b = (1,0,0,1),(0,1,1,0)
    require(all(x%2==0 for row in gram(a,b) for x in row), 'residue restriction failed')
    # Independent determinant expansion of the full four-handle matrix.
    det4 = 0
    for p in itertools.permutations(range(4)):
        sign = (-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
        det4 += sign*math.prod(Q[i][p[i]] for i in range(4))
    require(det4==1, 'full-link homology control failed')
    return {'status':'CONDITIONAL_FRAMING_GATE_NO_COUNTEREXAMPLE',
            'assumed_matrix':Q,'all_plus_matrix':gram(a,b),'signed_cases':cases,
            'case_count':len(cases),'determinant_counts':{'-4':8,'-8':8},
            'full_four_handle_determinant':det4,
            'positive_controls_passed':['same-side Hopf block','independent +1/-1 framings','full four-handle determinant'],
            'source_commit':'b7ae7270ea6abc6976c0ec598067e2cac3602887',
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'geometric_diagram_built':False,
            'limitations':['Scaffold has no surgery framings: Q is an explicitly chosen trace convention.',
              'Only the specified inherited two-handle sublink is excluded; not an arbitrary annulus modification.',
              'Additional retained/cancelled handles or changed framings require a separate calculation.',
              'Homology-sphere controls do not prove S3 or standard B4.']}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    require(not args.output.exists(),'Refusing to overwrite output')
    result=run()
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'case_count':result['case_count'],'all_plus_matrix':result['all_plus_matrix']}))

if __name__=='__main__':
    main()
