"""Find short, replayable diagram movies exposing K disjoint union an unknot.
The last identity is a strict Regina diagram signature, not a volume comparison.
"""
import json,time,collections
from pathlib import Path
import spherogram
from spherogram.links.links_base import CrossingStrand
from spherogram.links import simplify as ss
from pd_moves import simplify as pure_simplify
from analyze_L4_survivors import sig
ROOT=Path(__file__).parent

def r3_options(pd):
    L=spherogram.Link(pd)
    return [[(L.crossings.index(e.crossing),e.strand_index) for e in triple] for triple in ss.possible_type_III_moves(L)]

def apply(pd,spec):
    L=spherogram.Link(pd)
    valid=r3_options(pd);assert spec in valid
    triple=[CrossingStrand(L.crossings[i],j) for i,j in spec]
    ss.reidemeister_III(L,triple);L._rebuild(True)
    q=[list(x) for x in L.PD_code()];red,u,movie=pure_simplify(q)
    return red,u,{'before':pd,'type':'R3_then_R12','R3_triple':spec,'after_R3':q,'R12_movie':movie,'after':red,'new_trivial_components':u}

def main():
    start=time.time();src=json.loads((ROOT/'gst48.json').read_text())['pd'];target=sig(src)
    records=[r for r in json.loads((ROOT/'L4_followup.json').read_text())['records'] if r['status']=='unresolved'];out=[]
    for r in records:
        q=r['pd'];found=None;states=[(q,0,[])];seen={sig(q)}
        # Full search through four R3 moves; R1/R2 removals after every move.
        for depth in [1,2,3,4]:
            nextstates=[]
            for pd,u,hist in states:
                for spec in r3_options(pd):
                    new,v,step=apply(pd,spec);total=u+v
                    if total==1 and sig(new)==target:
                        found={'band':r['band'],'source_band_pd':q,'movie':hist+[step],'result_pd':new,'unlinked_unknots':total,'result_signature':target};break
                    key=(sig(new),total)
                    if key not in seen:
                        seen.add(key);nextstates.append((new,total,hist+[step]))
                if found:break
            if found:break
            states=nextstates
        out.append(found or {'band':r['band'],'short_movie_found':False})
        print(r['band'],'CERTIFIED' if found else 'UNRESOLVED','R3',len(found['movie']) if found else None,flush=True)
    result={'scope':'Explicit R3 plus individually recorded R1/R2 removals prove these prefixes only split off an unknot and return the same source knot. This does not exclude them as possible ribbon prefixes; completing them still requires solving the source knot.','input_count':len(records),'certified_source_plus_unknot':sum('movie' in r for r in out),'elapsed_seconds':time.time()-start,'records':out}
    (ROOT/'L4_trivial_movies.json').write_text(json.dumps(result,indent=2)+'\n');print('TOTAL',result['certified_source_plus_unknot'],time.time()-start)
if __name__=='__main__':main()
