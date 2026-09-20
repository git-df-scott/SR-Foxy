"""Independent standard-library check of the endpoint and all four RII moves.

No Spherogram import. Verify planar bigons, strand heights, smoothing, and
component counts, including the unswitched Hopf-link negative control.
"""
import hashlib
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def read_adj(raw):return {int(c):[tuple(x) for x in row] for c,row in raw.items()}

def valid(adj):
    assert all(len(row)==4 for row in adj.values())
    for c,row in adj.items():
        for p,y in enumerate(row):assert adj[y[0]][y[1]]==(c,p)

def components(adj):
    nodes={(c,p) for c in adj for p in range(4)};out=[]
    while nodes:
        start=min(nodes);stack=[start];cc=set()
        while stack:
            x=stack.pop()
            if x in cc:continue
            cc.add(x);c,p=x;stack.extend([adj[c][p],(c,(p+2)%4)])
        nodes-=cc;out.append(cc)
    return out

def faces(adj):
    todo={(c,p) for c in adj for p in range(4)};out=[]
    while todo:
        x=min(todo);start=x;cycle=[]
        while x not in cycle:
            todo.remove(x);cycle.append(x);x=adj[x[0]][(x[1]+1)%4]
        assert x==start;out.append(cycle)
    return out

def r2_bigons(adj,removed):
    result=[]
    for cycle in faces(adj):
        if len(cycle)!=2 or {x[0] for x in cycle}!=set(removed):continue
        # Each of the two strands must be over at both crossings or under
        # at both. A Hopf clasp has the OPPOSITE parity and cannot cancel.
        if all((p+1)%2==adj[c][(p+1)%4][1]%2 for c,p in cycle):result.append(cycle)
    return result

def smooth(adj,removed):
    removed=set(removed);out={c:list(row) for c,row in adj.items() if c not in removed}
    for c in out:
        for p in range(4):
            y=adj[c][p];visited=set()
            while y[0] in removed:
                assert y not in visited;visited.add(y)
                y=adj[y[0]][(y[1]+2)%4]
            out[c][p]=y
    vanished=sum(all(c in removed for c,p in cc) for cc in components(adj))
    return out,vanished

def cancel(w):
    out=[]
    for x in w:
        if out and out[-1]==-x:out.pop()
        else:out.append(x)
    return out

def even_port_isomorphism(a,b):
    """Spherogram may rotate a crossing by 180 degrees while orienting it."""
    assert set(a)==set(b)
    total={}
    while len(total)<len(a):
        seed=min(set(a)-set(total));solution=None
        for initial in [0,2]:
            shifts={seed:initial};queue=[seed];ok=True
            while queue and ok:
                c=queue.pop();s=shifts[c]
                for p,(d,q) in enumerate(a[c]):
                    bd,bq=b[c][(p+s)%4];sd=(bq-q)%4
                    if bd!=d or sd not in [0,2] or (d in shifts and shifts[d]!=sd):ok=False;break
                    if d not in shifts:shifts[d]=sd;queue.append(d)
            if ok:solution=shifts;break
        assert solution is not None,'Initial sublink changed more than an even port normalization'
        total.update(solution)
    return total

def main():
    d=json.loads((HERE/'A_ENDPOINT.json').read_text())
    for r in d['inputs']:assert hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256']
    end=read_adj(d['A_endpoint_adjacency']);target=read_adj(d['target_adjacency'])
    assert len(end)==len(target)==70
    for a in [end,target]:
        valid(a);assert len(faces(a))==len(a)+2;assert len(components(a))==4
    # Verify exactly ONE crossing switch, not an unnoticed rerouting.
    switch=d['transfer']['only_crossing_change'];assert switch==61
    rotate=lambda x:(x[0],(x[1]+1)%4) if x[0]==switch else x
    for c,row in target.items():
        for p,y in enumerate(row):
            x=rotate((c,p));assert end[x[0]][x[1]]==rotate(y)
    ee=components(end);cmap={x:i for i,cc in enumerate(ee) for x in cc}
    assert {cmap[switch,p] for p in range(4)}=={1,3}
    assert not any(all(cmap[c,p]==3 for p in range(4)) for c in end)
    # Derive each auxiliary diagram by deleting R and suppressing its mixed crossings.
    total_moves=0
    for trace,full in zip(d['auxiliary_unlink_replays'],[target,end]):
        cc=components(full);r_ports=cc[0]
        removed={c for c in full if any((c,p) in r_ports for p in range(4))}
        auxiliary,_=smooth(full,removed)
        normalized=read_adj(trace['initial']['adjacency'])
        even_port_isomorphism(auxiliary,normalized)
        assert len(auxiliary)==8 and len(components(auxiliary))==3
        current=normalized;unknots=0
        for move in trace['moves']:
            assert current==read_adj(move['before']['adjacency'])
            assert unknots==move['before']['unlinked_unknot_components']
            pair=move['removed'];assert len(pair)==2
            assert r2_bigons(current,pair),'No planar cancellable RII bigon'
            current,vanished=smooth(current,pair);unknots+=vanished
            assert current==read_adj(move['after']['adjacency'])
            assert unknots==move['after']['unlinked_unknot_components']
            valid(current);total_moves+=1
        assert current==read_adj(trace['final']['adjacency'])
        if trace['name']=='A_endpoint_switched':assert current=={} and unknots==3
        else:
            assert len(current)==2 and unknots==1
            assert not r2_bigons(current,list(current))  # negative control
    # Walk the actual based paths to the crossing before the local event.
    for key in ['A_traversal','A_prefix_to_intersection','a_prefix_to_intersection']:
        r=d[key];x=tuple(r['start']);word=[]
        for step in r['events']:
            assert x==tuple(step['incoming_port']);word+=step['R_letters']
            x=end[x[0]][(x[1]+2)%4]
        assert x==tuple(r['end']) and cancel(word)==r['R_word']
    pa=d['A_prefix_to_intersection']['R_word'];pp=d['a_prefix_to_intersection']['R_word']
    label=cancel(pa+[-x for x in reversed(pp)])
    assert label==d['transfer']['full_R_group_label']==[4,-3,1,-4]
    # The boundary word is A by ONE existing crossing-11 Wirtinger relation:
    # x1*x4*x1^-1=x3 => x1*x4^-1=x3^-1*x1.
    C=json.loads((ROOT/'results/astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json').read_text())
    assert [1,4,-1,-3] in C['boundary_relations']
    assert label[:2]+[-3,1]==[4,-3,-3,1]
    assert d['transfer']['sign']==-1
    assert d['transfer']['intersections_with_complete_Sigma'] is None
    report={'status':'PASS','full_diagram_crossings':70,'independent_RII_moves':total_moves,
            'A_endpoint_auxiliary_unlink_components':3,'unswitched_negative_control':'Hopf pair plus split unknot',
            'A_boundary_word':[4,-3,-3,1],'point_R_group_label':label,'point_sign':-1,
            'global_Sigma_intersections':None,'complete_pair':False,'CE':False}
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
