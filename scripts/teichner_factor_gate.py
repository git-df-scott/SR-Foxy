#!/usr/bin/env python3
"""A ribbon-only component gate for saved Teichner frontier links.
Abe--Tagami Corollary 4.3: two fibered knots with irreducible Alexander
polynomials can have ribbon difference only if they are isotopic.
"""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib,json
from pathlib import Path
import snappy,sympy
from component_guided_bands import parts,jones
from fusion_successors import diagram_signature
from nonfibered_reverse_audit import hfk

def run():
    cache={};rows={};hashes={};t=sympy.Symbol('t')
    for j in ['941','946']:
        p=Path('results/teichner_D01_J'+j+'_mixed.json');hashes[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest();D=json.loads(p.read_text());assert D['complete'];rows[j]=[]
        for i,r in enumerate(D['frontier']):
            pairlist=[]
            for c,P in enumerate(parts(snappy.Link(r['endpoint_pd']))):
                if not P.crossings:continue
                pieces=P.deconnect_sum()
                if len(pieces)!=2:continue
                keys=[]
                for Q in pieces:
                    Q.simplify('basic');key=diagram_signature(Q.PD_code()) if Q.crossings else 'U';cache[key]={'pd':Q.PD_code()};keys.append(key)
                pairlist.append({'component':c,'factors':keys})
            rows[j].append({'index':i,'depth':r['depth'],'pairs':pairlist})
    def compute(item):
        key,v=item
        if not v['pd']:return key,dict(v,status='unknot_not_eligible')
        try:
            H=hfk(v['pd']);v['HFK']=H;v['status']='computed'
            coeff=Counter()
            for A,M,n in H['ranks']:coeff[A]+=n*(-1 if M%2 else 1)
            coeff={A:n for A,n in coeff.items() if n};shift=min(coeff);P=sympy.Poly(sum(n*t**(A-shift) for A,n in coeff.items()),t)
            if P.eval(1)==-1:P=-P
            assert P.eval(1)==1
            v['alexander_from_HFK']=[int(P.nth(i)) for i in range(P.degree()+1)];v['irreducible']=bool(P.is_irreducible and P.degree()>0)
            # Exact independent specialization checks from the Seifert matrix.
            L=snappy.Link(v['pd']);V=sympy.Matrix(L.seifert_matrix());N=V.rows;assert N%2==0;g=P.degree()//2
            assert P.degree()%2==0
            checks=[]
            for x in [-1,1,2,3]:
                got=int((x*V-V.T).det(method='domain-ge'));expected=int(x**(N//2-g)*P.eval(x));checks.append([x,got,expected]);assert got==expected
            v['seifert_evaluation_checks']=checks;v['eligible']=bool(H['fibered'] and v['irreducible'])
            v['Jones']=sorted([[e,n] for e,n in jones(L).items()])
        except Exception as e:v.update(status='UNKNOWN',eligible=False,error=repr(e))
        return key,v
    with ThreadPoolExecutor(max_workers=4) as pool:
        cache=dict(pool.map(compute,cache.items()))
    for group in rows.values():
        for r in group:
            r['ribbon_completion_obstructed']=False
            for p in r['pairs']:
                a,b=[cache[k] for k in p['factors']];p['applies']=False
                if not a.get('eligible') or not b.get('eligible'):continue
                # Compare A to mirror(B). Distinct Jones is an independent
                # direct non-isotopy witness; do not infer identity from equality.
                aj=a['Jones'];mb=sorted([[-e,n] for e,n in b['Jones']]);p['Jones_distinguishes_A_from_mirror_B']=aj!=mb
                p['applies']=aj!=mb;r['ribbon_completion_obstructed']|=p['applies']
    summary={j:{'frontier':len(v),'obstructed':sum(r['ribbon_completion_obstructed'] for r in v),'first_stage_obstructed':sum(r['ribbon_completion_obstructed'] and r['depth']==1 for r in v)} for j,v in rows.items()}
    result={'complete':True,'source':'https://arxiv.org/html/1502.01102v3','theorem':'Corollary 4.3','input_hashes':hashes,'factors':cache,'rows':rows,'summary':summary,'scope':'Only two diagrammatically separated factors in a component, each fibered with irreducible Alexander polynomial, and distinguished from the other factor mirror by Jones. HFK is computational evidence, with independent Seifert evaluations. No slicing obstruction; pure ribbon-disk continuations only.'}
    Path('results/teichner_factor_gate.json').write_text(json.dumps(result,separators=(',',':'))+'\n');print(json.dumps(summary),flush=True);print('unknown factors',sum(v['status']=='UNKNOWN' for v in cache.values()),flush=True)
if __name__=='__main__':run()
