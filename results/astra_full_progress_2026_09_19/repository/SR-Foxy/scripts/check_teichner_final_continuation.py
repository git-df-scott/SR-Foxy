#!/usr/bin/env python3
import json
from pathlib import Path
import snappy,sympy
from spherogram.links.bands.core import add_one_band
from component_guided_bands import parts,jones
from fission_ancestry_audit import determinant,square
from colored_link_rank import check
S=json.loads(Path('results/teichner_component_slice_gate.json').read_text());paths=[r['certificate_prefix'] for r in S['rows']['946'] if not r['direct_or_inherited_obstruction']]
p=Path('results/teichner_D01_J946_component_filtered_continuation.json');D=json.loads(p.read_text());assert D['complete'] and D['stop']=='enumeration_finished' and not D['certified_slice'];n=0
for r in D['frontier']:
    assert r['certificate_prefix'][:-2] in paths
    L=add_one_band(snappy.Link(r['start_pd']),r['band']);assert L.PD_code()==[tuple(c) for c in r['raw_pd']]
    for c in r['rank_checks']:assert check(L,c['component_values'],c['prime'])==c
    for Q in parts(snappy.Link(r['endpoint_pd'])):
        assert square(determinant(jones(Q)));n+=1
J=snappy.Link('6_1');assert jones(J)!=jones(J.mirror())
card=json.loads(Path('data/knots/AbeTagami_D_0_1.json').read_text());K=snappy.Link(card['pd_code_snappy_0indexed']);assert jones(K)!=jones(K.mirror())
Path('results/teichner_final_continuation_validation.json').write_text(json.dumps({'status':'PASSED','raw_band_replays':len(D['frontier']),'component_Jones_square_determinant_checks':n,'partner_and_D01_Jones_chirality_checks':True,'scope':'96 retained paths remain unknown. Mirror partners are not removed by an amphichirality argument for D01.'},indent=2)+'\n');print('replayed',len(D['frontier']),'component checks',n,flush=True)
