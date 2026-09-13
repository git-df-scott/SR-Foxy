#!/usr/bin/env python3
"""Bounded reverse two-saddle search, with an Alexander-nullity filter.

A valid intermediate is concordant to K1 disjoint union unknot. Its generic
Alexander nullity is one. Full Alexander rank n-1 at t=2 mod101 therefore
rejects it; lower rank merely retains it. Numerical identification and
simplification are nominations, never a geometric slice certificate.
"""
import argparse,json,subprocess,sys,time
from pathlib import Path
import snappy
from spherogram.links.bands.core import banded_links,normalize_crossing_labels
from fusion_successors import diagram_signature


def rank_mod(rows,p=101):
    rows=[list(r) for r in rows];rank=0
    for j in range(len(rows[0]) if rows else 0):
        pivot=next((i for i in range(rank,len(rows)) if rows[i][j]%p),None)
        if pivot is None:continue
        rows[rank],rows[pivot]=rows[pivot],rows[rank]
        inv=pow(rows[rank][j]%p,-1,p);rows[rank]=[(v*inv)%p for v in rows[rank]]
        for i in range(rank+1,len(rows)):
            a=rows[i][j]%p
            if a:rows[i]=[(v-a*w)%p for v,w in zip(rows[i],rows[rank])]
        rank+=1
        if rank==len(rows):break
    return rank


def alex_rank(L,p=101,t=2):
    pieces=L._pieces();arc={tuple(cs):m for m,part in enumerate(pieces) for cs in part}
    n=len(pieces)
    # _pieces starts at undercrossings. An entirely overpassing component
    # has no such start and needs its own Wirtinger generator. This occurs
    # in split links with overlapping projections; omitting it caused a
    # KeyError in the focused reverse-search pilot.
    for comp in L.link_components:
        if all(cs.strand_index in (1,3) for cs in comp):
            for cs in comp:
                arc[cs.crossing,1]=n;arc[cs.crossing,3]=n
            n+=1
    n+=L.unlinked_unknot_components
    rows=[]
    for c in L.crossings:
        i,j,k=arc[(c,0)]+1,arc[(c,2)]+1,arc[(c,1)]+1
        # Match Spherogram's unoriented _pieces endpoints and Wirtinger signs.
        word=[-k,i,k,-j] if c.sign>0 else [k,i,-k,-j]
        row=[0]*n;power=0
        for a in word:
            if a>0:row[a-1]=(row[a-1]+pow(t,power,p))%p;power+=1
            else:power-=1;row[-a-1]=(row[-a-1]-pow(t,power,p))%p
        assert power==0 and sum(row)%p==0
        rows.append(row)
    return rank_mod(rows,p),n


def run(targets,output,seconds,first_limit,second_limit,length):
    out=Path(output)
    if out.exists():raise FileExistsError(out)
    target=json.loads(Path(targets).read_text())['candidates'][0]
    J=snappy.Link(target['endpoint_pd']);normalize_crossing_labels(J)
    sources={}
    for side,card in [('K0','AbeTagami_K_0_K_-1__6_3'),('K1','AbeTagami_K_1')]:
        d=json.loads(Path('data/knots/'+card+'.json').read_text());L=snappy.Link(d['pd_code_snappy_0indexed'])
        sources[side]={'hfk':L.knot_floer_homology()['ranks'],'signature':L.exterior().isometry_signature(of_link=True,ignore_orientation=False)}
    rec={'status':'BOUNDED_TWO_FISSION_SEARCH_NOT_A_CERTIFICATE','target':targets,
        'seconds_limit':seconds,'first_limit':first_limit,'second_limit_per_intermediate':second_limit,'length':length,'twists':2,
        'field':101,'evaluation':2,'first_attempts':0,'rank_rejected':0,'linking_rejected':0,
        'intermediates':[],'second_attempts':0,'endpoint_checks':[],'hits':[],'complete':False}
    start=time.monotonic();seen=set();endpoints=set();stop='first_enumeration_finished'
    def save():out.write_text(json.dumps(rec,indent=2)+'\n')
    for I,first in banded_links(J,2,length,'shortest'):
        rec['first_attempts']+=1
        if rec['first_attempts']>first_limit:stop='first_cap';break
        if time.monotonic()-start>seconds:stop='time_cap';break
        if len(I.link_components)!=2:continue
        if I.linking_number()!=0:rec['linking_rejected']+=1;continue
        I.simplify('basic')
        # A split death after the first saddle is already a sequential case;
        # keep it by reinserting a harmless two-crossing unknot for stage two.
        if I.unlinked_unknot_components:
            pd=I.PD_code();n=2*len(pd)
            I=snappy.Link(pd+[(n,n+1,n+1,n+2),(n+2,n+3,n+3,n)])
        normalize_crossing_labels(I)
        sig=diagram_signature(I.PD_code())
        if sig in seen:continue
        seen.add(sig)
        info={'first_band':first,'intermediate_pd':I.PD_code(),'second_attempts':0,'deaths':0}
        try:
            rank,n=alex_rank(I);info['alexander_rank']=rank;info['arc_count']=n
            assert rank<=n-1
            if rank==n-1:rec['rank_rejected']+=1;continue
        except (KeyError,AssertionError) as e:
            info['rank_unknown']=type(e).__name__+': '+str(e)
        rec['intermediates'].append(info)
        for S,second in banded_links(I,2,length,'shortest'):
            info['second_attempts']+=1;rec['second_attempts']+=1
            if info['second_attempts']>second_limit:info['stop']='second_cap';break
            if time.monotonic()-start>seconds:stop='time_cap';info['stop']=stop;break
            if len(S.link_components)!=3:continue
            raw=S.PD_code();S.simplify('basic')
            if S.unlinked_unknot_components!=2 or len(S.link_components)!=1:continue
            info['deaths']+=1;S.unlinked_unknot_components=0
            key=diagram_signature(S.PD_code())
            if key in endpoints:continue
            endpoints.add(key);row={'first_band':first,'second_band':second,'endpoint_pd':S.PD_code(),'raw_second_pd':raw}
            try:
                proc=subprocess.run([sys.executable,'scripts/hfk_worker.py'],input=json.dumps(S.PD_code()),capture_output=True,text=True,timeout=3,check=True)
                h=json.loads(proc.stdout);ranks={(a,m):v for a,m,v in h['ranks']};row['hfk']=h
                row['matching_source_HFK']=[name for name,s in sources.items() if ranks==s['hfk']]
                if row['matching_source_HFK']:
                    sig=S.exterior().isometry_signature(of_link=True,ignore_orientation=False)
                    row['numerical_source_matches']=[name for name in row['matching_source_HFK'] if sig==sources[name]['signature']]
                    if row['numerical_source_matches']:rec['hits'].append(row)
            except Exception as e:row['unknown']=type(e).__name__+': '+str(e)
            rec['endpoint_checks'].append(row)
        info.setdefault('stop','second_enumeration_finished');save()
        print('first',rec['first_attempts'],'retained',len(rec['intermediates']),'second',rec['second_attempts'],'endpoints',len(endpoints),'hits',[(x.get('numerical_source_matches')) for x in rec['hits']],flush=True)
        if stop=='time_cap':break
    rec['complete']=True;rec['stop']=stop;rec['seconds']=round(time.monotonic()-start,3);save()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('targets');p.add_argument('output');p.add_argument('--seconds',type=float,default=180)
    p.add_argument('--first',type=int,default=8000);p.add_argument('--second',type=int,default=2000);p.add_argument('--length',type=int,default=8);a=p.parse_args()
    run(a.targets,a.output,a.seconds,a.first,a.second,a.length)
