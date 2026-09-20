"""Greedy length-aware Tietze elimination on the Wirtinger presentation of the
ordered surgery link plus the two surgery relators, followed by a direct
#Hom(., A5) count on whatever small presentation comes out."""
import json, time, collections, itertools, sys, snappy
import periph, gaussbuild as GB, homcount as H
def red(w):
    r=[]
    for x in w:
        if r and r[-1]==-x: r.pop()
        else: r.append(x)
    return r
def cyc(w):
    w=red(w)
    while len(w)>1 and w[0]==-w[-1]: w=w[1:-1]
    return w
def eliminate(rels, cap=200000, verbose=True):
    rels=[cyc(r) for r in rels]; rels=[r for r in rels if r]
    t0=time.time()
    while True:
        occ=collections.Counter()
        for r in rels:
            for x in r: occ[abs(x)]+=1
        best=None
        for ri,r in enumerate(rels):
            c=collections.Counter(abs(x) for x in r)
            for g,k in c.items():
                if k!=1: continue
                cost=(occ[g]-1)*(len(r)-2)
                if best is None or cost<best[0]: best=(cost,ri,g)
        if best is None: break
        cost,ri,g=best
        r=rels[ri]
        # rotate so the single occurrence of g is first
        p=[i for i,x in enumerate(r) if abs(x)==g][0]
        r=r[p:]+r[:p]
        expr = [-x for x in reversed(r[1:])] if r[0]>0 else r[1:]
        # r = g^{+-1} * rest = 1  ->  g = rest^{-1} (if +) or g = rest (if -, since g^-1 rest =1 -> g = rest)
        new=[]
        for j,rr in enumerate(rels):
            if j==ri: continue
            out=[]
            for x in rr:
                if abs(x)==g: out += expr if x>0 else [-y for y in reversed(expr)]
                else: out.append(x)
            out=cyc(out)
            if out: new.append(out)
        tot=sum(len(x) for x in new)
        if tot>cap:
            if verbose: print('  stopping: total length would be',tot,flush=True)
            break
        rels=new
        if verbose and len(rels)%25==0:
            print(f'  {len(rels)} relators, total length {tot}, gens left {len(set(abs(x) for r in rels for x in r))} [{time.time()-t0:.0f}s]',flush=True)
    gens=sorted(set(abs(x) for r in rels for x in r))
    return gens, rels
def total_homs(gens, rels, G):
    idx={g:i for i,g in enumerate(gens)}
    mul,inv,e=G.mul,G.inv,G.e
    R=[[ (idx[abs(x)]+1) if x>0 else -(idx[abs(x)]+1) for x in r] for r in rels]
    byk=collections.defaultdict(list)
    for r in R: byk[max(abs(x) for x in r)].append(r)
    n=len(gens); tot=0
    def ev(w,val):
        z=e
        for x in w:
            v=val[abs(x)-1]; z=mul[z][v if x>0 else inv[v]]
        return z
    def rec(k,val):
        nonlocal tot
        if k>n: tot+=1; return
        for v in range(G.n):
            val.append(v)
            if all(ev(r,val)==e for r in byk[k]): rec(k+1,val)
            val.pop()
    rec(1,[]); return tot
if __name__=='__main__':
    gw=GB.extract_gauss(snappy.Link([tuple(x) for x in json.load(open('L_best_ordered.json'))]))
    ng,mer,rels,longs,wr,comp=periph.peripheral(gw)
    wirt=[[-s*b,i,s*b,-o] for (b,s,i,o) in rels]
    def sur(c,p,q):
        m=[mer[c]]; l=longs[c]; w=[]
        for _ in range(abs(p)): w += m if p>0 else [-x for x in reversed(m)]
        for _ in range(abs(q)): w += l if q>0 else [-x for x in reversed(l)]
        return red(w)
    A5=H.alt(5)
    for label,sa,sb,exp in [('CTRL meridian',(1,0),(1,0),1020),('TARGET',(1,1),(-1,1),'1020 R / 2220 D01')]:
        print(label,flush=True)
        gens,R2=eliminate(list(wirt)+[sur(1,*sa),sur(2,*sb)])
        print(f'  -> {len(gens)} generators, {len(R2)} relators, lengths {sorted(len(r) for r in R2)[-6:]}, total {sum(len(r) for r in R2)}',flush=True)
        if len(gens)<=4:
            t0=time.time(); print('  total #Hom(.,A5) =',total_homs(gens,R2,A5),'expected',exp,'[%.1fs]'%(time.time()-t0),flush=True)
