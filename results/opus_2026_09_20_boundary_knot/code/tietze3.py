"""Identification route that avoids every library group-simplifier.

1. Greedy length-aware Tietze elimination on the Wirtinger presentation of the
   ordered surgery link plus the two surgery relators, run with no length cap
   until no generator occurs exactly once in any relator.
2. A numpy-vectorised #Hom(., A5) count: evaluate each relator simultaneously
   over all |A5|^k generator assignments, pruning after each relator.

Controls: the meridian fillings must return 1020 (= K_0 # (-K_0)); the same code
on the stored diagrams of 6_3, K_1, D_{0,1} must return 180, 660, 2220.
"""
import json, time, itertools, collections, sys
import numpy as np, snappy
import periph, gaussbuild as GB, homcount as H, tietze
A5=H.alt(5)
MUL=np.array(A5.mul,dtype=np.int16); INV=np.array(A5.inv,dtype=np.int16); E=A5.e; N=A5.n

def homs_vec(ngens, rels, report=True):
    """rels: words over +-1..+-ngens (already re-indexed to 1..ngens)."""
    assign=np.array(list(itertools.product(range(N),repeat=ngens)),dtype=np.int16)  # (N^k, k)
    rels=sorted(rels,key=len)
    for ri,w in enumerate(rels):
        cur=np.full(assign.shape[0],E,dtype=np.int16)
        for x in w:
            v=assign[:,abs(x)-1]
            if x<0: v=INV[v]
            cur=MUL[cur,v]
        keep=cur==E
        assign=assign[keep]
        if report: print(f'      relator {ri} len {len(w)}: {assign.shape[0]} survivors',flush=True)
        if assign.shape[0]==0: break
    return int(assign.shape[0])

def reindex(gens,rels):
    idx={g:i+1 for i,g in enumerate(gens)}
    return [[ idx[abs(x)] if x>0 else -idx[abs(x)] for x in r] for r in rels]

def run(base,label,exp):
    t0=time.time()
    gens,R2=tietze.eliminate(base,cap=10**9,verbose=False)
    tot=sum(len(r) for r in R2)
    print(f'{label}: {len(gens)} gens, {len(R2)} rels, lengths {sorted(len(r) for r in R2)}, total {tot} [{time.time()-t0:.0f}s]',flush=True)
    if len(gens)>4:
        print('   too many generators for the vectorised count',flush=True); return
    t0=time.time()
    n=homs_vec(len(gens),reindex(gens,R2))
    print(f'   total #Hom(.,A5) = {n}   expected {exp}   [{time.time()-t0:.0f}s]',flush=True)
    return n

if __name__=='__main__':
    # --- calibration of the vectorised counter on the stored reference diagrams
    import wirt
    DATA='/home/user/SR-Foxy/data/knots/'
    for nm,fn,exp in [('6_3',None,180),('K_1','AbeTagami_K_1.json',660),('D_0_1','AbeTagami_D_0_1.json',2220)]:
        L=snappy.Link(nm) if fn is None else snappy.Link([list(c) for c in json.load(open(DATA+fn))['pd_code_snappy_0indexed']])
        n,rl,_=wirt.wirtinger(L)
        run([[-s*b,i,s*b,-o] for (b,s,i,o) in rl],f'CALIB {nm}',exp)
    # --- the surgery link
    gw=GB.extract_gauss(snappy.Link([tuple(x) for x in json.load(open('L_best_ordered.json'))]))
    ng,mer,rels0,longs,wr,comp=periph.peripheral(gw)
    wirt_rels=[[-s*b,i,s*b,-o] for (b,s,i,o) in rels0]
    def sur(c,p,q):
        m=[mer[c]]; l=longs[c]; w=[]
        for _ in range(abs(p)): w += m if p>0 else [-x for x in reversed(m)]
        for _ in range(abs(q)): w += l if q>0 else [-x for x in reversed(l)]
        return tietze.red(w)
    run(list(wirt_rels)+[sur(1,1,0),sur(2,1,0)],'CTRL meridian fills',1020)
    run(list(wirt_rels)+[sur(1,1,1),sur(2,-1,1)],'TARGET +1 on a / -1 on b_prime','1020 if R, 2220 if D_{0,1}')
