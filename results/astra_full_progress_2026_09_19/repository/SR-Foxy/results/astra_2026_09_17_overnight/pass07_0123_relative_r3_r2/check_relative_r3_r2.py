#!/usr/bin/env python3
"""Exact pure-Python audit of the first crossed-axis unlink move.

Reconstructs pass06's two-band 62-crossing marked diagram from the stored
54-crossing scaffold, then applies the exact combinatorial Reidemeister-III
rewiring used by Spherogram followed by Reidemeister II.

No SnapPy/Spherogram import, floating point, knot table, or random search.
"""
from collections import defaultdict, deque
from copy import deepcopy
import json

PD = [
[31,22,32,23],[19,66,20,67],[1,18,2,19],[0,8,1,7],[6,0,7,67],[30,4,31,3],
[29,85,30,84],[28,68,29,75],[27,10,28,11],[81,27,82,26],[72,26,73,25],[13,24,14,25],
[2,24,3,23],[86,21,87,22],[20,87,21,76],[69,16,70,17],[78,17,79,18],[15,70,16,71],
[14,79,15,80],[73,12,74,13],[82,11,83,12],[68,10,69,9],[77,9,78,8],[5,77,6,76],
[85,5,86,4],[83,75,84,74],[71,81,72,80],[41,33,42,32],[65,45,66,44],[45,63,46,62],
[56,63,57,64],[64,57,65,58],[60,33,61,34],[103,35,104,34],[94,36,95,35],[53,37,54,36],
[37,101,38,100],[38,92,39,91],[39,51,40,50],[40,61,41,62],[42,105,43,106],[106,43,107,44],
[47,88,48,89],[46,97,47,98],[89,48,90,49],[98,49,99,50],[51,92,52,93],[52,101,53,102],
[54,88,55,95],[55,97,56,96],[107,59,96,58],[59,105,60,104],[93,102,94,103],[99,90,100,91]]
BAND1={"along_top":[[15,2],[16,2],[2,2],[41,0]],"arc_is_under":[False,False],"twist":0}
BAND2={"along_top":[[13,2],[27,0],[32,2],[52,0]],"arc_is_under":[False,False],"twist":0}
EXPECTED_ETA=[[0,1,2,3],[4,0,3,5],[2,6,7,8],[9,7,6,10],[1,11,9,10],[4,5,8,11]]

def adjacency(pd):
    occ=defaultdict(list)
    for c,row in enumerate(pd):
        for p,e in enumerate(row): occ[e].append((c,p))
    assert all(len(v)==2 for v in occ.values())
    A={c:[None]*4 for c in range(len(pd))}
    for a,b in occ.values(): A[a[0]][a[1]]=b; A[b[0]][b[1]]=a
    return A

def conn(A,a,b): A[a[0]][a[1]]=b; A[b[0]][b[1]]=a

def components(A,active=None):
    if active is None: active=set(A)
    nodes={(c,p) for c in active for p in range(4)}; seen=set(); ans=[]
    for st in sorted(nodes):
        if st in seen: continue
        stack=[st]; C=set()
        while stack:
            x=stack.pop()
            if x in C: continue
            C.add(x); seen.add(x); c,p=x
            y=A[c][p]
            if y[0] not in active: raise RuntimeError("edge leaves active crossing set")
            for q in (y,(c,(p+2)%4)):
                if q not in C: stack.append(q)
        ans.append(C)
    return ans

def component_map(A,active=None):
    cs=components(A,active); w={}
    for i,C in enumerate(cs):
        for x in C:w[x]=i
    return cs,w

def add_zero_band(A,b):
    A={c:list(v) for c,v in A.items()}; along=[tuple(x) for x in b["along_top"]]
    bits=b["arc_is_under"]; assert b["twist"]==0 and len(bits)==len(along)-2
    X,Z=along[0],along[-1]; Y,W=A[X[0]][X[1]],A[Z[0]][Z[1]]
    mids=along[1:-1]; opp=[A[c][p] for c,p in mids]; n=max(A)+1
    Bs=list(range(n,n+len(mids))); Cs=list(range(n+len(mids),n+2*len(mids)))
    for c in Bs+Cs:A[c]=[None]*4
    for i,((ac,ap),(dc,dp)) in enumerate(zip(mids,opp)):
        B,C=Bs[i],Cs[i]
        if bits[i]: conn(A,(ac,ap),(B,2));conn(A,(dc,dp),(C,0));conn(A,(B,0),(C,2))
        else: conn(A,(ac,ap),(B,3));conn(A,(dc,dp),(C,1));conn(A,(B,1),(C,3))
    upper,lower=X,Y
    for i,bit in enumerate(bits):
        B,C=Bs[i],Cs[i]
        if bit: conn(A,upper,(B,3));conn(A,lower,(C,3));upper,lower=(B,1),(C,1)
        else: conn(A,upper,(B,0));conn(A,lower,(C,0));upper,lower=(B,2),(C,2)
    conn(A,upper,Z);conn(A,lower,W)
    assert all(all(x is not None for x in row) for row in A.values())
    return A

def edgekey(A,p): return tuple(sorted((p,A[p[0]][p[1]])))

def delete_component_pd(A,active,remove_comp):
    cs,cmap=component_map(A,active); parent={}
    def find(x):
        parent.setdefault(x,x)
        if parent[x]!=x: parent[x]=find(parent[x])
        return parent[x]
    def union(a,b):
        a,b=find(a),find(b)
        if a!=b: parent[a]=b
    for c in active:
        for p in range(4):find(edgekey(A,(c,p)))
    kept=[]
    for c in sorted(active):
        k0=cmap[(c,0)]!=remove_comp; k1=cmap[(c,1)]!=remove_comp
        if k0 and k1: kept.append(c)
        elif k0: union(edgekey(A,(c,0)),edgekey(A,(c,2)))
        elif k1: union(edgekey(A,(c,1)),edgekey(A,(c,3)))
    labels={}; pd=[]
    for c in kept:
        row=[]
        for p in range(4):
            r=find(edgekey(A,(c,p)))
            if r not in labels: labels[r]=len(labels)
            row.append(labels[r])
        pd.append(row)
    return pd,kept

def faces(A,active):
    corners={(c,p) for c in active for p in range(4)}; out=[]
    while corners:
        st=min(corners); cur=st; face=[]
        while True:
            corners.remove(cur); face.append(cur); c,p=cur
            cur=A[c][(p+1)%4]
            if cur==st: break
        out.append(face)
    return out

def possible_r3(A,active):
    out=[]
    for f in faces(A,active):
        if len(f)!=3 or sum(p%2 for c,p in f) not in (1,2): continue
        f=f[:]
        for _ in range(3):
            if f[1][1]%2==0 and f[2][1]%2==1: break
            f=f[1:]+f[:1]
        else: continue
        if len({c for c,p in f})==3: out.append(f)
    return out

def r3(A,triple):
    A=deepcopy(A); (aa,a),(bb,b),(cc,c)=triple; m=lambda x:x%4
    old=[(cc,m(c-1)),(cc,m(c-2)),(aa,m(a-1)),(aa,m(a-2)),(bb,m(b-1)),(bb,m(b-2))]
    new=[(aa,m(a)),(bb,m(b+1)),(bb,m(b)),(cc,m(c+1)),(cc,m(c)),(aa,m(a+1))]
    outs=[A[u[0]][u[1]] for u in old]
    for u,v in zip(new,outs): conn(A,u,v)
    conn(A,(aa,m(a-1)),(bb,m(b+2)))
    conn(A,(bb,m(b-1)),(cc,m(c+2)))
    conn(A,(cc,m(c-1)),(aa,m(a+2)))
    return A

def r2_candidates(A,active):
    out=[]
    for aa in sorted(active):
        for a in range(4):
            bb,b=A[aa][a]; cc,c=A[aa][(a+1)%4]
            if bb in active and cc in active and bb==cc and (b-1)%4==c and (a+b)%2==0:
                out.append((aa,bb,a,b))
    return out

def r2_remove(A,active,mv):
    A=deepcopy(A); active=set(active); aa,bb,a,b=mv
    W,w=A[aa][(a+2)%4]; X,x=A[aa][(a+3)%4]; Y,y=A[bb][(b+1)%4]; Z,z=A[bb][(b+2)%4]
    if W!=bb: conn(A,(W,w),(Z,z))
    if X!=bb: conn(A,(X,x),(Y,y))
    active.remove(aa);active.remove(bb)
    return A,active

def canonical(A,active): return tuple((c,tuple(A[c])) for c in sorted(active))

def bounded_unlock_search(A,active,target={25,52},max_depth=4):
    q=deque([(A,set(active),[])]); seen={canonical(A,active)}; expanded=0
    while q:
        D,S,path=q.popleft()
        for mv in r2_candidates(D,S):
            if {mv[0],mv[1]}==target: return {"status":"FOUND","depth":len(path),"path":path,"r2":mv,"states":len(seen)}
        if len(path)>=max_depth: continue
        for tri in possible_r3(D,S):
            N=r3(D,tri); k=canonical(N,S)
            if k in seen: continue
            seen.add(k); expanded+=1; q.append((N,set(S),path+[tri]))
    return {"status":"NO_TARGET_R2_THROUGH_DEPTH","depth":max_depth,"states":len(seen),"expanded":expanded}

def bounded_any_eta_r2_search(A,active,max_depth=4):
    q=deque([(A,set(active),[])]); seen={canonical(A,active)}; expanded=0
    while q:
        D,S,path=q.popleft(); cs,cmap=component_map(D,S); rcomp=cmap[(0,0)]
        eta_cross={c for c in S if cmap[(c,0)]!=rcomp and cmap[(c,1)]!=rcomp}
        for mv in r2_candidates(D,S):
            if mv[0] in eta_cross and mv[1] in eta_cross:
                return {"status":"FOUND_ETA_R2","depth":len(path),"path":path,"r2":mv,"states":len(seen)}
        if len(path)>=max_depth: continue
        for tri in possible_r3(D,S):
            N=r3(D,tri); k=canonical(N,S)
            if k in seen: continue
            seen.add(k); expanded+=1; q.append((N,set(S),path+[tri]))
    return {"status":"NO_ETA_R2_THROUGH_DEPTH","depth":max_depth,"states":len(seen),"expanded":expanded}

def main():
    A=adjacency(PD);A=add_zero_band(A,BAND1);A=add_zero_band(A,BAND2);active=set(A)
    cs,cmap=component_map(A,active); assert [len(C)//2 for C in cs]==[74,26,24]
    rcomp=cmap[(0,0)]; eta0,kept0=delete_component_pd(A,active,rcomp); assert eta0==EXPECTED_ETA
    for c in (17,18):
        assert cmap[(c,0)]==rcomp and cmap[(c,2)]==rcomp
        assert cmap[(c,1)]!=rcomp and cmap[(c,3)]!=rcomp
    triangles=[t for t in possible_r3(A,active) if {c for c,p in t}=={17,18,26}]
    assert triangles==[[(17,3),(18,2),(26,3)]],triangles
    tri=triangles[0]
    assert A[17][0]==(18,2)
    A1=r3(A,tri)
    hits=[m for m in r2_candidates(A1,active) if {m[0],m[1]}=={26,56}]
    assert hits==[(26,56,3,1),(56,26,0,0)],hits
    A2,active2=r2_remove(A1,active,hits[0])
    assert len(active2)==60
    cs2,cmap2=component_map(A2,active2); assert len(cs2)==3
    rcomp2=cmap2[(0,0)]; eta1,kept1=delete_component_pd(A2,active2,rcomp2)
    assert len(eta1)==4 and len(components(adjacency(eta1)))==2
    etaA=adjacency(eta1); etaactive=set(etaA); eta_r2=[]
    while etaactive:
        cand=r2_candidates(etaA,etaactive)
        if not cand: break
        mv=cand[0];eta_r2.append(mv);etaA,etaactive=r2_remove(etaA,etaactive,mv)
    assert not etaactive and len(eta_r2)==2
    assert r2_candidates(A2,active2)==[]
    search=bounded_unlock_search(A2,active2,max_depth=4)
    assert search["status"]=="NO_TARGET_R2_THROUGH_DEPTH"
    any_search=bounded_any_eta_r2_search(A2,active2,max_depth=4)
    assert any_search["status"]=="NO_ETA_R2_THROUGH_DEPTH"
    result={
      "status":"FIRST_RELATIVE_UNLINK_MOVE_CERTIFIED_NO_COUNTEREXAMPLE","counterexample":False,
      "input_main_commit":"9d4634224db3c32dce419e67510c994111bd7502",
      "bands":["a40a423e_0_0","d0826c36_0_0"],
      "initial_full_crossings":62,"initial_eta_sublink_crossings":6,
      "certified_full_link_isotopy":[{"move":"RIII","triangle":tri,"crossing_set":[17,18,26]},{"move":"RII","data":hits[0],"crossing_set":[26,56]}],
      "local_height_check":"At crossings 17 and 18, R occupies ports 0,2 (the under-strand) and eta occupies ports 1,3 (the over-strand). The same R strand joins the two mixed crossings. Thus the standard RIII can be realized by moving the two eta strands in the upper half of a local ball while keeping the bottom R strand fixed pointwise; projection alone did not obstruct the move.",
      "after_move_full_crossings":60,"after_move_eta_sublink_crossings":4,"after_move_eta_sublink_pd":eta1,
      "eta_only_remaining_RII_moves_after_deleting_R":eta_r2,"full_link_immediate_RII_after_move":[],
      "rIII_only_unlock_search_for_next_eta_pair":search,"rIII_only_search_for_any_eta_RII":any_search,
      "scope":["This corrects pass06's claim that the first eta RII cancellation is blocked by R.","The first RIII is supported off R because R is the bottom strand at both mixed crossings; together with the eta-eta RII this certifies the first eta cancellation by an isotopy in S3\\R. It still does not supply an annulus in the product-disk exterior.","The remaining four-crossing eta configuration is not certified unlink relative to R.","The depth-4 RIII search is finite diagram search only, not an obstruction theorem.","No surgery framing, boundary-knot identity, Park 0-standardness, or slice disk is certified."],
      "source_code_dependency":"Reidemeister-III rewiring and face criterion ported literally from Spherogram simplify.py; next_corner port rule from links_base.py."
    }
    print("PASS reconstruct explicit two-band 62-crossing marked diagram")
    print("PASS identify full-diagram RIII triangle (17,18,26)")
    print("PASS after RIII, crossings 26 and 56 admit exact full-diagram RII")
    print("PASS resulting full diagram has 60 crossings and eta sublink has 4")
    print("PASS eta-only residual is still the unlink after deleting R")
    print("PASS no immediate full-link RII; no eta-eta RII appears through exhaustive RIII depth 4")
    print(json.dumps(result,indent=2))
    return result
if __name__=='__main__':main()
