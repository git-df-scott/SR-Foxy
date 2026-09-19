"""Integer-labelled free words, with exact reductions."""
def red(w):
    out=[]
    for x in w:
        if not isinstance(x,int) or x==0: raise ValueError('nonzero integer letter required')
        if out and out[-1]==-x:out.pop()
        else:out.append(x)
    return tuple(out)
def inv(w):return tuple(-x for x in reversed(w))
def mul(*words):return red(x for w in words for x in w)
def sub(w, images):return red(y for x in w for y in (images[abs(x)] if x>0 else inv(images[abs(x)])))
def cyc(w):
    w=red(w);p=[]
    while len(w)>1 and w[0]==-w[-1]:p.append(w[0]);w=w[1:-1]
    return tuple(p),w

def eliminate(rels,keep=()):
    """Tietze-eliminate a generator occurring exactly once in a relator."""
    rels=[cyc(r)[1] for r in rels if cyc(r)[1]]
    gens={abs(x) for r in rels for x in r}
    images={g:(g,) for g in gens};log=[]
    while True:
        choices=[]
        for ri,r in enumerate(rels):
            for g in sorted(set(map(abs,r))-set(keep)):
                if sum(abs(x)==g for x in r)!=1:continue
                p=next(i for i,x in enumerate(r) if abs(x)==g)
                # r=A x B; x=B^-1 A^-1, with sign accounted for.
                expr=inv(r[p+1:]+r[:p]);expr=expr if r[p]>0 else inv(expr)
                occurrences=sum(sum(abs(x)==g for x in s) for s in rels)
                score=(len(expr)-1)*max(0,occurrences-1)
                choices.append((score,len(expr),g,ri,expr))
        if not choices:break
        _,_,g,ri,expr=min(choices)
        log.append({'generator':g,'defining_relator':list(rels[ri]),'replacement':list(expr)})
        subst={a:((a,) if a!=g else expr) for a in gens}
        rels=[cyc(sub(r,subst))[1] for j,r in enumerate(rels) if j!=ri]
        rels=[r for r in rels if r]
        images={a:sub(w,subst) for a,w in images.items()}
        gens.remove(g)
    return gens,rels,images,log
