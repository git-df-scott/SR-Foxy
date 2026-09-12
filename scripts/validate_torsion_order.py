#!/usr/bin/env python3
"""Cross-check monomial Smith form by GF2 ranks modulo U^N."""
import argparse
import json
from pathlib import Path
import snappy
from torsion_order import arrows,monomial_smith,torsion_order


def binary_rank(rows):
    pivots={}
    for row in rows:
        while row:
            p=row.bit_length()-1
            if p in pivots:row^=pivots[p]
            else:pivots[p]=row;break
    return len(pivots)


def truncated_rank(h,N):
    ids={g:i for i,g in enumerate(h['generators'])};n=len(ids);rows=[0]*(n*N)
    for a,b,e,v in arrows(h):
        if v:continue
        for k in range(N-e):rows[ids[b]*N+k+e]^=1<<(ids[a]*N+k)
    return binary_rank(rows)


def run(output,extended=False):
    if Path(output).exists():raise FileExistsError(output)
    controls=[{'entries':{(0,0):1,(0,1):2,(1,0):2},'smith':[1,3]},
              {'entries':{(0,0):1,(0,1):2,(1,1):1},'smith':[1,1]}]
    for c in controls:assert monomial_smith(c['entries'])==c['smith']
    inputs=[(n,snappy.Link(n).PD_code()) for n in ['6_3','6_1','8_19']]
    inputs += [('K1',json.loads(Path('data/knots/AbeTagami_K_1.json').read_text())['pd_code_snappy_0indexed']),
               ('J149',json.loads(Path('results/coupled_small_targets.json').read_text())['candidates'][0]['endpoint_pd'])]
    if extended:
        inputs += [(name,json.loads(Path('data/knots/'+name+'.json').read_text())['pd_code_snappy_0indexed'])
                   for name in ['18nh00000601','K_B_0friend','GST_knot']]
    result={'status':'TWO_ALGORITHM_EXACT_TORSION_CHECK','controls':[{'entries':[[i,j,e] for (i,j),e in c['entries'].items()],'smith':c['smith']} for c in controls],
            'knots':[],'meaning':'Actual elementary divisors and independent ranks of the differential over F2[U]/U^N. Largest entry exponent is diagnostic only.'}
    for name,pd in inputs:
        h=snappy.Link(pd).knot_floer_homology(complex=True);out=dict(name=name,pd=pd,**torsion_order(h));checks=[]
        assert out['localized_homology_rank']==1
        for N in range(1,out['torsion_order']+3):
            actual=truncated_rank(h,N);expected=sum(max(0,N-e) for e in out['smith_exponents'])
            assert actual==expected
            checks.append({'N':N,'binary_rank':actual,'predicted_rank':expected})
        out['independent_truncation_checks']=checks;result['knots'].append(out)
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print([(r['name'],r['max_U_exponent'],r['torsion_order']) for r in result['knots']])


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output');p.add_argument('--extended',action='store_true');a=p.parse_args();run(a.output,a.extended)
