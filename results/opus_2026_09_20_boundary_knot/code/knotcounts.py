import json, itertools, spherogram, wirt, homcount as H
def cyc(perm_cycles, deg):
    p=list(range(deg))
    for cyc_ in perm_cycles:
        for i in range(len(cyc_)):
            p[cyc_[i]]=cyc_[(i+1)%len(cyc_)]
    return tuple(p)
GROUPS={}
GROUPS['S3']=H.sym(3); GROUPS['S4']=H.sym(4); GROUPS['A4']=H.alt(4)
GROUPS['A5']=H.alt(5); GROUPS['S5']=H.sym(5)
GROUPS['D5']=H.PermGroup.generated([cyc([[0,1,2,3,4]],5), cyc([[1,4],[2,3]],5)])
GROUPS['D7']=H.PermGroup.generated([cyc([[0,1,2,3,4,5,6]],7), cyc([[1,6],[2,5],[3,4]],7)])
GROUPS['D13']=H.PermGroup.generated([cyc([list(range(13))],13), cyc([[i,13-i] for i in range(1,7)],13)])

def counts(name, ngens, rels, words, verbose=False):
    out={}
    for gname,G in GROUPS.items():
        H.count_homs.G=G
        for ci,cl in enumerate(G.classes):
            g=cl[0]
            if g==G.e: continue
            dom={x: cl for x in range(1,ngens+1)}
            dom[1]=[g]
            c,st=H.count_homs(ngens,rels,words,dom)
            out[f'{gname}/c{ci}(|C|={len(cl)},ord={order_of(G,g)})']=c
    return out
def order_of(G,g):
    x=g; k=1
    while x!=G.e: x=G.mul[x][g]; k+=1
    return k
def from_link(L):
    n,rels,_=wirt.wirtinger(L)
    return n,rels,[]
if __name__=='__main__':
    import sys
    DATA='/home/user/SR-Foxy/data/knots/'
    objs={}
    objs['6_3']=spherogram.Link('6_3')
    objs['K_1']=spherogram.Link([[a for a in c] for c in json.load(open(DATA+'AbeTagami_K_1.json'))['pd_code_snappy_0indexed']])
    objs['D_0_1_stored']=spherogram.Link([[a for a in c] for c in json.load(open(DATA+'AbeTagami_D_0_1.json'))['pd_code_snappy_0indexed']])
    res={}
    for k,L in objs.items():
        n,rels,w=from_link(L)
        res[k]=counts(k,n,rels,w)
        print(k,'arcs',n)
    keys=list(res['6_3'].keys())
    print(f'{"class":40s} {"6_3":>8s} {"K_1":>8s} {"63*K1":>10s} {"63^2":>8s} {"D01":>8s}')
    for kk in keys:
        a=res['6_3'][kk]; b=res['K_1'][kk]; d=res['D_0_1_stored'][kk]
        print(f'{kk:40s} {a:8d} {b:8d} {a*b:10d} {a*a:8d} {d:8d}')
    json.dump(res,open('knotcounts.json','w'),indent=1)
