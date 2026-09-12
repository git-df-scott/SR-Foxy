#!/usr/bin/env python3
"""Plain-Python exhaustive check; no SnapPy, Sage, SymPy or SAT solver.

Checks all 2^18 assignments, completeness of the 256 saved lifts, grading,
d^2=0 and the saved full-ring maps dF=Gd=0, GF=1.
"""
import argparse
import hashlib
import json
from pathlib import Path


def matrix_product(left,right):
    # left after right; dictionaries are indexed (target, source, U, V).
    entries=set()
    for t,k,u,v in left:
        for j,s,a,b in right:
            if k==j:
                key=(t,s,u+a,v+b)
                entries.symmetric_difference_update({key})
    return entries


def matrix(terms,source,target,degree):
    out=set()
    for i,j,a,b in terms:
        assert a>=0 and b>=0
        ai,mi=source[str(i)];aj,mj=target[str(j)]
        assert aj-a+b==ai and mj-2*a==mi+degree
        key=(j,i,a,b);assert key not in out
        out.add(key)
    return out


def verify(complex_path,lift_path,output):
    if Path(output).exists():raise FileExistsError(output)
    sources=json.loads(Path(complex_path).read_text())['source_complexes']
    lifts=json.loads(Path(lift_path).read_text())['results'];report=[]
    for source,entry in zip(sources,lifts):
        g=source['generators'];u={'0':(0,0)};variables=entry['mixed_variables']
        expected_variables=[]
        a_bound=(max(m for a,m in g.values())-min(m for a,m in g.values())+1)//2
        b_bound=max(a for a,m in g.values())-min(a for a,m in g.values())+a_bound
        for i,(ai,mi) in g.items():
            for j,(aj,mj) in g.items():
                for a in range(1,a_bound+1):
                    for b in range(1,b_bound+1):
                        if aj-a+b==ai and mj-2*a==mi-1:expected_variables.append([int(i),int(j),a,b])
        assert sorted(variables)==sorted(expected_variables)
        row_masks=[sum(1<<i for i in row) for row in entry['linear_equations']]
        all_masks={mask for mask in range(1<<len(variables)) if all((mask&r).bit_count()%2==0 for r in row_masks)}
        saved=set()
        for c in entry['completions']:
            mask=sum(1<<variables.index(t) for t in c['mixed_terms']);assert mask not in saved;saved.add(mask)
            d=matrix(source['arrows']+c['mixed_terms'],g,g,-1)
            assert not matrix_product(d,d)
            proof=c['unknot_retraction'];assert proof['status']=='SAT'
            f=matrix(proof['F'],u,g,0);p=matrix(proof['G'],g,u,0)
            assert not matrix_product(d,f)
            assert not matrix_product(p,d)
            assert matrix_product(p,f)=={(0,0,0,0)}
            if entry['knot']=='K1':
                # A single symbolic prescription works for every completion.
                mixed=c['mixed_terms']
                alpha=int([0,1,2,1] in mixed)^int([0,10,2,1] in mixed)
                beta=int([7,1,1,2] in mixed)^int([7,10,1,2] in mixed)
                projection=[[1,0,0,0],[10,0,0,0]]
                if alpha:projection.append([2,0,2,0])
                if beta:projection.append([8,0,0,2])
                f=matrix([[0,1,0,0]],u,g,0);p=matrix(projection,g,u,0)
                assert not matrix_product(d,f) and not matrix_product(p,d)
                assert matrix_product(p,f)=={(0,0,0,0)}
        assert saved==all_masks
        # Rebuild the linear equations directly by checking each single mixed
        # addition; quadratic mixed terms vanish because no two are composable.
        fixed=matrix(source['arrows'],g,g,-1);assert not matrix_product(fixed,fixed)
        assert not any(a[1]==b[0] for a in variables for b in variables)
        actual={}
        for i,t in enumerate(variables):
            d=fixed | matrix([t],g,g,-1)
            for key in matrix_product(d,d):actual[key]=actual.get(key,0)^(1<<i)
        assert set(actual.values())==set(row_masks)
        report.append({'knot':entry['knot'],'assignments_checked':1<<len(variables),
                       'square_zero_lifts':len(saved),'verified_unknot_retractions':len(saved),
                       'uniform_K1_projection_verified':entry['knot']=='K1'})
    record={'status':'EXACT_ALGEBRA_VERIFIED_NOT_A_SLICE_CERTIFICATE','checks':report,
            'complex_sha256':hashlib.sha256(Path(complex_path).read_bytes()).hexdigest(),
            'lift_sha256':hashlib.sha256(Path(lift_path).read_bytes()).hexdigest()}
    Path(output).write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('complexes');p.add_argument('lifts');p.add_argument('output')
    a=p.parse_args();verify(a.complexes,a.lifts,a.output)
