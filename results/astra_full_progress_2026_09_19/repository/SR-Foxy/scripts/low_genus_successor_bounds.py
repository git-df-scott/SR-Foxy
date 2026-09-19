#!/usr/bin/env python3
"""Exact consequences of Alexander divisibility, Fox-Milnor, and HFK injection.

These are necessary restrictions on common upper targets, never a statement
that such a target exists or cannot exist in higher genus.
"""
import json
from pathlib import Path
from collections import defaultdict
import sympy as s
import snappy


def euler(h):
    r=defaultdict(int)
    for (a,m),v in h.items():r[a]+=(-1 if m%2 else 1)*v
    return dict(r)


def tensor(h,k):
    r=defaultdict(int)
    for (a,m),v in h.items():
        for (b,n),w in k.items():r[a+b,m+n]+=v*w
    return dict(r)


def run(output):
    if Path(output).exists():raise FileExistsError(output)
    H=[snappy.Link(json.loads(Path('data/knots/'+n+'.json').read_text())['pd_code_snappy_0indexed']).knot_floer_homology()['ranks']
       for n in ['AbeTagami_K_0_K_-1__6_3','AbeTagami_K_1']]
    t=s.Symbol('t');delta=t**2-3*t+5-3/t+1/t**2
    envelope={g:max(h.get(g,0) for h in H) for g in set().union(*H)};chi=euler(envelope)
    assert sum(envelope.values())==21
    assert all(s.expand(sum(v*t**a for a,v in euler(h).items())-delta)==0 for h in H)
    def bound(poly):
        coeff={a:int(s.expand(poly).coeff(t,a)) for a in range(-8,9)}
        return sum(envelope.values())+sum(abs(coeff.get(a,0)-chi.get(a,0)) for a in coeff.keys()|chi.keys())
    assert bound(delta)==29
    fibered=[]
    # Every monic degree-2 factor with constant +/-1 and f(1)=+/-1,
    # modulo reciprocal/sign, gives exactly these three norm quotients.
    quotient_set=set()
    for c in [-1,1]:
        for value in [-1,1]:
            b=value-1-c;f=t*t+b*t+c;quotient_set.add(s.expand(f*f.subs(t,1/t)))
    assert len(quotient_set)==3
    for q in sorted(quotient_set,key=str):
        p=s.expand(delta*q)
        fibered.append({'quotient':str(q),'Alexander':str(p),'determinant':abs(int(p.subs(t,-1))),
                        'necessary_rank_bound':bound(p)})
    result={'status':'NECESSARY_LOW_GENUS_RESTRICTIONS','delta':str(delta),
        'bigraded_envelope':[[a,m,v] for (a,m),v in sorted(envelope.items())],
        'envelope_rank':21,'envelope_euler':str(sum(v*t**a for a,v in chi.items())),
        'same_Alexander_rank_bound':29,'same_Alexander_genus_3_rank_bound':33,
        'genus_3_nonconstant_quotient_minimum_rank':117,
        'common_fibered_minimum_genus':4,'fibered_genus_4_options':fibered,'pinned_targets':[],
        'sources':['https://arxiv.org/abs/1902.04050','https://arxiv.org/abs/1907.09031','https://www.unige.ch/math/folks/conway/Notes/AlgebraicConcordanceCassonGordon.pdf'],
        'limitations':'Source HFK is software-dependent. Rank bounds do not prove existence. Genus and fibered qualifications are essential. Named stabilizers below are only rank-screened, not newly certified ribbon.'}
    for name in ['6_1','8_8','8_9','8_20','9_27','9_41','9_46','10_3','10_22','10_87','10_99','11n42']:
        R=snappy.Link(name);h=R.knot_floer_homology();prod=tensor(H[0],h['ranks'])
        result['pinned_targets'].append({'stabilizer':name,'pd':R.PD_code(),'ranks':[[a,m,n] for (a,m),n in sorted(h['ranks'].items())],
            'delta_support':sorted({m-a for a,m in h['ranks']}),'target_rank':sum(prod.values()),
            'K1_injection_passed':all(prod.get(g,0)>=n for g,n in H[1].items())})
    # Q#(-Q) is ribbon for every Q; useful controls without a knot-table claim.
    for name in ['8_19','10_124','T(3,7)']:
        Q=snappy.Link(name);h=Q.knot_floer_homology()['ranks'];mirror={(-a,-m):n for (a,m),n in h.items()}
        r=tensor(h,mirror);prod=tensor(H[0],r)
        result['pinned_targets'].append({'stabilizer':name+' # inverse('+name+')','ribbon_reason':'K # (-K) standard ribbon disk',
            'companion_pd':Q.PD_code(),'delta_support':sorted({m-a for a,m in r}),
            'target_rank':sum(prod.values()),'K1_injection_passed':all(prod.get(g,0)>=n for g,n in H[1].items())})
    Path(output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['fibered_genus_4_options','common_fibered_minimum_genus']}))
    print([(r['stabilizer'],r['K1_injection_passed']) for r in result['pinned_targets']])


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('output');run(p.parse_args().output)
