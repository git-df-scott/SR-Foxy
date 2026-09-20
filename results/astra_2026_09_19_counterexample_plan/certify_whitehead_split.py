"""Bounded R3 search with explicit R1/R2 witnesses. Does not exclude ribbonness."""
import json, time
from pathlib import Path
from spherogram import Link
from spherogram.links.links_base import CrossingStrand
from spherogram.links import simplify as ss
from pd_moves import simplify
import regina
P=Path(__file__).parent

def sig(pd):
    return regina.Link.fromPD([[a+1 for a in q] for q in Link(pd).PD_code()]).sig(False,True,True)

def options(pd):
    L=Link(pd)
    return [[(L.crossings.index(e.crossing),e.strand_index) for e in triple] for triple in ss.possible_type_III_moves(L)]

def move(pd,spec):
    assert spec in options(pd)
    L=Link(pd)
    ss.reidemeister_III(L,[CrossingStrand(L.crossings[i],j) for i,j in spec])
    L._rebuild(True)
    q=[list(x) for x in L.PD_code()]
    reduced,u,hist=simplify(q)
    return reduced,u,dict(before=pd,R3_triple=spec,after_R3=q,R12_movie=hist,after=reduced,new_trivial_components=u)

def main():
    raw=json.loads((P/'WHITEHEAD_SURVIVOR.json').read_text())['raw_pd']
    initial,u,initial_movie=simplify(raw)
    states=[(initial,u,[])];seen={(sig(initial),u)};start=time.monotonic();found=None
    for depth in range(1,4):
        nxt=[]
        for pd,u,hist in states:
            for spec in options(pd):
                new,v,step=move(pd,spec);total=u+v
                if total==1:
                    found=dict(raw_pd=raw,initial_pd=initial,initial_R12=initial_movie,movie=hist+[step],result_pd=new,split_unknots=total);break
                key=(sig(new),total)
                if key not in seen:seen.add(key);nxt.append((new,total,hist+[step]))
            if found or time.monotonic()-start>35:break
        if found or time.monotonic()-start>35:break
        states=nxt
    assert found,'No short movie found within bound'
    pd,u,hist=simplify(found['raw_pd']);assert pd==found['initial_pd'] and hist==found['initial_R12']
    for step in found['movie']:
        new,v,actual=move(pd,step['R3_triple']);assert actual==step
        pd=new;u+=v
    assert pd==found['result_pd'] and u==1
    found.update(replay='PASS',seconds=time.monotonic()-start,visited=len(seen),scope='Explicit split unknot movie; identity of remaining knot checked separately in WHITEHEAD_COMPONENT_IDENTITY_EXHAUSTIVE.json')
    (P/'WHITEHEAD_SPLIT_MOVIE.json').write_text(json.dumps(found,indent=2))
    print(json.dumps({k:found[k] for k in ['replay','seconds','visited','split_unknots']}))
if __name__=='__main__':main()
