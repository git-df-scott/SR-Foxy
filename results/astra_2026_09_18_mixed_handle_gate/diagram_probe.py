"""Replay the one exploratory local simplification; no marked cable claim."""
import json
from pathlib import Path
import resource
from build_checks import g
from spherogram import Link
from spherogram.links import simplify

HERE=Path(__file__).resolve().parent

def snapshot(L):
    return {str(c.label):[[d.label,p] for d,p in c.adjacent] for c in L.crossings}

def main():
    resource.setrlimit(resource.RLIMIT_CPU,(10,12))
    out=HERE/'diagram_probe.json'
    if out.exists():raise FileExistsError(out)
    L=Link(g.SCAFFOLD)
    for i,c in enumerate(L.crossings):c.label=i
    R=L.sublink(0);upper=[c for c in R.crossings if c.label<27]
    bylabel={c.label:c for c in upper};bylabel[0][2]=bylabel[1][1]
    K=Link(upper);initial={'pd_code':K.PD_code(),'labels':[c.label for c in K.crossings],
                         'adjacency':snapshot(K)}
    previous=set();moves=[]
    for step in range(8):
        options=simplify.possible_type_III_moves(K)
        allowed=[f for f in options if {x.crossing.label for x in f}!=previous]
        if not allowed:break
        face=allowed[0];previous={x.crossing.label for x in face}
        entry={'move':'III','face':[[x.crossing.label,x.strand_index] for x in face],
               'before':snapshot(K)}
        simplify.reidemeister_III(K,face);entry['after']=snapshot(K);moves.append(entry)
        while True:
            changed=False
            for c in list(K.crossings):
                before=snapshot(K);label=c.label
                removed,_=simplify.reidemeister_I_and_II(K,c)
                if removed:
                    moves.append({'move':'I' if len(removed)==1 else 'II',
                                  'at_crossing':label,'removed':sorted(v.label for v in removed),
                                  'before':before,'after':snapshot(K)})
                    changed=True;break
            if not changed:break
        if len(K.crossings)<=6:break
    before_rebuild=snapshot(K);K._rebuild()
    assert len(K.crossings)==6 and K.is_planar()
    assert sum(m['move']=='III' for m in moves)==6 and sum(m['move']=='I' for m in moves)==3
    record={'initial':initial,'moves':moves,'before_orientation_rebuild':before_rebuild,
            'final':{'pd_code':K.PD_code(),'labels':[c.label for c in K.crossings],'adjacency':snapshot(K)},
            'scope':'Local source-knot isotopy probe using Spherogram; A-whisker and cable transport NOT completed.',
            'search_bound':'One deterministic non-immediately-reversing move path, at most eight III moves, 10 CPU seconds',
            'unfinished_comparison':'Direct even-rotation port comparison with stored K0 gave no map; no knot distinction follows.'}
    out.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'III_moves':6,'I_moves':3,'final_crossings':6,'marked_transfer':False}))

if __name__=='__main__':main()
