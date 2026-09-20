"""Route 7: SnapPy combinatorial fill -> Regina Triangulation3 -> intelligentSimplify
-> group presentation -> total #Hom(., A5).
Controls: AT meridian 180, AT annulus twist 660, surgery-link meridian 1020."""
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
def go(pd, slopes, label, expect=None):
    L=snappy.Link([tuple(x) for x in pd])
    T=L.exterior(with_hyperbolic_structure=False)
    T.dehn_fill(slopes)
    F=T.filled_triangulation()
    print(f'{label}: filled tets {F.num_tetrahedra()}',flush=True)
    t0=time.time()
    R=regina.Triangulation3(F._to_string())
    n0=R.size()
    for _ in range(30):
        if not R.intelligentSimplify(): break
    print(f'  regina tets {n0} -> {R.size()}  valid={R.isValid()} ideal={R.isIdeal()} [{time.time()-t0:.1f}s]',flush=True)
    t0=time.time()
    gp=R.group()
    for _ in range(6):
        gp.intelligentSimplify(); gp.smallCancellation()
    ng,rels=words_of(gp)
    print(f'  gens {ng} rels {len(rels)} lens {[len(r) for r in rels]} H1 {gp.abelianisation().str()} [{time.time()-t0:.1f}s]',flush=True)
    if ng<=5:
        t0=time.time(); t=total_homs(ng,rels)
        print(f'  ==> total #Hom(.,A5) = {t}    expected {expect}   [{time.time()-t0:.1f}s]',flush=True)
        return t
if __name__=='__main__':
    DATA='/home/user/SR-Foxy/data/knots/'
    at=json.load(open(DATA+'AbeTagami_L_63_c1_c2.json'))['pd_code_snappy_0indexed']
    go(at,[(0,0),(1,0),(1,0)],'CTRL AT meridian',180)
    go(at,[(0,0),(2,1),(0,1)],'CTRL AT twist n=1',660)
    pd=json.load(open('L_best_ordered.json'))
    go(pd,[(0,0),(1,0),(1,0)],'CTRL SURG meridian',1020)
    go(pd,[(0,0),(1,1),(-1,1)],'TARGET +1 a / -1 b_prime','1020 if R / 2220 if D01')
    go(pd,[(0,0),(-1,1),(1,1)],'VARIANT -1 a / +1 b_prime','?')
    go(pd,[(0,0),(1,1),(1,0)],'VARIANT +1 a only','?')
    go(pd,[(0,0),(1,0),(-1,1)],'VARIANT -1 b_prime only','?')
