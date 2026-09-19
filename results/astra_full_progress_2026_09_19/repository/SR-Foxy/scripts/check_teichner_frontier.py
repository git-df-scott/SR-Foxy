#!/usr/bin/env python3
"""Check saved Teichner moves, factor witnesses, and inherited dead prefixes."""
from collections import Counter
import hashlib,json
from pathlib import Path
import snappy,sympy
from spherogram.links.bands.core import add_one_band
from spherogram.links.bands.search import verify_ribbon_to_unknot
from component_guided_bands import parts,jones
from fusion_successors import diagram_signature
from colored_link_rank import check

G=json.loads(Path('results/teichner_factor_gate.json').read_text());assert G['complete'];counts=Counter();resume={};summary={}
for j in ['941','946']:
    p=Path('results/teichner_D01_J'+j+'_mixed.json');raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==G['input_hashes'][str(p)]
    D=json.loads(raw);P=json.loads(Path('results/teichner_D01_J'+j+'_probe.json').read_text())
    assert verify_ribbon_to_unknot(snappy.Link(P['partner_pd']),P['partner_certificate']);counts['partner_certificates']+=1
    rows=D['frontier'];blocked=[]
    for r in G['rows'][j]:
        if r['ribbon_completion_obstructed']:blocked.append(rows[r['index']]['certificate_prefix'])
    live=[];dead=0
    for i,r in enumerate(rows):
        L0=snappy.Link(r['start_pd']);L=add_one_band(L0,r['band']);assert L.PD_code()==[tuple(c) for c in r['raw_pd']];assert L.is_planar();counts['raw_band_replays']+=1
        assert r['certificate_prefix'][0]==D['start_pd'] and r['certificate_prefix'][-1]==r['endpoint_pd']
        if r['depth']==2:assert r['certificate_prefix'][-3]==r['start_pd']
        for x in r['rank_checks']:
            got=check(L,x['component_values'],x['prime']);assert got==x
        # Reconstruct the displayed factor decomposition for each claimed exclusion.
        gate=G['rows'][j][i];assert gate['index']==i
        if gate['ribbon_completion_obstructed']:
            ps=parts(snappy.Link(r['endpoint_pd']))
            for pair in gate['pairs']:
                if not pair['applies']:continue
                actual=ps[pair['component']].deconnect_sum();keys=[]
                for Q in actual:
                    Q.simplify('basic');keys.append(diagram_signature(Q.PD_code()) if Q.crossings else 'U')
                assert sorted(keys)==sorted(pair['factors']);a,b=[G['factors'][k] for k in keys]
                assert a['HFK']['fibered'] and b['HFK']['fibered'] and a['irreducible'] and b['irreducible']
                assert a['Jones']!=sorted([[-e,n] for e,n in b['Jones']]);counts['factor_obstruction_witnesses']+=1
        path=r['certificate_prefix'];inherited=any(path[:len(prefix)]==prefix for prefix in blocked)
        if inherited:dead+=1
        else:live.append(dict(r,original_index=i))
    resume[j]={'partner':D['parameters']['partner'],'start_pd':D['start_pd'],'live_frontier':live,'input_sha256':hashlib.sha256(raw).hexdigest()}
    summary[j]={'saved':len(rows),'direct_or_inherited_obstructed':dead,'live':len(live),'live_first_stage':sum(r['depth']==1 for r in live)}
# Falsification controls for the Jones non-isotopy step.
K=snappy.Link('6_3');assert jones(K)=={-e:n for e,n in jones(K.mirror()).items()}
D01=snappy.Link(json.loads(Path('data/knots/AbeTagami_D_0_1.json').read_text())['pd_code_snappy_0indexed']);A,B=D01.deconnect_sum();assert jones(A)!={-e:n for e,n in jones(B).items()}
counts['Jones_pairing_controls']=2
Path('results/teichner_live_frontier.json').write_text(json.dumps({'complete':True,'summary':summary,'partners':resume,'meaning':'Retained means no applied obstruction, not a ribbon or slice certificate.'},separators=(',',':'))+'\n')
Path('results/teichner_frontier_validation.json').write_text(json.dumps({'status':'PASSED','counts':dict(counts),'summary':summary,'limitations':'Same-library band/decomposition and partner-certificate replay. No independent formal checker for ribbon cache or HFK. The nonribbon gate is a theorem applied to computed hypotheses.'},indent=2)+'\n');print(json.dumps(summary),flush=True)
