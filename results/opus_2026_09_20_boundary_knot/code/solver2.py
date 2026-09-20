"""Arc-based hom counter with frontier-following variable order and
conjugation-equation filtering.  Relations: gen[o] = gen[b]^-s gen[i] gen[b]^s."""
import collections
class Counter:
    def __init__(self, G):
        self.G=G
        # conj[s][i][o] = list of x with x^{-s} i x^{s} == o
        self.solve={}
    def conj_solutions(self, s, vi, vo):
        key=(s,vi,vo)
        r=self.solve.get(key)
        if r is None:
            G=self.G; mul,inv=G.mul,G.inv
            r=[]
            for x in range(G.n):
                cb = x if s>0 else inv[x]
                if mul[mul[inv[cb]][vi]][cb]==vo: r.append(x)
            self.solve[key]=r
        return r
    def count(self, ngens, conj_rels, word_rels, domains, node_cap=None, on_solution=None):
        G=self.G; mul,inv,e=G.mul,G.inv,G.e
        val=[None]*(ngens+1)
        occ=[[] for _ in range(ngens+1)]
        for ri,(b,s,i,o) in enumerate(conj_rels):
            for g in (b,i,o): occ[g].append(ri)
        wocc=[[] for _ in range(ngens+1)]
        for ri,w in enumerate(word_rels):
            for x in set(abs(y) for y in w): wocc[x].append(ri)
        dom={g:list(v) for g,v in domains.items()}
        stats={'nodes':0,'sols':0,'capped':False}
        def evalword(w):
            r=e
            for x in w:
                v=val[abs(x)]
                if v is None: return None
                r=mul[r][v if x>0 else inv[v]]
            return r
        def propagate(pending, newly, extra):
            queue=list(pending)
            while queue:
                ri=queue.pop()
                b,s,i,o=conj_rels[ri]
                vb,vi,vo=val[b],val[i],val[o]
                if vb is not None:
                    cb=vb if s>0 else inv[vb]
                    if vi is not None:
                        u=mul[mul[inv[cb]][vi]][cb]
                        if vo is None:
                            if u not in dom[o]: return False
                            val[o]=u; newly.append(o); queue.extend(occ[o])
                        elif vo!=u: return False
                    elif vo is not None:
                        u=mul[mul[cb][vo]][inv[cb]]
                        if u not in dom[i]: return False
                        val[i]=u; newly.append(i); queue.extend(occ[i])
                elif vi is not None and vo is not None:
                    cand=[x for x in self.conj_solutions(s,vi,vo) if x in dom[b]]
                    if not cand: return False
                    if len(cand)==1:
                        val[b]=cand[0]; newly.append(b); queue.extend(occ[b])
                    else:
                        extra[b]=cand
            return True
        def check_words(touched):
            cand=set()
            for g in touched: cand.update(wocc[g])
            for ri in cand:
                r=evalword(word_rels[ri])
                if r is not None and r!=e: return False
            return True
        prio=set()
        for w in word_rels:
            for x in w: prio.add(abs(x))
        def pick(extra):
            # prefer arcs with a filtered (small) candidate set
            best=None; bs=None
            for g,c in extra.items():
                if val[g] is None and (bs is None or len(c)<bs):
                    best,bs=g,len(c)
            if best is not None: return best, extra[best]
            # else frontier: an unassigned arc sharing a relation with an assigned one
            bestg=None; score=-1
            for ri,(b,s,i,o) in enumerate(conj_rels):
                asg=sum(1 for x in (b,i,o) if val[x] is not None)
                if asg==0: continue
                for x in (b,i,o):
                    if val[x] is None:
                        sc=asg*2+(1 if x in prio else 0)
                        if sc>score: bestg,score=x,sc
            if bestg is None:
                for g in range(1,ngens+1):
                    if val[g] is None: return g, dom[g]
                return None,None
            return bestg, dom[bestg]
        def search():
            stats['nodes']+=1
            if node_cap and stats['nodes']>node_cap:
                stats['capped']=True; return
            g,cands=pick({})
            if g is None:
                for w in word_rels:
                    if evalword(w)!=e: return
                stats['sols']+=1; return
            for v in cands:
                val[g]=v
                newly=[]; extra={}
                ok=propagate(occ[g],newly,extra)
                if ok and check_words([g]+newly):
                    # re-pick using extra filtering
                    search_with(extra)
                for x in newly: val[x]=None
                val[g]=None
        def search_with(extra):
            stats['nodes']+=1
            if node_cap and stats['nodes']>node_cap:
                stats['capped']=True; return
            g,cands=pick(extra)
            if g is None:
                for w in word_rels:
                    if evalword(w)!=e: return
                stats['sols']+=1
                if on_solution is not None: on_solution(list(val))
                return
            for v in cands:
                val[g]=v
                newly=[]; ex2={}
                ok=propagate(occ[g],newly,ex2)
                if ok and check_words([g]+newly):
                    search_with(ex2)
                for x in newly: val[x]=None
                val[g]=None
        pre=[g for g in range(1,ngens+1) if len(dom[g])==1]
        for g in pre: val[g]=dom[g][0]
        newly=[]; extra={}
        if not propagate(range(len(conj_rels)),newly,extra): return 0,stats
        if not check_words(pre+newly): return 0,stats
        search_with(extra)
        return stats['sols'],stats
