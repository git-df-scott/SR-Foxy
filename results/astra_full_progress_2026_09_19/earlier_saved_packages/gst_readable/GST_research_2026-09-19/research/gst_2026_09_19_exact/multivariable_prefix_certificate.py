"""Close the three exceptional L3/T1 prefixes using separate meridian variables.
Cha--Friedl, arXiv:1001.0926, Theorem 1.1 with trivial representation:
a two-component slice link has Alexander rank one over Q(x,y).
"""
import json,time
from pathlib import Path
import sympy as s
import spherogram
from spherogram.links.bands.core import Band
from pd_algebra import DSU,structure,component_pd,determinant,alexander
from prefix_certify import bareiss_det
from extended_prefix_search import detmod
ROOT=Path(__file__).parent

def multivariable_fox(pd,variables):
    st=structure(pd)
    if len(variables)!=len(st['tours']):raise ValueError('One variable per component is required')
    uf=DSU(st['components'])
    for a,b,c,d in pd:uf.union(b,d)
    roots=sorted({uf.find(a) for a in st['components']});ix={a:i for i,a in enumerate(roots)}
    arc={a:ix[uf.find(a)] for a in st['components']}
    weight={arc[a]:variables[c] for a,c in st['components'].items()}
    A=s.zeros(len(pd),len(roots))
    for row,(u,o,v,eps) in enumerate(st['oriented']):
        tu=variables[st['components'][u]];to=variables[st['components'][o]]
        if eps==1:
            A[row,arc[o]]+=1-tu;A[row,arc[u]]+=to;A[row,arc[v]]-=1
        else:
            A[row,arc[o]]+=tu-1;A[row,arc[u]]+=1;A[row,arc[v]]-=to
    d1=s.Matrix([weight[i]-1 for i in range(len(roots))])
    assert A*d1==s.zeros(len(pd),1)
    return A,st

def main():
    source=json.loads((ROOT/'gst48.json').read_text())['pd'];K=spherogram.Link(source)
    records=json.loads((ROOT/'extended_prefix_L3_T1.json').read_text())['records'];out=[]
    for r in records:
        if r['status']!='inconclusive_specializations_zero':continue
        q=r['pd'];assert [list(z) for z in K.add_band(Band(r['band'])).PD_code()]==q
        A,st=multivariable_fox(q,[2,3]);n=A.cols
        # This same fixed cofactor works for all three exceptions.
        rows=list(range(n-1));cols=list(range(n-1));M=[[int(x) for x in row] for row in A.extract(rows,cols).tolist()]
        d=bareiss_det(M);assert d and int(s.Matrix(M).det(method='domain-ge'))==d
        assert d%1000003==detmod(M,1000003)
        entry={'band':r['band'],'pd':q,'variables':[2,3], 'rows':rows,'columns':cols,'specialized_matrix':M,
          'minor_determinant':d,'minor_determinant_mod_1000003':d%1000003,
          'multivariable_Alexander_rank':0,'slice_link':False,
          'component_determinants':[determinant(component_pd(q,i,st)) for i in range(2)]}
        if r['band']=='7f42_0_1':
            # Also test unequal meridional weights in an ordinary infinite cyclic cover.
            B,_=multivariable_fox(q,[2,4]);dd=bareiss_det(B[:n-1,:n-1].tolist())
            assert dd
            entry['weighted_cyclic_map']={'meridian_weights':[1,2],'t':2,'minor_determinant':dd,'Alexander_rank':0}
        out.append(entry);print(r['band'],'minor',d,'det components',entry['component_determinants'],flush=True)
    assert len(out)==3
    result={'source_theorem':'Cha--Friedl, Twisted torsion invariants and link concordance, arXiv:1001.0926 Theorem 1.1, trivial 1-dimensional representation; abelianization Z^2.',
      'scope':'The three remaining explicit bands in L3/T1; completes exclusion of all 1698 enumerated first bands, not arbitrary first bands.',
      'all_1698_prefixes_excluded':True,'records':out}
    (ROOT/'multivariable_prefix_certificates.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
