"""exterior_to_link on the target, retried over many seeds / Pachner budgets and
over several independently produced filled triangulations.
Controls in e2l.log already succeeded: the same call returned a 19-crossing K_1
from the genuine Abe-Tagami annulus twist and a 12-crossing 6_3 # 6_3 (which
deconnect_sum splits into two 6-crossing 6_3's) from the meridian fillings."""
import json, time, collections, random, snappy, regina
pd=[tuple(x) for x in json.load(open('L_best_ordered.json'))]
def make(seed=None):
    L=snappy.Link(pd)
    T=L.exterior(with_hyperbolic_structure=False)
    T.dehn_fill([(0,0),(1,1),(-1,1)])
    F=T.filled_triangulation()
    for _ in range(40):
        b=F.num_tetrahedra(); F.simplify()
        if F.num_tetrahedra()==b:
            F.randomize(); F.simplify()
            if F.num_tetrahedra()>=b: break
    return F
def report(L):
    M=L.copy(); M.simplify(mode='global')
    print('  LINK',M,'writhe',M.writhe(),flush=True)
    print('  PD',M.PD_code(KnotTheory=False),flush=True)
    json.dump([list(x) for x in M.PD_code(KnotTheory=False)],open('K_new_pd.json','w'))
    print('  deconnect_sum ->',M.deconnect_sum(),flush=True)
    E=M.exterior(with_hyperbolic_structure=False)
    for _ in range(20):
        b=E.num_tetrahedra(); E.simplify()
        if E.num_tetrahedra()==b: break
    print('  exterior tets',E.num_tetrahedra(),'H1',E.homology(),flush=True)
    try:
        cs=E.covers(5); h=collections.Counter(str(c.homology()) for c in cs)
        print('  deg-5 covers',len(cs),flush=True)
        for k,v in sorted(h.items()): print('     %d x %s'%(v,k),flush=True)
        print('  REFERENCE: R = 6_3#6_3 -> 9 covers ; D_{0,1} -> 21 covers',flush=True)
    except Exception as ex: print('  covers failed',ex,flush=True)
cands=[('saved219',snappy.Manifold(open('target_best.tri').read()))]
t0=time.time(); trial=0
while time.time()-t0<2400:
    trial+=1
    if cands:
        tag,T=cands.pop(0)
    else:
        F=make(); tag='fresh%d'%trial; T=snappy.Manifold(F)
    for tries in (10,40,120):
        for seed in range(3):
            try:
                L=T.exterior_to_link(check_input=False, check_answer=False,
                                     pachner_search_tries=tries, seed=seed)
                print(f'SUCCESS trial {trial} {tag} tets {T.num_tetrahedra()} tries {tries} seed {seed} [{time.time()-t0:.0f}s]',flush=True)
                report(L)
                raise SystemExit
            except SystemExit: raise
            except Exception as ex:
                pass
    print(f'trial {trial} {tag} tets {T.num_tetrahedra()}: no luck [{time.time()-t0:.0f}s]',flush=True)
print('exhausted',flush=True)
