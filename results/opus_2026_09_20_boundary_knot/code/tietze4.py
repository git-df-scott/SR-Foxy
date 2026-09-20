"""As tietze3, but (i) randomised-restart greedy Tietze to escape the deadlock,
(ii) Regina Nielsen/small-cancellation passes on the small presentation,
(iii) chunked numpy counting so up to 6 generators are affordable."""
import json, time, itertools, collections, random, sys
import numpy as np, snappy, regina
import periph, gaussbuild as GB, homcount as H, tietze
A5=H.alt(5)
MUL=np.array(A5.mul,dtype=np.int16); INV=np.array(A5.inv,dtype=np.int16); E=A5.e; N=A5.n

def homs_vec(k, rels, report=True, chunk=4_000_000):
    rels=sorted(rels,key=len)
    total=0; grand=N**k
    surv=[]
    start=0
    while start<grand:
        m=min(chunk,grand-start)
        idxs=np.arange(start,start+m,dtype=np.int64)
        cols=[]
        for j in range(k-1,-1,-1):
            cols.append((idxs//(N**j))%N)
        assign=np.stack(cols[::-1],axis=1).astype(np.int16)  # careful: build below
        # cols was built for j=k-1..0 meaning most significant first
        assign=np.stack([ (idxs//(N**(k-1-p)))%N for p in range(k)],axis=1).astype(np.int16)
        for w in rels:
            cur=np.full(assign.shape[0],E,dtype=np.int16)
            for x in w:
                v=assign[:,abs(x)-1]
                if x<0: v=INV[v]
                cur=MUL[cur,v]
            assign=assign[cur==E]
            if assign.shape[0]==0: break
        total+=assign.shape[0]
        start+=m
    return total

def reindex(gens,rels):
    idx={g:i+1 for i,g in enumerate(gens)}
    return [[ idx[abs(x)] if x>0 else -idx[abs(x)] for x in r] for r in rels]

def rand_eliminate(rels, tries=40, seed=0):
    """Greedy elimination with randomised tie-breaking; keep the fewest generators."""
    rng=random.Random(seed)
    best=None
    for t in range(tries):
        R=[tietze.cyc(r) for r in rels]; R=[r for r in R if r]
        while True:
            occ=collections.Counter()
            for r in R:
                for x in r: occ[abs(x)]+=1
            cands=[]
            for ri,r in enumerate(R):
                c=collections.Counter(abs(x) for x in r)
                for g,kk in c.items():
                    if kk==1: cands.append(((occ[g]-1)*(len(r)-2), ri, g))
            if not cands: break
            cands.sort()
            lo=cands[0][0]
            pool=[c for c in cands if c[0]<=lo+ (0 if t==0 else rng.choice([0,0,1,3,8]))]
            cost,ri,g=rng.choice(pool) if t>0 else cands[0]
            r=R[ri]
            p=[i for i,x in enumerate(r) if abs(x)==g][0]
            r=r[p:]+r[:p]
            expr=[-x for x in reversed(r[1:])] if r[0]>0 else r[1:]
            new=[]
            for j,rr in enumerate(R):
                if j==ri: continue
                out=[]
                for x in rr:
                    if abs(x)==g: out += expr if x>0 else [-y for y in reversed(expr)]
                    else: out.append(x)
                out=tietze.cyc(out)
                if out: new.append(out)
            if sum(len(x) for x in new)>3_000_000: break
            R=new
        gens=sorted({abs(x) for r in R for x in r})
        key=(len(gens),sum(len(r) for r in R))
        if best is None or key<best[0]: best=(key,gens,R)
    return best[1],best[2]

def regina_pass(gens,rels,rounds=3,nielsen=True):
    idx={g:i for i,g in enumerate(gens)}
    gp=regina.GroupPresentation(len(gens))
    for r in rels:
        w=regina.GroupExpression()
        for x in r: w.addTermLast(idx[abs(x)], 1 if x>0 else -1)
        gp.addRelation(w)
    for _ in range(rounds):
        gp.intelligentSimplify(); gp.smallCancellation()
        if nielsen:
            try: gp.intelligentNielsen()
            except Exception: pass
    out=[]
    for i in range(gp.countRelations()):
        w=gp.relation(i); wd=[]
        for j in range(w.countTerms()):
            tm=w.term(j); wd += [ (tm.generator+1) if tm.exponent>0 else -(tm.generator+1) ]*abs(tm.exponent)
        out.append(wd)
    return list(range(1,gp.countGenerators()+1)), out

def attack(base,label,exp,maxgen=6):
    t0=time.time()
    gens,R=rand_eliminate(base)
    print(f'{label}: randomised Tietze -> {len(gens)} gens, total {sum(len(r) for r in R)} [{time.time()-t0:.0f}s]',flush=True)
    for it in range(4):
        if len(gens)<=maxgen: break
        t1=time.time()
        gens,R=regina_pass(gens,R)
        print(f'   regina pass {it}: {len(gens)} gens, {len(R)} rels, total {sum(len(r) for r in R)} [{time.time()-t1:.0f}s]',flush=True)
        gens,R=rand_eliminate(R,tries=12,seed=it+1)
        print(f'   re-Tietze  {it}: {len(gens)} gens, total {sum(len(r) for r in R)}',flush=True)
    print(f'   final: {len(gens)} gens, {len(R)} rels, lengths {sorted(len(r) for r in R)[:8]}...',flush=True)
    if len(gens)>maxgen:
        print('   STILL too many generators',flush=True); return None
    t1=time.time(); n=homs_vec(len(gens),reindex(gens,R))
    print(f'   total #Hom(.,A5) = {n}   expected {exp}   [{time.time()-t1:.0f}s]',flush=True)
    return n

if __name__=='__main__':
    import wirt
    DATA='/home/user/SR-Foxy/data/knots/'
    L=snappy.Link([list(c) for c in json.load(open(DATA+'AbeTagami_D_0_1.json'))['pd_code_snappy_0indexed']])
    n,rl,_=wirt.wirtinger(L)
    attack([[-s*b,i,s*b,-o] for (b,s,i,o) in rl],'CALIB D_0_1',2220)
    gw=GB.extract_gauss(snappy.Link([tuple(x) for x in json.load(open('L_best_ordered.json'))]))
    ng,mer,rels0,longs,wr,comp=periph.peripheral(gw)
    W=[[-s*b,i,s*b,-o] for (b,s,i,o) in rels0]
    def sur(c,p,q):
        m=[mer[c]]; l=longs[c]; w=[]
        for _ in range(abs(p)): w += m if p>0 else [-x for x in reversed(m)]
        for _ in range(abs(q)): w += l if q>0 else [-x for x in reversed(l)]
        return tietze.red(w)
    attack(list(W)+[sur(1,1,0),sur(2,1,0)],'CTRL meridian fills',1020)
    attack(list(W)+[sur(1,1,1),sur(2,-1,1)],'TARGET +1 a / -1 b_prime','1020 if R, 2220 if D_{0,1}')
