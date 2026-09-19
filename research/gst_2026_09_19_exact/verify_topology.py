"""Independent construction checks; requires pinned topology packages.
These are computational checks, not a formal proof of the HFK engine.
"""
import json, random, time, platform, importlib.metadata
from pathlib import Path
from collections import Counter
import sympy as s
import spherogram, regina
from spherogram.links.bands import core
from pd_algebra import t, normalize
from prefix_certify import get_result
ROOT=Path(__file__).parent

def serial_hfk(h):
    out={k:v for k,v in h.items() if k not in ['ranks','generators','differentials']}
    out['ranks']=[{'A':a,'M':m,'rank':v} for (a,m),v in sorted(h['ranks'].items())]
    if 'generators' in h:
        out['generators']=[{'id':i,'A':a,'M':m} for i,(a,m) in sorted(h['generators'].items())]
        out['differentials']=[{'from':i,'to':j,'coefficient':v} for (i,j),v in sorted(h['differentials'].items())]
    return out

def rankmod(M,p):
    a=[[int(x)%p for x in row] for row in M]; nr=len(a);nc=len(a[0]) if nr else 0;r=0
    for c in range(nc):
        pivot=next((i for i in range(r,nr) if a[i][c]),None)
        if pivot is None: continue
        a[r],a[pivot]=a[pivot],a[r];z=pow(a[r][c],-1,p)
        a[r]=[(x*z)%p for x in a[r]]
        for i in range(r+1,nr):
            if a[i][c]:
                z=a[i][c];a[i]=[(x-z*y)%p for x,y in zip(a[i],a[r])]
        r+=1
        if r==nr:break
    return r

def main():
    start=time.time(); pd=json.loads((ROOT/'gst48.json').read_text())['pd'];K=spherogram.Link(pd)
    r=K.knot_floer_homology(complex=True); ranks=r['ranks']
    f=t**8-2*t**7+t**6+t**5-2*t**4+t**3-1
    expected=s.expand(f*f.subs(t,1/t))
    euler=s.expand(sum((-1 if m%2 else 1)*n*t**a for (a,m),n in ranks.items()))
    assert s.expand(expected-euler)==0
    assert ranks=={(-a,m-2*a):n for (a,m),n in ranks.items()}
    rm=K.mirror().knot_floer_homology();assert rm['ranks']=={(-a,-m):n for (a,m),n in ranks.items()}
    r3=K.knot_floer_homology(prime=3);assert r3['ranks']==ranks
    rng=random.Random(4311); labels=sorted({x for q in pd for x in q});shuffled=labels[:];rng.shuffle(shuffled); rename=dict(zip(labels,shuffled))
    pd2=[[rename[x] for x in q] for q in pd];rng.shuffle(pd2)
    rr=spherogram.Link(pd2).knot_floer_homology();assert rr['ranks']==ranks
    gens=r['generators'];diff=r['differentials'];ids=sorted(gens);index={v:i for i,v in enumerate(ids)};n=len(ids)
    assert Counter(gens.values())==Counter(ranks)
    V=[[0]*n for _ in range(n)]; H=[[0]*n for _ in range(n)]
    for (i,j),c in diff.items():
        ai,mi=gens[i];aj,mj=gens[j]
        num=mj-mi+1;assert num%2==0
        u=num//2;v=ai-aj+u
        assert u>=0 and v>=0 and u*v==0 and u+v>0,(i,j,u,v)
        if u==0:V[index[i]][index[j]]=c%2
        if v==0:H[index[i]][index[j]]=c%2
    # UV=0 d^2 check: sum coefficients separately for pure U and pure V monomials.
    adjacency={i:[] for i in ids}
    for (i,j),c in diff.items():
        ai,mi=gens[i];aj,mj=gens[j];u=(mj-mi+1)//2;v=ai-aj+u
        adjacency[i].append((j,c,u,v))
    d2={}
    for i in ids:
        for j,c,u,v in adjacency[i]:
            for k,d,x,y in adjacency[j]:
                if (u+x)*(v+y):continue
                key=(i,k,u+x,v+y);d2[key]=(d2.get(key,0)+c*d)%2
    assert not any(d2.values())
    rv=rankmod(V,2);rh=rankmod(H,2);assert n-2*rv==1 and n-2*rh==1
    # Independently build the same finite band class with Spherogram, then
    # compare exact Regina diagram signatures, not floating-point invariants.
    manual=json.loads((ROOT/'face_band_results.json').read_text())['records']
    def sig(q):
        lab={a:i+1 for i,a in enumerate(sorted({x for z in q for x in z}))}
        return regina.Link.fromPD([[lab[x] for x in z] for z in q]).sig(False,True,False)
    manual_by_sig={sig(get_result(pd,a)):a for a in manual}
    manual_multiset=Counter(sig(get_result(pd,a)) for a in manual)
    bands=list(core.simple_bands(K,max_twists=0,max_band_len=2))
    other=[]
    for b in bands:
        L=K.add_band(b);q=[list(x) for x in L.PD_code()];sg=sig(q)
        assert sg in manual_by_sig
        other.append({'band':b.compressed_spec(),'diagram_signature':sg,'manual_edge_labels':manual_by_sig[sg]['edge_labels'],'pd':q})
    assert Counter(a['diagram_signature'] for a in other)==manual_multiset
    (ROOT/'spherogram_band_crosscheck.json').write_text(json.dumps({'count':len(bands),'all_exact_diagram_signatures_match':True,'records':other},indent=2)+'\n')
    (ROOT/'gst48_uv0_complex.json').write_text(json.dumps(serial_hfk(r),indent=2)+'\n')
    (ROOT/'gst48_hfk_prime3.json').write_text(json.dumps(serial_hfk(r3),indent=2)+'\n')
    (ROOT/'gst48_hfk_mirror.json').write_text(json.dumps(serial_hfk(rm),indent=2)+'\n')
    # Seifert-matrix construction is independent of the Fox calculation.
    S=s.Matrix(K.seifert_matrix());assert S==s.Matrix(json.loads((ROOT/'spherogram_seifert_matrix.json').read_text()))
    poly=normalize((t*S-S.T).det(method='domain-ge'))
    assert s.expand(poly-t**8*expected)==0
    assert (S-S.T).det(method='domain-ge')==1
    result={'python':platform.python_version(),'versions':{p:importlib.metadata.version(p) for p in ['sympy','spherogram','snappy','regina','knot_floer_homology']},
      'hfk_total_rank':r['total_rank'],'genus':r['seifert_genus'],'fibered':r['fibered'],
      'top_Alexander_ranks':{str(m):v for (a,m),v in ranks.items() if a==10},
      'euler_equals_exact_Alexander':True,'conjugation_symmetry':True,'mirror_duality':True,'prime3_ranks_agree':True,'renumbered_PD_ranks_agree':True,
      'uv0_differential_squared_zero':True,'uv0_generators':n,'vertical_differential_rank':rv,'horizontal_differential_rank':rh,'vertical_homology_dimension':n-2*rv,'horizontal_homology_dimension':n-2*rh,
      'independent_face_band_enumeration_count':len(bands),'exact_Regina_signature_multisets_agree':True,'independent_Seifert_matrix_size':S.rows,'Seifert_Alexander_agrees':True,'elapsed_seconds':time.time()-start}
    (ROOT/'topology_verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__': main()
