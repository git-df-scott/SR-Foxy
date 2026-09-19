#!/usr/bin/env python3
"""Exact arithmetic checks for the crossed-band genus/handle gate.

No topology library is required. This does NOT construct an annulus.
It checks the Euler-characteristic bookkeeping and the conditional framed
linking matrices recorded in the accompanying README.
"""
import itertools
import json
from pathlib import Path

Q = [
    [ 2, 1, 0, 0],
    [ 1, 0, 0, 0],
    [ 0, 0,-2,-1],
    [ 0, 0,-1, 0],
]
# Columns are four genuinely mixed integral handle classes.
M = [
    [0,  2, 0,-1],
    [1, -2, 1, 1],
    [0,  1, 0,-1],
    [1, -1, 2, 1],
]
H2 = [
    [0,1,0,0],
    [1,0,0,0],
    [0,0,0,1],
    [0,0,1,0],
]
# Naive cross-pair classes e1+e4, e2+e3.
V = [
    [1,0],
    [0,1],
    [0,1],
    [1,0],
]

def transpose(A):
    return [list(x) for x in zip(*A)]

def mm(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]

def det(A):
    n=len(A)
    total=0
    for p in itertools.permutations(range(n)):
        inv=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        term=1
        for i,j in enumerate(p):
            term*=A[i][j]
        total += (-1 if inv%2 else 1)*term
    return total

checks = {}
# Two annuli: chi=0, b=4, components=2.
# First oriented boundary 1-handle joins distinct components: chi=-1,b=3,c=1.
# Second joins two distinct remaining boundary components in that same surface:
# chi=-2,b=2,c=1. For an orientable connected surface,
# chi = 2-2g-b, hence g=1.
chi0,b0,c0=0,4,2
chi1,b1,c1=chi0-1,b0-1,1
chi2,b2,c2=chi1-1,b1-1,1
g2=(2-b2-chi2)//2
checks["crossed_oriented_surface"]={
    "start":{"chi":chi0,"boundary":b0,"components":c0},
    "after_first_band":{"chi":chi1,"boundary":b1,"components":c1},
    "after_second_band":{"chi":chi2,"boundary":b2,"components":c2},
    "genus":g2,
    "is_annulus": (chi2==0 and b2==2 and g2==0),
}
assert (chi1,b1,c1)==(-1,3,1)
assert (chi2,b2,c2,g2)==(-2,2,1,1)

cross = mm(mm(transpose(V),Q),V)
mixed = mm(mm(transpose(M),Q),M)
checks["conditional_framing"]={
    "Q_det":det(Q),
    "naive_cross_pair_gram":cross,
    "naive_cross_pair_det":det(cross),
    "mixed_basis_det":det(M),
    "mixed_basis_gram":mixed,
    "target_hyperbolic_form":H2,
}
assert det(Q)==1
assert cross==[[2,0],[0,-2]]
assert abs(det(M))==1
assert mixed==H2
# Every mixed basis vector has nonzero support in both upper (coords 0,1)
# and lower (coords 2,3) halves.
cols=transpose(M)
assert all(any(v[i] for i in (0,1)) and any(v[i] for i in (2,3)) for v in cols)

checks["pure_four_two_handlebody"]={
    "two_handles":4,
    "one_handles":0,
    "three_handles_assumed":0,
    "H2_rank":4,
    "can_be_B4_without_additional_handle_cancellation":False,
}
# This is cellular handle-chain bookkeeping: C2=Z^4 -> C1=0.
assert checks["pure_four_two_handlebody"]["H2_rank"]==4

result={
    "status":"PASS_NO_COUNTEREXAMPLE",
    "claim":"The canonical crossed double boundary-banding of the two product annuli is genus one, not an annulus. Under the separately stated conditional framing hypothesis, the naive two-handle shortcut also fails, while a full mixed unimodular hyperbolic basis exists; integral framing alone therefore does not supply the missing compression or ambient-standardness.",
    "checks":checks,
}
print(json.dumps(result,indent=2))
if __name__=="__main__":
    Path("RESULTS.generated.json").write_text(json.dumps(result,indent=2)+"\n")
