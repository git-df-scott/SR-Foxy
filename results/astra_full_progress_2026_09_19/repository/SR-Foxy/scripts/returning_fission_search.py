#!/usr/bin/env python3
"""Embedded band cores may revisit faces; reject interleaving face chords.

Sample dual-edge trails, allow repeated faces, and certify that all chords
within every face are disjoint. Original arcs are not repeated. This is an
incomplete, biased family, broader than face-simple band paths.
"""
import argparse
from collections import Counter,defaultdict
import hashlib
import json
from pathlib import Path
import random
import time
import snappy
from spherogram.links.bands.core import Band,add_one_band
from component_guided_bands import inspect,jones
from colored_link_rank import check
from fusion_successors import diagram_signature,replay


def noninterleaving(order,chords):
    if len(set(order))!=len(order):raise ValueError('Repeated face boundary arc requires a different encoding')
    pos={x:i for i,x in enumerate(order)};n=len(order)
    ends=[x for chord in chords for x in chord]
    if len(set(ends))!=len(ends) or any(x not in pos for x in ends):return False
    for k,(a,b) in enumerate(chords):
        for c,d in chords[k+1:]:
            inside=lambda x:0<(pos[x]-pos[a])%n<(pos[b]-pos[a])%n
            if inside(c)!=inside(d):return False
    return True


def chord_certificate(faces,path,a,b,start,end):
    byface=defaultdict(list);previous=a;node=start
    for f,e,g in path:
        assert f==node
        byface[f].append((previous,e));previous=e;node=g
    assert node==end;byface[end].append((previous,b))
    for f,chords in byface.items():
        if not noninterleaving([cs.strand_label() for cs in faces[f]],chords):return None
    return [{'face':f,'boundary':[cs.strand_label() for cs in faces[f]],'chords':v} for f,v in sorted(byface.items())]


def returning_bands(J,seed,attempts,max_length,counts):
    rng=random.Random(seed);faces=J.faces();adj=defaultdict(list);edge_faces=defaultdict(list);ecs={}
    for f,face in enumerate(faces):
        for cs in face:edge_faces[cs.strand_label()].append(f);ecs[cs.strand_label(),f]=cs.opposite()
    for e,(f,g) in sorted(edge_faces.items()):adj[f].append((g,e));adj[g].append((f,e))
    facearcs=[[cs.strand_label() for cs in f] for f in faces];seen=set()
    for attempt in range(attempts):
        counts['walk_attempts']+=1;length=rng.randrange(2,max_length-1);start=node=rng.randrange(len(faces));path=[];used=set();nodes=[node]
        for _ in range(length):
            options=[(g,e) for g,e in adj[node] if e not in used]
            if not options:break
            g,e=rng.choice(options);used.add(e);path.append((node,e,g));node=g;nodes.append(node)
        if len(path)!=length:counts['short_walk']+=1;continue
        if len(set(nodes))==len(nodes):counts['no_face_return']+=1;continue
        aa=[e for e in facearcs[start] if e not in used];bb=[e for e in facearcs[node] if e not in used]
        if not aa or not bb:counts['no_attachment']+=1;continue
        a,b=rng.choice(aa),rng.choice(bb)
        if a==b:counts['same_attachment_arc']+=1;continue
        certificate=chord_certificate(faces,path,a,b,start,node)
        if certificate is None:counts['crossing_chords']+=1;continue
        X=ecs[a,start].opposite();Z=ecs[b,node];along=[X]+[ecs[e,f] for f,e,g in path]+[Z]
        parity=int((X==X.oriented())==(Z==Z.oriented()))
        B=Band([(cs.crossing.label,cs.strand_index) for cs in along],rng.randrange(1<<len(path)),parity)
        key=B.compressed_spec()
        if key in seen:counts['duplicate_band']+=1;continue
        seen.add(key)
        yield B,{'attempt':attempt,'dual_path':path,'attaching_arcs':[a,b],'repeated_face_visits':len(nodes)-len(set(nodes)),'face_chord_certificate':certificate}


def run(a):
    out=Path(a.output)
    if out.exists():raise FileExistsError(out)
    # Combinatorial falsification controls, including a cyclic wrap-around.
    assert not noninterleaving([0,1,2,3],[(0,2),(1,3)])
    assert noninterleaving([0,1,2,3],[(0,3),(1,2)])
    assert noninterleaving([0,1,2,3],[(0,1),(2,3)])
    assert not noninterleaving([0,1,2,3],[(0,1),(1,2)])
    raw=Path(a.input).read_bytes();entries=json.loads(raw)['candidates'][a.offset:a.offset+a.count]
    source='K0' if a.wanted=='K1' else 'K1';polys={};signatures={}
    for name,card in [('K0','AbeTagami_K_0_K_-1__6_3'),('K1','AbeTagami_K_1')]:
        pd=json.loads(Path('data/knots/'+card+'.json').read_text())['pd_code_snappy_0indexed'];L=snappy.Link(pd);L.simplify('basic');polys[name]=jones(L);signatures[name]=diagram_signature(L.PD_code())
    rec={'status':'BOUNDED_RETURNING_FACE_FISSION_SEARCH','parameters':vars(a),'input_sha256':hashlib.sha256(raw).hexdigest(),'runs':[],'complete':False,
         'scope':'Only edge-simple trails with noninterleaving chords. No exhaustive knot, band, or isotopy coverage. Rank-deficient evaluations remain unknown.'}
    def save():out.write_text(json.dumps(rec,separators=(',',':'))+'\n')
    save()
    for r in entries:
        assert not r['hfk_check']['fibered'] and replay(r);J=snappy.Link(r['endpoint_pd']);row={'index':r['index'],'start_pd':J.PD_code(),'counts':Counter(),'retained':[],'wanted_matches':[],'source_controls':[],'complete':False};rec['runs'].append(row);t0=time.monotonic();kept=set()
        for b,meta in returning_bands(J,a.seed+r['index'],a.attempts,a.length,row['counts']):
            if row['counts']['bands']>=a.moves or time.monotonic()-t0>a.seconds:break
            L=add_one_band(J,b);assert L.is_planar() and len(L.link_components)==2;row['counts']['bands']+=1
            old=int(L.linking_number());solutions=[]
            for t in sorted({b.num_twist-2*abs(old),b.num_twist+2*abs(old)}):
                B=Band(b.cs_along_top,b.arc_is_under,t);S=add_one_band(J,B)
                if S.linking_number()==0:solutions.append((B,S))
            assert len(solutions)==1;B,L=solutions[0];rawpd=L.PD_code();L.simplify('basic')
            checks=[]
            for values,p in [([2,2],101),([3,3],103),([2,3],101)]:
                c=check(L,values,p);checks.append(c)
                if c['maximal_minor_nonzero']:break
            if checks[-1]['maximal_minor_nonzero']:row['counts']['link_concordance_obstructed']+=1;continue
            row['counts']['rank_retained_unknown']+=1
            key=diagram_signature(L.PD_code())+':'+str(L.unlinked_unknot_components)
            if key in kept:continue
            # Spherogram.copy() drops detached unknot bookkeeping. Inspect the
            # unsimplified PD, in which both components are still explicit.
            kept.add(key);c=inspect(snappy.Link(rawpd),polys[a.wanted],True);c.update(band=B.compressed_spec(),raw_pd=rawpd,path_metadata=meta,rank_checks=checks)
            assert add_one_band(J,c['band']).PD_code()==rawpd;c['raw_replay']=True
            if c['component_Jones_match']:row['wanted_matches'].append(c)
            if L.unlinked_unknot_components==1 and len(L.link_components)==1 and diagram_signature(L.PD_code())==signatures[source]:row['source_controls'].append(c['band'])
            row['retained'].append(c)
            if len(row['retained'])%20==0:save()
        row.update(complete=True,seconds=round(time.monotonic()-t0,3));save()
        print(json.dumps({'index':r['index'],'counts':row['counts'],'retained_diagrams':len(row['retained']),'wanted_matches':len(row['wanted_matches']),'source_controls':len(row['source_controls'])}),flush=True)
    rec['complete']=True;save()


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('output');p.add_argument('--wanted',choices=['K0','K1'],required=True)
    p.add_argument('--count',type=int,default=2);p.add_argument('--offset',type=int,default=0);p.add_argument('--seed',type=int,default=20260918)
    p.add_argument('--length',type=int,default=14);p.add_argument('--attempts',type=int,default=200000);p.add_argument('--moves',type=int,default=12000);p.add_argument('--seconds',type=float,default=60)
    run(p.parse_args())
