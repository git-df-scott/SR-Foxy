"""One marked surface rerouting, not a knot search or a transfer certificate.

Run with Python's standard library. Existing outputs are never overwritten.
The old source presentation and its proved rewrite rules are input lemmas.
"""
import hashlib
import importlib.util
import json
import sys
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('transport', ROOT / 'results/astra_2026_09_18_marked_annulus_construction/build_transport.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
g = old.g
sys.path.insert(0, str(old.ARCHIVE))
import verify_product_collar as proof


def main():
    output = HERE / 'GEOMETRY.json'
    if output.exists():
        raise FileExistsError(output)
    paths = [old.ARCHIVE / 'RESULTS.json', old.ARCHIVE / 'diagram_core.py',
             old.ARCHIVE / 'verify_product_collar.py',
             ROOT / 'results/astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json',
             ROOT / 'results/astra_2026_09_18_marked_annulus_construction/transport.json',
             ROOT / 'results/astra_one_commutator_2026_09_18/BUNDLE.tar.xz']
    saved = json.loads(paths[0].read_text())
    C = json.loads(paths[3].read_text())
    transport = json.loads(paths[4].read_text())
    with tarfile.open(paths[5]) as archive:
        recipe = json.load(archive.extractfile('astra_one_commutator_2026_09_18/ONE_HANDLE_RECIPE.json'))
    images = {int(k)+1: v for k,v in saved['boundary_arc_images'].items()}
    regions = {int(k): v for k,v in saved['region_words'].items()}
    rules = [tuple(r) for r in saved['proof_rule_relators']]
    adj = g.adjacency_from_pd(g.SCAFFOLD)
    q = g.quotient_R_wirtinger(adj)
    upper = {c: list(adj[c]) for c in range(27)}
    g.connect(upper, (0,2), (1,1))
    # Reproduce the archived REGION NUMBERING, not another face enumeration.
    parent = {(c,p):(c,p) for c in upper for p in range(4)}
    def root(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def join(a,b):
        parent[root(a)] = root(b)
    for c in upper:
        for p,(d,r) in enumerate(upper[c]):
            join((c,p),(d,(r-1)%4)); join((c,(p-1)%4),(d,r))
    roots = sorted({root(x) for x in parent})
    index = {x:i for i,x in enumerate(roots)}
    face = {x:index[root(x)] for x in parent}
    assert face[0,2] == saved['base_region'] == 0
    assert len(roots) == 29
    mirror = {tuple(r['lower']):tuple(r['upper']) for r in transport['mirror_port_map']}
    endpoints = []
    for lower, upper_end in [((41,0),(13,2)), ((52,0),(19,2))]:
        source = mirror[lower]
        assert upper[source[0]][source[1]] == upper_end
        endpoints.append({'lower':lower, 'source_port':source, 'other_end_of_same_edge':upper_end})

    def native_path(start, stop=None):
        cur = start; events=[]; letters=[]
        while True:
            c,p=cur; term=[]
            if p%2 == 0 and q['cmap'][c,1] == 0:
                term=[(q['arcs'][c,1]+1)*q['signs'][c]]
            events.append({'incoming_port':cur, 'R_letters':term})
            letters += term
            cur=adj[c][(p+2)%4]
            if cur == (stop if stop is not None else start): break
            assert len(events)<100
        return {'start':start, 'stop':cur, 'events':events, 'R_word':letters}

    partial = native_path((19,2),(15,2))
    full_c1 = native_path((13,2))
    full_c2 = native_path((19,2))
    root_corridor = native_path((7,1),(19,2))
    assert partial['R_word'] == [4,-1]
    assert full_c1['R_word'] == [1,-9,4,-1,3,-4]
    assert full_c2['R_word'] == [4,-1,3,-4]
    assert root_corridor['R_word'] == []
    final = adj
    bands = [dict(g.BAND1,arc_is_under=[False,True]), dict(g.BAND2,arc_is_under=[True,False])]
    for b in bands:
        final = g.add_zero_twist_band(final,b)
    qf = g.quotient_R_wirtinger(final)
    fmap = g.map_final_R_arcs_to_scaffold(q,qf)
    band_events=[]
    for name,ports in [('B1',[(54,0),(55,3)]),('B2',[(58,3),(59,0)])]:
        events=[]; word=[]
        for c,p in ports:
            direction=1 if (c,p) in qf['incoming'] else -1
            sign=direction*qf['signs'][c]
            over=qf['cmap'][c,1]
            term=[]
            if p%2==0 and over==0:
                term=[sign*(fmap[qf['arcs'][c,1]]+1)]
            events.append({'incoming_port_along_core':(c,p), 'core_is_under':p%2==0,
                           'over_component':over, 'oriented_crossing_sign':sign,
                           'R_letters':term,
                           'retained_over_meridian':(c,1) if p%2==0 else None})
            word+=term
        band_events.append({'band':name,'events':events,'R_word':word})
    assert [x['R_word'] for x in band_events] == [[],[11]]
    # B1 passes UNDER a, not R. This event must NOT be erased in a protected-sheet movie.
    assert band_events[0]['events'][0]['over_component']==1
    assert band_events[0]['events'][0]['oriented_crossing_sign']==-1

    verticals=[]
    for p in [(13,2),(19,2)]:
        f,h=face[p],face[p[0],(p[1]-1)%4]
        assert proof.reduce_proven(old.red(regions[f]+old.inv(regions[h])),rules)[0]==()
        verticals.append({'upper_edge_port':p, 'adjacent_source_regions':[f,h],
                          'upper_to_lower':regions[f], 'lower_to_upper':old.inv(regions[f])})
    def loop(k):
        assert k in [0,1]
        factors=[old.sub(partial['R_word'],images),
                 old.sub(band_events[0]['R_word'],images),
                 verticals[0]['lower_to_upper'],
                 old.sub(full_c1['R_word'],images) if k else [],
                 old.sub(band_events[1]['R_word'],images),
                 verticals[1]['lower_to_upper']]
        return {'rho1_winding':k, 'ordered_source_factors':factors,
                'source_word':old.red(y for x in factors for y in x)}
    loops={'v': {'boundary_word':full_c2['R_word'], 'source_word':old.sub(full_c2['R_word'],images)},
           'z0':loop(0),'z1':loop(1)}
    for name in ['A','B']:
        w=recipe['handles'][name]['target_word']
        loops[name]={'boundary_word':w,'source_word':old.sub(w,images)}
    prime=17
    matrices={int(k):[sum(entry)%prime for entry in mat] for k,mat in C['source_matrices'].items()}
    def mm(a,b):
        return [(a[0]*b[0]+a[1]*b[2])%prime,(a[0]*b[1]+a[1]*b[3])%prime,
                (a[2]*b[0]+a[3]*b[2])%prime,(a[2]*b[1]+a[3]*b[3])%prime]
    def evaluate(w):
        m=[1,0,0,1]
        for x in w:
            n=matrices[abs(x)]
            if x<0:n=[n[3],-n[1]%prime,-n[2]%prime,n[0]]
            m=mm(m,n)
        return m
    assert all(evaluate(r)==[1,0,0,1] for r in C['source_relators'])
    for d in loops.values():
        d['matrix_mod17']=evaluate(d['source_word'])
        d['trace_mod17']=(d['matrix_mod17'][0]+d['matrix_mod17'][3])%prime
    assert loops['z0']['trace_mod17']==1
    assert loops['B']['trace_mod17']==loops['z1']['trace_mod17']==2
    replays=[]
    for name,initial in [('v A',old.red(loops['v']['source_word']+loops['A']['source_word'])),
                         ('z1 B^-1',old.red(loops['z1']['source_word']+old.inv(loops['B']['source_word'])))]:
        end,steps=proof.reduce_proven(initial,rules)
        assert end==()
        replays.append({'claim':name+'=1 in pi1(W)', 'initial':initial, 'steps':steps,'end':end})
    comm=lambda x,y:old.red(x+y+old.inv(x)+old.inv(y))
    commtraces={name:sum(evaluate(comm(loops['v']['source_word'],loops[name]['source_word']))[i] for i in [0,3])%prime for name in ['z0','z1']}
    assert commtraces=={'z0':1,'z1':11}
    report={'source_head':'3e4461e23fce6687293f6abef963011b37677c55',
            'scope':'Actual original-surface paths and one annular rerouting; relative connector prescription. NO complete correction-surface embedding, transfer pair, or caps.',
            'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths],
            'attachment_edge_matches':endpoints,'bands':bands,'band_core_events':band_events,
            'rho2_upper_path':partial,'positive_c1_winding':full_c1,'native_c2':full_c2,
            'b_root_corridor':root_corridor,'vertical_markings':verticals,'loops':loops,
            'source_matrices_mod17':matrices,'source_relators':C['source_relators'],
            'rewrite_rules_input':str(paths[0].relative_to(ROOT)), 'replays':replays,
            'punctured_torus_boundary_trace_mod17':commtraces,
            'surface_orientation':{'F_v_dot_z':1,'S_A_dot_B':-1,'minus_S_A_dot_B':1,
                                   'matched_correction_basis':['-A','B'],'matched_intersection':-1},
            'connector_intervals':{'F':['v-','z-','v+','z+'], 'correction_induced_P_order':['d+','c+','d-','c-'],
                                   'tracks_F_to_C':[['v-','c-'],['z-','d-'],['v+','c+'],['z+','d+']],
                                   'c':'-A','d':'B','corridor':'F vertex via short rho2 vertical to upper edge19, backwards native arc to b anchor (7,1), fixed b collar, correction root channel',
                                   'W_word':[],'protected_complement_word':None},
            'compression_topology':{'initial_chi':-4,'initial_boundary_count':2,'cut_complement_genus':0,'cut_complement_boundary_count':6,'after_two_abstract_compressions_genus':0,'after_two_abstract_compressions_boundary_count':2},
            'realization_still_missing':{'correction_disk_push_routes':True,'complete_transfer_movies':True,'global_intersection_ledger':True,'Whitney_disks':True,'compression_caps':True,'actual_surgery_boundary':True},
            'CE':False}
    output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'z0_trace':loops['z0']['trace_mod17'],'z1_equals_B_exact':True,
                      'positive_annulus_windings_added':1,'proof_steps':[len(r['steps']) for r in replays],
                      'complete_transfers':False,'CE':False}))

if __name__=='__main__':
    main()
