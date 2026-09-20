"""Independent saved-certificate replay; standard library, no search.

This checks finite paths and algebra, not the missing smooth transfer movies.
The previously certified source rewrite rules remain explicit input lemmas.
"""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def inverse(w): return [-a for a in reversed(w)]

def cancel(w):
    w=list(w)
    i=0
    while i+1<len(w):
        if w[i]==-w[i+1]:
            del w[i:i+2]
            i=max(0,i-1)
        else: i+=1
    return w

def substitute(w,images):
    out=[]
    for x in w: out.extend(images[str(abs(x))] if x>0 else inverse(images[str(abs(x))]))
    return cancel(out)

def replay(initial,steps,rules):
    w=cancel(initial)
    for pos,(idx,sign,shift,cut) in steps:
        assert sign in [-1,1]
        r=rules[idx] if sign==1 else inverse(rules[idx])
        r=r[shift:]+r[:shift]
        assert w[pos:pos+cut]==r[:cut]
        w=cancel(w[:pos]+inverse(r[cut:])+w[pos+cut:])
    return w

def mm(a,b):
    return [sum(a[2*i+k]*b[2*k+j] for k in range(2))%17 for i in range(2) for j in range(2)]

def mi(a): return [a[3],-a[1]%17,-a[2]%17,a[0]]

def main():
    d=json.loads((HERE/'GEOMETRY.json').read_text())
    for row in d['inputs']:
        assert hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256']
    old=json.loads((ROOT/d['rewrite_rules_input']).read_text())
    rules=old['proof_rule_relators']
    source_matrices=d['source_matrices_mod17']
    def evaluate(w):
        out=[1,0,0,1]
        for x in w:
            a=source_matrices[str(abs(x))]
            out=mm(out,a if x>0 else mi(a))
        return out
    def trace(a): return (a[0]+a[3])%17
    assert all((a[0]*a[3]-a[1]*a[2])%17==1 for a in source_matrices.values())
    assert all(evaluate(r)==[1,0,0,1] for r in d['source_relators'])
    images={str(int(k)+1):v for k,v in old['boundary_arc_images'].items()}
    for name,row in d['loops'].items():
        if 'boundary_word' in row: assert substitute(row['boundary_word'],images)==row['source_word']
        if 'ordered_source_factors' in row:
            assert cancel([a for f in row['ordered_source_factors'] for a in f])==row['source_word']
        assert evaluate(row['source_word'])==row['matrix_mod17']
        assert trace(row['matrix_mod17'])==row['trace_mod17']
    # Check each new equality from its exact words, not its saved Boolean.
    expected=[cancel(d['loops']['v']['source_word']+d['loops']['A']['source_word']),
              cancel(d['loops']['z1']['source_word']+inverse(d['loops']['B']['source_word']))]
    for r,w in zip(d['replays'],expected):
        assert r['initial']==w
        assert replay(w,r['steps'],rules)==r['end']==[]
    # Recover native directed paths independently from the original PD.
    pd=json.loads((ROOT/'data/knots/AbeTagami_marked_product_scaffold.json').read_text())['pd_code']
    occurrences={}
    for c,row in enumerate(pd):
        for p,e in enumerate(row): occurrences.setdefault(e,[]).append((c,p))
    assert all(len(x)==2 for x in occurrences.values())
    adj={}
    for a,b in occurrences.values(): adj[a]=b;adj[b]=a
    for key in ['rho2_upper_path','positive_c1_winding','native_c2','b_root_corridor']:
        row=d[key];x=tuple(row['start']);word=[]
        for step in row['events']:
            assert x==tuple(step['incoming_port'])
            word+=step['R_letters']
            x=adj[x[0],(x[1]+2)%4]
        assert x==tuple(row['stop']) and word==row['R_word']
    transport=json.loads((ROOT/'results/astra_2026_09_18_marked_annulus_construction/transport.json').read_text())
    mirror={tuple(r['lower']):tuple(r['upper']) for r in transport['mirror_port_map']}
    for r in d['attachment_edge_matches']:
        assert mirror[tuple(r['lower'])]==tuple(r['source_port'])
        assert adj[tuple(r['source_port'])]==tuple(r['other_end_of_same_edge'])
    # The ONLY geometric modification was one winding in annulus 1.
    z0=d['loops']['z0']['ordered_source_factors']
    z1=d['loops']['z1']['ordered_source_factors']
    assert z0[:3]==z1[:3] and z0[4:]==z1[4:]
    assert z0[3]==[] and z1[3]==substitute(d['positive_c1_winding']['R_word'],images)
    assert [v['adjacent_source_regions'] for v in d['vertical_markings']]==[[6,7],[26,27]]
    for row in d['vertical_markings']:
        assert row['upper_to_lower']==old['region_words'][str(row['adjacent_source_regions'][0])]
        assert row['lower_to_upper']==inverse(row['upper_to_lower'])
    # A coherent strip has reversed endpoint order at its two ends.
    intervals=d['connector_intervals']
    tracks=intervals['tracks_F_to_C']
    assert [t[0] for t in tracks]==intervals['F']
    assert [t[1] for t in tracks]==list(reversed(intervals['correction_induced_P_order']))
    assert set(t[0] for t in tracks)=={'v+','v-','z+','z-'}
    assert d['surface_orientation']['F_v_dot_z']+d['surface_orientation']['matched_intersection']==0
    topo=d['compression_topology']
    assert 2-2*topo['cut_complement_genus']-topo['cut_complement_boundary_count']==-4
    assert -4+2*2==2-2*topo['after_two_abstract_compressions_genus']-topo['after_two_abstract_compressions_boundary_count']==0
    # Negative controls must fail for a meaningful reason.
    assert trace(evaluate(d['loops']['z0']['source_word']))!=trace(evaluate(d['loops']['B']['source_word']))
    wrong_sign=cancel(d['loops']['z1']['source_word']+d['loops']['B']['source_word'])
    assert evaluate(wrong_sign)!=[1,0,0,1]
    wrong_vertical=list(z1)
    wrong_vertical[2]=inverse(wrong_vertical[2])
    assert evaluate([a for f in wrong_vertical for a in f])!=evaluate(d['loops']['B']['source_word'])
    assert d['band_core_events'][0]['events'][0]['retained_over_meridian']==[54,1]
    assert d['band_core_events'][0]['events'][0]['over_component']==1
    assert intervals['protected_complement_word'] is None
    assert all(d['realization_still_missing'].values())
    report={'status':'PASS','input_hashes':len(d['inputs']),'source_relators':len(d['source_relators']),
            'exact_equalities':['v=A^-1 in W','z1=B in W'],
            'negative_controls':['unwound rho1','wrong correction orientation','reversed vertical bridge'],
            'scope':'Finite path and word certificate; no verification of the unsupplied full transfer geometry',
            'full_transfers':False,'CE':False}
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
