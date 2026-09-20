"""Route 6: purely combinatorial SnapPy Triangulation: fill, retriangulate,
simplify, then fundamental group.  Then total #Hom(., A5)."""
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
def parse(w):
    return [ (ord(c.lower())-96) if c.islower() else -(ord(c.lower())-96) for c in w]
def go(pd, slopes, label, expect=None):
    L=snappy.Link([tuple(x) for x in pd])
    T=L.exterior(with_hyperbolic_structure=False)
    print(label,'raw tets',T.num_tetrahedra(),flush=True)
    T.dehn_fill(slopes)
    t0=time.time()
    F=T.filled_triangulation()
    print('  filled tets',F.num_tetrahedra(),'%.1fs'%(time.time()-t0),flush=True)
    t0=time.time()
    for _ in range(20):
        before=F.num_tetrahedra(); F.simplify()
        if F.num_tetrahedra()==before: break
    print('  simplified tets',F.num_tetrahedra(),'%.1fs'%(time.time()-t0),flush=True)
    t0=time.time(); G=F.fundamental_group()
    ng=G.num_generators(); rels=[parse(r) for r in G.relators()]
    print('  gens',ng,'rels',len(rels),'lens',[len(r) for r in rels],'%.1fs'%(time.time()-t0),flush=True)
    if ng<=5:
        t0=time.time(); print('  total #Hom(.,A5) =',total_homs(ng,rels),' expected',expect,'[%.1fs]'%(time.time()-t0),flush=True)
if __name__=='__main__':
    DATA='/home/user/SR-Foxy/data/knots/'
    at=json.load(open(DATA+'AbeTagami_L_63_c1_c2.json'))['pd_code_snappy_0indexed']
    go(at,[(0,0),(1,0),(1,0)],'CTRL AT meridian',180)
    go(at,[(0,0),(2,1),(0,1)],'CTRL AT twist n=1',660)
    pd=json.load(open('L_best_ordered.json'))
    go(pd,[(0,0),(1,0),(1,0)],'CTRL SURG meridian',1020)
    go(pd,[(0,0),(1,1),(-1,1)],'TARGET','1020 if R / 2220 if D01')
