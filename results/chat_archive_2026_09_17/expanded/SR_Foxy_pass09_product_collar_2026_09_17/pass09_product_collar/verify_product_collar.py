#!/usr/bin/env python3
"""Exact group gate for one specified Dehn-region collar map.

The program proves an equality in the source presentation, NOT the existence of
an embedded annulus, a slice disk for D01, or the geometric identity of the collar
map with the previously unmarked product-disk boundary parametrization.
Python standard library only. No network and no repository writes.
"""
from __future__ import annotations
import argparse, hashlib, json, time
from pathlib import Path
import diagram_core as g


def red(w):
    ans=[]
    for x in w:
        if ans and ans[-1]==-x:ans.pop()
        else:ans.append(x)
    return tuple(ans)
def inv(w):return tuple(-x for x in w[::-1])
def mul(*ws):return red(x for w in ws for x in w)
def power(w,n):return mul(*([w if n>=0 else inv(w)]*abs(n)))
def subst(w,m):return mul(*(m.get(x,(x,)) if x>0 else inv(m.get(-x,(-x,))) for x in w))
def cyclic(w):
    w=red(w)
    while len(w)>1 and w[0]==-w[-1]:w=w[1:-1]
    return w
def clean(rs):
    ans=[];seen=set()
    for w in rs:
        w=cyclic(w)
        if not w:continue
        k=min(v[i:]+v[:i] for v in (w,inv(w)) for i in range(len(v)))
        if k not in seen:seen.add(k);ans.append(w)
    return ans


def rules(rs):
    ans={}
    for k,w in enumerate(rs):
        for sign,v in ((1,w),(-1,inv(w))):
            for shift in range(len(v)):
                z=v[shift:]+v[:shift]
                for cut in range(len(z)//2+1,len(z)+1):
                    ans[z[:cut]]=(inv(z[cut:]),(k,sign,shift,cut))
    return sorted(ans.items(),key=lambda x:-len(x[0]))


def replay(initial, trace, rs):
    # Independent reduction of a word by the *recorded* relator applications.
    def cancel(w):
        w=list(w);i=0
        while i+1<len(w):
            if w[i]==-w[i+1]:del w[i:i+2];i=max(0,i-1)
            else:i+=1
        return tuple(w)
    w=cancel(initial)
    for pos,(idx,sign,shift,cut) in trace:
        r=rs[idx] if sign==1 else tuple(-x for x in reversed(rs[idx]))
        r=r[shift:]+r[:shift];a=r[:cut];b=tuple(-x for x in reversed(r[cut:]))
        assert w[pos:pos+len(a)]==a
        w=cancel(w[:pos]+b+w[pos+len(a):])
    return w


def reduce_proven(word, rs):
    initial=tuple(word);w=red(word);rr=rules(rs);trace=[]
    while True:
        found=False
        for a,(b,certificate) in rr:
            for pos in range(len(w)-len(a)+1):
                if w[pos:pos+len(a)]==a:
                    w=mul(w[:pos],b,w[pos+len(a):]);trace.append((pos,certificate));found=True;break
            if found:break
        if not found:break
    assert replay(initial,trace,rs)==w
    return w,trace


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if not __debug__:raise RuntimeError('Do not disable assertions')
    if args.output.exists():raise FileExistsError(args.output)
    start=time.monotonic();checks=0
    A=g.adjacency_from_pd(g.SCAFFOLD)
    seams=[(c,p,A[c][p]) for c in range(27) for p in range(4) if A[c][p][0]>=27]
    assert seams==[(0,2,(27,3)),(1,1,(28,2))]
    U={c:list(A[c]) for c in range(27)}
    L={c-27:[(d-27,p) for d,p in A[c]] for c in range(27,54)}
    g.connect(U,(0,2),(1,1));g.connect(L,(0,3),(1,2))
    shift={0:1}
    while len(shift)<27:
        old=len(shift)
        for c,s in list(shift.items()):
            for p,(d,q) in enumerate(U[c]):
                dl,ql=L[c][(p+s)%4];assert d==dl
                sd=(ql-q)%4;assert d not in shift or shift[d]==sd;shift[d]=sd
        assert len(shift)>old
    for c,s in shift.items():
        assert s in (1,3)
        for p,(d,q) in enumerate(U[c]):assert L[c][(p+s)%4]==(d,(q+shift[d])%4);checks+=1
    qu=g.quotient_R_wirtinger(U);q0=g.quotient_R_wirtinger(A)
    nr=1+max(qu['arcs'].values());assert nr==9
    rels=[mul(power((b+1,),-s),(i+1,),power((b+1,),s),(-o-1,)) for i,o,b,s,c in qu['relations']]
    initial_rels=rels[:];images={i:(i,) for i in range(1,nr+1)};eliminations=[]
    while True:
        rels=clean(rels)
        choices=[(len(w),x,ri) for ri,w in enumerate(rels) for x in set(map(abs,w)) if sum(abs(t)==x for t in w)==1]
        if not choices:break
        _,x,ri=min(choices);w=rels[ri];j=next(i for i,t in enumerate(w) if abs(t)==x)
        v=mul(inv(w[:j]),inv(w[j+1:]));v=v if w[j]>0 else inv(v)
        assert subst(w,{x:v})==();checks+=1
        eliminations.append({'generator':x,'relator':w,'image':v})
        images={i:subst(z,{x:v}) for i,z in images.items()}
        rels=[subst(z,{x:v}) for i,z in enumerate(rels) if i!=ri]
    original_reduced=rels[:];short=rels[:];derived=[]
    for _ in range(10):
        change=False
        for i,w in enumerate(short):
            other=short[:i]+short[i+1:]
            candidates=[]
            for j in range(len(w)):
                z=w[j:]+w[:j];end,trace=reduce_proven(z,other)
                candidates.append((len(cyclic(end)),cyclic(end),j,z,end,trace))
            _,best,j,z,end,trace=min(candidates)
            if len(best)<len(w):
                assert cyclic(replay(z,trace,other))==best
                derived.append({'start':z,'rules':other,'trace':trace,'end_before_cyclic_reduction':end,'new_relator':best})
                short[i]=best;change=True
        short=clean(short)
        if not change:break
    rule_rels=original_reduced+short
    for w in initial_rels:
        assert reduce_proven(subst(w,images),rule_rels)[0]==();checks+=1
    # Region (c,p) means sector between ports p and p+1.
    parent={(c,p):(c,p) for c in U for p in range(4)}
    def root(x):
        while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
        return x
    def join(a,b):parent[root(a)]=root(b)
    for c in U:
        for p,(d,q) in enumerate(U[c]):join((c,p),(d,(q-1)%4));join((c,(p-1)%4),(d,q))
    roots=sorted({root(x) for x in parent});rid={z:i for i,z in enumerate(roots)};face={x:rid[root(x)] for x in parent}
    assert len(roots)==29
    base=face[0,2];constraints=[]
    for c in U:
        for p in range(4):
            fl,fr=face[c,p],face[c,(p-1)%4]
            if (c,p) in qu['incoming']:fl,fr=fr,fl
            w=images[qu['arcs'][c,p]+1] if qu['cmap'][c,p]==0 else ()
            constraints.append((fl,fr,inv(w)))
    regions={base:()}
    while True:
        change=False
        for fl,fr,w in constraints:
            if fr in regions and fl not in regions:regions[fl]=mul(w,regions[fr]);change=True
            elif fl in regions and fr not in regions:regions[fr]=mul(inv(w),regions[fl]);change=True
        if not change:break
    assert len(regions)==29
    for fl,fr,w in constraints:
        assert reduce_proven(mul(regions[fl],inv(regions[fr]),inv(w)),rule_rels)[0]==();checks+=1
    col={};arc_consistency=[]
    for (c,p),a in qu['arcs'].items():
        fl,fr=face[c,p],face[c,(p-1)%4]
        if (c,p) in qu['incoming']:fl,fr=fr,fl
        w=mul(inv(regions[fl]),regions[fr]);ap=q0['arcs'][c+27,(p+shift[c])%4]
        if ap in col:arc_consistency.append(mul(col[ap],inv(w)))
        col.setdefault(ap,w)
    for (c,p),a in qu['arcs'].items():
        ap=q0['arcs'][c,p];w=images[a+1]
        if ap in col:arc_consistency.append(mul(col[ap],inv(w)))
        col[ap]=w
    for z in arc_consistency:assert reduce_proven(z,rule_rels)[0]==();checks+=1
    for i,o,b,s,c in q0['relations']:
        assert reduce_proven(mul(power(col[b],-s),col[i],power(col[b],s),inv(col[o])),rule_rels)[0]==();checks+=1
    F=g.add_zero_twist_band(g.add_zero_twist_band(A,g.BAND1),g.BAND2)
    qf=g.quotient_R_wirtinger(F);fmap=g.map_final_R_arcs_to_scaffold(q0,qf)
    def axis_word(comp):
        cur=min(qf['components'][comp]);seen=set();word=()
        while cur not in seen:
            seen.add(cur);c,p=cur
            if p in (0,2) and qf['cmap'][c,1]==qf['cmap'][c,3]==0:
                word=mul(word,power(col[fmap[qf['arcs'][c,1]]],qf['signs'][c]))
            cur=F[c][(p+2)%4]
        return word
    e1,e2=axis_word(1),axis_word(2)
    a,ta=reduce_proven(e1,rule_rels);b,tb=reduce_proven(e2,rule_rels)
    assert a==b;checks+=1
    difference,td=reduce_proven(mul(e1,inv(e2)),rule_rels);assert not difference;checks+=1
    # Negative control: append one meridian; abelianization prevents nullity.
    bad=mul(e1,inv(e2),(5,));assert sum(1 if x>0 else -1 for x in bad)==1
    assert reduce_proven(bad,rule_rels)[0];checks+=1
    report={'status':'EXACT_GROUP_IDENTITY_FOR_SPECIFIED_COLLAR_MAP_GEOMETRIC_MATCH_NOT_CERTIFIED','CE':False,'source_main':'f7ba2516304c0553a3180570abb6e257f4a68094','base_sector':[0,2],'base_region':base,'seams':seams,'mirror_port_rotations':shift,'source_relators':initial_rels,'tietze_eliminations':eliminations,'source_generator_images':images,'reduced_relators':original_reduced,'derived_relators':derived,'proof_rule_relators':rule_rels,'region_words':regions,'boundary_arc_images':col,'eta1_word':e1,'eta2_word':e2,'common_reduced_word':a,'eta1_reduction':ta,'eta2_reduction':tb,'difference_reduction':td,'exact_checks':checks,'seconds':time.monotonic()-start,'limitation':'All equalities are certified in the source presentation. The selected region/collar map must still be matched to the actual product-disk boundary parametrization. No embedded annulus, compression disk, surgery boundary, or D01 slice disk was constructed.'}
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','CE','base_sector','common_reduced_word','exact_checks','seconds')}))
if __name__=='__main__':main()
