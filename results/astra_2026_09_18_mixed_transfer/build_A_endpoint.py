"""Draw an A endpoint and a single-crossing full collar transfer.

Spherogram is used ONLY for the eight-crossing auxiliary unlink replay.
No knot census or randomized simplification. Existing outputs are preserved.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('old',ROOT/'results/astra_2026_09_18_marked_annulus_construction/build_transport.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
g=old.g

def pd(adj):
    labels={};rows=[]
    for c in sorted(adj):
        row=[]
        for p in range(4):
            x=(c,p);y=tuple(adj[c][p])
            if x not in labels:labels[x]=labels[y]=len(labels)//2
            row.append(labels[x])
        rows.append(row)
    return rows

def main():
    out=HERE/'A_ENDPOINT.json'
    if out.exists():raise FileExistsError(out)
    from spherogram import Link
    from spherogram.links import simplify
    orig=g.adjacency_from_pd(g.SCAFFOLD);q=g.quotient_R_wirtinger(orig)
    cs=sorted(c for c in orig if q['cmap'][c,0]==2 or q['cmap'][c,1]==2)
    assert cs==[7,10,15,17,19,21,25,26]
    copies={c:54+i for i,c in enumerate(cs)}
    adj={c:list(v) for c,v in orig.items()}
    for c in cs:adj[copies[c]]=[None]*4
    for c in cs:
        for p in range(4):
            if q['cmap'][c,p]==2:
                d,r=orig[c][p];g.connect(adj,(copies[c],p),(copies[d],r))
    for c in cs:
        inc=next(p for p in range(4) if q['cmap'][c,p]==2 and (c,p) in q['incoming'])
        side=(inc-1)%4;neighbor=adj[c][side]
        g.connect(adj,(copies[c],side),neighbor)
        g.connect(adj,(c,side),(copies[c],(side+2)%4))
    # The selected side avoids both original band routes; the other side
    # separates B1's first two ports and cannot be substituted silently.
    faces,ids=old.faces(adj)
    assert len(faces)==len(adj)+2
    route_faces=[]
    bands=[dict(g.BAND1,arc_is_under=[False,True]),dict(g.BAND2,arc_is_under=[True,False])]
    for band in bands:
        found=[]
        for x,y in zip(band['along_top'],band['along_top'][1:]):
            incident=lambda x:{ids[x],ids[x[0],(x[1]-1)%4]}
            common=incident(x)&incident(y)
            assert len(common)==1
            found.append(next(iter(common)))
        route_faces.append(found)
    parallel_scaffold={c:list(v) for c,v in adj.items()}
    for band in bands:adj=g.add_zero_twist_band(adj,band)
    target={c:list(v) for c,v in adj.items()}
    crossing=copies[26]
    def port_rotation(x): return (x[0],(x[1]+1)%4) if x[0]==crossing else x
    endpoint={c:[None]*4 for c in adj}
    for c,row in adj.items():
        for p,y in enumerate(row):
            x=port_rotation((c,p));y=port_rotation(y);endpoint[x[0]][x[1]]=y
    for a in [target,endpoint]:
        assert len(old.faces(a)[0])==len(a)+2
        assert len(g.components(a))==4
    qe=g.quotient_R_wirtinger(endpoint)
    fmap=g.map_final_R_arcs_to_scaffold(q,qe)
    assert qe['cmap'][54,1]==3
    def path(start,stop_crossing=None,closed=False):
        x=start;events=[];word=[]
        while True:
            c,p=x
            if c==stop_crossing:break
            letters=[];over=None
            if p%2==0:
                over={'local_port':[c,1],'component':qe['cmap'][c,1]}
                if over['component']==0:
                    direction=1 if x in qe['incoming'] else -1
                    letters=[direction*qe['signs'][c]*(fmap[qe['arcs'][c,1]]+1)]
            events.append({'incoming_port':x,'under_over_meridian':over,'R_letters':letters})
            word+=letters;x=endpoint[c][(p+2)%4]
            if closed and x==start:break
            assert len(events)<100
        return {'start':start,'end':x,'events':events,'R_word':old.red(word)}
    # Root at the midpoint of the incoming copied edge (54,1).
    # Reversed orientation FIRST reaches the other endpoint of that edge.
    A_start=endpoint[54][1]
    A_loop=path(A_start,closed=True)
    A_prefix=path(A_start,crossing)
    a_prefix=path((6,1),crossing)
    assert A_loop['R_word']==[4,-3,1,-4]
    assert A_prefix['R_word']==[4,-3]
    assert a_prefix['R_word']==[4,-1]
    label=old.red(A_prefix['R_word']+old.inv(a_prefix['R_word']))
    assert label==A_loop['R_word']

    def snapshot(L):
        return {'adjacency':{str(c.label):[[int(d.label),p] for d,p in c.adjacent] for c in L.crossings},
                'unlinked_unknot_components':L.unlinked_unknot_components}
    aux_traces=[]
    for name,a in [('target_unswitched',target),('A_endpoint_switched',endpoint)]:
        L=Link(pd(a));qq=g.quotient_R_wirtinger(a)
        component_map=[]
        for comp in L.link_components:
            values={qq['cmap'][int(p.crossing.label),p.strand_index] for p in comp}
            assert len(values)==1
            component_map.append(next(iter(values)))
        assert component_map==[0,1,2,3]
        aux=L.sublink([1,2,3]);before=snapshot(aux);aux_pd=aux.PD_code();moves=[]
        # Deterministic basic Reidemeister moves, no randomized search.
        while True:
            changed=False
            for c in sorted(aux.crossings,key=lambda x:int(x.label)):
                step_before=snapshot(aux)
                eliminated,_=simplify.reidemeister_I_and_II(aux,c)
                if eliminated:
                    moves.append({'at_crossing':int(c.label),'removed':sorted(int(x.label) for x in eliminated),
                                  'before':step_before,'after':snapshot(aux)})
                    changed=True;break
            if not changed:break
        assert len(aux.crossings)==(2 if name=='target_unswitched' else 0)
        assert aux.unlinked_unknot_components==(1 if name=='target_unswitched' else 3)
        aux_traces.append({'name':name,'component_order_R_a_b_C':component_map,
                           'initial_PD':aux_pd,'initial':before,'moves':moves,'final':snapshot(aux)})
    source_paths=[ROOT/'data/knots/AbeTagami_marked_product_scaffold.json',
                  ROOT/'results/astra_2026_09_18_marked_annulus_construction/transport.json']
    report={'scope':'Actual marked A endpoint and complete single-crossing collar annulus to reversed native parallel; NOT a complete pair of mixed transfers/caps',
            'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in source_paths],
            'parallel_side':'copy toward incoming_port-1 at every native c2 crossing',
            'copy_crossings':copies,'band_route_faces':route_faces,
            'parallel_scaffold_adjacency':parallel_scaffold,
            'A_endpoint_adjacency':endpoint,'A_endpoint_PD':pd(endpoint),
            'target_adjacency':target,'target_PD':pd(target),
            'A_orientation':{'root_incoming_edge_port':[54,1],'first_reversed_traversal_port':A_start,'opposite_native_c2':True},
            'A_traversal':A_loop,'A_prefix_to_intersection':A_prefix,'a_prefix_to_intersection':a_prefix,
            'transfer':{'from':'A_endpoint_switched with reversed C orientation','to':'target_unswitched with reversed C orientation',
                        'only_crossing_change':crossing,'original_scaffold_crossing':26,
                        'parameterization':'LOCAL_MOVIE T_minus in crossing ball 61, fixed cylinder outside; rescale coordinates into that ball',
                        'sheets':['T_A','P_a=a times I'], 'sign':-1,'parameter_time':'1/2',
                        'full_R_group_label_convention':'prefix_A * inverse(prefix_a), roots joined by globally-above paths',
                        'full_R_group_label':label,
                        'intersections_with_R_times_I':[],'intersections_with_b_times_I':[],
                        'self_intersections':[], 'framing':'transported zero framing; C has no self crossings before or after',
                        'intersections_with_complete_Sigma':None,'extension_to_F_v':None,
                        'B_transfer':None,'compression_disk':None},
            'auxiliary_unlink_replays':aux_traces,'CE':False}
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'A_endpoint_crossings':len(endpoint),'auxiliary_unlink_components':3,
                      'collar_transfer_points':1,'point_sign':-1,'point_R_label':label,'complete_pair':False}))

if __name__=='__main__':main()
