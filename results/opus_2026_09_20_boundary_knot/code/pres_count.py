"""Count Hom(pi, G) with a pinned meridian, from a small finite presentation."""
import itertools
def parse_word(w):
    out=[]
    for ch in w:
        i=ord(ch.lower())-ord('a')+1
        out.append(i if ch.islower() else -i)
    return out
def order_of(G,g):
    x=g;k=1
    while x!=G.e: x=G.mul[x][g];k+=1
    return k
def count(ngens, rels, merword, G, gfix):
    mul,inv,e=G.mul,G.inv,G.e
    n=G.n
    total=0
    def ev(w,val):
        r=e
        for x in w:
            v=val[abs(x)-1]
            r=mul[r][v if x>0 else inv[v]]
        return r
    for tup in itertools.product(range(n), repeat=ngens):
        if ev(merword,tup)!=gfix: continue
        ok=True
        for R in rels:
            if ev(R,tup)!=e: ok=False;break
        if ok: total+=1
    return total
def profile(ngens, rels, merword, groups):
    out={}
    for gname,G in groups:
        for ci,cl in enumerate(G.classes):
            g=cl[0]
            if g==G.e: continue
            tag=f'{gname}|cls{ci}|ord{order_of(G,g)}|size{len(cl)}'
            out[tag]=count(ngens,rels,merword,G,g)
    return out
