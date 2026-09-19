#!/usr/bin/env python3
"""Replay saved geometry and independently check polynomial/gate arithmetic."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import snappy
import sympy
from spherogram.links.bands.core import Band, add_one_band, normalize_crossing_labels
from component_guided_bands import controls, inspect, parts, jones, encoded, product, l1
from fission_ancestry_audit import determinant, deficits as hfk_deficits, square
from fusion_successors import diagram_signature, replay
from khovanov_upper_filter import parse_poincare, euler_check, deficits


def read(p):return json.loads(Path(p).read_text())


def main():
    rec={'status':'PASSED','counts':Counter(),'limitations':['Replay and exact invariants do not certify a concordance.','Jones equality does not recognize knot types or split links.','Ancestry exclusions concern pure-fission continuations of the specified links.']}
    controls();rec['positive_and_nonsplit_negative_controls']=True
    K0=snappy.Link(read('data/knots/AbeTagami_K_0_K_-1__6_3.json')['pd_code_snappy_0indexed']);K0.simplify('basic');K0sig=diagram_signature(K0.PD_code())
    for p in ['results/nonfibered_kh_survivors.json','results/K1_nonfibered_shortlist.json']:
        for r in read(p)['candidates']:assert replay(r);rec['counts']['forward_movies']+=1
    for p in ['results/component_guided_K0_to_K1.json','results/component_guided_K1_to_K0.json','results/normalized_component_neighborhoods.json','results/guided_second_fission_25533.json']:
        d=read(p);assert d['complete']
        for r in d['runs']:
            assert r['complete']
            if 'start_pd' in r:start_pd=r['start_pd']
            else:
                original=Path(d['parameters']['input']);assert hashlib.sha256(original.read_bytes()).hexdigest()==d['input_sha256']
                start_pd=next(x['start_pd'] for x in read(original)['runs'] if x['index']==r['index'])
            J=snappy.Link(start_pd)
            for c in r['matches']+r.get('best',[]):
                L=add_one_band(J,c['band']);assert L.is_planar()
                assert L.PD_code()==[tuple(x) for x in c['raw_pd']];assert not c['certified_concordance']
                rec['counts']['raw_reverse_bands']+=1
                P=parts(L);pol=[jones(K) for K in P]
                assert sorted(encoded(q) for q in pol)==sorted(c['component_Jones'])
                if 'whole_Jones' in c:
                    whole=jones(L);split={0:1}
                    for q in pol:split=product(split,q)
                    for _ in range(len(P)-1):split=product(split,{-1:1,1:1})
                    assert encoded(whole)==c['whole_Jones'] and encoded(split)==c['split_product_Jones']
                    assert (whole!=split)==c['nonsplit_by_Jones'];rec['counts']['whole_link_Jones']+=1
                if 'normalization' in c:
                    assert L.linking_number()==0;rec['counts']['zero_linking_normalizations']+=1
                    i=c['wanted_component'];match=diagram_signature(c['component_pd'][i])==K0sig;unknot=not c['component_pd'][1-i]
                    assert match==c['component_diagram_matches_target'] and unknot==c['other_component_is_unknot_by_simplification']
                    if match and unknot:rec['counts']['recognized_K0_and_unknot_components']+=1
    reg=read('results/fission_twist_orientation_regression.json');J=snappy.Link(reg['start_pd']);B=Band(reg['band'])
    old=add_one_band(J,B).linking_number();new=add_one_band(J,Band(B.cs_along_top,B.arc_is_under,B.num_twist+2)).linking_number()
    assert old==reg['linking_at_t'] and new==reg['linking_at_t_plus_2'] and abs(new-old)!=1
    rec['signed_linking_regression_reproduced']=True
    two=read('results/two_fission_nonfibered_25533.json');J=snappy.Link(read(two['target'])['candidates'][0]['endpoint_pd'])
    for r in two['intermediates']:
        I=add_one_band(J,r['first_band']);normalize_crossing_labels(I);I.simplify('basic')
        if I.unlinked_unknot_components:
            pd=I.PD_code();n=2*len(pd);I=snappy.Link(pd+[(n,n+1,n+1,n+2),(n+2,n+3,n+3,n)])
        normalize_crossing_labels(I)
        assert diagram_signature(I.PD_code())==diagram_signature(r['intermediate_pd'])
        rec['counts']['first_fission_replays']+=1
    ancestry=read('results/fission_ancestry_25533.json');assert ancestry['complete']
    for key,c in ancestry['components'].items():
        assert diagram_signature(c['pd'])==key
        if c['pd']:
            K=snappy.Link(c['pd']);V=sympy.Matrix(K.seifert_matrix());det=abs(int((V+V.T).det()))
        else:det=1
        assert det==c['det']==determinant(dict(c['Jones']))
        H=c['HFK'];assert abs(sum(n*(-1 if (a+m)%2 else 1) for a,m,n in H['ranks']))==det
        rec['counts']['Seifert_Jones_HFK_determinants']+=1
    # Recompute each saved assignment, retaining unknowns instead of rejecting.
    for r in ancestry['rows']:
        C=[ancestry['components'][k] for k in r['component_keys']]
        for side,A in r['sources'].items():
            S=ancestry['sources'][side]
            for a in A:
                T=C[a['target_component']];D=C[1-a['target_component']];why=[]
                if not square(S['det']*T['det']):why.append('target_determinant_product_not_square')
                if not square(D['det']):why.append('disk_determinant_not_square')
                if hfk_deficits(S['HFK']['ranks'],T['HFK']['ranks']):why.append('target_HFK_injection_fails')
                if T['HFK']['tau']!=S['HFK']['tau']:why.append('target_tau_differs')
                if hfk_deficits([[0,0,1]],D['HFK']['ranks']):why.append('unknot_HFK_injection_fails')
                if D['HFK']['tau']!=0:why.append('disk_tau_nonzero')
                assert why==a['rejections'] and (not why)==a['passes_necessary_any_number_of_fissions']
    gate=read('results/fission_ancestry_Kh/manifest.json');assert gate['complete']
    prior=read('results/nonfibered_khovanov_filter/manifest.json');low=next(r for r in prior['runs'] if r['name']=='K1');low={(i,j):n for i,j,n in low['ranks']}
    obstruction={}
    for r in gate['runs']:
        assert r['status']=='checked';kh=parse_poincare(Path('results/fission_ancestry_Kh',r['name']+'.log').read_text())
        assert euler_check(r['pd'],kh)['passed'];assert deficits(low,kh)==r['K1_deficits']
        obstruction[r['key']]=bool(deficits(low,kh))
        rec['counts']['component_Kh_logs']=rec['counts']['component_Kh_logs']+1
    kept={r['first_band'] for r in ancestry['rows'] if any(a['passes_necessary_any_number_of_fissions'] and not obstruction[r['component_keys'][a['target_component']]] for a in r['sources']['K1'])}
    assert kept==set(gate['retained_first_bands'])=={'6267660c_0_0','2b2a271f_1_0'}
    rec['counts']['ancestry_retained']=len(kept);rec['counts']['ancestry_excluded']=len(ancestry['rows'])-len(kept)
    rec['sha256']={}
    prefixes=['component_guided','normalized_component','fission_ancestry','fission_twist','guided_second_fission']
    paths=[p for p in Path('results').rglob('*') if p.is_file() and any(p.relative_to('results').parts[0].startswith(s) for s in prefixes)]
    paths += [Path('scripts',n+'.py') for n in ['component_guided_bands','normalize_fission_twists','fission_ancestry_audit','fission_ancestry_khovanov','guided_second_fission','check_component_session']]
    paths += [Path('research/17_fission_ancestry_and_linking.md'),Path('README.md'),Path('HANDOFF.md')]
    for p in paths:rec['sha256'][str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
    Path('results/component_session_validation.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec['counts']))


if __name__=='__main__':main()
