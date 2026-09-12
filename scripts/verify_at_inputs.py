#!/usr/bin/env python3
"""Check the non-ribbon theorem's hypotheses on the actual stored PDs.

This does not require identifying the second PD with a named annulus twist.
It uses exact Alexander/HFK calculations and verified hyperbolic volumes.
"""
import argparse
import json
from pathlib import Path
from sage.all import PolynomialRing, QQ
import snappy


def run(output):
    if Path(output).exists(): raise FileExistsError(output)
    R=PolynomialRing(QQ,'t');t=R.gen();expected=t**4-3*t**3+5*t**2-3*t+1
    assert expected.is_irreducible()
    rows=[];volumes=[]
    for name in ['AbeTagami_K_0_K_-1__6_3','AbeTagami_K_1']:
        d=json.loads(Path('data/knots/'+name+'.json').read_text());pd=d['pd_code_snappy_0indexed']
        L=snappy.Link(pd);h=L.knot_floer_homology();poly=R(L.alexander_polynomial())
        poly=R(poly/t**poly.valuation()/poly.leading_coefficient())
        assert poly==expected and h['fibered'] and h['seifert_genus']==2
        M=L.exterior();verified,_=M.verify_hyperbolicity(bits_prec=100);assert verified
        volume=M.volume(verified=True,bits_prec=100);volumes.append(volume)
        rows.append({'name':name,'pd':pd,'Alexander':str(poly),'irreducible':True,
                     'HFK_ranks':[[int(a),int(m),int(n)] for (a,m),n in sorted(h['ranks'].items())],
                     'fibered':True,'genus':2,'verified_hyperbolic':True,
                     'volume_lower':str(volume.lower()),'volume_upper':str(volume.upper())})
    assert volumes[0].upper()<volumes[1].lower()
    result={'inputs':rows,'verified_volume_intervals_disjoint':True,
            'non_ribbon_implication':'Abe-Tagami Corollary 4.3 applied to these stored diagrams: their connected sum with the concordance inverse of the second is not ribbon.',
            'source':'https://arxiv.org/html/1502.01102v5',
            'limitations':'Exact HFK and Alexander results depend on computational libraries; no formal verification of their implementations. This proves no sliceness assertion.'}
    Path(output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output');a=p.parse_args();run(a.output)
