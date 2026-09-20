"""Persistent randomised simplification of the TARGET filled triangulation.
If K_new were a small knot (R: 17 tets, D_{0,1}: ~20) this should find it."""
import json, time, snappy, regina
pd=json.load(open('L_best_ordered.json'))
L=snappy.Link([tuple(x) for x in pd])
T=L.exterior(with_hyperbolic_structure=False)
T.dehn_fill([(0,0),(1,1),(-1,1)])
F=T.filled_triangulation()
print('start',F.num_tetrahedra(),flush=True)
best=F.copy(); bn=F.num_tetrahedra()
t0=time.time()
rounds=0
while time.time()-t0<2400:
    rounds+=1
    C=best.copy()
    C.randomize()
    for _ in range(30):
        b=C.num_tetrahedra(); C.simplify()
        if C.num_tetrahedra()==b: break
    # also let Regina try
    RR=regina.Triangulation3(C._to_string())
    for _ in range(20):
        if not RR.intelligentSimplify(): break
    n=min(C.num_tetrahedra(), RR.size())
    if n<bn:
        bn=n
        best = C if C.num_tetrahedra()<=RR.size() else snappy.Triangulation(RR.snapPea())
        print(f'round {rounds}: new best {bn} tets  [{time.time()-t0:.0f}s]',flush=True)
        open('target_best.tri','w').write(best._to_string())
print('rounds',rounds,'best',bn,flush=True)
open('target_best.tri','w').write(best._to_string())
