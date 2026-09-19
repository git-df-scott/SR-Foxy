#!/usr/bin/env python3
"""Exact specialized Fox ranks, with separate variables for link components.

A nonzero maximal minor proves generic Alexander-module rank zero, which
obstructs link concordance to a split knot/unknot pair (generic rank one).
A deficient specialization is inconclusive; it is not a proof of generic rank.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import snappy
from spherogram.links.bands.core import add_one_band, normalize_crossing_labels
from component_guided_bands import controls
from coupled_births import replay_placement
from two_fission_target import alex_rank


def fox_matrix(L, values, prime):
    if len(values)!=len(L.link_components)+L.unlinked_unknot_components:raise ValueError('One value per component required')
    if any(v%prime in (0,1) for v in values):raise ValueError('Use nonzero values different from one')
    pieces=L._pieces();arc={};colors=[]
    for i,part in enumerate(pieces):
        labels={cs[0].strand_components[cs[1]] for cs in part}
        assert len(labels)==1
        colors.append(labels.pop())
        for cs in part:arc[tuple(cs)]=i
    for ci,comp in enumerate(L.link_components):
        if all(cs.strand_index in (1,3) for cs in comp):
            i=len(colors);colors.append(ci)
            for cs in comp:arc[cs.crossing,1]=i;arc[cs.crossing,3]=i
    colors.extend(range(len(L.link_components),len(values)))
    tv=[values[c]%prime for c in colors];rows=[]
    for c in L.crossings:
        i,j,k=arc[c,0]+1,arc[c,2]+1,arc[c,1]+1
        word=[-k,i,k,-j] if c.sign>0 else [k,i,-k,-j]
        row=[0]*len(tv);prefix=1
        for a in word:
            v=tv[abs(a)-1]
            if a>0:row[a-1]=(row[a-1]+prefix)%prime;prefix=prefix*v%prime
            else:prefix=prefix*pow(v,-1,prime)%prime;row[-a-1]=(row[-a-1]-prefix)%prime
        assert prefix==1 and sum(x*(v-1) for x,v in zip(row,tv))%prime==0
        rows.append(row)
    return rows,colors


def rank_minor(rows,n,p):
    A=[r.copy() for r in rows];row_ids=list(range(len(A)));selected=[];cols=[];rank=0
    for col in range(n):
        pivot=next((i for i in range(rank,len(A)) if A[i][col]%p),None)
        if pivot is None:continue
        A[rank],A[pivot]=A[pivot],A[rank];row_ids[rank],row_ids[pivot]=row_ids[pivot],row_ids[rank]
        selected.append(row_ids[rank]);cols.append(col);inv=pow(A[rank][col],-1,p)
        A[rank]=[x*inv%p for x in A[rank]]
        for i in range(rank+1,len(A)):
            v=A[i][col];A[i]=[(x-v*y)%p for x,y in zip(A[i],A[rank])]
        rank+=1
        if rank==len(A):break
    B=[[rows[i][j]%p for j in cols] for i in selected];det=1
    for k in range(rank):
        i=next(i for i in range(k,rank) if B[i][k])
        if i!=k:B[k],B[i]=B[i],B[k];det=-det
        v=B[k][k];det=det*v%p;inv=pow(v,-1,p)
        for i in range(k+1,rank):
            a=B[i][k]*inv%p
            for j in range(k,rank):B[i][j]=(B[i][j]-a*B[k][j])%p
    assert det%p!=0
    return {'rank':rank,'columns':n,'minor_rows':selected,'minor_columns':cols,'minor_determinant_mod_prime':det%p,
            'specialized_H1_dimension':n-rank-1,'maximal_minor_nonzero':rank==n-1}


def check(L,values,p):
    rows,colors=fox_matrix(L,values,p);r=rank_minor(rows,len(colors),p)
    assert r['rank']<=len(colors)-1
    return dict(r,prime=p,component_values=values,generator_components=colors)


def ribbon_control():
    placements={}
    with gzip.open('results/coupled_K0_double_return.jsonl.gz','rt') as f:
        for line in f:
            r=json.loads(line)
            if r['type']=='placement':placements[r['placement']]=r
            if r['type']=='first' and r['first_id']==20:
                p=placements[r['placement']];replay_placement(p);L=snappy.Link(p['birth_pd']);normalize_crossing_labels(L)
                I=add_one_band(L,r['band']);assert I.PD_code()==[tuple(c) for c in r['raw_output_pd']]
                return I,{'archive':'results/coupled_K0_double_return.jsonl.gz','first_id':20,'placement':r['placement'],'band':r['band'],'raw_replay':True}
    raise AssertionError('Missing positive control')


def run(a):
    out=Path(a.output)
    if out.exists():raise FileExistsError(out)
    raw=Path(a.input).read_bytes();d=json.loads(raw);assert d['complete']
    rec={'status':'EXACT_SPECIALIZED_RANK_OBSTRUCTIONS','input':a.input,'input_sha256':hashlib.sha256(raw).hexdigest(),
         'scope':'Nonzero maximal minors obstruct link concordance to a split knot/unknot pair. Other records remain unknown.',
         'controls':{},'rows':[],'complete':False}
    C=controls()
    for name,c in C.items():
        L=snappy.Link(c['link_pd']);L.unlinked_unknot_components=c['unlinked_unknots'];r=check(L,[2,3],101)
        assert r['maximal_minor_nonzero']==('Whitehead' in name);rec['controls'][name]=r
    L,meta=ribbon_control();r=check(L,[2,3],101);assert not r['maximal_minor_nonzero'];rec['controls']['nonsplit_ribbon_concordance']=dict(r,provenance=meta)
    # Calibrate specialized colored Fox computation against the earlier diagonal helper.
    counts=Counter()
    for run in d['runs']:
        for c in run['matches']:
            L=snappy.Link(c['link_pd']);L.unlinked_unknot_components=c['unlinked_unknots']
            row={'index':run['index'],'band':c['band'],'checks':[],'recognized_components':c['component_diagram_matches_target'] and c['other_component_is_unknot_by_simplification']}
            for values,p in [([2,2],101),([3,3],103),([2,3],101),([3,5],103)]:
                r=check(L,values,p);row['checks'].append(r)
                if values==[2,2]:assert (r['rank'],r['columns'])==alex_rank(L)
                if r['maximal_minor_nonzero']:break
            row['link_concordance_to_split_obstructed']=any(x['maximal_minor_nonzero'] for x in row['checks'])
            counts['obstructed' if row['link_concordance_to_split_obstructed'] else 'retained_unknown']+=1
            if row['recognized_components']:counts['recognized_obstructed' if row['link_concordance_to_split_obstructed'] else 'recognized_retained_unknown']+=1
            if row['link_concordance_to_split_obstructed']:counts['first_obstruction_'+str(len(row['checks']))]+=1
            rec['rows'].append(row)
    rec['counts']=dict(counts);rec['complete']=True;out.write_text(json.dumps(rec,separators=(',',':'))+'\n');print(json.dumps(rec['counts']),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('output');run(p.parse_args())
