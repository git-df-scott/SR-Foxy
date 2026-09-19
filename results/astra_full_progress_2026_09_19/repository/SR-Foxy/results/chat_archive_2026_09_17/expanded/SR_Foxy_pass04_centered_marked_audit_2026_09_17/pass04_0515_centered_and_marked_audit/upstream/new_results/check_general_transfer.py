#!/usr/bin/env python3
"""Exact finite checks for the proposed ALL-DEGREE transfer proof.

These verify algebra through a finite degree. The unbounded result depends on
PROPOSED_TRANSFER_THEOREM.md, not on extrapolation from this computation.
Only Python standard library; no knot software and no numerical arithmetic.
"""
from __future__ import annotations
import argparse, hashlib, json, math, time
from fractions import Fraction as Q
from pathlib import Path


def chebyshev(n: int) -> list[list[int]]:
    out = [[1]]
    if n:
        out.append([0, 1])
    for r in range(2, n + 1):
        a = [0] + out[-1]
        for j, c in enumerate(out[-2]):
            a[j] -= c
        out.append(a)
    return out


def inverse_series(a: list[Q], n: int) -> list[Q]:
    if not a or not a[0]:
        raise ValueError('Series must have nonzero constant')
    b = [1 / a[0]]
    for k in range(1, n + 1):
        b.append(-sum((a[j] * b[k-j] for j in range(1, min(k, len(a)-1)+1)), Q(0)) / a[0])
    return b


def mu(n: int, r: int) -> int:
    k = (n-r)//2
    return math.comb(n,k) - (math.comb(n,k-1) if k else 0)


def egf_coefficient(n: int, j: int, k: int, sec: list[Q], inv_sinc: list[Q]) -> Q:
    eps = n % 2
    d = n-j-k+eps
    if d < 0 or d % 2:
        return Q(0)
    sign = (-1)**(d//2)
    return sign * Q(math.factorial(n), math.factorial(j)*math.factorial(k)) * (inv_sinc if eps else sec)[d]


def apply_law(n: int, left: list[Q], right: list[Q], sec: list[Q], inv_sinc: list[Q]) -> Q:
    return sum((egf_coefficient(n,j,k,sec,inv_sinc)*left[j]*right[k]
                for j in range(n%2,n+1,2) for k in range(n%2,n+1,2)),Q(0))


def mod32(a: Q) -> int:
    if a.denominator % 2 == 0:
        raise ValueError('Even denominator cannot be inverted modulo 32')
    return a.numerator * pow(a.denominator,-1,32) % 32


def det(matrix: list[list[Q]]) -> Q:
    a = [list(map(Q,row)) for row in matrix]
    answer = Q(1)
    for i in range(len(a)):
        pivot = next((r for r in range(i,len(a)) if a[r][i]),None)
        if pivot is None:
            return Q(0)
        if pivot != i:
            a[pivot],a[i]=a[i],a[pivot];answer=-answer
        value=a[i][i];answer*=value
        for r in range(i+1,len(a)):
            t=a[r][i]/value
            for c in range(i,len(a)):
                a[r][c]-=t*a[i][c]
    return answer


def as_str(q: Q) -> str:
    return str(q.numerator) if q.denominator==1 else str(q)


def verify(max_n: int) -> dict:
    S=chebyshev(max_n)
    cos=[Q((-1)**(j//2),math.factorial(j)) if j%2==0 else Q(0) for j in range(max_n+1)]
    sinc=[Q((-1)**(j//2),math.factorial(j+1)) if j%2==0 else Q(0) for j in range(max_n+1)]
    sec=inverse_series(cos,max_n);inv_sinc=inverse_series(sinc,max_n)
    inv={r:inverse_series([Q(x) for x in S[r][r%2:]],max_n+1) for r in range(max_n+1)}
    checks={'chebyshev_decomposition':0,'kernel_lower_coefficient_zeros':0,
            'kernel_vs_egf_leading_coefficients':0,'two_integral_law_coefficients':0,
            'scalar_mod32_controls':0,'unit_and_diagonal_checks':0,
            'ribbon_family_vandermonde_checks':0,'negative_controls':0}
    low_laws={}
    for n in range(1,max_n+1):
        eps=n%2;rr=list(range(eps,n+1,2))
        for j in range(n+1):
            value=sum(mu(n,r)*(S[r][j] if j<=r else 0) for r in rr)
            if value!=int(j==n):raise AssertionError(('decomposition',n,j,value))
            checks['chebyshev_decomposition']+=1
        terms=[]
        for j in rr:
            for k in rr:
                # Q_njk(t)=t^(j+k) sum_r mu*c_rj*c_rk/S_r(t).
                # Rational series division is independent of the EGF formula.
                for power in range(eps,n):
                    index=power-j-k+eps
                    if index<0:continue
                    value=sum((Q(mu(n,r)*S[r][j]*S[r][k])*inv[r][index]
                               for r in rr if r>=max(j,k)),Q(0))
                    if value:raise AssertionError(('lower coefficient',n,j,k,power,value))
                    checks['kernel_lower_coefficient_zeros']+=1
                index=n-j-k+eps
                value=(sum((Q(mu(n,r)*S[r][j]*S[r][k])*inv[r][index]
                            for r in rr if r>=max(j,k)),Q(0)) if index>=0 else Q(0))
                expected=egf_coefficient(n,j,k,sec,inv_sinc)
                if value!=expected:raise AssertionError(('EGF mismatch',n,j,k,value,expected))
                checks['kernel_vs_egf_leading_coefficients']+=1
                if value.denominator%2==0:raise AssertionError(('even denominator',n,j,k,value))
                checks['two_integral_law_coefficients']+=1
                if value and n<=8:terms.append([j,k,as_str(value)])
        low_laws[str(n)]=terms if n<=8 else []
        synthetic=[Q(1)]+[Q(7*j+2) for j in range(1,n+1)]
        unit=[Q(1)]*(n+1)
        if apply_law(n,synthetic,unit,sec,inv_sinc)!=synthetic[n]:raise AssertionError('unit')
        if egf_coefficient(n,n,eps,sec,inv_sinc)!=1:raise AssertionError('diagonal')
        checks['unit_and_diagonal_checks']+=2
        for d in (1,9,17,25):
            for e in (1,9,17,25):
                ans=apply_law(n,[Q(d**j) for j in range(n+1)],[Q(e**j) for j in range(n+1)],sec,inv_sinc)
                if mod32(ans)!=(d*e)**n%32:raise AssertionError(('scalar congruence',n,d,e))
                checks['scalar_mod32_controls']+=1
        # Perturbing e_n by 1 must be detected with odd determinant 9.
        left=[Q(25**j) for j in range(n+1)]; right=[Q(9**j) for j in range(n+1)]
        a=apply_law(n,left,right,sec,inv_sinc);left[n]+=1
        b=apply_law(n,left,right,sec,inv_sinc)
        if mod32(b-a)!=(9 if eps else 1):raise AssertionError('mutation not detected')
        checks['negative_controls']+=1
    # Denominator-integrality is NOT automatic for rational arithmetic.
    try:mod32(Q(1,2))
    except ValueError:checks['negative_controls']+=1
    else:raise AssertionError('illegal mod-32 division accepted')
    if mod32(apply_law(2,[Q(1),Q(2),Q(4)],[Q(1),Q(2),Q(4)],sec,inv_sinc))==16:
        raise AssertionError('noneligible determinant control not rejected')
    checks['negative_controls']+=1
    # Varying higher seed values tests that the Vandermonde depends only on
    # e2-1 (even) or e3/e1-1 (odd). Unspecified values are synthetic, not knots.
    matrices=[]
    max_q=min(5,(max_n-1)//2)
    for eps in (0,1):
        for q in range(1,max_q+1):
            degree=2*q+eps
            for fixture in (0,1):
                seed=[Q(1)]+[Q(9**j + fixture*101*j) for j in range(1,degree+1)]
                seed[1]=Q(9)
                if degree>=2:seed[2]=Q(49)
                if degree>=3:seed[3]=Q(1785)
                if degree>=4:seed[4]=Q(19681)
                seq=[[Q(1)]*(degree+1)]
                for p in range(q):
                    seq.append([Q(1)]+[apply_law(n,seq[-1],seed,sec,inv_sinc) for n in range(1,degree+1)])
                mat=[[seq[p][2*a+eps] for a in range(q+1)] for p in range(q+1)]
                leading=[]
                for a in range(q+1):
                    if eps:
                        leading.append(Q(math.factorial(2*a+1),6**a*math.factorial(a))*(seed[3]/seed[1]-1)**a)
                    else:
                        leading.append(Q(math.factorial(2*a),2**a*math.factorial(a))*(seed[2]-1)**a)
                expected=math.prod(leading)*math.prod(Q(j-i) for i in range(q+1) for j in range(i+1,q+1))
                if eps:expected*=seed[1]**(q*(q+1)//2)
                got=det(mat)
                if got!=expected or not got:raise AssertionError(('Vandermonde',eps,q,got,expected))
                checks['ribbon_family_vandermonde_checks']+=1
                matrices.append({'parity':eps,'N':q,'fixture':fixture,'determinant':as_str(got),'expected_matches':True})
    # Known low control values; these predictions will also be tested by a
    # direct cabled-diagram state sum, not silently called computed knots.
    base=[Q(1),Q(9),Q(49),Q(1785),Q(19681)]
    predictions={str(n):as_str(apply_law(n,base,base,sec,inv_sinc)) for n in range(1,5)}
    return {'status':'FINITE_EXACT_ALGEBRA_CHECKS_PASSED','counterexample_found':False,
            'max_parallel_degree_checked':max_n,'checks':checks,'total_checks':sum(checks.values()),
            'leading_laws_j_k_coefficient':{k:v for k,v in low_laws.items() if v},
            'ribbon_connected_sum_predictions':predictions,'vandermonde_fixtures':matrices,
            'limitations':['Finite-degree arithmetic does not prove the all-degree claims.',
            'Higher seed values in Vandermonde tests are synthetic, not computed knot invariants.',
            'No new CE or disk is supplied; use the accompanying written proof and audit its hypotheses.']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--degree',type=int,default=20)
    args=parser.parse_args()
    if args.degree<4 or args.degree>32:parser.error('degree must be 4..32')
    if args.output.exists():parser.error('refusing overwrite')
    start=time.monotonic();report=verify(args.degree)
    report['seconds']=time.monotonic()-start
    report['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','max_parallel_degree_checked','checks','total_checks','seconds','ribbon_connected_sum_predictions')},indent=2))
if __name__=='__main__':main()
