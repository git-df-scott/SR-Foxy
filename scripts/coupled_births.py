#!/usr/bin/env python3
"""Two births BEFORE two fusions, allowing a non-split intermediate link.

The old sequential generator always births its second circle after the first
fusion. Here both initially split unknots exist before either band. Every band
joins different components, so the movie is an oriented annulus if the library
band/isotopy conventions are correct. All witnesses are nominations for later
independent geometric verification, not slice certificates.
"""
import argparse
from collections import defaultdict,deque
import gzip
import hashlib
import json
from pathlib import Path
import random
import time
import snappy
from spherogram.links.bands.core import Band,add_one_band,normalize_crossing_labels
from spherogram.links.simplify import reverse_type_II
from fusion_successors import diagram_signature,detour_paths


def two_births(pd,rng):
    n=len(pd);extra=[]
    for offset in [2*n,2*n+4]:extra.extend([(offset,offset+1,offset+1,offset+2),(offset+2,offset+3,offset+3,offset)])
    L=snappy.Link([tuple(r) for r in pd]+extra);normalize_crossing_labels(L)
    assert len(L.link_components)==3
    split=L.PD_code();isotopies=[]
    for labels in [{n,n+1},{n+2,n+3}]:
        faces=L.faces();outer=max((f for f in faces if all(cs.crossing.label in labels for cs in f)),key=len)
        others=[cs for comp in L.link_components for cs in comp if cs.crossing.label not in labels
                and (labels=={n+2,n+3} or cs.crossing.label<n)]
        c=rng.choice(others)
        if rng.randrange(2):c=c.opposite()
        d=outer[0];new_labels=[len(L.crossings),len(L.crossings)+1]
        isotopies.append({'c':[c.crossing.label,c.strand_index],'d':[d.crossing.label,d.strand_index],'labels':new_labels})
        reverse_type_II(L,c,d,*new_labels,rebuild=True);normalize_crossing_labels(L)
        assert L.is_planar() and len(L.link_components)==3
    return L,{'split_pd':split,'isotopies':isotopies,'birth_pd':L.PD_code()}


def random_bands(L,rng,count,length=8,twists=3,face_return=False,return_loops=1):
    """Sample endpoint/face/path/twist/overpass choices; no prefix overbit bias."""
    normalize_crossing_labels(L);faces=L.faces();edge_faces=defaultdict(list);edge_cs={}
    for node,face in enumerate(faces):
        for cs in face:
            arc=cs.strand_label();edge_faces[arc].append(node);edge_cs[arc,node]=cs.opposite()
    adj=defaultdict(list)
    for arc,ends in edge_faces.items():
        assert len(ends)==2
        a,b=ends;adj[a].append((b,arc));adj[b].append((a,arc))
    arcs=[sorted({cs.strand_label() for cs in c}) for c in L.link_components]
    pairs=[(i,j) for i in range(len(arcs)) for j in range(i+1,len(arcs))]
    seen=set();done=0
    for attempt in range(count*40):
        ci,cj=pairs[attempt%len(pairs)];a=rng.choice(arcs[ci]);b=rng.choice(arcs[cj])
        start=rng.choice(edge_faces[a]);end=rng.choice(edge_faces[b]);path=None
        if attempt%3:
            path=next(detour_paths(adj,start,end,{a,b},length-2,rng,5),None)
        if path is None:
            queue=deque([(start,[])]);visited={start}
            while queue:
                node,prefix=queue.popleft()
                if node==end:path=prefix;break
                if len(prefix)>=length-2:continue
                choices=list(adj[node]);rng.shuffle(choices)
                for nxt,arc in choices:
                    if arc not in (a,b) and nxt not in visited:
                        visited.add(nxt);queue.append((nxt,prefix+[(node,arc,nxt)]))
        if path is None:continue
        loop_positions=[]
        for loop_number in range(return_loops if face_return and len(arcs)>2 else 0):
            if len(path)>length-4:break
            # A simple dual path cannot enter an isolated circle's interior
            # and return to the same exterior face. Insert a two-edge return
            # across the remaining component. Distinct arcs are essential:
            # add_one_band cannot insert two crossings into one original arc.
            remaining=(set().union(*(set(v) for k,v in enumerate(arcs) if k not in (ci,cj)))
                       if loop_number%2==0 else set(min([arcs[ci],arcs[cj]],key=len)))
            used={a,b}|{arc for _,arc,_ in path}
            options=[]
            for pos,node in enumerate([start]+[v for _,_,v in path]):
                for mid,e1 in adj[node]:
                    if mid==node or e1 not in remaining or e1 in used:continue
                    for back,e2 in adj[mid]:
                        if back==node and e2 in remaining and e2 not in used and e2!=e1:
                            options.append((pos,node,e1,mid,e2))
            if options:
                pos,node,e1,mid,e2=rng.choice(options)
                path=path[:pos]+[(node,e1,mid),(mid,e2,node)]+path[pos:]
                loop_positions=[old+2 if old>=pos else old for old in loop_positions]+[pos]
        X=edge_cs[a,start].opposite();Z=edge_cs[b,end]
        parity=int((X==X.oriented())==(Z==Z.oriented()))
        twist=rng.choice([t for t in range(-twists,twists+1) if t%2==parity])
        along=[X]+[edge_cs[arc,node] for node,arc,_ in path]+[Z]
        overbits=rng.randrange(1<<len(path))
        for loop_at in loop_positions:
            # Force opposite heights on the two crossings of the free circle.
            overbits &= ~((1<<loop_at)|(1<<(loop_at+1)))
            overbits |= 1 << (loop_at+rng.randrange(2))
        band=Band([(cs.crossing.label,cs.strand_index) for cs in along],overbits,twist)
        spec=band.compressed_spec()
        if spec in seen:continue
        seen.add(spec)
        try:B=add_one_band(L,band)
        except AssertionError:
            if loop_positions:continue  # reject crossing chords in a face
            raise
        assert len(B.link_components)==len(L.link_components)-1
        yield B,{'band':spec,'component_pair':[ci,cj],'dual_path':path,'face_return_positions':loop_positions,'raw_output_pd':B.PD_code()}
        done+=1
        if done>=count:return


def replay_placement(p):
    from spherogram.links.links_base import CrossingStrand
    L=snappy.Link(p['split_pd']);normalize_crossing_labels(L)
    for iso in p['isotopies']:
        c=CrossingStrand(L.crossings[iso['c'][0]],iso['c'][1]);d=CrossingStrand(L.crossings[iso['d'][0]],iso['d'][1])
        reverse_type_II(L,c,d,*iso['labels'],rebuild=True);normalize_crossing_labels(L)
    assert L.PD_code()==[tuple(r) for r in p['birth_pd']]


def run(card,output,placements=12,first_count=8,second_count=24,length=8,twists=3,seed=20260916,seconds=180,face_return=False,return_loops=1):
    if Path(output).exists():raise FileExistsError(output)
    data=json.loads(Path(card).read_text());pd=data['pd_code_snappy_0indexed'];rng=random.Random(seed);random.seed(seed)
    t0=time.monotonic();seen=set();moves=0;first_id=0;stop='finite_box_finished'
    with gzip.open(output,'xt') as f:
        def write(row):f.write(json.dumps(row,separators=(',',':'))+'\n');f.flush()
        write({'type':'header','status':'TWO_BIRTHS_THEN_TWO_FUSIONS_NOT_A_SLICE_CERTIFICATE','card':card,'source_pd':pd,
               'placements':placements,'first_per_placement':first_count,'second_per_first':second_count,'length':length,
               'twists':twists,'seed':seed,'time_limit':seconds,'face_return':face_return,'return_loops':return_loops,'snappy':snappy.__version__})
        for placement in range(placements):
            L,birth=two_births(pd,rng);replay_placement(birth)
            write(dict(birth,type='placement',placement=placement))
            for I,first in random_bands(L,rng,first_count,length,twists,face_return,return_loops):
                first_id+=1
                replay=add_one_band(L,first['band']);assert replay.PD_code()==I.PD_code()
                # Diagnostic only; leave the actual intermediate untouched.
                diagnostic=I.copy();diagnostic.simplify('basic')
                first['detected_split_unknot']=diagnostic.unlinked_unknot_components>0
                first['simplified_intermediate_pd']=diagnostic.PD_code()
                write(dict(first,type='first',first_id=first_id,placement=placement))
                for J,second in random_bands(I,rng,second_count,length,twists):
                    moves+=1;replay=add_one_band(I,second['band']);assert replay.PD_code()==J.PD_code()
                    J.simplify('basic');endpoint=J.PD_code();sig=diagram_signature(endpoint)
                    second.update(type='move',index=moves,first_id=first_id,endpoint_pd=endpoint,
                                  diagram_signature=sig,new_signature=sig not in seen,crossings=len(endpoint),replay_passed=True)
                    seen.add(sig);write(second)
                    if time.monotonic()-t0>=seconds:stop='time_cap';break
                if stop=='time_cap':break
            if stop=='time_cap':break
            print('placement',placement+1,'moves',moves,'unique',len(seen),flush=True)
        summary={'type':'summary','moves':moves,'unique_diagrams':len(seen),'first_bands':first_id,
                 'seconds':round(time.monotonic()-t0,3),'stop':stop}
        write(summary);print(json.dumps(summary),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('card');p.add_argument('output')
    p.add_argument('--placements',type=int,default=12);p.add_argument('--first',type=int,default=8);p.add_argument('--second',type=int,default=24)
    p.add_argument('--length',type=int,default=8);p.add_argument('--twists',type=int,default=3);p.add_argument('--seed',type=int,default=20260916)
    p.add_argument('--seconds',type=float,default=180);p.add_argument('--face-return',action='store_true');p.add_argument('--return-loops',type=int,default=1);a=p.parse_args()
    run(a.card,a.output,a.placements,a.first,a.second,a.length,a.twists,a.seed,a.seconds,a.face_return,a.return_loops)
