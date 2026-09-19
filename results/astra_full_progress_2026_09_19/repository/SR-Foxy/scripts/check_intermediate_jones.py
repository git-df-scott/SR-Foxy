#!/usr/bin/env python3
"""Exact Jones split-product test, sufficient for nonsplitting when unequal.

Unlike generic Alexander nullity, this is not a concordance invariant and can
detect linked first stages in our ribbon movies. Equality is inconclusive.
"""
import argparse
import gzip
import json
from pathlib import Path
from sage.all import QQ,LaurentPolynomialRing
import snappy
import regina


def jones(L):
    # A second topology library avoids Morse-exhaustion failures on some
    # Spherogram link diagrams. Regina documents the conversion x -> -q.
    R=LaurentPolynomialRing(QQ,'q');q=R.gen()
    if not L.crossings:return (q+q**-1)**(L.unlinked_unknot_components-1)
    G=regina.Link.fromPD([[a+1 for a in c] for c in L.PD_code()]);p=G.jones()
    v=sum((QQ(str(p[i]))*(-q)**i for i in range(p.minExp(),p.maxExp()+1)),R(0))
    return v*(q+q**-1)**L.unlinked_unknot_components


def check(pd):
    L=snappy.Link(pd);assert len(L.link_components)==2
    P=L.sublink([0]);Q=L.sublink([1]);P.simplify('basic');Q.simplify('basic')
    # Selecting one component is known to give a knot. The sublink API can
    # drop its crossing-free circle without retaining the unknot counter.
    for K in [P,Q]:
        if not K.crossings:K.unlinked_unknot_components=1
    v=jones(L);p=jones(P);q=jones(Q);t=v.parent().gen()
    product=(t+t**-1)*p*q
    return {'pd':pd,'component_pd':[P.PD_code(),Q.PD_code()],
            'Jones':str(v),'component_Jones':[str(p),str(q)],'split_product':str(product),
            'nonsplit_by_Jones':bool(v!=product),'variable':'q','normalization':'V(unknot)=1; V(two-component unlink)=q+q^-1'}


def run(archive,output):
    if Path(output).exists():raise FileExistsError(output)
    rows=[r for x in gzip.open(archive,'rt') if (r:=json.loads(x))['type']=='first' and not r['detected_split_unknot']]
    rows.sort(key=lambda r:(len(r['simplified_intermediate_pd']),r['first_id']))
    # The split-product convention must be checked before the experiment.
    P=snappy.Link('3_1');Q=snappy.Link('4_1');n=2*len(P.crossings)
    split=P.PD_code()+[tuple(a+n for a in c) for c in Q.PD_code()]
    # Overlap the projections by a recorded-type RII placement, so this control
    # exercises the Jones calculation rather than only the split wrapper.
    from spherogram.links.simplify import reverse_type_II
    from spherogram.links.bands.core import normalize_crossing_labels
    S=snappy.Link(split);normalize_crossing_labels(S);fs=S.faces();nc=len(P.crossings)
    c=max((f for f in fs if all(x.crossing.label<nc for x in f)),key=len)[0]
    d=max((f for f in fs if all(x.crossing.label>=nc for x in f)),key=len)[0]
    reverse_type_II(S,c,d,len(S.crossings),len(S.crossings)+1,rebuild=True)
    control=check(S.PD_code());assert not control['nonsplit_by_Jones']
    assert jones(S)==S.jones_polynomial()
    hopf=check(snappy.Link('L2a1').PD_code());assert hopf['nonsplit_by_Jones']
    result={'archive':archive,'status':'EXACT_JONES_NONSPLITTING_TEST','backend':'Regina Jones; independent Spherogram overlap control','controls':[control,hopf],'checks':[],
        'limitations':'Jones implementation and PD construction are software dependencies. Inequality proves nonsplitting of this link, not nonexistence of other movies for the endpoint. Equality is inconclusive.'}
    for r in rows:
        c=check(r['simplified_intermediate_pd']);c.update(first_id=r['first_id'],placement=r['placement'],return_positions=r.get('face_return_positions'))
        result['checks'].append(c);Path(output).write_text(json.dumps(result,indent=2)+'\n')
        print('first',r['first_id'],'crossings',len(c['pd']),'nonsplit',c['nonsplit_by_Jones'],flush=True)
        if c['nonsplit_by_Jones']:break
    result['complete']=True
    Path(output).write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('archive');p.add_argument('output');a=p.parse_args();run(a.archive,a.output)
