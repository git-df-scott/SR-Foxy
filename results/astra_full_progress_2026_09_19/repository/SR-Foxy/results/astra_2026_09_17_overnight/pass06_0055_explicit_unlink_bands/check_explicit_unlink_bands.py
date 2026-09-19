#!/usr/bin/env python3
"""Standalone exact checker for one explicit crossed-axis band pair.

No SnapPy/Spherogram dependency. This reimplements only the small pieces of
Spherogram's documented PD/band combinatorics needed for this certificate:
- PD adjacency and link-component connectivity,
- the zero-twist case of add_one_band,
- deleting one component and smoothing mixed crossings,
- exact Reidemeister-II recognition/removal.

It does NOT certify an embedded annulus in the product-disk exterior.
"""
from collections import defaultdict
import json

SOURCE_COMMIT = "70c6e7edfae59ecd042ae2d72dea851a0142f23d"
SOURCE_PATH = "data/knots/AbeTagami_marked_product_scaffold.json"

PD = [
[31,22,32,23],[19,66,20,67],[1,18,2,19],[0,8,1,7],[6,0,7,67],[30,4,31,3],
[29,85,30,84],[28,68,29,75],[27,10,28,11],[81,27,82,26],[72,26,73,25],[13,24,14,25],
[2,24,3,23],[86,21,87,22],[20,87,21,76],[69,16,70,17],[78,17,79,18],[15,70,16,71],
[14,79,15,80],[73,12,74,13],[82,11,83,12],[68,10,69,9],[77,9,78,8],[5,77,6,76],
[85,5,86,4],[83,75,84,74],[71,81,72,80],[41,33,42,32],[65,45,66,44],[45,63,46,62],
[56,63,57,64],[64,57,65,58],[60,33,61,34],[103,35,104,34],[94,36,95,35],[53,37,54,36],
[37,101,38,100],[38,92,39,91],[39,51,40,50],[40,61,41,62],[42,105,43,106],[106,43,107,44],
[47,88,48,89],[46,97,47,98],[89,48,90,49],[98,49,99,50],[51,92,52,93],[52,101,53,102],
[54,88,55,95],[55,97,56,96],[107,59,96,58],[59,105,60,104],[93,102,94,103],[99,90,100,91]
]

BAND1 = {
    "along_top": [[15,2],[16,2],[2,2],[41,0]],
    "arc_is_under": [False,False],
    "twist": 0,
    "compressed_spec": "a40a423e_0_0",
    "intended_pair": ["c1_upper","c2_lower"],
}
BAND2 = {
    "along_top": [[13,2],[27,0],[32,2],[52,0]],
    "arc_is_under": [False,False],
    "twist": 0,
    "compressed_spec": "d0826c36_0_0",
    "intended_pair": ["c2_upper","c1_lower"],
}

EXPECTED_ETA_PD = [
    [0,1,2,3],
    [4,0,3,5],
    [2,6,7,8],
    [9,7,6,10],
    [1,11,9,10],
    [4,5,8,11],
]
EXPECTED_R2 = [
    ["R2",1,5,3,1],
    ["R2",0,2,2,0],
    ["R2",3,4,0,2],
]

def adjacency_from_pd(pd):
    occ = defaultdict(list)
    for c,row in enumerate(pd):
        assert len(row) == 4
        for p,e in enumerate(row):
            occ[e].append((c,p))
    assert all(len(v) == 2 for v in occ.values())
    adj = {c:[None]*4 for c in range(len(pd))}
    for a,b in occ.values():
        adj[a[0]][a[1]] = b
        adj[b[0]][b[1]] = a
    return adj

def components(adj):
    nodes = {(c,p) for c in adj for p in range(4)}
    seen, ans = set(), []
    for start in sorted(nodes):
        if start in seen:
            continue
        stack, cc = [start], set()
        while stack:
            c,p = stack.pop()
            if (c,p) in cc:
                continue
            cc.add((c,p)); seen.add((c,p))
            for q in (adj[c][p], (c,(p+2)%4)):
                if q not in cc:
                    stack.append(q)
        ans.append(cc)
    return ans

def component_map(adj):
    cs = components(adj)
    where = {}
    for i,cc in enumerate(cs):
        for x in cc:
            where[x] = i
    return cs, where

def connect(adj, a, b):
    adj[a[0]][a[1]] = b
    adj[b[0]][b[1]] = a

def compress_crossing_strands(seq):
    cmax = max(c for c,s in seq)
    nibbles = 2 if cmax < 64 else 3
    prefix = "" if cmax < 64 else "Z"
    x = 0
    for c,s in reversed(seq):
        x = (x << (4*nibbles)) + (c << 2) + s
    return prefix + f"{x:02x}".rjust(nibbles*len(seq), "0")

def compressed_spec(band):
    bits = sum((1 << i) for i,v in enumerate(band["arc_is_under"]) if v)
    return (compress_crossing_strands(band["along_top"]) + "_" +
            hex(bits)[2:] + "_" + str(band["twist"]))

def add_zero_twist_band(adj, band):
    assert band["twist"] == 0
    A = {c:list(v) for c,v in adj.items()}
    along = [tuple(x) for x in band["along_top"]]
    bits = band["arc_is_under"]
    assert len(bits) == len(along)-2
    X, Z = along[0], along[-1]
    Y, W = A[X[0]][X[1]], A[Z[0]][Z[1]]
    mids = along[1:-1]
    opposites = [A[c][p] for c,p in mids]
    next_id = max(A)+1
    Bs = list(range(next_id, next_id+len(mids)))
    Cs = list(range(next_id+len(mids), next_id+2*len(mids)))
    for c in Bs+Cs:
        A[c] = [None]*4
    for i,((ac,ap),(dc,dp)) in enumerate(zip(mids,opposites)):
        B,C = Bs[i],Cs[i]
        if bits[i]:
            connect(A,(ac,ap),(B,2))
            connect(A,(dc,dp),(C,0))
            connect(A,(B,0),(C,2))
        else:
            connect(A,(ac,ap),(B,3))
            connect(A,(dc,dp),(C,1))
            connect(A,(B,1),(C,3))
    upper, lower = X, Y
    for i,bit in enumerate(bits):
        B,C = Bs[i],Cs[i]
        if bit:
            connect(A,upper,(B,3)); connect(A,lower,(C,3))
            upper,lower = (B,1),(C,1)
        else:
            connect(A,upper,(B,0)); connect(A,lower,(C,0))
            upper,lower = (B,2),(C,2)
    connect(A,upper,Z)
    connect(A,lower,W)
    assert all(all(x is not None for x in row) for row in A.values())
    return A

def edge_key(adj, port):
    other = adj[port[0]][port[1]]
    return tuple(sorted((port,other)))

def sublink_delete_component(adj, remove_comp):
    cs,cmap = component_map(adj)
    parent = {}
    def find(x):
        parent.setdefault(x,x)
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    def union(a,b):
        a,b = find(a),find(b)
        if a != b:
            parent[a] = b
    for c in adj:
        for p in range(4):
            find(edge_key(adj,(c,p)))
    kept = []
    for c in sorted(adj):
        k0 = cmap[(c,0)] != remove_comp
        k1 = cmap[(c,1)] != remove_comp
        if k0 and k1:
            kept.append(c)
        elif k0:
            union(edge_key(adj,(c,0)), edge_key(adj,(c,2)))
        elif k1:
            union(edge_key(adj,(c,1)), edge_key(adj,(c,3)))
    labels, pd = {}, []
    for c in kept:
        row = []
        for p in range(4):
            r = find(edge_key(adj,(c,p)))
            if r not in labels:
                labels[r] = len(labels)
            row.append(labels[r])
        pd.append(row)
    return pd, kept

def r2_simplify(pd):
    A = adjacency_from_pd(pd)
    active = set(A)
    moves = []
    def conn(x,y):
        A[x[0]][x[1]] = y
        A[y[0]][y[1]] = x
    while True:
        found = None
        for aid in sorted(active):
            for a in range(4):
                B,b = A[aid][a]
                C,c = A[aid][(a+1)%4]
                if (B in active and C in active and B == C and
                    (b-1)%4 == c and (a+b)%2 == 0):
                    found = (aid,B,a,b)
                    break
            if found:
                break
        if not found:
            break
        aid,bid,a,b = found
        W,w = A[aid][(a+2)%4]
        X,x = A[aid][(a+3)%4]
        Y,y = A[bid][(b+1)%4]
        Z,z = A[bid][(b+2)%4]
        if W != bid:
            conn((W,w),(Z,z))
        if X != bid:
            conn((X,x),(Y,y))
        active.remove(aid); active.remove(bid)
        moves.append(["R2",aid,bid,a,b])
    return moves, active

def trace_smoothed_edge(full_adj, retained, start):
    """Follow an eta arc through deleted mixed crossings to next retained crossing."""
    retained = set(retained)
    nxt = full_adj[start[0]][start[1]]
    inter = []
    seen = set()
    while nxt[0] not in retained:
        if nxt in seen:
            raise RuntimeError("unexpected loop")
        seen.add(nxt)
        c,p = nxt
        inter.append(c)
        nxt = full_adj[c][(p+2)%4]
    return nxt, inter

def main():
    assert compressed_spec(BAND1) == BAND1["compressed_spec"]
    assert compressed_spec(BAND2) == BAND2["compressed_spec"]
    initial = adjacency_from_pd(PD)
    cs0,cmap0 = component_map(initial)
    initial_lengths = [len(c)//2 for c in cs0]
    assert initial_lengths == [68,12,8,12,8]
    raw_names = {0:"R",1:"c2_upper",2:"c1_upper",3:"c2_lower",4:"c1_lower"}
    assert raw_names[cmap0[tuple(BAND1["along_top"][0])]] == "c1_upper"
    assert raw_names[cmap0[tuple(BAND1["along_top"][-1])]] == "c2_lower"

    once = add_zero_twist_band(initial,BAND1)
    cs1,cmap1 = component_map(once)
    assert len(once) == 58 and len(cs1) == 4
    assert cmap1[tuple(BAND2["along_top"][0])] != cmap1[tuple(BAND2["along_top"][-1])]

    final = add_zero_twist_band(once,BAND2)
    csf,cmapf = component_map(final)
    final_lengths = [len(c)//2 for c in csf]
    assert len(final) == 62 and len(csf) == 3
    assert final_lengths == [74,26,24]

    r_comp = cmapf[(0,0)]
    eta_pd, retained = sublink_delete_component(final,r_comp)
    assert eta_pd == EXPECTED_ETA_PD
    eta_cs = components(adjacency_from_pd(eta_pd))
    assert [len(c)//2 for c in eta_cs] == [6,6]

    moves, active = r2_simplify(eta_pd)
    assert moves == EXPECTED_R2
    assert not active

    assert retained[1] == 26 and retained[5] == 56
    end4,path4 = trace_smoothed_edge(final,retained,(26,0))
    end5,path5 = trace_smoothed_edge(final,retained,(26,3))
    assert end4 == (56,0) and path4 == [17]
    assert end5 == (56,1) and path5 == [18]
    assert final[17][0] == (18,2) and final[18][2] == (17,0)

    result = {
        "status":"EXPLICIT_CROSSED_BANDS_BOUNDARY_IS_UNLINK_NO_COUNTEREXAMPLE",
        "source_commit":SOURCE_COMMIT,
        "source_path":SOURCE_PATH,
        "band1":BAND1,
        "band2":BAND2,
        "initial_component_lengths":initial_lengths,
        "final_crossings":len(final),
        "final_component_lengths":final_lengths,
        "eta_sublink_pd":eta_pd,
        "eta_sublink_components":2,
        "eta_sublink_crossings":len(eta_pd),
        "reidemeister_II_sequence":moves,
        "reidemeister_result":"zero-crossing two-component diagram; hence the 2-component unlink",
        "first_unlinking_bigon_relative_to_R":{
            "eta_crossings_full":[26,56],
            "side_1_mixed_crossings":path4,
            "side_2_mixed_crossings":path5,
            "R_edge_connects":[[17,0],[18,2]],
            "conclusion":"the first RII move is not available in the complement of R"
        },
        "scope":[
            "This certifies the two NEW boundary curves form L_0 in S^3.",
            "It does not certify an annulus between them in the product-disk exterior.",
            "It does not compute their based words in the product-disk group.",
            "It does not certify Park 0-standardness, surgery boundary knot identity, or a slice disk."
        ],
        "counterexample":False,
    }
    print("PASS scaffold component structure")
    print("PASS band specs", BAND1["compressed_spec"], BAND2["compressed_spec"])
    print("PASS explicit crossed pair gives 3-component full diagram")
    print("PASS eta1 union eta2 reduces by 3 RII moves to the 2-component unlink")
    print("PASS first unlinking bigon is pierced by one R strand in the full marked diagram")
    print(json.dumps(result,indent=2))
    return result

if __name__ == "__main__":
    main()
