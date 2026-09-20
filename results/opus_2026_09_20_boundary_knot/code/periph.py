"""Port of the verified peripheral() routine from check_exact_independent.mjs.
Input: per-component signed Gauss words [[cid,'O'/'U',sign],...].
Output: number of generators, meridian generator per component, Wirtinger
relators as (b,s,i,o) conj-triples, preferred (0-framed) longitudes, writhes."""
from collections import defaultdict

def reduce_w(w):
    r=[]
    for x in w:
        if r and r[-1]==-x: r.pop()
        else: r.append(x)
    return r

def peripheral(words):
    owners=defaultdict(list)
    for c,w in enumerate(words):
        for cid,typ,s in w: owners[cid].append(c)
    ng=0; mer=[]; comp={}; cr={}
    for c,w in enumerate(words):
        n=max(1,sum(1 for x in w if x[1]=='U'))
        start=ng+1; cur=start; ng+=n; mer.append(start)
        for g in range(start,ng+1): comp[g]=c
        for cid,typ,s in w:
            cr.setdefault(cid,{'s':s})
            if typ=='O': cr[cid]['b']=cur
            else:
                nxt=start+(cur-start+1)%n
                cr[cid]['i']=cur; cr[cid]['o']=nxt; cur=nxt
    rels=[]
    for cid in sorted(cr, key=lambda z: (0,z,"") if isinstance(z,int) else (1,0,str(z))):
        c=cr[cid]; rels.append((c['b'],c['s'],c['i'],c['o']))
    longs=[]; wr=[]
    for c,w in enumerate(words):
        self_w=sum(x[2] for x in w if x[1]=='U' and all(o==c for o in owners[x[0]]))
        wr.append(self_w)
        fix=[(-mer[c] if self_w>=0 else mer[c])]*abs(self_w)
        longs.append(reduce_w(fix+[x[2]*cr[x[0]]['b'] for x in w if x[1]=='U']))
    return ng, mer, rels, longs, wr, comp
