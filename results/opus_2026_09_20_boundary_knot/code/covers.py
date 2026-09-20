"""Route 9 (decisive & cheap): degree-5 cover census of the surgered knot exterior,
computed straight from the filled triangulation.  No presentation simplification.
References (same code path, from PD codes):
  6_3            : 2 covers
  K_1            : 8 covers
  6_3 # -6_3 (=R): 9 covers,  H1 multiset {Z/7+Z/7+Z^3 x2, (Z/4)^8+Z x1, Z^5 x6}
  stored D_{0,1} : 21 covers, richer multiset
Controls run here: meridian fillings (must reproduce R) and the genuine
Abe-Tagami annulus twist (must reproduce K_1)."""
import json, time, collections, snappy
DATA='/home/user/SR-Foxy/data/knots/'
def prof(T,label,deg=5):
    t0=time.time(); cs=T.covers(deg)
    h=collections.Counter(str(c.homology()) for c in cs)
    print(f'{label}: #deg{deg} covers = {len(cs)}   [{time.time()-t0:.1f}s]',flush=True)
    for k,v in sorted(h.items()): print(f'      {v} x  {k}',flush=True)
    return len(cs), dict(h)
def filled(pd, sa, sb, label):
    L=snappy.Link([tuple(x) for x in pd])
    T=L.exterior(with_hyperbolic_structure=False)
    T.dehn_fill([(0,0),sa,sb])
    F=T.filled_triangulation()
    for _ in range(20):
        b=F.num_tetrahedra(); F.simplify()
        if F.num_tetrahedra()==b: break
    print(f'{label}: filled triangulation {F.num_tetrahedra()} tets, cusps {F.num_cusps()}, H1 {F.homology()}',flush=True)
    return F
if __name__=='__main__':
    at=json.load(open(DATA+'AbeTagami_L_63_c1_c2.json'))['pd_code_snappy_0indexed']
    prof(filled(at,(1,0),(1,0),'CTRL AT meridian (expect 6_3: 2)'),'CTRL AT meridian')
    prof(filled(at,(2,1),(0,1),'CTRL AT twist n=1 (expect K_1: 8)'),'CTRL AT twist n=1')
    pd=json.load(open('L_best_ordered.json'))
    prof(filled(pd,(1,0),(1,0),'CTRL SURG meridian (expect R: 9)'),'CTRL SURG meridian')
    prof(filled(pd,(1,1),(-1,1),'TARGET +1 a / -1 b_prime'),'TARGET')
    prof(filled(pd,(-1,1),(1,1),'VARIANT -1 a / +1 b_prime'),'VARIANT swap')
    prof(filled(pd,(1,1),(1,0),'VARIANT +1 a only'),'VARIANT a only')
    prof(filled(pd,(1,0),(-1,1),'VARIANT -1 b_prime only'),'VARIANT b only')
