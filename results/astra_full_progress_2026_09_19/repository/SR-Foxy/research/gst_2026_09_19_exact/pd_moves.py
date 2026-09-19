"""Elementary planar R1/R2 removal with explicit before/after witnesses."""
from pd_algebra import *
def delete_crossings(pd,ids):
    uf=DSU({a for q in pd for a in q})
    for i in ids:
        a,b,c,d=pd[i];uf.union(a,c);uf.union(b,d)
    kept=[[uf.find(a) for a in q] for i,q in enumerate(pd) if i not in ids]
    # Labels need only occur twice in the retained diagram. Lost classes record trivial circles.
    oldst=structure(pd); expected=len(oldst['tours'])
    newst=structure(kept) if kept else {'tours':[]}
    extra=expected-len(newst['tours'])
    if extra<0:raise ValueError('Reidemeister removal cannot add components')
    return kept,extra

def simplify(pd):
    pd=[list(q) for q in pd];movie=[];trivial=0
    while pd:
        st=structure(pd);choice=None
        for fi,face in enumerate(st['faces']):
            if len(face)==1:
                choice=('R1',[face[0][0]],face);break
            if len(face)==2:
                d,e=face
                if d[0]!=e[0] and st['alpha'][d][1]%2==d[1]%2:
                    choice=('R2',sorted({d[0],e[0]}),face);break
        if choice is None:break
        kind,ids,face=choice;new,extra=delete_crossings(pd,set(ids))
        movie.append({'type':kind,'direction':'remove','crossings':ids,'face_darts':[list(d) for d in face],'before':pd,'after':new,'new_trivial_components':extra})
        trivial+=extra;pd=new
    return pd,trivial,movie

def braid_pd(word,n=None):
    if n is None:n=max(abs(x) for x in word)+1
    top=list(range(1,n+1));cur=top[:];nextlabel=n+1;pd=[]
    for v in word:
        i=abs(v)-1
        if not 0<=i<n-1:raise ValueError('Braid generator out of range')
        a,b=cur[i],cur[i+1];c,d=nextlabel,nextlabel+1;nextlabel+=2
        # left -> right and right -> left, strands directed downwards.
        pd.append([b,a,c,d] if v>0 else [a,c,d,b])
        cur[i],cur[i+1]=c,d
    uf=DSU(range(1,nextlabel))
    for a,b in zip(cur,top):uf.union(a,b)
    return [[uf.find(a) for a in q] for q in pd]
