"""Route 4 -- the cleanest one.  Inputs: ONLY the frozen certified 675-generator
Wirtinger presentation and preferred longitudes of surgery_diagram.json (verified
byte-for-byte against framed_fox_boundary.json by periph.py), plus the two
surgery relators  mu_a*lam_a  and  mu_b'^-1*lam_b'.
No SnapPy triangulation, no diagram simplification.  Regina simplifies the
presentation; the hom count is my own code.

Reference total #Hom(pi,A5):  K_0 # -K_0 = 1020 ;  D_{0,1} = K_0 # -K_1 = 2220.
"""
import json, time, collections, sys, regina
import periph, homcount as H
A5=H.alt(5)
def total_homs(ngens, rels, G=A5):
    mul,inv,e=G.mul,G.inv,G.e; n=G.n
    def ev(w,val):
        r=e
        for x in w:
            v=val[abs(x)-1]; r=mul[r][v if x>0 else inv[v]]
        return r
    byk=collections.defaultdict(list)
    for R in rels: byk[max((abs(x) for x in R),default=1)].append(R)
    tot=0
    def rec(k,val):
        nonlocal tot
        if k>ngens: tot+=1; return
        for v in range(n):
            val.append(v)
            if all(ev(R,val)==e for R in byk[k]): rec(k+1,val)
            val.pop()
    rec(1,[]); return tot
def simplify_pres(ngens, rels, rounds=6):
    gp=regina.GroupPresentation(ngens)
    for R in rels:
        w=regina.GroupExpression()
        for x in R: w.addTermLast(abs(x)-1, 1 if x>0 else -1)
        gp.addRelation(w)
    for i in range(rounds):
        gp.intelligentSimplify(); gp.smallCancellation()
    gp.intelligentSimplify()
    out=[]
    for i in range(gp.countRelations()):
        w=gp.relation(i); word=[]
        for j in range(w.countTerms()):
            tm=w.term(j); g=tm.generator+1; ex=tm.exponent
            word += [g if ex>0 else -g]*abs(ex)
        out.append(word)
    return gp.countGenerators(), out, gp
D='/home/user/SR-Foxy/results/astra_genus_one_2026_09_18/'
dg=json.load(open(D+'surgery_diagram.json'))
gw=[[list(c) for c in w] for w in dg['gauss_words']]
ng,mer,rels,longs,wr,comp=periph.peripheral(gw)
f=json.load(open(D+'framed_fox_boundary.json'))
assert ng==f['n_generators'] and mer==f['meridians'] and longs==f['preferred_longitudes'] and wr==f['self_writhes']
print('frozen presentation reproduced: gens',ng,'meridians',mer,'writhes',wr,flush=True)
wirt=[[-s*b, i, s*b, -o] for (b,s,i,o) in rels]
assert wirt==[list(r) for r in f['relators']]
print('all 675 Wirtinger relators identical to framed_fox_boundary.json',flush=True)
def surgery_relator(cusp, p, q):
    m=[mer[cusp]]; l=longs[cusp]
    w=[]
    for _ in range(abs(p)): w += m if p>0 else [-x for x in reversed(m)]
    for _ in range(abs(q)): w += l if q>0 else [-x for x in reversed(l)]
    return periph.reduce_w(w)
CASES=[('CTRL meridian fills -> expect R = 1020', (1,0),(1,0), 1020),
       ('TARGET +1 on a, -1 on b_prime', (1,1),(-1,1), None),
       ('VARIANT -1 on a, +1 on b_prime', (-1,1),(1,1), None),
       ('VARIANT +1 on both', (1,1),(1,1), None)]
for label,sa,sb,exp in CASES:
    allr=list(wirt)+[surgery_relator(1,*sa), surgery_relator(2,*sb)]
    t0=time.time()
    n2,r2,gp=simplify_pres(ng, allr)
    print(f'{label}: slopes a={sa} b\'={sb} -> gens {n2} rels {len(r2)} lens {[len(r) for r in r2]} abelianisation {gp.abelianisation().str()} [{time.time()-t0:.1f}s]',flush=True)
    if n2<=5:
        t0=time.time(); t=total_homs(n2,r2)
        print(f'   total #Hom(.,A5) = {t}   expected-if-R 1020, expected-if-D01 2220   [{time.time()-t0:.1f}s]',flush=True)
    else:
        print('   gens too large for brute force:',n2,flush=True)
