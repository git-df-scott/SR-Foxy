"""Finite port, face, ribbon-route, and word transport for an explicit collar.

The geometric map is specified in GEOMETRY.md. These checks validate its
marked diagram inputs and consequences, not a 4D annulus embedding.
Standard library; no census, word search, or new invariant calculation.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
ARCHIVE = ROOT/'results/chat_archive_2026_09_17/expanded/SR_Foxy_pass09_product_collar_2026_09_17/pass09_product_collar'

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

g = module('diagram_core', ARCHIVE/'diagram_core.py')

def red(w):
    out = []
    for x in w:
        if out and out[-1] == -x: out.pop()
        else: out.append(x)
    return out

def inv(w): return [-x for x in reversed(w)]
def sub(w, images): return red(v for x in w for v in (images[x] if x > 0 else inv(images[-x])))

def faces(adj):
    unused = {(c,p) for c in adj for p in range(4)}
    cycles, labels = [], {}
    while unused:
        start = min(unused); x = start; cycle = []
        while x not in cycle:
            assert x in unused
            unused.remove(x); labels[x] = len(cycles); cycle.append(x)
            c,p = x
            x = adj[c][(p+1)%4]
        assert x == start
        cycles.append(cycle)
    return cycles, labels

def main():
    paths = [ROOT/'data/knots/AbeTagami_marked_product_scaffold.json',
             ARCHIVE/'RESULTS.json', ARCHIVE/'diagram_core.py',
             ROOT/'results/astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json',
             ROOT/'results/night_2026_09_18/word_correction.json',
             ROOT/'results/night_2026_09_18_surface/surface_certificate.json']
    source = json.loads(paths[0].read_text())
    saved = json.loads(paths[1].read_text())
    C = json.loads(paths[3].read_text())
    repair = json.loads(paths[4].read_text())
    surface = json.loads(paths[5].read_text())
    assert source['pd_code'] == g.SCAFFOLD
    A = g.adjacency_from_pd(g.SCAFFOLD)
    U = {c:list(A[c]) for c in range(27)}
    L = {c-27:[(d-27,p) for d,p in A[c]] for c in range(27,54)}
    seams = [[c,p,list(A[c][p])] for c in range(27) for p in range(4) if A[c][p][0] >= 27]
    assert seams == [[0,2,[27,3]],[1,1,[28,2]]]
    g.connect(U,(0,2),(1,1)); g.connect(L,(0,3),(1,2))
    shift = {int(c):s for c,s in saved['mirror_port_rotations'].items()}
    port_map = []
    for c in U:
        for p,(d,q) in enumerate(U[c]):
            assert L[c][(p+shift[c])%4] == (d,(q+shift[d])%4)
            port_map.append({'upper':[c,p], 'lower':[c+27,(p+shift[c])%4]})
    fU,idU = faces(U); fA,idA = faces(A)
    # Face numbering here is lexicographic-cycle numbering, not archived DSU IDs.
    neck0, neck6 = idA[0,2], idA[0,1]
    assert neck0 != neck6
    neck = []
    for sector,face_id in [((0,2),neck0),((0,1),neck6)]:
        lower = [(c-27,(p-shift[c-27])%4) for c,p in fA[face_id] if c >= 27]
        lower_ids = {idU[x] for x in lower}
        assert len(lower_ids) == 1
        assert next(iter(lower_ids)) == idU[0,1 if sector==(0,2) else 2]
        neck.append({'upper_saved_sector':sector, 'double_face':fA[face_id],
                     'lower_pullback_source_sectors':lower,
                     'side_exchange_checked':True})

    bands = [dict(g.BAND1,arc_is_under=[False,True]),
             dict(g.BAND2,arc_is_under=[True,False])]
    routes = []
    for bi,band in enumerate(bands):
        segments = []
        for x,y in zip(band['along_top'],band['along_top'][1:]):
            incident = lambda v: {idA[v],idA[v[0],(v[1]-1)%4]}
            common = incident(x)&incident(y)
            assert len(common) == 1
            f = next(iter(common))
            crosses_neck = (x[0] < 27) != (y[0] < 27)
            if crosses_neck: assert f == (neck0 if bi == 0 else neck6)
            segments.append({'from':x,'to':y,'face_cycle':fA[f],
                             'crosses_neck':crosses_neck,
                             'target_neck_side':('plus_y' if bi==0 else 'minus_y') if crosses_neck else None})
        routes.append({'band':band,'segments':segments,
                       'ribbon_transport':'Both core and material normal field pull back by D(Phi^-1); no reset to a straight product ribbon.'})
    F = g.add_zero_twist_band(g.add_zero_twist_band(A,bands[0]),bands[1])
    qb,qf = g.quotient_R_wirtinger(A),g.quotient_R_wirtinger(F)
    fmap = g.map_final_R_arcs_to_scaffold(qb,qf)
    images = {int(i)+1:w for i,w in saved['boundary_arc_images'].items()}
    assert images == {int(i)+1:w for i,w in C['boundary_arc_images'].items()}
    axes = []
    for ci in [1,2]:
        cur = min(qf['components'][ci]); seen = set(); steps = []; word = []
        while cur not in seen:
            seen.add(cur); c,p = cur; letter = []
            if p in (0,2) and qf['cmap'][c,1] == qf['cmap'][c,3] == 0:
                letter = [(fmap[qf['arcs'][c,1]]+1)*qf['signs'][c]]
                word += letter
            steps.append({'port':cur,'boundary_letters':letter,'source_word':sub(letter,images)})
            cur = F[c][(p+2)%4]
        assert cur == min(qf['components'][ci])
        axes.append({'component':ci,'steps':steps,'boundary_word':red(word),
                     'source_image':sub(word,images),
                     'self_crossings':[c for c in F if all(qf['cmap'][c,p]==ci for p in range(4))]})
    assert [a['boundary_word'] for a in axes] == [repair['original_axis1'],repair['original_axis2']]
    mu = images[repair['seam_meridian_boundary_generator']]
    corrected = sub(repair['corrected_axis2'],images)
    assert corrected == red(inv(mu)+axes[0]['source_image']+mu)

    # One exact finite quotient measures the two proposed compression loops.
    # R(1)=17, so z=1 specializes the archived representation to F_17.
    assert sum(C['riley_polynomial_ascending']) == 17
    prime = 17
    matrices = {int(k):[sum(entry)%prime for entry in M] for k,M in C['source_matrices'].items()}
    I = [1,0,0,1]
    def mm(a,b):
        return [(a[0]*b[0]+a[1]*b[2])%prime,(a[0]*b[1]+a[1]*b[3])%prime,
                (a[2]*b[0]+a[3]*b[2])%prime,(a[2]*b[1]+a[3]*b[3])%prime]
    def value(w):
        ans = I
        for x in w:
            a = matrices[abs(x)]
            if x<0: a = [a[3],-a[1]%prime,-a[2]%prime,a[0]]
            ans = mm(ans,a)
        return ans
    assert all((a[0]*a[3]-a[1]*a[2])%prime == 1 for a in matrices.values())
    assert all(value(r)==I for r in C['source_relators'])
    obstruction = []
    for key in ['left_boundary_word','right_boundary_word']:
        w = surface['commutators'][9][key]; qw = sub(w,images); mat = value(qw)
        assert mat != I and (mat[0]+mat[3])%prime == 3
        obstruction.append({'handle':key,'boundary_word':w,'source_word':qw,
                            'matrix_mod17':mat,'trace_mod17':3,
                            'conclusion':'This particular loop cannot bound even a disk map in W.'})
    output = {'scope':'Marked transport for the explicitly completed zero-turn product model in GEOMETRY.md; no immersed-annulus movie or embedded modifying annulus',
              'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths],
              'seams':seams,'mirror_port_map':port_map,'source_faces':fU,'neck_faces':neck,
              'collar':{'source_region0':'y>0','forward_rotation':'R_theta(y,z)=(y cos(theta)-z sin(theta), y sin(theta)+z cos(theta))',
                        'theta':'pi*chi(s), chi constant near 0 and 1',
                        'above_whisker_pullback':'(r sin(theta),r cos(theta))',
                        'gluing_identity':'S_y R_pi = S_z',
                        'opposite_rotation_control':'Same endpoint maps; above pullback uses region6 and gives q1.'},
              'band_routes':routes,'boundary_meridian_images':images,'axes':axes,
              'word_repair':{'corrected_boundary_word':repair['corrected_axis2'],'source_image':corrected,
                             'conjugating_meridian':mu,'geometric_representative':'Research42 existence surface only; no new marked PD asserted'},
              'compression_test':{'field':17,'z':1,'all_source_relators_pass':True,'factor_index_one_based':10,'loops':obstruction}}
    path=HERE/'transport.json'
    if path.exists(): raise FileExistsError(path)
    path.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'port_pairs':len(port_map),'neck_faces':len(neck),'axis_routes':len(axes),
                      'geometric_model_map':'q0 for specified collar','compression_loops_nontrivial':len(obstruction)}))

if __name__=='__main__': main()
