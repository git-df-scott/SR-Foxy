"""Route 8: staged filling with retriangulation + simplification between the two
Dehn fillings (SnapPy preserves cusp peripheral framings under simplify), then
Regina for the group presentation, then total #Hom(., A5)."""
import json, time, collections, snappy, regina
import homcount as H
A5=H.alt(5)
def total_homs(ngens, rels, G=A5):
    mul,inv,e=G.mul,G.inv,G.e
    byk=collections.defaultdict(list)
    for R in rels: byk[max((abs(x) for x in R),default=1)].append(R)
    def ev(w,val):
        r=e
        for x in w:
            v=val[abs(x)-1]; r=mul[r][v if x>0 else inv[v]]
        return r
    tot=0
    def rec(k,val):
        nonlocal tot
        if k>ngens: tot+=1; return
        for v in range(G.n):
            val.append(v)
            if all(ev(R,val)==e for R in byk[k]): rec(k+1,val)
            val.pop()
    rec(1,[]); return tot
def words_of(gp):
    out=[]
    for i in range(gp.countRelations()):
        w=gp.relation(i); word=[]
        for j in range(w.countTerms()):
            tm=w.term(j); word += [ (tm.generator+1) if tm.exponent>0 else -(tm.generator+1) ]*abs(tm.exponent)
        out.append(word)
    return gp.countGenerators(), out
def shrink(T, rounds=40):
    for _ in range(rounds):
        b=T.num_tetrahedra(); T.simplify()
        if T.num_tetrahedra()==b:
            T.randomize()
            T.simplify()
            if T.num_tetrahedra()>=b: break
    return T
def go(pd, sa, sb, label, expect=None):
    L=snappy.Link([tuple(x) for x in pd])
    T=L.exterior(with_hyperbolic_structure=False)
    T.dehn_fill(sa,1)
    F=T.filled_triangulation([1])
    print(f'{label}: after 1st fill {F.num_tetrahedra()} tets, cusps {F.num_cusps()}',flush=True)
    shrink(F)
    print(f'  shrunk to {F.num_tetrahedra()}',flush=True)
    # remaining cusps: 0 = R, 1 = b'
    F.dehn_fill(sb,1)
    G2=F.filled_triangulation([1])
    print(f'  after 2nd fill {G2.num_tetrahedra()} tets, cusps {G2.num_cusps()}',flush=True)
    shrink(G2)
    print(f'  shrunk to {G2.num_tetrahedra()}',flush=True)
    t0=time.time()
    RR=regina.Triangulation3(G2._to_string())
    for _ in range(30):
        if not RR.intelligentSimplify(): break
    gp=RR.group()
    for _ in range(6):
        gp.intelligentSimplify(); gp.smallCancellation()
    ng,rels=words_of(gp)
    print(f'  regina tets {RR.size()} gens {ng} rels {len(rels)} lens {[len(r) for r in rels]} H1 {gp.abelianisation().str()} [{time.time()-t0:.1f}s]',flush=True)
    if ng<=5:
        t0=time.time(); t=total_homs(ng,rels)
        print(f'  ==> total #Hom(.,A5) = {t}    expected {expect}   [{time.time()-t0:.1f}s]',flush=True)
        return t
if __name__=='__main__':
    DATA='/home/user/SR-Foxy/data/knots/'
    at=json.load(open(DATA+'AbeTagami_L_63_c1_c2.json'))['pd_code_snappy_0indexed']
    go(at,(1,0),(1,0),'CTRL AT meridian',180)
    go(at,(2,1),(0,1),'CTRL AT twist n=1',660)
    pd=json.load(open('L_best_ordered.json'))
    go(pd,(1,0),(1,0),'CTRL SURG meridian',1020)
    go(pd,(1,1),(-1,1),'TARGET +1 a / -1 b_prime','1020 if R / 2220 if D01')
