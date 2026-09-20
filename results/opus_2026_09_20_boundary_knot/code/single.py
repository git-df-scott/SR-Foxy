import json, collections, time, snappy, regina
pd=[tuple(x) for x in json.load(open('L_best_ordered.json'))]
def go(slopes,label):
    L=snappy.Link(pd); T=L.exterior(with_hyperbolic_structure=False)
    T.dehn_fill(slopes); F=T.filled_triangulation()
    for _ in range(60):
        b=F.num_tetrahedra(); F.simplify()
        if F.num_tetrahedra()==b:
            F.randomize(); F.simplify()
            if F.num_tetrahedra()>=b: break
    RR=regina.Triangulation3(F._to_string())
    for _ in range(25):
        if not RR.intelligentSimplify(): break
    print(label,'tets snappy',F.num_tetrahedra(),'regina',RR.size(),flush=True)
    G=F if F.num_tetrahedra()<=RR.size() else snappy.Triangulation(RR.snapPea())
    if G.num_tetrahedra()<100:
        t0=time.time(); cs=G.covers(5)
        h=collections.Counter(str(c.homology()) for c in cs)
        print('   deg-5 covers',len(cs),'[%.1fs]'%(time.time()-t0),flush=True)
        for k,v in sorted(h.items()): print('      %d x %s'%(v,k),flush=True)
        gp=regina.Triangulation3(G._to_string()).group()
        for _ in range(6): gp.intelligentSimplify(); gp.smallCancellation()
        print('   group gens',gp.countGenerators(),'rels',gp.countRelations(),flush=True)
go([(0,0),(1,1),(1,0)],'A: +1 on a only')
go([(0,0),(-1,1),(1,0)],'B: -1 on a only')
go([(0,0),(1,0),(-1,1)],'C: -1 on b_prime only')
go([(0,0),(1,0),(1,1)],'D: +1 on b_prime only')
