"""Identify the actual 19-crossing factor of stored D01. No invariant sweep.

Trust boundary: SnapPy PD exteriors and topology-preserving retriangulations,
as audited in research/44. Final face maps have a standard-library checker.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import snappy
from spherogram import Link

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

finite=load('finite',HERE/'check_saved.py')
maps=load('maps',ROOT/'results/night_2026_09_18_positive_identification/build_certificate.py')

def cut_factor(A,vertices):
    loose=sorted(x for x,y in A.items() if x[0] in vertices and y[0] not in vertices)
    assert len(loose)==2
    B={x:y for x,y in A.items() if x[0] in vertices and y[0] in vertices}
    B[loose[0]]=loose[1];B[loose[1]]=loose[0]
    labels={};rows=[]
    for c in sorted(vertices):
        row=[]
        for p in range(4):
            x=(c,p)
            if x not in labels:labels[x]=labels[B[x]]=len(labels)//2
            row.append(labels[x])
        rows.append(row)
    return loose,rows

def main():
    resource.setrlimit(resource.RLIMIT_CPU,(30,35))
    out=HERE/'factor_identification';out.mkdir(exist_ok=False)
    snappy.set_rand_seed(18092026)
    paths=[ROOT/'data/knots'/n for n in
           ['AbeTagami_D_0_1.json','AbeTagami_K_0_K_-1__6_3.json','AbeTagami_K_1.json']]
    cards=[json.loads(p.read_text()) for p in paths]
    A=finite.adjacency(cards[0]['pd_code'])
    seams=[(x,y) for x,y in A.items() if x[0]<6<=y[0]]
    pieces=[cut_factor(A,set(range(lo,hi))) for lo,hi in [(0,6),(6,25)]]
    assert finite.adjacency(pieces[0][1])==finite.adjacency(cards[1]['pd_code'])
    # The two cut edges must share both incident faces, giving a dual bigon.
    unseen=set(A);face_of={};faces=[]
    while unseen:
        start=min(unseen);x=start;cycle=[]
        while True:
            assert x in unseen;unseen.remove(x);cycle.append(x);face_of[x]=len(faces)
            x=A[x[0],(x[1]+1)%4]
            if x==start:break
        faces.append(cycle)
    incident=[sorted([face_of[(x[0],(x[1]-1)%4)],face_of[x]]) for x,y in seams]
    assert incident[0]==incident[1] and len(set(incident[0]))==2
    K=Link(pieces[1][1]);M=Link(cards[2]['pd_code']).mirror()
    assert K.is_planar() and len(K.link_components)==1
    stages=[]
    def save(T,name):
        filename=name+'.tri';T.save(str(out/filename))
        stages.append({'file':filename,'sha256':hashlib.sha256((out/filename).read_bytes()).hexdigest()})
    X,Y=K.exterior(),M.exterior()
    save(X,'factor_pd_exterior');save(Y,'mirror_K1_pd_exterior')
    X.canonize();Y.canonize()
    save(X,'factor_retriangulated');save(Y,'mirror_K1_retriangulated')
    ga,gb=X._get_tetrahedra_gluing_data(),Y._get_tetrahedra_gluing_data()
    mapping=maps.find_map(ga,gb)
    peripheral=[]
    for iso in X.isomorphisms_to(Y):
        mat=iso.cusp_maps()[0]
        peripheral.append([[int(mat[i,j]) for j in range(2)] for i in range(2)])
    assert any(m[1][0]==0 and abs(m[0][0])==1 for m in peripheral)
    c={'source_gluings':ga,'target_gluings':gb,'orientation_preserving_simplex_map':mapping,
       'source_cusps':X._get_cusp_indices_and_peripheral_curve_data()[0],
       'target_cusps':Y._get_cusp_indices_and_peripheral_curve_data()[0]}
    report={'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths],
            'snappy_version':snappy.__version__,'seed':18092026,'cut_edges':seams,
            'cut_incident_faces':incident,'faces':faces,
            'factors':[{'cut_ports':loose,'pd_code':pd} for loose,pd in pieces],
            'K0_factor':'identical port adjacency to stored K0',
            'K1_factor':'orientation-preserving complement identification with mirror of stored K1; knot orientation not independently tracked',
            'stages':stages,'case':c,'kernel_peripheral_maps':peripheral,
            'scope':'Enough for unoriented prime summand types and the nonribbon pairing obstruction; not an oriented concordance construction',
            'failed_prechecks':['Whole connected-sum PDs did not have a diagram isomorphism at the chosen cuts',
                                'The 19-crossing factors did not have a direct plane diagram isomorphism; this is not a knot distinction']}
    (out/'certificate.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'K0_exact_adjacency':True,'factor_tetrahedra':len(ga),'mirror_K1_positive_map':True,'peripheral_maps':peripheral}))

if __name__=='__main__':main()
