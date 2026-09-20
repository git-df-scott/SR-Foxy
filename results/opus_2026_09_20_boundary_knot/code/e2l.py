"""Most direct route: Dunfield-Obeidin-Rudd exterior_to_link on the filled
1-cusped target, to obtain an ordinary diagram of K_new.
Controls first: the same call on the meridian-filled surgery link must return a
diagram of R = 6_3 # 6_3, and on the Abe-Tagami annulus twist a diagram of K_1."""
import json, time, collections, snappy, regina
def show(L,label):
    print(f'{label}: {L}  writhe {L.writhe()}',flush=True)
    M=L.copy(); M.simplify(mode='global')
    print(f'   simplified: {M}',flush=True)
    print(f'   PD: {M.PD_code(KnotTheory=False)}',flush=True)
    E=M.exterior(with_hyperbolic_structure=False)
    for _ in range(20):
        b=E.num_tetrahedra(); E.simplify()
        if E.num_tetrahedra()==b: break
    try:
        cs=E.covers(5); h=collections.Counter(str(c.homology()) for c in cs)
        print(f'   deg-5 covers {len(cs)}',flush=True)
        for k,v in sorted(h.items()): print(f'      {v} x {k}',flush=True)
    except Exception as ex: print('   covers failed',ex,flush=True)
    try:
        S=M.deconnect_sum(); print('   deconnect_sum ->',S,flush=True)
    except Exception as ex: print('   deconnect failed',ex,flush=True)
    return M
def build(pd,slopes,label):
    L=snappy.Link([tuple(x) for x in pd])
    T=L.exterior(with_hyperbolic_structure=False)
    T.dehn_fill(slopes)
    F=T.filled_triangulation()
    for _ in range(60):
        b=F.num_tetrahedra(); F.simplify()
        if F.num_tetrahedra()==b:
            F.randomize(); F.simplify()
            if F.num_tetrahedra()>=b: break
    print(f'{label}: filled triangulation {F.num_tetrahedra()} tets',flush=True)
    return F
DATA='/home/user/SR-Foxy/data/knots/'
at=json.load(open(DATA+'AbeTagami_L_63_c1_c2.json'))['pd_code_snappy_0indexed']
pd=json.load(open('L_best_ordered.json'))
for F,label in [(build(at,[(0,0),(2,1),(0,1)],'CTRL AT twist (expect K_1)'),'CTRL K_1'),
                (build(pd,[(0,0),(1,0),(1,0)],'CTRL SURG meridian (expect R)'),'CTRL R')]:
    t0=time.time()
    try:
        L=snappy.Manifold(F).exterior_to_link(check_input=False, check_answer=False, verbose=False)
        print(f'   exterior_to_link ok [{time.time()-t0:.0f}s]',flush=True)
        show(L,label)
    except Exception as ex:
        print(f'   {label} exterior_to_link FAILED after {time.time()-t0:.0f}s: {ex}',flush=True)
# the target: use the best triangulation found earlier
T=snappy.Manifold(open('target_best.tri').read())
print('TARGET triangulation',T.num_tetrahedra(),'cusps',T.num_cusps(),flush=True)
t0=time.time()
try:
    L=T.exterior_to_link(check_input=False, check_answer=False, verbose=True)
    print(f'TARGET exterior_to_link ok [{time.time()-t0:.0f}s]',flush=True)
    M=show(L,'TARGET K_new')
    json.dump([list(x) for x in M.PD_code(KnotTheory=False)],open('K_new_pd.json','w'))
except Exception as ex:
    print(f'TARGET exterior_to_link FAILED after {time.time()-t0:.0f}s: {ex}',flush=True)
