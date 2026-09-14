#!/usr/bin/env python3
"""Prioritize first bands attached across the summand boundary; save full paths.
This is a biased search, not a complete ribbonness test. Strong-sliceness
rank filtering is necessary only. Cache hits require certificate replay.
"""
import argparse,hashlib,json,random,time
from math import isqrt
from collections import Counter
from pathlib import Path
import snappy
import sympy
from spherogram.links.bands.core import min_len_bands,add_one_band,normalize_crossing_labels
from spherogram.links.bands.search import linking_nums_all_zero,is_unlink_exterior,verify_ribbon_to_unknot
from fusion_successors import diagram_signature
from colored_link_rank import check
from component_guided_bands import parts

def run(a):
    out=Path(a.output);assert not out.exists();random.seed(a.seed)
    D=json.loads(Path('data/knots/AbeTagami_D_0_1.json').read_text());K=snappy.Link(D.get('pd_code_snappy_0indexed') or D['pd_code']);J=snappy.Link(a.partner)
    # connected_sum keeps the first factor's crossings first. Verify labels
    # before using this only as a sampling preference.
    S=K.connected_sum(J);nK=len(K.crossings);assert len(S.crossings)==nK+len(J.crossings);normalize_crossing_labels(S)
    assert [c.label for c in S.crossings]==list(range(len(S.crossings)))
    prior=json.loads(Path(a.partner_certificate).read_text());assert prior['partner']==a.partner
    assert verify_ribbon_to_unknot(snappy.Link(prior['partner_pd']),prior['partner_certificate'])
    rec={'status':'BOUNDED_MIXED_ATTACHMENT_FRONTIER','parameters':vars(a),'start_pd':S.PD_code(),'K_crossing_count':nK,'partner_ribbon_verified':True,
         'counts':Counter(),'frontier':[],'hits':[],'complete':False,'certified_slice':False,
         'scope':'First-band endpoints lie on different connected-sum factors. Incomplete priority family. Rank-deficient evaluations remain unknown. All retained paths saved.'}
    def save():out.write_text(json.dumps(rec,separators=(',',':'))+'\n')
    seen=set();work=[(S,[S.PD_code()],0)];known={};det_cache={}
    if a.resume_component_live:
        p=Path('results/teichner_component_slice_gate.json');raw=p.read_bytes();R=json.loads(raw)
        rec['resume_component_sha256']=hashlib.sha256(raw).hexdigest()
        group=R['rows'][a.partner.replace('_','')]
        work=[(snappy.Link(r['endpoint_pd']),r['certificate_prefix'],r['depth']) for r in group if not r['direct_or_inherited_obstruction']]
        rec['scope']='One further fission on paths surviving component slice tests; determinant-square gate applied before retaining new links. Possible trivial returns are not assumed new knots.'
    if a.resume_depth2:
        p=Path('results/teichner_live_frontier.json');raw=p.read_bytes();R=json.loads(raw)['partners'][a.partner.replace('_','')]
        assert R['start_pd']==json.loads(json.dumps(S.PD_code()))
        rec['resume_sha256']=hashlib.sha256(raw).hexdigest()
        raw=Path('results/teichner_factor_gate.json').read_bytes();known=json.loads(raw)['factors'];rec['factor_gate_sha256']=hashlib.sha256(raw).hexdigest()
        candidates=[r for r in R['live_frontier'] if r['depth']==2]
        random.shuffle(candidates);candidates.sort(key=lambda r:r['crossings'])
        work=[(snappy.Link(r['endpoint_pd']),r['certificate_prefix'],2) for r in candidates]
        rec['scope']='One further fission on retained depth-two prefixes, ordered by crossing count after seeded shuffle. Cached Miyazaki factor gate applied. Incomplete; no slice conclusion from survival.'
    save();start=time.monotonic();cursor=0
    while cursor<len(work):
        L0,past,depth=work[cursor];cursor+=1
        if time.monotonic()-start>=a.seconds:break
        for B in min_len_bands(L0,max_twists=2,max_band_len=a.length):
            if time.monotonic()-start>=a.seconds:break
            if depth==0:
                ends=[B.cs_along_top[0][0],B.cs_along_top[-1][0]]
                if (ends[0]<nK)==(ends[1]<nK):rec['counts']['nonmixed_skipped']+=1;continue
            rec['counts']['bands']+=1;L=add_one_band(L0,B);raw=L.PD_code();assert L.is_planar()
            if not linking_nums_all_zero(L):rec['counts']['linking_rejected']+=1;continue
            m=len(L.link_components);ranks=[check(L,[2]*m,101),check(L,[3]*m,103)]
            if any(r['specialized_H1_dimension']<m-1 for r in ranks):rec['counts']['rank_rejected']+=1;continue
            L.simplify('global');normalize_crossing_labels(L);L.unlinked_unknot_components=0
            if a.resume_component_live:
                bad_det=False
                for Q in parts(L):
                    if not Q.crossings:continue
                    key=diagram_signature(Q.PD_code())
                    if key not in det_cache:
                        V=sympy.Matrix(Q.seifert_matrix());det_cache[key]=abs(int((V+V.T).det(method='domain-ge')))
                    d=det_cache[key]
                    if isqrt(d)**2!=d:bad_det=True;break
                if bad_det:rec['counts']['component_determinant_rejected']+=1;continue
            forbidden=False
            if known:
                for component in parts(L):
                    if not component.crossings:continue
                    factors=component.deconnect_sum()
                    if len(factors)!=2:continue
                    keys=[]
                    for Q in factors:
                        Q.simplify('basic');keys.append(diagram_signature(Q.PD_code()) if Q.crossings else 'U')
                    f=[known.get(k,{}) for k in keys]
                    if all(x.get('eligible') for x in f) and f[0]['Jones']!=sorted([[-e,n] for e,n in f[1]['Jones']]):forbidden=True;break
            if forbidden:rec['counts']['nonribbon_component_rejected']+=1;continue
            endpoint=None;E=None
            if not L.link_components:endpoint='unknot'
            else:
                E=L.exterior()
                if is_unlink_exterior(E):endpoint='unknot'
                elif E.solution_type(enum=True) in {1,2}:
                    cache=snappy.RibbonLinks.identify(E,extends_to_link=True)
                    if cache:endpoint=cache.name()
            spec=B.compressed_spec()
            if endpoint:
                cert=past+[spec,endpoint];verified=bool(verify_ribbon_to_unknot(S,cert));rec['hits'].append({'certificate':cert,'verified':verified,'raw_pd':raw})
                rec['certified_slice']=verified and rec['partner_ribbon_verified'];save()
                if verified:rec['complete']=True;rec['status']='CERTIFICATE_FOUND';save();return
            sig=diagram_signature(L.PD_code())
            if sig in seen:rec['counts']['duplicate_diagram']+=1;continue
            seen.add(sig);path=past+[spec,L.PD_code()]
            row={'depth':depth+1,'band':spec,'start_pd':L0.PD_code(),'raw_pd':raw,'endpoint_pd':L.PD_code(),'certificate_prefix':path,'rank_checks':ranks,'signature':sig,'crossings':len(L.crossings)}
            rec['frontier'].append(row);rec['counts']['retained']+=1;save()
            if depth==0:work.append((L,path,1))
        rec['counts']['parents_started']=cursor
    rec.update(complete=True,elapsed_seconds=round(time.monotonic()-start,3),stop='time_cap' if time.monotonic()-start>=a.seconds else 'enumeration_finished',queued_parents=len(work),parents_started=cursor)
    save();print(json.dumps({'counts':rec['counts'],'frontier':len(rec['frontier']),'stop':rec['stop'],'certified_slice':rec['certified_slice']}),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('partner');p.add_argument('partner_certificate');p.add_argument('output');p.add_argument('--seconds',type=int,default=150);p.add_argument('--length',type=int,default=6);p.add_argument('--seed',type=int,default=20260920);p.add_argument('--resume-depth2',action='store_true');p.add_argument('--resume-component-live',action='store_true');run(p.parse_args())
