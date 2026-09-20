import json, sys, time, spherogram, wirt, homcount as H
DATA='/home/user/SR-Foxy/data/knots/'
def order_of(G,g):
    x=g;k=1
    while x!=G.e: x=G.mul[x][g];k+=1
    return k
GROUPS=[('A4',H.alt(4)),('S4',H.sym(4)),('A5',H.alt(5)),('S5',H.sym(5))]
objs={}
objs['6_3']=spherogram.Link('6_3')
objs['K_1']=spherogram.Link([list(c) for c in json.load(open(DATA+'AbeTagami_K_1.json'))['pd_code_snappy_0indexed']])
objs['D_0_1']=spherogram.Link([list(c) for c in json.load(open(DATA+'AbeTagami_D_0_1.json'))['pd_code_snappy_0indexed']])
pres={k:wirt.wirtinger(L)[:2] for k,L in objs.items()}
for k,(n,r) in pres.items(): print(k,'arcs',n,'rels',len(r),flush=True)
res={}
for gname,G in GROUPS:
    H.count_homs.G=G
    for ci,cl in enumerate(G.classes):
        g=cl[0]
        if g==G.e: continue
        tag=f'{gname}|cls{ci}|ord{order_of(G,g)}|size{len(cl)}'
        row={}
        for k,(n,rels) in pres.items():
            dom={x:cl for x in range(1,n+1)}; dom[1]=[g]
            t0=time.time(); c,st=H.count_homs(n,rels,[],dom); row[k]=c
            print(f'  {tag} {k}={c} ({time.time()-t0:.1f}s nodes={st["nodes"]})',flush=True)
        res[tag]=row
        print(f'{tag}: 6_3={row["6_3"]} K_1={row["K_1"]} | 63*K1={row["6_3"]*row["K_1"]} 63^2={row["6_3"]**2} | storedD01={row["D_0_1"]}',flush=True)
        json.dump(res,open('counts2.json','w'),indent=1)
