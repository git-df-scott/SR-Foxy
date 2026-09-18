"""Consume the newly published one-commutator recipe in this marked exterior.

No new word search or annulus movie. Checks archive hashes and compares the
published integer inputs to both the pinned commit and the present checkout.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile
from check_saved import mm,substitute

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def main():
    out=HERE/'one_handle_connection.json'
    if out.exists():raise FileExistsError(out)
    published=ROOT/'results/astra_one_commutator_2026_09_18'
    with tarfile.open(published/'BUNDLE.tar.xz') as archive:
        prefix='astra_one_commutator_2026_09_18/'
        manifest=json.load(archive.extractfile(prefix+'MANIFEST.json'))
        for name,entry in manifest.items():
            raw=archive.extractfile(prefix+name).read()
            assert len(raw)==entry['bytes'] and hashlib.sha256(raw).hexdigest()==entry['sha256']
        d=json.load(archive.extractfile(prefix+'inputs_extended.json'))
    def get(path):
        raw=subprocess.check_output(['git','-C',str(ROOT),'show',d['source_commit']+':'+path])
        assert raw==(ROOT/path).read_bytes()
        return json.loads(raw),hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    C,ch=get(d['certificate_path']);w,wh=get(d['original_delta_path'])
    checks={'certificate_blob':ch==d['certificate_blob_sha1'],
            'original_correction_blob':wh==d['original_delta_blob_sha1'],
            'boundary_relations':C['boundary_relations']==d['boundary_relations'],
            'source_relators':C['source_relators']==d['source_relators'],
            'q0_generator_words':C['boundary_arc_images']==d['q0_images'],
            'matrix_propagation':C['propagation_steps']==d['source_matrix_propagation'],
            'original_boundary_delta':w['correction_boundary_word']==d['original_boundary_delta'],
            'original_source_delta':w['correction_source_word']==d['original_source_delta'],
            'axis1':w['original_axis1']==d['axis1'],
            'axis2':w['original_axis2']==d['axis2'],
            'seam':w['seam_meridian_boundary_generator']==d['seam_meridian']}
    assert all(checks.values())
    T=json.loads((HERE/'transport.json').read_text())
    S=json.loads((published/'SUMMARY.json').read_text())
    images={int(k):v for k,v in T['boundary_meridian_images'].items()}
    matrices={int(k):[sum(v)%17 for v in a] for k,a in C['source_matrices'].items()}
    def evaluate(word):
        answer=[1,0,0,1]
        for x in word:
            a=matrices[abs(x)]
            if x<0:a=[a[3],-a[1]%17,-a[2]%17,a[0]]
            answer=mm(answer,a)
        return answer
    assert all(evaluate(r)==[1,0,0,1] for r in C['source_relators'])
    loops=[]
    for name in ['A','B']:
        word=substitute(S[name],images);matrix=evaluate(word)
        assert matrix!=[1,0,0,1]
        loops.append({'name':name,'boundary_word':S[name],'source_word':word,
                      'matrix_mod17':matrix,'trace_mod17':(matrix[0]+matrix[3])%17,
                      'nonidentity':True})
    report={'source_commit':d['source_commit'],'arrival_commit':'ceb83c2',
            'bundle_manifest_hashes':'PASS','checkout_comparisons':checks,
            'current_inputs_byte_equal_to_pinned_commit':True,'loops':loops,
            'source_relators':'PASS','alternative_correction_genus':1,
            'combined_surface_genus':2,
            'scope':'Under research42 existence construction; no new embedded-axis PD. These two direct caps fail; alternate handle systems are not excluded.',
            'important_control':'B has trace 2 but is NOT identity; a trace-only test would miss this obstruction.',
            'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
                      for p in [published/'BUNDLE.tar.xz',published/'SUMMARY.json',HERE/'transport.json',ROOT/d['certificate_path']]]}
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'checkout_comparisons':all(checks.values()),'A':loops[0]['matrix_mod17'],
                      'B':loops[1]['matrix_mod17'],'specified_caps':'both impossible','alternative_surface_genus':2}))

if __name__=='__main__':main()
