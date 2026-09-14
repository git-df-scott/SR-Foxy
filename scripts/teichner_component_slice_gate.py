#!/usr/bin/env python3
"""Restore cheap component slice filters without native multivariate minors."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib,json
from math import isqrt
from pathlib import Path
import snappy,sympy
from component_guided_bands import parts
from fusion_successors import diagram_signature
from nonfibered_reverse_audit import hfk
T=sympy.Symbol('t')

def norm_test(P):
    def canonical(p):
        p=sympy.Poly(p,T);return tuple(int(x) for x in (p if p.LC()>0 else -p).all_coeffs())
    unit,factors=sympy.factor_list(P.as_expr(),T);multiplicity={canonical(f):n for f,n in factors}
    witnesses=[]
    for f,n in factors:
        key=canonical(f);reverse=canonical(sympy.Poly.from_list(list(reversed(key)),T))
        if (key==reverse and n%2) or (key!=reverse and multiplicity.get(reverse,0)!=n):witnesses.append({'factor':list(key),'multiplicity':n,'reciprocal':list(reverse),'reciprocal_multiplicity':multiplicity.get(reverse,0)})
    return witnesses

def run():
    # Exact polynomial controls: a norm, an unpaired self-reciprocal factor,
    # and a non-self-reciprocal pair.
    assert not norm_test(sympy.Poly((T*T-3*T+1)**2,T))
    assert norm_test(sympy.Poly(T*T-3*T+1,T))
    assert not norm_test(sympy.Poly((2*T-1)*(2-T),T))
    base=Path('results/teichner_live_frontier.json');D=json.loads(base.read_text());rows={};cache={};hashes={str(base):hashlib.sha256(base.read_bytes()).hexdigest()}
    for j in ['941','946']:
        inputs=[('mixed',r) for r in D['partners'][j]['live_frontier']]
        p=Path('results/teichner_D01_J'+j+'_third_band.json');raw=p.read_bytes();R=json.loads(raw);assert R['complete'];hashes[str(p)]=hashlib.sha256(raw).hexdigest();inputs += [('third',r) for r in R['frontier']];rows[j]=[]
        for i,(origin,r) in enumerate(inputs):
            keys=[]
            for Q in parts(snappy.Link(r['endpoint_pd'])):
                key=diagram_signature(Q.PD_code()) if Q.crossings else 'U';cache[key]={'pd':Q.PD_code()};keys.append(key)
            rows[j].append({'index':i,'origin':origin,'depth':r['depth'],'components':keys,'certificate_prefix':r['certificate_prefix'],'endpoint_pd':r['endpoint_pd']})
    def compute(item):
        key,row=item
        if key=='U':return key,dict(row,determinant=1,rejections=[],status='known_unknot')
        try:
            V=sympy.Matrix(snappy.Link(row['pd']).seifert_matrix());det=abs(int((V+V.T).det(method='domain-ge')));row['determinant']=det;row['rejections']=[]
            if isqrt(det)**2!=det:row['rejections'].append('determinant_not_square')
            else:
                try:
                    H=hfk(row['pd']);row['HFK']=H
                    if H['tau']!=0:row['rejections'].append('tau_nonzero')
                    if not any(A==0 and M==0 and n for A,M,n in H['ranks']):row['rejections'].append('ribbon_HFK_unknot_injection_fails')
                    coeff=Counter()
                    for A,M,n in H['ranks']:coeff[A]+=n*(-1 if M%2 else 1)
                    coeff={a:n for a,n in coeff.items() if n};lo=min(coeff);P=sympy.Poly(sum(n*T**(a-lo) for a,n in coeff.items()),T)
                    if P.eval(1)==-1:P=-P
                    assert P.eval(1)==1 and abs(int(P.eval(-1)))==det
                    row['alexander_coefficients_low_to_high']=[int(P.nth(i)) for i in range(P.degree()+1)];row['norm_failure_witnesses']=norm_test(P)
                    if row['norm_failure_witnesses']:row['rejections'].append('Fox_Milnor_norm_fails')
                except Exception as e:row['HFK_unknown']=repr(e)
            row['status']='checked'
        except Exception as e:row.update(status='UNKNOWN',error=repr(e),rejections=[])
        return key,row
    with ThreadPoolExecutor(max_workers=4) as pool:cache=dict(pool.map(compute,cache.items()))
    summary={}
    for j,group in rows.items():
        bad=[]
        for row in group:
            row['direct_obstruction']=any(cache[k]['rejections'] for k in row['components'])
            if row['direct_obstruction']:bad.append(row['certificate_prefix'])
        for row in group:row['direct_or_inherited_obstruction']=any(row['certificate_prefix'][:len(p)]==p for p in bad)
        summary[j]={'input_paths':len(group),'direct_exclusions':sum(r['direct_obstruction'] for r in group),'direct_or_inherited_exclusions':sum(r['direct_or_inherited_obstruction'] for r in group),'retained_unknown':sum(not r['direct_or_inherited_obstruction'] for r in group)}
    rec={'complete':True,'input_hashes':hashes,'components':cache,'rows':rows,'summary':summary,'unknown_component_calculations':sum(r['status']=='UNKNOWN' or 'HFK_unknown' in r for r in cache.values()),'scope':'Each component must be ribbon to finish this pure-fission disk search. Determinant, tau, Fox-Milnor and unknot HFK injection are necessary only. Unknowns retained.'}
    Path('results/teichner_component_slice_gate.json').write_text(json.dumps(rec,separators=(',',':'))+'\n');print(json.dumps(summary),flush=True);print('components',len(cache),'unknown',rec['unknown_component_calculations'],flush=True)
if __name__=='__main__':run()
