"""Try many independently simplified diagrams of the ordered surgery link; for each,
fill (1,1)/(-1,1), retriangulate, simplify, and record the tetrahedron count.
Whenever a filled triangulation gets small enough, compute the degree-5 cover
census (the discriminator: R -> 9 covers, D_{0,1} -> 21)."""
import json, time, collections, random, snappy, regina, spherogram
import gaussbuild as GB, track
dg,gw0,uc,oc=track.load()
L0=GB.build_link(gw0)
def unan(Mx):
    out=[]
    for comp in Mx.link_components:
        v=collections.Counter()
        for ep in comp:
            c=ep.crossing
            if c.label in uc: v[uc[c.label] if ep.strand_index==0 else oc[c.label]]+=1
        out.append(v)
    return out
def ordered(M):
    u=unan(M)
    if not all(len(d)==1 for d in u): return None
    ids=[list(d)[0] for d in u]
    order=[None]*3
    for j,oi in enumerate(ids): order[oi]=j
    track.reorder(M,order)
    return M
best=(10**9,None)
t0=time.time()
trial=0
while time.time()-t0<2400:
    trial+=1
    M=L0.copy()
    M.simplify(mode='global')
    if trial>1:
        M.backtrack(steps=random.choice([10,25,50,80]))
        M.simplify(mode='global')
    M=ordered(M)
    if M is None: continue
    nc=len(M.crossings)
    T=M.exterior(with_hyperbolic_structure=False)
    T.dehn_fill([(0,0),(1,1),(-1,1)])
    F=T.filled_triangulation()
    for _ in range(25):
        b=F.num_tetrahedra(); F.simplify()
        if F.num_tetrahedra()==b:
            F.randomize(); F.simplify()
            if F.num_tetrahedra()>=b: break
    RR=regina.Triangulation3(F._to_string())
    for _ in range(25):
        if not RR.intelligentSimplify(): break
    n=min(F.num_tetrahedra(),RR.size())
    if n<best[0]:
        best=(n,F.copy() if F.num_tetrahedra()<=RR.size() else snappy.Triangulation(RR.snapPea()))
        print(f'trial {trial}: {nc} crossings -> filled {n} tets  [{time.time()-t0:.0f}s]',flush=True)
        open('best_filled.tri','w').write(best[1]._to_string())
        if n<=60:
            try:
                cs=best[1].covers(5)
                h=collections.Counter(str(c.homology()) for c in cs)
                print('   *** deg-5 covers:',len(cs),dict(h),flush=True)
            except Exception as e:
                print('   covers failed',e,flush=True)
print('trials',trial,'best',best[0],flush=True)
