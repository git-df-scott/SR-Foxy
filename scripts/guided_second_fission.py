#!/usr/bin/env python3
"""Sample the second saddle only on component-HFK/Kh surviving intermediates."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import time
import snappy
from spherogram.links.bands.core import Band, add_one_band
from component_guided_bands import parts, jones, l1, encoded, product
from fusion_successors import diagram_signature
from nonfibered_reverse_audit import sampled_bands


def linking_size(L):
    M=L.linking_matrix()
    return sum(abs(M[i][j]) for i in range(len(M)) for j in range(i))


def run(a):
    out=Path(a.output)
    if out.exists():raise FileExistsError(out)
    raw=Path(a.input).read_bytes();data=json.loads(raw)
    gate_raw=Path(a.gate).read_bytes();gate=json.loads(gate_raw);assert gate['complete']
    retained=set(gate['retained_first_bands']);pd=json.loads(Path('data/knots/AbeTagami_K_1.json').read_text())['pd_code_snappy_0indexed']
    wanted=jones(snappy.Link(pd))
    rec={'status':'BOUNDED_SECOND_FISSION_SEARCH_NOT_A_CERTIFICATE','parameters':vars(a),
         'input_sha256':hashlib.sha256(raw).hexdigest(),'gate_sha256':hashlib.sha256(gate_raw).hexdigest(),
         'runs':[],'complete':False}
    def save():out.write_text(json.dumps(rec,indent=2)+'\n')
    for r in data['intermediates']:
        if r['first_band'] not in retained:continue
        J=snappy.Link(r['intermediate_pd']);row={'first_band':r['first_band'],'start_pd':J.PD_code(),
             'counts':Counter(),'matches':[],'best':[],'complete':False};rec['runs'].append(row);t0=time.monotonic();seen=set()
        for b,meta in sampled_bands(J,a.seed+len(rec['runs']),a.attempts,a.length,1):
            if row['counts']['sampled_bands']>=a.moves or time.monotonic()-t0>a.seconds:break
            row['counts']['sampled_bands']+=1;L=add_one_band(J,b)
            if len(L.link_components)!=3:row['counts']['fusion_not_fission']+=1;continue
            # Only the pair of descendants can change linking under a full twist.
            # Trying both corrections avoids orientation changes during rebuilding.
            n=int(linking_size(L));sol=[]
            for twist in sorted({b.num_twist-2*n,b.num_twist+2*n}):
                B=Band(b.cs_along_top,b.arc_is_under,twist);S=add_one_band(J,B)
                if linking_size(S)==0:sol.append((B,S))
            if not sol:row['counts']['linking_rejected']+=1;continue
            assert len(sol)==1
            B,S=sol[0];row['counts']['zero_linking_fissions']+=1;P=parts(S);assert len(P)==3
            pol=[jones(K) for K in P]
            score,i=min((l1(pol[i],wanted)+sum(l1(pol[j],{0:1}) for j in range(3) if j!=i),i) for i in range(3))
            if score and len(row['best'])>=8 and score>=row['best'][-1]['polynomial_distance']:continue
            G=S.copy();G.simplify('basic');key=diagram_signature(G.PD_code())+':'+str(G.unlinked_unknot_components)
            if key in seen:continue
            seen.add(key)
            c={'band':B.compressed_spec(),'path_metadata':meta,'raw_pd':S.PD_code(),'link_pd':G.PD_code(),
               'unlinked_unknots':G.unlinked_unknot_components,'component_pd':[K.PD_code() for K in P],
               'component_Jones':[encoded(p) for p in pol],'polynomial_distance':score,'wanted_component':i,
               'certified_concordance':False}
            assert add_one_band(J,c['band']).PD_code()==c['raw_pd'];c['raw_replay']=True
            if score==0:
                whole=jones(S);split={0:1}
                for p in pol:split=product(split,p)
                for _ in range(2):split=product(split,{-1:1,1:1})
                c.update(whole_Jones=encoded(whole),split_product_Jones=encoded(split),nonsplit_by_Jones=whole!=split)
                if whole==split:
                    G.simplify('global',type_III_limit=200);c['after_global_pd']=G.PD_code()
                    c['two_split_unknots_detected']=G.unlinked_unknot_components==2 and len(G.link_components)==1
                row['matches'].append(c)
            else:
                row['best'].append(c);row['best'].sort(key=lambda c:c['polynomial_distance']);row['best']=row['best'][:8]
            save()
        row.update(complete=True,seconds=round(time.monotonic()-t0,3));save()
        print(json.dumps({'first_band':row['first_band'],'counts':row['counts'],'matches':len(row['matches']),'best_distance':row['best'][0]['polynomial_distance'] if row['best'] else None}),flush=True)
    rec['complete']=True;save()


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ['input','gate','output']:p.add_argument(arg)
    p.add_argument('--seed',type=int,default=20260917);p.add_argument('--moves',type=int,default=30000)
    p.add_argument('--attempts',type=int,default=300000);p.add_argument('--length',type=int,default=14);p.add_argument('--seconds',type=float,default=90)
    run(p.parse_args())
