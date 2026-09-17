#!/usr/bin/env python3
"""Independent cleared-denominator audit of the corrected Chebyshev proof.

No prior checker is imported. Integer polynomial products clear every S_r
before reading exact orders at t=0. This differs from the prior reciprocal-
series check. Finite checks do not replace the centered-polynomial proof.
"""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import argparse, hashlib, json, time

def trim(a):
    while len(a)>1 and a[-1]==0:a.pop()
    return a

def add(a,b):
    c=[0]*max(len(a),len(b))
    for i,x in enumerate(a):c[i]+=x
    for i,x in enumerate(b):c[i]+=x
    return trim(c)

def scale(a,c):return [x*c for x in a]
def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):c[i+j]+=x*y
    return trim(c)
def valuation(a):return next((i for i,x in enumerate(a) if x),None)
def cheb(n):
    C=[[1],[0,1]]
    for i in range(2,n+1):C.append(add([0]+C[-1],scale(C[-2],-1)))
    return C

def weight(n,r):
    k=(n-r)//2
    return comb(n,k)-(comb(n,k-1) if k else 0)

def moment(n,power,shift):
    eps=n%2
    return sum(weight(n,r)*(-1)**((r-eps)//2)*(r+shift)**power for r in range(eps,n+1,2))

def reciprocal(a,n):
    c=[1/a[0]]
    for i in range(1,n+1):c.append(-sum((a[k]*c[i-k] for k in range(1,i+1)),F(0))/a[0])
    return c

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--degree',type=int,default=20)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args()
    if a.degree<3 or a.degree>24:ap.error('degree must be 3..24')
    if a.output.exists():ap.error('refusing overwrite')
    start=time.monotonic();N=a.degree;C=cheb(N)
    sec=reciprocal([F((-1)**(i//2),factorial(i)) if i%2==0 else F(0) for i in range(N+1)],N)
    sinc=reciprocal([F((-1)**(i//2),factorial(i+1)) if i%2==0 else F(0) for i in range(N+1)],N)
    counts={'centered_moments':0,'lower_centered_moments':0,'cleared_denominator_orders':0,'leading_coefficient_comparisons':0,'odd_denominator_checks':0,'deliberate_wrong_shift_rejections':0}
    errors=[];low=[]
    for n in range(1,N+1):
        eps=n%2;rr=list(range(eps,n+1,2))
        expect=(-1)**((n-eps)//2)*2**n*factorial(n)
        centered=moment(n,n,1);old=moment(n,n,0)
        if centered!=expect:raise RuntimeError(('CENTERED_IDENTITY_FAILED',n,centered,expect))
        counts['centered_moments']+=1
        if n in (1,2):
            if old==expect:raise RuntimeError('The wrong-shift counterfixture failed')
            counts['deliberate_wrong_shift_rejections']+=1
        errors.append({'n':n,'old_L_r_power':old,'correct_L_centered_power':centered,'claimed_formula':expect,'old_formula_matches':old==expect})
        for k in range(eps,n,2):
            if moment(n,k,1):raise RuntimeError(('LOWER_CENTERED_MOMENT',n,k))
            counts['lower_centered_moments']+=1
        pref=[[1]]
        for r in rr:pref.append(mul(pref[-1],C[r]))
        suff=[[1] for _ in range(len(rr)+1)]
        for i in reversed(range(len(rr))):suff[i]=mul(C[rr[i]],suff[i+1])
        den=pref[-1];vden=valuation(den)
        other=[mul(pref[i],suff[i+1]) for i in range(len(rr))]
        for j in rr:
            for k in rr:
                numerator=[0]
                for i,r in enumerate(rr):
                    if j<=r and k<=r:numerator=add(numerator,scale(other[i],weight(n,r)*C[r][j]*C[r][k]))
                numerator=[0]*(j+k)+numerator
                vn=valuation(numerator)
                if vn is not None and vn-vden<n:raise RuntimeError(('FILTERED_ORDER_FAILED',n,j,k,vn,vden))
                counts['cleared_denominator_orders']+=1
                lead=F(numerator[n+vden],den[vden]) if n+vden<len(numerator) else F(0)
                d=n-j-k+eps
                formula=F(0) if d<0 or d%2 else F((-1)**(d//2)*factorial(n),factorial(j)*factorial(k))*(sinc if eps else sec)[d]
                if lead!=formula:raise RuntimeError(('LEADING_LAW_FAILED',n,j,k,lead,formula))
                counts['leading_coefficient_comparisons']+=1
                if lead.denominator%2==0:raise RuntimeError(('ILLEGAL_EVEN_DENOMINATOR',n,j,k,lead))
                counts['odd_denominator_checks']+=1
                if n<=4 and lead:low.append({'n':n,'j':j,'k':k,'coefficient':str(lead)})
    out={'status':'CORRECTED_IDENTITY_AND_KERNEL_CHECKS_PASS','counterexample_found':False,'degree':N,'method':'cleared denominator integer polynomials, not reciprocal-series kernel evaluation','counts':counts,'total_checks':sum(counts.values()),'wrong_shift_counterexamples':errors,'low_law_terms':low,'seconds':time.monotonic()-start,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'The false identity in the original draft is detected. The corrected centered identity and derived laws pass these finite checks. The written all-degree proof is a separate argument, not an extrapolation.'}
    a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','degree','counts','total_checks','seconds')},indent=2))
    print(json.dumps(errors[:3],indent=2))
if __name__=='__main__':main()
