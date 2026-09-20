"""Anneal the target's filled triangulation with Regina Pachner perturbations +
intelligentSimplify, and attempt exterior_to_link (cheap budget) whenever the
tetrahedron count reaches a new low.  The controls that already succeeded needed
11 and 18 tetrahedra, so the goal is to get well under ~80."""
import json, time, random, collections, snappy, regina
best=snappy.Triangulation(open('target_best.tri').read())
bn=best.num_tetrahedra()
print('start',bn,flush=True)
def reg(T):
    R=regina.Triangulation3(T._to_string())
    for _ in range(40):
        if not R.intelligentSimplify(): break
    return R
def try_link(T,tag):
    try:
        M=snappy.Manifold(T._to_string())
        L=M.exterior_to_link(check_input=False, check_answer=False, pachner_search_tries=12, seed=0)
        M2=L.copy(); M2.simplify(mode='global')
        print(f'*** exterior_to_link SUCCEEDED at {tag}: {M2}',flush=True)
        print('    PD',M2.PD_code(KnotTheory=False),flush=True)
        json.dump([list(x) for x in M2.PD_code(KnotTheory=False)],open('K_new_pd.json','w'))
        print('    deconnect_sum ->',M2.deconnect_sum(),flush=True)
        E=M2.exterior(with_hyperbolic_structure=False)
        for _ in range(20):
            b=E.num_tetrahedra(); E.simplify()
            if E.num_tetrahedra()==b: break
        cs=E.covers(5); h=collections.Counter(str(c.homology()) for c in cs)
        print('    deg-5 covers',len(cs),' (R=9, D_{0,1}=21)',flush=True)
        for k,v in sorted(h.items()): print('       %d x %s'%(v,k),flush=True)
        return True
    except Exception as ex:
        print(f'    exterior_to_link at {tag}: {type(ex).__name__} {str(ex)[:80]}',flush=True)
        return False
rng=random.Random(1)
t0=time.time(); it=0; last_try=bn+1
while time.time()-t0<3300:
    it+=1
    R=regina.Triangulation3(best._to_string())
    # random Pachner perturbation: a few 1-4 moves then simplify
    for _ in range(rng.choice([1,2,3,5,8])):
        idx=rng.randrange(R.size())
        try: R.pachner(R.tetrahedron(idx))
        except Exception: pass
    for _ in range(40):
        if not R.intelligentSimplify(): break
    T=snappy.Triangulation(R.snapPea())
    for _ in range(15):
        b=T.num_tetrahedra(); T.simplify()
        if T.num_tetrahedra()==b: break
    n=T.num_tetrahedra()
    if n<bn:
        bn=n; best=T.copy()
        open('target_best.tri','w').write(best._to_string())
        print(f'iter {it}: new best {bn} tets [{time.time()-t0:.0f}s]',flush=True)
        if bn<=120 and bn<last_try-8:
            last_try=bn
            if try_link(best,f'{bn} tets'): break
print('done iters',it,'best',bn,flush=True)
